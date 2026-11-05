# Saneamento técnico — resultado consolidado

05/11/2026. Escopo técnico, sem nova fase científica. Nenhum treinamento, previsão, avaliação do fold 10, ajuste de calibração ou alteração de resultado. O primeiro commit e799a5d permanece raiz do histórico.

## O que foi efetivamente resolvido

|Problema original|Causa|Correção executada|Evidência / estado|
|---|---|---|---|
|Git parcial: 39 textos|Documentação científica/configurações ainda não adicionadas|Commit bdc086b, com 86 caminhos alterados; protocolo, decisões, relatórios, manuscritos, tabelas agregadas, locks e manifestos agora rastreados|CONCLUÍDO para código/documentação escolhidos; 32 Python próprios rastreados; sem remoto|
|Risco de inclusão acidental|Ignore não abrangia modelos, probabilidades, fontes e saídas JSON|.gitignore ampliado; saídas JSON ainda não revisadas ficam locais; arquivos já auditados/rastreados permanecem no Git|CONCLUÍDO; checagem de ignores e staged, nenhuma exclusão|
|Finais de linha poderiam mudar hashes|core.autocrlf=true no ambiente|.gitattributes com * -text, sem normalizar arquivo algum|CONCLUÍDO; blobs Git comparados aos bytes locais|
|Snapshot histórico rejeita README atualizado|before_hashes registra instante pré-treino, não documentação atual|Registro separado e verificador novo com transições exatas, sem exceções por substring|CONCLUÍDO; 111 entradas iguais e quatro diferenças documentadas; hashes ativos PASS|
|Versões históricas em risco|Objetos internos Git não são histórico convencional suficiente|Dois textos antigos recuperados dos blobs e preservados em JSON, com SHA-256 original|CONCLUÍDO para dois textos; bytes antigos de outros dois arquivos não recuperados|
|Ambientes nunca reconstruídos|Somente locks e venvs locais existentes|Duas venvs novas fora do OneDrive, instalação por PyPI público, versões exatas|CONCLUÍDO no mesmo Windows/Python; pip check, imports e sete modelos legíveis sem inferência|
|Testes antigos não seguros para consulta|Suíte inclui fit/predict e verificadores escrevem|Nova suíte independente test_maintenance.py; verificador somente leitura|CONCLUÍDO; nove testes passaram|
|Backup apenas descritivo|Sem ferramenta nem destino independente confirmado|backup_project.py implementado e testado com fixtures; detecta mesmo disco, copia, confere e restaura|PARCIAL: ferramenta validada nos testes; backup real PENDENTE|

## Arquivos e commits

**bdc086bc86264a1559f772c50e8ca4b6e57c4a1f** — “Preserve research documentation and add non-predictive integrity and backup tools”. Inclui:
- .gitattributes/.gitignore;
- scripts/verify_preservation.py, backup_project.py e inspect_environment.py;
- tests/test_maintenance.py;
- experiments/integrity_maintenance.json;
- reports/saneamento_evidencias.json;
- documentos científicos existentes, protocolos, manuscritos v1/v2, apresentação, tabelas agregadas, locks, configurações e manifestos selecionados.

Lista exata e recuperável: git diff-tree --no-commit-id --name-status -r bdc086b. Nenhum manuscrito ou artefato científico foi editado: foram acrescentados ao Git como estavam.

O commit documental de encerramento contém exatamente:
1. .gitignore (proteção conservadora de JSON ainda não revisado);
2. README.md;
3. STATUS_DATAMIND.md;
4. GUIA_DO_PROJETO.md;
5. reports/auditoria_git.md;
6. reports/plano_backup.md;
7. reports/saneamento_tecnico_final.md;
8. reports/phase7/fontes_verificadas.md;
9. reports/phase7/revisao_final.md;
10. reports/phase8/revisao_log.md;
11. reports/phase6/final001/PREDICTION_STARTED.lock.

