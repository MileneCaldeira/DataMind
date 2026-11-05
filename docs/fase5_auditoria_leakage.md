# Auditoria de origem e vazamento — Fase 5

## Origem e versões
PTB-XL+ 1.0.1 declara PTB-XL 1.0.3 como base. ECGDeli obtém pontos fiduciais do sinal e resume medidas por batimento em mediana, IQR e contagem. Diagnósticos 12SL e anotações estendidas ficam em outros arquivos, que não entram no pipeline. [Fonte oficial](https://physionet.org/content/ptb-xl-plus/1.0.1/)

CRBBB é presença da chave em scp_codes, derivado do laudo convertido para SCP. O laudo pode ter origem cardiológica ou automática, com validação posterior em parte dos registros. Não pressupor padrão-ouro independente. A confiança não é preditor nem critério de exclusão. Não juntar IRBBB. [Origem das anotações](https://physionet.org/content/ptb-xl/1.0.3/)

## Auditoria dos campos
A whitelist será construída expandindo apenas entradas ECGDeli do dicionário oficial para derivações, acrescidas de _iqr e _count. Exigir correspondência exata às 531 colunas. Isso inclui morfologia da onda P e eixo elétrico derivados do sinal, não heart_axis do laudo. HA__Global e P_Morph são códigos numéricos do extrator, tratados como números nesta regressão inicial, limitação de codificação registrada.

| Painel fixo | Unidade | Justificativa |
|---|---|---|
| QRS_Dur_Global | ms | Duração global da condução ventricular |
| RR_Mean_Global | ms | Intervalo RR, contexto de frequência |
| QRS_Dur_V1 e QRS_Dur_V6 | ms | Duração em derivações que caracterizam morfologia de condução |
| R_Amp_V1 e R_Amp_V6 | mV | Amplitudes R |
| S_Amp_V1 e S_Amp_V6 | mV | Amplitudes S |

Mapeamento confirmado no feature_description.csv local preservado. RR_Mean_Global é nome harmonizado, associado a RRi_max no extrator, não recalculado aqui. Não aplicar novamente conversões de outros extratores. O painel não é critério diagnóstico validado nem foi escolhido por desempenho. A disponibilidade por partição será medida apenas em desenvolvimento/validação nesta fase.

## Limite da independência
Duração e amplitudes de QRS participam da interpretação que produz CRBBB. Predizer esse rótulo a partir do sinal é a tarefa de reconhecimento proposta, mas não prova previsão de doença independente ou desfecho futuro. Excluir dados do laudo impede vazamento direto, sem eliminar essa dependência de construto.

## Controles implementados
Hashes dos 17 arquivos, IDs únicos, join um para um com cobertura integral e pacientes disjuntos entre os dez folds serão verificados. O loader retira fold 10 antes de construir y e X de modelagem, usando do teste somente IDs/fold para integridade. Whitelist de medidas exclui identificadores, laudos, diagnósticos automáticos, confiança, validadores e metadados.

Modelos possuem guarda que rejeita fold 9/10 no fit e fold 10 no predict, além de rejeitar pacientes vistos pelo modelo em predições de avaliação. Estatísticas de transformação são estimadas somente no fit. Pré-processamento é refeito em cada divisão. Testes desafiam contaminação de partição, cardinalidade, esquema, mediana, indicadores, constantes, limiar e pareamento.

A auditoria documental não encontrou vazamento material que impeça o piloto. Não foi repetida a extração ECGDeli de todo o sinal bruto, portanto a cadeia upstream não foi verificada integralmente por execução. Resultados da auditoria programática serão preservados em reports/phase5/run001/audit.json.

Tentativa inicial de leitura do dicionário falhou com KeyError por BOM UTF-8. Corrigida para utf-8-sig antes de qualquer treino, sem editar arquivo bruto. Não houve falha de download dos dados, pois foram reutilizados.

## Resultado da execução
Whitelist exata de 531 campos confirmada. Join 1:1 e 17 hashes íntegros. Matriz de modelagem contém apenas 19.601 exames de 1–9. Não há perfis numéricos idênticos no desenvolvimento, mas isso não exclui duplicação de sinais brutos não reextraídos. Pacientes permanecem em um só fold oficial. O painel tem um exame incompleto no desenvolvimento e nenhum em 9.

14 testes passaram e os hashes de treino/avaliação de todos os 160 ajustes foram reconciliados com a regra de divisão. Não foi identificado vazamento direto de rótulo ou paciente. As probabilidades salvas têm fold máximo 9. As limitações de anotação, seleção de hiperparâmetro, sobreajuste e construto permanecem descritas em fase5_limitacoes.md.
