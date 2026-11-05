# Revisão direcionada — qualidade, harmonização e comparabilidade

**Corte: 03/11/2026.** Revisão direcionada para decisão de viabilidade, não revisão sistemática própria. Priorizamos revisões sistemáticas, escopo, diretrizes e fontes metodológicas; incluímos estudos específicos para avaliar sobreposição da proposta. Não houve dois revisores, protocolo registrado, busca exaustiva em bases assinadas ou avaliação formal de risco de viés. Não inferir ausência de publicação porque uma busca não a encontrou.

## Busca e rastreabilidade

Busca web em fontes primárias: PubMed/PMC, periódicos, UCI, PhysioNet, Maelstrom, OHDSI e repositórios de autores. Grupos de consultas efetivamente executadas:

1. `electronic health records data quality assessment systematic review harmonization multicenter Weiskopf Weng 2013 Schmidt 2021`
2. `"Methods and dimensions" "Weiskopf" 2013 data quality`; `"METRIC-framework" "2024" systematic review`
3. `"data quality framework" "Schmidt" "2021" observational health research`; `"Maelstrom" "harmonization" "guidelines" 2017`
4. `"multicenter" "data quality" "selection" "complete case" harmonization`; `"data quality" "cohort" "sensitivity" "harmonization" systematic review`
5. `"heart disease" "harmonization" "data quality" UCI`; título do artigo de Amin abaixo
6. `"PhysioNet" "2019" "missingness" "selection bias"`; `"PhysioNet" "2019" "missingness" hospital data quality`
7. `"missing data" "complete case" bias Sterne 2009 BMJ`
8. Buscas por títulos de Lewis, Hosseinzadeh e Bian para confirmar metadados; acesso a estudos de outubro de 2026 retornados nas buscas.

Critério de inclusão no núcleo: fonte primária acessível, pertinência a dimensões de qualidade, harmonização ou seleção e método identificável. Rankings de classificadores não servem como demonstração metodológica, mas estudos específicos de Heart/PhysioNet são úteis para detectar sobreposição. Blogs, resultados de agregadores e snippets sem fonte primária confirmada não sustentam conclusões. Não foram inventadas contagens de um fluxo PRISMA. A tabela seguinte é o conjunto selecionado de leitura, não todas as ocorrências das buscas.

## Síntese crítica das fontes

