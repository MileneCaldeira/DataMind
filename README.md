# DataMind — estado atual

Atualizado em 05/11/2026 após auditoria técnica de leitura. **Fases 1–9 documentadas; modelos treinados e teste final executado.** Manuscrito v2 preparado para revisão humana, sem validação clínica ou submissão.

## Comece aqui

- [Painel de estado](STATUS_DATAMIND.md): concluído, pendente e não verificado.
- [Entenda a IA construída](docs/ENTENDA_A_IA.md): explicação para quem trabalha com BI/SQL.
- [Guia do projeto](GUIA_DO_PROJETO.md): trajetória e arquivos principais.
- [Auditoria master](reports/auditoria_master.md): evidências, limites e achados.

## Pesquisa e resultado

Investigamos como a disponibilidade de medidas de ECG modifica cobertura, composição e avaliação de classificadores da **anotação CRBBB**. A comparação principal é operacional: 531 medidas com imputação (E3) versus oito medidas com fallback (E2-fallback), nos mesmos exames. Não isola o efeito causal da imputação.

PTB-XL 1.0.3 fornece metadados/anotações; PTB-XL+ 1.0.1 fornece medidas ECGDeli dos mesmos exames. Não são bases de validação independentes. Heart Disease, Adult, diabetes, uma amostra PhysioNet 2019 e materiais CODE-test pertencem à trajetória de viabilidade; não foram usados para treinar o classificador atual.

Foram implementadas regressões logísticas L2: E1 (531 completas), E2-C (oito, treino restrito aos completos), E2 (oito, treino elegível), E3 (531 imputadas), E3-I (com indicadores) e controles C=1. B0 é prevalência constante; fallback e híbrida combinam estratégias existentes. Não há Random Forest, XGBoost, rede neural treinada pelo projeto, aplicativo clínico ou API implantada.

Teste final: **2.198 exames / 1.904 pacientes; 54 positivos / 45 pacientes**. Brier E2-fallback **0,006655**, E3 **0,006042**; diferença **−0,000613**, IC95% **[−0,002380; +0,001133]**. Superioridade não sustentada; equivalência não demonstrada. Exigir 531 medidas completas cobriu **49,50% dos exames e 64,81% dos positivos**. Fallback não acionado. Híbrida: Brier **0,005384**, secundário. [Resultados completos](reports/fase6_resultados_finais.md).

## Arquitetura e pastas

Dados → auditoria/integração → transformações no treino → modelos → probabilidades salvas → métricas → manuscrito/apresentação.

|Local|Função|
|---|---|
|data/|Originais, fontes e amostras; preservar e revisar licenças antes de distribuir|
|experiments/|Configurações históricas e do piloto; não são autorização para executar|
|src/datamind/; scripts/; tests/|Lógica compartilhada, executores e testes|
|reports/phase5/run001/|Configuração, limiares, ambiente, modelos e freeze.json|
|reports/phase6/final001/|Probabilidades finais, métricas e registro da execução única|
|docs/; reports/|Protocolos, literatura, decisões e interpretação|
|artigo/; apresentacao/|Manuscrito v2, histórico v1, figuras/tabelas e cinco slides Markdown|
|.venv-phase5/; .venv-phase7/|Ambientes Windows/Python; reconstrução limpa ainda não retestada|

## Consulta segura e reprodução

Para consultar, abra Markdown, JSON, CSV e figuras existentes **sem executar scripts**. Fonte numérica: reports/phase6/final001/metrics.json. Sensibilidade/especificidade com limiares congelados estão em overall/strata e bootstrap.binary_frozen_thresholds; campos legados primary/paired e bootstrap.metrics usam 0,5.

Duas verificações inspecionadas como somente leitura, executadas da raiz com Python: `python -B scripts/verify.py` e `python -B scripts/fase5_freeze.py --check`. Elas verificam referências específicas; não validam clinicamente o estudo nem reproduzem treinamento.

Não chamar novamente fase6_predict_once.py. Não executar verificadores indiscriminadamente: fase5_verify.py gera previsões de validação e executa testes com ajustes sintéticos; outros scripts escrevem logs, resultados ou manifestos. Instruções históricas abaixo não são um roteiro de execução atual.

