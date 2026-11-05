# Fase 6 — registro anterior à execução final

Autorização explícita da pesquisadora para uma execução preditiva no fold 10. Este registro complementa a autorização e não modifica o protocolo congelado.

- Preservar todos os 57 arquivos da referência freeze.json, inclusive docs/decisoes.md. Decisões novas ficam neste documento e nos relatórios da Fase 6.
- O desempenho do fold 9 já influenciou a interpretação exploratória e a comunicação do piloto. Não altera modelos, grade, painel, imputação, probabilidades, limiares ou contraste primário.
- Primário permanece Δ Brier E3 − E2-fallback na população completa de referência, IC95% percentil com 2.000 sorteios de pacientes, semente 20261104. Intervalo inteiramente abaixo de zero sustenta a hipótese direcional, sem demonstrar utilidade clínica.
- Todas as demais estratégias, controles C=1, calibração, estratos e composição são secundários. Sem correção para múltiplas comparações, não serão promovidos a hipóteses confirmatórias.
- A configuração piloto bloqueia fold 10. Será usado executor final separado, autorizado nesta fase, que aplica diretamente os pipelines serializados após verificar paciente, esquema e hashes. O bloqueio original permanece intacto. Nenhum fit ou escolha de limiar será realizado nos modelos preditivos.
- Uma trava de execução exclusiva será gravada antes da primeira chamada preditiva. Cada um dos sete pipelines salvos será chamado uma vez em seu suporte. Estratégias compostas reutilizam essas previsões. Nenhuma nova chamada preditiva será usada para conferir resultados.
- Bootstrap e métricas serão calculados a partir do CSV salvo, sem novas previsões. Sensibilidade/especificidade principais usam os limiares congelados de 9. Métricas a 0,5 geradas pelo utilitário histórico são apenas diagnóstico secundário, identificadas como tal.
- Em 9, E2-fallback não acionou B0. Verificar utilização em 10 sem alterar a política. Uma política que não aciona fallback não demonstra desempenho sob falta frequente das oito medidas.
- Preditores permanecem na whitelist das medidas ECGDeli, incluindo resumos de batimentos. Anotações diagnósticas, laudo, confiança, IDs e metadados não são preditores. CRBBB continua sendo anotação da interpretação do próprio ECG, não referência clínica independente.
- Contagens estruturais do teste já tinham sido vistas na Fase 4. A declaração de ausência de previsões anteriores se baseará nos artefatos, logs e guards disponíveis, não em garantia sobre atividades fora deste repositório.
