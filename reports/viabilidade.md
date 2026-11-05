# DataMind — diagnóstico de viabilidade

**Data:** 03/11/2026, America/Sao_Paulo. **Escopo:** acesso, auditoria descritiva e escolha provisória de linha de pesquisa. Nenhum modelo preditivo construído.

Recomendo começar por **qualidade de dados e condições de comparabilidade entre centros em saúde**, usando UCI Heart Disease como piloto pequeno e reproduzível. A experiência da pesquisadora em SQL, modelagem de dados e qualidade é diretamente aproveitável. O acesso técnico foi resolvido para esse piloto; relevância e originalidade de uma tese/artigo ainda dependem de revisão e de validação adicional. Não recomendo simplesmente substituir MIMIC/eICU pelo Heart Disease e manter as mesmas pretensões de transportabilidade clínica.

## 1. Três direções possíveis

| Direção e pergunta candidata | Dados e unidade | Entrega científica possível, ainda não demonstrada |
|---|---|---|
| **A. Qualidade de dados multicêntricos em saúde.** Como completude, codificação e regras de plausibilidade alteram quais registros podem ser comparados entre centros? | UCI Heart Disease; uma linha clínica por registro, quatro arquivos de centros | Protocolo de auditoria e análise de sensibilidade das populações elegíveis, com validação externa posterior |
| **B. Confiabilidade de derivados de inquéritos de saúde.** Que informação e representatividade se perdem ao transformar um inquérito em benchmark de IA? | CDC Diabetes Health Indicators/UCI; linha de respondente conforme catálogo. BRFSS original como fonte de referência a reconstruir | Estudo de proveniência, seleção, categorização, pesos e efeitos descritivos de regras de limpeza |
| **C. Qualidade de dados para avaliação de equidade fora da saúde.** Como limpeza, perfis repetidos e particionamento afetam representação de grupos? | UCI Adult; linha individual de dados censitários. ACS/Folktables como extensão futura | Avaliação reproduzível da sensibilidade de indicadores por grupo e adequação dos benchmarks |

São perguntas de investigação, não descobertas nem alegações de novidade. A relação com confiabilidade de IA está na validade dos dados e do desenho de avaliação; nesta fase não se mede confiabilidade de um modelo.

## 2. Acesso efetivamente verificado e recursos

Todos os arquivos abaixo tiveram **GET HTTP 200, bytes gravados, hash SHA-256 e leitura bem-sucedida**, sem login, pagamento, treinamento obrigatório ou credenciamento nesta sessão. Os originais estão em `data/raw/`; os logs e hashes em [access_log.jsonl](access_log.jsonl). Não houve falha nos seis downloads registrados de dados/metadados. Isso não garante disponibilidade futura.

