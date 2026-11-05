
# Slide 1 — Disponibilidade de medidas de ECG
**DataMind · estudo de caso para revisão humana**

Como exigir medidas completas muda quem é avaliado e o desempenho observado?

- PTB-XL / PTB-XL+: medidas dos mesmos exames.
- Alvo: anotação CRBBB, não diagnóstico independente.
- Contribuição candidata: avaliação de cobertura e denominadores.

Fonte: artigo/manuscrito_v2.md, Introdução e Métodos. Material preparado com assistência de IA; sem revisão humana independente concluída.

---
# Slide 2 — Desenho e comparação principal
- Regressão logística L2; pacientes separados entre partições.
- Folds 1–8: desenvolvimento; fold 9: limiares; fold 10: teste único.
- E3: 531 medidas imputadas.
- E2-fallback: oito medidas; prevalência se indisponíveis.
- Comparação na mesma população; não isola efeito causal da imputação.

**Teste: 2.198 exames · 1.904 pacientes · 54 positivos em 45 pacientes.**

Fonte: reports/phase4/preflight.json; experiments/fase5.json; phase6/final001/metrics.json → primary.

---
# Slide 3 — Resultado primário inconclusivo
|Estratégia|Brier, menor é melhor|
|---|---:|
|E2-fallback|0,006655|
|E3|0,006042|

**Δ E3 − E2-fallback = −0,000613**  
**IC95% [−0,002380; +0,001133]**

Bootstrap agrupado por paciente: 2.000 réplicas. Sem suporte à superioridade; sem demonstração de equivalência.

Fonte: reports/phase6/final001/metrics.json → primary. Brier é erro probabilístico, não porcentagem de acerto.

---
# Slide 4 — Cobertura e seleção de exames
|Exigência de 531 medidas completas|Atendidos|
|---|---:|
|Todos os exames|1.088/2.198 — 49,50%|
|Exames positivos|35/54 — 64,81%|

- A composição muda: não comparar E1 restrito com modelos integrais como se fossem pareados.
- Oito medidas disponíveis em todo o teste: **fallback não acionado**.
- Híbrida: Brier 0,005384, resultado secundário; não “vencedora” confirmada.

Fonte: metrics.json → overall; composition.json. As contagens são de exames, não de pessoas únicas.

---
# Slide 5 — O que precisamos revisar
- **Clínica:** QRSd_max, RRi_max, unidades e significado do alvo.
- **Estatística:** poucos positivos, calibração e sensibilidade de 100% com IC bootstrap degenerado.
- **Publicação:** contribuição incremental suficiente para trabalho curto?

Sem validação externa. AUC elevada não demonstra diagnóstico independente. Revisão humana antes de decisão de submissão.

**Pedido ao DataMind:** indicações de colaboradores clínicos, estatísticos e editoriais.

Fontes: reports/fase8_pendencias_especialistas.md; docs/fase8_originalidade.md. Referência para perguntas: docs/guia_defesa_pesquisa.md.
