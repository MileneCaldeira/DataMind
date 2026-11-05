
# Matriz de comparação e originalidade
Data: 05/11/2026. Referências e profundidade de leitura: [revisão](fase7_revisao_literatura.md). Ausência de informação confirmada está marcada; não presumir que o estudo não a tenha reportado.

|Trabalho|Pergunta, dados/população|Modelos e ausências|Métricas e denominadores|Resultado relevante e limitação|Diferença para DataMind|
|---|---|---|---|---|---|
|Wagner 2020|Disponibilizar ECGs clínicos anotados, PTB-XL|Dataset, não contraste de imputação|Estatísticas da base e anotações|Recurso de referência; rótulos não são desfechos independentes|DataMind reutiliza versão atualizada|
|Strodthoff 2023|Características e anotações complementares dos mesmos ECGs|Extratores, benchmark RF; código associado trata NaN|Macro-AUC por tarefas e fontes, subconjuntos compatíveis|Demonstra valor de medidas tabulares; métricas não equivalem a CRBBB binário|Nós explicitamos elegibilidade e contraste pareado de Brier; não inauguramos classificação tabular|
|Zhou 2026|LVH versus normais, população selecionada PTB-XL+|LR e modelos de árvores; mediana, remoção de variáveis muito ausentes; demografia|AUROC/AP e classificação, validação cruzada|Bom desempenho reportado em outra tarefa; seleção clínica restringe denominador|Ausência de teste direto da nossa pergunta não demonstra inovação|
|Sisk 2023|Ausência no desenvolvimento e uso; simulações e aplicação clínica|Imputações e indicadores|Brier, discriminação e calibração nos cenários|Efeito depende do mecanismo; simulações não equivalem a ECGDeli|Sobreposição metodológica forte; nosso caso tem ausências naturais|
|Tsvetanova v3 2026, preprint|Compatibilidade do tratamento entre etapas; simulações e cirurgia pulmonar|CCA, imputações e modelos por padrões|Brier, AUC e calibração conforme população de aplicação|Validação incompatível pode distorcer avaliação; revisão por pares não confirmada|Sobreposição conceitual mais próxima: denominador e uso; extensão empírica em ECG|
|SelectiveNet 2019|Aprender predição com rejeição|Rede e seletor de confiança|Risco versus cobertura nos benchmarks|Seleção otimizada; contexto distinto de ausência estrutural|Nossa cobertura é disponibilidade, não rejeição aprendida|
|Van Calster 2019|Avaliar probabilidades|Trabalho metodológico|Calibração global/local, não benchmark CRBBB|AUC insuficiente; precisão exige informação amostral|Fundamenta limitações, não lacuna original|
|Avula 2023|Panorama clínico de modelos ECG profundos|Revisão sistemática, modelos heterogêneos|Resultados e qualidade de relato por estudo|Não é comparação de imputação tabular|Contexto de validade externa e transparência|
|DataMind|Reconhecer anotação CRBBB com disponibilidade natural|LR L2, completos, painel de oito, imputação, indicadores e híbrida|Brier pareado primário; cobertura, AUC/AP e calibração; 2.198 exames/1.904 pacientes|IC cruza zero, 54 exames positivos; sem validação externa|Estudo metodológico incremental e reproduzível|

## Classificação das alegações
- **Demonstrado:** cobertura completa de 49,50%, seleção de composição, contraste operacional inconclusivo, ausência de acionamento do fallback no teste.
- **Incremental:** tornar explícitos denominadores e controles em uma aplicação ECG pública.
- **Potencial, não demonstrado:** novidade da combinação exata da pergunta, relevância editorial de artigo curto.
- **Não sustentado:** superioridade definitiva, equivalência, causalidade da imputação, validade clínica, novo algoritmo ou primeiro estudo do tema.

A sobreposição não torna o trabalho inútil. Impede vendê-lo como solução inédita para ausências. Posicionamento honesto: estudo de caso metodológico com resultado negativo/inconclusivo e material reproduzível.
