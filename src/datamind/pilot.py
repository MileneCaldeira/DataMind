"""Pipeline piloto. O fold 10 nunca pode receber previsões por esta API."""
import ast
import hashlib
import json
import re
import warnings
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.exceptions import ConvergenceWarning
from .integrity import PANEL, verify_hashes, disjoint_patients

ARMS = ("E1", "E2-C", "E2", "E3", "E3-I")
def hash_ids(ids):
    return hashlib.sha256(",".join(map(str,sorted(ids))).encode()).hexdigest()
def allowed(meta, training=False):
    folds=set(meta.strat_fold.astype(int))
    valid=set(range(1,9)) if training else set(range(1,10))
    if not folds <= valid:
        raise ValueError("Partição proibida")
    if meta.ecg_id.duplicated().any():
        raise ValueError("ecg_id duplicado")
def whitelist(root):
    desc=pd.read_csv(root/"data/raw/phase3/feature_description.csv",encoding="utf-8-sig",dtype=str).fillna("")
    lead=["I","II","III","aVR","aVL","aVF","V1","V2","V3","V4","V5","V6"]
    mapping={}
    for _,r in desc.iterrows():
        if not r.ecgdeli_feature: continue
        names=[r.id[:-1]+x for x in lead] if r.id.endswith("_X") else [r.id]
        for name in names:
            for suffix in ["","_iqr","_count"]:
                mapping[name+suffix]={"definition":r.description,"unit":"count" if suffix=="_count" else r.unit,"source":r.ecgdeli_feature}
    return mapping
def load_development(root):
    verify_hashes(root)
    meta=pd.read_csv(root/"data/raw/phase3/ptbxl_database.csv")
    feat=pd.read_csv(root/"data/raw/phase3/ecgdeli_features.csv")
    if meta.ecg_id.duplicated().any() or feat.ecg_id.duplicated().any():
        raise ValueError("Cardinalidade inválida")
    disjoint_patients(meta[["patient_id","strat_fold"]].astype(str).assign(strat_fold=meta.strat_fold.astype(str)).to_dict("records"))
    cols=[x for x in feat if x!="ecg_id"]
    mapping=whitelist(root)
    if len(cols)!=531 or set(cols)!=set(mapping):
        raise ValueError("Whitelist divergente: "+str(set(cols)^set(mapping)))
    if set(feat.ecg_id)!=set(meta.ecg_id):
        raise ValueError("Join não cobre IDs exatamente")
    # Remove holdout BEFORE labels and modeling features are assembled.
    meta=meta.loc[meta.strat_fold.le(9)].copy().sort_values("ecg_id").reset_index(drop=True)
    feat=feat.loc[feat.ecg_id.isin(meta.ecg_id)]
    frame=meta[["ecg_id"]].merge(feat,on="ecg_id",validate="one_to_one",sort=False)
    X=frame[cols].astype(float)
    if np.isinf(X.to_numpy()).any(): raise ValueError("Inf encontrado")
    meta["y"]=meta.scp_codes.map(lambda x:int("CRBBB" in ast.literal_eval(x)))
    meta["complete"]=X.notna().all(axis=1).to_numpy()
    meta["panel_complete"]=X[PANEL].notna().all(axis=1).to_numpy()
    # Only non-predictive metadata needed for audit; reports/labels are dropped.
    meta=meta[["ecg_id","patient_id","strat_fold","y","complete","panel_complete","age","sex","device","site"]]
    allowed(meta)
    audit={"source_hashes_verified":17,"features":mapping,"n_development_validation":len(meta),
           "folds":sorted(meta.strat_fold.unique().tolist()),
           "duplicate_feature_profiles_dev":int(X[meta.strat_fold.le(8)].duplicated().sum()),
           "partitions":{},"panel":{}}
    for part,mask in [("development",meta.strat_fold.le(8)),("validation",meta.strat_fold.eq(9))]:
        g=meta[mask]
        audit["partitions"][part]={"n":len(g),"patients":g.patient_id.nunique(),"positive":int(g.y.sum()),
          "complete":int(g.complete.sum()),"complete_positive":int(g.loc[g.complete,"y"].sum()),
          "panel_complete":int(g.panel_complete.sum()),"panel_positive":int(g.loc[g.panel_complete,"y"].sum())}
    for name in PANEL:
        v=X.loc[meta.strat_fold.le(8),name]
        audit["panel"][name]={"unit":mapping[name]["unit"],"missing_dev":int(v.isna().sum()),
                              "min_dev":float(v.min()),"median_dev":float(v.median()),"max_dev":float(v.max())}
    return meta,X,audit
