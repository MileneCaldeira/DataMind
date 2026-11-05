
# Roteiro para bioestatístico
05/11/2026. Solicitação de parecer humano; sem nova análise nesta fase.

## Desenho a revisar
Estudo retrospectivo de reconhecimento de anotação. Treino/seleção de C nos folds 1–8, limiares no fold 9, execução final única no fold 10. Pacientes separados entre partições. Teste: 2.198 exames/1.904 pacientes; 54 positivos/45 pacientes positivos.

Estimando principal: diferença média de perdas por exame, Brier(E3) − Brier(E2-fallback), no mesmo conjunto de exames. Pacientes com mais exames têm maior peso no estimando. Não é efeito causal da imputação: também muda o painel.

|Resultado congelado|Valor|
|---|---|
|Brier E2-fallback|0,006655|
|Brier E3|0,006042|
|Δ primário / IC95%|−0,000613 / [−0,002380; +0,001133]|
|Brier híbrida, secundário|0,005384|

## Inferência e limitações
Bootstrap percentil de 2.000 réplicas, semente 20261104: pacientes com reposição, mantendo todos os exames e os mesmos sorteios entre comparadores. IC condicionado aos modelos, imputadores e limiares; não inclui novo desenvolvimento. Não há margem de equivalência.

Sensibilidade observada de 100% nas estratégias integrais de classificação; IC bootstrap [1;1] degenerado. Reamostragem dos acertos não cria falsos negativos; não significa sensibilidade populacional perfeita. Campos binários corretos: metrics.json overall/strata e bootstrap.binary_frozen_thresholds; campos legados aninhados usam 0,5.

Calibração: faixas fixas e ajuste diagnóstico com intercepto e inclinação livres. Intercepto conjunto não é CITL com inclinação fixada em 1. Poucos eventos, sem IC de intercepto/inclinação. Não houve recalibração.

Brier depende de prevalência/composição; B0 usa prevalência do treino. E1 atende apenas 1.088 completos e não deve ser ranqueado diretamente com modelos integrais. Fallback nunca acionado em 9/10.

## Controles existentes no mesmo suporte completo
|Contraste secundário|ΔBrier|IC95%|
|---|---:|---|
|E1 − E2-C, C selecionado|−0,003409|[−0,006613; −0,000498]|
|E1_C1 − E2-C_C1|+0,000465|[−0,003872; +0,005073]|
|E2-C − E2|+0,000842|[−0,000126; +0,001830]|

C escolhido: E1/E3/E3-I = 0,01; E2/E2-C = 10. C=1 comum não iguala complexidade efetiva. Contrastes secundários sem ajuste de multiplicidade; não promovidos a hipótese principal.

## Questões obrigatórias
- **B1:** estimando por exame, agrupamento por paciente e pressupostos de independência são defensáveis?
- **B2:** IC percentil condicionado e pequena quantidade de pacientes positivos estão adequadamente limitados?
- **B3:** descrição da sensibilidade degenerada evita falsa certeza? Há necessidade de esclarecimento textual adicional?
- **B4:** calibração e efeito da prevalência estão descritos corretamente?
- **B5:** os controles permitem a interpretação proposta sem atribuição causal indevida a painel, C ou treinamento?
- **B6:** resultados de 9 e 10 e primários/secundários permanecem separados, sem equivalência implícita?

Pedir parecer com gravidade e justificativa, não novos cálculos. Se uma análise adicional for considerada indispensável, solicitar proposta separada com objetivo, caráter pós-hoc e necessidade de autorização.

Fontes: [v2](../artigo/manuscrito_v2.md), [auditoria](../reports/fase8_auditoria_estatistica.md), [resultados](../reports/fase6_resultados_finais.md), src/datamind/evaluation.py, experiments/fase5.json. Respostas: [matriz](../reports/fase9_matriz_feedback.md).