Os quatro últimos são registros existentes inalterados. Seu conteúdo não é dado individual. O identificador do commit de encerramento está no histórico Git; não se insere o hash do próprio commit no arquivo, evitando autorreferência/emenda.

**Fora do Git por decisão:** dados/amostras, ambientes, modelos com IDs de treino, probabilidades/OOF por exame, caches, artigos/suplementos baixados, imagens binárias, logs com informações de máquina e saídas não revisadas. Não houve git add -A, -f, push, configuração de remoto ou reescrita.

O código de terceiros arquivado em reports/phase7/sources não é código próprio essencial do pipeline; permanece local por proveniência/licença. O versionamento protege o código e a documentação necessária ao entendimento/reprodução, mas a reprodução exige também os insumos fora do Git e suas licenças. Clone isolado não equivale a backup integral.

## Snapshots: cronologia sem reescrever evidências

1. **before_hashes.json:** capturado pelo treinador antes dos fits. Contém 115 entradas.
2. Entre esse snapshot e o freeze final, mudaram docs/decisoes.md, docs/fase5_auditoria_leakage.md e tests/test_phase5.py. Os bytes finais estão congelados. Os registros permitem estabelecer esse intervalo, **não o instante exato de cada edição em relação a cada ajuste**. Não inventamos cronologia mais precisa.
3. **freeze.json:** referência final do piloto com 57 entradas, anterior à avaliação final. Manifestos Fases 6–9 registram entregas posteriores.
4. **Auditoria master:** atualizou experiments/README.md por autorização explícita, depois do treino/congelamento. Seu hash pré-treino não deveria passar como se fosse documentação atual.
5. **Saneamento:** nenhum manifesto anterior alterado. Novo registro distingue essas camadas e rejeita qualquer diferença não cadastrada ou hash atual inesperado.

O verificador antigo fase5_verify.py contém exclusões por fase5/phase5 e decisões, mas não por experiments/README. Continuaria rejeitando o README e também tem capacidade de prever/treinar testes. Não foi modificado nem executado.

**Recuperação byte a byte:** docs/decisoes.md pré-treino e experiments/README.md pré-treino foram encontrados em objetos Git existentes, conferidos com os hashes do snapshot e incorporados como recovered_utf8 em experiments/integrity_maintenance.json. Isso torna a evidência independente da permanência dos objetos internos. Os outros dois textos anteriores não foram encontrados: seus hashes permanecem registrados, e seus estados finais são íntegros. Não presumir recuperação completa da evolução histórica.

Novo comando:

```powershell
python -B scripts/verify_preservation.py
```

Usa somente biblioteca padrão; não importa modelos, não grava e não calcula métricas. Confere oito hashes âncora dos manifestos/snapshot, seus conteúdos ativos, 44 entradas Fase 2, 17 entradas Fase 3, as quatro transições históricas e sete tabelas individuais já salvas contra o consolidado. Mostra separadamente PASS ativo e DOCUMENTED_DIFFERENCES_NOT_IDENTICAL_TO_PRETRAIN; não mascara diferenças com PASS histórico absoluto. Documentação corrente é versionada pelo Git, não promovida a novo congelamento científico.

## Reconstrução realmente executada

Diretório temporário privado local fora do OneDrive, basename **datamind-rebuild-2reye_o_**, sob a pasta temporária do usuário no disco C:. Não é backup; não alterou .venv-phase5 ou .venv-phase7. Python base **3.13.7, Windows x64**. A mensagem do venv sobre ADMINI~1 versus Administrador é resolução do caminho curto do Windows, não troca de disco.

Foram criados dois ambientes vazios e usados:
- pip --isolated install --disable-pip-version-check --no-cache-dir --only-binary=:all: --index-url https://pypi.org/simple -r LOCK;
- pip --isolated check;
- pip --isolated freeze;
- scripts/inspect_environment.py --kind phase5 ou phase7, com python -B;
- nove testes de manutenção e o verificador de preservação na venv temporária phase5.

