# Heart Disease: documentação original e comparabilidade

Investigação de 03/11/2026. Fonte primária: membros `heart-disease.names`, `WARNING`, `ask-detrano`, `Index` e arquivos de dados no [ZIP UCI](https://archive.ics.uci.edu/static/public/45/heart+disease.zip), preservado desde a Fase 1. DOI [10.24432/C52P4X](https://doi.org/10.24432/C52P4X). Cópias documentais locais estão em `data/raw/phase2/`; hashes dos originais e resultados estão em `reports/phase2/`. A documentação é histórica e contém dúvidas explícitas, não um padrão clínico atual.

## Os 76 atributos e a projeção de 14

O dicionário enumera 76 campos, incluindo alvo e campos artificiais. O índice completo, gerado a partir dele, está em [attributes76.json](../reports/phase2/attributes76.json); a [tabela dos 76 campos](atributos_heart76.md) mostra posições, seleção e ausência nos arquivos estruturais legíveis. Não são 76 preditores utilizáveis.

| Grupo | Índices | Interpretação e limitações |
|---|---|---|
| Identificação | 1–2, 76 | `id`, `ccf`, `name`; documentação informa substituição de identificação sensível por valores artificiais. Não usar como chave global nem provar unicidade de pessoas |
| Demografia e sintomas | 3–9 | Idade, sexo codificado, localização/desencadeamento/alívio da dor e categoria de dor; `pncaden` descrito como soma dos componentes |
| História e medidas de repouso | 10–19 | Pressão, colesterol, tabagismo, glicemia, diabetes, história familiar e ECG; `htn` sem definição detalhada e `smoke` descrito com incerteza pelo curador |
| Data e medicações do exercício | 20–27 | Data de ECG e uso de medicações; existência de datas no bruto corrige qualquer leitura de que toda a base não tem datas. Não constitui acompanhamento longitudinal verificável |
| Protocolo e exercício | 28–44 | Protocolo, duração, frequência cardíaca, pressão, angina, ST, vasos; `dummy` e abreviações pouco definidas. `ask-detrano` registra dúvida sobre os códigos de protocolo |
| Exames complementares | 45–54 | Enzimas/fração de ejeção/movimento da parede e `thal`; vários campos marcados pelo dicionário como irrelevantes ou não usados, com grafia/interpretação incerta |
| Cateterismo e alvo | 55–58 | Datas e status angiográfico `num`; não confundir com risco futuro ou mortalidade |
| Territórios vasculares | 59–68 | `lmt`, `ladprox`, `laddist`, `diag`, `cxmain`, `ramus`, `om1`, `om2`, `rcaprox`, `rcadist`; não há definição completa dos códigos no dicionário |
| Campos adicionais | 69–75 | `lvx1`–`lvx4`, `lvf`, `cathef`, `junk`; indicados como não usados, sem base para tratá-los como medidas harmonizadas |

A projeção usada na Fase 1 é **3, 4, 9, 10, 12, 16, 19, 32, 38, 40, 41, 44, 51, 58**, nessa ordem. O arquivo bruto tem registros distribuídos em várias linhas; uma linha física não é um registro. O parser usa o terminador artificial `name` e exige 75 tokens anteriores, totalizando 76 campos. A verificação estrutural não assegura correção clínica.

## Centros, corrupção e versões

- Cleveland: 303 registros no processado. `WARNING` informa corrupção do bruto e recomenda o processado para os 14 atributos. A inspeção confirma blocos irregulares, portanto o bruto de Cleveland foi **excluído da projeção de 76 campos**, sem tentar recuperá-lo por suposição.
- Hungarian: 294 blocos de 76 campos; `reprocessed.hungarian.data` tem 294 linhas de 14 campos e coincide exatamente, como multiconjunto numérico, com a projeção do bruto após reconhecer −9. O arquivo `processed.hungarian.data` é outra versão, com alvo binário e uma diferença adicional em `ca`.
- Switzerland: 123 blocos de 76 campos. Os registros processados não preservam a mesma ordem dos brutos. O dicionário menciona Zurich e credita também Basel; não é possível separar essas instituições no processado.
- VA Long Beach: 200 blocos de 76 campos. Há diferenças pontuais de codificação no processado.

O estudo de [Detrano et al. (1989)](https://pubmed.ncbi.nlm.nih.gov/2756873/) descreve 303 registros de derivação em Cleveland e grupos externos de 425, 200 e 143. Esses números não autorizam expandir os arquivos UCI de 294 e 123 ou afirmar que são as coortes integrais do estudo. Também não demonstram que quatro arquivos equivalem a quatro hospitais operacionalmente homogêneos.

## Ausências, zeros e alterações entre versões

No dicionário bruto, ausência é **−9.0**; no material há formas `-9` e `-9.` numericamente equivalentes. Nos processados, aparece `?`. A Fase 1 estava correta para os processados, mas sua lista de tokens não deve ser reaplicada aos 76 campos sem essa adaptação. O código novo reconhece −9 numericamente em leitura separada, sem alterar a Fase 1.

| Comparação bruto → processado | Evidência observada |
|---|---|
| Hungarian | Categorias 2, 3 e 4 de `num` desaparecem e aumentam a contagem de 1; um `ca=9` dá lugar a uma ausência |
| Switzerland | Dois valores de `thal`, 1 e 4, dão lugar a ausências |
| VA | Um `slope=0` e sete códigos `thal` fora de {3,6,7} dão lugar a ausências |

Teste forense: uma transformação candidata que substitui **somente categorias fora dos domínios declarados** por ausência e binariza `num` **somente na Hungria** reproduz exatamente os multiconjuntos dos três processados. É uma explicação compatível com os bytes, **não recuperação comprovada do script histórico nem pareamento de indivíduos**. Essa transformação é isolada da análise de políticas, que continua usando os processados da Fase 1.

Zeros de `chol` já constam nos brutos suíço/VA; não são introduzidos apenas pelos processados. Isso não esclarece se representam sentinela, não coleta ou outro problema. Zero é válido em campos como `sex`, `fbs`, `exang`, `ca` e `oldpeak`; não foi convertido globalmente em ausência. Os 11 valores negativos de `oldpeak` suíços e um do VA são relatados sem exclusão automática, pois o significado do sinal não foi adjudicado.

## Alvo e limites semânticos

O texto geral documenta `num=0` versus presença nas categorias 1–4. A descrição detalhada de #58 liga 0 a estreitamento menor que 50% e 1 a maior que 50%; não resolve o caso exatamente igual a 50% nem os significados individuais de 2–4. `ask-detrano` pergunta se os níveis são ordenados. Portanto, **não interpretar 1–4 como escala ordinal de gravidade validada**. Para composição, usamos explicitamente `num>0`, sem substituir a coluna original.

Unidades de pressão e colesterol estão documentadas, mas não foram demonstrados calibração dos equipamentos, procedimentos de aquisição, seleção de casos, adjudicação ou equivalência do protocolo de exercício entre centros. Completude e domínio podem ser auditados; acurácia clínica e intercambialidade das medidas não podem ser estabelecidas apenas por estes arquivos.
