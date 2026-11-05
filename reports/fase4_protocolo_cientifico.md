# Fase 4 — protocolo científico candidato
Versão 1, 04/11/2026. Estado — preparado para aprovação da pergunta e do desenho. Nenhum modelo treinado. Não constitui registro prospectivo externo.

## Pergunta e escopo
Em exames PTB-XL 1.0.3, como a exigência de completude das medidas ECGDeli altera a cobertura e a avaliação de classificadores da anotação CRBBB, e qual é o erro probabilístico de estratégias que atendem a mesma população de referência?

Tema delimitado — avaliação de políticas de disponibilidade de medidas para reconhecimento de bloqueio completo de ramo direito anotado no ECG. O alvo é a presença da chave CRBBB em scp_codes, independentemente de sua confiança numérica. Ausência da chave significa ausência da anotação, não exclusão clínica confirmada. Não agregar IRBBB. A anotação deriva de interpretação do ECG, não de seguimento clínico. Revisão por especialista antes da aprovação deve conferir sentido do alvo e do painel. [Documentação original](https://physionet.org/content/ptb-xl/1.0.3/)

Hipótese principal H1 — E3, regressão logística com 531 medidas e imputação, terá menor Brier que E2 com painel de oito e fallback de prevalência, considerando todos os exames do teste. Definir Δ = Brier(E3) − Brier(E2-fallback). Estimar Δ e IC95%, admitindo resultado em qualquer direção. Superioridade estatística exige limite superior abaixo de zero. Não foi estabelecida margem de importância clínica, portanto significância não demonstra utilidade.

Hipóteses secundárias — a seleção por completude muda a composição da amostra e as métricas de um modelo fixo; usar 531 variáveis pode alterar desempenho em comparação às oito quando treino e avaliação são os mesmos; acrescentar indicadores de ausência pode alterar discriminação e calibração. São análises secundárias, com intervalos descritivos e sem promoção a conclusão primária por resultado favorável.

## Evidências disponíveis antes do treino
A [auditoria offline](phase4/preflight.json) validou os 17 hashes do manifesto da Fase 3, 531 colunas numéricas, correspondência um para um dos ecg_id e ausência de pacientes entre folds. Nenhum número não finito ou token não numérico fora dos códigos de ausência declarados foi encontrado. Isso não valida plausibilidade fisiológica de cada medida.

| Partição | Exames | Pacientes | CRBBB exames/pacientes | Completos 531 / positivos | Completos 8 / positivos |
|---|---:|---:|---:|---:|---:|
| Treino 1–8 | 17.418 | 15.023 | 432 / 370 | 8.874 / 212 | 17.417 / 432 |
| Validação 9 | 2.183 | 1.942 | 55 / 49 | 1.137 / 22 | 2.183 / 55 |
| Teste 10 | 2.198 | 1.904 | 54 / 45 | 1.088 / 35 | 2.198 / 54 |

Prevalência por exame é 2,48%, 2,52% e 2,46%, respectivamente. Os rótulos CRBBB têm confiança 100 em 428/432 registros de treino, 54/55 de validação e 54/54 de teste. Não remover registros de baixa confiança silenciosamente. A análise primária mantém a definição por presença. Sensibilidade por confiança seria emenda exploratória, sem substituir o resultado primário.

As contagens de teste foram consultadas por exigência de viabilidade, antes do treinamento. Nenhuma previsão, perda ou ordenação de modelos foi calculada. O conjunto é reservado para avaliação preditiva, mas não inteiramente desconhecido. O painel foi escolhido após exploração de disponibilidade no desenvolvimento. Documentar esse histórico em qualquer publicação. O teste 10 é interno, separado por paciente, não validação externa independente.

## Viabilidade técnica
Tabelas e licenças CC BY 4.0 já estão locais. A tabela de medidas tem 62.235.868 bytes. Matriz total densa float64 ocupa aproximadamente 88 MiB, sem overhead. Dataframes, cópias, validação cruzada e imputação podem exigir 1–4 GiB, estimativa de planejamento. O equipamento inspecionado na Fase 3 tem aproximadamente 16 GiB. Usar CPU e execução serial, sem GPU ou serviço pago.

Estimativa não medida de treinamento — minutos a poucas horas para logística e grade pequena, dependendo de convergência, CPU e implementação. Reservar um dia de execução para desenvolvimento, bootstrap e relatórios. Cronometrar piloto apenas após aprovação. Se exceder 4 GiB ou 4 horas na etapa piloto, registrar e revisar orçamento antes de ampliar. Não prometer duração como benchmark executado.

A auditoria e os testes usam biblioteca padrão Python 3.13.7. Ambiente observado tem numpy 2.5.4 e pandas 3.0.6. SciPy e scikit-learn ausentes. Treino futuro requer ambiente virtual isolado com numpy, scipy, pandas e scikit-learn compatíveis, teste de instalação e lock de versões exatas. Nenhum pacote foi instalado nesta fase. Sem extração nova de sinais, WFDB, MATLAB e redes profundas são desnecessários.

## Controle e reprodução
Configuração candidata em [experiments/fase4.json](../experiments/fase4.json), integridade reutilizável em src/datamind, testes em tests. Executar da raiz do projeto

```powershell
python scripts/verify_phase2.py
python scripts/fase4_preflight.py
python -m unittest discover -s tests -v
```

O preflight verifica entradas pelo manifesto existente e escreve somente reports/phase4/preflight.json. Não baixa nem altera brutos. A configuração não habilita treino e não existe executor de modelagem nesta entrega. Antes do futuro teste final, congelar protocolo, configuração, IDs, ambiente, código e hashes. Registrar toda emenda com data, motivo e acesso aos resultados já ocorrido. Resultados confirmatórios se limitam ao contraste principal congelado antes das previsões de teste. Análises motivadas pelos resultados serão explicitamente exploratórias.

[Desenho operacional](../docs/fase4_desenho_experimental.md) · [Riscos](../docs/fase4_riscos_metodologicos.md) · [Literatura](../docs/fase4_literatura_relacionada.md) · [Decisão](fase4_decisao.md)
