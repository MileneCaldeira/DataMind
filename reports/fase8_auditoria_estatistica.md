
# Auditoria estatística e computacional — Fase 8
05/11/2026. Auditoria de números e implementação existente; não nova análise inferencial.

## Rastreabilidade dos resultados
|Conteúdo do manuscrito|Fonte original / localização|Conferência|
|---|---|---|
|Exames/pacientes/positivos por partição|reports/phase4/preflight.json, partitions|17.418/15.023/432; 2.183/1.942/55; 2.198/1.904/54|
|Pacientes positivos no teste|partitions.test.positive_patients|45|
|Brier, AUC, AP, médias e classificação|phase6/final001/metrics.json, overall|Tabela integral e texto reconciliados com arredondamento|
|Δ primário e IC95%|metrics.json, primary|−0,0006129320876249411; [−0,002380012257832108; +0,0011330219950107495]|
|Cobertura|overall.E1.coverage / positive_coverage|1.088/2.198 = 49,50%; 35/54 = 64,81%|
|Contrastes de controles|paired_secondary e bootstrap.paired_brier|Reapresentados, não recalculados|
|Estratos e composição|metrics.json.strata; composition.json|35 positivos completos; 19 incompletos; 130 pacientes em ambos|
|Idade|composition.json, age_median_under90|62/64 anos entre valores <90; não mediana irrestrita|
|Fold 9|phase5/run001/evaluation.json, validation|Brier E2-fallback 0,007983; E3 0,008256; contraste +0,000273 e IC incluindo zero|
|Calibração|overall.*.calibration; evaluation.py|Faixas e ajustes já existentes, sem novo fit|

## Avaliação dos dez controles solicitados
1. Primário preservado. Híbrida permanece secundária, mesmo com menor Brier pontual integral.
2. Primário pareado nos 2.198 exames. E1 separado da tabela integral; controles E1/E2-C e C=1 em 1.088 completos.
3. IC primário cruza zero: inconclusivo para direção congelada.
4. Não há equivalência/não inferioridade: margem não foi definida; não fazer teste retrospectivo.
5. Sensibilidade 100% é 54/54 exames nas estratégias integrais, oriundos de 45 pacientes. Reamostrar só acertos gera [1;1]; não significa precisão perfeita. Não substituímos por intervalo binomial de exames independentes.
6. AUC alta refere-se à anotação do mesmo sinal; não diagnóstico independente.
7. Fallback não acionado em 9/10, logo nenhum contraste empírico entre E2 e seu fallback nesses conjuntos.
8. Código cluster_intervals sorteia pacientes com reposição e atribui multiplicidade a todos os seus exames; mesmos sorteios entre braços. Não executado nesta fase.
9. C selecionado por braço pode explicar parte das diferenças, mas os resultados não identificam causalmente a contribuição de C. C=1 fixa valor nominal, não graus de liberdade efetivos.
10. Fold 9 escolheu limiar; fold 10 estima resultado final condicionado ao limiar. Os dois não foram agrupados para estimar desempenho.

## Crítica estatística
**Brier e prevalência.** É uma perda probabilística própria, mas seu nível depende do desfecho raro. B0 usa a prevalência do treino, e não a do teste otimizada retrospectivamente. Comparações no mesmo suporte são informativas; diferenças entre estratos não isolam desempenho. Não introduzimos Brier escalado, decomposição ou benefício líquido.

**Calibração.** O programa ajusta a e b conjuntamente em logit(Y) = a+b logit(p), com clipping numérico apenas para logit. Assim a não é o intercepto obtido com offset b=1. Faixas fixas têm poucos eventos; média prevista próxima da prevalência não valida toda a escala. Valores de a/b são diagnósticos pontuais sem IC, não estimativas precisas para uso clínico. Nenhuma nova regressão de calibração foi executada.

**Estimando e dependência.** Exames têm peso igual; pacientes com múltiplos exames influenciam mais o alvo estimado. Reamostragem por paciente preserva agrupamento observado, mas não incorpora dependência por equipamento/local nem garante representatividade externa. A análise de peso igual por paciente existe nos JSON, mas não foi promovida a novo resultado principal.

**Precisão.** As 2.000 réplicas percentis não incorporam incerteza de novos treinos, seleção de C, escolha do painel ou limiar. Não quantificamos erro Monte Carlo adicional nesta revisão. A amostra positiva pequena restringe conclusões sobre calibração, AP, sensibilidade e subgrupos; não justifica declarar efeito nulo.

**Regularização.** E1−E2-C ajustado: −0,003409 [−0,006613; −0,000498]; controle C=1: +0,000465 [−0,003872; +0,005073]. Diferença de conclusões pontuais exige moderação; não constitui teste formal de interação entre regularização e painel. E2-C−E2: +0,000842 [−0,000126; +0,001830], também secundário.

## Integridade e limites da verificação
scripts/fase8_verify.py usa somente biblioteca padrão para hashes, cardinalidade, pacientes, igualdade de probabilidades já armazenadas e correspondência de números. Não importa modelos, não reamostra, não recalcula Brier nem ajusta calibradores. Confere manifestos anteriores, 17 arquivos brutos, versões declaradas e fontes das tabelas. O manifesto da Fase 7 inclui figuras e v1; todos permanecem imutáveis.

A auditoria lê ainda os testes/logs históricos e a implementação; não reexecuta testes que treinam modelos ou escrevem em artefatos anteriores. Campos legados primary/paired e bootstrap.metrics de sensibilidade usam 0,5; overall/strata e bootstrap.binary_frozen_thresholds correspondem aos limiares congelados. V2 mantém a fonte correta.

Não houve discrepância numérica material detectada. A checagem automatizada de valores arredondados é complementada por leitura contextual; presença de um número em JSON, isoladamente, não prova sua atribuição correta. Registro: reports/phase8/verification.json. Questões humanas: fase8_pendencias_especialistas.md.
