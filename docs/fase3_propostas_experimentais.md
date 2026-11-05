# Fase 3 — três propostas candidatas
Consolidação em 04/11/2026. Nenhum treinamento ou métrica preditiva executado.

| Proposta | Hipótese testável e avaliação | Refutação e limites |
|---|---|---|
| A — cobertura das medidas | Imputar medidas pode reduzir erro probabilístico em toda a coorte em comparação com painel reduzido. Regressão logística, controle constante, folds 1–8/9/10, exames pareados e bootstrap por paciente. Brier primário, AP, ROC-AUC, calibração e cobertura secundários | Diferença Brier nula/incerta ou desfavorável contraria a hipótese. Maior cobertura sozinha não é benefício clínico |
| B — contexto de aquisição | Indicadores de ausência podem ajudar na origem e perder vantagem no destino. Origem candidata CS100 3, destino AT-6 C 5.5, escolhidos pela disponibilidade no desenvolvimento. LR com e sem indicadores, mesmo destino, pacientes distintos, grupos oficiais preservados | Ausência de interação enfraquece hipótese. Equipamento/local confundidos. Teste interno por domínio não é hospital externo |
| C — referência da avaliação | Com escores CODE fixos, Brier e calibração podem variar entre leitores e referência adjudicada. Reanálise dos mesmos 827 exames, bootstrap pareado, RBBB inicial. Sem retreino e sem ajuste no teste | Diferenças pequenas ou imprecisas limitam utilidade. Poucos positivos e desacordos, leitores não independentes da adjudicação |

A tem desenho detalhado na [Fase 4](fase4_desenho_experimental.md). Para B, definir todo ajuste nos folds de origem 1–8, limiar em 9 da origem e avaliar origem/destino em 10. Conferir suporte antes de qualquer inferência. Não escolher domínio pelo resultado preditivo. Para C, manter probabilidades e ordem das linhas dos autores, documentar ordem de classes e fonte. Estimar diferenças entre referências, sem interpretar adjudicação como verdade clínica perfeita.

Todas exigem definição de unidade, proveniência do alvo e registro de exclusões. Classes minoritárias não justificam SMOTE antes da divisão. Métricas em exames precisam respeitar repetição por paciente. A/B usam anotações do mesmo ECG, constituindo reconhecimento de padrão, não previsão de eventos futuros. Custos computacionais baixos a moderados, dificuldade estatística maior que a implementação.
