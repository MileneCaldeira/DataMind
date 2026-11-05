# Fontes, atribuições e limites

Verificação: 03/11/2026. Acesso anônimo aos arquivos foi confirmado, não apenas a existência de páginas.

| Dataset | Catálogo e DOI | Licença consultada | Arquivo acessado |
|---|---|---|---|
| Heart Disease | [UCI 45](https://archive.ics.uci.edu/dataset/45/heart+disease), [DOI](https://doi.org/10.24432/C52P4X) | CC BY 4.0 declarada pela UCI | [ZIP](https://archive.ics.uci.edu/static/public/45/heart+disease.zip) |
| Adult | [UCI 2](https://archive.ics.uci.edu/dataset/2/adult), [DOI](https://doi.org/10.24432/C5XW20) | CC BY 4.0 declarada pela UCI | [ZIP](https://archive.ics.uci.edu/static/public/2/adult.zip) |
| CDC Diabetes Health Indicators | [UCI 891](https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators), [DOI](https://doi.org/10.24432/C53919) | Catálogo remete à fonte externa; não foi possível confirmar licença específica da derivação | [CSV hospedado na UCI](https://archive.ics.uci.edu/static/public/891/data.csv) |

Heart Disease: criadores Andras Janosi, William Steinbrunn, Matthias Pfisterer e Robert Detrano. Adult: Barry Becker e Ronny Kohavi. [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) exige atribuição, referência à licença e indicação de alterações. As amostras deste projeto contêm somente as primeiras 20 linhas, cabeçalhos adicionados quando necessários, espaços normalizados e rótulos Adult sem ponto final. Não há endosso dos autores.

CDC Diabetes: a API aponta [Alex Teboul/Kaggle](https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset) como fonte externa, enquanto o resumo aponta BRFSS 2014. A página Kaggle não forneceu texto legível ao navegador de pesquisa. Não transferimos automaticamente uma licença de outro espelho nem a política geral do CDC para o CSV derivado. Consulta à [política do CDC](https://www.cdc.gov/other/agencymaterials.html) confirma que existem exceções ao domínio público. A referência ao CDC não implica endosso; materiais originais estão disponíveis gratuitamente no site da agência.

As páginas de catálogo e APIs não substituem o dicionário clínico nem garantem proveniência completa. Os hashes comprovam os bytes usados, não a autenticidade clínica dos registros. Downloads foram locais, não publicados. Arquivos em `data/raw/` e amostra de diabetes estão excluídos do Git.
