# Parecer crítico sobre o DataMind até o manuscrito v3

16/11/2026. Escopo documental, metodológico e bibliográfico. A pesquisadora permanece responsável por aceitar, revisar e defender as decisões científicas. Este parecer registra uma revisão documental apoiada por ferramentas computacionais e as evidências consultadas. Pareceres humanos externos continuam pendentes.

## Julgamento atual

O estudo sustenta uma contribuição empírica incremental sobre elegibilidade e avaliação de classificadores de uma anotação de ECG. Há coerência entre a comparação operacional congelada, o pipeline inspecionado e o resultado primário relatado. A interpretação mais ampla depende de esclarecimento semântico das medidas, revisão estatística e avaliação externa de relevância. A integridade dos arquivos demonstra preservação, enquanto a validade científica depende também das definições, pressupostos e alcance das conclusões.

O resultado inconclusivo é um resultado legítimo. Sua contribuição depende da pergunta e da qualidade do relato. A redação pode explicar que a comparação deixou incerteza sobre vantagem e desvantagem das estratégias, mantendo as estimativas e seus intervalos. A originalidade específica ainda exige julgamento crítico da literatura próxima.

## Evidências sustentadas

|Afirmação|Evidência local|Alcance|
|---|---|---|
|O contraste primário compara estratégias na mesma população|metrics.json, primary, e protocolo Fase 4|2.198 exames, 1.904 pacientes, 54 exames positivos de 45 pacientes|
|A superioridade prevista ficou inconclusiva|primary.delta_brier e primary.CI95|E3 menos E2-fallback = −0,000613, IC95% [−0,002380; +0,001133]|
|Exigir todas as medidas reduz cobertura e muda composição|overall.E1, composition.json e relatório final|1.088 exames elegíveis, 49,50% do total, 35/54 positivos, 64,81%|
|E2 e E2-fallback coincidem neste teste|fallback_count e relato da Fase 6|Mecanismo de fallback com frequência zero neste conjunto|
|Há medidas de controle contra vazamento de paciente e ajuste global|pilot.py, GuardedModel e load_development; fase5_train.py|Pipeline ajustado em cada treino interno, verificações de IDs e pacientes, seleção em 1–8|
|O IC primário respeita repetição de exames por paciente|evaluation.py, cluster_intervals|Reamostragem dos pacientes com multiplicidade aplicada aos exames e sorteios compartilhados entre estratégias|

Fonte numérica principal em `reports/phase6/final001/metrics.json`. Brier de E2-fallback = 0,006655, de E3 = 0,006042, de B0 = 0,023964. Esses valores foram lidos de resultados existentes. O arquivo também contém métricas binárias legadas no limiar 0,5 dentro de primary. Para os limiares definidos no fold 9, a fonte correta é overall/strata e bootstrap.binary_frozen_thresholds.

A cobertura do fold 10 já aparecia no preflight da Fase 4. Portanto, sua apresentação final é consolidação de uma característica conhecida da coorte. A avaliação preditiva reservada acrescenta a comparação de probabilidades. Essa distinção precisa acompanhar a frase de contribuição.

## Auditoria metodológica

### Painel e significado clínico

A Fase 4 registra escolha exploratória das oito medidas após análise de disponibilidade no desenvolvimento. O painel inclui duração global, RR e características de V1/V6. Existe relação plausível com condução e morfologia, mas a documentação não demonstra que cada campo seja necessário, que o conjunto seja ótimo ou que tenha sido aprovado por cardiologista antes do treino. A contribuição específica de RR permanece sem justificativa clínica suficientemente desenvolvida. A revisão deve recuperar a razão efetivamente registrada para incluí-lo, evitando justificativa retrospectiva apresentada como decisão prospectiva.

O dicionário associa RR_Mean_Global a RRi_max e QRS_Dur_Global a QRSd_max. O mapeamento e as unidades publicadas estão documentados. A definição dos pontos fiduciais e da agregação permanece pendente. P_Morph e HA__Global foram tratados como números no painel amplo. A relação linear imposta a códigos pode limitar essa representação. Avaliar essa limitação requer conhecimento do extrator e dos domínios dos códigos.

### Alvo, circularidade e vazamento

A chave CRBBB em scp_codes define o alvo. O processamento utiliza medidas extraídas do sinal e exclui laudos, códigos e identificadores dos preditores. Isso sustenta controle de vazamento direto no conjunto de entradas inspecionado. Medidas e anotação, contudo, descrevem o mesmo ECG. A tarefa tem forte proximidade de construto com a interpretação morfológica. Uma AUC elevada pode ser compatível com esse objetivo, e sua leitura deve permanecer vinculada ao reconhecimento da anotação.

