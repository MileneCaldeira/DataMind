# Literatura e busca exploratória

Data: 03/11/2026. Busca orientada por fontes primárias via busca web, páginas UCI, PubMed/PMC, CDC, NeurIPS e arXiv. **Não é revisão sistemática, nem demonstração de originalidade.** A leitura foi de metadados, resumos e trechos disponíveis; não se afirma leitura integral de todos os artigos. Não foi feita busca exaustiva de trabalhos de 2025–2026.

| Referência verificada | Utilidade para o projeto | Limite |
|---|---|---|
| Kahn et al. (2016), [A Harmonized Data Quality Assessment Terminology and Framework](https://pubmed.ncbi.nlm.nih.gov/27713905/), DOI 10.13063/2327-9214.1244 | Estruturar avaliação de qualidade e explicitar o que cada regra mede | Não prova que uma regra particular é clinicamente correta |
| Detrano et al. (1989), [International application of a new probability algorithm](https://pubmed.ncbi.nlm.nih.gov/2756873/), DOI 10.1016/0002-9149(89)90524-9 | Contexto clínico e avaliação entre centros já estudada | As coortes descritas no artigo não têm os mesmos tamanhos de todos os arquivos processados atuais |
| Hohman et al. (2024), [Validation of MENDS Data](https://www.cdc.gov/pcd/issues/2024/23_0409.htm), DOI 10.5888/pcd21.230409 | Exemplo aplicado de validação de fontes e transformações de dados de saúde | Não implica acesso aberto aos microdados MENDS |
| CDC, [BRFSS 2015: documentação](https://www.cdc.gov/brfss/annual_data/annual_2015.html) e [overview](https://www.cdc.gov/brfss/annual_data/2015/pdf/overview_2015.pdf) | Desenho amostral, ponderação e limites de inferência populacional | O CSV UCI não teve sua linhagem até esse ano demonstrada |
| Ding et al. (2021), [Retiring Adult: New Datasets for Fair Machine Learning](https://proceedings.nips.cc/paper_files/paper/2021/hash/32e54441e6382a7fbacbbbaf3c450059-Abstract.html) | Limitações do Adult e alternativa ACS/Folktables para variação temporal/geográfica | ACS/Folktables não foi baixado/auditado nesta etapa |
| Fabris et al. (2022), [Algorithmic Fairness Datasets: the Story so Far](https://arxiv.org/abs/2202.01711), DOI 10.1007/s10618-022-00854-z | Documentação e adequação dos benchmarks de equidade | Não define uma única métrica de equidade apropriada a todo problema |
| Gebru et al., [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) (preprint inicial 2018) | Registrar origem, população, transformações e usos pretendidos | Documentar não elimina viés |
| Kapoor e Narayanan (2023), [Leakage and the reproducibility crisis in machine-learning-based science](https://pmc.ncbi.nlm.nih.gov/articles/PMC10499856/), DOI 10.1016/j.patter.2023.100804 | Projetar validações futuras sem vazamento | Padrões repetidos nesta auditoria não demonstram, sozinhos, vazamento de pessoas |

Consultas executadas incluíram `site.archive.ics.uci.edu dataset 45 heart disease license`, `site.archive.ics.uci.edu diabetes health indicators 891`, `site.archive.ics.uci.edu adult dataset license`, `site.pubmed.ncbi.nlm.nih.gov Kahn 2016 harmonized data quality assessment electronic health record`, `site.proceedings.neurips.cc Retiring Adult New Datasets Fair Machine Learning 2021`, `site.cdc.gov brfss 2015 annual data weighting missing values`, `"heart disease" "data quality" missing multicenter benchmark` e `"diabetes health indicators" "duplicates"`. Resultados de terceiros não foram usados como comprovação de licença ou de originalidade.

## Lacunas candidatas a confirmar

1. **Saúde multicêntrica:** em que medida regras explícitas de completude e plausibilidade mudam a população utilizável e a comparabilidade entre centros? Contribuição candidata: protocolo auditável com análise de sensibilidade e validação em mais de uma base. A mera identificação de ausentes ou comparação entre hospitais não é inédita.
2. **Inquéritos de saúde:** como seleção de casos completos, categorização e eliminação de perfis repetidos afetam composição e estatísticas descritivas? Contribuição candidata: comparação rastreável entre microdados originais e derivados. Depende de resolver ano, regras de transformação e pesos; não foi executada.
3. **Fora da saúde:** como decisões de limpeza e particionamento alteram a representação de grupos em benchmarks tabulares? Contribuição candidata: auditoria de estabilidade dos resultados descritivos, com extensão a ACS. Criticar Adult ou discutir fairness já tem literatura extensa.

## Próxima revisão, antes de fechar o tema

Pesquisar combinações de `data quality`, `missingness`, `data cleaning`, `duplicate profiles`, `dataset shift`, `fairness`, `BRFSS`, `UCI Heart Disease` e `ACS`; ampliar para trabalhos de 2020–2026 e referências fundamentais. Incluir estudos com método explícito, base identificável e avaliação reprodutível; registrar separadamente os sem código/dados. Excluir tutoriais e simples rankings de classificadores como evidência de contribuição metodológica. Registrar por estudo: pergunta, dados/versão, regras, unidade de análise, avaliação, artefatos, limitações e sobreposição com a proposta. Fazer rastreamento de referências e citações dos artigos acima. Só então formular a contribuição e os critérios de sucesso.
