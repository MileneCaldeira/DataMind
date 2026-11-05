# Auditoria Git — primeiro versionamento local

## Atualização: saneamento técnico de 05/11/2026

O primeiro commit **e799a5d** existe, contém os 39 arquivos registrados abaixo e foi preservado. Branch master, sem remoto ou push. O novo commit **bdc086b** acrescenta proteção e histórico científico: 86 caminhos alterados, incluindo .gitattributes, .gitignore, três ferramentas de manutenção, testes não preditivos, registro de snapshots, protocolos, manuscritos v1/v2, apresentação, relatórios científicos, tabelas agregadas, locks, configurações e manifestos. Lista exata: `git diff-tree --no-commit-id --name-status -r bdc086b`.

Todos os 32 arquivos Python próprios em src/scripts/tests estão rastreados. Código experimental antigo e manuscritos mantêm bytes originais. .gitattributes impede normalização automática dos finais de linha. .gitignore agora protege dados/amostras, ambientes, modelos, probabilidades CSV, fontes bibliográficas baixadas, binários, logs e arquivos típicos de credencial. Nenhuma exclusão local foi realizada.

Diff completo do primeiro saneamento: 553.634 caracteres / 7.889 linhas, SHA-256 bf792fb1290debdc5a9d62cc91deb839763d8daa3094574230eea1e94aa580eb. Blobs staged comparados byte a byte com arquivos locais; leitura textual, sintaxe, caminhos e padrões de segredos verificados. Dezessete avisos de whitespace correspondiam exatamente a dois espaços de quebra Markdown em três documentos congelados: preservados, não “corrigidos”.

Um commit documental subsequente registra o resultado final, atualiza README/STATUS/guia/plano/esta auditoria e inclui as notas de revisão remanescentes. Seu conteúdo exato está no histórico Git e no relatório final; nenhum commit anterior foi emendado. Dados, modelos, probabilidades por registro e cópias de terceiros permanecem fora do Git. Essa exclusão é deliberada e exige backup independente, ainda pendente.

Os tópicos abaixo descrevem o primeiro commit, não o estado atual completo. Licença para publicação continua pendente; commits são exclusivamente locais.

05/11/2026. Decisão: **seleção apta para primeiro commit exclusivamente local**, após conferência do index. Não configurar remoto, publicar ou enviar arquivos. Este documento registra a seleção; a efetivação é comprovada pelo commit no histórico local, não pela existência desta lista.

## Estado encontrado

Branch master sem commits; git ls-files vazio; sem remoto configurado. .git contém objetos e referências internas refs/codex/turn-diffs, que não foram apagados, convertidos ou tratados como histórico da branch. Não foi feita limpeza de objetos ou reescrita de histórico.

Há identidade Git já configurada; usá-la sem inventar autoria e sem reproduzir seu e-mail neste relatório. O commit é registro técnico sob essa configuração, não declaração de autoria científica. Não há hooks ativos identificados: apenas arquivos .sample. core.autocrlf=true está configurado no ambiente; a inclusão utiliza override **-c core.autocrlf=false** para preservar os bytes atuais nos blobs, sem alterar configuração global.

## Conteúdo selecionado

Somente código próprio do projeto, testes com exemplos sintéticos, configurações, .gitignore e documentação de manutenção/agregada. **39 arquivos** explicitamente listados:

```text
.gitignore
GUIA_DO_PROJETO.md
README.md
STATUS_DATAMIND.md
docs/ENTENDA_A_IA.md
experiments/README.md
experiments/fase4.json
experiments/fase5.json
reports/auditoria_git.md
reports/auditoria_master.md
reports/plano_backup.md
scripts/audit.py
scripts/fase3.py
scripts/fase4_preflight.py
scripts/fase5_evaluate.py
scripts/fase5_freeze.py
scripts/fase5_reports.py
scripts/fase5_train.py
scripts/fase5_verify.py
scripts/fase6_analyze.py
scripts/fase6_predict_once.py
scripts/fase6_reports.py
scripts/fase6_verify.py
scripts/fase7_materials.py
scripts/fase7_verify.py
scripts/fase8_revise.py
scripts/fase8_verify.py
scripts/fase9_verify.py
scripts/phase2.py
scripts/verify.py
scripts/verify_phase2.py
src/datamind/__init__.py
src/datamind/evaluation.py
src/datamind/final_eval.py
src/datamind/integrity.py
src/datamind/pilot.py
tests/test_integrity.py
tests/test_phase5.py
tests/test_phase6.py
```

Não foram incluídos dados brutos/amostras, probabilidades por exame, identificadores individuais, modelos, ambientes, caches, artigos/suplementos de terceiros, imagens ou todo o diretório reports. Os scripts têm links públicos e regras de acesso; não contêm as bases baixadas. A lista não usa curingas de diretórios na operação git add, nem -A, nem -f.