Folds 1–8: desenvolvimento; 9: limiares/validação; 10: teste já utilizado. Preserve dados, modelos, configurações, limiares, probabilidades e manifestos. Dependências: reports/phase5/run001/requirements.lock.txt e reports/phase7/requirements-render.lock. Python 3.13.7 registrado. [Plano de backup](reports/plano_backup.md) e [auditoria Git](reports/auditoria_git.md): versionamento não substitui backup.

## Limites e publicação

Poucos pacientes positivos; alvo derivado do próprio ECG; ausência de validação externa; painel exploratório; ambiguidades RR_Mean_Global/RRi_max e QRS_Dur_Global/QRSd_max; calibração limitada. AUC alta e sensibilidade observada de 100% não provam diagnóstico independente ou perfeição populacional.

Contribuição incremental de avaliação e cobertura. [Manuscrito v2](artigo/manuscrito_v2.md) pronto para revisão especializada, não para uso clínico ou submissão automática. Faltam cardiologista, bioestatístico, avaliação editorial e decisões institucionais/autoria/licença. [Pacote de revisão](reports/fase9_pendencias.md).

## Registro histórico preservado — Fases 1–2

O texto abaixo descreve o estado em 03/11/2026. Afirmações de ausência de modelos, biblioteca padrão e experimentos futuros têm esse escopo histórico; não descrevem as Fases 5–9.

### DataMind (texto original)

Diagnóstico de viabilidade realizado em **03/11/2026 (America/Sao_Paulo)**. Nenhum modelo foi treinado.

**Fase 2 concluída:** [validação científica](reports/validacao_cientifica.md), [revisão direcionada](docs/revisao_literatura.md), [matriz de qualidade](docs/matriz_qualidade.md) e [perguntas candidatas](docs/perguntas_candidatas.md). Recomendação: **reformular A**, sem aprovação definitiva. Acesso amostral ao PhysioNet confirmado, com divergência de licença registrada.

Leia [o relatório](reports/viabilidade.md), [as decisões](docs/decisoes.md) e [a revisão inicial](docs/literatura.md).

## Reproduzir

Python 3.13.7 foi usado no Windows 11. O código usa apenas a biblioteca padrão, sem instalação de pacotes, conta ou credencial.

```powershell
python scripts/audit.py
python scripts/verify.py
```

Para repetir sem rede, após o primeiro download:

```powershell
python scripts/audit.py --offline
python scripts/verify.py
```

Execute de qualquer diretório usando o caminho do script. Os caminhos de saída são relativos à raiz do projeto. A auditoria sobrescreve `reports/audit.json`, inventários, amostras e `runtime.json`; o log de acesso é cumulativo. A execução inicial está preservada em `reports/baseline/`. A verificação compara hashes dos arquivos e resultados ao diagnóstico inicial; se a fonte mudar, falha para revisão humana, sem atualizar a referência automaticamente.

Fase 2, usando cache local (padrão sem rede):

```powershell
python scripts/phase2.py
python scripts/verify_phase2.py
```

Em uma cópia nova, após obter os arquivos da Fase 1, use `python scripts/phase2.py --download` para baixar documentos e a amostra PhysioNet. Arquivos já presentes não são substituídos. O manifesto da Fase 2 registra os bytes usados e falha se forem diferentes; não se atualiza automaticamente. `docs/matriz_qualidade.md` e `docs/atributos_heart76.md` são gerados pelo script; os demais relatórios são interpretativos. A verificação de reprodução não equivale a validação científica independente.

## Organização

- `scripts/`: download, auditoria e verificação; sem modelagem.
- `data/raw/`: originais locais, ignorados pelo Git; URLs e hashes no log.
- `data/samples/`: primeiras 20 linhas de cada tabela, apenas para inspeção de formato, sem representatividade estatística.
- `reports/`: resultados completos por coluna, acesso, inventários ZIP e relatório interpretativo.
- `docs/`: decisões, literatura e atribuições.
- `experiments/`: protocolo para trabalhos futuros, ainda não executados.

Heart Disease e Adult: amostras derivadas de dados UCI sob CC BY 4.0; ver [atribuições](docs/dados-e-licencas.md). A amostra de diabetes permanece local e ignorada pelo Git enquanto a licença da derivação não for esclarecida. Dados brutos não são redistribuídos por este repositório. Não há licença geral de software definida nesta etapa.
