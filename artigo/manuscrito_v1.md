
# Disponibilidade de medidas eletrocardiográficas e avaliação de classificadores da anotação de bloqueio completo do ramo direito

**Versão 1, para revisão científica — 05/11/2026. Não submetido.**

Títulos alternativos:
1. Cobertura e desempenho de classificadores de anotação eletrocardiográfica sob diferentes requisitos de completude.
2. Medidas incompletas de eletrocardiogramas: comparação operacional de painéis reduzidos e imputação no PTB-XL.

Autores, afiliações e autor correspondente: **pendentes de definição e concordância**.

## Resumo
**Contexto:** exigir medidas completas pode restringir a população avaliada por classificadores de eletrocardiogramas. **Objetivo:** comparar estratégias de disponibilidade de medidas para reconhecer a anotação de bloqueio completo do ramo direito (CRBBB). **Métodos:** estudo retrospectivo com PTB-XL/PTB-XL+, regressões logísticas L2 e partições sem pacientes compartilhados. Folds 1–8 desenvolveram os modelos; fold 9 definiu limiares; fold 10 recebeu avaliação única. O contraste primário comparou Brier de 531 medidas imputadas (E3) com oito medidas e fallback (E2-fallback), por bootstrap agrupado por paciente. **Resultados:** o teste incluiu 2.198 exames de 1.904 pacientes; 54 exames positivos pertenciam a 45 pacientes. E2-fallback apresentou Brier 0,006655 e E3, 0,006042. A diferença foi −0,000613 (IC95% −0,002380 a +0,001133). Exigir 531 medidas completas cobriu 49,50% dos exames e 64,81% dos positivos. O fallback não foi acionado. A estratégia híbrida apresentou Brier 0,005384 em análise secundária. **Conclusão:** não houve suporte estatístico à superioridade primária nem demonstração de equivalência. Requisitos de completude alteraram cobertura e composição da avaliação. Os resultados sustentam um estudo metodológico incremental, sem estabelecer utilidade clínica ou generalização externa.

Palavras-chave provisórias: eletrocardiografia; dados ausentes; avaliação de modelos. Adequação DeCS/MeSH pendente.

## Introdução
Características extraídas automaticamente de ECGs oferecem uma representação tabular para modelos estatísticos. PTB-XL e PTB-XL+ disponibilizam ECGs, anotações e medidas complementares do mesmo conjunto de exames [1,2]. Essa disponibilidade facilita experimentos reproduzíveis, mas não garante que todas as medidas possam ser obtidas em cada exame.

A análise restrita a registros completos muda a população a que as métricas se referem. Imputar características ou reduzir o painel pode ampliar a cobertura, mas também modifica a informação disponível e o processo de desenvolvimento. Trabalhos metodológicos já discutem essas escolhas e a compatibilidade entre desenvolvimento e uso [3,4]. A nossa investigação não propõe uma solução nova para dados ausentes.

A lacuna candidata é uma caracterização explícita, neste recurso de ECG, da cobertura e do desempenho probabilístico sob requisitos distintos de disponibilidade, preservando uma comparação primária na mesma população. O objetivo foi comparar operacionalmente 531 medidas imputadas e um painel de oito medidas, com controles para completude, conjunto de variáveis e população de treinamento. O alvo é uma anotação de CRBBB, não um diagnóstico independente adjudicado para este estudo.

## Metodologia

### Desenho, dados e alvo
Estudo retrospectivo secundário do PTB-XL 1.0.3 e PTB-XL+ 1.0.1, distribuídos sob CC BY 4.0. As duas bases representam os mesmos exames; sua combinação não constitui validação externa. A integração por ecg_id foi verificada como 1:1. Identificadores foram usados somente para integração, agrupamento e auditoria.

A população integrada contém 21.799 exames de 18.869 pacientes. O alvo binário foi definido pela presença da chave CRBBB em scp_codes, independentemente do valor de confiança. IRBBB não foi agregado. A ausência da chave significa ausência dessa anotação, não exclusão clínica de doença. As anotações derivam da interpretação do próprio ECG; não houve nova adjudicação clínica.

