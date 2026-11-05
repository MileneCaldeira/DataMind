# Plano de backup independente

## Atualização executável — saneamento técnico

Inspeção em 05/11/2026 encontrou somente o disco físico 0 (NVMe de aproximadamente 1 TB), com C: e partições de sistema/recuperação, cerca de 589 GB livres em C:. Nenhuma unidade externa acessível ou destino previamente autorizado foi identificado. Outra pasta em C: não será tratada como backup independente.

**O que precisa da pesquisadora:** conectar SSD/HD externo privado e autorizar um diretório existente nele, informando caminho completo (por exemplo E:/BackupPrivadoDataMind, somente se E: for realmente outro disco). Recomenda-se pelo menos 2 GiB livres para a primeira cópia e folga; manter espaço adicional para versões.

Foi implementado scripts/backup_project.py. Após autorização do destino, executar da raiz:

```powershell
python -B scripts/backup_project.py --destination "E:/BackupPrivadoDataMind" --authorized-destination
```

O exemplo NÃO autoriza E: nem cria esse diretório automaticamente. O programa identifica o número do disco via Get-Partition, recusa disco igual, destinos dentro da origem, junções/symlinks que exijam revisão e espaço insuficiente. Cria snapshot datado com sufixo único, copia sem sobrescrever, verifica SHA-256/inventário, verifica estabilidade da origem e restaura quatro arquivos críticos a partir da cópia, sem carregar modelos. Recibo com destino, data, contagem, bytes e hashes fica no snapshot. Cópia interrompida não recebe status PASS e não é apagada.

Nove testes não preditivos passaram; incluem cópia/restauração de fixtures, adulteração, destino dentro da origem e recusa do mesmo disco. **Isso valida a ferramenta nesses cenários, não constitui backup real do projeto nem teste em disco externo.**

As duas venvs foram reconstruídas a partir dos locks no mesmo Windows/Python; importações e leitura dos modelos passaram. A opção --essential omite somente .venv-phase5 e .venv-phase7, mantendo dados, código, modelos, resultados, documentação e .git. Mesmo assim, recomenda-se primeira cópia integral: instalação futura depende da disponibilidade dos pacotes e não foi testada offline. Não remover ambientes originais. Área temporária de reconstrução no disco C: não é backup.

As estimativas e o procedimento manual histórico abaixo permanecem como registro. Preferir agora a ferramenta testada, fechar gravadores e estabilizar o OneDrive antes de executar. O estado real do backup continua **PENDENTE**.

05/11/2026. **PENDENTE:** nenhum destino externo previamente autorizado foi identificado. Não foi criada cópia em local arbitrário nem enviado conteúdo a serviço externo.

## Necessidade e tamanho

Inventário inicial desta auditoria: 16.358 arquivos, 582.157.761 bytes, incluindo .git, ambientes e três documentos da organização anterior. A diferença para 16.354 arquivos é de quatro arquivos internos do Git; não representa novo experimento. Contagens/tamanho variam com novos documentos e commits.

- Integral: cerca de **556 MiB por instantâneo**, antes do crescimento do Git/novos textos. Reservar pelo menos **2 GiB livres** para uma cópia e folga, mais espaço para versões.
- Essencial sem os dois ambientes: cerca de **117 MiB**, incluindo dados, resultados, código/documentação e .git. Reservar **1 GiB** para versões e crescimento.
- Ambientes: cerca de **439 MiB**. A reconstrução limpa/offline não foi demonstrada. A primeira cópia recomendada é integral.

Armazenamento recomendado: SSD/HD externo privado, em dispositivo físico distinto e fora do OneDrive, preferencialmente protegido por criptografia gerida pela pesquisadora. Outra pasta/partição no mesmo disco não protege de falha física. Uma segunda cópia em local físico separado aumenta resiliência; serviço externo exige autorização específica.

OneDrive pode sincronizar exclusão, corrupção e conflito. Histórico remoto e status de disponibilidade não foram verificados. Arquivos apenas online podem precisar de download durante leitura/cópia; confirmar disponibilidade local previamente. Nunca interpretar “sincronizado” como restauração testada.

## O que preservar

Integralmente: data/raw, data/samples históricos, src, scripts, tests, experiments, docs, reports, artigo, apresentacao, arquivos da raiz e .git. Em reports preservar modelos, OOF, grids, configurações, limiares, ambiente/locks, probabilidades finais, logs, receipts, guard e manifestos. Preservar versões anteriores do manuscrito e resultados negativos.

Ambientes são reconstruíveis em princípio; ainda não são substituíveis por uma garantia de reinstalação. Caches podem ser regenerados, mas a cópia integral não precisa excluí-los. Um commit de código/documentação não contém os dados e resultados completos.