| ID / referência | Tipo e material consultado | O que já cobre | Limite e implicação para DataMind |
|---|---|---|---|
| R1 — Weiskopf & Weng, 2013, [Methods and dimensions…](https://pubmed.ncbi.nlm.nih.gov/22733976/), DOI 10.1136/amiajnl-2011-000681 | Revisão; resumo e trechos PMC | Taxonomia, presença de elementos, comparações de distribuições e verificações de validade | Listar ausentes e domínios não constitui método novo; qualidade depende do uso |
| R2 — Kahn et al., 2016, [A Harmonized Data Quality Assessment Terminology and Framework](https://pubmed.ncbi.nlm.nih.gov/27713905/), DOI 10.13063/2327-9214.1244 | Framework, fonte da Fase 1 | Conformidade, completude e plausibilidade; distinguir verificação de validação | Um alerta interno não é validação contra a verdade clínica |
| R3 — Bian et al., 2020, [Assessing the practice of data quality evaluation…](https://pmc.ncbi.nlm.nih.gov/articles/PMC7727392/) | Revisão de escopo sistemática; trechos indexados, abertura direta com desafio de navegador | Relaciona dimensões/métodos a avaliação em rede clínica | Fundamenta auditoria multicêntrica, mas não garante generalização para benchmarks históricos |
| R4 — Schmidt et al., 2021, [Facilitating harmonized data quality assessments](https://pubmed.ncbi.nlm.nih.gov/33810787/), DOI 10.1186/s12874-021-01252-7 | Framework metodológico e software R; resumo | Liga conceitos de qualidade a implementação reutilizável | Uma biblioteca Python de regras, por si só, não é contribuição inédita |
| R5 — Lewis et al., 2023, [Electronic health record data quality assessment and tools](https://pubmed.ncbi.nlm.nih.gov/37390812/), DOI 10.1093/jamia/ocad120 | Revisão sistemática; resumo, trechos indexados de métodos/discussão; PMC direto bloqueado | Atualiza abordagens e ferramentas de 2013 a abril de 2023 | Busca centrada em PubMed; demanda por ferramentas não significa inexistência de ferramentas |
| R6 — Schwabe et al., 2024, [METRIC-framework](https://pmc.ncbi.nlm.nih.gov/articles/PMC11297942/) e [versão dos autores](https://arxiv.org/abs/2402.13635) | Revisão sistemática; resumo e trechos | Dimensões de qualidade voltadas a dados de IA médica | Não afirmar criação do primeiro framework de confiabilidade; requer demonstrar utilidade incremental |
| R7 — Hosseinzadeh et al., 2025, [Data quality assessment in healthcare, dimensions, methods and tools](https://link.springer.com/article/10.1186/s12911-025-03136-y), DOI 10.1186/s12911-025-03136-y | Revisão sistemática; métodos/resultados/discussão consultados no editor | Mapeia dimensões, métodos e ferramentas para dados estruturados; busca em três bases até novembro de 2024 | Critérios excluem certos estudos apenas comparativos e dados não estáticos; não é evidência de que comparações de políticas ou séries temporais não existam |
| R8 — Kariuki et al., 2026, [Data Harmonization Methods and Data Quality Assessment…](https://pmc.ncbi.nlm.nih.gov/articles/PMC13684885/), DOI 10.63116/AH.000000007 | Revisão sistemática publicada em 21/10/2026; resumo/métodos/limitações | Síntese de 69 estudos de harmonização entre sistemas; indica necessidade de relato consistente e contexto | Sem avaliação formal de risco de viés; síntese descritiva não estabelece superioridade causal de uma técnica |
| R9 — Fortier et al., 2017, [Maelstrom Research guidelines](https://doi.org/10.1093/ije/dyw075); [guia oficial](https://mica.maelstrom-research.org/page/maelstrom-guidelines) | Diretriz; guia consultado | Protocolo, definição do esquema alvo, avaliação de potencial de harmonização, documentação | Reduzir colunas para aumentar retenção muda o esquema e precisa de justificativa científica |
| R10 — Sterne et al., 2009, [Multiple imputation… potential and pitfalls](https://pmc.ncbi.nlm.nih.gov/articles/PMC2714692/), DOI 10.1136/bmj.b2393 | Metodologia; metadados/trechos, acesso integral não obtido | Riscos de dados ausentes e pressupostos do tratamento | Não se pode escolher imputação ou presumir MAR por observar diferenças; nesta fase não foi implementada imputação |
| R11 — OHDSI, [DataQualityDashboard](https://ohdsi.github.io/DataQualityDashboard/) | Documentação oficial consultada | Regras parametrizadas, limiares e relatório auditável em OMOP CDM | Não foi instalado nem comparado experimentalmente; competir apenas por automação é contribuição fraca |
| R12 — Amin et al., 2025, [Harmonization of Heart Disease Dataset…](https://www.techscience.com/cmc/v82n3/59942/html), DOI 10.32604/cmc.2025.061645 | Estudo aplicado; metadados/resumo e descrição do pré-processamento | Já aplica harmonização/preparação em dados cardíacos para ML | Não foi reproduzido nem validada sua avaliação; a existência do estudo basta para rejeitar novidade baseada apenas em “harmonizar Heart” |
| R13 — Singh, Sato & Ohkuma, 2021, [On Missingness Features…](https://medinform.jmir.org/2021/12/e25022/), DOI 10.2196/25022 | Estudo observacional; resumo/discussão/limitações | Examina missingness, subgrupos e avaliação externa usando PhysioNet 2012/2019 | Usa modelagem e contextos específicos; missingness informativa e variação entre hospitais não são descobertas novas |
| R14 — Aaron et al., 2026, [When Missingness Identifies the Hospital](https://www.preprints.org/manuscript/202610.1449), v1, 15/10/2026 | **Preprint sem revisão por pares**, resumo | Estuda transferência A↔B, indicadores de observação e explicações em PhysioNet 2019 | Resultados não reproduzidos; sobreposição temática forte, sem tratá-los como consenso estabelecido |
| R15 — Siddappa et al., 2026, [Alert-List Concordance…](https://arxiv.org/abs/2610.22635), v1, 15/10/2026 | Manuscrito de autores; resumo; página informa aceite em workshop DMBIH 2026 | Compara estratégias de imputação e concordância de listas em PhysioNet 2019 | Não reproduzido; mostra que sensibilidade a preparação/seleção também possui trabalhos recentes |
| R16 — Ding et al., 2021, [Retiring Adult](https://proceedings.nips.cc/paper_files/paper/2021/hash/32e54441e6382a7fbacbbbaf3c450059-Abstract.html); Fabris et al., 2022, [Algorithmic Fairness Datasets](https://arxiv.org/abs/2202.01711) | Literatura de comparação com C, consultada na Fase 1 | Crítica ao Adult, documentação e alternativas ACS | Migrar para C não remove o problema da originalidade nem a necessidade de contexto |

Fontes dos datasets: [UCI Heart e documentos internos](heart_documentacao.md); [PhysioNet 2019](https://physionet.org/content/challenge-2019/1.0.0/) e [Reyna et al., 2020](https://pubmed.ncbi.nlm.nih.gov/31939789/), DOI 10.1097/CCM.0000000000004145. Não confundir ano do desafio com ano do volume do artigo.

## Questões consolidadas e questões ainda candidatas

| Afirmação possível | Avaliação após leitura |
|---|---|
| “Dados clínicos têm ausências, valores incompatíveis e heterogeneidade” | Já amplamente estabelecido; não é lacuna |
| “Completude é diferente de plausibilidade e acurácia” | Já estabelecido por frameworks |
| “Casos completos podem alterar composição e gerar seleção” | Problema metodológico conhecido; quantificar neste piloto é diagnóstico, não novidade |
| “Padronizar formato garante semântica” | Falso; diretrizes de harmonização já exigem equivalência conceitual contextual |
| “Missingness pode carregar informação do processo assistencial” | Já estudado, inclusive no PhysioNet 2019 |
| “Não existem ferramentas abertas de auditoria” | Falso: dataquieR, OHDSI e outros exemplos |
| “O efeito de decisões semânticas rastreáveis sobre a coorte elegível pode ser comparado com um relato apenas de completude” | Pergunta delimitada ainda a testar neste projeto; ausência de solução equivalente **não demonstrada** |
| “Um contrato de auditoria pode ser aplicado separadamente a dados estáticos e horários sem confundir denominadores” | Candidata a avaliação metodológica, mas exige comparação com práticas existentes e não é garantidamente original |

## O que falta para uma reivindicação de contribuição

Selecionar um comparador metodológico existente; mapear cada componente proposto a R1–R11 e explicitar o que excede aplicação de boas práticas. Ampliar busca de citações e estudos com “cohort attrition”, “fitness for use”, “data quality rules”, “sensitivity analysis”, “semantic harmonization” e “multiverse analysis”. Avaliar materiais suplementares e código dos trabalhos mais próximos, inclusive R12–R15; não basta ler resumos. Submeter regras a revisão clínica independente e definir avaliação antes de examinar novos recortes. Não concluir que “pouco relatado” equivale a “nunca estudado”.
