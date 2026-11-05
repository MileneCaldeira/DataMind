# Fontes e limitações — Fase 2

Data de referência 03/11/2026, America/Sao_Paulo. Horários dos downloads em UTC no log. Este registro complementa as atribuições e limitações da Fase 1, sem substituir o histórico.

| Evidência | Origem | Preservação / status |
|---|---|---|
| 14 campos e versões brutas Heart | ZIP UCI da Fase 1, DOI 10.24432/C52P4X | SHA-256 anterior mantido; resultados em `reports/phase2/heart_analysis.json` |
| Dicionário/avisos históricos | `heart-disease.names`, `WARNING`, `ask-detrano`, `Index` do mesmo ZIP | Cópias locais em `data/raw/phase2`; inventário derivado de 76 campos |
| Literatura | Fontes primárias listadas em [revisao_literatura.md](revisao_literatura.md) | Consultas e nível de leitura registrados; sem alegação de revisão sistemática própria |
| Página do Challenge | [PhysioNet 2019 v1.0.0](https://physionet.org/content/challenge-2019/1.0.0/) | HTML recebido e salvo como `catalog.txt`; anuncia CC BY 4.0 |
| Arquivo de licença | [LICENSE.txt oficial](https://physionet.org/files/challenge-2019/1.0.0/LICENSE.txt) | HTTP 200 via Python; conteúdo ODbL, em conflito com catálogo; não se escolheu uma licença por inferência |
| Amostras A/B | [Diretório oficial](https://physionet.org/files/challenge-2019/1.0.0/training/) | Listagens completas e 24 arquivos; URLs finais (inclusive redirecionamentos), bytes e hashes no log |

**Atribuição PhysioNet:** Reyna M, Josef C, Jeter R, Shashikumar S, Moody B, Westover MB, Sharma A, Nemati S, Clifford GD. Early Prediction of Sepsis from Clinical Data: The PhysioNet/Computing in Cardiology Challenge 2019, version 1.0.0. [DOI 10.13026/v64v-d857](https://doi.org/10.13026/v64v-d857). Publicação clínica: Reyna et al., *Critical Care Medicine* 2020;48(2):210–217, [DOI 10.1097/CCM.0000000000004145](https://doi.org/10.1097/CCM.0000000000004145). A página também solicita a referência de plataforma: Pollard et al. (2026), [PhysioNet as a global platform for biomedical research](https://doi.org/10.1038/s44360-026-00096-z). Referências não implicam endosso.

Os autores Heart continuam creditados em [dados-e-licencas.md](dados-e-licencas.md). O código novo produz apenas estatísticas e índices locais de linhas; não altera o ZIP. Os 24 PSV não são publicados ou copiados para `data/samples/`; permanecem no diretório bruto ignorado pelo Git. A divergência de licença é uma pendência documental, não uma falha de download e não justificativa para contornar controles.

## Registro das tentativas e problemas

- Link de download histórico do Challenge: 404 no navegador; diretório oficial atual acessível. Não foi baixado pacote integral de 42 MB nem presumida a existência de ZIP em outro endereço.
- Algumas aberturas PMC retornaram desafio de navegador. Foram usados resumos PubMed, trechos indexados da fonte primária ou páginas do editor, com limites de leitura explícitos.
- Abertura do LICENSE no navegador de pesquisa falhou ao seguir redirecionamento S3 (erro da ferramenta); o mesmo recurso já havia sido recebido e verificado por Python. Não confundir indisponibilidade em uma ferramenta com ausência do arquivo.
- Leitura manual do catálogo com `Path.read_text()` sem codificação explícita falhou em cp1252. Repetição com `encoding='utf-8'` funcionou; nenhum byte foi alterado. O pipeline usa decodificação explícita nos arquivos textuais que analisa.
- Bruto Cleveland: aviso de corrupção e blocos de largura irregular; não corrigido por conjectura. A exclusão desse bruto da projeção está no código e no relatório.
- Reconciliação de licença PhysioNet: não resolvida; nenhum contato enviado. Contagem de rótulos positivos na amostra: zero; limite amostral, não evidência de ausência de sepse no dataset.

## Limitações transversais

Políticas foram definidas após o piloto da Fase 1; não são pré-registro confirmatório. Não houve revisão clínica, validação contra prontuários, definição de população-alvo externa ou inferência causal. A correspondência de multiconjuntos entre versões não identifica pessoas nem recupera a intenção do curador. Dados com a mesma unidade física não são automaticamente o mesmo construto clínico. Revisão bibliográfica de um único agente, sem avaliação formal de viés ou exaustividade. Resultados de artigos não foram reproduzidos.
