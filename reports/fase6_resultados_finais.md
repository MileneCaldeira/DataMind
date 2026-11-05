# Fase 6 — resultados finais

Consolidação em 05/11/2026. Uma execução preditiva, sem retreinamento. Esta consolidação usa exclusivamente arquivos já salvos.

## Integridade e análise primária

Os 57 arquivos congelados e 17 hashes de dados permanecem íntegros. Os 18 testes prévios passaram. Confirmados join 1:1, separação de pacientes e correspondência exata entre predictions.csv e sete arquivos individuais. Os registros mostram uma chamada por pipeline e nenhuma previsão anterior de 10 nos artefatos auditados. Isso não verifica atividades fora do repositório.
A população primária contém 2.198 exames de 1.904 pacientes, com 54 exames positivos em 45 pacientes. E3 e E2-fallback cobrem exatamente os mesmos exames. Fallback acionado em zero exames, tanto em 9 quanto em 10.
**Δ Brier E3 − E2-fallback = -0.000613, IC95% [-0.002380; 0.001133]. A hipótese de menor Brier de E3 não recebeu suporte estatístico pelo critério congelado.** O intervalo contém zero e admite efeitos em ambas as direções. Ausência de suporte não demonstra equivalência.
Bootstrap percentil com 2.000 réplicas, semente 20261104, reamostragem de pacientes com todos os seus exames. Intervalos condicionais aos modelos treinados. O contraste e seu intervalo foram reconciliados por uma implementação independente a partir das perdas salvas.

## Métricas por estratégia

Brier menor é melhor. AUC e AP maiores indicam melhor discriminação. E1 e E1_C1 têm suporte C e não devem ser comparados diretamente a estratégias de cobertura integral.

| Estratégia | Exames / pacientes | Positivos | Cobertura exames / positivos | Brier e IC95% | ROC-AUC e IC95% | AP e IC95% |
|---|---:|---:|---:|---|---|---|
| B0 | 2198 / 1904 | 54 | 100.00% / 100.00% | 0.023964 [0.016978; 0.031105] | 0.500000 [0.500000; 0.500000] | 0.024568 [0.017217; 0.032081] |
| E1 | 1088 / 1021 | 35 | 49.50% / 64.81% | 0.005830 [0.003082; 0.008945] | 0.998616 [0.996738; 0.999859] | 0.953360 [0.880419; 0.995763] |
| E2-C | 2198 / 1904 | 54 | 100.00% / 100.00% | 0.007052 [0.004673; 0.009552] | 0.996994 [0.994836; 0.998704] | 0.863493 [0.751159; 0.943591] |
| E2 | 2198 / 1904 | 54 | 100.00% / 100.00% | 0.006655 [0.004333; 0.009163] | 0.997141 [0.995013; 0.998828] | 0.862865 [0.752135; 0.946527] |
| E3 | 2198 / 1904 | 54 | 100.00% / 100.00% | 0.006042 [0.003899; 0.008592] | 0.997625 [0.995759; 0.999010] | 0.909119 [0.833254; 0.965318] |
| E3-I | 2198 / 1904 | 54 | 100.00% / 100.00% | 0.006089 [0.003937; 0.008657] | 0.997607 [0.995748; 0.999006] | 0.908265 [0.830754; 0.964604] |
| E1_C1 | 1088 / 1021 | 35 | 49.50% / 64.81% | 0.009733 [0.004869; 0.015469] | 0.996228 [0.992738; 0.998949] | 0.908245 [0.820850; 0.971719] |
| E2-C_C1 | 2198 / 1904 | 54 | 100.00% / 100.00% | 0.007071 [0.004691; 0.009575] | 0.997020 [0.994910; 0.998740] | 0.864412 [0.752078; 0.944482] |
| E2-fallback | 2198 / 1904 | 54 | 100.00% / 100.00% | 0.006655 [0.004333; 0.009163] | 0.997141 [0.995013; 0.998828] | 0.862865 [0.752135; 0.946527] |
| Hybrid | 2198 / 1904 | 54 | 100.00% / 100.00% | 0.005384 [0.003571; 0.007490] | 0.998152 [0.996565; 0.999356] | 0.909652 [0.820284; 0.973473] |