def train_mask(meta,arm):
    return meta.complete.to_numpy() if arm in ("E1","E2-C") else (meta.panel_complete.to_numpy() if arm=="E2" else np.ones(len(meta),bool))
def predict_mask(meta,arm):
    return meta.complete.to_numpy() if arm=="E1" else (meta.panel_complete.to_numpy() if arm in ("E2","E2-C") else np.ones(len(meta),bool))

class MedianIndicators(TransformerMixin,BaseEstimator):
    def __init__(self,impute=True,indicators=False):
        self.impute=impute
        self.indicators=indicators
    def fit(self,X,y=None):
        x=np.asarray(X,dtype=float)
        self.n_features_in_=x.shape[1]
        self.empty_=np.isnan(x).all(axis=0)
        if not self.impute and np.isnan(x).any(): raise ValueError("Ausência em braço completo")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore",RuntimeWarning)
            self.statistics_=np.nanmedian(x,axis=0)
        self.statistics_[self.empty_]=0
        return self
    def transform(self,X):
        x=np.asarray(X,dtype=float)
        if x.shape[1]!=self.n_features_in_: raise ValueError("Schema incompatível")
        missing=np.isnan(x)
        if not self.impute and missing.any(): raise ValueError("Ausência em braço completo")
        out=np.where(missing,self.statistics_,x)
        return np.hstack([out,missing.astype(float)]) if self.indicators else out

class GuardedModel:
    def __init__(self,arm,C,cfg,columns):
        self.arm,self.C,self.cfg=arm,C,cfg
        self.columns=list(PANEL) if arm in ("E2","E2-C") else list(columns)
        self.pipeline=Pipeline([
          ("missing",MedianIndicators(impute=arm in ("E3","E3-I"),indicators=arm=="E3-I")),
          ("scale",StandardScaler()),
          ("lr",LogisticRegression(C=C,solver=cfg["solver"],max_iter=cfg["max_iter"],
                                   tol=cfg["tol"],random_state=cfg["seed"],class_weight=None))])
    def fit(self,meta,X):
        allowed(meta,training=True)
        self.train_patients_=set(meta.patient_id)
        self.train_ids_=set(meta.ecg_id)
        if len(meta)!=len(X) or not meta.index.equals(X.index): raise ValueError("Alinhamento inválido")
        if len(np.unique(meta.y))!=2: raise ValueError("Classe ausente")
        with warnings.catch_warnings(record=True) as captured:
            warnings.simplefilter("always")
            self.pipeline.fit(X[self.columns],meta.y)
        self.warnings_=[str(w.message) for w in captured]
        if any(issubclass(w.category,ConvergenceWarning) for w in captured):
            raise RuntimeError("Falha de convergência: "+str(self.warnings_))
        self.fit_info_={"n":len(meta),"patients":len(self.train_patients_),"positive":int(meta.y.sum()),
          "id_hash":hash_ids(self.train_ids_),"iterations":int(self.pipeline["lr"].n_iter_[0]),
          "empty_columns":[self.columns[i] for i in np.flatnonzero(self.pipeline["missing"].empty_)],
          "constant_columns":int((self.pipeline["scale"].var_==0).sum()),"warnings":self.warnings_}
        return self
    def predict(self,meta,X):
        allowed(meta)
        if len(meta)!=len(X) or not meta.index.equals(X.index): raise ValueError("Alinhamento inválido")
        if self.train_patients_ & set(meta.patient_id): raise ValueError("Paciente visto no treino")
        return self.pipeline.predict_proba(X[self.columns])[:,1]
def threshold95(y,p,target=.95):
    y=np.asarray(y)
    p=np.asarray(p)
    if len(np.unique(y))<2: return None
    thresholds=np.r_[np.unique(p),np.nextafter(p.max(),np.inf)]
    # Specificity increases monotonically with threshold; choose smallest admissible.
    neg=np.sort(p[y==0])
    spec=np.searchsorted(neg,thresholds,side="left")/len(neg)
    return float(thresholds[np.flatnonzero(spec>=target)[0]])
def choose_C(scores,tolerance):
    best=min(scores.values())
    return min(float(c) for c,s in scores.items() if s<=best+tolerance)
def combine(pred):
    result=dict(pred)
    result["E2-fallback"]=np.where(np.isfinite(pred["E2"]),pred["E2"],pred["B0"])
    result["Hybrid"]=np.where(np.isfinite(pred["E1"]),pred["E1"],result["E2-fallback"])
    return result