### Preditores e ausências
As 531 colunas ECGDeli resumem medidas extraídas do sinal, incluindo estatísticas e contagens; não representam 531 quantidades fisiológicas independentes. Não foram incluídos códigos diagnósticos, laudos, identificadores ou metadados diagnósticos como preditores. A auditoria não identificou vazamento direto de rótulos na lista autorizada. Contudo, medidas de duração e morfologia se relacionam aos critérios usados na anotação, o que limita a interpretação clínica da discriminação.

O painel reduzido contém QRS_Dur_Global, RR_Mean_Global, QRS_Dur_V1, R_Amp_V1, S_Amp_V1, QRS_Dur_V6, R_Amp_V6 e S_Amp_V6. Durações são expressas em milissegundos e amplitudes em milivolts, preservando sinal. O painel foi definido após exploração inicial de disponibilidade, antes do treinamento; não foi uma seleção externa independente. Ausências explícitas foram preservadas; zero não foi convertido automaticamente em ausência.

### Partições e desenvolvimento
Folds oficiais 1–8: 17.418 exames, 15.023 pacientes e 432 exames positivos. Fold 9: 2.183 exames, 1.942 pacientes e 55 positivos. Fold 10: 2.198 exames, 1.904 pacientes e 54 positivos. Não houve pacientes compartilhados entre partições.

Regressões logísticas L2 utilizaram lbfgs e padronização aprendida no treino. O parâmetro C foi escolhido entre 0,01; 0,1; 1; 10 por validação deixando um fold oficial de desenvolvimento de fora, minimizando Brier agregado fora do treino; empate até 10⁻⁶ favoreceu menor C. Imputação, padronização e regras de colunas foram ajustadas somente no treino correspondente. Não houve ponderação de classes, sobreamostragem ou recalibração. Os modelos finais utilizaram apenas folds 1–8. C selecionado: 0,01 para E1/E3/E3-I; 10 para E2/E2-C. Controles adicionais fixaram C=1.

O fold 9 definiu limiares pelo menor valor que atendesse à especificidade empírica de pelo menos 95%, conforme implementação congelada. Seu desempenho também orientou nossa interpretação exploratória, mas não modificou os modelos após o congelamento. Os limiares constam da tabela reproduzível. A análise final não foi precedida por registro público prospectivo; houve exploração prévia e conhecimento de contagens do teste, mas não de suas previsões antes da execução final.

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

Os controles E1/E2-C distinguem conjuntos de variáveis na mesma população de treinamento; E2-C/E2 investigam mudança de treinamento. Eles não tornam causal o contraste primário, que altera simultaneamente painel e tratamento operacional de ausência.

### Avaliação e integridade
O desfecho primário foi Brier(E3) − Brier(E2-fallback), pareado nos mesmos exames. Brier é a média do erro quadrático entre probabilidade e alvo binário; menor é melhor. O suporte direcional exigia limite superior do IC95% abaixo de zero. Não foi definida margem de equivalência.

Os intervalos percentis utilizaram 2.000 reamostragens de pacientes, semente 20261104, mantendo todos os exames de cada paciente sorteado e os mesmos sorteios entre comparadores. O estimando principal pondera exames igualmente, enquanto o agrupamento respeita dependência intrapaciente. A incerteza é condicional aos modelos treinados, sem refazer seu desenvolvimento. ROC-AUC, Average Precision (AP), calibração, cobertura e contrastes adicionais são secundários; não houve correção de multiplicidade que permitisse promovê-los a confirmações independentes.

A Fase 6 gerou uma única execução preditiva, com modelos, transformações e limiares congelados. A Fase 7 somente leu agregados existentes para redação e figuras. Hashes dos 57 arquivos do manifesto da Fase 5 e dos 31 arquivos do manifesto de entrega da Fase 6 permaneceram íntegros. Testes e verificações de correspondência entre probabilidades individuais e predictions.csv estão registrados na Fase 6. Não foram repetidas previsões nesta fase.

## Resultados

