# Entenda a IA construída no DataMind

05/11/2026. Guia para uma analista de BI aprendendo Machine Learning. Baseado no código e artefatos preservados, sem novo treinamento ou previsão.

## O que construímos

Construímos um **experimento de classificação supervisionada com regressão logística**. Não é um chatbot, uma rede neural nem um sistema hospitalar. É Machine Learning porque aprende coeficientes a partir de exemplos com resposta conhecida; também é um método estatístico clássico. Chamar de IA não significa raciocínio médico ou autonomia clínica.

Existem modelos serializados, scripts, testes, tabelas de probabilidades e documentação. Não existe aplicativo clínico, interface para pacientes ou API implantada.

## Machine Learning versus uma regra SQL

Em SQL, uma regra CASE WHEN medida > limite THEN 1 ELSE 0 END utiliza um limite escolhido por você. O modelo aprende pesos para combinar medidas a partir dos exemplos. Mas pessoas continuam escolhendo alvo, dados, variáveis, partições e critérios de sucesso. O algoritmo não definiu sozinho a pesquisa.

|Conceito de BI|Correspondência no experimento|
|---|---|
|Tabela fato|Uma linha por exame ECG, não por pessoa|
|ecg_id|Chave do exame para join; não é preditor|
|patient_id|Chave da pessoa para separar partições e agrupar a incerteza|
|Join 1:1|Mesmos 21.799 exames únicos nas tabelas de medidas/metadados|
|Coluna resposta|y=1 quando scp_codes contém CRBBB|
|ETL parametrizado|Imputação e padronização com parâmetros aprendidos no treino|
|Parâmetros persistidos|Medianas, médias, escalas, pesos e intercepto|
|Tabela de saída|predictions.csv, já calculado|
|Indicador de qualidade|Métrica com população e denominador explícitos|

## O alvo CRBBB

CRBBB designa a anotação de bloqueio completo do ramo direito, relacionada a um padrão de condução elétrica no ECG. Não criamos um diagnóstico por regras clínicas: y é a presença da chave CRBBB em scp_codes, independentemente do valor de confiança. IRBBB não foi agregado.

Ausência da chave significa ausência dessa anotação, não doença clinicamente excluída. Laudos podem ter origem humana ou automática, com validação em parte da base. Não houve nova adjudicação por cardiologista.

O modelo aprendeu associações entre medidas e a **anotação do mesmo ECG**. Não aprendeu a prever um evento clínico futuro independente nem demonstrou compreender fisiopatologia.

## Quais informações entram

PTB-XL 1.0.3 fornece metadados/anotações; PTB-XL+ 1.0.1 fornece medidas dos mesmos exames. São recursos relacionados, não validação externa.

As 531 colunas ECGDeli expandem 177 medidas em mediana, intervalo interquartil e contagem. Incluem durações, amplitudes, códigos morfológicos e informações de detecção; não são 531 conceitos fisiológicos independentes. Reutilizamos tabelas públicas, sem reextrair todos os sinais.

O painel reduzido contém:

|Campo|Fonte ECGDeli|Unidade publicada|
|---|---|---|
|QRS_Dur_Global|QRSd_max|ms|
|RR_Mean_Global|RRi_max|ms|
|QRS_Dur_V1|QRSd_V1|ms|
|R_Amp_V1|RPa_V1|mV|
|S_Amp_V1|SPa_V1|mV|
|QRS_Dur_V6|QRSd_V6|ms|
|R_Amp_V6|RPa_V6|mV|
|S_Amp_V6|SPa_V6|mV|

O nome RR_Mean_Global e sua descrição de média **não resolvem** o mapeamento para RRi_max. QRS_Dur_Global também não deve ser automaticamente equiparado ao QRS clínico convencional: mapeia QRSd_max. Especialista precisa confirmar definição e agregação do extrator. Não renomeamos valores nem aplicamos conversões destinadas a outros extratores.

Identificadores, laudos, diagnósticos e metadados como idade/sexo/aparelho não entram no modelo. Alguns constam das tabelas para auditoria, o que não os transforma em preditores.

## Como funciona a regressão logística

Depois de preparar as medidas, calcula-se:

z = intercepto + peso1 × medida1_padronizada + ... + pesok × medidak_padronizada.

A função logística produz p = 1 / (1 + exp(−z)), entre zero e um. Isso não torna p automaticamente uma probabilidade clínica confiável.

**Treinar** significa estimar pesos/intercepto minimizando perda logística com penalização L2. A penalização reduz pesos excessivos; menor C significa mais regularização. Brier foi usado para selecionar C na validação cruzada, não como função diretamente otimizada no ajuste da regressão.

Padronizar subtrai a média e divide pela escala calculadas no treino. No teste, esses parâmetros são reutilizados, não recalculados.

O painel de 531 oferece mais informação potencial, mas também mais ausências, correlações e possibilidade de sobreajuste. Oito medidas não são universalmente suficientes; 531 não são automaticamente superiores.

## Como tratamos ausências

Zero permanece zero. Não foi automaticamente transformado em ausência.

E3 preenche cada ausência com a mediana daquela coluna calculada no treino apropriado. A regra congelada para coluna totalmente ausente no treino é preencher zero, registrando isso; não é afirmação fisiológica. Colunas constantes são mantidas.

E3-I acrescenta 531 indicadores: 1 para medida originalmente ausente e 0 para presente. Após transformação, a regressão recebe 1.062 entradas. Indicadores podem carregar informação do processo de extração, mas não provam o mecanismo de ausência.

Cada divisão de validação cruzada aprende suas próprias transformações somente no treino.

## Modelos e estratégias

|Nome|Regra|
|---|---|
|B0|Prevalência constante do treino; não usa medidas|
|E1|531 medidas; treino e uso somente em exames completos|
|E2-C|Oito medidas; treino na população completa de E1; uso onde as oito existem|
|E2|Oito medidas; treino em todos os elegíveis ao painel|
|E2-fallback|E2 quando possível; B0 quando faltam medidas do painel|
|E3|531 medidas com imputação|
|E3-I|E3 mais indicadores|
|Híbrida|E1 nos completos; E2 nos demais elegíveis; B0 no restante|
|E1_C1 / E2-C_C1|Controles adicionais com C=1|

Há **sete joblib**, cinco regressões selecionadas e dois controles. B0 está em JSON. Fallback e híbrida combinam componentes já treinados; não exigem novos modelos independentes.

C selecionado foi 0,01 para E1/E3/E3-I e 10 para E2/E2-C. Fixar C igual não iguala a complexidade efetiva de painéis diferentes.

## Treinamento, validação e teste

- Folds 1–8: 17.418 exames, 15.023 pacientes. Desenvolvimento, seleção de C e 160 ajustes de validação cruzada; sete ajustes finais/controles registrados.
- Fold 9: 2.183 exames, 1.942 pacientes. Avaliação e escolha dos limiares para especificidade empírica de pelo menos 95%. Métricas no próprio limiar escolhido não são avaliação independente desse limiar.
- Fold 10: 2.198 exames, 1.904 pacientes. Uma execução final registrada com modelos e limiares congelados.

Um paciente pode ter vários exames, mas não aparece em folds diferentes. O teste já foi usado. Selecionar novas estratégias agora por seu resultado não constitui confirmação independente.

## Como interpretar as métricas

**Brier:** média de (p − y)². Menor é melhor. Depende da prevalência; comparar com B0 evita confundir erro pequeno em doença rara com grande utilidade.

**ROC-AUC:** mede ordenação de positivos e negativos ao variar limiares. Não mede diretamente calibração ou benefício clínico.

**AP:** Average Precision resume precisão ao recuperar positivos; depende da prevalência. Não é área trapezoidal da curva precisão–revocação.

**Calibração:** compara probabilidades com frequências observadas. Média prevista próxima à prevalência não garante acerto em toda a escala.

**Sensibilidade/especificidade:** dependem de limiar. Usar o congelado no fold 9, distinguindo campos legados calculados a 0,5.

**IC95%:** descreve incerteza sob o método utilizado. O bootstrap sorteia pacientes e mantém seus exames juntos. O estimando pondera exames igualmente: pessoas com mais exames contribuem mais. Os intervalos condicionam nos modelos/limiares existentes, sem repetir desenvolvimento.

