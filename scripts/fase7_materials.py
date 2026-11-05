
"""Render only frozen aggregate results; no model imports, fitting or predictions."""
from pathlib import Path
import json, hashlib, csv, sys, subprocess
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
def read(p): return json.loads((ROOT/p).read_text(encoding="utf-8-sig"))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks={}
for name in ["reports/phase5/run001/freeze.json","reports/phase6/final001/delivery_manifest.json"]:
    entries=read(name)["files"]
    assert all(sha(ROOT/p)==h for p,h in entries.items()), name
    checks[name]=len(entries)
m=read("reports/phase6/final001/metrics.json")
v=read("reports/phase5/run001/evaluation.json")["validation"]
out=ROOT/"artigo/figuras";out.mkdir(parents=True,exist_ok=True)
tab=ROOT/"artigo/tabelas";tab.mkdir(exist_ok=True)
plt.rcParams.update({"font.size":10,"svg.fonttype":"none","axes.spines.top":False,"axes.spines.right":False})
def save(fig,name,source):
    fig.text(.01,.012,source,fontsize=7)
    fig.savefig(out/(name+".png"),dpi=180,bbox_inches="tight")
    fig.savefig(out/(name+".svg"),bbox_inches="tight")
    fig.savefig(out/(name+".pdf"),bbox_inches="tight")
    plt.close(fig)
arms=["B0","E1","E2-C","E2","E2-fallback","E3","E3-I","Hybrid"]
headers=["Estratégia","Exames","Pacientes","Positivos","Brier","IC95% Brier","ROC-AUC","AP","Sensibilidade","Especificidade","Limiar fold 9"]
rows=[]
for a in arms:
    d=m["overall"][a];ci=m["bootstrap"]["metrics"][a]["brier"]
    rows.append([a,d["n"],d["patients"],d["positive"],f'{d["brier"]:.6f}',f'[{ci["low"]:.6f}; {ci["high"]:.6f}]',f'{d["roc_auc"]:.6f}',f'{d["average_precision"]:.6f}',f'{d["sensitivity"]:.4f}',f'{d["specificity"]:.4f}',str(d.get("threshold_from_fold9","—"))])
with (tab/"metricas.csv").open("w",newline="",encoding="utf-8") as f:
    writer=csv.writer(f);writer.writerow(headers);writer.writerows(rows)
md="| "+" | ".join(headers)+" |\n|"+"|".join(["---"]*len(headers))+"|\n"
md+="".join("| "+" | ".join(map(str,r))+" |\n" for r in rows)
md+="\nFonte: metrics.json overall e bootstrap.metrics.*.brier. E1 é condicional aos completos; não ordenar seu Brier com o da população integral. Sensibilidade/especificidade usam overall (limiares congelados), não os campos legados a 0,5. IC de Brier: bootstrap por paciente, 2.000 réplicas.\n"
(tab/"metricas.md").write_text(md,encoding="utf-8")
comparison="|Estratégia|Brier fold 9|Brier fold 10|\n|---|---:|---:|\n"
for a in arms:comparison+=f'|{a}|{v["overall"][a]["brier"]:.6f}|{m["overall"][a]["brier"]:.6f}|\n'
(tab/"folds.md").write_text(comparison,encoding="utf-8")
fig,ax=plt.subplots(figsize=(10,6));ax.axis("off")
boxes=[(.5,.88,"PTB-XL / PTB-XL+\n21.799 exames · 18.869 pacientes"),
(.18,.55,"Treino: folds 1–8\n17.418 exames / 15.023 pacientes\n432 exames positivos"),
(.5,.55,"Validação: fold 9\n2.183 exames / 1.942 pacientes\n55 exames positivos"),
(.82,.55,"Teste: fold 10\n2.198 exames / 1.904 pacientes\n54 exames positivos / 45 pacientes"),
(.48,.19,"531 medidas completas\n1.088 exames / 1.021 pacientes\n35 exames positivos"),
(.87,.19,"Medidas incompletas\n1.110 exames / 1.013 pacientes\n19 exames positivos")]
for x,y,t in boxes:ax.text(x,y,t,ha="center",va="center",fontsize=9,bbox=dict(boxstyle="round,pad=.5",fc="#edf3f8",ec="#47718d"))
for start,end in [((.5,.79),(.18,.65)),((.5,.79),(.5,.65)),((.5,.79),(.82,.65)),((.82,.44),(.48,.29)),((.82,.44),(.87,.29))]:
    ax.annotate("",xy=end,xytext=start,arrowprops=dict(arrowstyle="->"))
