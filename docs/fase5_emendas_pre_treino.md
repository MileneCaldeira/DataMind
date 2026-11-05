# Emendas anteriores ao treinamento — 04/11/2026

A autorização da Fase 5 permite treinamento exploratório em 1–8 e avaliação em 9. Fold 10 não recebe previsões. Os documentos da Fase 4 permanecem intactos.

1. O contraste primário permanece Δ Brier(E3) − Brier(E2-fallback), na mesma população. É contraste entre estratégias operacionais, alterando variáveis e tratamento da ausência simultaneamente. Não estima efeito causal da imputação. E1/E2-C e E2-C/E2 preservam os controles de variáveis e amostra de treino.
2. A grade C={.01,.1,1,10} é selecionada por Brier agrupado fora do fold em 1–8. OOF do C selecionado é diagnóstico de seleção com otimismo possível. OOF com C=1 previamente fixado é avaliação de desenvolvimento sem escolha de hiperparâmetro por esses resultados. Fold 9 fornece avaliação das probabilidades dos modelos ajustados em 1–8. Não usar métricas de 9 para trocar C ou modelo.
3. Limiar de especificidade ≥95% é ajustado em 9 e guardado para avaliação futura. Sensibilidade/especificidade nesse mesmo conjunto no limiar ajustado serão rotuladas como ajuste aparente, não validação independente. Reportar métricas binárias no limiar fixo 0,5, definido antes do treino, como diagnóstico sem escolha pelos dados. Não atribuir significado clínico ao limiar.
4. Bootstrap pareado por paciente, 2.000 réplicas, em 9 para métricas e diferenças. ICs de Brier no desenvolvimento são condicionais às previsões OOF e não incluem seleção/retreinamento. Calibração, composição e contrastes em 9 são exploratórios, não confirmatórios.
5. LR L2, solver lbfgs, tolerância 1e-6, até 3.000 iterações. Convergência insuficiente interrompe a execução para diagnóstico e emenda. CPU com uma thread BLAS. Sem pesos de classe. Mediana, indicadores fixos e escala ajustados dentro de cada treino.
6. Indicadores são gerados para todas as colunas. Colunas constantes recebem escala 1 e são preservadas, sem seleção orientada por alvo. Coluna inteiramente ausente no treino recebe zero explícito, registrado. Medidas inválidas não são corrigidas silenciosamente.
7. Não existe verificação clínica independente nova nesta etapa. A revisão da Fase 4 e autorização da pesquisadora permitem o piloto técnico de anotação CRBBB, preservada a limitação clínica. O painel é exploratório e não será alterado por desempenho.
8. O congelamento ao término registrará códigos, configuração, ambiente, modelos e limiares. “Congelado” significa referência reprodutível. A liberação do teste final depende de revisão dos achados e nova autorização.

Nenhum resultado preditivo foi consultado para formular estas emendas.
