
"""Audit only: saved files and manuscript, no model/metric/fit execution."""
from pathlib import Path
import json,csv,hashlib,re,sys
R=Path(__file__).resolve().parents[1]
def j(p):return json.loads((R/p).read_text(encoding="utf-8-sig"))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
base=j("reports/phase8/baseline_hashes.json")
for p,h in {**base["files"],**base["manifests"]}.items():assert sha(R/p)==h,p
entries=j("reports/phase3/entradas.json")
for name,info in entries.items():assert sha(R/"data/raw/phase3"/name)==info["sha256"],name
def rows(p):
    with (R/p).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
meta=rows("data/raw/phase3/ptbxl_database.csv")
ids={r["ecg_id"] for r in meta};assert len(ids)==len(meta)==21799
patients={}
for row in meta:
    pat=row["patient_id"];fold=row["strat_fold"]
    assert pat not in patients or patients[pat]==fold
    patients[pat]=fold
with (R/"data/raw/phase3/ecgdeli_features.csv").open(encoding="utf-8-sig",newline="") as f:
    rd=csv.DictReader(f);columns=set(rd.fieldnames)-{"ecg_id"}
    fids=[row["ecg_id"] for row in rd]
assert len(fids)==len(set(fids)) and set(fids)==ids and len(columns)==531
desc=rows("data/raw/phase3/feature_description.csv")
expanded=set()
for row in desc:
    if not row["ecgdeli_feature"]:continue
    names=[row["id"][:-1]+l for l in ["I","II","III","aVR","aVL","aVF","V1","V2","V3","V4","V5","V6"]] if row["id"].endswith("_X") else [row["id"]]
    expanded.update(n+s for n in names for s in ["","_iqr","_count"])
assert expanded==columns
pred=rows("reports/phase6/final001/predictions.csv")
lookup={r["ecg_id"]:r for r in pred};assert len(lookup)==len(pred)==2198
matched={}
for p in sorted((R/"reports/phase6/final001").glob("scores_*.csv")):
    arm=p.stem[len("scores_"):]
    rr=rows(p.relative_to(R))
    assert len(rr)==len({r["ecg_id"] for r in rr})
    for row in rr:assert row["probability"]==lookup[row["ecg_id"]][arm],(arm,row["ecg_id"])
    assert len(rr)==len(pred)
    assert sum(bool(x['probability']) for x in rr)==sum(bool(x[arm]) for x in pred)
    matched[arm]={"rows":len(rr),"nonmissing":sum(bool(x['probability']) for x in rr)}
assert all(x["E2"]==x["E2-fallback"] and x["panel_complete"]=="True" for x in pred)
# Reuse only the previously reviewed, standard-library document checker, targeting v2.
old=(R/"scripts/fase7_verify.py").read_text(encoding="utf-8")
code=old.replace("artigo/manuscrito_v1.md","artigo/manuscrito_v2.md")
exec(compile(code,"phase7_document_checker_for_v2","exec"),{"__file__":str(R/"scripts/fase7_verify.py")})
m=j("reports/phase6/final001/metrics.json")
v2=(R/"artigo/manuscrito_v2.md").read_text(encoding="utf-8")
def pt(x):return f"{x:.6f}".replace(".",",").replace("-","−")
for key in ["E1 minus E2-C","E1_C1 minus E2-C_C1","E2-C minus E2"]:
    d=m["paired_secondary"][key];ci=m["bootstrap"]["paired_brier"][key]
    for val in [d["delta_brier"],ci["low"],ci["high"]]:assert pt(val) in v2,(key,val)
for a,label in [("B0","B0"),("E2-C","E2-C"),("E2-fallback","E2 / E2-fallback"),("E3","E3"),("E3-I","E3-I"),("Hybrid","Híbrida")]:
    d=m["overall"][a]
    line=f'|{label}|2.198|{pt(d["brier"])}|{pt(d["roc_auc"])}|{pt(d["average_precision"])}|'
    assert line in v2,line
assert "população completa|1.088" not in v2
required=["reports/fase8_parecer_cientifico.md","reports/fase8_auditoria_estatistica.md","docs/fase8_originalidade.md","artigo/manuscrito_v2.md","reports/fase8_pendencias_especialistas.md","docs/guia_defesa_pesquisa.md","reports/fase8_decisao.md"]
for p in required:assert (R/p).is_file()
out={"status":"PASS","date":"2026-11-05","previous_unique_files_checked":len(base["files"]),"previous_manifests_checked":len(base["manifests"]),"raw_hashes_checked":len(entries),"join":"1:1; 21799 IDs","patients_disjoint":True,"saved_probabilities_exact_text_match":matched,"primary_recomputed":False,"new_predictions":0,"new_training":0,"new_calibration_fits":0,"new_bootstrap":0,"v1_unchanged":True,"figures_unchanged":True,"main_table_and_controls_reconciled":True,"deliverables":required,"python":sys.version}
(R/"reports/phase8/verification.json").write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding="utf-8")
print(json.dumps(out,ensure_ascii=True))