## Limiar congelado e calibração

Probabilidades não foram recalibradas. Os limiares foram escolhidos exclusivamente em 9. Intercepto/inclinação são diagnósticos, não transformações aplicadas aos escores.

| Estratégia | Limiar de 9 | Sensibilidade e IC95% | Especificidade e IC95% | Probabilidade média / prevalência | Intercepto / inclinação |
|---|---:|---|---|---|---|
| B0 | 0.02480193 | 0.000000 [0.000000; 0.000000] | 1.000000 [1.000000; 1.000000] | 0.024802 / 0.024568 | NA / NA |
| E1 | 0.01809937 | 1.000000 [1.000000; 1.000000] | 0.959164 [0.945945; 0.971029] | 0.029579 / 0.032169 | 0.948 / 1.577 |
| E2-C | 0.01204572 | 1.000000 [1.000000; 1.000000] | 0.956623 [0.947001; 0.965856] | 0.022620 / 0.024568 | 0.546 / 1.306 |
| E2 | 0.01031401 | 1.000000 [1.000000; 1.000000] | 0.954291 [0.944548; 0.963586] | 0.023867 / 0.024568 | 0.294 / 1.274 |
| E3 | 0.01381882 | 1.000000 [1.000000; 1.000000] | 0.960821 [0.951886; 0.969456] | 0.024421 / 0.024568 | 0.224 / 1.235 |
| E3-I | 0.01409615 | 1.000000 [1.000000; 1.000000] | 0.962687 [0.953881; 0.971049] | 0.024446 / 0.024568 | 0.214 / 1.228 |
| E1_C1 | 0.00014500 | 1.000000 [1.000000; 1.000000] | 0.949668 [0.935514; 0.962892] | 0.032028 / 0.032169 | -0.303 / 0.484 |
| E2-C_C1 | 0.01254446 | 1.000000 [1.000000; 1.000000] | 0.957556 [0.948102; 0.966485] | 0.022604 / 0.024568 | 0.565 / 1.318 |
| E2-fallback | 0.01031401 | 1.000000 [1.000000; 1.000000] | 0.954291 [0.944548; 0.963586] | 0.023867 / 0.024568 | 0.294 / 1.274 |
| Hybrid | 0.01473131 | 1.000000 [1.000000; 1.000000] | 0.961287 [0.952578; 0.969643] | 0.024019 / 0.024568 | 0.427 / 1.456 |
Todos os classificadores atenderam os positivos observados em seus respectivos suportes nos limiares congelados. Os ICs empíricos de sensibilidade [1;1] são degenerados porque nenhum falso negativo pode ser criado ao reamostrar apenas acertos observados. Não representam certeza de sensibilidade perfeita na população. B0 apresenta degenerescência análoga em zero. Não introduzimos intervalo alternativo após ver o teste.

## Calibração por faixas previamente definidas

| Modelo | Faixa | Exames / positivos | Probabilidade média | Frequência observada |
|---|---|---:|---:|---:|
| E2-fallback | 0–0.02 | 2093 / 0 | 0.001655 | 0.000000 |
| E2-fallback | 0.02–0.05 | 20 / 0 | 0.029367 | 0.000000 |
| E2-fallback | 0.05–0.1 | 8 / 1 | 0.072925 | 0.125000 |
| E2-fallback | 0.1–0.2 | 7 / 1 | 0.151195 | 0.142857 |
| E2-fallback | 0.2–1 | 70 / 52 | 0.668088 | 0.742857 |
| E3 | 0–0.02 | 2080 / 0 | 0.001603 | 0.000000 |
| E3 | 0.02–0.05 | 31 / 1 | 0.030795 | 0.032258 |
| E3 | 0.05–0.1 | 10 / 1 | 0.073701 | 0.100000 |
| E3 | 0.1–0.2 | 9 / 2 | 0.120140 | 0.222222 |
| E3 | 0.2–1 | 68 / 50 | 0.699569 | 0.735294 |
| Hybrid | 0–0.02 | 2077 / 0 | 0.001880 | 0.000000 |
| Hybrid | 0.02–0.05 | 32 / 0 | 0.027274 | 0.000000 |
| Hybrid | 0.05–0.1 | 14 / 0 | 0.068444 | 0.000000 |
| Hybrid | 0.1–0.2 | 8 / 2 | 0.149068 | 0.250000 |
| Hybrid | 0.2–1 | 67 / 52 | 0.684568 | 0.776119 |
Faixas pequenas limitam a precisão. A proximidade entre probabilidade média e prevalência não garante boa calibração em toda a escala. O baseline constante não tem inclinação identificável.

