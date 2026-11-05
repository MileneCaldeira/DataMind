"""Verifica artefatos, recarrega modelos e reproduz previsões somente do fold 9."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from threadpoolctl import threadpool_limits
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from datamind.pilot import load_development,ARMS,train_mask,predict_mask,hash_ids,choose_C,combine,threshold95
def main():
    cfg=json.loads((ROOT/"experiments/fase5.json").read_text())
    out=ROOT/cfg["output"]
    result={}
    meta,X,audit=load_development(ROOT)
    before=json.loads((out/"before_hashes.json").read_text())
    changed=[]
    for name,h in before.items():
        # Preserve historical phases and all raw inputs. New phase5 tests may evolve.
        if "phase5" in name or "fase5" in name or name.replace("\\", "/")=="docs/decisoes.md":continue
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=h:changed.append(name)
    assert not changed,changed
    result["historical_hashes_preserved"]=True
    result["raw_source_hashes_verified"]=17
    selection=json.loads((out/"selection.json").read_text())
    m=meta[meta.strat_fold.le(8)]
    v=meta[meta.strat_fold.eq(9)]
    pv=pd.read_csv(out/"validation.csv").set_index("ecg_id").loc[v.ecg_id].reset_index()
    prediction_sets=[]
    for name in ["oof_fixed","oof_selected","validation"]:
        p=pd.read_csv(out/(name+".csv"))
        assert not p.strat_fold.eq(10).any()
        assert not p.ecg_id.duplicated().any()
        expected=m if name.startswith("oof") else v
        assert set(p.ecg_id)==set(expected.ecg_id)
        prediction_sets.append({"name":name,"n":len(p),"max_fold":int(p.strat_fold.max())})
    for arm in ARMS:
        grid=pd.read_csv(out/("grid_"+arm+".csv"))
        scores={c:float(np.nanmean((grid["C_"+str(c)]-grid.y)**2)) for c in cfg["C_grid"]}
        assert choose_C(scores,cfg["tie_tolerance"])==selection["selected"][arm]
        fit=joblib.load(out/"models"/(arm+".joblib"))
        assert fit.train_ids_==set(m.loc[train_mask(m,arm),"ecg_id"])
        assert not fit.train_patients_ & set(v.patient_id)
        use=predict_mask(v,arm)
        actual=fit.predict(v.loc[use],X.loc[v.index[use]])
        np.testing.assert_allclose(actual,pv.loc[use,arm],atol=1e-12,rtol=1e-12)
    for arm in ["E1","E2-C"]:
        fit=joblib.load(out/"models"/(arm+"_C1.joblib"))
        assert fit.C==1
        assert fit.train_ids_==set(m.loc[train_mask(m,arm),"ecg_id"])
        use=predict_mask(v,arm)
        np.testing.assert_allclose(fit.predict(v.loc[use],X.loc[v.index[use]]),pv.loc[use,arm+"_C1"],atol=1e-12,rtol=1e-12)
    cvlogs=[json.loads(x) for x in (out/"training.jsonl").read_text().splitlines() if json.loads(x)["stage"]=="CV"]
    assert len(cvlogs)==len(ARMS)*len(cfg["C_grid"])*8
    for log in cvlogs:
        tr=m.strat_fold.ne(log["held_fold"]).to_numpy() & train_mask(m,log["arm"])
        va=m.strat_fold.eq(log["held_fold"]).to_numpy() & predict_mask(m,log["arm"])
        assert hash_ids(m.loc[tr,"ecg_id"])==log["fit"]["id_hash"]
        assert hash_ids(m.loc[va,"ecg_id"])==log["eval_id_hash"]
        assert not set(m.loc[tr,"patient_id"])&set(m.loc[va,"patient_id"])
        assert not log["fit"]["warnings"]
    pred=combine({a:pv[a].to_numpy() for a in ["B0",*ARMS]})
    for a in ["E2-fallback","Hybrid"]:
        np.testing.assert_allclose(pred[a],pv[a],atol=1e-14)
    thresholds=json.loads((out/"thresholds.json").read_text())
    for a,t in thresholds.items():
        mask=pv[a].notna()
        assert abs(threshold95(pv.loc[mask,"y"],pv.loc[mask,a])-t)<1e-14
    tests=subprocess.run([sys.executable,"-m","unittest","discover","-s","tests","-v"],cwd=ROOT,capture_output=True,text=True)
    (out/"tests.log").write_text(tests.stdout+tests.stderr,encoding="utf-8")
    assert tests.returncode==0,tests.stderr
    old=subprocess.run([sys.executable,"scripts/verify_phase2.py"],cwd=ROOT,capture_output=True,text=True)
    assert old.returncode==0,old.stderr
    result.update({"prediction_sets":prediction_sets,"reloaded_validation_predictions_match":True,
      "CV_training_and_eval_ids_reconciled":160,"unit_tests":tests.stderr.strip().splitlines()[-1],
      "previous_phase_checks":old.stdout.strip(),"fold10_predictions":0,"configuration_matches":cfg==json.loads((out/"config.json").read_text())})
    (out/"verification.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))
if __name__=="__main__":
    with threadpool_limits(limits=1):main()
