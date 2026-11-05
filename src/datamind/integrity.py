"""Validação offline, sem estimar parâmetros nem treinar."""
import ast
import csv
import hashlib
import json
import math
from pathlib import Path

PANEL = ["QRS_Dur_Global","RR_Mean_Global","QRS_Dur_V1","R_Amp_V1","S_Amp_V1","QRS_Dur_V6","R_Amp_V6","S_Amp_V6"]
MISSING = {"", "nan", "na", "null"}
def missing(value):
    return value.strip().lower() in MISSING
def verify_hashes(root):
    manifest = json.loads((root/"reports/phase3/entradas.json").read_text(encoding="utf-8"))
    for name, info in manifest.items():
        data = (root/"data/raw/phase3"/name).read_bytes()
        if hashlib.sha256(data).hexdigest() != info["sha256"]:
            raise ValueError("Hash divergente: "+name)
    return len(manifest)
def unique(rows, key):
    result = {}
    for row in rows:
        if not row[key] or row[key] in result:
            raise ValueError("ID vazio ou repetido: "+key)
        result[row[key]] = row
    return result
def disjoint_patients(meta):
    groups = {}
    for row in meta:
        patient = row["patient_id"]
        if not patient:
            raise ValueError("Paciente vazio")
        fold = int(row["strat_fold"])
        if fold not in range(1,11):
            raise ValueError("Fold inválido")
        if patient in groups and groups[patient] != fold:
            raise ValueError("Vazamento de paciente")
        groups[patient] = fold
def audit(root):
    n_hashes = verify_hashes(root)
    with (root/"data/raw/phase3/ptbxl_database.csv").open(encoding="utf-8") as f:
        meta = list(csv.DictReader(f))
    index = unique(meta,"ecg_id")
    disjoint_patients(meta)
    result = {"source_hashes":n_hashes,"partitions":{}}
    for name, folds in [("train",range(1,9)),("validation",[9]),("test",[10])]:
        rows = [r for r in meta if int(r["strat_fold"]) in folds]
        result["partitions"][name] = {
            "exams":len(rows),"patients":len({r["patient_id"] for r in rows}),
            "positive":sum("CRBBB" in ast.literal_eval(r["scp_codes"]) for r in rows),
            "positive_patients":len({r["patient_id"] for r in rows if "CRBBB" in ast.literal_eval(r["scp_codes"])}),
            "complete531":0,"complete8":0,"complete531_positive":0,"complete8_positive":0,
            "CRBBB_likelihoods":{}}
        out=result["partitions"][name]
        for r in rows:
            codes=ast.literal_eval(r["scp_codes"])
            if "CRBBB" in codes:
                k=str(codes["CRBBB"])
                out["CRBBB_likelihoods"][k]=out["CRBBB_likelihoods"].get(k,0)+1
    seen=set()
    invalid=0
    with (root/"data/raw/phase3/ecgdeli_features.csv").open(encoding="utf-8") as f:
        reader=csv.DictReader(f)
        features=[k for k in reader.fieldnames if k!="ecg_id" and not k.startswith("Unnamed")]
        if len(features)!=531 or not set(PANEL)<=set(features):
            raise ValueError("Esquema inesperado")
        for r in reader:
            key=r["ecg_id"]
            if key in seen or key not in index:
                raise ValueError("Join não é um para um")
            seen.add(key)
            for k in features:
                if not missing(r[k]):
                    try:
                        if not math.isfinite(float(r[k])): invalid+=1
                    except ValueError:
                        invalid+=1
            m=index[key]
            part="train" if int(m["strat_fold"])<=8 else ("validation" if m["strat_fold"]=="9" else "test")
            out=result["partitions"][part]
            positive="CRBBB" in ast.literal_eval(m["scp_codes"])
            for suffix,cols in [("531",features),("8",PANEL)]:
                complete=all(not missing(r[k]) for k in cols)
                out["complete"+suffix]+=complete
                out["complete"+suffix+"_positive"]+=complete and positive
    if seen!=set(index) or invalid:
        raise ValueError("IDs ausentes ou números inválidos")
    result["numeric_invalid_cells"]=invalid
    result["feature_count"]=len(features)
    result["panel"]=PANEL
    return result