### Cobertura e população
A exigência das 531 medidas completas reteve 1.088/2.198 exames (49,50%) e 35/54 positivos (64,81%). Os 1.110 exames incompletos incluíram 19 positivos. Portanto, no teste, positivos foram proporcionalmente menos excluídos que o conjunto total. Todos os exames tinham as oito medidas: E2 e E2-fallback coincidiram e o mecanismo de fallback não foi avaliado empiricamente nesse conjunto.

A prevalência da anotação foi 3,22% nos completos e 1,71% nos incompletos. Havia 1.021 e 1.013 pacientes nesses estratos, com 130 pacientes em ambos; suas contagens não são aditivas. A idade mediana foi 62 e 64 anos, respectivamente, com as regras de valores indisponíveis da análise original. Trata-se de composição descritiva, não de demonstração do mecanismo de ausência.

### Comparação primária
E3 apresentou Brier 0,006042 (IC95% 0,003899–0,008592), contra 0,006655 (0,004333–0,009163) de E2-fallback. A diferença pareada foi −0,000613 (−0,002380 a +0,001133). A hipótese de superioridade de E3 não recebeu suporte estatístico. O intervalo admite vantagem ou desvantagem e não demonstra equivalência.

### Análises secundárias
|Estratégia|Exames|Brier|ROC-AUC|AP|
|---|---:|---:|---:|---:|
|B0|2.198|0,023964|0,500000|0,024568|
|E1, população completa|1.088|0,005830|0,998616|0,953360|
|E2-C|2.198|0,007052|0,996994|0,863493|
|E2 / E2-fallback|2.198|0,006655|0,997141|0,862865|
|E3|2.198|0,006042|0,997625|0,909119|
|E3-I|2.198|0,006089|0,997607|0,908265|
|Híbrida|2.198|0,005384|0,998152|0,909652|

Fonte: reports/phase6/final001/metrics.json, overall. Tabela integral com IC, limiares e métricas binárias: [tabelas/metricas.md](tabelas/metricas.md). O resultado de E1 não deve ser ordenado diretamente com os das estratégias que atendem todos os exames.

A híbrida teve o menor Brier pontual entre as estratégias de cobertura integral. Sua diferença para E2-fallback foi −0,001271 (IC95% −0,002821 a +0,000121), secundária e inconclusiva. Indicadores de ausência não evidenciaram benefício: E3-I menos E3 foi +0,000047 (−0,000020 a +0,000129).

Nos completos, Brier de E2 foi 0,008397 e de E3, 0,005856; nos incompletos, 0,004947 e 0,006223. São contrastes descritivos dentro de cada estrato; não se deve atribuir a diferença entre estratos a uma dificuldade intrínseca sem considerar prevalência e composição.

E2-fallback, E3 e híbrida tiveram sensibilidade observada de 100% nos limiares congelados, com especificidades de 95,43%, 96,08% e 96,13%. Os IC bootstrap de sensibilidade [1;1] são degenerados: todos os positivos observados foram classificados corretamente, e reamostrar esses mesmos pacientes não cria falsos negativos. Isso não demonstra sensibilidade populacional perfeita. Não calculamos novo intervalo que ignorasse o agrupamento.

Probabilidades médias foram 0,023867, 0,024421 e 0,024019, respectivamente, ante prevalência 0,024568. Intercepto/inclinação de calibração foram 0,294/1,274; 0,224/1,235; e 0,427/1,456. Esses diagnósticos existentes não foram usados para recalibrar. Faixas de probabilidade contêm poucos eventos e não sustentam calibração fina.

### Comparação descritiva com fold 9
No fold 9, E2-fallback teve Brier 0,007983 e E3, 0,008256; a diferença foi +0,000273 (IC95% −0,001586 a +0,001984). A ordenação pontual se inverteu no teste, mas ambos os intervalos incluem zero. O painel reduzido permaneceu numericamente competitivo; equivalência não foi testada.

A cobertura completa dos positivos passou de 40,00% no fold 9 a 64,81% no teste. Nos completos/incompletos do fold 9 havia 22/1.137 e 33/1.046 positivos. A direção da diferença de prevalência entre estratos mudou. Essa heterogeneidade é compatível com composição e incerteza amostral; não estabelece data drift nem seu mecanismo.

