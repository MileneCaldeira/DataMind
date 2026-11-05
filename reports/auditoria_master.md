# DataMind — auditoria master

05/11/2026. Auditoria automatizada sob perspectivas de ML, dados, engenharia e metodologia. Não representa equipe humana independente nem validação clínica. Escopo: manutenção documental, inspeção de artefatos e verificações de leitura. Nenhum novo fit, previsão, bootstrap ou cálculo de métricas; nenhum resultado científico substituído.

## Conclusão

**VALIDADO INTERNAMENTE:** integridade tabular e dos artefatos ativos, configuração dos modelos carregados sem execução, correspondência das probabilidades e rastreabilidade dos resultados. **NÃO VERIFICADO:** reprodução integral em ambiente limpo, extração original do sinal, validade clínica e generalização. **PENDENTE:** revisão humana e backup independente.

A pergunta operacional é defensável: comparar disponibilidade, cobertura e erro probabilístico para reconhecer uma anotação de ECG. Não identifica efeito causal isolado da imputação. O contraste primário continua inconclusivo. Contribuição contextual/incremental; manuscrito v2 adequado para solicitar revisão especializada, não pronto para submissão automática.

## Como interpretar a evidência

- **Fato conferido agora:** leitura dos bytes, dados, código, parâmetros e correspondências descritas abaixo.
- **Registro histórico:** logs e relatórios documentam execuções anteriores; não foram repetidas.
- **Inferência:** interpretação metodológica plausível, identificada como tal.
- **NÃO VERIFICADO:** alegação que exigiria execução proibida, novas fontes, especialista ou observação fora do repositório.

Cobertura: inventário recursivo; leitura do núcleo src, executores de treino/avaliação/verificação, testes, configurações, manuscrito v2, protocolos/emendas e relatórios das fases. Textos restantes foram indexados e consultados por tema; bibliotecas dos ambientes não foram auditadas linha a linha. Não alegamos revisão integral de código de terceiros nem atualização da busca bibliográfica.

## Trajetória reconstruída

|Fase|Objetivo e execução comprovada por artefatos|Decisão / limites|
|---|---|---|
|1|Auditoria de Heart Disease, Adult e diabetes; arquivos/cache, access_log, baseline e oito visões|Qualidade multicêntrica como direção provisória; diabetes condicionado à linhagem/licença; obstáculos MIMIC/eICU são relato da pesquisadora, não falha retestada|
|2|Dicionário Heart de 76 atributos, políticas de elegibilidade e 24 PSV PhysioNet 2019|Reformular A; alterações de composição não provam viés causal; amostra sepse sem positivos e licença divergente|
|3|PTB-XL/PTB-XL+ e inspeção CODE-test; 17 entradas locais|Cobertura ECG preferida; mudança de aquisição/CODE/sepse ficaram alternativas; CODE model.npy é probabilidade externa, não treino local|
|4|Protocolo, oito campos, partições e preflight|Ainda candidato; painel e contagens explorados antes do treino; teste não completamente cego quanto a disponibilidade|
|5|160 ajustes CV, cinco regressões selecionadas e dois controles finais; validação 9 e congelamento|Contraste operacional emendado antes do treino; sem expandir grade após validação|
|6|Sete chamadas finais registradas, uma por pipeline; probabilidades, métricas, ICs e composição|Resultado primário inconclusivo; teste consumido; não selecionar novas estratégias pelo teste|
|7|Revisão direcionada, v1, cinco figuras em três formatos e tabelas|Contribuição incremental, sem novidade ampla demonstrada|
|8|Revisão automatizada crítica e v2|Explicitadas regularização, semântica de medidas e limites inferenciais; requer especialistas|
|9|Resumo, cinco slides Markdown, três roteiros e matriz de feedback|Preparado para convite, sem comentários humanos fictícios ou envio registrado|

Não houve treinamento local de Random Forest, XGBoost, deep learning, modelos Heart/Adult/diabetes/sepse ou do CODE. As letras A/B/C mudaram de significado entre fases; não confundir direções antigas e novas.

