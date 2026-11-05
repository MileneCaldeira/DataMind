# Fase 5 — resultados exploratórios de validação

04/11/2026. Nenhuma previsão do fold 10. Métricas por exame, IC95% por bootstrap de pacientes, 2.000 réplicas. Os intervalos condicionam nos modelos treinados e não incluem incerteza de seleção ou novo treinamento.

## Fold 9 — probabilidades dos modelos ajustados em 1–8

As estratégias com cobertura integral são comparáveis na mesma população. E1 atende somente C e não pode ser comparado diretamente às linhas de cobertura integral. O baseline da última coluna é calculado nos mesmos exames de cada linha.

| Estratégia | Exames / pacientes | Positivos | Cobertura / positivos | Brier (IC95%) | ROC-AUC (IC95%) | AP (IC95%) | Brier B0 no mesmo suporte |
|---|---:|---:|---:|---|---|---|---:|
| B0 | 2183 / 1942 | 55 | 100.00% / 100.00% | 0.02456 [0.01801, 0.03181] | 0.50000 [0.50000, 0.50000] | 0.02519 [0.01830, 0.03283] | 0.02456 |
| E1 | 1137 / 1055 | 22 | 52.08% / 40.00% | 0.00707 [0.00361, 0.01112] | 0.99560 [0.99087, 0.99883] | 0.80364 [0.62413, 0.94847] | 0.01900 |
| E2-C | 2183 / 1942 | 55 | 100.00% / 100.00% | 0.00848 [0.00552, 0.01192] | 0.99380 [0.98562, 0.99856] | 0.82817 [0.70675, 0.93335] | 0.02456 |
| E2-fallback | 2183 / 1942 | 55 | 100.00% / 100.00% | 0.00798 [0.00518, 0.01134] | 0.99387 [0.98603, 0.99848] | 0.82125 [0.69827, 0.93113] | 0.02456 |
| E3 | 2183 / 1942 | 55 | 100.00% / 100.00% | 0.00826 [0.00519, 0.01155] | 0.99561 [0.99280, 0.99800] | 0.77898 [0.65264, 0.90942] | 0.02456 |
| E3-I | 2183 / 1942 | 55 | 100.00% / 100.00% | 0.00823 [0.00517, 0.01154] | 0.99547 [0.99251, 0.99794] | 0.77878 [0.65068, 0.90836] | 0.02456 |
| Hybrid | 2183 / 1942 | 55 | 100.00% / 100.00% | 0.00809 [0.00531, 0.01128] | 0.99638 [0.99377, 0.99843] | 0.82298 [0.70715, 0.92820] | 0.02456 |

## Contrastes pareados no fold 9

Diferença é primeiro menos segundo, em Brier. Valores negativos favorecem o primeiro. E1/E2-C e E2-C/E2 usam somente C. Os demais contrastes operacionais usam toda a coorte.

| Contraste | Exames | Δ Brier | IC95% |
|---|---:|---:|---|
| E3 minus E2-fallback | 2183 | 0.000273 | [-0.00159, 0.00198] |
| E3-I minus E3 | 2183 | -0.000028 | [-0.00008, 0.00002] |
| Hybrid minus E2-fallback | 2183 | 0.000111 | [-0.00133, 0.00153] |
| E1 minus E2-C | 1137 | -0.000083 | [-0.00294, 0.00268] |
| E2-C minus E2 | 1137 | 0.000297 | [-0.00039, 0.00102] |
| E1_C1 minus E2-C_C1 | 1137 | 0.006356 | [0.00114, 0.01158] |

O contraste primário é entre duas políticas, não efeito causal da imputação. As diferenças entre estratégias com cobertura integral são pequenas e os intervalos serão interpretados com a incerteza, sem escolher vencedora universal.

## Calibração e limiar fixo

Sensibilidade/especificidade abaixo usam 0,5 previamente fixado, sem otimização no fold 9. O diagnóstico de intercepto/inclinação usa o próprio conjunto avaliado, sem corrigir probabilidades. Referência ideal aproximada 0/1. B0 constante não identifica inclinação.

| Estratégia | Média prevista / observada | Intercepto / inclinação | Sensibilidade (IC95%) | Especificidade (IC95%) |
|---|---|---|---|---|
| B0 | 0.02480 / 0.02519 | NA / NA | 0.000 [0.00000, 0.00000] | 1.000 [1.00000, 1.00000] |
| E1 | 0.01993 / 0.01935 | 0.238 / 1.202 | 0.636 [0.42105, 0.84005] | 0.997 [0.99372, 1.00000] |
| E2-C | 0.02058 / 0.02519 | 1.004 / 1.248 | 0.655 [0.50908, 0.80000] | 0.996 [0.99346, 0.99860] |
| E2-fallback | 0.02170 / 0.02519 | 0.711 / 1.158 | 0.673 [0.52941, 0.81637] | 0.996 [0.99290, 0.99815] |
| E3 | 0.02327 / 0.02519 | 0.367 / 1.078 | 0.745 [0.62294, 0.86051] | 0.996 [0.99343, 0.99860] |
| E3-I | 0.02322 / 0.02519 | 0.377 / 1.080 | 0.745 [0.62294, 0.86051] | 0.996 [0.99343, 0.99860] |
| Hybrid | 0.02263 / 0.02519 | 0.657 / 1.219 | 0.691 [0.54836, 0.82692] | 0.997 [0.99422, 0.99906] |

