# Fase 6 — interpretação científica
Conclusão em 05/11/2026. Usados exclusivamente resultados já salvos. Nenhuma nova previsão, treinamento ou recalibração.

## Resposta à pergunta principal
A hipótese direcional de que E3 teria menor Brier que E2-fallback não recebeu suporte estatístico no teste reservado. A diferença foi −0,000613, com IC95% [−0,002380; +0,001133]. A estimativa pontual favorece E3, mas a precisão permite efeitos nos dois sentidos. Não há evidência de equivalência ou de ausência de diferença.

Esse contraste compara duas estratégias operacionais, que mudam simultaneamente o conjunto de variáveis e o tratamento das ausências. Mesmo um resultado significativo não isolaria efeito causal da imputação. Não se pode concluir que “imputar melhora” ou “imputar não funciona”.

## Principal resultado experimental
O resultado mais defensável é uma avaliação reproduzível que separa disponibilidade de medidas e qualidade das previsões em população comum. Exigir 531 medidas atende 49,50% dos exames do teste, enquanto o painel de oito atende todos. A ampliação de variáveis e imputação não demonstrou vantagem inequívoca no contraste primário.

O painel reduzido permaneceu competitivo — Brier 0,006655, AUC 0,997141 e AP 0,862865, com cobertura integral. E3 apresentou Brier 0,006042, AUC 0,997625 e AP 0,909119. “Competitivo” é descrição do desempenho observado, não conclusão formal de não inferioridade.

A híbrida apresentou o menor Brier entre as estratégias de cobertura integral, 0,005384. Seu contraste com E2-fallback foi −0,001271, IC95% [−0,002821; +0,000121]. É resultado secundário, com intervalo incluindo zero. Não foi promovido a hipótese principal nem usado para alterar modelos.

E3-I não demonstrou ganho claro sobre E3. Sua diferença de Brier foi +0,000047, IC95% [−0,000020; +0,000129]. Não há justificativa experimental forte para afirmar benefício dos indicadores neste cenário.

## Seleção e denominadores
No teste, E1 excluiu 50,50% de todos os exames, mas 35,19% dos positivos. Portanto, a seleção preservou proporcionalmente mais positivos, elevando a prevalência entre os completos para 3,22%, frente a 1,71% nos incompletos.

No fold 9, a direção era diferente — completos tinham prevalência de 1,93%, incompletos de 3,15%, e somente 40% dos positivos eram completos. Essa inversão invalida uma narrativa universal de que exigir completude necessariamente exclui mais positivos. A regra muda a população, mas a direção da mudança depende da amostra.

Comparar E1 em completos com E2 em todos os exames confundiria capacidade do modelo com mudança na composição. Os controles pareados evitam isso. E1 versus E2-C ajustados, em C, teve diferença −0,003409, IC95% [−0,006613; −0,000498]. Entretanto, esse contraste secundário inclui regularizações escolhidas diferentes. No controle com C=1 comum, a diferença foi +0,000465, IC95% [−0,003872; +0,005073]. Não há demonstração simples de que mais variáveis sejam sempre melhores.

As contagens de completude já haviam sido examinadas na Fase 4. Sua reprodução na Fase 6 confirma consistência computacional, não descoberta confirmatória independente. O novo resultado do teste é a avaliação preditiva dos modelos congelados.

## Mudanças entre validação e teste
E2-fallback liderava o Brier de cobertura integral em 9. A híbrida liderou em 10. O sinal da diferença primária mudou, mas os intervalos dos dois folds incluem zero. Todas as estratégias tiveram Brier numericamente menor em 10, inclusive B0. A prevalência, a composição e a seleção por completude também variam.

Essas mudanças são compatíveis com incerteza amostral e diferenças de composição. Não foi demonstrado data drift, mudança temporal, causalidade ou diferença estatística formal entre folds. A comparação entre folds é descritiva e posterior ao piloto.

O fallback não foi acionado em 9 nem em 10. Assim, E2 e E2-fallback são empiricamente iguais nesses conjuntos. A avaliação não demonstra robustez do fallback quando as oito medidas faltam com frequência.

## Calibração e alcance da evidência
No teste, probabilidades médias ficaram próximas da prevalência para E3 e painel reduzido, mas interceptos, inclinações e faixas revelam diferenças locais. A híbrida, apesar do menor Brier, teve inclinação de calibração aproximadamente 1,456. Brier baixo e AUC elevada não tornam a calibração automaticamente adequada para uma decisão clínica.

AUCs altas são compatíveis com proximidade entre medidas de duração/morfologia do ECG e critérios usados para anotar CRBBB. O alvo é interpretação do próprio sinal. Não é confirmação independente de doença, previsão de evento futuro ou evidência de benefício para pacientes.

São 54 exames positivos em 45 pacientes. Isso permitiu detectar forte sinal de discriminação neste conjunto, mas gerou intervalos largos para diferenças pequenas e faixas de calibração pouco povoadas. Não há base para equivalência, segurança, desempenho perfeito, conclusões por subgrupos ou transporte hospitalar.

## Contribuição efetivamente demonstrada
Foi demonstrado um estudo de caso metodológico incremental, com dados públicos, controle de identidade, contraste pré-especificado, registro da execução única e análise de cobertura em denominadores explícitos. Mostra quantitativamente como a seleção de completos altera a população e como resultados por métricas e partições podem induzir conclusões diferentes.

Não foi demonstrado algoritmo novo, superioridade universal, originalidade inédita nem solução geral para missingness. O achado primário inconclusivo deve ocupar o centro da comunicação, acompanhado da seleção de exames e dos controles que delimitam sua interpretação.

[Resultados completos](fase6_resultados_finais.md) · [Limitações](../docs/fase6_limitacoes.md) · [Decisão de publicação](fase6_decisao_publicacao.md)