## Procedimento proposto — não executado

Primeiro: fechar processos que gravem no projeto, esperar sincronização estável, marcar a pasta como disponível localmente e escolher um dispositivo independente. Conferir dispositivo físico no Gerenciamento de Disco; letras diferentes não provam independência. Confirmar capacidade e permissão.

O bloco abaixo é para **PowerShell 7**, a partir da raiz DataMind. Trocar o caminho de exemplo somente após confirmar/autorizar o dispositivo; não usar automaticamente E: se apontar para outro local. Não usa /MIR, /PURGE nem exclusão.

```powershell
$origemDataMind = (Get-Location).Path
$raizBackupDataMind = 'E:\BackupPrivadoDataMind' # EXEMPLO: confirmar disco externo antes
if (!(Test-Path -LiteralPath (Split-Path $raizBackupDataMind -Qualifier))) {
    throw 'Dispositivo de backup não disponível'
}
if (!(Test-Path -LiteralPath (Join-Path $origemDataMind 'STATUS_DATAMIND.md'))) {
    throw 'Execute na raiz correta do DataMind'
}
$destinoDataMind = Join-Path $raizBackupDataMind ('DataMind_' + (Get-Date -Format 'yyyyMMdd_HHmmss'))
if (Test-Path -LiteralPath $destinoDataMind) { throw 'Destino já existe' }
if ([IO.Path]::GetFullPath($destinoDataMind).StartsWith(
    [IO.Path]::GetFullPath($origemDataMind) + [IO.Path]::DirectorySeparatorChar,
    [StringComparison]::OrdinalIgnoreCase)) { throw 'Destino dentro da origem' }

# Verificar espaço livre e independência física ANTES de prosseguir.
New-Item -ItemType Directory -Path $destinoDataMind -ErrorAction Stop | Out-Null
& robocopy $origemDataMind $destinoDataMind /E /COPY:DAT /DCOPY:T /XJ /R:1 /W:1
if ($LASTEXITCODE -ge 8) { throw 'Falha de cópia: não considerar backup válido' }

$arquivosOrigem = @(Get-ChildItem -LiteralPath $origemDataMind -File -Recurse -Force -ErrorAction Stop)
$arquivosDestino = @(Get-ChildItem -LiteralPath $destinoDataMind -File -Recurse -Force -ErrorAction Stop)
if ($arquivosOrigem.Count -ne $arquivosDestino.Count) { throw 'Contagens diferentes' }
$verificacaoBackup = foreach ($arquivoDataMind in $arquivosOrigem) {
    $relativoDataMind = [IO.Path]::GetRelativePath($origemDataMind, $arquivoDataMind.FullName)
    $copiaDataMind = Join-Path $destinoDataMind $relativoDataMind
    if (!(Test-Path -LiteralPath $copiaDataMind -PathType Leaf)) { throw "Falta: $relativoDataMind" }
    $hashOrigemDataMind = (Get-FileHash -LiteralPath $arquivoDataMind.FullName -Algorithm SHA256).Hash
    $hashCopiaDataMind = (Get-FileHash -LiteralPath $copiaDataMind -Algorithm SHA256).Hash
    if ($hashOrigemDataMind -ne $hashCopiaDataMind) { throw "Divergência: $relativoDataMind" }
    [pscustomobject]@{Path=$relativoDataMind; SHA256=$hashOrigemDataMind}
}
$verificacaoBackup | Export-Csv -LiteralPath ($destinoDataMind + '_SHA256.csv') -NoTypeInformation -Encoding utf8
```

O CSV de conferência fica ao lado da cópia, sem alterar origem ou manifestos experimentais. Reparse points/junções reais precisam de inspeção própria: /XJ evita seguir junções; qualquer diferença de contagem exige investigação, não aprovação automática. A leitura de placeholders OneDrive também pode falhar; registrar falhas.

Após copiar, abrir documentos e conferir manifestos na cópia sem executar modelos. Testar restauração em diretório separado, nunca sobre a única origem. Uma venv copiada pode conservar caminhos absolutos: cópia íntegra de bytes não demonstra execução portátil.

## Rotina recomendada

Manter pelo menos dois instantâneos datados, um anterior a mudanças importantes. Desconectar o dispositivo após conferência quando apropriado; não deixar a única cópia sempre exposta às mesmas credenciais/processos. Registrar data, destino, resultado de hashes e teste de restauração em registro privado.

Backup essencial pode ser considerado depois de validar reconstrução em cópia separada. Não remover ambientes atuais ou ajustar arquivos congelados para facilitar cópia.
