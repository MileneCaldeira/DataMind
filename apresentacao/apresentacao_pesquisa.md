# Disponibilidade de medidas de ECG e avaliação da anotação CRBBB

**Milene Caldeira · pesquisadora integrante do DataMind**

Como a disponibilidade das medidas afeta a cobertura e a avaliação dos classificadores?

- PTB-XL e PTB-XL+: anotações e medidas dos mesmos exames.
- Regressões logísticas com painéis de oito e 531 medidas.
- Objetivo: comparar estratégias de disponibilidade na mesma população.

Fonte: [Manuscrito](../artigo/manuscrito_v4.md), Introdução e Métodos.

---
# Desenho do estudo

- Folds 1–8: desenvolvimento; fold 9: validação e limiares; fold 10: avaliação final única.
- Pacientes separados entre as partições.
- E3: 531 medidas com imputação.
- E2-fallback: oito medidas; baseline constante quando indisponíveis.
- Contraste operacional: modifica painel e tratamento de ausências; não isola efeito causal da imputação.

**Teste: 2.198 exames de 1.904 pacientes; 54 positivos em 45 pacientes.**

Fonte: [Métodos e resultados](../artigo/manuscrito_v4.md).

---
# Comparação principal

|Estratégia|Brier Score — menor é melhor|
|---|---:|
|E2-fallback|0,006655|
|E3|0,006042|

**Diferença E3 − E2-fallback: −0,000613**

**IC95%: [−0,002380; +0,001133]**

Bootstrap agrupado por paciente, 2.000 réplicas. O resultado não sustenta superioridade de E3 e não demonstra equivalência. Brier mede erro probabilístico, não porcentagem de acerto.

Fonte: [Resultados finais](../reports/fase6_resultados_finais.md).

---
# Cobertura e composição

|Exigência de 531 medidas completas|Exames atendidos|
|---|---:|
|Total|1.088/2.198 — 49,50%|
|Positivos|35/54 — 64,81%|

- Exigir completude altera a população avaliada.
- As oito medidas estavam disponíveis em todo o teste; o fallback não foi acionado.
- Híbrida: Brier 0,005384 em análise secundária; sem superioridade confirmada.
- Resultados em populações distintas não constituem comparação pareada.

Fonte: [Resultados finais](../reports/fase6_resultados_finais.md). Contagens por exame; cobertura já conhecida no preflight.

---
# Conclusões e limites

A disponibilidade das medidas afeta cobertura e composição. A comparação probabilística principal permaneceu inconclusiva.

- Apenas 45 pacientes positivos: precisão limitada, especialmente para sensibilidade e calibração.
- Alvo: anotação CRBBB do próprio ECG; desempenho elevado não estabelece diagnóstico independente.
- Sem validação externa ou demonstração de utilidade clínica.
- Definições das medidas globais e interpretação estatística exigem esclarecimentos especializados.

Contribuição: análise contextual e reproduzível de cobertura, denominadores e comparação de estratégias.

Fonte: [Discussão e limitações](../artigo/manuscrito_v4.md).
