
# Pendências clínicas, estatísticas e editoriais
05/11/2026. Revisão documental não equivale a validação clínica independente.

## Cardiologista ou especialista em ECG
CRBBB significa bloqueio completo do ramo direito: alteração de condução intraventricular reconhecida por padrão eletrocardiográfico. A recomendação AHA/ACCF/HRS inclui, em adultos, QRS ≥120 ms e aspectos morfológicos em V1/V2 e derivações laterais, não somente uma duração. Critérios variam com idade e contexto; não foram aplicados para reclassificar esta coorte. [Referência primária](https://doi.org/10.1016/j.jacc.2008.12.013). Não é orientação diagnóstica individual.

|Campo preservado|Fonte ECGDeli no dicionário|Unidade declarada|Questão humana precisa|
|---|---|---|---|
|QRS_Dur_Global|QRSd_max|ms|Qual definição de início/fim e agregação produz este global? Não assumir equivalência com QRS clínico; auditoria prévia registrou mediana de desenvolvimento 160 ms|
|RR_Mean_Global|RRi_max|ms|Por que o nome “Mean” mapeia “max”? Confirmar agregação antes de chamá-lo média aritmética|
|QRS_Dur_V1|QRSd_V1|ms|Validade da duração por derivação e falhas de delineação|
|R_Amp_V1|RPa_V1|mV|R versus R′ e referência de amplitude; painel não representa toda a morfologia|
|S_Amp_V1|SPa_V1|mV|Sinal e referência, inclusive ondas não detectadas|
|QRS_Dur_V6|QRSd_V6|ms|Comparabilidade com duração global e lateral|
|R_Amp_V6|RPa_V6|mV|Interpretação morfológica e estabilidade|
|S_Amp_V6|SPa_V6|mV|Amplitude não substitui duração/entalhe da onda S|

Fonte: data/raw/phase3/feature_description.csv. Não aplicar fatores das colunas Uni-G/12SL a ECGDeli. Os valores permanecem iguais; unidades documentadas não provam plausibilidade fisiológica individual.

As 531 colunas são 177 entradas expandidas por mediana, IQR e contagem, extraídas de pontos fiduciais; códigos morfológicos e contagens exigem interpretação. Avaliar se tratar P_Morph e HA__Global como números limita a representação. Identificar se ausência reflete onda não identificável, inexistente ou falha de processamento requer revisão do extrator/sinais, não pode ser deduzido de NaN.

O alvo é presença da chave SCP CRBBB. Laudos podem ter origem humana/automática, com validação em parte da base; confiança não é probabilidade calibrada de doença. Todas as 54 anotações positivas de teste têm confiança registrada 100, o que não equivale a adjudicação independente. Conferir se a ausência da chave é controle adequado para a pergunta e como coanotações limitam a tarefa. Não há autorização para relabeling.

**Produto esperado do especialista:** parecer sobre adequação semântica do alvo/painel e texto clínico, com distinção entre limitação tolerável e inconsistência que exija outro estudo. Se houver erro material de unidades/definições, suspender submissão; não “corrigir” resultados históricos silenciosamente.

## Bioestatístico humano
- Julgar estimando por exame e influência de pacientes com muitos registros; IC condicionado aos modelos/limiares.
- Revisar plausibilidade de independência entre pacientes e limites de agrupamento por paciente sem centro/aparelho.
- Conferir reamostragem percentil, tratamento das réplicas e precisão com 45 pacientes positivos; nenhum novo cálculo é solicitado nesta fase.
- Avaliar relato da sensibilidade [1;1], sem considerar isso garantia; qualquer intervalo adicional exige justificativa e nova autorização.
- Distinguir intercepto conjunto de CITL com offset; revisar se gráficos esparsos e ausência de IC de calibração estão adequadamente limitados.
- Rever controles com C diferente versus C=1, multiplicidade, ausência de margem de equivalência e falta de inferência sobre mudança entre folds.

## Pesquisador/editor e instituição
Validar frase de contribuição e comparação com literatura, especialmente Rueda, Hoogland, Sisk e Tsvetanova. Completar checklist TRIPOD+AI, autores/CRediT/ética/financiamento/conflitos e política de IA. Definir licença do código e depósito público com atribuições dos dados; artigos e suplementos baixados não devem ser redistribuídos automaticamente como se tivessem a licença do dataset.

Nenhuma pendência justifica, por si, treinar modelos adicionais. Primeiro obter revisão humana focalizada.
