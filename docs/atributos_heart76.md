# Inventário dos 76 atributos originais

Gerado do dicionário no ZIP UCI. Ausências são valores numéricos −9; não incluem zeros nem códigos fora de domínio. Cleveland bruto não auditado por corrupção documentada. H/S/V: Hungarian (294), Switzerland (123), VA (200).

| Posição | Nome original | Nos 14 processados? | Ausentes H | Ausentes S | Ausentes V |
|---:|---|---|---:|---:|---:|
| 1 | id | não | 0 | 0 | 0 |
| 2 | ccf | não | 0 | 0 | 0 |
| 3 | age | sim | 0 | 0 | 0 |
| 4 | sex | sim | 0 | 0 | 0 |
| 5 | painloc | não | 0 | 0 | 0 |
| 6 | painexer | não | 0 | 0 | 0 |
| 7 | relrest | não | 0 | 0 | 4 |
| 8 | pncaden | não | 294 | 123 | 200 |
| 9 | cp | sim | 0 | 0 | 0 |
| 10 | trestbps | sim | 1 | 2 | 56 |
| 11 | htn | não | 1 | 30 | 3 |
| 12 | chol | sim | 23 | 0 | 7 |
| 13 | smoke | não | 282 | 100 | 5 |
| 14 | cigs | não | 293 | 112 | 10 |
| 15 | years | não | 294 | 121 | 12 |
| 16 | fbs | sim | 8 | 75 | 7 |
| 17 | dm | não | 273 | 115 | 157 |
| 18 | famhist | não | 293 | 121 | 8 |
| 19 | restecg | sim | 1 | 1 | 0 |
| 20 | ekgmo | não | 0 | 1 | 52 |
| 21 | ekgday | não | 0 | 1 | 53 |
| 22 | ekgyr | não | 0 | 1 | 52 |
| 23 | dig | não | 1 | 5 | 60 |
| 24 | prop | não | 2 | 2 | 60 |
| 25 | nitr | não | 1 | 3 | 59 |
| 26 | pro | não | 1 | 1 | 59 |
| 27 | diuretic | não | 1 | 6 | 73 |
| 28 | proto | não | 9 | 50 | 53 |
| 29 | thaldur | não | 2 | 1 | 53 |
| 30 | thaltime | não | 190 | 34 | 160 |
| 31 | met | não | 2 | 50 | 53 |
| 32 | thalach | sim | 1 | 1 | 53 |
| 33 | thalrest | não | 1 | 1 | 54 |
| 34 | tpeakbps | não | 1 | 3 | 59 |
| 35 | tpeakbpd | não | 1 | 3 | 59 |
| 36 | dummy | não | 1 | 2 | 56 |
| 37 | trestbpd | não | 1 | 2 | 56 |
| 38 | exang | sim | 1 | 1 | 53 |
| 39 | xhypo | não | 2 | 3 | 53 |
| 40 | oldpeak | sim | 0 | 6 | 56 |
| 41 | slope | sim | 190 | 17 | 101 |
| 42 | rldv5 | não | 1 | 77 | 65 |
| 43 | rldv5e | não | 0 | 77 | 65 |
| 44 | ca | sim | 290 | 118 | 198 |
| 45 | restckm | não | 294 | 123 | 200 |
| 46 | exerckm | não | 294 | 123 | 199 |
| 47 | restef | não | 294 | 123 | 172 |
| 48 | restwm | não | 291 | 123 | 173 |
| 49 | exeref | não | 294 | 123 | 198 |
| 50 | exerwm | não | 292 | 123 | 197 |
| 51 | thal | sim | 266 | 50 | 159 |
| 52 | thalsev | não | 267 | 51 | 169 |
| 53 | thalpul | não | 277 | 97 | 199 |
| 54 | earlobe | não | 294 | 123 | 199 |
| 55 | cmo | não | 0 | 9 | 2 |
| 56 | cday | não | 0 | 9 | 0 |
| 57 | cyr | não | 0 | 9 | 0 |
| 58 | num | sim | 0 | 0 | 0 |
| 59 | lmt | não | 275 | 0 | 0 |
| 60 | ladprox | não | 236 | 0 | 0 |
| 61 | laddist | não | 246 | 0 | 0 |
| 62 | diag | não | 276 | 0 | 0 |
| 63 | cxmain | não | 235 | 0 | 0 |
| 64 | ramus | não | 285 | 0 | 0 |
| 65 | om1 | não | 271 | 0 | 0 |
| 66 | om2 | não | 289 | 0 | 1 |
| 67 | rcaprox | não | 244 | 0 | 1 |
| 68 | rcadist | não | 269 | 0 | 1 |
| 69 | lvx1 | não | 0 | 17 | 2 |
| 70 | lvx2 | não | 0 | 17 | 2 |
| 71 | lvx3 | não | 0 | 17 | 2 |
| 72 | lvx4 | não | 0 | 17 | 2 |
| 73 | lvf | não | 0 | 13 | 3 |
| 74 | cathef | não | 266 | 17 | 23 |
| 75 | junk | não | 294 | 123 | 81 |
| 76 | name | não | campo artificial | campo artificial | campo artificial |

Uma coluna preenchida com valores artificiais ou sem definição não se torna utilizável por ter completude alta. Definições, incertezas e grupos semânticos em [heart_documentacao.md](heart_documentacao.md). Valores observados e resumos numéricos dos 75 campos numéricos estão em `raw76_profiles` de [heart_analysis.json](../reports/phase2/heart_analysis.json).