Não há evidência documental de que o rótulo seja uma função exata das oito medidas. Assim, chamar toda a tarefa de circularidade matemática comprovada seria excessivo. Também não há adjudicação independente de doença ou avaliação de benefício clínico. Cabe ao especialista julgar a adequação do alvo para a pergunta e a plausibilidade das medidas.

### Ausências e imputação

E3 utiliza mediana aprendida no treino de cada divisão. E3-I acrescenta indicadores fixos. A rotina preserva zeros observados e prevê preenchimento zero para coluna totalmente ausente no treino. Isso torna a transformação executável em novos registros, mas não demonstra recuperação do valor fisiológico perdido nem ausência de viés.

MCAR, MAR e MNAR não foram identificados neste estudo. A mediana como estratégia preditiva pode ser avaliada operacionalmente sem declarar um desses mecanismos verdadeiro. Sua estabilidade depende das relações entre observação, ausência, sinal e alvo. Contagens e indicadores podem capturar características do extrator. A diferença entre completos e incompletos não esclarece sozinha por que uma medida faltou.

### Desenvolvimento, regularização e teste

Os modelos selecionam C entre 0,01, 0,1, 1 e 10, usando previsões fora do fold oficial em 1–8. Pré-processamento ocorre dentro de cada treino. O erro OOF usado para escolher C tem otimismo possível como estimativa do desempenho do procedimento selecionado. O teste final separado avalia os modelos congelados e não remove todas as limitações da seleção prévia do painel.

Os modelos amplos escolheram a borda inferior da grade. Isso limita afirmações sobre otimização. Nos controles, usar o mesmo C fixa uma configuração nominal, sem igualar complexidade efetiva. O contraste E3/E2-fallback muda painel e tratamento da ausência e admite pequena diferença na elegibilidade de treino. O protocolo original tinha linguagem de isolamento em controles, qualificada pelas emendas e pela v3. A interpretação atual deve seguir essa qualificação.

