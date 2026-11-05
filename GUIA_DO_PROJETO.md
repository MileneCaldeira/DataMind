# Guia do projeto DataMind

Guia de leitura e preservação — 05/11/2026. Não autoriza novas execuções.

**Saneamento técnico concluído no escopo permitido:** ambientes reconstruídos sem inferência, código/documentação com versionamento local ampliado e verificador seguro disponível. Use `python -B scripts/verify_preservation.py` para conferir integridade sem executar modelos. O backup real ainda aguarda dispositivo externo autorizado. [Resultados e limites](reports/saneamento_tecnico_final.md).

**Atualização master:** consulte [STATUS_DATAMIND.md](STATUS_DATAMIND.md), [Entenda a IA](docs/ENTENDA_A_IA.md) e [auditoria master](reports/auditoria_master.md). Os READMEs foram atualizados, mantendo textos históricos. As observações abaixo sobre README desatualizado e Git sem commits descrevem o inventário anterior; o estado atual do versionamento está em [auditoria Git](reports/auditoria_git.md). Nenhum resultado científico foi alterado.

## Por onde começar

Leia nesta ordem:

1. [Resumo da pesquisa](reports/fase9_resumo_pesquisa.md).
2. [Guia para compreender e defender o estudo](docs/guia_defesa_pesquisa.md).
3. [Manuscrito atual, versão 2](artigo/manuscrito_v2.md).
4. [Resultados científicos finais](reports/fase6_resultados_finais.md).
5. [Pendências para revisão e publicação](reports/fase9_pendencias.md).

## O que é o DataMind

É um projeto de pesquisa sobre dados e inteligência artificial aplicada à saúde. O repositório guarda a investigação atual e o caminho até ela: viabilidade, decisões, dados, programas, resultados e textos científicos.

A pesquisa atual estuda como a disponibilidade de medidas extraídas do eletrocardiograma afeta cobertura, composição da população avaliada e desempenho de classificadores da **anotação CRBBB**, relacionada ao bloqueio completo do ramo direito. Reconhecer essa anotação do próprio ECG não demonstra diagnóstico independente ou utilidade clínica.

Utilizamos PTB-XL/PTB-XL+, regressões logísticas e estratégias com painéis completos, reduzidos e imputação de ausências. O contraste principal muda tanto o painel quanto o tratamento de ausências: não isola um efeito causal da imputação.

## O que foi construído nas Fases 1–9

|Fase|Produto e localização|
|---|---|
|1|Viabilidade de bases públicas: reports/viabilidade.md.|
|2|Qualidade e comparabilidade do Heart Disease e amostra PhysioNet 2019: reports/validacao_cientifica.md.|
|3|Redefinição para ECG, PTB-XL+ e alternativa CODE-test: reports/fase3_comparacao_final.md.|
|4|Protocolo, desenho, riscos e configurações: reports/fase4_protocolo_cientifico.md.|
|5|Auditoria, treinamento piloto, validação e congelamento: reports/fase5_treinamento_piloto.md.|
|6|Execução final única no fold 10, resultados e interpretação preservados em reports/fase6_*.md.|
|7|Literatura, figuras, tabelas e artigo/manuscrito_v1.md.|
|8|Revisão crítica automatizada, artigo/manuscrito_v2.md e questões para especialistas.|
|9|Pacote para revisores humanos, resumo, cinco slides Markdown e matriz de comentários ainda sem pareceres reais.|

A revisão automatizada não substitui avaliação humana independente. O README.md e experiments/README.md descrevem etapas antigas; suas afirmações de que não houve treinamento não representam o estado atual. Foram preservados.

## Mapa simples

```text
DataMind/
├── data/                 dados das fontes e amostras
├── experiments/          configurações e planejamento histórico
├── src/datamind/          funções reutilizáveis
├── scripts/              programas de cada etapa
├── tests/                verificações automatizadas
├── reports/              relatórios e evidências computacionais
│   ├── phase5/run001/    treinamento, modelos e congelamento
│   └── phase6/final001/  probabilidades finais e métricas
├── docs/                 protocolos, literatura, decisões e guias
├── artigo/               manuscritos, tabelas e figuras
├── apresentacao/         cinco slides em Markdown
├── .venv-phase5/         ambiente Python experimental
├── .venv-phase7/         ambiente de figuras
└── .git/                 metadados locais de Git
```

**Dados originais → Auditoria → Preparação → Treinamento → Modelos → Avaliação → Resultados → Manuscrito → Apresentação.**

Protocolos e configurações orientam o fluxo; testes e manifestos verificam integridade. Folds 1–8 foram usados no desenvolvimento, fold 9 na validação e fold 10 no teste final. O teste já foi utilizado e não deve ser repetido para escolher modelos.

## Onde encontrar os componentes

