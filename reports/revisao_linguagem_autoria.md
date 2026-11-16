# Revisão de linguagem, autoria e apresentação acadêmica

16/11/2026. Revisão documental e editorial; nenhuma nova execução científica. A responsabilidade pelas decisões e pela aprovação do texto permanece com a pesquisadora. Apoio computacional não constitui autoria científica nem parecer humano independente.

## Escopo e evidências

Foram percorridos os 129 arquivos rastreados na base `55b35088b139d91da7d4ae3118addddf5d4a258f`, incluindo código, comentários, configurações, documentos e templates. A busca textual cobriu também os 136 blobs únicos dos três commits alcançáveis no histórico local. Ocorrências foram avaliadas no contexto; palavras como “automático” também descrevem testes e extração de medidas, sem atribuição de autoria. Essa inspeção documental não equivale a revisão científica externa nem garante ausência de todo problema de redação.

Os commits e799a5d, bdc086b e 55b3508 registram MileneCaldeira como autora e committer. Suas mensagens descrevem auditoria, preservação e reconstrução de ambientes; não atribuem autoria científica a uma ferramenta. Não foram alterados autores, datas ou commits anteriores. A identificação MileneCaldeira é a do repositório, não um nome acadêmico completo presumido. A branch é master e o origin é https://github.com/MileneCaldeira/DataMind.git. A consulta somente leitura de master remoto confirmou a base 55b3508; esta revisão não faz push nem altera configurações remotas.

A busca não encontrou atribuição a Claude, autodescrição “como modelo de IA” ou equipe fictícia de agentes. Não foram encontrados candidatos nos padrões de credenciais examinados (tokens GitHub, chaves privadas e chaves AWS); isso não constitui auditoria de segurança abrangente. Dados individuais, modelos, probabilidades e ambientes não integram o commit editorial.

## Problemas e tratamento

|Problema observado|Correção ou decisão|Impacto|
|---|---|---|
|Título duplicado na v3 e menção ao apoio de IA no cabeçalho|Criada v4 com um título e cabeçalho editorial; declaração de uso de IA preservada em seção própria|Apresentação, sem mudança de resultados|
|Autoria inteiramente pendente no cabeçalho|Identificada a pesquisadora responsável pelo nome usado no Git; nome para publicação, afiliação e eventuais coautorias continuam sujeitos à confirmação|Não inventa colaboradores ou credenciais|
|Primeira pessoa plural podia sugerir equipe constituída|Redação impessoal nos trechos interpretativos e de apresentação|Não afirma execução manual nem revisão humana|
|Expressão “negativo/inconclusivo” ambígua|Na v4, resultado primário descrito como inconclusivo|Mantém ausência de suporte à superioridade e de demonstração de equivalência|
|Guia e painel apontavam a versões e estados antigos|Atualizada navegação para v4; distinguido histórico de Git da revisão local|Não altera registros datados|
|Plano mencionava “pesquisadora com orientador” sem vínculo estabelecido|Substituído por apoio de revisor a confirmar; painel também usa perfil a consultar|Não simula orientação existente|
|Parecer novo usava “análise do assistente”|Escopo definido como revisão documental apoiada por ferramentas computacionais|Preserva a ausência de parecer humano externo|
|Referências a ferramenta em relatórios históricos|Preservadas quando registram execução ou a origem das revisões|Evita apagar proveniência|

O propósito não é retirar todas as referências a IA. A declaração do manuscrito informa apoio à revisão, organização, redação e materiais; deve ser confirmada pela pesquisadora e adaptada ao veículo escolhido. O uso de ferramentas não transfere responsabilidade científica nem demonstra que houve conferência humana do conteúdo.

## Preservação e limites de edição

Dos 129 caminhos rastreados, 112 aparecem nos manifestos, snapshots ou registros de transição consultados. Não foram editados para melhorar estilo. Também foram preservados os arquivos de controle de integridade e as evidências de manutenção. Exemplos:

- `reports/fase8_parecer_cientifico.md`: referência ao mesmo assistente explica que não foram três revisores humanos. É proveniência, não atribuição de autoria científica.
- `artigo/manuscrito_v1.md` e `artigo/manuscrito_v2.md`: versões históricas congeladas; a redação atual está na v4.
- `scripts/fase8_revise.py`: template histórico associado à produção da v2, não executado nem reescrito.
- `reports/auditoria_git.md` e `reports/auditoria_master.md`: menções a refs/objetos Codex documentam o estado técnico encontrado.
- Materiais Fase 9: pedidos de parecer e declarações de assistência não significam parecer recebido. Referem-se à v2 histórica; eventual envio deve identificar a versão efetivamente enviada.

A v3 foi preservada byte a byte, SHA-256 `abb382cb059e68a48a4d437d9965b128beebbb59e18a7cd78857498675cc7`. A v4 mantém integralmente sua seção Resultados e sua lista de Referências. Hipóteses, dados, modelos, métricas, números, limiares e contrastes não foram alterados. A comparação de 279 arquivos com o inventário anterior a esta revisão identificou mudanças apenas em README, guia, painel e no responsável hipotético do plano de quatro semanas; os demais arquivos inventariados permaneceram iguais.

## Conteúdo do commit editorial

Arquivos atuais revisados: `README.md`, `GUIA_DO_PROJETO.md`, `STATUS_DATAMIND.md`.

Documentos anteriormente locais incorporados para preservar a trajetória: `artigo/manuscrito_v3.md`, `reports/aprimoramento_pesquisa_2026-11-16.md` e `reports/verificacao_pos_migracao.md`. O último é um registro de manutenção anterior, não execução repetida nesta revisão. O plano recebeu apenas a correção do perfil de apoio mencionada acima.

Novos documentos: `artigo/manuscrito_v4.md`, este relatório, `reports/parecer_cientifico_v3.md`, `reports/matriz_lacunas_v3.md`, `docs/plano_evolucao_cientifica.md` e `docs/guia_estudos_datamind.md`. Os quatro últimos concluem a solicitação anterior de diagnóstico e aprendizagem: não alteram o protocolo nem representam decisões científicas já aprovadas pela pesquisadora.

Total selecionado: 12 arquivos textuais. Os dois registros verification.txt e os dois requirements-venv-*.txt previamente não rastreados ficam fora deste commit. Não foram apagados. Nenhum arquivo ignorado foi forçado ao Git.

## Validações

- `python -B scripts/verify_preservation.py`: PASS; manifestos ativos F5/F6/F7/F8/F9 com 57/31/37/16/9 entradas; F2 com 44 e entradas brutas F3 com 17; sete arquivos de probabilidades salvas correspondem ao consolidado. Quatro diferenças históricas continuam registradas, sem atualização dos hashes congelados.
- `python -B -m unittest discover -s tests -p test_maintenance.py -v`: nove testes passaram. Somente fixtures de preservação, cópia e validação de caminhos; nenhuma execução de modelo. A recusa de backup no mesmo disco exibida pelo teste é o comportamento esperado.
- Comparação textual v3/v4: seção Resultados e Referências idênticas; números do corpo científico mantidos; um único título principal na v4.
- Conferência dos links locais nos documentos selecionados; links externos da revisão científica documentados no parecer, sem afirmar uma nova certificação de todas as referências históricas.
- Inspeção do diff e dos caminhos selecionados, busca de credenciais e `git -c core.whitespace=cr-at-eol diff --cached --check` antes do commit. Não houve normalização dos arquivos congelados.

Nenhum treinamento, previsão, nova métrica, bootstrap, avaliação do fold 10 ou push. A integridade técnica não valida a semântica clínica, a análise estatística ou a originalidade.

## Pendências reais

A pesquisadora precisa confirmar identificação acadêmica, aprovar a redação e poder defender as decisões. Continuam pendentes revisão clínica das medidas e do alvo, revisão bioestatística, avaliação editorial, requisitos institucionais e política de declaração de IA do veículo. O resultado principal continua inconclusivo. Os materiais antigos são mantidos como histórico, não como pareceres externos ou apresentação vigente. O commit permanece local até autorização de envio; backup independente permanece pendente.