## Verificações realizadas nesta auditoria

|Verificação de leitura|Resultado|
|---|---|
|Fase 1: scripts/verify.py inspecionado e executado|6 hashes de fontes e auditoria idêntica ao baseline; oito visões|
|Fase 2: leitura SHA-256 do manifesto|44 entradas correspondentes|
|Entradas ECG/CODE da Fase 3|17 hashes correspondentes|
|Manifestos Fases 5/6/7/8/9|57/31/37/16/9 entradas conferidas, sem divergência; contagens se sobrepõem|
|freeze --check|PASS; não executa modelos|
|Metadados ECG|21.799 linhas e ecg_id únicos; 18.869 patient_id; nenhum paciente em mais de um fold|
|Medidas|21.799 IDs únicos, mesmo conjunto dos metadados; 531 colunas|
|Validade numérica estrutural|Nenhuma célula observada não finita; 286.584 células ausentes explícitas; não é auditoria de plausibilidade clínica|
|Predições finais salvas|2.198 IDs únicos; patient_id, fold e y correspondem à origem; sete scores_*.csv coincidem textualmente com predictions.csv|
|Fallback final|E2 e E2-fallback coincidem em todas as linhas; nenhum acionamento|
|Modelos carregados sem fit/predict|Sete joblib legíveis; C/configuração/IDs/pacientes de treino correspondem às coortes; sem interseção com pacientes de 9/10|
|Validação cruzada|160 hashes de IDs de treino/avaliação reconciliados com as regras, sem warnings nos logs|
|Tabelas científicas|Oito linhas de Brier/denominadores de artigo/tabelas/metricas.csv correspondem a metrics.json|
|Sintaxe local|28 arquivos Python analisados por AST, sem execução; sintaxe válida|

As sete chamadas registradas sustentam execução única **nos artefatos existentes**; não provam ausência de atividades fora do repositório. Não foram repetidos os 18 testes históricos: a suíte inclui ajuste e predição sintéticos. PASS histórico é evidência registrada, não nova execução.

## Auditoria de dados e Machine Learning

Proveniência por URL/versão/hash em reports/phase3/entradas.json: PTB-XL 1.0.3 e PTB-XL+ 1.0.1. A tabela de medidas e metadados representa exames, com repetição legítima de pacientes. Join tem validação one_to_one e igualdade de conjuntos de IDs. Perfis numéricos duplicados no desenvolvimento foram reportados como zero na Fase 5; isso não exclui sinais brutos duplicados, não reextraídos aqui.

Alvo: presença de CRBBB em scp_codes, sem filtro por confiança e sem IRBBB. Preditores são a expansão de campos ECGDeli autorizados no dicionário. Laudos, IDs e diagnósticos não entram no X; idade/sexo/site/device só apoiam auditoria. A relação fisiológica entre medidas e rótulo é dependência de construto, não prova de vazamento direto. Extração upstream permanece NÃO VERIFICADA integralmente.

Código pilot.py remove fold 10 antes de montar X/y de modelagem. As matrizes de origem são lidas para conferir esquema; contagens do teste já eram conhecidas antes do treino, como declarado. Não confundir leitura estrutural com desempenho preditivo.

Transformações pertencem ao pipeline de cada ajuste: mediana, indicadores e StandardScaler. Zero não vira ausência. Coluna vazia recebe zero; constante permanece. E3-I cria todos os 531 indicadores. P_Morph e HA__Global numéricos impõem representação não clinicamente validada.

|Modelo salvo|C|Entradas da regressão|Exames/pacientes de treino|
|---|---:|---:|---:|
|E1|0,01|531|8.874 / 8.175|
|E1_C1|1|531|8.874 / 8.175|
|E2-C|10|8|8.874 / 8.175|
|E2-C_C1|1|8|8.874 / 8.175|
|E2|10|8|17.417 / 15.022|
|E3|0,01|531|17.418 / 15.023|
|E3-I|0,01|1.062|17.418 / 15.023|

