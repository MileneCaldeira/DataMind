# Fase 4 — desenho experimental
Versão candidata de 04/11/2026. O [protocolo](../reports/fase4_protocolo_cientifico.md) define pergunta, hipóteses e população. Aqui ficam as regras executáveis futuras.

## Unidades e conjuntos
Unidade de previsão e estimando primário — exame. Cada exame recebe peso igual nas métricas. Paciente é unidade de separação e reamostragem. Pessoas com mais exames contribuem mais ao estimando por exame. Sensibilidade secundária dará peso 1/n_exames_do_paciente a cada exame. Não escolher um exame por pessoa após observar desempenho.

R é a população de referência do fold avaliado, com join íntegro e anotação interpretável. A auditoria atual encontrou todos os registros elegíveis para R. C contém exames de R com as 531 medidas disponíveis. P contém exames com as oito medidas disponíveis. Como o painel é subconjunto, C está contido em P. M é R menos C. Não usar ausência de medida como ausência de CRBBB.

Painel fixado exploratoriamente na Fase 3 — QRS_Dur_Global, RR_Mean_Global, QRS_Dur_V1, R_Amp_V1, S_Amp_V1, QRS_Dur_V6, R_Amp_V6, S_Amp_V6. Abrange duração e morfologia relevantes para condução, mas não é escore clínico validado. Todas as 531 colunas são medidas/resumos do extrator, não 531 variáveis independentes. Confirmar unidades por descrição oficial antes do treino. Zero é valor, nunca ausência automática.

## Estratégias e controles
| Estratégia | Treino | Variáveis e ausência | População atendida |
|---|---|---|---|
| B0 | Todos os exames de treino | Probabilidade constante igual à prevalência do treino | R |
| E1 | C de treino | 531 medidas, sem imputar | C, abstém-se fora de C |
| E2-C | Mesmo C de treino de E1 | Painel de oito, sem imputar | P |
| E2 | P de treino | Painel de oito, sem imputar | P |
| E2-fallback | E2 e B0 | E2 em P, B0 em R menos P | R |
| E3 | R de treino | 531 medidas, mediana de treino | R |
| E3-I | R de treino | E3 mais indicadores fixos de ausência para todas as 531 colunas | R |
| Híbrida, secundária | E1, E2 e B0 | E1 em C, E2 em P menos C, B0 no restante | R |

E1 significa 531 colunas exigidas para elegibilidade. Colunas constantes no treino não têm coeficiente informativo e podem ser removidas pelo pipeline, registrando a lista. Isso não muda a definição de C. Para E3, coluna totalmente ausente no treino recebe constante zero e indicador quando aplicável, com registro explícito. Não estimar sua mediana em validação ou teste. Valores observados zero são preservados.

## Contrastes que separam as causas
1. **Escolha de variáveis** — E1 versus E2-C no mesmo C de teste, treinados exatamente no mesmo C de treino, mesma família, regularização e procedimento de ajuste. Diferença é do conjunto de variáveis sob esse protocolo, não efeito causal de cada medida.
2. **População de treinamento** — E2-C versus E2 no mesmo C de teste. Isola ampliação da amostra de treinamento mantendo o painel.
3. **Seleção na avaliação** — manter E2 fixo e comparar resultados em C e P menos C. Reportar prevalência, distribuição e métricas por estrato. Diferença entre grupos é associativa. AUC é dependente da composição, não atribuir diferença automaticamente à dificuldade intrínseca.
4. **Política operacional** — contraste primário E3 versus E2-fallback, ambos em R de teste. Comparar também híbrida e B0, secundariamente. E1 sozinho não possui Brier em R porque não prevê fora de C.

Para cada estratégia mostrar cobertura total, cobertura entre positivos, métricas condicionais nos atendidos e composição de excluídos. Atribuir probabilidade zero aos excluídos seria mudar a política, portanto não fazer. A abstenção não é acerto nem erro definido sem função de custo.

