# Disponibilidade de medidas de ECG e avaliação da anotação CRBBB em uma comparação de estratégias com PTB-XL

**Versão 4 — revisão de linguagem e apresentação, 16/11/2026. Rascunho para revisão científica. Base experimental e resultados provenientes das Fases 5–6.**

Pesquisadora responsável pelo DataMind: **MileneCaldeira**, identificação utilizada no repositório. Nome para publicação, afiliação e correspondência: **a confirmar pela pesquisadora**. Eventuais coautorias dependem de contribuições reais e concordância; não há equipe de especialistas presumida.

## Resumo
**Contexto:** exigir medidas completas pode restringir a população avaliada por classificadores de eletrocardiogramas. **Objetivo:** comparar estratégias de disponibilidade de medidas para reconhecer a anotação de bloqueio completo do ramo direito (CRBBB). **Métodos:** estudo retrospectivo com PTB-XL/PTB-XL+, regressões logísticas L2 e partições sem pacientes compartilhados. Folds 1–8 desenvolveram os modelos; fold 9 definiu limiares; fold 10 recebeu avaliação única. O contraste primário comparou Brier de 531 medidas imputadas (E3) com oito medidas e fallback (E2-fallback), por bootstrap agrupado por paciente. **Resultados:** o teste incluiu 2.198 exames de 1.904 pacientes; 54 exames positivos pertenciam a 45 pacientes. E2-fallback apresentou Brier 0,006655 e E3, 0,006042. A diferença foi −0,000613 (IC95% −0,002380 a +0,001133). Exigir 531 medidas completas cobriu 49,50% dos exames e 64,81% dos positivos. O fallback não foi acionado. A estratégia híbrida apresentou Brier 0,005384 em análise secundária. **Conclusão:** não houve suporte estatístico à superioridade primária nem demonstração de equivalência. Requisitos de completude alteraram cobertura e composição da avaliação. A observação é contextual e não estabelece utilidade clínica ou generalização externa.

Palavras-chave provisórias: eletrocardiografia; dados ausentes; avaliação de modelos. Adequação DeCS/MeSH pendente.

## Introdução
Características extraídas automaticamente de ECGs oferecem uma representação tabular para modelos estatísticos. PTB-XL e PTB-XL+ disponibilizam ECGs, anotações e medidas complementares do mesmo conjunto de exames [1,2]. Essa disponibilidade facilita experimentos reproduzíveis, mas não garante que todas as medidas possam ser obtidas em cada exame.

A análise restrita a registros completos muda a população a que as métricas se referem. Imputar características ou reduzir o painel pode ampliar a cobertura, mas também modifica a informação disponível e o processo de desenvolvimento. Trabalhos metodológicos já discutem essas escolhas e a compatibilidade entre desenvolvimento e uso [3,4]. A nossa investigação não propõe uma solução nova para dados ausentes.

A pergunta primária foi se a estratégia de 531 medidas com imputação apresentava menor erro probabilístico de classificação da anotação CRBBB que a estratégia de oito medidas com fallback, quando avaliadas nos mesmos exames. O objetivo primário foi estimar a diferença pareada de Brier entre essas estratégias. Os objetivos secundários foram descrever cobertura, composição dos exames atendidos, calibração e os controles de painel e população de treinamento. A contribuição candidata é a quantificação contextual dessas escolhas em um benchmark público de ECG. A hipótese e a hierarquia das análises seguem o protocolo congelado.

A escolha de CRBBB foi pragmática e exploratória: uma anotação binária disponível, relacionada a características de condução ventricular e compatível com um piloto tabular de baixo custo. Não houve comparação prospectiva entre diagnósticos que demonstrasse ser o alvo mais relevante. A relação estreita com o QRS facilita a interpretação da tarefa, mas também restringe a novidade e a independência clínica.

CRBBB corresponde a bloqueio completo do ramo direito. Critérios eletrocardiográficos em adultos incluem QRS alargado e morfologia característica em derivações direitas e laterais [9]. Não aplicamos esses critérios para criar ou validar os rótulos. Trabalhos anteriores já examinam marcadores de bloqueios de ramo em bases que incluem PTB-XL [11]; reconhecer essa anotação não é, por si, contribuição nova.

