"""Aplicação autorizada de pipeline congelado, sem métodos de ajuste."""
import numpy as np
def final_predict(model,meta,X):
    if set(meta.strat_fold.astype(int))!={10}:raise ValueError("Somente fold 10")
    if meta.ecg_id.duplicated().any():raise ValueError("ID duplicado")
    if len(meta)!=len(X) or not meta.index.equals(X.index):raise ValueError("Alinhamento")
    if model.train_patients_ & set(meta.patient_id):raise ValueError("Paciente no treino")
    if model.train_ids_ & set(meta.ecg_id):raise ValueError("Exame no treino")
    if not set(model.columns)<=set(X.columns):raise ValueError("Colunas ausentes")
    p=model.pipeline.predict_proba(X[model.columns])[:,1]
    if not np.isfinite(p).all() or np.any((p<0)|(p>1)):raise ValueError("Probabilidade inválida")
    return p
def claim(path):
    with path.open("x",encoding="utf-8") as f:f.write("Execução final iniciada. Não repetir previsões.\n")
