"""Gera tabelas piloto a partir dos artefatos, sem refazer previsões."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"reports/phase5/run001"
def f(x,n=5):
    return "NA" if x is None else format(x,"."+str(n)+"f")
def ci(x):
    return "["+f(x["low"])+", "+f(x["high"])+"]" if x else "NA"
def main():
    e=json.loads((OUT/"evaluation.json").read_text())
    selection=json.loads((OUT/"selection.json").read_text())
    runtime=json.loads((OUT/"runtime.json").read_text())
    fit=json.loads((OUT/"final_fit.json").read_text())
    val=pd.read_csv(OUT/"validation.csv")
    lines=["# Fase 5 — resultados exploratórios de validação",
      "04/11/2026. Nenhuma previsão do fold 10. Métricas por exame, IC95% por bootstrap de pacientes, 2.000 réplicas. Os intervalos condicionam nos modelos treinados e não incluem incerteza de seleção ou novo treinamento.",
      "## Fold 9 — probabilidades dos modelos ajustados em 1–8",
      "As estratégias com cobertura integral são comparáveis na mesma população. E1 atende somente C e não pode ser comparado diretamente às linhas de cobertura integral. O baseline da última coluna é calculado nos mesmos exames de cada linha.",
      "| Estratégia | Exames / pacientes | Positivos | Cobertura / positivos | Brier (IC95%) | ROC-AUC (IC95%) | AP (IC95%) | Brier B0 no mesmo suporte |",
      "|---|---:|---:|---:|---|---|---|---:|"]
    for a in ["B0","E1","E2-C","E2-fallback","E3","E3-I","Hybrid"]:
        r=e["validation"]["overall"][a]
        ints=e["validation"]["bootstrap"]["metrics"][a]
        g=val[val[a].notna()]
        b0=np.mean((g.B0-g.y)**2)
        lines.append(f"| {a} | {r['n']} / {r['patients']} | {r['positive']} | {100*r['coverage']:.2f}% / {100*r['positive_coverage']:.2f}% | {f(r['brier'])} {ci(ints['brier'])} | {f(r['roc_auc'])} {ci(ints['roc_auc'])} | {f(r['average_precision'])} {ci(ints['average_precision'])} | {f(b0)} |")
    lines+=["","## Contrastes pareados no fold 9","Diferença é primeiro menos segundo, em Brier. Valores negativos favorecem o primeiro. E1/E2-C e E2-C/E2 usam somente C. Os demais contrastes operacionais usam toda a coorte.",
      "| Contraste | Exames | Δ Brier | IC95% |","|---|---:|---:|---|"]
    for a,r in e["validation"]["paired"].items():
        lines.append(f"| {a} | {r['n']} | {f(r['delta_brier'],6)} | {ci(e['validation']['bootstrap']['paired_brier'][a])} |")
    lines+=["","O contraste primário é entre duas políticas, não efeito causal da imputação. As diferenças entre estratégias com cobertura integral são pequenas e os intervalos serão interpretados com a incerteza, sem escolher vencedora universal.",
      "## Calibração e limiar fixo",
      "Sensibilidade/especificidade abaixo usam 0,5 previamente fixado, sem otimização no fold 9. O diagnóstico de intercepto/inclinação usa o próprio conjunto avaliado, sem corrigir probabilidades. Referência ideal aproximada 0/1. B0 constante não identifica inclinação.",
      "| Estratégia | Média prevista / observada | Intercepto / inclinação | Sensibilidade (IC95%) | Especificidade (IC95%) |",
      "|---|---|---|---|---|"]
    for a in ["B0","E1","E2-C","E2-fallback","E3","E3-I","Hybrid"]:
        r=e["validation"]["overall"][a]; it=e["validation"]["bootstrap"]["metrics"][a]; cal=r["calibration"]
        lines.append(f"| {a} | {f(r['mean_probability'])} / {f(r['prevalence'])} | {f(cal['intercept'],3)} / {f(cal['slope'],3)} | {f(r['sensitivity'],3)} {ci(it['sensitivity'])} | {f(r['specificity'],3)} {ci(it['specificity'])} |")
    lines+=["","Os limiares de especificidade ≥95% foram ajustados em 9 para uso futuro. Sua sensibilidade no próprio 9 é aparente, não avaliação independente. Valores e diagnósticos estão em thresholds.json e evaluation.json. Não usar intervalos acima, que são de 0,5, para esses limiares.",
      "## Calibração em faixas fixas",
      "| Modelo | Faixa | n / positivos | Média prevista | Frequência observada |","|---|---|---:|---:|---:|"]
    for a in ["E2-fallback","E3","E3-I"]:
        for b in e["validation"]["overall"][a]["calibration"]["bins"]:
            lines.append(f"| {a} | {b['lower']}–{b['upper']} | {b['n']} / {b['positive']} | {f(b['mean_p'])} | {f(b['observed'])} |")
    lines+=["","## Desenvolvimento fora do treino",
      "OOF significa previsão de exame cujo fold não participou daquele ajuste. C=1 foi definido antes do treino. A grade selecionada usa os mesmos resultados OOF para escolher C e tem otimismo de seleção possível. Não tratá-la como validação externa ou CV aninhada.",
      "| Estratégia | C selecionado | Brier OOF C=1 | Brier OOF selecionado | Faixa Brier entre folds, selecionado | Brier aparente treino final |",
      "|---|---:|---:|---:|---|---:|"]
    for a in ["E1","E2-C","E2","E3","E3-I"]:
        bs=[x[a]["brier"] for x in e["oof_selected"]["folds"].values()]
        lines.append(f"| {a} | {selection['selected'][a]} | {f(e['oof_fixed']['overall'][a]['brier'])} | {f(e['oof_selected']['overall'][a]['brier'])} | {f(min(bs))}–{f(max(bs))} | {f(fit[a]['apparent_train_brier'])} |")
    lines+=["","Para cobertura integral, E3-I apresentou o menor Brier OOF selecionado, seguido de E3. Com C=1 fixo, o painel reduzido foi melhor. No fold 9, E2-fallback teve o menor Brier entre as estratégias de cobertura integral. A ordenação depende de regularização e partição, indicando cautela.",
      "O Brier de treino é apenas diagnóstico aparente e não evidência de generalização. A diferença treino/OOF é maior nos painéis completos. A grade termina em C=0,01 na direção de regularização forte, onde os braços completos foram selecionados. Não foi demonstrado ótimo global. Manter a grade prevista evita escolhê-la a partir de 9. Uma expansão futura seria emenda de desenvolvimento com novo congelamento.",
      "## Completos e incompletos no fold 9",
      "| Estrato | Exames / pacientes | Positivos / prevalência | Brier E2 | Brier E3 | AUC E2 / E3 | AP E2 / E3 |",
      "|---|---:|---:|---:|---:|---|---|"]
    for label in ["complete","incomplete"]:
        r=e["validation"]["strata"][label]; a=r["E2-fallback"]; b=r["E3"]
        lines.append(f"| {label} | {a['n']} / {a['patients']} | {a['positive']} / {100*a['prevalence']:.2f}% | {f(a['brier'])} | {f(b['brier'])} | {f(a['roc_auc'])} / {f(b['roc_auc'])} | {f(a['average_precision'])} / {f(b['average_precision'])} |")
    lines+=["","Esses estratos são populações diferentes, com prevalências distintas. Diferença entre seus Briers não estima efeito causal da ausência. Comparações E2/E3 dentro de cada estrato são pareadas. Há pacientes com exames em ambos os estratos, portanto contagens de pacientes por estrato não devem ser somadas como indivíduos independentes.",
      "## Interpretação",
      "Há sinal preditivo em relação à prevalência constante para reconhecer a anotação. Não há demonstração de superioridade definitiva de E3 sobre E2-fallback. Maior AUC da estratégia completa não se traduziu em menor Brier/AP no fold 9. O ganho marginal dos indicadores de ausência é pequeno.",
      "A pergunta permanece pertinente porque a cobertura de E1 é limitada e a ordenação das políticas muda entre critérios. Generalização externa, utilidade clínica, causalidade e originalidade permanecem não demonstradas.",
      "Detalhes completos, ICs OOF de Brier, métricas com peso igual por paciente, frequências demográficas e todos os limiares estão nos [resultados JSON](phase5/run001/evaluation.json), [composição](phase5/run001/composition.json) e [configuração](phase5/run001/config.json)."]
    formatted=[]
    for line in lines:
        if formatted and line and ((line.startswith("|") and not formatted[-1].startswith("|")) or line.startswith("#") or (formatted[-1].startswith("#"))):
            if formatted[-1]:formatted.append("")
        formatted.append(line)
    (ROOT/"reports/fase5_resultados_validacao.md").write_text("\n".join(formatted)+"\n",encoding="utf-8")
if __name__=="__main__":main()
