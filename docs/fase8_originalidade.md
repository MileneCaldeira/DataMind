
# Originalidade e aprofundamento documental — Fase 8
05/11/2026. Complementa a revisão direcionada da Fase 7; não é revisão sistemática nem comprovação de ausência de estudos equivalentes.

## Busca e leitura
Consultas adicionais: “PTB-XL CRBBB complete imputation”, “ECGdeli RRi_max QRS_Dur_Global”, “Handling missing predictor values validating applying”, “Compelling new electrocardiographic markers automatic diagnosis”; referências citadas por Tsvetanova e documentação PhysioNet. Critério: proximidade da pergunta, tarefa e unidade de análise, não apenas coincidência de palavras.

Métodos do PTB-XL+ e Sisk revisitados nos XML arquivados. Nesta fase, o suplemento de Sisk foi efetivamente recuperado pela API pública Europe PMC; texto/apêndices e tabelas foram lidos, sem alegar inspeção completa de todas as figuras embutidas. Hoogland foi lido em XML integral (métodos). Rueda foi consultado em preprint v2, inclusive apêndice B; versão publicada identificada, equivalência integral entre versões não estabelecida. Tsvetanova v3: métodos, exemplo empírico e legendas suplementares; tentativa de screenshots suplementares falhou por timeout. Não inferimos resultados visuais não vistos.