## Contrastes secundários pareados

Intervalos descritivos sem ajuste para multiplicidade. E1/E2-C, E2-C/E2 e os controles C=1 são avaliados somente nos mesmos exames completos. Os demais usam toda a coorte.

| Contraste | Exames | Δ Brier | IC95% |
|---|---:|---:|---|
| E1 minus E2-C | 1088 | -0.003409 | [-0.006613; -0.000498] |
| E2-C minus E2 | 1088 | 0.000842 | [-0.000126; 0.001830] |
| E1_C1 minus E2-C_C1 | 1088 | 0.000465 | [-0.003872; 0.005073] |
| E3-I minus E3 | 2198 | 0.000047 | [-0.000020; 0.000129] |
| Hybrid minus E2-fallback | 2198 | -0.001271 | [-0.002821; 0.000121] |
E1 versus E2-C ajustados tem intervalo abaixo de zero, mas é contraste secundário com regularizações selecionadas diferentes. O controle com C=1 comum não reproduz evidência inequívoca. Não promover o resultado secundário a confirmação da hipótese primária.

## Completude e população atendida

| Estrato | Exames / pacientes | Positivos / prevalência | Mediana idade abaixo de 90 | Sexo codificado 0 |
|---|---:|---:|---:|---:|
| complete | 1088 / 1021 | 35 / 3.22% | 62 | 567 |
| incomplete | 1110 / 1013 | 19 / 1.71% | 64 | 565 |
Há 130 pacientes com exames em ambos os estratos. Contagens de pacientes dos estratos não se somam como indivíduos distintos. Idades anonimizadas acima de 89 não entram nos resumos etários.

| Estrato | Modelo | Brier | ROC-AUC | AP | Sensibilidade | Especificidade |
|---|---|---:|---:|---:|---:|---:|
| complete | B0 | 0.031189 | 0.500000 | 0.032169 | 0.000000 | 1.000000 |
| complete | E1 | 0.005830 | 0.998616 | 0.953360 | 1.000000 | 0.959164 |
| complete | E2-C | 0.009240 | 0.996554 | 0.886678 | 1.000000 | 0.956315 |
| complete | E2 | 0.008397 | 0.996853 | 0.890852 | 1.000000 | 0.953466 |
| complete | E3 | 0.005856 | 0.998291 | 0.942916 | 1.000000 | 0.968661 |
| complete | E3-I | 0.005881 | 0.998263 | 0.942221 | 1.000000 | 0.969611 |
| complete | E1_C1 | 0.009733 | 0.996228 | 0.908245 | 1.000000 | 0.949668 |
| complete | E2-C_C1 | 0.009268 | 0.996608 | 0.888427 | 1.000000 | 0.958215 |
| complete | E2-fallback | 0.008397 | 0.996853 | 0.890852 | 1.000000 | 0.953466 |
| complete | Hybrid | 0.005830 | 0.998616 | 0.953360 | 1.000000 | 0.951567 |
| incomplete | B0 | 0.016883 | 0.500000 | 0.017117 | 0.000000 | 1.000000 |
| incomplete | E2-C | 0.004907 | 0.997636 | 0.816016 | 1.000000 | 0.956920 |
| incomplete | E2 | 0.004947 | 0.997491 | 0.805021 | 1.000000 | 0.955087 |
| incomplete | E3 | 0.006223 | 0.996430 | 0.844337 | 1.000000 | 0.953254 |
| incomplete | E3-I | 0.006293 | 0.996430 | 0.844337 | 1.000000 | 0.956004 |
| incomplete | E2-C_C1 | 0.004917 | 0.997636 | 0.816016 | 1.000000 | 0.956920 |
| incomplete | E2-fallback | 0.004947 | 0.997491 | 0.805021 | 1.000000 | 0.955087 |
| incomplete | Hybrid | 0.004947 | 0.997491 | 0.805021 | 1.000000 | 0.970669 |
As comparações entre modelos dentro do mesmo estrato têm população comum. Comparar completos com incompletos é comparação entre populações diferentes, sem interpretação causal. Métricas por estrato são descritivas.
Exigir completude excluiu 1.110/2.198 exames (50,50%) e 19/54 positivos (35,19%). Assim, no teste, positivos foram proporcionalmente menos excluídos que a coorte geral. Isso contrasta com 9, onde foram excluídos 60% dos positivos. A regra não produz um efeito universal de exclusão desproporcional de positivos.
Diferenças padronizadas completos menos incompletos, descritivas