A licença geral do projeto segue pendente para distribuição. Armazenar localmente o código/documentação produzidos no projeto não atribui licença nova nem redistribui material de terceiros. Scripts que obtêm fontes externas são distintos de cópias das fontes. Se surgisse conteúdo de autoria/licença incerta no conjunto selecionado, o commit deveria parar; nenhum caso material foi identificado nessa seleção.

Este é um **primeiro snapshot técnico**, não pacote de reprodução autossuficiente: dados, modelos, resultados e protocolos detalhados continuam locais e precisam de backup. Links para arquivos não versionados podem não funcionar numa cópia só do commit; isso é explícito, não evidência de perda local.

## Inspeção de segurança e tamanho

Foram examinados texto e imports do código, padrões de chaves privadas/tokens conhecidos, atribuições de segredos e caminhos/e-mails no conjunto candidato. Não houve correspondências de credenciais nesses controles. Varredura ampliada de 177 arquivos textuais em diretórios científicos também não encontrou os padrões fortes de segredo pesquisados. Isso não é certificação de ausência de qualquer segredo: padrões não detectam toda credencial possível e não auditam binários/ambientes.

Caminhos pessoais aparecem em reports/mapa_repositorio.md e reports/phase5/run001/environment.json (este com escapes JSON); ambos ficaram fora da seleção. Configuração Git contém identidade pessoal normal de autoria do commit; não é publicada nesta ação.

Os maiores arquivos reais são medidas ECGDeli (~62 MB), diabetes (~13,5 MB), metadados (~6,6 MB) e OOF (~3,7 MB cada); não entram. Seleção é textual e pequena, sem arquivos acima de 1 MB. Modelos contêm conjuntos de IDs de treino e não devem ser publicados indiscriminadamente.

.gitignore raiz exclui dados brutos, amostra diabetes, caches e .venv-phase5. .venv-phase7 tem .gitignore interno “*”; git check-ignore confirmou ambos ambientes excluídos. A ausência de regras para modelos/probabilidades torna **inadequado git add -A**, mesmo após o primeiro commit. .gitignore não foi alterado.

## Procedimento e verificações do index

1. Exigir index inicialmente vazio; não remover staged de outra pessoa.
2. Adicionar somente a lista literal acima com git -c core.autocrlf=false add -- caminhos.
3. Comparar git diff --cached --name-only com a lista exata.
4. Ler todos os blobs staged; conferir SHA-256 igual aos arquivos de trabalho, tamanho e tipo texto; repetir varredura de credenciais.
5. Analisar sintaxe dos 28 Python sem executar modelos. Não rodar suíte que treina/prediz.
6. git diff --cached --check pode sinalizar linhas em branco históricas; distinguir formatação de erro sem editar código congelado.
7. Criar commit local “Document and audit DataMind research pipeline”.
8. Conferir HEAD, arquivos e identidade de bytes. Deixar arquivos científicos não selecionados intactos e não rastreados.

Não incluir hash do próprio commit dentro deste documento, evitando autorreferência e emenda do commit. A confirmação pode ser consultada com git log -1 --oneline e git show --stat HEAD. Se o commit falhar, não declarar sucesso; a lista é preparação auditada, não execução.

## Resultado da conferência antes do commit

Index preparado com exatamente os 39 caminhos acima; todos os blobs staged foram lidos e comparados byte a byte aos arquivos locais. Sintaxe dos 28 Python válida, sem execução. Nenhum binário, dado por exame/paciente, modelo ou ambiente incluído. Os demais arquivos continuam fora do index.

A primeira captura de git diff --check falhou ao decodificar a saída com cp1252; não foi erro experimental. Repetida com decodificação UTF-8 explícita e core.whitespace incluindo cr-at-eol, para reconhecer os finais CRLF preservados: **exit 0**, sem problemas de whitespace. Não foram normalizados finais de linha nem editado código congelado.

Snapshot de leitura desta auditoria confirmou que os únicos arquivos anteriores alterados são README.md, experiments/README.md e GUIA_DO_PROJETO.md. A seleção será reconferida imediatamente antes do commit; a presença de HEAD e seus 39 caminhos confirma a efetivação local.

## Riscos remanescentes do versionamento

- Git local não é backup independente.
- Clone/checkout com conversão de finais de linha pode divergir dos SHA-256 experimentais; usar core.autocrlf=false ao materializar os arquivos e conferir hashes. Não normalizar arquivos congelados.
- Documentação atualizada não equivale a autorização de execução: alguns verificadores escrevem e fazem previsões.
- README de experiments foi atualizado por autorização, mas é referido no snapshot pré-treino. A divergência documental está registrada em auditoria_master.md; não reescrever a referência antiga.
- Revisão de licença, ética e privacidade é necessária antes de qualquer depósito público; não existe autorização de publicação.
