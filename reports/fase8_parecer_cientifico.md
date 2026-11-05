
# Parecer científico — Fase 8
05/11/2026. Revisão automatizada sob três perspectivas, realizada pelo mesmo assistente; não representa três avaliadores humanos independentes. Leitura integral da v1 e confronto com protocolos, implementação e resultados. V1 preservada.

## Juízo geral
O estudo tem pergunta operacional delimitada, separação por paciente e contraste primário adequado à mesma população. Seus resultados são internamente auditáveis. Não foi identificado erro crítico que invalide o resultado primário. A contribuição é contextual e incremental; a redação anterior omitia aspectos importantes para interpretar os controles e as medidas. Não há base para submissão clínica ou alegação de inovação ampla.

Critério de gravidade: **crítico** = invalida resultado ou conclusão central; **importante** = limita interpretação/reprodutibilidade ou exige revisão substancial; **editorial** = apresentação/clareza. Ausência de erro crítico detectado não certifica toda a cadeia upstream.

|ID / gravidade / perspectiva|Evidência na v1 ou fonte|Impacto|Correção na v2 / pendência|
|---|---|---|---|
|P1 Importante — ML|CRBBB escolhido sem justificativa explícita; protocolos registram escolha exploratória|Alvo parece seleção clínica fundamentada quando é caso pragmático|Justificativa retrospectiva transparente, sem inventar escolha prospectiva; revisão clínica|
|P2 Importante — estatística|E1/E2-C apresentados como distinção de variáveis; C=0,01 versus 10|Contraste também muda regularização|Explicitar comparação operacional; incluir controle C=1 já existente, sem novos cálculos|
|P3 Importante — relato|Resultados dos controles C=1 ausentes na v1, embora previstos|Discussão incompleta da robustez; omite resultado que limita interpretação favorável ao painel amplo|Tabela dos três contrastes secundários e interpretação sem causalidade|
|P4 Importante — clínica/ML|RR_Mean_Global mapeia RRi_max; QRS_Dur_Global mapeia QRSd_max no dicionário|Nome harmonizado pode sugerir equivalência fisiológica não demonstrada|Mapeamento e ressalvas explícitos; não renomear dados nem converter; especialista precisa conferir extração|
|P5 Importante — estatística|evaluation.py calibra com intercepto e inclinação livres|Intercepto pode ser confundido com calibration-in-the-large de inclinação fixa|Definir equação; separar média prevista/prevalência; não gerar novo ajuste|
|P6 Importante — clínica|Alvo vem de laudo humano/automático convertido a SCP; preditores medem mesmo ECG|AUC alta não valida diagnóstico independente|Manter alvo como anotação; acrescentar história de aquisição e limites de construto|
|P7 Importante — precisão|54 exames positivos em 45 pacientes; IC sensibilidade [1;1]|Bootstrap empírico não informa adequadamente risco de futuros falsos negativos|Contextualização mantida; nenhum intervalo alternativo calculado; revisão bioestatística|
|P8 Importante — ML|531 incluem mediana/IQR/count; P_Morph e HA__Global numéricos|Contagens podem informar detecção; codificação ordinal não validada|Explicitar representação e limites; não atribuir ganho exclusivamente a fisiologia|
|P9 Importante — publicação|Revisão anterior não incluía Hoogland 2020 nem marcadores BBB de Rueda 2022|Posicionamento de originalidade incompleto|Acrescentar sobreposição, métodos/apêndices; formato incremental|
|P10 Importante — validade externa|PTB-XL+ é derivado do PTB-XL; nenhuma base independente|Não demonstra transporte; recurso histórico e rótulo específico|Limites preservados; não recomendar ampliação indiscriminada|
|P11 Importante — inferência|Bootstrap condicionado a modelos; pacientes com mais exames pesam mais|IC não descreve todo novo desenvolvimento nem estimando por pessoa|Explicitar estimando e condicionamento a limiares; não alterar análise|
|P12 Importante — fallback|Zero acionamentos nos folds 9/10|Não há evidência empírica de desempenho sob falha do painel reduzido|Destaque no resumo/resultados; E2-fallback coincide com E2 no teste|
|P13 Editorial — tabelas|E1 figurava junto a modelos integrais com ressalva apenas textual|Leitura rápida pode induzir ranking indevido|Separar E1 em população restrita|
|P14 Editorial — reprodução|Detalhes de solver e calibração pouco explícitos|Reprodução depende de procurar arquivos|Adicionar parâmetros, fontes e caminhos; v2 não é protocolo novo|
|P15 Importante — acesso público|Repositório/DOI e licença do próprio código pendentes|Reprodução local não equivale a pacote público reutilizável|Declarar pendência; licença CC BY dos dados não resolve código/autoria|
|P16 Importante — clínica|Idades extremas anonimizadas; cadeia de extração não reexecutada|Não assegurar plausibilidade de cada medida ou exclusão de sinais duplicados|Especificar idade abaixo de 90; separar integridade tabular de validação fisiológica|

## Três perspectivas
**ML aplicado à saúde:** pipeline simples e auditável adequado ao estudo de caso; ausência de modelos complexos não é falha. A contagem de variáveis, correlação e codificação restringem interpretabilidade dos coeficientes. Não foi demonstrado efeito isolado da imputação.

**Bioestatística:** pareamento primário e reamostragem por paciente são coerentes com repetição de exames. Não confundir precisão de AUC com precisão de sensibilidade/calibração. Mudanças entre folds não são teste de drift. IC cruzando zero não confirma igualdade. Resultados secundários não devem ser selecionados pela significância.

**Publicação:** texto v2 é mais honesto e completo. A contribuição defensável é a demonstração contextual dos denominadores e resultados operacionais, não nova metodologia. Trabalho curto de congresso é preferível; artigo conciso depende de julgamento externo de relevância incremental.

## Encaminhamento
**Pronto para revisão especializada externa**, sem prontidão para submissão. Não há autorização nem justificativa nesta revisão para novos modelos ou análises. Pendências específicas: fase8_pendencias_especialistas.md. Evidência numérica: fase8_auditoria_estatistica.md.
