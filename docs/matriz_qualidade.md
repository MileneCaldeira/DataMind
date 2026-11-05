# Matriz de qualidade e políticas — Heart Disease

Gerado por `python scripts/phase2.py`. Unidade: registro no arquivo processado; não pessoa comprovadamente única. Contagens integrais; nenhuma imputação ou deduplicação. Regras exploratórias, não protocolo clínico validado.

## Completude e alertas por variável

Cada célula: ausentes explícitos / alertas de domínio ou não positividade. Denominadores: Cleveland 303, Hungarian 294, Switzerland 123, VA 200. `oldpeak < 0` é relatado separadamente, sem ser declarado inválido.

| Variável | Cleveland | Hungarian | Switzerland | VA |
|---|---:|---:|---:|---:|
| age | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| sex | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| cp | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| trestbps | 0 / 0 | 1 / 0 | 2 / 0 | 56 / 1 |
| chol | 0 / 0 | 23 / 0 | 0 / 123 | 7 / 49 |
| fbs | 0 / 0 | 8 / 0 | 75 / 0 | 7 / 0 |
| restecg | 0 / 0 | 1 / 0 | 1 / 0 | 0 / 0 |
| thalach | 0 / 0 | 1 / 0 | 1 / 0 | 53 / 0 |
| exang | 0 / 0 | 1 / 0 | 1 / 0 | 53 / 0 |
| oldpeak | 0 / 0 | 0 / 0 | 6 / 0 | 56 / 0 |
| slope | 0 / 0 | 190 / 0 | 17 / 0 | 102 / 0 |
| ca | 4 / 0 | 291 / 0 | 118 / 0 | 198 / 0 |
| thal | 2 / 0 | 266 / 0 | 52 / 0 | 166 / 0 |
| num | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |

Alertas: categorias fora do dicionário; `age`, `trestbps`, `chol` ou `thalach` ≤ 0. Alertas não são prova de erro nem códigos de ausência. As regras de elegibilidade P3/P4 só aplicam alertas às variáveis exigidas.

## Distribuições (todos os valores observados, inclusive alertas)

| Centro | Variável | n observado | Mínimo | Q1 | Mediana | Q3 | Máximo |
|---|---|---:|---:|---:|---:|---:|---:|
| cleveland | age | 303 | 29.0 | 48.0 | 56.0 | 61.0 | 77.0 |
| cleveland | trestbps | 303 | 94.0 | 120.0 | 130.0 | 140.0 | 200.0 |
| cleveland | chol | 303 | 126.0 | 211.0 | 241.0 | 275.0 | 564.0 |
| cleveland | thalach | 303 | 71.0 | 133.5 | 153.0 | 166.0 | 202.0 |
| cleveland | oldpeak | 303 | 0.0 | 0.0 | 0.8 | 1.6 | 6.2 |
| hungarian | age | 294 | 28.0 | 42.0 | 49.0 | 54.0 | 66.0 |
| hungarian | trestbps | 293 | 92.0 | 120.0 | 130.0 | 140.0 | 200.0 |
| hungarian | chol | 271 | 85.0 | 209.0 | 243.0 | 282.5 | 603.0 |
| hungarian | thalach | 293 | 82.0 | 122.0 | 140.0 | 155.0 | 190.0 |
| hungarian | oldpeak | 294 | 0.0 | 0.0 | 0.0 | 1.0 | 5.0 |
| switzerland | age | 123 | 32.0 | 51.0 | 56.0 | 61.5 | 74.0 |
| switzerland | trestbps | 121 | 80.0 | 115.0 | 125.0 | 145.0 | 200.0 |
| switzerland | chol | 123 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| switzerland | thalach | 122 | 60.0 | 104.25 | 121.0 | 140.0 | 182.0 |
| switzerland | oldpeak | 117 | -2.6 | 0.0 | 0.3 | 1.5 | 3.7 |
| va | age | 200 | 35.0 | 55.0 | 60.0 | 64.0 | 77.0 |
| va | trestbps | 144 | 0.0 | 120.0 | 130.0 | 147.0 | 190.0 |
| va | chol | 193 | 0.0 | 0.0 | 216.0 | 258.0 | 458.0 |
| va | thalach | 147 | 69.0 | 109.0 | 120.0 | 140.0 | 180.0 |
| va | oldpeak | 144 | -0.5 | 0.0 | 1.5 | 2.0 | 4.0 |

