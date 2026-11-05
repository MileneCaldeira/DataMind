
# Fase 9 — prontidão e pendências
05/11/2026. Pacote preparado para convite à revisão humana; **não enviado e não pronto para submissão científica**.

## Conteúdo e encaminhamento
|Destinatário|Material principal|Complementos|
|---|---|---|
|Grupo DataMind|Resumo científico, síntese acessível, mensagem e perguntas em fase9_resumo_pesquisa.md|Apresentação de cinco slides em Markdown|
|Clínico de ECG|manuscrito_v2.md + docs/fase9_revisao_clinica.md|Dicionário e auditoria de origem, se solicitados|
|Bioestatístico|manuscrito_v2.md + docs/fase9_revisao_estatistica.md|Fase 6, configuração e código de métricas para inspeção|
|Pesquisador/editor|manuscrito_v2.md + docs/fase9_revisao_editorial.md|Matriz de originalidade e literatura da Fase 8|

Os arquivos são Markdown, conforme solicitado, não PPTX ou PDF diagramado. A síntese acessível está contida no resumo, com extensão para uma página; paginação final depende do editor. Para enviar fora do repositório, manter caminhos relativos ou converter os documentos no formato acordado. Não é necessário encaminhar dados brutos, modelos ou artigos baixados no primeiro contato.

## Obrigatório obter de especialistas
- Parecer clínico sobre QRSd_max/RRi_max, amplitudes e definição da anotação; distinguir limitação de inconsistência invalidante.
- Parecer bioestatístico sobre estimando, bootstrap, precisão, calibração, sensibilidade degenerada e controles de regularização.
- Parecer científico/editorial sobre contribuição frente à literatura e adequação do formato.

Revisão automatizada anterior não substitui esses pareceres. Não preencher a matriz antes de receber comentários.

## Antes de apresentar, a pesquisadora deve conseguir explicar
1. Reconhecemos uma anotação do próprio ECG, sem diagnóstico independente.
2. Exame e paciente são unidades diferentes; partições e bootstrap respeitam pacientes.
3. Brier é erro probabilístico; IC cruzando zero não prova igualdade.
4. E3/E2-fallback muda painel e estratégia; não identifica efeito causal da imputação.
5. E1 avalia população restrita; cobertura/composição fazem parte da interpretação.
6. Híbrida é secundária; sensibilidade de 100% não é certeza populacional; fallback não foi testado em ação.
7. Originalidade e utilidade clínica não foram demonstradas.

Consultar docs/guia_defesa_pesquisa.md para dez perguntas difíceis e respostas.

## O que falta para submissão
Revisores humanos e resolução dos comentários prioritários; acordo de autoria/CRediT e afiliações; avaliação institucional de ética/dispensa; financiamento, conflitos e declaração de IA; licença do código e plano de depósito público; escolha do veículo e reconfirmação de suas regras; versão futura aprovada pelos autores e adaptada ao formato. Nenhuma aprovação ou isenção foi presumida.

Validação externa seria necessária para alegações de generalização, mas não foi definida como condição automática para comunicar honestamente este estudo de caso. Qualquer novo experimento precisa de pergunta e autorização próprias.

## Registro de integridade e decisões
Verificação documental por scripts/fase9_verify.py: manifestos anteriores, correspondência dos valores selecionados com metrics.json, resumo até 250 palavras, cinco slides e ausência de linhas fictícias na matriz. Não executa modelos, métricas, bootstrap ou ajustes. Resultado em reports/phase9/verification.json.

V2, resultados e materiais anteriores permanecem intactos. Esta nota acrescenta decisões ao histórico sem reescrever registros congelados. Não iniciadas Fase 10, comunicação com terceiros ou submissão. Próxima ação humana: escolher colaboradores e enviar o convite após conferir assinatura e anexos.