|Controle|phase5|phase7|
|---|---|---|
|Instalação de wheels públicas|Exit 0|Exit 0|
|Versões do pip freeze iguais ao lock|11/11, sem extras no freeze|11/11, sem extras no freeze|
|pip check|No broken requirements found|No broken requirements found|
|Imports relevantes|PASS|PASS, incluindo backend Agg|
|Modelos|Sete joblib carregados após conferir freeze; sem fit/transform/predict|Não aplicável|
|Renderização/treino/previsão|Não executados|Não executados|

Dependências diretas do experimento incluem numpy, pandas, scipy, scikit-learn, joblib, psutil e threadpoolctl; renderização usa matplotlib e dependências de gráficos. Os locks completos foram preservados, incluindo dependências auxiliares/transitivas; nenhuma versão foi removida por parecer desnecessária. pip check valida metadados de dependências, não a segurança de toda a cadeia de fornecedores.

Modelo E3-I mantém coeficientes 1×1.062; painéis reduzidos 1×8; completos 1×531. C, estrutura e carregamento são legíveis no novo ambiente. Não foram geradas probabilidades para provar equivalência de inferência. Repetição integral, determinismo numérico de novo treino, portabilidade Linux, reextração ECGDeli/MATLAB e instalação offline continuam **NÃO RETESTADOS**. O ambiente base Windows/Python não foi reconstruído do zero.

Evidência persistente: reports/saneamento_evidencias.json contém versões, resultados de inspeção, saídas completas de instalação/check/freeze/testes/verificação e SHA-256 dos logs. O texto embutido de cada log reconstitui seu hash. Logs originais também permaneceram na área temporária. Nenhum dado de paciente foi enviado ao PyPI; apenas pacotes públicos foram baixados. Nenhuma instalação global ou cobrança.

### Repetir somente a reconstrução técnica

Da raiz, criar um novo destino temporário, nunca reutilizar as venvs originais:

```powershell
$envDataMind = Join-Path $env:TEMP ('datamind-check-' + [guid]::NewGuid().ToString('N'))
python -m venv (Join-Path $envDataMind 'phase5')
python -m venv (Join-Path $envDataMind 'phase7')
$pythonPiloto = Join-Path $envDataMind 'phase5/Scripts/python.exe'
$pythonFiguras = Join-Path $envDataMind 'phase7/Scripts/python.exe'
& $pythonPiloto -m pip --isolated install --disable-pip-version-check --no-cache-dir --only-binary=:all: --index-url https://pypi.org/simple -r reports/phase5/run001/requirements.lock.txt
if ($LASTEXITCODE -ne 0) { throw 'Falha de instalação phase5' }
& $pythonFiguras -m pip --isolated install --disable-pip-version-check --no-cache-dir --only-binary=:all: --index-url https://pypi.org/simple -r reports/phase7/requirements-render.lock
if ($LASTEXITCODE -ne 0) { throw 'Falha de instalação phase7' }
& $pythonPiloto -m pip --isolated check
& $pythonFiguras -m pip --isolated check
& $pythonPiloto -B scripts/inspect_environment.py --kind phase5
& $pythonFiguras -B scripts/inspect_environment.py --kind phase7
& $pythonPiloto -B -m unittest discover -s tests -p test_maintenance.py -v
& $pythonPiloto -B scripts/verify_preservation.py
```

Conferir o exit code de cada etapa; falha não autoriza mudar versões. Não substituir os comandos por descoberta de toda a suíte antiga.

## Testes e segurança

Nove testes com arquivos fictícios:
- detecção de hash adulterado;
- aceitação somente de transição histórica exata;
- rejeição de transição não registrada;
- rejeição de texto histórico recuperado adulterado;
- rejeição de caminho fora da raiz;
- cópia, verificação e restauração em snapshots distintos;
- detecção de adulteração da cópia;
- recusa de destino dentro da origem e do mesmo disco físico (teste mock da CLI);
- exclusão somente das duas venvs no modo essencial.

