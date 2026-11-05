
"""Read-only verification of original artifacts and manuscript numbers. No ML."""
from pathlib import Path
import json,hashlib,re,csv
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding="utf-8-sig"))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for manifest in ["reports/phase5/run001/freeze.json","reports/phase6/final001/delivery_manifest.json"]:
    for p,h in read(manifest)["files"].items():assert digest(R/p)==h,p
m=read("reports/phase6/final001/metrics.json")
v=read("reports/phase5/run001/evaluation.json")["validation"]
p=read("reports/phase4/preflight.json")["partitions"]
assert [(p[k]["exams"],p[k]["patients"],p[k]["positive"]) for k in ["train","validation","test"]]==[(17418,15023,432),(2183,1942,55),(2198,1904,54)]
assert p["test"]["positive_patients"]==45
assert p["test"]["complete531"]==1088 and p["test"]["complete531_positive"]==35
assert p["validation"]["complete531"]==1137 and p["validation"]["complete531_positive"]==22
c=read("reports/phase6/final001/composition.json")
assert c["complete"]["patients"]+c["incomplete"]["patients"]-c["all"]["patients"]==130
assert [c[k]["age_median_under90"] for k in ["complete","incomplete"]]==[62,64]
receipt=read("reports/phase6/final001/prediction_receipt.json")
assert receipt["execution_count"]==1 and len(receipt["model_calls"])==7
prior=read("reports/phase6/final001/verification.json")
assert prior["saved_probability_files_exact_match"] and prior["patient_disjoint"]
assert digest(R/"reports/phase6/final001/predictions.csv")==prior["predictions_sha256"]
text=(R/"artigo/manuscrito_v1.md").read_text(encoding="utf-8")
def pt(x,d=6):return f"{x:.{d}f}".replace(".",",").replace("-","−")
for a in ["B0","E1","E2-C","E2-fallback","E3","E3-I","Hybrid"]:
    for key in ["brier","roc_auc","average_precision"]:
        assert pt(m["overall"][a][key]) in text,(a,key)
for val in [m["primary"]["delta_brier"],m["primary"]["CI95"]["low"],m["primary"]["CI95"]["high"]]:assert pt(val) in text
for a in ["E2-fallback","E3"]:
    assert pt(v["overall"][a]["brier"]) in text
for a in ["E2-fallback","E3","Hybrid"]:
    assert pt(100*m["overall"][a]["specificity"],2)+"%" in text
    assert m["overall"][a]["sensitivity"]==1
for a in ["E2-fallback","E3","Hybrid"]:
    for key in ["intercept","slope"]:assert pt(m["overall"][a]["calibration"][key],3) in text
# Every decimal smaller than one in the manuscript must be a rounded existing result.
nums=[]
def collect(obj):
    if isinstance(obj,dict):
        for x in obj.values():collect(x)
    elif isinstance(obj,list):
        for x in obj:collect(x)
    elif isinstance(obj,(int,float)):nums.append(obj)
collect(m);collect(v)
for token in set(re.findall(r"[−+]?0,\d{3,6}",text)):
    precision=len(token.split(",")[1])
    normalized=token.lstrip("+")
    assert any(pt(n,precision)==normalized for n in nums),token
for target in re.findall(r"\]\(([^)]+)\)",text):
    if not target.startswith("http"):assert (R/"artigo"/target).exists(),target
print("PASS: frozen hashes, receipt, counts, rounded manuscript results and local links.")