|Necessidade|Arquivo ou pasta|
|---|---|
|Medidas e metadados ECG|data/raw/phase3/ecgdeli_features.csv e ptbxl_database.csv|
|Origem e risco de vazamento|docs/fase5_auditoria_leakage.md|
|Regras e emendas pré-treino|reports/fase4_protocolo_cientifico.md; docs/fase5_emendas_pre_treino.md|
|Configuração e limiares registrados|reports/phase5/run001/config.json e thresholds.json|
|Modelos treinados|reports/phase5/run001/models/|
|Congelamento|reports/phase5/run001/freeze.json|
|Probabilidades já calculadas|reports/phase6/final001/predictions.csv e scores_*.csv|
|Métricas e composição finais|reports/phase6/final001/metrics.json e composition.json|
|Interpretação científica|reports/fase6_interpretacao_cientifica.md|
|Manuscrito vigente|artigo/manuscrito_v2.md|
|Apresentação|apresentacao/fase9_apresentacao.md|
|Decisões|docs/decisoes.md, docs/decisoes_fase7.md e relatórios de decisão por fase|

Arquivos .py são programas; .json são configurações ou resultados; .csv são tabelas; .joblib guardam modelos; .md são textos; .png/.svg/.pdf são figuras. Ler resultados não exige executar programas.

## Resultados já obtidos

O teste final contém **2.198 exames de 1.904 pacientes**, com **54 exames positivos de 45 pacientes**.

- Brier E2-fallback: **0,006655**; E3: **0,006042**. Menor Brier significa menor erro probabilístico médio.
- Diferença principal E3 − E2-fallback: **−0,000613**, IC95% **[−0,002380; +0,001133]**.
- O intervalo inclui zero: superioridade não recebeu suporte estatístico; equivalência também não foi demonstrada.
- Exigir as 531 medidas completas cobre **49,50% dos exames** e **64,81% dos positivos**: seleciona uma população diferente.
- A híbrida teve Brier **0,005384**, resultado secundário.
- O fallback não foi acionado no teste; seu funcionamento em uso efetivo não foi validado nessa população.

Fonte: resultados salvos da Fase 6. Nenhuma métrica foi recalculada nesta organização. Há poucos pacientes positivos, o alvo vem do próprio ECG e não houve validação externa.

## Consultar resultados sem executar

Abra relatórios e manuscrito no editor. Para detalhes, visualize os JSON, tabelas e figuras existentes. Evite salvar CSV abertos em planilhas: conversões automáticas podem alterar valores e identificadores.

**Nenhum script é necessário para leitura.** “verify” no nome não garante ausência de escrita: alguns verificadores geram logs e manifestos. Geradores de materiais sobrescrevem entregas. scripts/fase6_predict_once.py não é um comando de consulta.

## O que falta para publicação

O pacote permite solicitar revisão humana, não submissão imediata. Faltam parecer clínico sobre medidas e alvo, revisão bioestatística e editorial, resolução dos comentários e definições de autoria, afiliações, ética institucional, conflitos, financiamento, declaração de IA e disponibilização do código.

Consulte docs/fase9_revisao_*.md. A matriz reports/fase9_matriz_feedback.md aguarda comentários reais. Nada foi enviado por esta tarefa.

## Arquivos que não devem ser modificados

Preserve dados brutos, modelos, probabilidades, configurações, limiares, protocolos congelados, manifestos, logs finais e PREDICTION_STARTED.lock. Preserve também manuscritos anteriores, resultados negativos, código, fontes e versões das dependências. Um arquivo gerado pode ser evidência essencial.

data/raw/phase3/model.npy contém escores externos do CODE; não é um modelo treinado pelo DataMind. Os ambientes virtuais são reconstruíveis em princípio, mas isso depende de Python e pacotes compatíveis e não foi testado nesta auditoria.

## Como preservar e fazer backup

1. Faça cópia integral datada em destino privado independente da pasta sincronizada, mantendo caminhos e manifestos; não sobrescreva o único backup.
2. Confirme disponibilidade local dos arquivos OneDrive e confira restauração e hashes em cópia separada.
3. Preserve data/, código, configurações, documentação e reports/, incluindo modelos e probabilidades. Só o manuscrito não permite auditoria.
4. Considere backups menores sem ambientes somente após validar sua reconstrução. Preserve locks, versões e código necessário para carregar modelos.
5. Git não substitui backup. A branch atual não tem commits nem arquivos rastreados, embora .git contenha objetos e referências. É necessário estabelecer posteriormente um histórico versionado revisado.

Não publique automaticamente dados de saúde, identificadores ou artigos baixados. Permissões variam entre fontes; a licença geral do código é pendente.

Detalhes: [inventário técnico](reports/mapa_repositorio.md) e [melhorias propostas](reports/recomendacoes_organizacao.md). Nenhuma reorganização foi executada.