Há nove métodos, alguns cobrindo mais de um cenário. Nenhum carrega modelo experimental ou chama fit/predict. Os testes de cópia não demonstram funcionamento num disco externo real; esse ensaio depende do destino.

Segredos: diff completo, blobs e nomes staged examinados; padrões de chaves privadas/tokens e caminhos pessoais não encontrados na seleção. Isso é triagem, não garantia universal. Materiais de terceiros/saídas individuais ficaram fora. .gitattributes preserva bytes, incluindo CRLF. Dezessete avisos de whitespace eram quebras Markdown intencionais em documentos congelados; nenhuma alteração foi feita para silenciá-los.

Não houve refatoração do pipeline científico. Funções novas são separadas; mudanças comportamentais em treinamento/avaliação continuam proibidas. A ferramenta de backup grava somente no destino explicitamente fornecido, não na origem. O verificador de integridade não grava em lugar algum. Inspect_environment limita eventual cache Matplotlib a diretório temporário.

## Backup: ferramenta pronta, cópia real pendente

Get-Disk/Get-Partition/Get-Volume mostraram somente **disco 0, NVMe ~1 TB, C:** e partições de sistema. Não há disco externo disponível nem destino autorizado. Não foi criada cópia grande em C: ou em outro serviço.

backup_project.py implementa snapshot único, proteção contra mesmo disco, inventário SHA-256 antes/depois, conferência de origem estável, cópia sem sobrescrita e restauração de freeze.json, E3.joblib (bytes, sem desserialização), predictions.csv e manuscrito_v2.md. Registro receipt.json contém destino/data/contagem/bytes/hashes. Falhas interrompem e não apagam evidências.

**Precisa da pesquisadora:** conectar dispositivo privado fisicamente independente e autorizar um diretório existente nele. Exemplo apenas após confirmação: E:/BackupPrivadoDataMind, mínimo recomendado 2 GiB livres para a primeira cópia com folga. Não considerar a unidade E: autorizada só por aparecer neste exemplo.

Integral preserva tudo, incluindo .git e ambientes (~556 MiB, sujeito ao crescimento). Essencial omite só as duas venvs (~117 MiB no inventário anterior). Reconstrução online comprovada permite considerar essencial, mas primeira cópia integral continua preferível: ausência futura de pacotes e restauração de ambiente não foram testadas offline. Detalhes em plano_backup.md.

## Validação final e pendências

Manifestos ativos: 57/31/37/16/9 entradas, todos conferidos; 44 Fase 2 e 17 Fase 3. Sete scores individuais correspondem ao CSV final. As diferenças frente ao snapshot do início desta tarefa ficam restritas à manutenção autorizada; fontes científicas e resultados não mudaram. Históricos e logs preditivos continuam iguais.

**Corrigido / CONCLUÍDO:** código/documentação versionados; proteção de finais de linha e ignorados; verificador em camadas; duas versões históricas preservadas; reconstrução online dos ambientes; compatibilidade de leitura dos modelos; nove testes seguros; procedimento de backup executável.

**Pendente de autorização / PENDENTE:** destino externo privado para realizar e verificar backup real. Publicação GitHub não autorizada e não realizada.

**Pendente de especialista / PENDENTE:** medidas RRi_max/QRSd_max e alvo, precisão/inferência, autoria/licenças e revisão editorial. Nenhuma dessas questões foi “resolvida” por testes técnicos.

**Não verificado / PARCIAL:** reprodução experimental integral e upstream, instalação offline/outro sistema, auditoria completa de vulnerabilidades, funcionamento da cópia no futuro disco externo e bytes de duas versões pré-treino não recuperadas.

Próxima ação técnica necessária: conectar/autorizar o destino de backup. Não há necessidade técnica demonstrada de retreinar ou explorar novamente o teste para concluir este saneamento.
