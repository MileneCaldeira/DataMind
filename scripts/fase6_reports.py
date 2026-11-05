"""Consolida exclusivamente métricas/probabilidades salvas, sem modelos ou ajustes."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"reports/phase6/final001"
def fmt(x,n=6):return "NA" if x is None else f"{x:.{n}f}"
def ci(x):return f"[{fmt(x['low'])}; {fmt(x['high'])}]"
def main():
 m=json.loads((OUT/"metrics.json").read_text())
 old=json.loads((ROOT/"reports/phase5/run001/evaluation.json").read_text())["validation"]
 comp=json.loads((OUT/"composition.json").read_text())
 lines=["# Fase 6 — resultados finais","Consolidação em 05/11/2026. Uma execução preditiva, sem retreinamento. Esta consolidação usa exclusivamente arquivos já salvos.",
 "## Integridade e análise primária",
 "Os 57 arquivos congelados e 17 hashes de dados permanecem íntegros. Os 18 testes prévios passaram. Confirmados join 1:1, separação de pacientes e correspondência exata entre predictions.csv e sete arquivos individuais. Os registros mostram uma chamada por pipeline e nenhuma previsão anterior de 10 nos artefatos auditados. Isso não verifica atividades fora do repositório.",
 "A população primária contém 2.198 exames de 1.904 pacientes, com 54 exames positivos em 45 pacientes. E3 e E2-fallback cobrem exatamente os mesmos exames. Fallback acionado em zero exames, tanto em 9 quanto em 10.",
 f"**Δ Brier E3 − E2-fallback = {fmt(m['primary']['delta_brier'])}, IC95% {ci(m['primary']['CI95'])}. A hipótese de menor Brier de E3 não recebeu suporte estatístico pelo critério congelado.** O intervalo contém zero e admite efeitos em ambas as direções. Ausência de suporte não demonstra equivalência.",
 "Bootstrap percentil com 2.000 réplicas, semente 20261104, reamostragem de pacientes com todos os seus exames. Intervalos condicionais aos modelos treinados. O contraste e seu intervalo foram reconciliados por uma implementação independente a partir das perdas salvas.",
 "## Métricas por estratégia",
 "Brier menor é melhor. AUC e AP maiores indicam melhor discriminação. E1 e E1_C1 têm suporte C e não devem ser comparados diretamente a estratégias de cobertura integral.",
 "| Estratégia | Exames / pacientes | Positivos | Cobertura exames / positivos | Brier e IC95% | ROC-AUC e IC95% | AP e IC95% |",
 "|---|---:|---:|---:|---|---|---|"]
 for a,r in m["overall"].items():
  it=m["bootstrap"]["metrics"][a]
  lines.append(f"| {a} | {r['n']} / {r['patients']} | {r['positive']} | {100*r['coverage']:.2f}% / {100*r['positive_coverage']:.2f}% | {fmt(r['brier'])} {ci(it['brier'])} | {fmt(r['roc_auc'])} {ci(it['roc_auc'])} | {fmt(r['average_precision'])} {ci(it['average_precision'])} |")
 lines+=["## Limiar congelado e calibração",
 "Probabilidades não foram recalibradas. Os limiares foram escolhidos exclusivamente em 9. Intercepto/inclinação são diagnósticos, não transformações aplicadas aos escores.",
 "| Estratégia | Limiar de 9 | Sensibilidade e IC95% | Especificidade e IC95% | Probabilidade média / prevalência | Intercepto / inclinação |",
 "|---|---:|---|---|---|---|"]
 for a,r in m["overall"].items():
  b=m["bootstrap"]["binary_frozen_thresholds"][a];c=r["calibration"]
  lines.append(f"| {a} | {fmt(r['threshold_from_fold9'],8)} | {fmt(r['sensitivity'])} {ci(b['sensitivity'])} | {fmt(r['specificity'])} {ci(b['specificity'])} | {fmt(r['mean_probability'])} / {fmt(r['prevalence'])} | {fmt(c['intercept'],3)} / {fmt(c['slope'],3)} |")
 lines+=["Todos os classificadores atenderam os positivos observados em seus respectivos suportes nos limiares congelados. Os ICs empíricos de sensibilidade [1;1] são degenerados porque nenhum falso negativo pode ser criado ao reamostrar apenas acertos observados. Não representam certeza de sensibilidade perfeita na população. B0 apresenta degenerescência análoga em zero. Não introduzimos intervalo alternativo após ver o teste.",
 "## Calibração por faixas previamente definidas",
 "| Modelo | Faixa | Exames / positivos | Probabilidade média | Frequência observada |","|---|---|---:|---:|---:|"]
 for a in ["E2-fallback","E3","Hybrid"]:
  for b in m["overall"][a]["calibration"]["bins"]:
   lines.append(f"| {a} | {b['lower']}–{b['upper']} | {b['n']} / {b['positive']} | {fmt(b['mean_p'])} | {fmt(b['observed'])} |")
 lines+=["Faixas pequenas limitam a precisão. A proximidade entre probabilidade média e prevalência não garante boa calibração em toda a escala. O baseline constante não tem inclinação identificável.",
 "## Contrastes secundários pareados",
 "Intervalos descritivos sem ajuste para multiplicidade. E1/E2-C, E2-C/E2 e os controles C=1 são avaliados somente nos mesmos exames completos. Os demais usam toda a coorte.",
 "| Contraste | Exames | Δ Brier | IC95% |","|---|---:|---:|---|"]
 for a,r in m["paired_secondary"].items():
  lines.append(f"| {a} | {r['n']} | {fmt(r['delta_brier'])} | {ci(m['bootstrap']['paired_brier'][a])} |")
 lines+=["E1 versus E2-C ajustados tem intervalo abaixo de zero, mas é contraste secundário com regularizações selecionadas diferentes. O controle com C=1 comum não reproduz evidência inequívoca. Não promover o resultado secundário a confirmação da hipótese primária.",
 "## Completude e população atendida",
 "| Estrato | Exames / pacientes | Positivos / prevalência | Mediana idade abaixo de 90 | Sexo codificado 0 |",
 "|---|---:|---:|---:|---:|"]
 for label in ["complete","incomplete"]:
  c=comp[label]
  lines.append(f"| {label} | {c['n']} / {c['patients']} | {c['positive']} / {100*c['prevalence']:.2f}% | {c['age_median_under90']:.0f} | {c['sex'].get('0',0)} |")
 lines+=["Há 130 pacientes com exames em ambos os estratos. Contagens de pacientes dos estratos não se somam como indivíduos distintos. Idades anonimizadas acima de 89 não entram nos resumos etários.",
 "| Estrato | Modelo | Brier | ROC-AUC | AP | Sensibilidade | Especificidade |","|---|---|---:|---:|---:|---:|---:|"]
 for label,rs in m["strata"].items():
  for a,r in rs.items():
   lines.append(f"| {label} | {a} | {fmt(r['brier'])} | {fmt(r['roc_auc'])} | {fmt(r['average_precision'])} | {fmt(r['sensitivity'])} | {fmt(r['specificity'])} |")
 lines+=["As comparações entre modelos dentro do mesmo estrato têm população comum. Comparar completos com incompletos é comparação entre populações diferentes, sem interpretação causal. Métricas por estrato são descritivas.",
 "Exigir completude excluiu 1.110/2.198 exames (50,50%) e 19/54 positivos (35,19%). Assim, no teste, positivos foram proporcionalmente menos excluídos que a coorte geral. Isso contrasta com 9, onde foram excluídos 60% dos positivos. A regra não produz um efeito universal de exclusão desproporcional de positivos.",
 "Diferenças padronizadas completos menos incompletos, descritivas",
 "| Variável | SMD |","|---|---:|"]
 for k,v in comp["SMD_complete_minus_incomplete"].items():lines.append(f"| {k} | {fmt(v,4)} |")
 lines+=["Distribuição de contexto de aquisição, com três aparelhos mais frequentes por estrato",
 "| Estrato | Aparelhos e contagens |","|---|---|"]
 for k in ["complete","incomplete"]:
  top=sorted(comp[k]["device"].items(),key=lambda z:-z[1])[:3]
  lines.append("| "+k+" | "+", ".join(a+" = "+str(n) for a,n in top)+" |")
 lines+=["Todas as frequências de aparelhos, locais e exames por paciente estão em composition.json. Diferenças de composição não identificam causa de missingness nem efeito de equipamento.",
 "## Fold 9 versus fold 10",
 "| Estratégia | Brier 9 → 10 | AUC 9 → 10 | AP 9 → 10 |","|---|---|---|"]
 for a in ["B0","E1","E2-C","E2-fallback","E3","E3-I","Hybrid"]:
  x=old["overall"][a];y=m["overall"][a]
  lines.append(f"| {a} | {fmt(x['brier'])} → {fmt(y['brier'])} | {fmt(x['roc_auc'])} → {fmt(y['roc_auc'])} | {fmt(x['average_precision'])} → {fmt(y['average_precision'])} |")
 lines+=["Todas as estratégias tiveram Brier numericamente menor em 10. Entre as de cobertura integral, E2-fallback teve o menor Brier em 9 e a híbrida em 10. O contraste primário mudou de +0,000273 para −0,000613, com ambos os ICs incluindo zero. São amostras diferentes. Não foi realizado teste formal de mudança entre folds, e essa diferença não demonstra data drift.",
 "## Rastreabilidade",
 "Fonte exclusiva das métricas — [metrics.json](phase6/final001/metrics.json). [Composição](phase6/final001/composition.json), [recibo da execução](phase6/final001/prediction_receipt.json), [verificação](phase6/final001/verification.json).",
 "No JSON, overall e strata contêm sensibilidade/especificidade nos limiares congelados. Campos aninhados nos objetos paired e primary, além de bootstrap.metrics.sensitivity/specificity, são diagnósticos legados a 0,5. Para os ICs dos limiares de 9, usar bootstrap.binary_frozen_thresholds. Não intercambiar esses campos.",
 "O aviso de depreciação float_precision do pandas foi registrado na leitura/verificação. Não houve erro nem mudança de regras, previsões ou estimativas. O bootstrap foi calculado apenas sobre os escores salvos.",
 "Não executar fase6_predict_once.py novamente. O diretório existente e a trava bloqueiam repetição. scripts/fase6_verify.py verifica escores e hashes sem chamar modelos. scripts/fase6_reports.py apenas renderiza dados existentes."]
 out=[]
 for line in lines:
  if out and line and (line.startswith("#") or out[-1].startswith("#") or (line.startswith("|") and not out[-1].startswith("|"))):
   if out[-1]:out.append("")
  out.append(line)
 (ROOT/"reports/fase6_resultados_finais.md").write_text("\n".join(out)+"\n",encoding="utf-8")
if __name__=="__main__":main()