| Conjunto | Tamanho efetivamente recebido | Escopo auditado | Licença e condição |
|---|---:|---|---|
| [Heart Disease/UCI](https://archive.ics.uci.edu/dataset/45/heart+disease) | ZIP: 128.894 bytes | Quatro arquivos processados completos, 920 linhas, 14 campos cada | CC BY 4.0 declarada no catálogo; atribuição necessária |
| [Adult/UCI](https://archive.ics.uci.edu/dataset/2/adult) | ZIP: 620.237 bytes | Treino e teste históricos completos, 48.842 linhas, 15 campos | CC BY 4.0 declarada no catálogo; atribuição necessária |
| [CDC Diabetes/UCI](https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators) | CSV: 13.494.568 bytes | 253.680 linhas, 23 campos: ID, alvo e 21 atributos | Acesso confirmado; licença específica da derivação não confirmada |

Inventários dos ZIPs: [Heart](heart_archive.json) e [Adult](adult_archive.json), incluindo tamanhos descomprimidos por membro. O diagnóstico auditou os arquivos processados Heart, não todos os arquivos clínicos originais do ZIP. O tamanho de 303 linhas mostrado no catálogo Heart não descreve a soma dos quatro arquivos.

Recursos observados: Windows 11, Python 3.13.7, 17.089.736.704 bytes de RAM instalada (aprox. 15,9 GiB), 12 processadores lógicos e cerca de 535 GiB livres em disco. A execução inicial de download e auditoria levou **15,145 segundos**. Não foi medido pico de memória, disponibilidade instantânea de RAM nem custo futuro de modelagem. A execução concluída demonstra suficiência para esta auditoria; não se exige GPU ou nuvem. Código sem dependências externas reduz o esforço de reprodução.

Fonte oficial adicional: [BRFSS 2015/CDC](https://www.cdc.gov/brfss/annual_data/annual_2015.html) publica documentação e informa 441.456 registros e ZIP ASCII de 64,3 MB. **Esse arquivo não foi baixado nem auditado.** A página ajuda a dimensionar uma extensão, mas não resolve a linhagem do CSV UCI. [ACS/Folktables](https://github.com/socialfoundations/folktables) foi identificado na literatura; acesso aos seus microdados, tamanho por recorte e termos específicos não foram testados. Nenhuma dessas extensões recebe o mesmo status de viabilidade comprovada dos três downloads.

## 3. Método da auditoria

O script [audit.py](../scripts/audit.py) lê os arquivos completos, valida largura das linhas, produz perfil por coluna, valores distintos, extremos numéricos, tokens de ausência, contagens de alvos, repetições e tabelas descritivas por grupos disponíveis. Tipos são inferidos pela representação, não pelo significado: um código inteiro pode ser categoria nominal ou ordinal.

Ausentes são apenas tokens explícitos (`?`, vazio, `NA`, `NaN`, `nan`, `null`). Zeros não foram recodificados. “Duplicadas” na tabela significa **excedente de linhas com valores idênticos**, retirando ID quando presente, e não número de pessoas repetidas. Não há identificadores suficientes para verificar unicidade de pessoas nos arquivos Heart e Adult. A auditoria de repetição usa strings após remoção de espaços; não é uma resolução de entidades nem uma comparação numérica tolerante entre centros.

Adult: o comentário inicial do teste é ignorado e o ponto final dos rótulos é removido; os arquivos originais permanecem intactos. As amostras são as primeiras 20 linhas e servem somente para conferir o esquema. Todos os números seguintes vêm da auditoria integral, não dessas amostras. Não houve imputação, exclusão, deduplicação ou treino.

## 4. Resultados observados

Fonte computacional: [audit.json](audit.json), com resultados por coluna e por grupo; referência inicial preservada em [baseline/audit.json](baseline/audit.json).

| Arquivo | Linhas | Células ausentes | Linhas com algum ausente | Repetições excedentes sem ID | Alvo observado |
|---|---:|---:|---:|---:|---|
| Heart Cleveland | 303 | 6 | 6 | 0 | `num`: 0=164; 1=55; 2=36; 3=35; 4=13 |
| Heart Hungarian | 294 | 782 | 293 | 1 | `num`: 0=188; 1=106 |
| Heart Switzerland | 123 | 273 | 123 | 0 | `num`: 0=8; 1=48; 2=32; 3=30; 4=5 |
| Heart VA | 200 | 698 | 199 | 1 | `num`: 0=51; 1=56; 2=41; 3=42; 4=10 |
| Adult treino | 32.561 | 4.262 | 2.399 | 24 | `<=50K`: 24.720; `>50K`: 7.841 |
| Adult teste | 16.281 | 2.203 | 1.221 | 5 | `<=50K`: 12.435; `>50K`: 3.846 |
| Adult combinado | 48.842 | 6.465 | 3.620 | 52 | `<=50K`: 37.155; `>50K`: 11.687 |
| Diabetes | 253.680 | 0 | 0 | 24.206 | `Diabetes_binary`: 0=218.334; 1=35.346 |

### A. Heart: piloto viável, comparabilidade exige cuidado

Esquema: `age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, num`. Centro é informação do arquivo, não uma coluna original. Não há sequência longitudinal, identificação estável de paciente ou datas para avaliar mudança temporal. O alvo se refere a diagnóstico, não a um evento futuro.

Em Cleveland, ausências explícitas estão em `ca` (4) e `thal` (2). Nos demais centros, `ca` falta em 291/294, 118/123 e 198/200 registros, respectivamente. Exigir completude dos 14 campos deixaria 297 registros de Cleveland, 1 da Hungria, nenhum suíço e 1 do VA. Essa é uma consequência descritiva da regra de casos completos, não uma política recomendada.

**Alerta semântico observado:** todos os 123 valores de `chol` da Suíça são zero; no VA há 49 zeros, além de sete `?`. “Nenhum ausente explícito” em `chol` suíço não significa medição utilizável. O significado desses zeros precisa ser validado na documentação ou com apoio clínico, sem recodificação silenciosa.

O alvo húngaro só apresenta 0/1, enquanto outros arquivos contêm 0–4. A eventual harmonização binária `num > 0` exige justificativa. O artigo de [Detrano et al.](https://pubmed.ncbi.nlm.nih.gov/2756873/) descreve amostras húngara e suíça maiores que os arquivos processados disponíveis. Não se pode assumir reprodução da coorte integral do artigo.

**Implicação:** boa base para aprender e testar regras, fraca base isolada para conclusão clínica atual. Amostra pequena, histórica e selecionada; diferenças de centro podem refletir coleta, seleção e codificação, além de composição clínica. Não foi testada transportabilidade de modelos.

### B. Diabetes: acesso fácil, proveniência ainda insuficiente

O CSV contém ID e alvo binário, além de indicadores de saúde, comportamento, acesso e categorias demográficas. `Age` é código de faixa etária, não idade em anos. Ausência de tokens faltantes não estabelece qualidade da coleta original: o arquivo pode ter passado por seleção ou recodificação não inteiramente documentada.

Com ID, não há linhas completas idênticas; sem ele há 24.206 excedentes. Existem ainda **1.566 padrões de atributos associados a mais de um valor do alvo**. Isso pode ocorrer com categorização e atributos incompletos para descrever uma pessoa; não demonstra erro de rótulo. Não eliminar tais registros automaticamente.

A API/catalogação descreve simultaneamente 35 atributos em texto, 21 no esquema e três classes na narrativa, embora o arquivo tenha alvo binário. A descrição do alvo no catálogo agrupa pré-diabetes/diabetes em 1; **essa semântica não foi validada contra a transformação original**. Há referência a BRFSS 2014 e a uma derivação externa. Não é seguro rotular o CSV como extração verificada de BRFSS 2015 apenas por semelhança de tamanho.

Não existem no CSV campos explícitos de estado, ano, estrato, unidade primária amostral e peso final do inquérito. Os 35.346 positivos (aprox. 13,93%) são frequência não ponderada no arquivo, não estimativa populacional de diabetes. A [documentação BRFSS](https://www.cdc.gov/brfss/annual_data/2015/pdf/overview_2015.pdf) fundamenta a importância dos pesos para generalização.

**Implicação:** excelente caso para investigar proveniência, mas opção condicionada. É preciso recuperar transformação, ano, definição de alvo e termos de uso; alternativamente, trabalhar diretamente com fonte oficial e desenho amostral adequado. Não há fundamento para uso clínico individual.

### C. Adult: alternativa acessível fora da saúde

Esquema: 14 atributos demográficos/socioeconômicos e alvo `income`. `fnlwgt` é peso, não identificador; `education-num` codifica escolaridade. Os ausentes explícitos estão em `workclass` (2.799), `occupation` (2.809) e `native-country` (857) no conjunto combinado.

Foram encontrados **23 padrões completos distintos compartilhados entre treino e teste históricos**, após normalizar rótulos. Isso merece investigação para futuros protocolos, mas não prova que uma pessoa aparece nas duas partições. Há cinco padrões de atributos com alvos diferentes no conjunto combinado. As tabelas por `sex` e `race` estão no JSON; não foram calculadas métricas de desempenho ou discriminação de modelos.

O [catálogo UCI](https://archive.ics.uci.edu/dataset/2/adult) informa origem censitária de 1994, seleção prévia de registros e alvo de renda acima de US$ 50 mil. Categorias históricas e um limiar antigo limitam validade atual. [Ding et al.](https://proceedings.nips.cc/paper_files/paper/2021/hash/32e54441e6382a7fbacbbbaf3c450059-Abstract.html) já discutem limitações e oferecem uma alternativa baseada em ACS; o Adult deve ser piloto, não evidência suficiente de novidade em equidade.

## 5. Literatura, lacunas e força da evidência

O [registro de literatura](../docs/literatura.md) reúne oito referências/documentos, links, consultas e limitações. Kahn oferece base para organizar qualidade; Hohman traz aplicação recente em saúde; Gebru fundamenta documentação; Kapoor/Narayanan discutem vazamento e reprodução; Ding e Fabris orientam os limites de fairness benchmarks. A revisão é exploratória, não sistemática.

As lacunas candidatas são: sensibilidade da comparabilidade entre centros às regras de qualidade (A); perda de informação na transformação de inquéritos (B); e estabilidade da representação de grupos sob políticas de preparação dos dados (C). A contribuição teria de ser demonstrada por protocolo, comparação explícita de políticas e validação em dados independentes. **Encontrar ausentes e duplicidades em bases conhecidas não basta como contribuição científica.**

## 6. Comparação e recomendação

Avaliação qualitativa baseada na auditoria e no perfil informado; não é pontuação estatística. Esforços abaixo são estimativas de planejamento para aprofundar o diagnóstico, supondo 6–8 horas semanais e acesso mantido, não para concluir artigo ou dissertação.

| Critério | A — qualidade multicêntrica | B — inquéritos/derivação | C — qualidade e equidade |
|---|---|---|---|
| Relevância potencial | Alta para validade de pesquisa em saúde | Alta para interpretação e representatividade | Alta para avaliação responsável de IA |
| Viabilidade técnica imediata | Alta; quatro arquivos auditados | Alta para CSV, condicionada para estudo de proveniência | Alta para Adult; extensão ACS não testada |
| Clareza de uso | Licença explícita | Licença da derivação pendente | Licença explícita |
| Esforço de próximo piloto | Baixo–médio; 2–4 semanas | Médio–alto; 4–8 semanas ou mais conforme linhagem | Médio; 3–6 semanas |
| Conhecimento especializado | Estatística descritiva e apoio clínico para regras | Epidemiologia, amostragem complexa e documentação de ETL | Estatística, equidade e contexto socioeconômico |
| Adequação ao perfil atual | Muito alta | Alta em ETL/qualidade, maior lacuna estatística | Alta em dados, requer formação em fairness |
| Risco científico principal | Benchmark antigo/pequeno e contribuição incremental | Confusão de alvo, ano e inferência sem pesos | Benchmark saturado e conclusões normativas indevidas |

**Recomendação provisória: A.** Título de trabalho: “Avaliação reproduzível da qualidade e comparabilidade de dados tabulares multicêntricos em saúde”. Primeira entrega: matriz de regras, proveniência, diferenças entre centros e sensibilidade descritiva das populações elegíveis. Isso preserva a opção de saúde e aproveita competências já consolidadas, sem depender inicialmente de ML avançado.

Critérios para confirmar a linha: (1) revisão mostrar pergunta não suficientemente respondida; (2) regras críticas terem respaldo documental/clínico; (3) existir segunda base adequada e acessível para validar o protocolo. Se não se cumprirem, reduzir a ambição a estudo metodológico de reprodução ou migrar para C com expansão de dados verificada. B deve avançar somente após resolver linhagem/licença, porque o acesso fácil ao CSV não resolve a validade do estudo.

## 7. Tentativas malsucedidas e limites

| Tentativa/questão | Resultado efetivo | Causa ou limite e consequência |
|---|---|---|
| Ler página externa Kaggle apontada pela API de diabetes | Navegador de pesquisa retornou página sem linhas legíveis | Causa técnica específica não determinada; não confirmar licença com conteúdo ausente. Nenhum download Kaggle foi tentado |
| Reconciliar descrição e esquema de diabetes pela UCI/API | Não resolvido: narrativa, esquema e referência de ano não bastam | Metadados inconsistentes; requer fonte da transformação, não suposição |
| Downloads UCI (três metadados e três arquivos) | Todos bem-sucedidos | Sem falhas de download nesta execução; consultar log HTTP e hashes |
| Consultar último commit Git | Falhou: branch `master` ainda sem commits | Repositório novo, não falha dos dados |
| MIMIC-IV/eICU | Não retestados | Obstáculo histórico relatado pela pesquisadora; nenhuma alegação de erro de servidor nesta sessão |

Não foram feitas revisão sistemática, auditoria clínica independente, validação da seleção original, identificação de pessoas repetidas, teste de hipóteses, inferência causal ou modelagem. Semântica de sentinelas e equivalência de variáveis entre centros continuam pendentes. A ausência de um código de missing no CSV não demonstra ausência de informação perdida a montante.

## 8. Reprodução e próximos passos

O [README](../README.md) contém os comandos. A execução offline deve reproduzir exatamente o JSON de auditoria e os hashes iniciais; tempos de execução e data naturalmente variam. `scripts/verify.py` valida isso e sinaliza mudanças de fonte ou código.

O repositório contém decisões, atribuições, código, dados locais, pequenas amostras, logs e protocolo para [experimentos futuros](../experiments/README.md). O próximo passo científico é aprofundar a revisão e validar as regras semânticas da direção A; não treinar um classificador sobre esses arquivos para escolher o tema pelo melhor desempenho.
