# Fase 4 — literatura relacionada e contribuição candidata
Busca direcionada atualizada em 04/11/2026. Consultas incluíram “PTB-XL+ ECGDeli missing features benchmark”, “PTB-XL+ 2026 left ventricular hypertrophy”, “Sisk Sperrin imputation missing indicators” e “ECG systematic review”. Complementa a [revisão da Fase 3](fase3_revisao_literatura.md). Não é revisão sistemática própria.

| Fonte | O que já foi investigado | Implicação para o protocolo |
|---|---|---|
| Strodthoff et al., 2023, PTB-XL+ | Benchmark de extratores, classificadores e conjuntos compartilhados de variáveis | Não propor novidade apenas por usar medidas tabulares ou painel menor. [Artigo](https://doi.org/10.1038/s41597-023-02153-8) |
| Código público do benchmark | Função replace_nans preenche pela mediana e o código inclui classificadores tabulares | Imputação também não é contribuição nova. Código consultado no branch main em 04/11/2026, não reproduzido nem atribuído automaticamente à versão do artigo. [Código](https://github.com/tmehari/ptbxl_feature_benchmark/blob/main/code/feature_utils/utils.py) |
| Zhou, Luo e Du, 2026 | Estudo de hipertrofia ventricular com PTB-XL+, medidas comerciais, imputação e modelos | Sobreposição relevante de método/base. Outro rótulo não basta. [Artigo](https://doi.org/10.3389/fcvm.2026.1825829) |
| Sisk et al., 2023 | Estratégias de imputação e indicadores em desenvolvimento/implantação sob mecanismos diferentes | E3-I é análise secundária, com estabilidade do mecanismo como limitação. [Artigo](https://doi.org/10.1177/09622802231165001) |
| Avula, Wu e Carrick, 2023 | Revisão sistemática de aplicações clínicas e relato metodológico em ECG profundo | Reforça distinguir avaliação técnica de utilidade clínica. [Artigo](https://doi.org/10.1016/j.jacadv.2023.100686) |
| Elhussain et al., 2026 | Revisão sistemática de evidência até maio de 2026, com avaliação PROBAST | Atualiza contexto, mas não resolve nosso contraste específico. Artigo aceito em versão antecipada. [Artigo](https://doi.org/10.1186/s12872-026-06234-5) |
| Van Calster et al., 2019 | Metodologia de calibração | Justifica avaliar probabilidades além de AUC. [Artigo](https://doi.org/10.1186/s12916-019-1466-7) |
| Collins et al., 2024 | TRIPOD+AI | Orienta registrar escolhas, população e resultados completos. [Diretriz](https://doi.org/10.1136/bmj-2023-078378) |

Contribuição possível — demonstrar, com controles de treino e denominadores explícitos, quanto da mudança na avaliação vem de escolher exames completos, quanto vem do conjunto de variáveis e qual política apresenta menor erro na coorte de referência. Entregar código e resultados negativos também seria útil.

A busca consultada não identificou demonstração exatamente equivalente de todos esses contrastes para CRBBB/ECGDeli. Isso não prova ineditismo. Falta revisão exaustiva de suplementos, estudos de abstenção/classificação seletiva e trabalhos que usem outras palavras para o mesmo problema. A novidade científica permanece pendente, enquanto a pergunta experimental é testável.

E1 é um controle de seleção relevante ao problema proposto, não reprodução fiel do benchmark publicado que já trata ausências. Não atribuir aos autores exclusão de incompletos sem evidência. Se um trabalho equivalente for identificado, reformular para reprodução crítica explícita ou extensão externamente validada.

Limites de acesso — página Nature voltou a falhar por redirecionamento HTTP 500, embora trechos indexados e documentos oficiais estejam acessíveis. Foram consultadas páginas de artigos, documentação e código, sem execução dos benchmarks. Não transformar resultados publicados em confirmação independente local.