O fold 9 escolheu limiares e orientou interpretação exploratória. Sensibilidade nesse fold, no limiar escolhido nele, é aparente. O fold 10 foi reservado para aplicação preditiva, com contagens já conhecidas antes do treino. A própria fonte PTB-XL informa maior controle humano dos rótulos dos folds 9/10. Isso merece explicação ao comparar desenvolvimento e avaliação. [PTB-XL 1.0.3](https://physionet.org/content/ptb-xl/1.0.3/)

### Métricas, precisão e população

Brier mede erro quadrático das probabilidades. Em baixa prevalência, o baseline constante é indispensável para contextualizar seu nível. Comparar perdas no mesmo suporte resolve a diferença de denominadores entre esses comparadores, mas não torna causal a comparação. O desempenho de E1 restrito aos completos responde a outra população.

O estimando pondera exames igualmente. Pacientes com mais exames contribuem mais, mesmo com bootstrap agrupado. O IC é condicionado aos modelos, transformações e limiares preservados. A amostra de 45 pacientes positivos restringe sensibilidade, calibração e análises por subgrupos. O bootstrap [1;1] de sensibilidade resulta dos acertos observados e não quantifica adequadamente a possibilidade de futuros erros. Uma proposta de esclarecimento estatístico adicional deve passar pelo bioestatístico e pela pesquisadora antes de execução.

O ajuste conjunto de intercepto e inclinação descreve calibração com precisão limitada. Média prevista próxima da prevalência não garante concordância ao longo de toda a escala. A direção da diferença de Brier mudou entre folds, com ambos os intervalos incluindo zero. Esse fato não demonstra data drift nem equivalência.

## Revisão bibliográfica direcionada

Consulta em 16/11/2026. Buscas incluíram “PTB-XL complete case imputation CRBBB”, “PTB-XL+ missing data logistic regression coverage” e títulos das referências metodológicas. A seleção priorizou mesma base, representação, tarefa ou política de ausência. A busca tem escopo direcionado, sem protocolo de revisão sistemática.

|Fonte verificada|Proximidade e resultado pertinente|Implicação para o DataMind|Acesso desta revisão|
|---|---|---|---|
|Strodthoff et al., PTB-XL+, 2023, DOI 10.1038/s41597-023-02153-8|Mesma base de medidas, múltiplos extratores e benchmarks|O uso de medidas tabulares já é estabelecido; a comparação específica deve enfatizar denominadores e perda probabilística|Documentação oficial PhysioNet lida; abertura Nature falhou por redirecionamento|
|Rueda et al., 2022, DOI 10.1016/j.cmpb.2022.106807|Regras para bloqueios com FMMecg; pré-processamento exclui fragmentos e imputa parâmetros de batimentos|Forte proximidade de tarefa, com outras medidas e unidade de imputação; resultados não são diretamente intercambiáveis|Métodos e apêndice B do preprint v2 consultados; equivalência à versão publicada ainda a conferir|
|Zhou et al., 2026, DOI 10.3389/fcvm.2026.1825829|PTB-XL+, hipertrofia ventricular, exclusão de campos muito ausentes, mediana e diferentes classificadores|Mesma família de representação e manejo, com alvo e população distintos; mudar o desfecho por si só não fundamenta originalidade|Texto publicado, seção 3.3 consultada|
|Sisk et al., 2023, DOI 10.1177/09622802231165001|Simulação de imputação e indicadores no desenvolvimento e aplicação|Referência metodológica para dependência do desempenho em relação ao cenário|Registro indexado verificado e resumo do preprint consultado; suplemento não relido nesta rodada|
|Hoogland et al., 2020, DOI 10.1002/sim.8682|Métodos para preditores ausentes em novo indivíduo, simulação e aplicação clínica|A transformação usada na avaliação precisa representar aquela disponível ao aplicar o modelo|Texto integral em PMC consultado|
|Tsvetanova et al., arXiv:2504.06799v3, 2026|Compatibilidade de tratamento entre desenvolvimento, validação e uso; simulação e cirurgia torácica|Sobreposição conceitual importante, mas sem o mesmo estimando de ECG|Resumo e histórico v3 confirmados; publicação revisada por pares não confirmada|
|Van Calster et al., 2019, DOI 10.1186/s12916-019-1466-7|Calibração e avaliação de probabilidades|Fundamenta a necessidade de avaliar a qualidade das probabilidades além da discriminação|Página do artigo acessível|
|Geifman e El-Yaniv, SelectiveNet, 2019|Aprendizado com opção de rejeição|Contextualiza cobertura; o DataMind aplica elegibilidade determinística por campos|Registro e resumo PMLR consultados|

Fontes primárias acessadas ou identificadas nesta consulta

- [PTB-XL+ 1.0.1](https://physionet.org/content/ptb-xl-plus/1.0.1/)
- [Rueda, preprint e apêndices](https://arxiv.org/html/2112.12196v2)
- [Zhou, artigo publicado](https://www.frontiersin.org/journals/cardiovascular-medicine/articles/10.3389/fcvm.2026.1825829/full)
- [Sisk, registro publicado](https://pubmed.ncbi.nlm.nih.gov/37105540/) e [preprint](https://arxiv.org/abs/2206.12295)
- [Hoogland, texto integral](https://pmc.ncbi.nlm.nih.gov/articles/PMC7586995/)
- [Tsvetanova, v3](https://arxiv.org/abs/2504.06799v3)
- [Van Calster, artigo](https://link.springer.com/article/10.1186/s12916-019-1466-7)
- [SelectiveNet, PMLR](https://proceedings.mlr.press/v97/geifman19a.html)

Falhas registradas nesta rodada incluem redirecionamento inacessível na Nature, conteúdo PubMed inicialmente incompleto e tentativa de HTML Sisk v4 com resposta 404. O endereço do preprint disponível foi confirmado posteriormente. Não se presume leitura de suplemento a partir de sua citação em relatório anterior. A documentação histórica sobre Avula e Surawicz permanece consultável no projeto; seus textos completos não foram revalidados nesta rodada. Leitura clínica especializada, suplementos finais de comparadores e atualização do status editorial do preprint permanecem pendentes.

Nenhum estudo verificado nesta busca foi estabelecido como réplica exata do contraste, população e políticas do DataMind. O alcance da busca não permite afirmar inexistência de estudo equivalente. O conhecimento de que a completude pode selecionar a amostra já é estabelecido. A contribuição candidata é sua quantificação auditável neste caso, junto ao contraste probabilístico inconclusivo.

## TRIPOD+AI aplicado ao relato

Usado como referência de relato para desenvolvimento e avaliação de modelos. O enquadramento é estudo de reconhecimento de anotação em benchmark. Aplicabilidade clínica e envolvimento de pacientes devem ser descritos conforme o que ocorreu. O preenchimento de itens não certifica qualidade metodológica. A tabela registra avaliação própria do manuscrito por grupos de itens. [Checklist oficial consultado](https://www.tripod-statement.org/wp-content/uploads/2019/12/TRIPODAI_checklist.pdf)

|Itens|Localização e situação na v3|Ação documental|
|---|---|---|
|1–2|Título duplicado; resumo com desenho, números e conclusão|Escolher um título; explicitar avaliação de classificadores; conferir checklist específico do resumo antes do envio|
|3a–c, 4|Introdução delimita anotação e objetivo; contexto de uso e desigualdades limitados|Definir público científico e alcance do estudo; declarar limites de equidade|
|5a–b, 6a–c|Versões/datas constam; elegibilidade e contexto de aquisição dispersos|Consolidar origem, critérios e ausência de seguimento pertinente|
|7, 8a–c|Controles e alvo descritos; origem dos avaliadores e cegamento incompletos|Indicar o que a fonte fornece e o que é desconhecido|
|9a–c|Painel exploratório e tabela disponíveis; agregação pendente|Vincular escolha registrada a definições verificáveis|
|10|Contagens disponíveis, suficiência não demonstrada|Explicar uso da amostra disponível e ausência de dimensionamento prospectivo|
|11, 12a–c|Pipeline, imputação e seleção descritos|Esclarecer pressupostos sem atribuir mecanismo de ausência|
|12d–g|Paciente agrupado; pouca análise de outras heterogeneidades|Explicitar limites e objetos congelados utilizados|
|13–15|Classes, saídas e limiares documentados; equidade não investigada|Distinguir descrição da população e avaliação de equidade|
|16|Folds comparados parcialmente|Explicitar diferença documental na revisão dos rótulos|
|17, 18a–f|Declarações e distribuição pendentes; protocolo local identificado|Obter confirmações institucionais e de autoria, acesso e licença|
|19|Envolvimento de pacientes/público não relatado|Pesquisadora confirmar situação real antes de declaração|
|20a–c, 21|Fluxo e denominadores presentes; caracterização distribuída|Consolidar apenas resumos já existentes e apontar informações indisponíveis|
|22|Arquivos locais descritos; acesso externo pendente|Definir pacote que permita auditoria respeitando identificadores e licenças|
|23a–b, 24|ICs e limitações relatados; sem atualização do modelo|Revisar leitura da sensibilidade e limitações por subgrupos|
|25–26|Discussão e limitações extensas|Concentrar argumento em pergunta, resultado e alcance|
|27a–c|Políticas de disponibilidade descritas; uso clínico não demonstrado|Explicar escopo científico e requisitos para eventual estudo futuro|

## Publicação e voz autoral

Pôster ou trabalho curto são formatos proporcionais ao estudo após revisão das definições e da inferência. Um artigo empírico conciso é possibilidade condicionada à relevância que um revisor atribua ao caso e à resolução dos pontos principais. Resultado inconclusivo não determina rejeição. Nenhum formato dispensa relato honesto e requisitos do veículo. Prazos, taxas e regras de veículos específicos deverão ser conferidos quando a pesquisadora escolher o destino.

A pesquisadora deve explicar as escolhas com suas palavras, aceitando inclusive que algumas foram propostas com assistência técnica e depois adotadas. O histórico não permite atribuir retroativamente toda decisão a uma pessoa ou a uma equipe. A v3 contém declaração real de assistência em seção própria. Recomenda-se concentrar proveniência nessa seção e no histórico, adaptando à regra editorial aplicável, sem repetir avisos no argumento científico. A futura redação pode usar linguagem impessoal clara. CRediT e autoria dependem de contribuições reais e concordância.

## Mudanças propostas e impacto

A v3 foi preservada nesta entrega. Antes de editar conteúdo substantivo, a pesquisadora poderá revisar a justificativa e o impacto abaixo.

|Proposta|Justificativa|Impacto esperado|
|---|---|---|
|Remover um dos títulos iniciais|Duplicação editorial introduzida na atualização anterior|Organização, sem efeito numérico|
|Precisar o tamanho de amostra como disponível|Ausência de dimensionamento prospectivo registrado|Torna explícita a limitação de precisão|
|Explicitar que a cobertura do teste já era conhecida no preflight|Evitar tratar consolidação como descoberta independente|Restringe a novidade atribuída a esse resultado|
|Explicar a revisão humana dos rótulos em 9/10|Diferença documentada entre partições|Qualifica comparação desenvolvimento/teste|
|Evitar “negativo/inconclusivo” como sinônimos|IC permite efeitos nas duas direções|Aumenta precisão da conclusão|
|Concentrar declaração de assistência na seção e histórico pertinentes|Voz autoral mais natural com proveniência rastreável|Mudança editorial sujeita às normas do destino|

Referências internas principais em artigo/manuscrito_v3.md, reports/fase4_protocolo_cientifico.md, docs/fase5_emendas_pre_treino.md, docs/fase5_limitacoes.md, src/datamind/pilot.py, src/datamind/evaluation.py, scripts/fase5_train.py e reports/phase6/final001/metrics.json. Próximas ações em [plano de evolução](../docs/plano_evolucao_cientifica.md).

Encaminhamento editorial posterior a este diagnóstico: a revisão de linguagem autorizada produziu a v4, preservando a v3. Foram corrigidos o título, a apresentação da autoria e a expressão “negativo/inconclusivo”; as demais propostas substantivas desta tabela continuam pendentes. Registro em [revisão de linguagem](revisao_linguagem_autoria.md).
