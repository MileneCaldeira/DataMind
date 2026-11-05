
"""Document-only checks; no model imports, metric calculation or previous-file writes."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text(encoding="utf-8-sig"))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifests=["reports/phase5/run001/freeze.json","reports/phase6/final001/delivery_manifest.json","reports/phase7/manifest.json","reports/phase8/manifest.json"]
files={}
for name in manifests:files.update(read(name)["files"])
for name,digest in files.items():assert sha(R/name)==digest,name
m=read("reports/phase6/final001/metrics.json")
assert m["primary"]["n"]==2198 and m["primary"]["patients"]==1904 and m["primary"]["positive"]==54
assert read("reports/phase4/preflight.json")["partitions"]["test"]["positive_patients"]==45
assert m["overall"]["E1"]["n"]==1088 and m["overall"]["E1"]["positive"]==35
def pt(x):return f"{x:.6f}".replace(".",",").replace("-","−")
summary=(R/"reports/fase9_resumo_pesquisa.md").read_text(encoding="utf-8")
abstract=summary.split("## Resumo científico\n",1)[1].split("\n## ",1)[0]
words=len(abstract.split());assert words<=250,words
simple=summary.split("## Síntese acessível",1)[1].split("\n## Cinco",1)[0]
slides=(R/"apresentacao/fase9_apresentacao.md").read_text(encoding="utf-8")
assert len(re.findall(r"^# Slide [1-5] —",slides,re.M))==5
for text in [abstract,slides,(R/"docs/fase9_revisao_estatistica.md").read_text(encoding="utf-8")]:
    for val in [m["primary"]["delta_brier"],m["primary"]["CI95"]["low"],m["primary"]["CI95"]["high"],m["overall"]["E3"]["brier"],m["overall"]["E2-fallback"]["brier"],m["overall"]["Hybrid"]["brier"]]:
        assert pt(val) in text,pt(val)
for key in ["coverage","positive_coverage"]:
    value=f'{m["overall"]["E1"][key]*100:.2f}'.replace(".",",")+"%"
    assert value in abstract and value in slides
matrix=(R/"reports/fase9_matriz_feedback.md").read_text(encoding="utf-8")
assert len([line for line in matrix.splitlines() if line.startswith("|")])==2
required=["reports/fase9_resumo_pesquisa.md","docs/fase9_revisao_clinica.md","docs/fase9_revisao_estatistica.md","docs/fase9_revisao_editorial.md","reports/fase9_matriz_feedback.md","apresentacao/fase9_apresentacao.md","reports/fase9_pendencias.md"]
for name in required:
    p=R/name;assert p.is_file()
    for link in re.findall(r"\]\(([^)]+)\)",p.read_text(encoding="utf-8")):
        if not link.startswith("http"):assert (p.parent/link).exists(),(name,link)
out=R/"reports/phase9";out.mkdir(exist_ok=True)
result={"date":"2026-11-05","status":"PASS","previous_files_verified":len(files),"previous_manifests":len(manifests),"v2_sha256":sha(R/"artigo/manuscrito_v2.md"),"abstract_words":words,"plain_summary_words":len(simple.split()),"slides":5,"human_comments":0,"new_predictions":0,"new_training":0,"new_statistical_analyses":0,"messages_sent":0,"results_source":"reports/phase6/final001/metrics.json"}
(out/"verification.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
outputs=[R/p for p in required]+[R/"scripts/fase9_verify.py",out/"verification.json"]
(out/"manifest.json").write_text(json.dumps({"phase":9,"files":{p.relative_to(R).as_posix():sha(p) for p in outputs},"prior_manifest_hashes":{p:sha(R/p) for p in manifests}},indent=2),encoding="utf-8")
print(json.dumps(result,ensure_ascii=True))
