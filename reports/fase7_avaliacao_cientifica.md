
# Fase 7 — avaliação científica
05/11/2026. Fontes: resultados congelados das Fases 5–6; revisão direcionada em docs/fase7_revisao_literatura.md.

1. **Contribuição demonstrada:** estudo de caso reproduzível mostrando cobertura, seleção e comparação operacional pareada para anotação CRBBB. Não é novo algoritmo nem nova teoria de ausência.
2. **Além dos benchmarks:** explicitação dos denominadores e da população excluída, controles e contraste probabilístico pré-congelado. O interesse editorial depende dessa transparência, não de recorde de AUC.
3. **Populações:** E3/E2-fallback usam os mesmos 2.198 exames. E1 só atende 1.088; seu Brier isolado não é comparável diretamente ao de modelos integrais. Controles em suporte comum ajudam, sem identificação causal.
4. **Seleção:** completos têm 35/1.088 positivos; incompletos, 19/1.110. É seleção de composição observada, não demonstração de mecanismo MNAR ou viés causal quantificado.
5. **Folds:** ordenação E2-fallback/E3 se inverte, mas ambos os IC primários incluem zero. Nenhuma análise formal de drift foi feita; não atribuir mudança a drift.
6. **Positivos:** 54 exames de 45 pacientes não sustentam inferências clínicas robustas, calibração detalhada ou estratificações extensas. Não usar poder pós-hoc para reinterpretar resultado negativo.
7. **AUC e sensibilidade:** AUC alta é plausível quando características e anotação vêm do mesmo ECG. Sensibilidade observada 100% é amostral. Bootstrap [1;1] resulta de reamostrar somente positivos corretamente classificados; não mede certeza de perfeição. Esclarecimento metodológico pós-hoc, sem novo teste ou alteração primária.
8. **Validação externa:** inexistente. PTB-XL+ não é base independente do PTB-XL. Não há evidência de transporte a serviços/equipamentos contemporâneos.
9. **Alvo:** presença de anotação, sem diagnóstico adjudicado independente. Negativo não significa doença clinicamente excluída.
10. **Publicação:** comunicação metodológica incremental é defensável; artigo curto é possível após revisão humana rigorosa. Não demonstrada originalidade suficiente para alegação de inovação ampla.

## Resultado primário e secundários
ΔBrier E3 − E2-fallback = −0,000613; IC95% [−0,002380; +0,001133]. Sem suporte à superioridade; sem teste de equivalência. Híbrida tem menor Brier pontual integral (0,005384), secundário; seu contraste também inclui zero. A ausência de significância não apaga o resultado descritivo de cobertura.

## Integridade
O renderizador da Fase 7 verifica 57 hashes da Fase 5 e 31 da Fase 6, sem executar código de predição. Mantidos todos os manifestos anteriores. A verificação original da Fase 6 permanece a evidência de joins, separação por paciente, probabilidades e execução única. Não foram reexecutados testes que escrevem nos diretórios congelados. Registro atual: reports/phase7/verification.json.

Uma cautela computacional foi preservada: campos legados de sensibilidade em primary e bootstrap.metrics usam 0,5; a tabela usa overall e, para intervalos binários, a fonte correta é binary_frozen_thresholds. Nenhuma correção retroativa dos artefatos foi realizada.

## Decisão
Revisar o manuscrito antes de ampliar o estudo. Uma revisão clínica das medidas e do alvo e uma segunda leitura bibliográfica agregam mais valor imediato que treinar novos modelos. Validação externa só deve ser planejada se a próxima pergunta exigir generalização e houver compatibilidade de medidas/anotações. Não é requisito para relatar honestamente este estudo de caso, mas é indispensável para alegações de transporte.
