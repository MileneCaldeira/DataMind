# Aprimoramento da pesquisa — 16/11/2026

## Decisão e escopo

A solicitação de continuidade foi aplicada à revisão editorial e à organização das pendências identificadas. O produto é uma v3 para leitura especializada, com a hipótese primária e a hierarquia do protocolo original. A tarefa corresponde ao aprimoramento do ciclo existente. Aprovação humana, resolução clínica e envio externo permanecem pendentes.

## Melhorias implementadas

|Problema|Mudança efetiva|Evidência|
|---|---|---|
|Objetivo amplo dificultava identificar o contraste principal|Pergunta explícita sobre Brier de E3 versus E2-fallback na mesma população, com objetivos secundários separados|Introdução da v3|
|Dicionário do painel dependia de documentos externos ao manuscrito|Tabela com oito campos, identificadores ECGDeli, unidades publicadas e dúvidas de interpretação|Métodos da v3 e conferência direta de feature_description.csv|
|Limitações de seleção estavam mais completas no piloto que no artigo|Inclusão da escolha de C na borda inferior da grade e do otimismo possível dos diagnósticos OOF usados na seleção|Limitações da v3, docs/fase5_limitacoes.md e docs/fase5_emendas_pre_treino.md|
|Guia operacional continha estados antigos de Git e ambientes|Correção dos parágrafos e referência à verificação pós-migração|GUIA_DO_PROJETO.md|
|Navegação apontava apenas para a v2|README, guia e painel direcionam à v3, mantendo referências históricas nos materiais de cada fase|README.md e STATUS_DATAMIND.md|

A versão 2 tem SHA-256 `093514d7597a78769ceba41fa5767dfdd40e25c2bbe1c75fafc32e0f83f1a76d`. A seção Resultados e o trecho Referências até o fim do manuscrito foram comparados entre v2/v3 e coincidem. A nova tabela foi conferida contra o dicionário local. A correspondência documental de nomes e unidades está verificada. A interpretação fisiológica da agregação continua pendente de especialista.

O texto adicional sobre regularização relata uma limitação anterior ao teste. Seu registro na v3 não converte uma nova escolha de hiperparâmetro em decisão prospectiva. O artigo conserva o resultado principal inconclusivo e a ausência de evidência de equivalência.

## Plano de quatro semanas

Estimativa de planejamento para 6–8 horas semanais da pesquisadora. Prazo de pareceres depende de disponibilidade e concordância dos revisores. As atividades externas abaixo aguardam iniciativa da pesquisadora.

|Semana|Trabalho delimitado|Responsável ou perfil|Entrega verificável|Situação|
|---|---|---|---|---|
|1|Ler e explicar a pergunta, a tabela das medidas e os limites; escolher revisores|Pesquisadora|Apresentação oral de três minutos e lista de revisores com disponibilidade confirmada|Rascunho e roteiros preparados; contatos pendentes|
|2|Revisar semântica do painel e validade da anotação|Especialista em ECG e, se necessário, conhecedor de ECGDeli|Respostas C1–C7 do roteiro clínico com fonte ou indicação de ponto não verificável|PENDENTE|
|2|Revisar estimando, bootstrap, sensibilidade, calibração e regularização|Bioestatístico|Respostas B1–B6 com gravidade e correção textual proposta|PENDENTE|
|3|Consolidar comentários e revisar a versão editorial|Pesquisadora; apoio de revisor a confirmar|Matriz de feedback preenchida apenas com pareceres reais e respostas dos autores|PENDENTE dos pareceres|
|3|Conferir a completude do relato com checklist TRIPOD+AI oficial|Pesquisadora com revisor metodológico|Cada item associado à seção e às lacunas; adequação avaliada item a item|PENDENTE; matriz de prontidão abaixo preparada|
|4|Avaliar contribuição e adequação de trabalho curto|Pesquisador experiente em publicação|Parecer editorial, pendências institucionais identificadas e texto aprovado pelos autores para próximo encaminhamento|PENDENTE|

Se um especialista não estiver disponível, o produto do mês será a revisão editorial com pendências explícitas. Receber um comentário e resolver uma dúvida são etapas distintas. Uma questão sem resposta mantém seu status pendente.

