"""Auditoria descritiva da Fase 3. Executar sem argumentos para usar o cache."""
import argparse
import ast
import csv
import hashlib
import io
import json
import struct
import urllib.request
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data/raw/phase3"
OUT = ROOT / "reports/phase3"
PTB = "https://physionet.org/files/ptb-xl/1.0.3/"
PLUS = "https://physionet.org/files/ptb-xl-plus/1.0.1/"
ZEN = "https://zenodo.org/records/3765780/files/data.zip?download=1"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main(download):
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    def get(name, url, byte_range=None):
        path = CACHE / name
        if not path.exists():
            if not download:
                raise FileNotFoundError(f"Cache ausente: {name}")
            headers = {"Range":byte_range} if byte_range else {}
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=90) as response:
                if byte_range and response.status != 206:
                    raise ValueError("Servidor não confirmou leitura parcial")
                body = response.read(70_000_001)
                if len(body)>70_000_000:
                    raise ValueError("Limite de 70 MB excedido")
                log = {"url":url, "status":response.status,"final_url":response.url,"range":byte_range,"bytes":len(body),"sha256":sha(body)}
            path.write_bytes(body)
            with (OUT/"acesso.jsonl").open("a",encoding="utf-8") as f:
                f.write(json.dumps(log)+"\n")
        body = path.read_bytes()
        manifest[name] = {"bytes":len(body),"sha256":sha(body),"url":url}
        return body
    def records(body):
        return csv.DictReader(io.StringIO(body.decode("utf-8-sig")))
    meta = list(records(get("ptbxl_database.csv", PTB+"ptbxl_database.csv")))
    dictionary = list(records(get("scp_statements.csv", PTB+"scp_statements.csv")))
    get("license_ptb.txt",PTB+"LICENSE.txt")
    get("license_plus.txt",PLUS+"LICENSE.txt")
    get("feature_description.csv", PLUS+"features/feature_description.csv")
    feature_data=get("ecgdeli_features.csv",PLUS+"features/ecgdeli_features.csv")
    index={r["ecg_id"]:r for r in meta}
    patients=defaultdict(set)
    for r in meta:
        patients[r["patient_id"]].add(r["strat_fold"])
    def positive(r):
        return "CRBBB" in ast.literal_eval(r["scp_codes"])
    development={k:r for k,r in index.items() if int(r["strat_fold"])<=8}
    features=records(feature_data)
    fields=list(features.fieldnames)
    idcol="ecg_id"
    measurements=[k for k in fields if k!=idcol and not k.startswith("Unnamed")]
    compact = {"QRS_Dur_Global","RR_Mean_Global","QRS_Dur_V1","R_Amp_V1","S_Amp_V1","QRS_Dur_V6","R_Amp_V6","S_Amp_V6"}
    assert compact.issubset(measurements)
    counts=Counter()
    missing=Counter()
    seen=set()
    signatures=Counter()
    for row in features:
        key=row[idcol]
        if key in seen: counts["repeated_feature_ids"]+=1
        seen.add(key)
        if key not in development:continue
        blank=[k for k in measurements if row[k].strip().lower() in {"","nan","na","null"}]
        missing.update(blank)
        signatures[sha("\x1f".join(row[k] for k in measurements).encode())]+=1
        counts["compact_complete"]+=compact.isdisjoint(blank)
        counts["compact_complete_positive"]+=compact.isdisjoint(blank) and positive(index[key])
        counts["joined_dev"]+=1
        counts["all_features_complete"]+=not blank
        counts["positive_complete"]+=not blank and positive(index[key])
        counts["positive_joined"]+=positive(index[key])
    dev=list(development.values())
    waveform=[]
    for row in sorted(dev,key=lambda r:sha(r['ecg_id'].encode()))[:3]:
        base=row["filename_lr"]
        header=get(base.split("/")[-1]+".hea",PTB+base+".hea").decode()
        body=get(base.split("/")[-1]+".dat",PTB+base+".dat")
        waveform.append({"header":header.splitlines()[0],"bytes":len(body),"sha256":sha(body)})
    record=json.loads(get("zenodo.json","https://zenodo.org/api/records/3765780"))
    archive=zipfile.ZipFile(io.BytesIO(get("code_tail.bin",ZEN,"bytes=-65536")))
    annotation={}
    for member in archive.namelist():
        if "/annotations/" in member and member.endswith(".csv"):
            annotation[Path(member).stem]=list(records(archive.read(member)))
    gold=annotation["gold_standard"]
    diffs={}
    for name,table in annotation.items():
        if name=="dnn":continue
        assert len(table)==len(gold)
        diffs[name]={k:sum(a[k]!=b[k] for a,b in zip(gold,table)) for k in gold[0]}
    stats={
        "ptb":{"exams":len(meta),"ecg_ids":len(index),"patients":len(patients),"patients_multiple_folds":sum(len(x)>1 for x in patients.values()),"repeated_patients":sum(v>1 for v in Counter(r["patient_id"] for r in meta).values()),"dev_exams":len(dev),"dev_patients":len({r["patient_id"] for r in dev}),"dev_CRBBB":sum(positive(r) for r in dev),"dev_CRBBB_patients":len({r["patient_id"] for r in dev if positive(r)}),"dev_devices":dict(Counter(r["device"] for r in dev)),"dev_sites":dict(Counter(r["site"] for r in dev)),"dev_years":dict(Counter(r["recording_date"][:4] for r in dev)),"sample_waveforms":waveform,"CRBBB_dictionary":[r for r in dictionary if "CRBBB" in r.values()]},
        "plus":{"features":len(measurements),"unique_ecg_ids":len(seen),"meta_ids_without_features":len(set(index)-seen),"extra_ids":len(seen-set(index)),"dev":dict(counts),"dev_duplicate_numeric_text_profiles_excess":sum(v-1 for v in signatures.values()),"dev_missing_by_feature":dict(missing)},
        "code_test":{"zip_bytes":record["files"][0]["size"],"license":record["metadata"]["license"],"members":{i.filename:i.file_size for i in archive.infolist()},"reference_n":len(gold),"reference_positive":{k:sum(r[k].strip().lower() in {"true","1","1.0"} for r in gold) for k in gold[0]},"discordant_vs_reference":diffs,"dnn_columns":list(annotation["dnn"][0]),"dnn_n":len(annotation["dnn"]),"readme":archive.read("data/README.md").decode()[:0]},
    }
    del stats["code_test"]["readme"]
    upstream = "https://raw.githubusercontent.com/antonior92/automatic-ecg-diagnosis/403934867cea25a85b54faca025ac65b1ac18a45/"
    get("scores_readme.md", upstream+"dnn_predicts/README.md")
    get("upstream_license.txt", upstream+"LICENSE")
    scores = get("model.npy", upstream+"dnn_predicts/model.npy")
    assert scores.startswith(b"\x93NUMPY\x01\x00")
    end_header = 10 + int.from_bytes(scores[8:10],"little")
    header = ast.literal_eval(scores[10:end_header].decode("ascii").strip())
    assert header["shape"] == (len(gold),6) and header["descr"] == "<f4"
    values = struct.unpack("<" + str(len(gold)*6) + "f",scores[end_header:])
    assert all(0 <= v <= 1 for v in values)
    stats["code_test"]["score_matrix"] = {"rows":len(gold),"columns":6,"nonbinary_cells":sum(0 < v < 1 for v in values),"format":header["descr"]}
    stats["plus"]["compact_panel"]=sorted(compact)
    stats["ptb"]["dev_device_support"]={}
    for device in stats["ptb"]["dev_devices"]:
        group=[r for r in dev if r["device"]==device]
        stats["ptb"]["dev_device_support"][device]={"n":len(group),"positive":sum(positive(r) for r in group),"sites":dict(Counter(r["site"] for r in group))}
    for name,obj in [("auditoria.json",stats),("entradas.json",manifest)]:
        (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding="utf-8")
    print(counts,stats["code_test"]["reference_positive"])
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--download",action="store_true")
    main(parser.parse_args().download)