Parâmetros inspecionados: lbfgs, l1_ratio=0, sem pesos de classe, semente 20261104; na versão registrada, penalty aparece como “deprecated”, não como texto “l2”. l1_ratio=0 e implementação/versão documentam L2; não houve troca de penalização. C é selecionado por Brier OOF agregado em grade 0,01/0,1/1/10; empate até 10⁻⁶ favorece menor C. OOF do C escolhido tem otimismo de seleção; não é validação aninhada. Controle C=1 não remove diferenças de complexidade entre painéis.

## Auditoria da inferência e resultados

Fonte numérica: reports/phase6/final001/metrics.json; interpretação conferida contra código, sem recalcular resultados.

Teste: 2.198 exames, 1.904 pacientes; 54 positivos de 45 pacientes. Brier E2-fallback 0,006655; E3 0,006042; Δ −0,000613, IC95% [−0,002380; +0,001133]. Hipótese direcional sem suporte; não há margem/teste de equivalência. Híbrida 0,005384 é secundária; não vencedora confirmada.

Bootstrap percentil: 2.000 sorteios de pacientes, todos os exames com multiplicidade do paciente, mesmos sorteios para comparadores. Estimando por exame, condicionado aos modelos e limiares; não inclui novo desenvolvimento. Contraste primário usa mesma população. E1 atende só 1.088 exames e não pode entrar em ranking integral sem ressalva. Controles são pareados no suporte comum.

Sensibilidade 100% nos limiares congelados não significa perfeição populacional. IC empírico [1;1] é degenerado. Campos primary/paired e bootstrap.metrics usam limiar legado 0,5; overall/strata e bootstrap.binary_frozen_thresholds são as fontes corretas para limiares de 9. Não corrigir o JSON silenciosamente.

Calibração ajusta intercepto e inclinação conjuntamente: intercepto não é calibration-in-the-large com offset fixo. Médias próximas à prevalência não comprovam calibração fina. Poucos eventos limitam curvas e AP; não há IC dos parâmetros de calibração nem recalibração aplicada.

Completude 531: 49,50% dos exames e 64,81% dos positivos. Completos/incompletos têm 35/1.088 e 19/1.110 positivos; pacientes dos estratos se sobrepõem. Isso demonstra seleção de composição observada, não mecanismo MCAR/MAR/MNAR ou efeito causal. Fold 9 tinha 40% de cobertura positiva e ordem pontual E2/E3 inversa; não é teste de drift.

Sobreajuste: resultados históricos mostram Brier aparente E3 0,004878 versus OOF escolhido 0,007521, sensibilidade à regularização e melhor C no limite da grade. São sinais compatíveis com otimismo/capacidade excessiva, não vazamento demonstrado nem razão para mudar a grade após teste. Não há warnings de convergência registrados.

## Achados e decisões