## Matriz de prontidão do relato

Esta tabela organiza o trabalho de revisão. O preenchimento do checklist oficial TRIPOD+AI exige leitura de cada item e análise de aplicabilidade.

|Tema|Onde encontrar na v3|Critério de fechamento|Estado|
|---|---|---|---|
|Pergunta e contraste|Introdução e Avaliação e integridade|Revisor identifica população, estratégias, desfecho e estimando sem ambiguidade|Texto aprimorado; parecer pendente|
|Dados e alvo|Desenho, dados e alvo|Revisão confirma interpretação de presença/ausência de CRBBB e limites da anotação|Documentado; revisão clínica pendente|
|Medidas e ausências|Preditores e ausências; Dicionário|Resolver agregação QRSd_max/RRi_max ou restringir explicitamente a interpretação|Mapeamento verificado; semântica pendente|
|Desenvolvimento|Partições e desenvolvimento; Limitações|Revisor avalia separação por paciente, pipeline e seleção de C|Documentado; revisão metodológica pendente|
|Inferência|Avaliação e integridade|Parecer sobre estimando por exame, IC condicionado e sensibilidade degenerada|Documentado; parecer pendente|
|Resultados e denominadores|Resultados|Conferência preserva população integral versus completos e hierarquia das análises|Texto da v2 preservado|
|Calibração|Avaliação e integridade; Resultados|Confirmar que o relato sustenta apenas o alcance permitido pelos poucos eventos|Documentado; parecer pendente|
|Originalidade|Introdução e Discussão; docs/fase8_originalidade.md|Revisor compara a contribuição com os trabalhos próximos|Posicionamento incremental; avaliação externa pendente|
|Disponibilidade e reprodução|Figuras e material reproduzível|Definir acesso permitido, licença do código e forma de compartilhamento|Versões locais registradas; decisões de distribuição pendentes|
|Autoria e declarações|Declarações pendentes|Autores confirmam afiliações, contribuições, requisitos institucionais e declarações|PENDENTE|

Checklist de referência já identificado na revisão anterior em https://www.tripod-statement.org/wp-content/uploads/2019/12/TRIPODAI_checklist.pdf. Esta atualização não realizou uma nova busca bibliográfica nem uma avaliação formal de conformidade TRIPOD+AI.

## Uso dos roteiros e comentários

Os roteiros clínico e estatístico da Fase 9 continuam úteis para as mesmas perguntas, embora citem a v2 histórica. Para a próxima rodada, encaminhar a v3 e informar ao revisor a versão recebida. Usar reports/fase9_matriz_feedback.md para registrar respostas reais. A matriz permanece vazia enquanto não houver parecer recebido.

Prioridade clínica para QRSd_max/RRi_max, definição do alvo e codificação morfológica. Prioridade estatística para o estimando, poucos pacientes positivos, intervalo degenerado e controles de regularização. Caso a revisão identifique erro material, registrar impacto e discutir uma proposta específica de correção antes de qualquer novo cálculo.

## Verificações e limites

A verificação de preservação executada antes das alterações aprovou os manifestos ativos Fases 5–9, entradas F2/F3 e correspondência dos sete arquivos de probabilidades com predictions.csv. Verificação final registrada na conclusão desta nota. A análise integral dos sinais, validação clínica, novos intervalos e novas avaliações preditivas ficam fora do escopo editorial.

Os arquivos de requisitos não rastreados já presentes na raiz foram mantidos. A atualização do guia usa o histórico de reconstrução de 05/11/2026. Não houve nova inspeção do destino de backup nem nova certificação do estado remoto do GitHub nesta revisão.

Verificação final em 16/11/2026 aprovada. Manifestos ativos íntegros, sete arquivos de scores correspondentes às probabilidades consolidadas, SHA-256 da v2 conferido e seções Resultados/Referências da v3 idênticas à v2. Links locais do manuscrito e dos guias atualizados encontrados. O diff reconhece os finais de linha Windows com core.whitespace=cr-at-eol. Nenhuma previsão, treinamento, métrica nova, commit ou push nesta atualização.
