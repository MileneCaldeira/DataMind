"""Métricas exploratórias, calibração e bootstrap por paciente."""
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import expit
from sklearn.metrics import roc_auc_score, average_precision_score

def metrics(y,p,threshold=.5,weights=None):
    y=np.asarray(y); p=np.asarray(p)
    w=np.ones(len(y)) if weights is None else np.asarray(weights)
    valid=w>0
    y,p,w=y[valid],p[valid],w[valid]
    binary=len(np.unique(y))==2
    out={"brier":float(np.average((p-y)**2,weights=w)),
      "roc_auc":float(roc_auc_score(y,p,sample_weight=w)) if binary else None,
      "average_precision":float(average_precision_score(y,p,sample_weight=w)) if binary else None,
      "mean_probability":float(np.average(p,weights=w)),
      "prevalence":float(np.average(y,weights=w)),
      "calibration_mean_error":float(np.average(p-y,weights=w))}
    out["sensitivity"]=float(np.average(p[y==1]>=threshold,weights=w[y==1])) if np.any(y==1) else None
    out["specificity"]=float(np.average(p[y==0]<threshold,weights=w[y==0])) if np.any(y==0) else None
    return out
def calibration(y,p):
    y=np.asarray(y); p=np.asarray(p)
    logit=np.log(np.clip(p,1e-6,1-1e-6)/(1-np.clip(p,1e-6,1-1e-6)))
    edges=[0,.02,.05,.1,.2,1.00000001]
    bins=[]
    for lo,hi in zip(edges[:-1],edges[1:]):
        mask=(p>=lo)&(p<hi)
        bins.append({"lower":lo,"upper":min(hi,1),"n":int(mask.sum()),
          "positive":int(y[mask].sum()),"mean_p":float(p[mask].mean()) if mask.any() else None,
          "observed":float(y[mask].mean()) if mask.any() else None})
    result={"bins":bins,"intercept":None,"slope":None,"status":"constant_score_or_single_class"}
    if len(np.unique(y))<2 or np.std(logit)<1e-10:return result
    def fun(b):
        z=b[0]+b[1]*logit
        return np.mean(np.logaddexp(0,z)-y*z)
    def jac(b):
        d=expit(b[0]+b[1]*logit)-y
        return np.array([d.mean(),np.mean(d*logit)])
    fit=minimize(fun,[0.,1.],jac=jac,method="BFGS",options={"gtol":1e-8})
    result["status"]=str(fit.message)
    if fit.success:
        result["intercept"],result["slope"]=map(float,fit.x)
    return result
def summarize(frame,arms):
    result={}
    for arm in arms:
        valid=frame[arm].notna()
        group=frame[valid]
        result[arm]={"n":len(group),"patients":int(group.patient_id.nunique()),
          "positive":int(group.y.sum()),"coverage":float(valid.mean()),
          "positive_coverage":float(group.y.sum()/frame.y.sum()) if frame.y.sum() else None,
          **metrics(group.y,group[arm]),"calibration":calibration(group.y,group[arm])}
        size=group.groupby("patient_id").ecg_id.transform("size")
        result[arm]["patient_equal_weight"]=metrics(group.y,group[arm],weights=1/size)
    return result
def cluster_intervals(frame,arms,reps,seed,full_metrics=True):
    """Same patient draws for all arms; NAN predictions remain abstentions."""
    inv=pd.factorize(frame.patient_id)[0]
    n=inv.max()+1
    rng=np.random.default_rng(seed)
    arrays={a:(frame[a].notna().to_numpy(),frame[a].to_numpy()) for a in arms}
    y=frame.y.to_numpy()
    boot={a:{} for a in arms}
    # fixed paired contrasts, on intersection only
    pairs=[("E3","E2-fallback"),("E3-I","E3"),("Hybrid","E2-fallback"),
           ("E1","E2-C"),("E2-C","E2"),("E1_C1","E2-C_C1")]
    pairs=[(a,b) for a,b in pairs if a in arms and b in arms]
    differences={a+" minus "+b:[] for a,b in pairs}
    for _ in range(reps):
        pw=np.bincount(rng.integers(0,n,n),minlength=n)
        w=pw[inv]
        for a,(mask,p) in arrays.items():
            use=mask & (w>0)
            if not use.any():continue
            if full_metrics:
                vals=metrics(y[use],p[use],weights=w[use])
            else:
                vals={"brier":float(np.average((p[use]-y[use])**2,weights=w[use]))}
            for key,v in vals.items():
                if v is not None:boot[a].setdefault(key,[]).append(v)
        for a,b in pairs:
            use=arrays[a][0]&arrays[b][0]&(w>0)
            if (a,b)==("E2-C","E2"):
                use &= frame.complete.to_numpy()
            d=(arrays[a][1][use]-y[use])**2-(arrays[b][1][use]-y[use])**2
            if len(d):differences[a+" minus "+b].append(float(np.average(d,weights=w[use])))
    def interval(values):
        return {"low":float(np.quantile(values,.025)),"high":float(np.quantile(values,.975)),"valid_replicates":len(values)} if values else None
    return {"metrics":{a:{k:interval(v) for k,v in row.items()} for a,row in boot.items()},
            "paired_brier":{k:interval(v) for k,v in differences.items()},"replicates":reps,"unit":"patient"}
def paired(frame,a,b,mask=None):
    use=frame[a].notna()&frame[b].notna()
    if mask is not None:use&=mask
    g=frame[use]
    return {"n":len(g),"patients":int(g.patient_id.nunique()),"positive":int(g.y.sum()),
            "delta_brier":float(np.mean((g[a]-g.y)**2-(g[b]-g.y)**2)),
            a:metrics(g.y,g[a]),b:metrics(g.y,g[b])}
