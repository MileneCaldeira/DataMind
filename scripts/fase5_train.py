"""Treino piloto offline. Saída nova obrigatória, nunca sobrescreve uma execução."""
import os
os.environ["OMP_NUM_THREADS"]="1"
os.environ["OPENBLAS_NUM_THREADS"]="1"
os.environ["MKL_NUM_THREADS"]="1"
import hashlib
import json
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import psutil
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from datamind.pilot import ARMS,GuardedModel,load_development,train_mask,predict_mask,choose_C,combine,threshold95,hash_ids
def write(path,obj):
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False),encoding="utf-8")
def main():
    cfg=json.loads((ROOT/"experiments/fase5.json").read_text())
    out=ROOT/cfg["output"]
    out.mkdir(parents=True,exist_ok=False)
    (out/"models").mkdir()
    start=time.time()
    logpath=out/"training.jsonl"
    def log(obj):
        obj["utc"]=datetime.now(timezone.utc).isoformat()
        with logpath.open("a",encoding="utf-8") as f:f.write(json.dumps(obj,allow_nan=False)+"\n")
        print(json.dumps(obj),flush=True)
    # Snapshot protocol, source and previous output hashes BEFORE any model fit.
    previous={}
    for base in ["data/raw","docs","reports","scripts","src","experiments","tests"]:
        for path in (ROOT/base).rglob("*"):
            if path.is_file() and out not in path.parents and "__pycache__" not in str(path) and not path.suffix==".pyc":
                previous[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    write(out/"before_hashes.json",previous)
    write(out/"config.json",cfg)
    freeze=subprocess.check_output([sys.executable,"-m","pip","freeze"],text=True)
    (out/"requirements.lock.txt").write_text(freeze,encoding="utf-8")
    write(out/"environment.json",{"python":sys.version,"platform":platform.platform(),"executable":sys.executable,
                                "ram_bytes":psutil.virtual_memory().total,"threads":cfg["threads"]})
    meta,X,audit=load_development(ROOT)
    write(out/"audit.json",audit)
    meta.to_csv(out/"cohorts.csv",index=False)
    dev=meta.strat_fold.le(8)
    val=meta.strat_fold.eq(9)
    m=meta[dev]; x=X[dev]
    selected={}
    grid_scores={}
    oof_fixed={}
    oof_selected={}
    oof_b0=np.full(len(m),np.nan)
    splitlogs=[]
    for fold in cfg["train_folds"]:
        tr=m.strat_fold.ne(fold).to_numpy()
        va=~tr
        oof_b0[va]=m.loc[tr,"y"].mean()
    for arm in ARMS:
        predictions={}
        for C in cfg["C_grid"]:
            pred=np.full(len(m),np.nan)
            for fold in cfg["train_folds"]:
                tr=m.strat_fold.ne(fold).to_numpy() & train_mask(m,arm)
                va=m.strat_fold.eq(fold).to_numpy() & predict_mask(m,arm)
                if set(m.loc[tr,"patient_id"]) & set(m.loc[va,"patient_id"]):raise ValueError("Overlap")
                t=time.time()
                model=GuardedModel(arm,C,cfg,list(X)).fit(m.loc[tr],x.loc[tr])
                pred[va]=model.predict(m.loc[va],x.loc[va])
                info={"stage":"CV","arm":arm,"C":C,"held_fold":fold,"seconds":time.time()-t,
                      "eval_n":int(va.sum()),"eval_id_hash":hash_ids(m.loc[va,"ecg_id"]),
                      "fit":model.fit_info_,"rss_bytes":psutil.Process().memory_info().rss}
                log(info)
                splitlogs.append(info)
            predictions[C]=pred
        scores={C:float(np.nanmean((p-m.y.to_numpy())**2)) for C,p in predictions.items()}
        best=choose_C(scores,cfg["tie_tolerance"])
        selected[arm]=best
        grid_scores[arm]=scores
        oof_fixed[arm]=predictions[cfg["fixed_C"]]
        oof_selected[arm]=predictions[best]
        # Retain ALL candidate OOF predictions for tuning audit.
        tab=m[["ecg_id","patient_id","strat_fold","y"]].copy()
        for C,p in predictions.items():tab["C_"+str(C)]=p
        tab.to_csv(out/("grid_"+arm+".csv"),index=False)
        log({"stage":"selected","arm":arm,"C":best,"scores":scores})
    for name,pred in [("oof_fixed",oof_fixed),("oof_selected",oof_selected)]:
        pred["B0"]=oof_b0
        tab=m.copy()
        for arm,p in combine(pred).items():tab[arm]=p
        tab.to_csv(out/(name+".csv"),index=False)
    write(out/"selection.json",{"selected":selected,"scores":grid_scores})
    mv=meta[val]; xv=X[val]
    preds={"B0":np.full(len(mv),m.y.mean())}
    final_fit={}
    for arm in ARMS:
        tr=train_mask(m,arm)
        va=predict_mask(mv,arm)
        t=time.time()
        model=GuardedModel(arm,selected[arm],cfg,list(X)).fit(m.loc[tr],x.loc[tr])
        pred=np.full(len(mv),np.nan)
        pred[va]=model.predict(mv.loc[va],xv.loc[va])
        preds[arm]=pred
        # Explicit in-sample fit diagnostic, not evaluation predictions.
        train_p=model.pipeline.predict_proba(x.loc[tr,model.columns])[:,1]
        final_fit[arm]={"C":selected[arm],"fit":model.fit_info_,
                       "apparent_train_brier":float(np.mean((train_p-m.loc[tr,"y"])**2))}
        joblib.dump(model,out/"models"/(arm+".joblib"),compress=3)
        log({"stage":"final_dev_fit","arm":arm,"seconds":time.time()-t,**final_fit[arm]})
    # Fixed C=1 controls for E1 and E2-C, independent of tuning.
    for arm in ["E1","E2-C"]:
        tr=train_mask(m,arm); va=predict_mask(mv,arm)
        model=GuardedModel(arm,1,cfg,list(X)).fit(m.loc[tr],x.loc[tr])
        p=np.full(len(mv),np.nan); p[va]=model.predict(mv.loc[va],xv.loc[va])
        preds[arm+"_C1"]=p
        joblib.dump(model,out/"models"/(arm+"_C1.joblib"),compress=3)
        log({"stage":"fixed_control","arm":arm,"fit":model.fit_info_})
    preds=combine(preds)
    tab=mv.copy()
    thresholds={}
    for arm,p in preds.items():
        tab[arm]=p
        mask=np.isfinite(p)
        thresholds[arm]=threshold95(mv.loc[mask,"y"],p[mask],cfg["target_specificity"])
    tab.to_csv(out/"validation.csv",index=False)
    write(out/"thresholds.json",thresholds)
    write(out/"final_fit.json",final_fit)
    write(out/"models"/"B0.json",{"prevalence":float(m.y.mean()),"train_ids_hash":hash_ids(m.ecg_id)})
    write(out/"runtime.json",{"seconds":time.time()-start,"peak_working_set_bytes":psutil.Process().memory_info().peak_wset,
                             "fold10_predictions":0,"max_prediction_fold":9,"fits_cv":len(splitlogs),"complete":True})
    log({"stage":"complete","seconds":time.time()-start})
if __name__=="__main__":
    with threadpool_limits(limits=1):main()