## Matriz de proximidade
|Trabalho / problema|Contribuição e metodologia|Dataset / unidade|Resultado pertinente|Sobreposição e diferença demonstrada|
|---|---|---|---|---|
|[PTB-XL+, Strodthoff 2023](https://doi.org/10.1038/s41597-023-02153-8): medidas e anotações ECG|Características de extratores, harmonização e benchmark RF; medianas/IQR/contagens ECGDeli|Mesmos ECGs PTB-XL, tarefas multilabel|Medidas tabulares permitem classificação; concordância entre extratores/anotações varia|Não somos pioneiros em medidas tabulares. Diferença: cobertura explícita e Brier pareado para CRBBB; macro-AUC do benchmark não é comparável ao nosso AUC binário|
|[Rueda 2022](https://doi.org/10.1016/j.cmpb.2022.106807): marcadores de bloqueios de ramo|FMMecg e regras com poucos marcadores; apêndice do preprint remove batimentos inválidos e imputa parâmetros por mediana do próprio fragmento|PTB-XL, Georgia e CPSC (referida como CPCS no texto); processamento por batimento/derivação|Regras de identificação de bloqueios com discriminação favorável reportada; tarefa inclui CLBBB/CBBB, não nosso contraste binário isolado|Sobreposição forte em tarefa e representação compacta. Imputação dentro do fragmento difere de mediana de coluna aprendida no treino; elegibilidade e denominadores distintos. Não comparamos números como benchmark|
|[Sisk 2023](https://doi.org/10.1177/09622802231165001): ausência no desenvolvimento/uso|Simulações, imputação por regressão/múltipla, indicadores e interações; suplemento detalha cenários e calibração|Simulações e aplicação MIMIC-III|Benefícios dependem de cenário; suplemento diferencia CITL com offset e efeitos na discriminação|Nós não inovamos em imputação/indicadores. Nossa ausência natural em ECG não identifica mecanismos simulados por eles|
|[Hoogland 2020](https://doi.org/10.1002/sim.8682): aplicar modelos com preditores faltantes|Submodelos, marginalização e imputação transportável; sete abordagens no estudo|Simulação e aplicação clínica, novos pacientes|Validação deve representar o método disponível para um novo paciente; métodos têm requisitos operacionais distintos|Nosso congelamento do imputador segue princípio conhecido. Painel/fallback não constitui nova família de soluções|
|[Tsvetanova v3 2026](https://arxiv.org/abs/2504.06799v3): compatibilidade entre etapas|CCA, imputações e modelos por padrões, simulações; exemplo de mortalidade após ressecção pulmonar|NCORR e simulação; não ECG|Incompatibilidades podem enviesar estimativas de desempenho na aplicação|Principal sobreposição conceitual. Nosso contraste descreve políticas na mesma coorte; não estima viés contra um mecanismo verdadeiro conhecido. Preprint, revisão por pares não confirmada|
|[SelectiveNet 2019](https://proceedings.mlr.press/v97/geifman19a.html): predição com rejeição aprendida|Rede com seletor conjunto e restrição de cobertura|Benchmarks de classificação/regressão|Melhora de risco–cobertura reportada|Nossa seleção determinística por presença de campos não é algoritmo seletivo aprendido nem contribuição nessa teoria|
|[Zhou 2026](https://doi.org/10.3389/fcvm.2026.1825829): LVH com características tabulares|Imputação mediana, filtragem de variáveis e classificadores, incluindo LR|PTB-XL+, LVH versus controles normais|Desempenho favorável reportado em população selecionada|Trocar LVH por CRBBB não cria novidade. Nosso enfoque é denominador, não algoritmo ou escore clínico|

## O que mudou com o aprofundamento
O suplemento de Sisk explicita CITL como intercepto com preditor linear em offset, diferente do ajuste conjunto do DataMind. A v2 esclarece essa diferença sem recalcular nada. Seu apêndice de imputação empilhada também mostra que o mecanismo de aplicação deve ser especificado; nossa mediana congelada é uma opção simples, não solução geral.

O apêndice B de Rueda é particularmente relevante: exclusão por quantidade insuficiente de batimentos e preenchimento por parâmetros de batimentos válidos mostram que seleção e imputação já integram classificadores de ECG. Não encontramos demonstração de que esse artigo responda exatamente ao contraste E3/E2-fallback; há sobreposição substantiva que impede reivindicar novidade por usar poucos marcadores ou discutir ausências.

## Frase defensável
“Neste estudo de caso com PTB-XL/ECGDeli, quantificamos a cobertura e a composição decorrentes da exigência de medidas completas e avaliamos, na mesma população reservada, estratégias probabilísticas previamente congeladas para reconhecer a anotação CRBBB, obtendo resultado primário inconclusivo.”

## Separação das contribuições
- **Conhecido:** completude pode selecionar população; imputação precisa ser compatível com aplicação; AUC não basta; medidas compactas podem reconhecer padrões ECG.
- **Contextual demonstrado:** 49,50% de cobertura completa e 64,81% entre positivos; composição distinta e contraste pareado inconclusivo; fallback não acionado.
- **Incremental:** documentação de denominadores, controles de regularização e execução preservada para este caso específico.
- **Futuro, não demonstrado:** generalização externa, equivalência de painel, custo/benefício clínico e mecanismo das ausências.

Não está demonstrada contribuição metodológica geral suficiente para um artigo de inovação. Comunicação curta é defensável após revisão humana. Artigo original conciso pode caber como estudo empírico incremental; isso depende de avaliação editorial, não é conclusão de originalidade.

## Referências, acesso e limites
Referências 1–8 da v2 têm registros verificados na Fase 7 (reports/phase7/fontes_verificadas.md), mantidos e revisitados quando relevantes. Novas:
- Surawicz B et al., JACC 2009;53:976–981, [DOI](https://doi.org/10.1016/j.jacc.2008.12.013), [PubMed 19281930](https://pubmed.ncbi.nlm.nih.gov/19281930/).
- Hoogland J et al., Statistics in Medicine 2020;39:3591–3607, [DOI](https://doi.org/10.1002/sim.8682); XML PMC7586995 arquivado.
- Rueda C et al., Computer Methods and Programs in Biomedicine 2022;221:106807, [PubMed 35525215](https://pubmed.ncbi.nlm.nih.gov/35525215/); [preprint/apêndices](https://arxiv.org/abs/2112.12196v2).

Falhas: JACC 403; arXiv HTML v3 404; screenshots arXiv timeout; PDF no repositório UVA retornou proteção Anubis, consultado preprint público; Wiley abriu inicialmente, depois 403, usado Europe PMC. URL tentativa de suplemento SelectiveNet não acessível; página PMLR não listava suplemento separado. Não alegamos leitura de arquivos indisponíveis. Sisk: bloqueio SAGE anterior superado por cópia pública Europe PMC, sem contornar autenticação. Downloads/hashes: reports/phase8/sources/access.json.
