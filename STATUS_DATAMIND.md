# Estado do DataMind

Atualizado em 05/11/2026 — auditoria master. Estados técnicos não representam validação clínica.

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
|Reprodução completa nova|NÃO VERIFICADO|Sem retreino, predição, reextração ECGDeli ou instalação limpa nesta auditoria|
|Manuscrito v2|CONCLUÍDO — rascunho|Preparado para revisão externa, preservado nesta manutenção|
|Revisão externa humana|PENDENTE|Cardiologista, bioestatístico e pesquisador/editor; pacote Fase 9 pronto, sem pareceres reais registrados|
|Git local|VALIDADO INTERNAMENTE — escopo selecionado|Consultar reports/auditoria_git.md para lista, estado do commit e limites; não é cópia integral|
|Backup independente|PENDENTE|Pesquisadora deve indicar destino autorizado em dispositivo independente; plano em reports/plano_backup.md|
|Uso clínico|BLOQUEADO|Não demonstrados segurança, utilidade, generalização ou validação clínica|
|Submissão|PENDENTE|Revisão humana, contribuição editorial, autoria, ética institucional, financiamento, conflitos e licença|
|Nova fase experimental|BLOQUEADO nesta tarefa|Não autorizada; fold 10 já consumido|

## Riscos principais

Poucos positivos (54 exames/45 pacientes); dependência de construto entre medidas e anotação; ambiguidade de medidas globais; regularização/seleção; IC degenerado de sensibilidade; calibração limitada; único recurso histórico; ausência de backup independente confirmado.

## Próximas três ações

1. Pesquisadora + apoio de TI: escolher destino externo privado e validar backup.
2. Cardiologista + bioestatístico: resolver questões dos roteiros da Fase 9.
3. Pesquisadora + orientador/editor: decidir formato após pareceres, completar condições institucionais e de autoria.

[Entenda a IA](docs/ENTENDA_A_IA.md) · [Guia](GUIA_DO_PROJETO.md) · [Auditoria](reports/auditoria_master.md) · [Manuscrito](artigo/manuscrito_v2.md).

Não há nova aprovação científica, envio a terceiros ou publicação decorrente desta auditoria.
