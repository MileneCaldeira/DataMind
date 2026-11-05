
# Pacote para revisão externa — DataMind
05/11/2026. Manuscrito de referência: [v2](../artigo/manuscrito_v2.md), sem alterações nesta fase. Materiais preparados com assistência automatizada; nenhum parecer humano recebido foi presumido.

## Resumo científico
**Contexto:** requisitos de completude podem restringir a população avaliada por classificadores de eletrocardiogramas. **Objetivo:** examinar cobertura, composição e desempenho de estratégias para reconhecer a anotação CRBBB. **Métodos:** estudo retrospectivo com PTB-XL 1.0.3 e PTB-XL+ 1.0.1, utilizando regressões logísticas L2. Folds 1–8 foram usados no desenvolvimento, fold 9 na escolha de limiares e fold 10 em avaliação preditiva única, sem pacientes compartilhados entre partições. O contraste primário comparou Brier de 531 medidas imputadas (E3) com oito medidas e fallback de prevalência (E2-fallback), na mesma população. IC95% foram obtidos por 2.000 reamostragens agrupadas por paciente. **Resultados:** o teste reuniu 2.198 exames de 1.904 pacientes; 54 exames positivos pertenciam a 45 pacientes. Brier foi 0,006042 para E3 e 0,006655 para E2-fallback; diferença −0,000613, IC95% [−0,002380; +0,001133]. Exigir 531 medidas completas reteve 49,50% dos exames e 64,81% dos positivos. O fallback não foi acionado. A híbrida apresentou Brier 0,005384 em análise secundária. **Conclusão:** a comparação primária não sustentou superioridade de E3 nem demonstrou equivalência. A contribuição é uma análise contextual e reproduzível de cobertura e denominadores. Amostra positiva reduzida, alvo derivado do próprio ECG e ausência de validação externa limitam as conclusões; não foi demonstrada utilidade clínica.

## Síntese acessível — conteúdo para uma página
**O problema.** Um modelo pode parecer bom porque só foi avaliado nos exames que conseguiu atender. Queremos entender quem fica de fora quando exigimos todas as medidas e comparar estratégias nos mesmos exames.

**O que fizemos.** Utilizamos ECGs públicos e medidas já extraídas. Os modelos tentam reconhecer uma anotação chamada CRBBB, relacionada ao bloqueio completo do ramo direito. Não realizamos novos diagnósticos. Usamos regressão logística, uma forma de combinar medidas para produzir probabilidades. Pacientes de treinamento e teste foram mantidos separados.

**O que encontramos.** No teste, exigir as 531 medidas completas permitiu atender 1.088 dos 2.198 exames: 49,50%. Foram atendidos 35 dos 54 positivos: 64,81%. Assim, nesse conjunto, positivos foram proporcionalmente menos excluídos que os exames em geral. As oito medidas estavam disponíveis para todos; a alternativa de recorrer à prevalência não precisou funcionar.

**Como interpretar o resultado.** O Brier mede erro de probabilidade, não porcentagem de acerto. E3 teve erro numericamente menor que E2-fallback, mas o intervalo da diferença atravessou zero. Não conseguimos sustentar superioridade nem provar que os modelos sejam equivalentes. A híbrida teve o menor valor pontual integral, mas era uma comparação secundária.

**Por que isso importa.** A pesquisa mostra, neste caso, como requisitos de disponibilidade mudam a cobertura e a composição da avaliação. Comparar grupos diferentes pode confundir desempenho do modelo com seleção de exames.

**O que falta.** Há apenas 45 pacientes positivos e nenhuma base externa independente. Precisamos de especialistas para revisar medidas, rótulo, inferência e contribuição científica. O trabalho está pronto para essa discussão, não para uso clínico.

## Cinco limitações principais
1. Alvo é anotação derivada do mesmo ECG que gera os preditores; não diagnóstico independente.
2. Poucos pacientes positivos limitam precisão, calibração e interpretação da sensibilidade observada de 100%.
3. PTB-XL+ deriva do PTB-XL; não há validação externa.
4. Painel escolhido após exploração; contraste primário muda variáveis e estratégia, sem isolar efeito causal da imputação. Controles com C distinto exigem cautela.
5. Semântica de medidas globais e falhas de extração requerem revisão clínica; fallback sem acionamentos no teste não teve seu desempenho empiricamente demonstrado.

## Perguntas para discussão com o DataMind
- Quem pode revisar a definição do alvo e as medidas QRSd_max/RRi_max?
- O estimando por exame e a apresentação da incerteza são adequados à pergunta?
- A distinção entre primário e secundários está clara para um leitor externo?
- Que contribuição específica diferencia este caso dos trabalhos próximos?
- Trabalho curto, pôster ou artigo conciso é o formato mais honesto?
- Que pendências são apenas de redação e quais realmente impedem submissão?
- Há colaboradores interessados em uma revisão focalizada, sem compromisso antecipado de autoria?

## Mensagem ao grupo — rascunho, não enviada
**Assunto: DataMind — pedido de indicações para revisão de estudo sobre medidas de ECG**

Olá, pessoal!

Preparei uma primeira investigação com PTB-XL/PTB-XL+ sobre como a disponibilidade de medidas de ECG afeta a cobertura e a avaliação de classificadores da anotação CRBBB. O experimento está encerrado, com resultados preservados. A comparação principal foi inconclusiva; não estamos afirmando superioridade dos modelos nem utilidade clínica.

Gostaria de solicitar indicações de colegas com experiência em ECG/cardiologia, bioestatística ou publicação científica para revisar pontos específicos do manuscrito. Organizei um resumo, uma apresentação de cinco slides e roteiros por especialidade. A colaboração inicial seria uma leitura crítica, especialmente sobre o significado das medidas, a interpretação estatística e a contribuição frente à literatura.

Vocês poderiam indicar pessoas interessadas ou sugerir a melhor forma de apresentar o estudo ao grupo? Podemos combinar escopo e prazo conforme a disponibilidade de cada colaborador.

Agradeço desde já.
[Nome da pesquisadora]

## Fontes e navegação
Números: [Fase 6](fase6_resultados_finais.md), [metrics.json](phase6/final001/metrics.json) e [composição](phase6/final001/composition.json). A síntese é dimensionada para uma página textual; a paginação depende do editor.
Roteiros: [clínico](../docs/fase9_revisao_clinica.md), [estatístico](../docs/fase9_revisao_estatistica.md), [editorial](../docs/fase9_revisao_editorial.md).
[Apresentação](../apresentacao/fase9_apresentacao.md) · [Matriz de feedback](fase9_matriz_feedback.md) · [Pendências](fase9_pendencias.md).