| Variável | SMD |
|---|---:|
| age_under90 | -0.0949 |
| sex0 | 0.0243 |
| positive | 0.0972 |
Distribuição de contexto de aquisição, com três aparelhos mais frequentes por estrato

| Estrato | Aparelhos e contagens |
|---|---|
| complete | CS-12 = 330, CS-12   E = 222, AT-6 C 5.5 = 190 |
| incomplete | CS-12 = 373, CS-12   E = 215, AT-6 C 5.5 = 194 |
Todas as frequências de aparelhos, locais e exames por paciente estão em composition.json. Diferenças de composição não identificam causa de missingness nem efeito de equipamento.

## Fold 9 versus fold 10

| Estratégia | Brier 9 → 10 | AUC 9 → 10 | AP 9 → 10 |
|---|---|---|
| B0 | 0.024560 → 0.023964 | 0.500000 → 0.500000 | 0.025195 → 0.024568 |
| E1 | 0.007068 → 0.005830 | 0.995597 → 0.998616 | 0.803640 → 0.953360 |
| E2-C | 0.008484 → 0.007052 | 0.993797 → 0.996994 | 0.828172 → 0.863493 |
| E2-fallback | 0.007983 → 0.006655 | 0.993874 → 0.997141 | 0.821248 → 0.862865 |
| E3 | 0.008256 → 0.006042 | 0.995608 → 0.997625 | 0.778977 → 0.909119 |
| E3-I | 0.008228 → 0.006089 | 0.995472 → 0.997607 | 0.778785 → 0.908265 |
| Hybrid | 0.008094 → 0.005384 | 0.996377 → 0.998152 | 0.822980 → 0.909652 |
Todas as estratégias tiveram Brier numericamente menor em 10. Entre as de cobertura integral, E2-fallback teve o menor Brier em 9 e a híbrida em 10. O contraste primário mudou de +0,000273 para −0,000613, com ambos os ICs incluindo zero. São amostras diferentes. Não foi realizado teste formal de mudança entre folds, e essa diferença não demonstra data drift.

## Rastreabilidade

Fonte exclusiva das métricas — [metrics.json](phase6/final001/metrics.json). [Composição](phase6/final001/composition.json), [recibo da execução](phase6/final001/prediction_receipt.json), [verificação](phase6/final001/verification.json).
No JSON, overall e strata contêm sensibilidade/especificidade nos limiares congelados. Campos aninhados nos objetos paired e primary, além de bootstrap.metrics.sensitivity/specificity, são diagnósticos legados a 0,5. Para os ICs dos limiares de 9, usar bootstrap.binary_frozen_thresholds. Não intercambiar esses campos.
O aviso de depreciação float_precision do pandas foi registrado na leitura/verificação. Não houve erro nem mudança de regras, previsões ou estimativas. O bootstrap foi calculado apenas sobre os escores salvos.
Não executar fase6_predict_once.py novamente. O diretório existente e a trava bloqueiam repetição. scripts/fase6_verify.py verifica escores e hashes sem chamar modelos. scripts/fase6_reports.py apenas renderiza dados existentes.
