# DataMind — resumo executivo da pesquisa
Conclusão em 05/11/2026.

## O que estudamos?
Um programa extrai medidas de duração e amplitude de um eletrocardiograma. Algumas medidas podem faltar. Investigamos como exigir todas as medidas, usar apenas oito ou preencher ausências muda os exames atendidos e a avaliação de classificadores da anotação de bloqueio completo do ramo direito, CRBBB.

Os dados são públicos, PTB-XL e sua extensão PTB-XL+. A extensão contém medidas dos mesmos exames. Não é uma segunda população independente.

## Como fizemos?
Treinamos regressões logísticas em pacientes de desenvolvimento, escolhemos limiares em um conjunto separado e congelamos as decisões. Depois executamos uma única avaliação final em 2.198 exames de 1.904 pacientes. Havia 54 exames com anotação CRBBB, pertencentes a 45 pacientes.

Comparamos estratégias nos mesmos exames sempre que a pergunta exigia comparação direta. Calculamos intervalos reamostrando pacientes, porque uma pessoa pode ter vários exames.

## O que encontramos?
A estratégia que exige todas as 531 medidas atende aproximadamente metade dos exames, 49,50%. Ela mantém 64,81% dos positivos. O painel de oito atende todos os exames do teste. Seu fallback não precisou ser acionado.

A comparação principal foi entre o painel de oito e o modelo de 531 medidas com imputação. O Brier mede o erro das probabilidades e quanto menor, melhor.

| Estratégia | Brier no teste |
|---|---:|
| Prevalência constante, B0 | 0,023964 |
| Oito medidas, E2-fallback | 0,006655 |
| 531 medidas com imputação, E3 | 0,006042 |
| Híbrida, análise secundária | 0,005384 |

E3 teve erro numericamente menor que o painel reduzido. Porém, a diferença foi −0,000613, com intervalo de confiança de −0,002380 a +0,001133. Como o intervalo inclui zero e valores nos dois sentidos, não pudemos estabelecer uma vantagem clara. Isso também não demonstra que as estratégias sejam equivalentes.

A híbrida teve o menor erro observado, mas é uma análise secundária e sua diferença em relação ao painel reduzido também foi incerta. Não há vencedora definitiva.

## Por que cobertura importa?
Um modelo pode parecer melhor porque foi avaliado apenas em exames selecionados. Precisamos distinguir a qualidade de suas probabilidades da parcela de exames que consegue atender.

No conjunto de validação, exigir todas as medidas excluía proporcionalmente mais positivos. No teste, ocorreu o contrário. A lição é examinar quem foi excluído, sem presumir que o efeito da seleção será sempre o mesmo.

## O que isso não prova?
A anotação CRBBB foi feita a partir do próprio ECG. Medidas do ECG estão próximas dos critérios usados nessa anotação. Assim, AUC alta mostra reconhecimento do padrão anotado neste conjunto, sem comprovar diagnóstico independente, segurança clínica ou previsão de problemas futuros.

Há poucos pacientes positivos para distinguir diferenças pequenas ou avaliar subgrupos com precisão. Também não testamos outra população hospitalar independente.

## Como apresentar a contribuição?
“Realizamos uma avaliação reproduzível de estratégias de disponibilidade de medidas de ECG. Exigir completude reduziu a cobertura e alterou a população avaliada. No teste reservado, a vantagem do painel completo com imputação sobre oito medidas permaneceu estatisticamente inconclusiva.”

É uma contribuição metodológica incremental. Pode sustentar pôster, congresso ou relato curto. Um artigo completo dependerá de uma lacuna bem delimitada e do veículo escolhido.

## Próximo passo recomendado
Encerrar o ciclo experimental e solicitar autorização para preparar a redação com esses resultados. Não continuar ajustando modelos para buscar significância. Uma validação externa seria um projeto futuro, necessário para investigar generalização, e não foi iniciada.

[Resultados detalhados](fase6_resultados_finais.md) · [Interpretação](fase6_interpretacao_cientifica.md) · [Decisão de publicação](fase6_decisao_publicacao.md)
