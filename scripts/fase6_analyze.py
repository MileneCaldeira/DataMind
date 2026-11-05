"""Somente métricas sobre CSV final preservado. Nunca carrega modelos."""
import hashlib,json,sys
from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from datamind.evaluation import metrics,summarize,cluster_intervals,paired
OLD=ROOT/"reports/phase5/run001"; OUT=ROOT/"reports/phase6/final001"
def write(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2,allow_nan=False),encoding="utf-8")
def binary_bootstrap(frame,arms,thresholds,reps,seed):
    inv=pd.factorize(frame.patient_id)[0]; n=inv.max()+1
    rng=np.random.default_rng(seed)
    values={a:{"sensitivity":[],"specificity":[]} for a in arms}
    y=frame.y.to_numpy()
    for _ in range(reps):
        weights=np.bincount(rng.integers(0,n,n),minlength=n)[inv]
        for a in arms:
            p=frame[a].to_numpy()
            ok=np.isfinite(p)
            for label,key in [(1,"sensitivity"),(0,"specificity")]:
                use=ok&(y==label)
                den=weights[use].sum()
                if den:
                    good=p[use]>=thresholds[a] if label else p[use]<thresholds[a]
                    values[a][key].append(float(np.sum(weights[use]*good)/den))
    return {a:{k:{"low":float(np.quantile(v,.025)),"high":float(np.quantile(v,.975)),"valid_replicates":len(v)}
                   for k,v in row.items()} for a,row in values.items()}
def with_thresholds(frame,arms,thresholds):
    result=summarize(frame,arms)
    for a in arms:
        g=frame[frame[a].notna()]
        result[a]["fixed_05_diagnostic"]={k:result[a][k] for k in ["sensitivity","specificity"]}
        result[a].update(metrics(g.y,g[a],thresholds[a]))
        result[a]["threshold_from_fold9"]=thresholds[a]
        weights=1/g.groupby("patient_id").ecg_id.transform("size")
        result[a]["patient_equal_weight"]=metrics(g.y,g[a],thresholds[a],weights)
    return result
def composition(g):
    age=g.age.where(g.age<=89)
    return {"n":len(g),"patients":int(g.patient_id.nunique()),"positive":int(g.y.sum()),"negative":int((g.y==0).sum()),
       "prevalence":float(g.y.mean()),"age_median_under90":float(age.median()),"age_mean_under90":float(age.mean()),
       "age_missing_or_masked":int(age.isna().sum()),
       "sex":{str(k):int(v) for k,v in g.sex.value_counts(dropna=False).items()},
       "device":{str(k):int(v) for k,v in g.device.value_counts(dropna=False).items()},
       "site":{str(k):int(v) for k,v in g.site.value_counts(dropna=False).items()},
       "exams_per_patient":{str(k):int(v) for k,v in g.groupby("patient_id").size().value_counts().items()}}
def smd(a,b):
    den=np.sqrt((a.var(ddof=1)+b.var(ddof=1))/2)
    return float((a.mean()-b.mean())/den) if den>0 else None
def main():
    path=OUT/"predictions.csv"
    receipt=json.loads((OUT/"prediction_receipt.json").read_text())
    if hashlib.sha256(path.read_bytes()).hexdigest()!=receipt["predictions_sha256"]:raise ValueError("Prediction hash")
    df=pd.read_csv(path,float_precision="round_trip")
    if set(df.strat_fold)!={10} or df.ecg_id.duplicated().any():raise ValueError("Fold/ID")
    cfg=json.loads((OLD/"config.json").read_text())
    thresholds=json.loads((OLD/"thresholds.json").read_text())
    arms=list(thresholds)
    if df[["E3","E2-fallback"]].isna().any().any():raise ValueError("Primary support")
    result={"primary":paired(df,"E3","E2-fallback"),
            "overall":with_thresholds(df,arms,thresholds),"strata":{},"paired_secondary":{},
            "fallback_count":int((~df.panel_complete).sum()),"seed":cfg["seed"],"bootstrap_reps":cfg["bootstrap"]}
    # Frozen function yields same percentile patient-bootstrap estimand as planned.
    result["bootstrap"]=cluster_intervals(df,arms,cfg["bootstrap"],cfg["seed"],True)
    result["bootstrap"]["binary_frozen_thresholds"]=binary_bootstrap(df,arms,thresholds,cfg["bootstrap"],cfg["seed"])
    result["bootstrap"]["note"]="metrics.sensitivity/specificity use legacy 0.5; binary_frozen_thresholds use fold9 thresholds"
    result["primary"]["CI95"]=result["bootstrap"]["paired_brier"]["E3 minus E2-fallback"]
    result["primary"]["directional_hypothesis_supported"]=result["primary"]["CI95"]["high"]<0
    for label,mask in [("complete",df.complete),("incomplete",~df.complete)]:
        usearms=[a for a in arms if df.loc[mask,a].notna().any()]
        result["strata"][label]=with_thresholds(df[mask],usearms,thresholds)
    for a,b,mask in [("E1","E2-C",df.complete),("E2-C","E2",df.complete),
                     ("E1_C1","E2-C_C1",df.complete),("E3-I","E3",None),("Hybrid","E2-fallback",None)]:
        result["paired_secondary"][a+" minus "+b]=paired(df,a,b,mask)
    complete=df[df.complete]; incomplete=df[~df.complete]
    comp={label:composition(g) for label,g in [("all",df),("complete",complete),("incomplete",incomplete)]}
    comp["SMD_complete_minus_incomplete"]={
        "age_under90":smd(complete.age.where(complete.age<=89).dropna(),incomplete.age.where(incomplete.age<=89).dropna()),
        "sex0":smd(complete.sex.eq(0).astype(float),incomplete.sex.eq(0).astype(float)),
        "positive":smd(complete.y,incomplete.y)}
    comp["patients_in_both_strata"]=len(set(complete.patient_id)&set(incomplete.patient_id))
    write(OUT/"metrics.json",result);write(OUT/"composition.json",comp)
    print(json.dumps({"primary":result["primary"],"fallback_count":result["fallback_count"]},indent=2))
if __name__=="__main__":main()