Quantis por interpolação linear em posição (n−1)p. Frequências completas de todas as variáveis, incluindo categorias, estão em [heart_analysis.json](../reports/phase2/heart_analysis.json). Não comparar medianas de variáveis ordinais como medidas contínuas.

## Políticas explícitas

- **P0**: Todos os registros processados; preservar ausências e alertas. Exigidas: nenhuma.
- **P1**: Casos completos nos 14 campos; somente ausências explícitas. Exigidas: age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, num.
- **P2**: Casos completos em 8 campos de repouso/demografia/alvo. Exigidas: age, sex, cp, trestbps, chol, fbs, restecg, num.
- **P3**: P2 mais domínios categóricos e idade/pressão/colesterol positivos. Exigidas: age, sex, cp, trestbps, chol, fbs, restecg, num.
- **P4**: P3 retirando colesterol do esquema exigido. Exigidas: age, sex, cp, trestbps, fbs, restecg, num.

P1 usa deleção por completude; P2 restringe a pergunta ao conjunto pré-exercício escolhido para sensibilidade; P3 acrescenta conformidade/plausibilidade mínima; P4 abandona a exigência de colesterol e muda o conjunto de informação. Não são tratamentos equivalentes da mesma pergunta. Referências e justificativas em [validação](../reports/validacao_cientifica.md).

## Elegibilidade e composição

| Política | Centro | Elegíveis / total | Retenção % | Participação do centro % | Idade média | Sexo 0 % | Alvo >0 % |
|---|---|---:|---:|---:|---:|---:|---:|
| P0 | cleveland | 303 / 303 | 100.0 | 32.93 | 54.44 | 32.01 | 45.87 |
| P0 | hungarian | 294 / 294 | 100.0 | 31.96 | 47.83 | 27.55 | 36.05 |
| P0 | switzerland | 123 / 123 | 100.0 | 13.37 | 55.32 | 8.13 | 93.5 |
| P0 | va | 200 / 200 | 100.0 | 21.74 | 59.35 | 3.0 | 74.5 |
| P1 | cleveland | 297 / 303 | 98.02 | 99.33 | 54.54 | 32.32 | 46.13 |
| P1 | hungarian | 1 / 294 | 0.34 | 0.33 | 47.0 | 0.0 | 100.0 |
| P1 | switzerland | 0 / 123 | 0.0 | 0.0 | — | — | — |
| P1 | va | 1 / 200 | 0.5 | 0.33 | 56.0 | 0.0 | 100.0 |
| P2 | cleveland | 303 / 303 | 100.0 | 40.73 | 54.44 | 32.01 | 45.87 |
| P2 | hungarian | 261 / 294 | 88.78 | 35.08 | 47.77 | 26.44 | 37.55 |
| P2 | switzerland | 47 / 123 | 38.21 | 6.32 | 56.85 | 6.38 | 97.87 |
| P2 | va | 133 / 200 | 66.5 | 17.88 | 59.34 | 3.76 | 76.69 |
| P3 | cleveland | 303 / 303 | 100.0 | 45.63 | 54.44 | 32.01 | 45.87 |
| P3 | hungarian | 261 / 294 | 88.78 | 39.31 | 47.77 | 26.44 | 37.55 |
| P3 | switzerland | 0 / 123 | 0.0 | 0.0 | — | — | — |
| P3 | va | 100 / 200 | 50.0 | 15.06 | 59.84 | 5.0 | 78.0 |
| P4 | cleveland | 303 / 303 | 100.0 | 39.35 | 54.44 | 32.01 | 45.87 |
| P4 | hungarian | 284 / 294 | 96.6 | 36.88 | 47.82 | 26.76 | 36.27 |
| P4 | switzerland | 47 / 123 | 38.21 | 6.1 | 56.85 | 6.38 | 97.87 |
| P4 | va | 136 / 200 | 68.0 | 17.66 | 59.5 | 3.68 | 77.21 |

