
# Conferência final da versão 1
05/11/2026.

- Verificação scripts/fase7_verify.py passou: hashes dos manifestos anteriores, recibo de execução única, hash de predictions.csv, contagens das partições/estratos, métricas arredondadas do manuscrito e links locais.
- Os números fracionários de resultados do manuscrito foram reconciliados com os JSON, sem recalcular previsões. Contagens e parâmetros conferidos contra preflight/configuração. Informações bibliográficas e editoriais têm fontes específicas; não constituem resultados experimentais.
- Cinco figuras inspecionadas visualmente. Corrigidos sobreposição das caixas do fluxograma, posicionamento de rótulos e espaço da legenda da composição. Sem alteração dos valores.
- Tabela principal e tabela integral correspondem a overall; intervalos de Brier vêm de bootstrap.metrics. Campos binários legados a 0,5 não foram usados como limiares congelados.
- Todas as oito referências do manuscrito têm registros identificados. O quarto trabalho é explicitamente preprint. Suplementos bloqueados não foram apresentados como lidos.
- Conclusões limitadas à anotação CRBBB, sem superioridade, equivalência, benefício clínico, causalidade ou validação externa.
- Revisão humana especializada e informações institucionais permanecem pendentes; isso limita prontidão para submissão, não a entrega da versão 1.
- Manifesto próprio registra entregas novas e scripts; resultados anteriores preservados.

Comando de verificação sem escrita nos artefatos anteriores:
```
.venv-phase7/Scripts/python scripts/fase7_verify.py
```
