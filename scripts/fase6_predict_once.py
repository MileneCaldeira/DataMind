"""Uma única execução preditiva autorizada. Nunca alterar/retreinar os modelos."""
import os
os.environ["OMP_NUM_THREADS"]="1"
os.environ["MKL_NUM_THREADS"]="1"
os.environ["OPENBLAS_NUM_THREADS"]="1"
import ast,hashlib,json,subprocess,sys,platform,time
from datetime import datetime,timezone
from pathlib import Path
import joblib,numpy as np,pandas as pd
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from datamind.pilot import ARMS,whitelist,train_mask,predict_mask,combine
from datamind.integrity import PANEL,disjoint_patients
from datamind.final_eval import final_predict,claim
OLD=ROOT/"reports/phase5/run001"
OUT=ROOT/"reports/phase6/final001"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,obj):
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False),encoding="utf-8")
def main():
    OUT.mkdir(parents=True,exist_ok=False)
    checks={}
    # All controls and tests precede assembly of holdout labels/features.
    check=subprocess.run([sys.executable,"scripts/fase5_freeze.py","--check"],cwd=ROOT,capture_output=True,text=True)
    (OUT/"freeze_pre.log").write_text(check.stdout+check.stderr,encoding="utf-8")
    if check.returncode:raise RuntimeError("Freeze inválido")
    tests=subprocess.run([sys.executable,"-m","unittest","discover","-s","tests","-v"],cwd=ROOT,capture_output=True,text=True)
    (OUT/"tests_pre.log").write_text(tests.stdout+tests.stderr,encoding="utf-8")
    if tests.returncode:raise RuntimeError("Testes falharam")
    current=subprocess.check_output([sys.executable,"-m","pip","freeze"],text=True)
    if sorted(current.splitlines())!=sorted((OLD/"requirements.lock.txt").read_text().splitlines()):
        raise RuntimeError("Ambiente diverge")
    write(OUT/"environment.json",{"python":sys.version,"platform":platform.platform(),"pip_freeze":current,"threads":1})
    # Prior recorded prediction tables are restricted to 1..9.
    scans=[]
    for p in (ROOT/"reports").rglob("*.csv"):
        if OUT in p.parents:continue
        header=pd.read_csv(p,nrows=0)
        if "strat_fold" in header and any(c in header for c in [*ARMS,"C_0.01"]):
            folds=pd.read_csv(p,usecols=["strat_fold"]).strat_fold
            if folds.eq(10).any():raise RuntimeError("Previsões anteriores de 10 registradas")
            scans.append({"path":str(p.relative_to(ROOT)),"max_fold":int(folds.max()),"sha256":sha(p)})
    if not scans:raise RuntimeError("Sem evidência de previsões anteriores")
    previous=json.loads((OLD/"verification.json").read_text())
    if previous["fold10_predictions"]!=0:raise RuntimeError("Holdout já usado")
    meta=pd.read_csv(ROOT/"data/raw/phase3/ptbxl_database.csv")
    structural=meta[["ecg_id","patient_id","strat_fold"]]
    if structural.isna().any().any() or structural.ecg_id.duplicated().any():raise RuntimeError("IDs inválidos")
    disjoint_patients(structural.astype(str).to_dict("records"))
    feat=pd.read_csv(ROOT/"data/raw/phase3/ecgdeli_features.csv")
    cols=[c for c in feat if c!="ecg_id"]
    if feat.ecg_id.duplicated().any() or set(feat.ecg_id)!=set(meta.ecg_id):raise RuntimeError("Join inválido")
    if len(cols)!=531 or set(cols)!=set(whitelist(ROOT)):raise RuntimeError("Whitelist inválida")
    cfg=json.loads((OLD/"config.json").read_text())
    thresholds=json.loads((OLD/"thresholds.json").read_text())
    selected=json.loads((OLD/"selection.json").read_text())["selected"]
    models={}
    train=meta[meta.strat_fold.le(8)]
    devfeat=train[["ecg_id"]].merge(feat,on="ecg_id",validate="one_to_one")
    train=train.reset_index(drop=True)
    train["complete"]=devfeat[cols].notna().all(axis=1)
    train["panel_complete"]=devfeat[PANEL].notna().all(axis=1)
    for name in [*ARMS,"E1_C1","E2-C_C1"]:
        model=joblib.load(OLD/"models"/(name+".joblib"))
        arm=name.removesuffix("_C1")
        expected_C=1 if name.endswith("_C1") else selected[arm]
        expected_cols=PANEL if arm in ["E2","E2-C"] else cols
        if model.C!=expected_C or model.columns!=expected_cols or model.cfg!=cfg:raise RuntimeError("Modelo/configuração divergentes")
        tm=train_mask(train,arm)
        if model.train_ids_!=set(train.loc[tm,"ecg_id"]) or model.train_patients_!=set(train.loc[tm,"patient_id"]):raise RuntimeError("Treino diverge")
        if set(meta.loc[meta.strat_fold.eq(10),"patient_id"])&model.train_patients_:raise RuntimeError("Overlap paciente")
        models[name]=model
    if set(thresholds)!={*models,"B0","E2-fallback","Hybrid"}:raise RuntimeError("Limiar incompleto")
    if not all(t is not None and np.isfinite(t) for t in thresholds.values()):raise RuntimeError("Limiar inválido")
    val=pd.read_csv(OLD/"validation.csv")
    if not val.panel_complete.all() or not np.allclose(val.E2,val["E2-fallback"],atol=0,rtol=0):raise RuntimeError("Fallback 9 inesperado")
    before={str(p.relative_to(ROOT)):sha(p) for p in [OLD/"freeze.json",*list((OLD/"models").glob("*")),OLD/"thresholds.json",
         ROOT/"scripts/fase6_predict_once.py",ROOT/"src/datamind/final_eval.py",ROOT/"docs/fase6_plano_execucao.md"]}
    checks.update({"passed":True,"utc":datetime.now(timezone.utc).isoformat(),"prior_prediction_scan":scans,
      "previous_recorded_fold10_predictions":0,"fold9_fallback_count":0,"joins":"1:1 exact ID sets",
      "patient_folds_disjoint":True,"whitelist_count":531,"test_outcomes_used_to_change_protocol":False,
      "fold9_interpretation_exploratory":True,"pre_execution_hashes":before})
    write(OUT/"preflight.json",checks)
    print("CONTROLS PASSED. Beginning one authorized prediction execution.",flush=True)
    claim(OUT/"PREDICTION_STARTED.lock")
    start=time.time()
    held=meta.loc[meta.strat_fold.eq(10)].copy().sort_values("ecg_id").reset_index(drop=True)
    joined=held[["ecg_id"]].merge(feat,on="ecg_id",validate="one_to_one",sort=False)
    X=joined[cols].astype(float)
    if np.isinf(X.to_numpy()).any():raise RuntimeError("Inf")
    held["y"]=held.scp_codes.map(lambda s:int("CRBBB" in ast.literal_eval(s)))
    held["complete"]=X.notna().all(axis=1)
    held["panel_complete"]=X[PANEL].notna().all(axis=1)
    held=held[["ecg_id","patient_id","strat_fold","y","complete","panel_complete","age","sex","device","site"]]
    B0=json.loads((OLD/"models/B0.json").read_text())["prevalence"]
    preds={"B0":np.full(len(held),B0)}
    calls=[]
    for name,model in models.items():
        mask=predict_mask(held,name.removesuffix("_C1"))
        # Exactly one call per saved pipeline on its eligible holdout support.
        p=np.full(len(held),np.nan)
        call={"model":name,"n":int(mask.sum()),"utc":datetime.now(timezone.utc).isoformat()}
        with (OUT/"prediction_calls.jsonl").open("a",encoding="utf-8") as f:f.write(json.dumps(call)+"\n")
        p[mask]=final_predict(model,held.loc[mask],X.loc[mask])
        preds[name]=p
        pd.DataFrame({"ecg_id":held.ecg_id,"probability":p}).to_csv(OUT/("scores_"+name+".csv"),index=False)
        calls.append(call)
    preds=combine(preds)
    if not np.isfinite(preds["E3"]).all() or not np.isfinite(preds["E2-fallback"]).all():raise RuntimeError("Primary population mismatch")
    for name,p in preds.items():held[name]=p
    held.to_csv(OUT/"predictions.csv",index=False)
    write(OUT/"prediction_receipt.json",{"complete":True,"execution_count":1,"model_calls":calls,
      "n":len(held),"patients":int(held.patient_id.nunique()),"positive":int(held.y.sum()),
      "fallback_count":int((~held.panel_complete).sum()),"fallback_positive":int(held.loc[~held.panel_complete,"y"].sum()),
      "primary_same_population":True,"seconds":time.time()-start,"predictions_sha256":sha(OUT/"predictions.csv")})
    if any(sha(ROOT/p)!=h for p,h in before.items()):raise RuntimeError("Frozen inputs altered")
    print("Predictions saved. Do not rerun. Metrics must use saved CSV.",flush=True)
if __name__=="__main__":
    with threadpool_limits(limits=1):main()
