"""Verificações finais sobre artefatos; nenhuma chamada preditiva."""
import hashlib,json,subprocess,sys
from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"reports/phase6/final001"
def main():
    frozen=subprocess.run([sys.executable,"scripts/fase5_freeze.py","--check"],cwd=ROOT,capture_output=True,text=True)
    assert frozen.returncode==0,frozen.stderr
    (OUT/"freeze_post.log").write_text(frozen.stdout+frozen.stderr,encoding="utf-8")
    receipt=json.loads((OUT/"prediction_receipt.json").read_text())
    p=OUT/"predictions.csv"
    assert hashlib.sha256(p.read_bytes()).hexdigest()==receipt["predictions_sha256"]
    d=pd.read_csv(p,float_precision="round_trip")
    calls=[json.loads(x) for x in (OUT/"prediction_calls.jsonl").read_text().splitlines()]
    assert len(calls)==7 and len({c["model"] for c in calls})==7
    assert calls==receipt["model_calls"] and receipt["execution_count"]==1
    for c in calls:
        small=pd.read_csv(OUT/("scores_"+c["model"]+".csv"),float_precision="round_trip")
        np.testing.assert_array_equal(small.ecg_id,d.ecg_id)
        np.testing.assert_allclose(small.probability,d[c["model"]],atol=0,rtol=0,equal_nan=True)
        assert d[c["model"]].notna().sum()==c["n"]
    assert d.strat_fold.eq(10).all() and d.ecg_id.is_unique
    metadata=pd.read_csv(ROOT/"data/raw/phase3/ptbxl_database.csv",usecols=["ecg_id","patient_id","strat_fold"])
    assert set(d.ecg_id)==set(metadata.loc[metadata.strat_fold.eq(10),"ecg_id"])
    assert not set(d.patient_id)&set(metadata.loc[metadata.strat_fold.le(9),"patient_id"])
    np.testing.assert_allclose(d["E2-fallback"],np.where(d.E2.notna(),d.E2,d.B0),atol=0,rtol=0)
    np.testing.assert_allclose(d.Hybrid,np.where(d.E1.notna(),d.E1,d["E2-fallback"]),atol=0,rtol=0)
    m=json.loads((OUT/"metrics.json").read_text())
    assert d[["E3","E2-fallback"]].notna().all().all()
    delta=(d.E3-d.y)**2-(d["E2-fallback"]-d.y)**2
    np.testing.assert_allclose(delta.mean(),m["primary"]["delta_brier"],atol=1e-14)
    # Independent implementation of primary grouped bootstrap via patient loss sums.
    inv=pd.factorize(d.patient_id)[0];n=inv.max()+1
    counts=np.bincount(inv);sums=np.bincount(inv,weights=delta)
    rng=np.random.default_rng(m["seed"]);samples=[]
    for _ in range(m["bootstrap_reps"]):
        draws=rng.integers(0,n,n)
        samples.append(sums[draws].sum()/counts[draws].sum())
    quantiles=np.quantile(samples,[.025,.975])
    np.testing.assert_allclose(quantiles,[m["primary"]["CI95"]["low"],m["primary"]["CI95"]["high"]],atol=1e-14)
    # Metrics threshold agreement, without predicting anything.
    thresholds=json.loads((ROOT/"reports/phase5/run001/thresholds.json").read_text())
    for a,t in thresholds.items():
        g=d[d[a].notna()]
        assert abs(m["overall"][a]["sensitivity"]-np.mean(g.loc[g.y.eq(1),a]>=t))<1e-14
        assert abs(m["overall"][a]["specificity"]-np.mean(g.loc[g.y.eq(0),a]<t))<1e-14
    result={"frozen_phase5_unchanged":True,"unique_prediction_execution":1,"calls_per_pipeline":1,
      "saved_probability_files_exact_match":True,"patient_disjoint":True,"primary_same_reference_population":True,
      "primary_bootstrap_independently_reconciled":True,"threshold_metrics_reconciled":True,
      "predictions_sha256":receipt["predictions_sha256"],"no_prediction_calls_in_verification":True}
    (OUT/"verification.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