A proporção `num>0` é uma sumarização derivada explícita; o alvo original não é substituído. Percentuais não são prevalência populacional. Com n=0 a composição é indefinida; com n=1 não há estabilidade inferencial.

## Retenção por subgrupo: numerador / denominador

| Política | Centro | Sexo 0 | Sexo 1 | Idade ≥65 | Idade <65 | Alvo 0 | Alvo >0 |
|---|---|---:|---:|---:|---:|---:|---:|
| P1 | cleveland | 96 / 97 | 201 / 206 | 41 / 41 | 256 / 262 | 160 / 164 | 137 / 139 |
| P1 | hungarian | 0 / 81 | 1 / 213 | 0 / 4 | 1 / 290 | 0 / 188 | 1 / 106 |
| P1 | switzerland | 0 / 10 | 0 / 113 | 0 / 16 | 0 / 107 | 0 / 8 | 0 / 115 |
| P1 | va | 0 / 6 | 1 / 194 | 0 / 42 | 1 / 158 | 0 / 51 | 1 / 149 |
| P2 | cleveland | 97 / 97 | 206 / 206 | 41 / 41 | 262 / 262 | 164 / 164 | 139 / 139 |
| P2 | hungarian | 69 / 81 | 192 / 213 | 3 / 4 | 258 / 290 | 163 / 188 | 98 / 106 |
| P2 | switzerland | 3 / 10 | 44 / 113 | 9 / 16 | 38 / 107 | 1 / 8 | 46 / 115 |
| P2 | va | 5 / 6 | 128 / 194 | 26 / 42 | 107 / 158 | 31 / 51 | 102 / 149 |
| P3 | cleveland | 97 / 97 | 206 / 206 | 41 / 41 | 262 / 262 | 164 / 164 | 139 / 139 |
| P3 | hungarian | 69 / 81 | 192 / 213 | 3 / 4 | 258 / 290 | 163 / 188 | 98 / 106 |
| P3 | switzerland | 0 / 10 | 0 / 113 | 0 / 16 | 0 / 107 | 0 / 8 | 0 / 115 |
| P3 | va | 5 / 6 | 95 / 194 | 22 / 42 | 78 / 158 | 22 / 51 | 78 / 149 |
| P4 | cleveland | 97 / 97 | 206 / 206 | 41 / 41 | 262 / 262 | 164 / 164 | 139 / 139 |
| P4 | hungarian | 76 / 81 | 208 / 213 | 4 / 4 | 280 / 290 | 181 / 188 | 103 / 106 |
| P4 | switzerland | 3 / 10 | 44 / 113 | 9 / 16 | 38 / 107 | 1 / 8 | 46 / 115 |
| P4 | va | 5 / 6 | 131 / 194 | 28 / 42 | 108 / 158 | 31 / 51 | 105 / 149 |

## Comparabilidade semântica

| Campos | Correspondência disponível | Limite |
|---|---|---|
| age, sex | Mesmos nomes e códigos no dicionário | Mesma mensuração e seleção entre centros não verificadas; sex 0/1 é codificação histórica |
| cp, fbs, restecg | Domínios documentados compartilhados | Não há adjudicação independente de diagnóstico ou padronização de procedimentos |
| trestbps, chol | Unidades documentadas mmHg e mg/dl | Zeros requerem investigação; nenhum motivo de não coleta foi demonstrado |
| thalach, exang, oldpeak, slope | Medidas ligadas ao exercício | Protocolo de exercício original #28 varia e possui dúvidas no arquivo ask-detrano; equivalência operacional não estabelecida |
| ca, thal | Domínios documentados | Grande perda de dados em três centros; disponibilidade não implica comparabilidade clínica |
| num | Status angiográfico; resumo permite 0 vs >0 | Dicionário não resolve interpretação ordinal 1–4, fronteira exata 50% e derivação histórica; versão húngara processada é binária |

Ver [documentação dos 76 atributos](heart_documentacao.md). Não se demonstrou acurácia por padrão-ouro, equivalência de instrumentos ou mecanismo MCAR/MAR/MNAR. Diferenças de retenção mostram seleção observada; viés relativo à população clínica não é identificável aqui.
