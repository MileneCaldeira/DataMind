
# Roteiro para revisor clínico de ECG
05/11/2026. Convite à avaliação humana; este documento não contém parecer independente ou validação clínica.

**Objetivo da leitura:** decidir se alvo, medidas e interpretação clínica da [v2](../artigo/manuscrito_v2.md) são semanticamente adequados ao estudo de reconhecimento de anotação.

## Alvo e limites
Positivo = presença da chave CRBBB em scp_codes, independentemente da confiança. IRBBB não foi agregado. Negativo = ausência dessa anotação, não exclusão clínica confirmada. CRBBB designa bloqueio completo do ramo direito. Não reaplicamos critérios clínicos aos sinais nem realizamos adjudicação.

Laudos humanos ou automáticos foram convertidos para SCP; houve validação cardiológica em parte dos registros. Preditores e alvo vêm do mesmo ECG. Excluir laudos dos preditores evita vazamento direto, mas não cria independência clínica. AUC elevada não comprova diagnóstico independente.

## Oito campos preservados
|Campo|Origem ECGDeli|Significado documental|Unidade|
|---|---|---|---|
|QRS_Dur_Global|QRSd_max|Duração global de QRS; agregação a esclarecer|ms|
|RR_Mean_Global|RRi_max|Intervalo RR; nome “Mean” não resolve a definição de “max”|ms|
|QRS_Dur_V1|QRSd_V1|Duração de QRS em V1|ms|
|R_Amp_V1|RPa_V1|Amplitude R em V1|mV|
|S_Amp_V1|SPa_V1|Amplitude S em V1|mV|
|QRS_Dur_V6|QRSd_V6|Duração de QRS em V6|ms|
|R_Amp_V6|RPa_V6|Amplitude R em V6|mV|
|S_Amp_V6|SPa_V6|Amplitude S em V6|mV|

Fonte: data/raw/phase3/feature_description.csv. Valores/sinais preservados; zero não convertido em ausência. Não aplicados fatores de outros extratores. As 531 colunas incluem mediana, IQR e contagem de batimentos de 177 medidas, não 531 grandezas independentes.

## Questões para responder
- **C1 — obrigatória:** a definição por presença de CRBBB é coerente para reconhecimento de anotação? Como descrever coanotações, confiança e negativos?
- **C2 — obrigatória:** quais pontos fiduciais e agregação definem QRSd_max? Há equivalência com medida clínica convencional ou apenas nome semelhante?
- **C3 — obrigatória:** como interpretar RRi_max sob o nome RR_Mean_Global? É necessário corrigir a descrição científica, preservando os valores?
- **C4 — obrigatória:** amplitudes R/S distinguem R′ e referências de linha de base de modo suficiente para a justificativa do painel?
- C5: códigos P_Morph/HA__Global tratados como números comprometem interpretação ou somente limitam este baseline?
- C6: ausência pode representar onda não identificada ou não aplicável? O texto evita tratá-la automaticamente como erro de coleta?
- **C7 — obrigatória:** há alguma afirmação clínica que deva ser retirada ou alguma inconsistência que impeça submissão?

Solicitamos resposta por código C1–C7 com evidência, gravidade e sugestão textual. “Não foi possível verificar” é uma resposta válida; não presumir aprovação pelo silêncio. Revisão documental não autoriza alterar rótulos ou executar nova extração.

## Material de apoio
[Pendências detalhadas e referência clínica](../reports/fase8_pendencias_especialistas.md), [auditoria de origem](fase5_auditoria_leakage.md), dicionário local e referências 1, 2 e 9 da v2. Se houver interesse em sinais individuais, definir escopo posteriormente, sem inventar que essa revisão já ocorreu.
Registrar comentários recebidos na [matriz](../reports/fase9_matriz_feedback.md).
