# Estado do DataMind

Atualizado em 16/11/2026 — aprimoramento editorial. Estado técnico apoiado no saneamento e na verificação pós-migração de 05/11/2026. Plano de revisão em reports/aprimoramento_pesquisa_2026-11-16.md.

|Área|Estado|Situação / responsável ou perfil necessário|
|---|---|---|
|Pesquisa atual|CONCLUÍDO — ciclo experimental|Disponibilidade de medidas ECG, cobertura e classificação da anotação CRBBB|
|Objetivo/hipótese|CONCLUÍDO — avaliação|E3 versus E2-fallback no mesmo suporte; superioridade não sustentada, equivalência não demonstrada|
|Dados|VALIDADO INTERNAMENTE|PTB-XL 1.0.3 / PTB-XL+ 1.0.1; hashes, 21.799 IDs e join 1:1; pacientes separados|
|Semântica clínica|PENDENTE|Cardiologista e especialista ECGDeli: QRSd_max/RRi_max, unidades/agregação e alvo|
|Modelos|VALIDADO INTERNAMENTE|Sete regressões logísticas salvas, B0 e combinações fallback/híbrida; inspecionados sem previsão|
|Resultado primário|CONCLUÍDO|2.198 exames; Δ Brier −0,000613, IC95% [−0,002380; +0,001133]|
|Cobertura|CONCLUÍDO|531 completas: 49,50% dos exames / 64,81% dos positivos; fallback não acionado|
|Integridade ativa|VALIDADO INTERNAMENTE|Manifestos Fases 5–9 e entradas conferidos; probabilidades individuais correspondem ao consolidado|
|Reconstrução dos ambientes|CONCLUÍDO|Duas venvs temporárias; locks exatos, pip check/importações e leitura de sete modelos passaram; originais preservados|
|Reprodução completa nova|NÃO VERIFICADO|Não executados retreino, predição, reextração ECGDeli ou novas métricas|
|Snapshots e verificador seguro|CONCLUÍDO|Novo verificador somente leitura; quatro diferenças históricas explícitas, duas versões antigas recuperadas; nove testes de manutenção passaram|
|Manuscrito v4|CONCLUÍDO — rascunho editorial|Pergunta explícita, dicionário das medidas e limites de seleção detalhados; revisão humana PENDENTE|
|Revisão externa humana|PENDENTE|Cardiologista, bioestatístico e pesquisador/editor; pacote Fase 9 pronto, sem pareceres reais registrados|
|Git local|VALIDADO INTERNAMENTE — ampliado|Todo código próprio, testes, configurações, protocolos, manuscritos e documentos científicos principais; dados/modelos ficam no backup; primeiro commit preservado|
|Backup independente|PENDENTE|Só disco físico 0/C: acessível; conectar e autorizar diretório privado em outro disco. Ferramenta de cópia/restauração testada apenas com fixtures|
|Uso clínico|BLOQUEADO|Não demonstrados segurança, utilidade, generalização ou validação clínica|
|Submissão|PENDENTE|Revisão humana, contribuição editorial, autoria, ética institucional, financiamento, conflitos e licença|
|Nova fase experimental|BLOQUEADO nesta tarefa|Não autorizada; fold 10 já consumido|

## Riscos principais

Poucos positivos (54 exames/45 pacientes); dependência de construto entre medidas e anotação; ambiguidade de medidas globais; regularização/seleção; IC degenerado de sensibilidade; calibração limitada; único recurso histórico; ausência de backup independente confirmado.

## Próximas três ações

1. Pesquisadora + apoio de TI: escolher destino externo privado e validar backup.
2. Cardiologista + bioestatístico: resolver questões dos roteiros da Fase 9.
3. Pesquisadora + pesquisador/editor a consultar: decidir formato após pareceres, completar condições institucionais e de autoria.

[Entenda a IA](docs/ENTENDA_A_IA.md) · [Guia](GUIA_DO_PROJETO.md) · [Auditoria](reports/auditoria_master.md) · [Manuscrito](artigo/manuscrito_v4.md).

Não há nova aprovação científica, envio a terceiros ou publicação decorrente desta auditoria.