## Metodologia

### Desenho, dados e alvo
Estudo retrospectivo secundário do [PTB-XL 1.0.3](https://doi.org/10.13026/kfzx-aw45) e [PTB-XL+ 1.0.1](https://doi.org/10.13026/g6h6-7g88), distribuídos sob CC BY 4.0. As duas bases representam os mesmos exames; sua combinação não constitui validação externa. A integração por ecg_id foi verificada como 1:1. Identificadores foram usados somente para integração, agrupamento e auditoria.

A população integrada contém 21.799 exames de 18.869 pacientes. O alvo binário foi definido pela presença da chave CRBBB em scp_codes, independentemente do valor de confiança. IRBBB não foi agregado. A ausência da chave significa ausência dessa anotação, não exclusão clínica de doença. Segundo a documentação original, os registros foram adquiridos entre 1989 e 1996; laudos humanos ou automáticos foram convertidos em códigos SCP, com validação cardiológica em parte dos registros. Não houve nova adjudicação clínica neste estudo.

### Preditores e ausências
As 531 colunas ECGDeli correspondem à expansão de 177 medidas por mediana entre batimentos, intervalo interquartil e contagem de batimentos utilizados. Portanto, incluem características morfológicas e de disponibilidade, não 531 quantidades fisiológicas independentes. As contagens não são anotações diagnósticas, mas podem carregar informação sobre detecção de ondas. Não foram incluídos códigos diagnósticos, laudos, identificadores ou metadados diagnósticos como preditores. A auditoria não identificou vazamento direto de rótulos na lista autorizada. Contudo, medidas de duração e morfologia se relacionam aos critérios usados na anotação, o que limita a interpretação clínica da discriminação.

O painel reduzido contém QRS_Dur_Global, RR_Mean_Global, QRS_Dur_V1, R_Amp_V1, S_Amp_V1, QRS_Dur_V6, R_Amp_V6 e S_Amp_V6. Durações são expressas em milissegundos e amplitudes em milivolts, preservando sinal. O painel foi definido após exploração inicial de disponibilidade, antes do treinamento; não foi uma seleção externa independente. Ausências explícitas foram preservadas; zero não foi convertido automaticamente em ausência.

O dicionário harmonizado requer cautela: QRS_Dur_Global mapeia QRSd_max; RR_Mean_Global, embora descrito como intervalo RR médio, mapeia RRi_max. Mantivemos os valores distribuídos, sem reinterpretar RRi_max como média aritmética nem recalcular medidas. Os seis campos de V1/V6 mapeiam QRSd_X, RPa_X e SPa_X. As amplitudes já estão em mV; não aplicamos fatores de conversão de outros extratores. A equivalência com medidas clínicas convencionais permanece pendente de especialista. Não foram aplicados cortes clínicos de QRS aos valores globais.

### Dicionário do painel reduzido

|Campo utilizado|Identificador ECGDeli no dicionário|Unidade publicada|Interpretação e pendência|
|---|---|---|---|
|QRS_Dur_Global|QRSd_max|ms|Agregação global e pontos fiduciais precisam de confirmação especializada|
|RR_Mean_Global|RRi_max|ms|O nome harmonizado sugere média, mas a correspondência com RRi_max exige esclarecer a agregação|
|QRS_Dur_V1|QRSd_X, X=V1|ms|Duração por derivação, dependente da delineação|
|R_Amp_V1|RPa_X, X=V1|mV|Amplitude assinada, referência e distinção R/R′ a revisar|
|S_Amp_V1|SPa_X, X=V1|mV|Amplitude assinada, referência e ausência de onda a revisar|
|QRS_Dur_V6|QRSd_X, X=V6|ms|Duração por derivação, dependente da delineação|
|R_Amp_V6|RPa_X, X=V6|mV|Amplitude assinada, referência a revisar|
|S_Amp_V6|SPa_X, X=V6|mV|Amplitude assinada, referência a revisar|

Fonte documental local em `data/raw/phase3/feature_description.csv`, conferida na auditoria da Fase 5. As pendências indicam o limite da interpretação das variáveis empregadas. O esclarecimento da semântica requer consulta ao extrator e revisão especializada.

### Partições e desenvolvimento
Folds oficiais 1–8: 17.418 exames, 15.023 pacientes e 432 exames positivos. Fold 9: 2.183 exames, 1.942 pacientes e 55 positivos. Fold 10: 2.198 exames, 1.904 pacientes e 54 positivos. Não houve pacientes compartilhados entre partições.

Regressões logísticas L2 utilizaram lbfgs, máximo de 3.000 iterações, tolerância 10⁻⁶ e semente 20261104. Medianas, médias e desvios foram aprendidos no treino. Colunas constantes foram preservadas com escala unitária; a regra congelada para coluna totalmente ausente era preenchimento zero, sem estimar parâmetros fora do treino. E3-I adicionou indicadores para todas as 531 colunas, inclusive quando constantes. O parâmetro C foi escolhido entre 0,01; 0,1; 1; 10 por validação deixando um fold oficial de desenvolvimento de fora, minimizando Brier agregado fora do treino; empate até 10⁻⁶ favoreceu menor C. Imputação, padronização e regras de colunas foram ajustadas somente no treino correspondente. Não houve ponderação de classes, sobreamostragem ou recalibração. Os modelos finais utilizaram apenas folds 1–8. C selecionado: 0,01 para E1/E3/E3-I; 10 para E2/E2-C. Controles adicionais fixaram C=1.

O fold 9 definiu limiares pelo menor valor que atendesse à especificidade empírica de pelo menos 95%, conforme implementação congelada. Seu desempenho também orientou a interpretação exploratória, mas não modificou os modelos após o congelamento. Os limiares constam da tabela reproduzível. A análise final não foi precedida por registro público prospectivo; houve exploração prévia e conhecimento de contagens do teste, mas não de suas previsões antes da execução final.

### Estratégias
|Estratégia|Treinamento e predição|População atendida|
|---|---|---|
|B0|Prevalência constante dos folds 1–8|Todos|
|E1|531 medidas, treinamento e uso somente em completos|Completos nas 531|
|E2-C|Oito medidas, treinamento nos mesmos completos de E1|Exames com oito medidas|
|E2|Oito medidas, treinamento em todos os elegíveis ao painel|Exames com oito medidas|
|E2-fallback|E2 quando disponível; B0 caso contrário|Todos|
|E3|531 medidas com imputação mediana do treino|Todos|
|E3-I|E3 com indicadores de ausência|Todos|
|Híbrida|E1 nos completos; E2 nos demais elegíveis; B0 no restante|Todos|

Os controles E1/E2-C com C selecionado comparam estratégias com diferentes variáveis e regularizações, embora treinadas na mesma população. O controle adicional C=1 mantém o valor nominal da penalização, mas não iguala complexidade efetiva ou geometria entre painéis de dimensões distintas. E2-C/E2 investigam mudança de treinamento sob o mesmo painel; não se presume isolamento causal. Eles não tornam causal o contraste primário, que altera simultaneamente painel e tratamento operacional de ausência.

### Avaliação e integridade
O desfecho primário foi Brier(E3) − Brier(E2-fallback), pareado nos mesmos exames. Brier é a média do erro quadrático entre probabilidade e alvo binário; menor é melhor. Seu nível depende da prevalência e da composição. Foi reportado B0, constante igual à prevalência do treino, sem interpretar Brier pequeno como utilidade clínica. AP designa Average Precision, não integração trapezoidal da curva precisão–revocação. O suporte direcional exigia limite superior do IC95% abaixo de zero. Não foi definida margem de equivalência.

Os intervalos percentis utilizaram 2.000 reamostragens de pacientes, semente 20261104, mantendo todos os exames de cada paciente sorteado e os mesmos sorteios entre comparadores. O estimando principal pondera exames igualmente, enquanto o agrupamento respeita dependência intrapaciente. A incerteza é condicional aos modelos, imputadores e limiares congelados, sem refazer desenvolvimento ou seleção do limiar. Os pacientes são tratados como unidades independentes de reamostragem; não há ajuste para dependência adicional por local ou aparelho. ROC-AUC, Average Precision (AP), calibração, cobertura e contrastes adicionais são secundários; não houve correção de multiplicidade que permitisse promovê-los a confirmações independentes.

Calibração foi descrita nas faixas fixas [0; 0,02; 0,05; 0,10; 0,20; 1], e pelo ajuste diagnóstico logit Pr(Y=1) = a + b logit(p), com a e b estimados conjuntamente. Clipping em [10⁻⁶; 1−10⁻⁶] foi usado apenas nesse logit. O intercepto a não é calibration-in-the-large estimada com inclinação fixada em 1. Não há IC reportado para a e b; não foram usadas essas estimativas para corrigir probabilidades.

A Fase 6 gerou uma única execução preditiva, com modelos, transformações e limiares congelados. As Fases 7 e 8 utilizaram resultados existentes para redação, auditoria documental e figuras, sem nova inferência preditiva. Hashes dos 57 arquivos do manifesto da Fase 5 e dos 31 arquivos do manifesto de entrega da Fase 6 permaneceram íntegros. Testes e verificações de correspondência entre probabilidades individuais e predictions.csv estão registrados na Fase 6. Não foram repetidas previsões nesta fase.

## Resultados

### Cobertura e população
A exigência das 531 medidas completas reteve 1.088/2.198 exames (49,50%) e 35/54 positivos (64,81%). Os 1.110 exames incompletos incluíram 19 positivos. Portanto, no teste, positivos foram proporcionalmente menos excluídos que o conjunto total. Todos os exames tinham as oito medidas: E2 e E2-fallback coincidiram e o mecanismo de fallback não foi avaliado empiricamente nesse conjunto.

A prevalência da anotação foi 3,22% nos completos e 1,71% nos incompletos. Havia 1.021 e 1.013 pacientes nesses estratos, com 130 pacientes em ambos; suas contagens não são aditivas. A idade mediana entre valores abaixo de 90 anos foi 62 e 64 anos, respectivamente; valores elevados sujeitos à anonimização não entraram nesse resumo. Trata-se de composição descritiva, não de demonstração do mecanismo de ausência.

### Comparação primária
E3 apresentou Brier 0,006042 (IC95% 0,003899–0,008592), contra 0,006655 (0,004333–0,009163) de E2-fallback. A diferença pareada foi −0,000613 (−0,002380 a +0,001133). A hipótese de superioridade de E3 não recebeu suporte estatístico. O intervalo admite vantagem ou desvantagem e não demonstra equivalência.

### Análises secundárias
|Estratégia|Exames|Brier|ROC-AUC|AP|
|---|---:|---:|---:|---:|
|B0|2.198|0,023964|0,500000|0,024568|
|E2-C|2.198|0,007052|0,996994|0,863493|
|E2 / E2-fallback|2.198|0,006655|0,997141|0,862865|
|E3|2.198|0,006042|0,997625|0,909119|
|E3-I|2.198|0,006089|0,997607|0,908265|
|Híbrida|2.198|0,005384|0,998152|0,909652|

**Resultado em população restrita:** E1, nos 1.088 completos, teve Brier 0,005830, ROC-AUC 0,998616 e AP 0,953360. Esse resultado não pertence à ordenação da tabela de cobertura integral.

Fonte: reports/phase6/final001/metrics.json, overall. Tabela integral com IC, limiares e métricas binárias: [tabelas/metricas.md](tabelas/metricas.md). O resultado de E1 não deve ser ordenado diretamente com os das estratégias que atendem todos os exames.

A híbrida teve o menor Brier pontual entre as estratégias de cobertura integral. Sua diferença para E2-fallback foi −0,001271 (IC95% −0,002821 a +0,000121), secundária e inconclusiva. Indicadores de ausência não evidenciaram benefício: E3-I menos E3 foi +0,000047 (−0,000020 a +0,000129).

#### Controles secundários de treinamento e regularização
Os três contrastes abaixo utilizam os mesmos 1.088 exames completos. Foram previstos no protocolo; sua inclusão nesta versão corrige omissão de relato, sem realizar nova análise.

|Contraste secundário|ΔBrier|IC95% por paciente|
|---|---:|---|
|E1 − E2-C, C selecionado|−0,003409|[−0,006613; −0,000498]|
|E1_C1 − E2-C_C1, C=1|+0,000465|[−0,003872; +0,005073]|
|E2-C − E2|+0,000842|[−0,000126; +0,001830]|

Fonte: metrics.json, paired_secondary e bootstrap.paired_brier. O contraste ajustado E1/E2-C tem IC abaixo de zero, mas combina painel e regularização; o controle C=1 é inconclusivo. Não se conclui que a diferença seja causada pela penalização, nem que o painel completo seja superior em geral. Multiplicidade e incerteza impedem promover esse resultado à hipótese primária.

Nos completos, Brier de E2 foi 0,008397 e de E3, 0,005856; nos incompletos, 0,004947 e 0,006223. São contrastes descritivos dentro de cada estrato; não se deve atribuir a diferença entre estratos a uma dificuldade intrínseca sem considerar prevalência e composição.

E2-fallback, E3 e híbrida tiveram sensibilidade observada de 100% nos limiares congelados, com especificidades de 95,43%, 96,08% e 96,13%. Os IC bootstrap de sensibilidade [1;1] são degenerados: todos os positivos observados foram classificados corretamente, e reamostrar esses mesmos pacientes não cria falsos negativos. Isso não demonstra sensibilidade populacional perfeita. Não calculamos novo intervalo que ignorasse o agrupamento.

Probabilidades médias foram 0,023867, 0,024421 e 0,024019, respectivamente, ante prevalência 0,024568. Intercepto/inclinação de calibração foram 0,294/1,274; 0,224/1,235; e 0,427/1,456. Esses diagnósticos existentes não foram usados para recalibrar. Faixas de probabilidade contêm poucos eventos e não sustentam calibração fina.

### Comparação descritiva com fold 9
No fold 9, E2-fallback teve Brier 0,007983 e E3, 0,008256; a diferença foi +0,000273 (IC95% −0,001586 a +0,001984). A ordenação pontual se inverteu no teste, mas ambos os intervalos incluem zero. O painel reduzido permaneceu numericamente competitivo; equivalência não foi testada.

A cobertura completa dos positivos passou de 40,00% no fold 9 a 64,81% no teste. Nos completos/incompletos do fold 9 havia 22/1.137 e 33/1.046 positivos. A direção da diferença de prevalência entre estratos mudou. Essa heterogeneidade é compatível com composição e incerteza amostral; não estabelece data drift nem seu mecanismo.

## Discussão
O principal resultado é a combinação de perda importante de cobertura sob completude estrita e comparação probabilística inconclusiva entre estratégias operacionais na população integral. O painel reduzido alcançou todos os exames de teste, mas o desenho não permite concluir que oito medidas sejam universalmente suficientes.

Os benchmarks de PTB-XL+ já estabelecem o interesse de características tabulares [2]. Estudos sobre dados ausentes discutem alinhamento entre desenvolvimento, validação e aplicação [3,4,10]. O suplemento de Sisk diferencia calibração global com offset de inclinação e descreve condições em que indicadores e imputação mudam de desempenho. Os resultados não identificam um mecanismo de ausência. O estudo apresenta um caso reproduzível de ECG com denominadores explícitos, controles e resultado primário inconclusivo. Isso constitui contribuição incremental; a busca direcionada não comprova que a combinação exata seja inédita.

Comparar modelos apenas em suas populações atendidas pode confundir modelo e seleção. O Brier de E1 refere-se a uma população com prevalência diferente. A comparação primária pareada evita essa confusão de denominadores, mas não separa o efeito causal da imputação daquele da mudança de variáveis.

O trabalho de Rueda et al. [11], cujo manuscrito público descreve exclusão de segmentos sem batimentos suficientes e imputação de parâmetros de batimentos, aproxima-se do tema disponibilidade em ECG. Entretanto, seus marcadores, regras, unidades de processamento e comparações de bloqueios diferem do contraste probabilístico aqui estudado. Não são comparados numericamente os resultados entre estudos, nem atribuídos à versão final detalhes não confirmados no texto público.

A seleção por disponibilidade difere da classificação seletiva aprendida por confiança [5]. O estudo não estima uma curva ótima de risco–cobertura. Tampouco demonstra que ausências sejam aleatórias ou que exista uma direção universal de exclusão de positivos.

AUCs próximas de um podem refletir a proximidade entre medidas do sinal e os critérios usados na interpretação do próprio ECG. Isso é compatível com reconhecimento de anotação, mas não equivale a diagnóstico independente, validação clínica ou identificação de benefício ao paciente. Calibração e discriminação precisam ser avaliadas separadamente [6]. A experiência mais ampla com modelos de ECG também recomenda cautela ao traduzir resultados de benchmarks para aplicação [7].

## Limitações

A grade de regularização selecionou seu menor valor avaliado, C=0,01, nos painéis amplos. Isso deixa em aberto o comportamento com penalizações mais fortes. Além disso, as previsões fora do treino usadas para selecionar C também embasaram diagnósticos exploratórios de desenvolvimento, sujeitos a otimismo de seleção. A avaliação final utilizou os modelos previamente congelados. Esses limites já constavam das emendas e do relatório piloto e restringem a interpretação da escolha de hiperparâmetros.
Amostra de apenas 54 exames positivos em 45 pacientes limita sensibilidade, AP, calibração e análises de subgrupos. Não foi demonstrada precisão suficiente para equivalência ou segurança clínica. O bootstrap não incorpora a variabilidade de todo o desenvolvimento e apresenta degeneração para sensibilidade. Não foram produzidos novos intervalos, testes de interação, métricas ou análises de poder após a revisão.

Há um único recurso público e alvo derivado da interpretação do ECG, sem adjudicação independente ou validação externa. O painel resultou de exploração inicial. Os folds 9 e 10 tiveram composição distinta, e o teste não foi completamente cego quanto a contagens. Não identificamos o mecanismo de ausência nem testamos transportabilidade entre serviços, aparelhos ou populações.

A calibração foi resumida por faixas fixas, intercepto e inclinação; poucos eventos restringem sua interpretação. Os códigos P_Morph e HA__Global foram tratados numericamente, sem demonstrar adequação de sua ordem/distância. A interpretação clínica de QRSd_max e RRi_max exige revisão especializada. A auditoria da tabela não reexecutou a extração do sinal, nem exclui duplicação de sinais não investigada ou falhas upstream. A estratégia de fallback não foi acionada no teste. Resultados secundários múltiplos não confirmam superioridade da híbrida.

## Conclusão
No teste interno reservado, exigir todas as medidas reduziu cobertura e selecionou uma composição distinta. A comparação primária não sustentou superioridade de 531 medidas imputadas sobre oito medidas com fallback, nem estabeleceu equivalência. A contribuição é uma análise metodológica incremental da relação entre disponibilidade, população avaliada e desempenho, restrita ao reconhecimento de uma anotação.

## Figuras e material reproduzível
1. [Fluxograma](figuras/01_fluxograma.png): partições e denominadores, com sobreposição intrateste explicitada.
2. [Cobertura](figuras/02_cobertura.png): exames e positivos atendidos.
3. [Brier pareado](figuras/03_brier_pareado.png): contraste primário e secundários na população integral.
4. [Calibração](figuras/04_calibracao.png): pontos por faixas fixas e seus denominadores; descritivo.
5. [Composição](figuras/05_composicao.png): proporção positiva por completude e fold.

Para comunicação curta, priorizar fluxograma e contraste pareado; cobertura, calibração e composição podem permanecer como suplemento. Todos os materiais mantêm os valores da versão 1.

Arquivos vetoriais e PDF correspondentes disponíveis. O script scripts/fase7_materials.py apenas renderiza os resultados anteriores. Requisitos e verificação em reports/phase7. Repositório público/DOI de arquivamento: **pendente**. Configuração: experiments/fase5.json; versões: reports/phase5/run001/environment.json e reports/phase5/run001/requirements.lock.txt (Python 3.13.7; scikit-learn 1.9.1; NumPy 2.5.4; pandas 3.1.1; SciPy 1.18.1); entradas: reports/phase3/entradas.json; resultados: reports/phase6/final001/metrics.json; controle histórico da v2: scripts/fase8_verify.py. A revisão editorial da v3 está registrada em reports/aprimoramento_pesquisa_2026-11-16.md. A revisão de linguagem da v4 está registrada em reports/revisao_linguagem_autoria.md; a v3 foi preservada integralmente. A reprodução da extração original depende de ECGDeli/MATLAB; a análise tabular reutiliza CSVs públicos. Licença dos dados não licencia automaticamente o código do projeto ou artigos de terceiros; a licença de distribuição do código precisa ser definida. Não executar novamente o preditor final no diretório preservado.

## Declarações pendentes
Ética: uso secundário de dados públicos; **confirmar requisitos institucionais e eventual dispensa**, sem afirmar aprovação inexistente. Financiamento, conflitos, contribuições CRediT e agradecimentos: **preencher e confirmar pelos autores**. Não há registro prospectivo público declarado.

Uso de IA: esta versão foi produzida com assistência de IA para revisão direcionada, organização, redação e geração de materiais a partir dos resultados existentes. A verificação final, responsabilidade científica e aprovação do texto cabem aos autores humanos; adequar a declaração à política do veículo.

## Referências
1. Wagner P et al. PTB-XL, a large publicly available electrocardiography dataset. Scientific Data. 2020;7:154. https://doi.org/10.1038/s41597-020-0495-6
2. Strodthoff N et al. PTB-XL+, a comprehensive electrocardiographic feature dataset. Scientific Data. 2023;10:279. https://doi.org/10.1038/s41597-023-02153-8
3. Sisk R et al. Imputation and missing indicators for handling missing data in the development and deployment of clinical prediction models: A simulation study. Statistical Methods in Medical Research. 2023;32:1461–1477. https://doi.org/10.1177/09622802231165001
4. Tsvetanova A et al. Compatibility of Missing Data Handling Methods across the Stages of Producing Clinical Prediction Models. arXiv:2504.06799v3. 2026. Preprint. https://arxiv.org/abs/2504.06799v3
5. Geifman Y, El-Yaniv R. SelectiveNet: A Deep Neural Network with an Integrated Reject Option. PMLR. 2019;97:2151–2159. https://proceedings.mlr.press/v97/geifman19a.html
6. Van Calster B et al. Calibration: the Achilles heel of predictive analytics. BMC Medicine. 2019;17:230. https://doi.org/10.1186/s12916-019-1466-7
7. Avula V, Wu KC, Carrick RT. Clinical Applications, Methodology, and Scientific Reporting of Electrocardiogram Deep-Learning Models: A Systematic Review. JACC: Advances. 2023;2:100686. https://doi.org/10.1016/j.jacadv.2023.100686
8. Collins GS et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. BMJ. 2024;385:e078378. https://doi.org/10.1136/bmj-2023-078378

9. Surawicz B et al. AHA/ACCF/HRS recommendations for the standardization and interpretation of the electrocardiogram: part III: intraventricular conduction disturbances. J Am Coll Cardiol. 2009;53:976–981. https://doi.org/10.1016/j.jacc.2008.12.013
10. Hoogland J et al. Handling missing predictor values when validating and applying a prediction model to new patients. Statistics in Medicine. 2020;39:3591–3607. https://doi.org/10.1002/sim.8682
11. Rueda C et al. Compelling new electrocardiographic markers for automatic diagnosis. Computer Methods and Programs in Biomedicine. 2022;221:106807. https://doi.org/10.1016/j.cmpb.2022.106807. Métodos e apêndices consultados na versão pública https://arxiv.org/abs/2112.12196v2; equivalência integral à versão publicada não verificada.

Relato orientado por TRIPOD+AI [8], ainda sem declaração de conformidade integral.

## Pendências humanas antes de submissão
Cardiologista: semântica das medidas, validade do alvo e limites da interpretação. Bioestatístico: estimando, inferência condicionada, degeneração e interpretação dos controles. Pesquisador externo: originalidade e adequação editorial. A revisão documental realizada não substitui pareceres humanos independentes. Não há recomendação de uso clínico.