## O que encontramos

|Resultado final salvo|Valor|
|---|---|
|Positivos|54 exames de 45 pacientes|
|Brier E2-fallback|0,006655|
|Brier E3|0,006042|
|Diferença E3 − E2-fallback|−0,000613|
|IC95% da diferença|[−0,002380; +0,001133]|
|Brier híbrida — secundário|0,005384|
|Cobertura exigindo 531 completas|49,50% dos exames; 64,81% dos positivos|
|Fallback no teste|Zero acionamentos|

O intervalo inclui zero: não demonstramos superioridade de E3 nem equivalência. A comparação muda painel e tratamento de ausência; não isola efeito causal da imputação.

No fold 9, E2-fallback tinha Brier pontualmente menor; no teste, E3. Ambos os intervalos primários incluem zero. Essa mudança não prova data drift.

Sensibilidade observada de 100% não é garantia: reamostrar somente positivos classificados corretamente produz IC [1;1], sem informar adequadamente futuros falsos negativos. AUC alta é plausível porque medidas e anotação representam o mesmo padrão de ECG.

## Exemplo fictício do fluxo completo

**Somente ilustração; nenhum valor abaixo é resultado real do DataMind.**

Imagine exames A e B da pessoa P e exame C da pessoa Q. A e B precisam ficar na mesma partição. Uma tabela contém identificação/anotação; outra contém medidas. Um join 1:1 não pode duplicar A.

Suponha que B tenha as oito medidas, mas falte outra das 531. E1 não atende B; E2 atende; E3 imputa a medida ausente.

Para ilustrar a mediana, valores fictícios 100, 110 e 120 no treino produzem 110. Uma ausência na validação recebe 110, sem participar do cálculo. Depois, o pipeline aplica escalas e pesos aprendidos e produziria a coluna p_modelo. **Não inventamos aqui uma probabilidade numérica como se o modelo tivesse sido executado.**

A tabela de saída seria consultada como qualquer tabela de BI: exame, resposta de referência e probabilidade. A avaliação compara p_modelo com y e registra denominadores. SQL pode consultar essas saídas já existentes sem reexecutar o modelo.

## O que a IA não consegue fazer

O experimento reconhece uma anotação em uma avaliação interna específica. Não demonstrou diagnóstico independente, previsão de eventos futuros, identificação de todas as doenças, generalização a outro hospital, manejo de qualquer ausência ou recomendação de tratamento.

Não há revisão clínica independente concluída, garantia de semântica de todas as medidas, calibração suficiente, segurança ou benefício ao paciente. Não utilizar para diagnóstico clínico.

## Onde estão os modelos e as previsões

- Modelos: reports/phase5/run001/models/.
- Regras: src/datamind/pilot.py.
- Configuração/limiares: config.json e thresholds.json em run001.
- Previsões finais existentes: reports/phase6/final001/predictions.csv e scores_*.csv.
- Resultados agregados: metrics.json e composition.json.
- Texto acessível: reports/fase6_resultados_finais.md.

Abra em modo de leitura; não salve CSV novamente em planilha. Não executar scripts de treino/predição nem verificadores que os chamem. Tabelas individuais contêm identificadores pseudônimos/metadados de saúde; não encaminhá-las automaticamente.

data/raw/phase3/model.npy contém probabilidades externas CODE, não um modelo treinado pelo DataMind.

## O que faltaria para virar software

Definir finalidade, confirmar medidas com especialistas, validar externamente quando a finalidade exigir generalização, avaliar calibração e segurança, estabelecer governança e contrato de entrada, tratar erros, criar testes de integração, interface/API, acesso, privacidade, versionamento e monitoramento. Requisitos institucionais e regulatórios dependeriam do uso pretendido.

Nada disso foi implementado como produto nem autorizado como próxima fase. A prioridade é revisão humana do estudo.

**Como apresentar:** “Comparamos estratégias simples para reconhecer uma anotação de ECG e mostramos como exigir medidas completas muda quem é avaliado. A comparação principal ficou inconclusiva e não valida diagnóstico clínico.”
