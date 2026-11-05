# Experimentos — situação atual e registro histórico

Atualização de manutenção em 05/11/2026. O experimento ECG das Fases 5–6 foi executado; o fold 10 já recebeu sua avaliação final única. Não executar novamente para escolher modelos.

- fase4.json preserva o protocolo candidato e seu estado anterior à autorização.
- fase5.json preserva a configuração piloto efetiva: regressão logística, grade C, semente, partições e diretório de saída.
- Modelos/configuração/limiares congelados: ../reports/phase5/run001/.
- Probabilidades e resultados finais: ../reports/phase6/final001/.
- Próxima ação científica: revisão humana, não novos experimentos. Ver ../STATUS_DATAMIND.md.

As alternativas abaixo são propostas históricas; não foram transformadas em novos modelos. Heart foi investigado descritivamente, diabetes/Adult ficaram como alternativas, ACS não foi baixado. O foco migrou para cobertura ECG.

**Rastreabilidade:** o conteúdo original abaixo foi mantido. A atualização deste README altera seu hash em relação ao snapshot pré-treino before_hashes.json, por autorização de manutenção. Nenhum manifesto foi reescrito. O antigo fase5_verify.py compara esse snapshot e passaria a sinalizar este README; não executá-lo nem alterar sua exceção silenciosamente. O freeze ativo e os artefatos experimentais permanecem intactos. Ver ../reports/auditoria_master.md.

## Experimentos futuros — não executados (texto histórico)

Antes de qualquer modelo: definir pergunta, população, estimando, regras semânticas, hipótese e métrica de sucesso; registrar versão dos dados e plano de análise.

1. Piloto Heart: matriz centro × variável, validação de sentinelas com documentação, comparação descritiva de políticas de inclusão. Preservar versão sem recodificação e versão com regras justificadas. Não chamar registros com todos os campos de amostra representativa.
2. Se houver contribuição metodológica plausível, selecionar segunda base independente e verificar acesso/licença antes de ampliar o escopo. Um único benchmark antigo não basta para conclusões gerais em saúde.
3. Diabetes: reconstruir linhagem e definição de alvo; comparar apenas depois de recuperar dicionário, pesos e regras de seleção. Não remover perfis repetidos como se fossem pessoas duplicadas.
4. Adult/ACS: distinguir sobreposição de atributos de repetição de indivíduos; definir unidade de particionamento e grupos mínimos. Não inferir discriminação causal de diferenças de frequência.
5. Modelagem, somente em etapa posterior: pré-processamento ajustado dentro de cada partição de treino, avaliação preservada, desenho de validação compatível com centros/tempo/unidade e incerteza explícita. A auditoria já examinou o teste histórico Adult; isso deve ser declarado e esse arquivo não deve ser apresentado como um novo teste cego.

Cada execução futura deve ter pasta própria com protocolo, comando, ambiente, hashes, semente quando aplicável, saídas e interpretação que diferencie observações e hipóteses.