## Ajuste e prevenção de vazamento
Usar folds oficiais 1–8 para desenvolvimento. Validação cruzada Leave-One-Official-Fold-Out nesses oito grupos, sem misturar pacientes. Pipeline inteiro ajustado dentro de cada treino interno. Selecionar C da logística L2 em {0.01, 0.1, 1, 10} pelo Brier médio das previsões fora do fold no suporte de cada braço. Empate numérico até 1e-6 favorece C menor. Para comparação de variáveis E1/E2-C, incluir controle com C=1 comum, além dos modelos ajustados.

Padronizar pela média/desvio do treino após imputação. Desvio zero tratado explicitamente como constante. Não selecionar colunas por correlação com alvo global. Não incluir patient_id, ecg_id, fold, laudo, scp_codes, diagnóstico automático, confiança do rótulo, validadores, aparelho ou local como preditores. Metadados são apenas para integridade e descrição. Não usar imputação condicionada ao alvo na implantação.

Logística L2 é baseline probabilístico, interpretável e adequado ao porte. Sem pesos de classe ou oversampling no primário, para manter a distribuição observada. Avaliar classe rara por AP e sensibilidade, não acurácia. Random forest seria extensão exploratória que requer emenda e orçamento próprios. Redes profundas não são necessárias à pergunta.

Após escolher C em 1–8, ajustar os pipelines em seus respectivos conjuntos de 1–8. Fold 9 serve somente para escolher limiar operacional de cada estratégia. Fixar menor limiar que alcance especificidade observada ≥95% no suporte da estratégia, maximizando sensibilidade entre os admissíveis. Critério é experimental, sem alegação de segurança clínica. Congelar limiar antes do teste. Se alguma classe faltar no suporte, não definir limiar e registrar limitação.

Calibração primária avalia probabilidades originais, sem pós-calibração ajustada em 9. Isso evita repartir 55 positivos entre calibrador e escolha de limiar. Uma análise futura com Platt exigirá protocolo próprio ou cross-fitting no desenvolvimento. Não retreinar incluindo fold 9 antes de aplicar os limiares definidos.

## Métricas e inferência
Primário — diferença pareada de Brier em R, com IC95% por bootstrap de pacientes. Brier é média de (p−y)², sensível ao erro probabilístico e à prevalência. Sempre apresentar B0, pois baixa prevalência pode dar Brier pequeno a modelo pouco útil.

Secundários — average precision, explicitamente AP e não área trapezoidal PR, ROC-AUC, sensibilidade/especificidade no limiar congelado, Brier por estrato, calibração média, gráfico de calibração em cinco faixas fixas de probabilidade [0,.02,.05,.10,.20,1]. Mostrar n e positivos em cada faixa. Intercepto/inclinação de calibração como diagnóstico no teste, nunca correção das previsões. Clipping numérico de p para [1e-6,1−1e-6] somente para logit, registrado. Se ajuste de calibração não convergir, reportar indisponível.

Bootstrap com 2.000 réplicas e semente 20261104, amostrando pacientes de teste com reposição e carregando todos os seus exames. Usar os mesmos sorteios para todos os modelos e contrastes. Intervalos percentis. Réplicas sem ambas as classes deixam AUC/AP indisponíveis, com fração de réplicas válidas reportada. Brier permanece definido. Intervalos condicionais aos modelos treinados não incluem variabilidade de novo treinamento.

O teste tem só 45 pacientes com algum CRBBB, e C contém 35 exames positivos. Não alegar poder suficiente para equivalência, não inferioridade ou subgrupos. Não há margem clínica fixada. Δ com IC abrangendo zero é inconclusivo. Resultado desfavorável ou precisamente nulo deve ser publicado como tal, sem trocar alvo, política ou métrica primária.

## Composição e prestação de contas
Descrever C, P menos C e R menos P em cada partição por idade, sexo codificado, aparelho/local, prevalência e número de exames por paciente. Apresentar contagens, percentuais e diferenças padronizadas, sem testes em massa. Idades muito elevadas podem refletir anonimização, exigindo documentação antes de interpretação. Missingness pode ser informativo ou refletir ondas não identificáveis, não prova defeito de coleta.

A escolha final será baseada no contraste primário, cobertura, calibração e incerteza, com trade-offs explícitos. Uma estratégia pode discriminar melhor e calibrar pior. Sem função de custo clínica, não declarar vencedora universal.