ax.text(.02,.05,"Partições sem pacientes compartilhados. Dentro do teste, 130 pacientes têm exames nos dois estratos.\nContagens de pacientes dos estratos não são aditivas.",fontsize=9)
save(fig,"01_fluxograma","Fonte: reports/phase4/preflight.json; phase6/final001/composition.json e metrics.json.")
fig,ax=plt.subplots(figsize=(10,4.5))
x=list(range(len(arms)))
ax.bar([i-.18 for i in x],[m["overall"][a]["coverage"]*100 for a in arms],.36,label="Exames (N=2.198)")
ax.bar([i+.18 for i in x],[m["overall"][a]["positive_coverage"]*100 for a in arms],.36,label="Positivos (N=54)",color="#d68a39")
ax.set(xticks=x,xticklabels=arms,ylim=(0,115),ylabel="Cobertura (%)")
ax.text(1,70,"49,50% / 64,81%",ha="center",fontsize=9)
ax.legend(loc="upper left",bbox_to_anchor=(0,1.15),ncol=2)
save(fig,"02_cobertura","Fonte: phase6/final001/metrics.json → overall. E2-fallback: nenhuma chamada ao fallback no teste.")
fig,ax=plt.subplots(figsize=(9,4))
p=m["primary"]
items=[("Primário: E3 − E2-fallback",p["delta_brier"],p["CI95"])]
for k in ["Hybrid minus E2-fallback","E3-I minus E3"]:
    d=m["paired_secondary"][k]
    ci=m["bootstrap"]["paired_brier"][k]
    items.append(("Secundário: "+k.replace(" minus "," − "),d["delta_brier"],ci))
for i,(name,val,ci) in enumerate(items):
    ax.errorbar(val,i,xerr=[[val-ci["low"]],[ci["high"]-val]],fmt="o",capsize=5,color="#1f5e83" if i==0 else "#777777")
ax.axvline(0,color="black",lw=1);ax.set(yticks=range(3),yticklabels=[i[0] for i in items],xlabel="Diferença de Brier (adimensional); menor favorece a primeira estratégia",xlim=(-.0032,.0032),ylim=(2.5,-.5))
fig.tight_layout(rect=(0,.08,1,1))
save(fig,"03_brier_pareado","Fonte: metrics.json → primary / paired_secondary / bootstrap.paired_brier; N=2.198 exames, 1.904 pacientes; IC95% agrupado.")
fig,axs=plt.subplots(1,3,figsize=(12,4.8))
for ax,a in zip(axs,["E2-fallback","E3","Hybrid"]):
    bins=m["overall"][a]["calibration"]["bins"]
    ax.plot([0,1],[0,1],"--",color="gray",lw=1)
    for i,b in enumerate(bins):
        ax.scatter(b["mean_p"],b["observed"],s=40)
        ax.annotate(str(i+1),(b["mean_p"],b["observed"]),xytext=(3,5+12*(i==1)),textcoords="offset points",fontsize=8)
    ax.set(title=a,xlim=(-.02,1.02),ylim=(-.02,1.02),xlabel="Probabilidade média",ylabel="Fração observada de CRBBB")
    ax.text(0,-.30,"Faixas: n / positivos\n"+"; ".join(f'{i+1}: {b["n"]}/{b["positive"]}' for i,b in enumerate(bins)),transform=ax.transAxes,fontsize=7,wrap=True)
fig.subplots_adjust(bottom=.30,wspace=.35)
save(fig,"04_calibracao","Fonte: metrics.json → overall.*.calibration.bins; N=2.198. Faixas fixas: [0;0,02;0,05;0,10;0,20;1]. Descritivo, sem novos ajustes/IC.")
fig,ax=plt.subplots(figsize=(8,4.5))
vals=[22/1137*100,33/1046*100,35/1088*100,19/1110*100]
ax.bar(range(4),vals,color=["#47718d","#c58c52"]*2)
for i,(val,label) in enumerate(zip(vals,["22/1.137","33/1.046","35/1.088","19/1.110"])):ax.text(i,val+.12,label,ha="center")
ax.set(xticks=range(4),xticklabels=["Fold 9\nCompletos","Fold 9\nIncompletos","Fold 10\nCompletos","Fold 10\nIncompletos"],ylim=(0,5),ylabel="Exames com anotação CRBBB (%)")
fig.subplots_adjust(bottom=.24)
save(fig,"05_composicao","Fonte: phase5/run001/composition.json e phase6/final001/composition.json. Descritivo; pacientes podem contribuir a ambos os estratos.")
report=ROOT/"reports/phase7"
report.mkdir(exist_ok=True)
(report/"verification.json").write_text(json.dumps({"frozen_hashes_checked":checks,"new_predictions":0,"new_training":0,"sources":["reports/phase6/final001/metrics.json","reports/phase5/run001/evaluation.json"],"python":sys.version,"matplotlib":matplotlib.__version__},indent=2),encoding="utf-8")
(report/"requirements-render.lock").write_text(subprocess.check_output([sys.executable,"-m","pip","freeze"],text=True),encoding="utf-8")
print("Frozen files verified; figures and tables rendered from existing aggregates.")
