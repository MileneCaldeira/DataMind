# DataMind

**Pesquisa em Ciência de Dados aplicada à eletrocardiografia**  
**Autoria:** Milene Caldeira

O DataMind investiga como a disponibilidade de medidas extraídas de eletrocardiogramas (ECGs) influencia a cobertura de exames e a avaliação de modelos de classificação. O estudo utiliza dados públicos do PTB-XL e PTB-XL+ para comparar diferentes estratégias de uso de medidas eletrocardiográficas na identificação da anotação de **bloqueio completo do ramo direito (CRBBB)**.

## Pergunta de pesquisa

Como diferentes requisitos de disponibilidade das medidas eletrocardiográficas afetam a proporção de exames avaliáveis e o desempenho probabilístico de classificadores da anotação CRBBB?

A análise considera tanto os resultados dos modelos quanto os exames que cada estratégia consegue atender. A comparação é operacional: as estratégias diferem no conjunto de variáveis e no tratamento de medidas ausentes, portanto os resultados não isolam um efeito causal da imputação.

## Dados e metodologia

O estudo utiliza duas fontes complementares do mesmo conjunto de ECGs:

- [PTB-XL 1.0.3](https://doi.org/10.13026/kfzx-aw45): metadados e anotações eletrocardiográficas.
- [PTB-XL+ 1.0.1](https://doi.org/10.13026/g6h6-7g88): medidas extraídas dos exames, incluindo características do ECGDeli.

A integração é realizada por `ecg_id`. Como as fontes correspondem aos mesmos exames, sua combinação não representa validação externa.

Foram desenvolvidos classificadores com **regressão logística e regularização L2**, além de controles para examinar o efeito da disponibilidade das características e da população de desenvolvimento. O contraste principal compara:

| Estratégia | Descrição |
| --- | --- |
| **E2-fallback** | Painel de oito medidas, com política de fallback definida no protocolo. |
| **E3** | Painel de 531 medidas, com imputação para valores ausentes. |

As partições seguem os folds do conjunto de dados, sem compartilhamento de pacientes entre desenvolvimento e teste: folds 1–8 para desenvolvimento, fold 9 para validação e definição de limiares e fold 10 para avaliação final. O desfecho principal é a diferença pareada no **Brier Score**, com intervalo de confiança obtido por reamostragem agrupada por paciente.

O protocolo, as demais estratégias e os critérios de comparação estão documentados nos [relatórios do projeto](reports/) e no [manuscrito](artigo/manuscrito_v4.md).

## Resultados principais

A avaliação final reuniu **2.198 exames de 1.904 pacientes**, incluindo **54 exames com a anotação CRBBB, pertencentes a 45 pacientes**.

| Indicador | Resultado |
| --- | ---: |
| Brier Score — E2-fallback | 0,006655 |
| Brier Score — E3 | 0,006042 |
| Diferença de Brier (E3 − E2-fallback) | −0,000613 |
| IC de 95% da diferença | [−0,002380; +0,001133] |
| Cobertura com as 531 medidas completas | 49,50% dos exames |
| Cobertura dos positivos com as 531 medidas completas | 64,81% |

A diferença observada no Brier Score **não sustenta uma conclusão de superioridade entre as estratégias**, e o estudo não foi desenhado para demonstrar equivalência. O fallback não foi acionado na avaliação final. Uma estratégia híbrida apresentou Brier de 0,005384, resultado considerado **secundário**.

Os resultados mostram que exigir todas as medidas altera a população de exames incluídos na avaliação. Isso reforça a importância de relatar **cobertura e desempenho conjuntamente**, sem concluir que o painel reduzido seja suficiente em outros contextos.

[Resultados detalhados](reports/fase6_resultados_finais.md) · [Manuscrito v4](artigo/manuscrito_v4.md)

## Limitações

A pesquisa utiliza anotações disponibilizadas nas bases de origem, sem reavaliação clínica independente dos diagnósticos. O número de pacientes positivos é limitado, e a comparação não inclui validação em uma população externa. A seleção das oito medidas foi exploratória e há pontos de interpretação das características eletrocardiográficas que ainda precisam ser esclarecidos.

Os resultados descrevem o comportamento dos modelos neste conjunto de dados. **Não constituem validação para uso clínico ou diagnóstico individual.**

## Estrutura do repositório

| Diretório | Conteúdo |
| --- | --- |
| `artigo/` | Manuscritos, figuras e tabelas |
| `docs/` | Protocolos, referências e decisões metodológicas |
| `src/datamind/` | Código de processamento e modelagem |
| `scripts/` | Rotinas de análise e verificação |
| `tests/` | Testes de manutenção |
| `experiments/` | Configurações experimentais |
| `reports/phase5/run001/` | Configurações e artefatos dos modelos finais |
| `reports/phase6/final001/` | Probabilidades e métricas da avaliação final |
| `data/` | Arquivos de dados e amostras locais, sujeitos às respectivas licenças |

## Reprodutibilidade

O ambiente original foi registrado com **Python 3.13.7**. As dependências estão documentadas em `reports/phase5/run001/requirements.lock.txt` e `reports/phase7/requirements-render.lock`.

Na raiz do projeto, as verificações de manutenção podem ser executadas com o ambiente Python correspondente:

```bash
python -B scripts/verify_preservation.py
python -B -m unittest discover -s tests -p test_maintenance.py -v
```

Esses comandos verificam a integridade dos artefatos e aspectos de manutenção; **não reproduzem integralmente o treinamento ou a avaliação final**. As probabilidades e métricas da execução original estão preservadas em `reports/phase6/final001/`.

Para informações sobre ambientes, preservação e recuperação dos resultados, consulte a [documentação técnica](reports/saneamento_tecnico_final.md).

## Documentação

- [Manuscrito atual](artigo/manuscrito_v4.md)
- [Resultados da avaliação final](reports/fase6_resultados_finais.md)
- [Guia do projeto](GUIA_DO_PROJETO.md)
- [Plano de evolução da pesquisa](docs/plano_evolucao_cientifica.md)
- [Fontes de dados e licenças](docs/dados-e-licencas.md)

**Situação da pesquisa:** experimentos e avaliação final concluídos; interpretação metodológica e preparação do manuscrito em andamento.