## Discussão
O principal resultado é a combinação de perda importante de cobertura sob completude estrita e comparação probabilística inconclusiva entre estratégias operacionais na população integral. O painel reduzido alcançou todos os exames de teste, mas o desenho não permite concluir que oito medidas sejam universalmente suficientes.

Os benchmarks de PTB-XL+ já estabelecem o interesse de características tabulares [2]. Estudos sobre dados ausentes demonstram a importância de alinhar desenvolvimento e aplicação [3,4]. Acrescentamos um caso reproduzível de ECG com denominadores explícitos, controles e resultado primário negativo/inconclusivo. Isso constitui contribuição incremental; a busca direcionada não comprova que a combinação exata seja inédita.

Comparar modelos apenas em suas populações atendidas pode confundir modelo e seleção. O Brier de E1 refere-se a uma população com prevalência diferente. A comparação primária pareada evita essa confusão de denominadores, mas não separa o efeito causal da imputação daquele da mudança de variáveis.

Nossa seleção por disponibilidade difere da classificação seletiva aprendida por confiança [5]. O estudo não estima uma curva ótima de risco–cobertura. Tampouco demonstra que ausências sejam aleatórias ou que exista uma direção universal de exclusão de positivos.

AUCs próximas de um podem refletir a proximidade entre medidas do sinal e os critérios usados na interpretação do próprio ECG. Isso é compatível com reconhecimento de anotação, mas não equivale a diagnóstico independente, validação clínica ou identificação de benefício ao paciente. Calibração e discriminação precisam ser avaliadas separadamente [6]. A experiência mais ampla com modelos de ECG também recomenda cautela ao traduzir resultados de benchmarks para aplicação [7].

## Limitações
Amostra de apenas 54 exames positivos em 45 pacientes limita sensibilidade, AP, calibração e análises de subgrupos. Não foi demonstrada precisão suficiente para equivalência ou segurança clínica. O bootstrap não incorpora a variabilidade de todo o desenvolvimento e apresenta degeneração para sensibilidade.

Há um único recurso público e alvo derivado da interpretação do ECG, sem adjudicação independente ou validação externa. O painel resultou de exploração inicial. Os folds 9 e 10 tiveram composição distinta, e o teste não foi completamente cego quanto a contagens. Não identificamos o mecanismo de ausência nem testamos transportabilidade entre serviços, aparelhos ou populações.

A calibração foi resumida por faixas fixas, intercepto e inclinação; poucos eventos restringem sua interpretação. Variáveis codificadas numericamente e a interpretação clínica de algumas medidas globais exigem revisão especializada. A estratégia de fallback não foi acionada no teste. Resultados secundários múltiplos não confirmam superioridade da híbrida.

## Conclusão
No teste interno reservado, exigir todas as medidas reduziu cobertura e selecionou uma composição distinta. A comparação primária não sustentou superioridade de 531 medidas imputadas sobre oito medidas com fallback, nem estabeleceu equivalência. A contribuição é uma análise metodológica incremental da relação entre disponibilidade, população avaliada e desempenho, restrita ao reconhecimento de uma anotação.

## Figuras e material reproduzível
1. [Fluxograma](figuras/01_fluxograma.png): partições e denominadores, com sobreposição intrateste explicitada.
2. [Cobertura](figuras/02_cobertura.png): exames e positivos atendidos.
3. [Brier pareado](figuras/03_brier_pareado.png): contraste primário e secundários na população integral.
4. [Calibração](figuras/04_calibracao.png): pontos por faixas fixas e seus denominadores; descritivo.
5. [Composição](figuras/05_composicao.png): proporção positiva por completude e fold.

Arquivos vetoriais e PDF correspondentes disponíveis. O script scripts/fase7_materials.py apenas renderiza os resultados anteriores. Requisitos e verificação em reports/phase7. Repositório público/DOI de arquivamento: **pendente**.

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

Relato orientado por TRIPOD+AI [8], ainda sem declaração de conformidade integral.
