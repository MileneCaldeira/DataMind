# Recomendações de organização — sem execução

05/11/2026. Escopo: inspeção e criação de três documentos. Não houve exclusão, mudança de nomes/caminhos, alteração de dados/modelos/resultados, instalação, publicação ou execução experimental.

## Prioridades

|Prioridade e evidência|Melhoria futura sugerida|Impacto e benefício|Risco e cuidado|
|---|---|---|---|
|Alta — README termina na Fase 2 e afirma não haver modelos|Atualizar futuramente a porta de entrada para apontar ao guia e distinguir instruções históricas das atuais|Evita execução inadequada e confusão sobre o estágio do estudo|Reescrita pode apagar contexto; manter história e não alterar protocolos congelados|
|Alta — git ls-files vazio e master sem commits|Planejar primeiro versionamento com seleção explícita de código/documentos e política de dados|Histórico revisável, colaboração e recuperação|Não usar git add indiscriminadamente; revisar saúde, licenças, fontes bibliográficas e artefatos sensíveis|
|Alta — projeto dentro de OneDrive|Estabelecer backup privado independente, datado, com teste de restauração e conferência de hashes|Protege contra exclusões sincronizadas, conflitos e perda local|Sincronização não é backup; disponibilidade local e status real do OneDrive não foram confirmados|
|Alta — scripts de verificação e materiais também escrevem|Documentar comandos por efeito: leitura, escrita, download, treino e predição|Reduz risco de sobrescrever evidências ou repetir teste final|Não alterar agora scripts congelados; qualquer nova interface precisa de revisão própria|
|Alta — dados de saúde e cópias bibliográficas locais|Revisar distribuição arquivo a arquivo antes de qualquer GitHub/depósito|Permite reprodução compatível com licenças e privacidade|Licença pública não autoriza automaticamente qualquer redistribuição ou dispensa institucional|
|Média — ambientes representam 460 MB e 15.770 arquivos|Testar futuramente reconstrução em local separado e considerar ambientes fora da sincronização|Menos arquivos sincronizados e backups mais simples|Caminhos absolutos, versões e serialização podem impedir reprodução; não mover ambientes atuais|
|Média — locks existentes sem demonstração de reconstrução offline|Documentar procedimento de reconstrução e, se autorizado, preparar acervo de pacotes verificados|Melhora recuperação quando versões deixam de estar disponíveis|Instalação/atualização pode alterar resultados; nunca substituir ambiente experimental sem comparação e registro|
|Média — nomes genéricos model.npy e code_tail.bin|Usar índice de proveniência com descrição explícita; o mapa já fornece essa tradução|Evita confundir escores externos com modelo DataMind e download parcial com corrupção|Renomear quebraria scripts/hashes; preferir documentação|
|Média — experiments/README ainda “futuros — não executados”|Adicionar futuramente aviso de escopo histórico e apontar para configurações executadas|Distingue propostas abandonadas do experimento ECG|Não reescrever decisões anteriores como se já fossem conhecidas|
|Média — resultados e documentação por fase se parecem|Manter índice do documento vigente, com referências aos históricos|Reduz redundância de leitura sem eliminar rastreabilidade|Não fundir nem excluir relatórios, manuscritos v1/v2 ou baseline sem análise de dependências|
|Baixa — onze .pyc locais derivados dos .py|Considerar limpeza de caches somente em manutenção autorizada|Pequena redução de ruído; regeneráveis|Não confundir __pycache__ com locks, logs de auditoria ou probabilidades|
|Baixa — maiores dados em 62,2 MB e 13,5 MB|Avaliar armazenamento privado separado apenas se o projeto crescer|Pode simplificar repositório de código|Hoje não é necessário migrar; links externos podem quebrar reprodução offline|

## Redundância aparente não é descarte

- reports/baseline e relatórios iniciais têm função de referência histórica; nomes semelhantes não demonstram duplicação dispensável.
- Relatórios de treinamento, validação, interpretação e decisão respondem a perguntas diferentes. O guia dá uma ordem de leitura sem fundi-los.
- oof_fixed.csv e oof_selected.csv não são cópias intercambiáveis: representam controles/seleções diferentes.
- Gráficos PNG, SVG e PDF são formatos alternativos da mesma figura, úteis para leitura e publicação. Não são automaticamente desperdício.
- Manuscritos v1 e v2 documentam revisão; devem continuar preservados.
- Freeze da Fase 5 registra estado anterior à autorização final. Seu status histórico não deve ser “corrigido” para refletir a Fase 6.
- PREDICTION_STARTED.lock e prediction_receipt.json protegem/documentam execução única; não são temporários.
- Fontes baixadas e logs de tentativas malsucedidas sustentam a auditoria, mesmo quando a alternativa científica foi abandonada.

Não foi demonstrado conjunto de arquivos científicos obsoletos seguro para exclusão.

## Dependências e reconstrução

Há locks para treino e renderização e registros de ambiente. Não foi identificada, pela inspeção, uma biblioteca obrigatória específica comprovadamente ausente desses registros. A fragilidade é operacional: não há demonstração nesta auditoria de reconstrução limpa/offline nem portabilidade dos ambientes Windows.

O README geral descreve somente biblioteca padrão, o que está desatualizado para as fases recentes. Modelos joblib dependem das versões e das classes em src/datamind; guardar só modelos e CSV não é suficiente. A documentação deve distinguir reconstruir ambiente, regenerar figuras e repetir experimento — são ações diferentes e não autorizadas por esta tarefa.

A raiz ignora .venv-phase5 explicitamente, e phase7 tem exclusão interna criada pelo venv. A verificação confirmou que phase7 está ignorado. Não se recomenda mudar .gitignore por uma falha presumida. Estar ignorado tampouco torna um arquivo descartável.

## O que não publicar automaticamente

|Grupo|Motivo para revisão antes de distribuição|
|---|---|
|data/raw e amostras derivadas|Licenças e atribuições variam; diabetes tem questão de licença registrada nas fases iniciais|
|Metadados de saúde e probabilidades por exame/paciente|Pseudonimização não elimina necessidade de governança e avaliação da redistribuição|
|OOF, validation.csv e predictions.csv|Podem vincular identificadores a rótulos/probabilidades; preferir resultados agregados no primeiro contato|
|Artigos XML, suplementos ZIP e cópias locais|Direitos bibliográficos não são definidos pela licença dos datasets|
|Ambientes virtuais|Volumosos, específicos de plataforma e com componentes de terceiros|
|.git, logs e environment.json|Podem revelar caminhos locais, histórico ou metadados; revisão prévia, sem afirmar presença de segredos|
|Código e modelos|Falta resolver licença geral e condições de depósito; licenças de dados não licenciam automaticamente o software|

Para revisão externa inicial, encaminhar apenas manuscrito, resumo, figuras pertinentes e roteiros por especialidade após decisão humana. Esta auditoria não encaminhou nenhum arquivo.

## Ordem recomendada de manutenção futura

1. Consolidar backup privado e testar restauração.
2. Atualizar a entrada documental e planejar versionamento com revisão de conteúdo.
3. Validar reconstrução dos ambientes em cópia separada, sem repetir teste final.
4. Somente então avaliar simplificações de armazenamento e eventual depósito autorizado.

Todas são propostas. Nesta tarefa foram criados somente GUIA_DO_PROJETO.md, reports/mapa_repositorio.md e este documento. Os manifestos anteriores continuam sendo a referência de integridade; não foram atualizados para incluir esta documentação.