|ID / gravidade|Evidência e impacto|Ação|
|---|---|---|
|M1 Importante científico|RR_Mean_Global → RRi_max; QRS_Dur_Global → QRSd_max|Documentado novamente; NÃO VERIFICADA equivalência clínica. Especialista deve conferir algoritmo/agregação, não apenas nomes|
|M2 Importante inferencial|Poucos positivos, IC degenerado, tuning OOF e regularização diferente|Manter limites no v2; bioestatístico humano; nenhuma análise adicional|
|M3 Importante manutenção|README global ainda dizia não haver treino|Atualizado com estado atual; conteúdo histórico preservado abaixo|
|M4 Importante reprodução|experiments/README.md é referenciado em before_hashes.json|Atualização autorizada registrada; verificador histórico exigirá tratamento explícito numa cópia futura; sem modificar congelamento|
|M5 Importante proteção|Branch inicialmente sem commits; objetos/ref Codex não equivalem a histórico da branch|Seleção local explícita em auditoria_git.md; nenhum remoto/publicação|
|M6 Importante proteção|OneDrive sem destino independente comprovado|Plano executável condicionado a destino autorizado; backup PENDENTE|
|M7 Importante execução|fase5_verify prevê fold 9 e testa modelos; outros verificadores escrevem|README distingue consulta de execução; código congelado não alterado|
|M8 Importante inferência|Campos binários legados versus limiares de 9|Guia aponta fontes corretas; nenhuma migração de resultados|
|M9 Moderado engenharia|Repetição de funções write/composition e regras de elegibilidade em scripts|Refatoração apenas proposta; mudaria código congelado e exigiria testes|
|M10 Moderado testes|Sem teste clínico do dicionário ou reconstrução limpa; verificações textuais não provam semântica|Não apresentar testes existentes como cobertura completa; planejar revisão focal|
|M11 Moderado segurança|joblib usa serialização executável; IDs de treino estão dentro dos modelos|Carregados só artefatos locais de hash conferido; não carregar arquivos desconhecidos nem publicar automaticamente|
|M12 Moderado ambiente|Versões fixas, dependências transitivas e caminhos Windows|Nenhuma dependência removida; limpeza/reconstrução e análise de vulnerabilidades NÃO VERIFICADAS|

Não foi detectado novo erro numérico material no contraste primário pelos controles feitos. Isso não equivale a certificado de correção total.

## Problema documental das medidas — decisão específica

feature_description.csv confirma literalmente ms para QRS_Dur_Global/QRSd_max e RR_Mean_Global/RRi_max, e mV para amplitudes R/S. Descrição “Mean value during study” conflita semanticamente com a leitura intuitiva de “max”. Não deduzimos se “max” é máximo entre batimentos, derivações ou outra operação. Isso exige inspecionar a versão do extrator e confirmar com especialista.

Manuscrito v2 já explicita a ressalva; não havia justificativa para editar dados ou textos congelados. Antes da submissão, resolver se há apenas nome harmonizado impreciso ou interpretação materialmente incorreta. Se material, documentar o alcance e suspender alegações clínicas; não ajustar valores históricos para obter resultado favorável.

## Histórico de hashes versus congelamento ativo

Antes desta manutenção, before_hashes.json já diferia em docs/decisoes.md, docs/fase5_auditoria_leakage.md e tests/test_phase5.py. O verificador histórico contém exceções amplas para decisões e nomes fase5/phase5. O congelamento posterior inclui seus bytes finais e passa hoje. Não chamar o snapshot inicial de cópia integral imutável do estado final.

Agora experiments/README.md recebe atualização explicitamente solicitada. Seu hash anterior é d6a8ee2778c8467578ebcdb703a62c4dd991d093bef3f648033a8918255d1145. Preservamos o texto histórico dentro do arquivo e o manifesto original. O verificador fase5_verify.py passaria a rejeitar essa diferença documental antes de prever; não o executamos nem relaxamos controles. O freeze ativo registra before_hashes.json como arquivo, mas não exige que toda referência histórica nele continue atual. Todos os hashes ativos continuam conferidos.

## Manutenção realizada e estado científico

README e experiments/README atualizados; guia recebe nota de atualização; criados painel de estado, explicação didática, esta auditoria, auditoria Git e plano de backup. Nenhum código experimental, dado, modelo, resultado, manifesto, manuscrito ou figura alterado.

V2 não omite as principais limitações identificadas: origem do alvo, painel exploratório, falta de validação externa, regularização, calibração, baixa amostra positiva e ambiguidades semânticas. A suficiência editorial/originalidade permanece julgamento humano; esta auditoria não refez busca sistemática nem verificou literatura nova.

**Próximas ações prioritárias:** (1) backup independente verificado; (2) revisão clínica/estatística focalizada, usando o pacote da Fase 9; (3) após comentários, decisão editorial sobre comunicação curta e condições de autoria/licença. Não iniciar novo experimento para perseguir significância.