Os limiares de especificidade ≥95% foram ajustados em 9 para uso futuro. Sua sensibilidade no próprio 9 é aparente, não avaliação independente. Valores e diagnósticos estão em thresholds.json e evaluation.json. Não usar intervalos acima, que são de 0,5, para esses limiares.

## Calibração em faixas fixas

| Modelo | Faixa | n / positivos | Média prevista | Frequência observada |
|---|---|---:|---:|---:|
| E2-fallback | 0–0.02 | 2079 / 1 | 0.00179 | 0.00048 |
| E2-fallback | 0.02–0.05 | 29 / 0 | 0.03239 | 0.00000 |
| E2-fallback | 0.05–0.1 | 9 / 3 | 0.06924 | 0.33333 |
| E2-fallback | 0.1–0.2 | 4 / 1 | 0.14144 | 0.25000 |
| E2-fallback | 0.2–1 | 62 / 50 | 0.66978 | 0.80645 |
| E3 | 0–0.02 | 2051 / 0 | 0.00172 | 0.00000 |
| E3 | 0.02–0.05 | 49 / 2 | 0.02901 | 0.04082 |
| E3 | 0.05–0.1 | 12 / 3 | 0.07341 | 0.25000 |
| E3 | 0.1–0.2 | 8 / 3 | 0.12237 | 0.37500 |
| E3 | 0.2–1 | 63 / 47 | 0.69835 | 0.74603 |
| E3-I | 0–0.02 | 2053 / 1 | 0.00173 | 0.00049 |
| E3-I | 0.02–0.05 | 47 / 1 | 0.02965 | 0.02128 |
| E3-I | 0.05–0.1 | 14 / 3 | 0.07575 | 0.21429 |
| E3-I | 0.1–0.2 | 8 / 3 | 0.14890 | 0.37500 |
| E3-I | 0.2–1 | 61 / 47 | 0.71295 | 0.77049 |

## Desenvolvimento fora do treino

OOF significa previsão de exame cujo fold não participou daquele ajuste. C=1 foi definido antes do treino. A grade selecionada usa os mesmos resultados OOF para escolher C e tem otimismo de seleção possível. Não tratá-la como validação externa ou CV aninhada.

| Estratégia | C selecionado | Brier OOF C=1 | Brier OOF selecionado | Faixa Brier entre folds, selecionado | Brier aparente treino final |
|---|---:|---:|---:|---|---:|
| E1 | 0.01 | 0.01125 | 0.00790 | 0.00267–0.01184 | 0.00477 |
| E2-C | 10.0 | 0.00810 | 0.00808 | 0.00685–0.01016 | 0.00800 |
| E2 | 10.0 | 0.00783 | 0.00782 | 0.00655–0.00984 | 0.00765 |
| E3 | 0.01 | 0.01107 | 0.00752 | 0.00499–0.00973 | 0.00488 |
| E3-I | 0.01 | 0.01111 | 0.00749 | 0.00498–0.00971 | 0.00486 |

Para cobertura integral, E3-I apresentou o menor Brier OOF selecionado, seguido de E3. Com C=1 fixo, o painel reduzido foi melhor. No fold 9, E2-fallback teve o menor Brier entre as estratégias de cobertura integral. A ordenação depende de regularização e partição, indicando cautela.
O Brier de treino é apenas diagnóstico aparente e não evidência de generalização. A diferença treino/OOF é maior nos painéis completos. A grade termina em C=0,01 na direção de regularização forte, onde os braços completos foram selecionados. Não foi demonstrado ótimo global. Manter a grade prevista evita escolhê-la a partir de 9. Uma expansão futura seria emenda de desenvolvimento com novo congelamento.

## Completos e incompletos no fold 9

| Estrato | Exames / pacientes | Positivos / prevalência | Brier E2 | Brier E3 | AUC E2 / E3 | AP E2 / E3 |
|---|---:|---:|---:|---:|---|---|
| complete | 1137 / 1055 | 22 / 1.93% | 0.00685 | 0.00647 | 0.98928 / 0.99690 | 0.78427 / 0.84492 |
| incomplete | 1046 / 985 | 33 / 3.15% | 0.00921 | 0.01019 | 0.99683 / 0.99438 | 0.84474 / 0.74584 |

Esses estratos são populações diferentes, com prevalências distintas. Diferença entre seus Briers não estima efeito causal da ausência. Comparações E2/E3 dentro de cada estrato são pareadas. Há pacientes com exames em ambos os estratos, portanto contagens de pacientes por estrato não devem ser somadas como indivíduos independentes.

## Interpretação

Há sinal preditivo em relação à prevalência constante para reconhecer a anotação. Não há demonstração de superioridade definitiva de E3 sobre E2-fallback. Maior AUC da estratégia completa não se traduziu em menor Brier/AP no fold 9. O ganho marginal dos indicadores de ausência é pequeno.
A pergunta permanece pertinente porque a cobertura de E1 é limitada e a ordenação das políticas muda entre critérios. Generalização externa, utilidade clínica, causalidade e originalidade permanecem não demonstradas.
Detalhes completos, ICs OOF de Brier, métricas com peso igual por paciente, frequências demográficas e todos os limiares estão nos [resultados JSON](phase5/run001/evaluation.json), [composição](phase5/run001/composition.json) e [configuração](phase5/run001/config.json).
