# Fase 3 — revisão direcionada
Consolidada em 04/11/2026. Busca orientada a decisões, sem pretensão de revisão sistemática própria. Consultas combinaram PTB-XL+, missing features, calibration, clinical prediction missing indicators, ECG systematic review e leakage. Fontes primárias priorizadas. A atualização e a comparação mais específica estão na [literatura da Fase 4](fase4_literatura_relacionada.md).

| Trabalho e tipo | Evidência relevante | Limite e relação com nossas opções |
|---|---|---|
| Wagner et al., 2020, descrição de dados. [DOI](https://doi.org/10.1038/s41597-020-0495-6) | PTB-XL, anotações e partições por paciente | Base histórica, não validação prospectiva. Sustenta A/B/E |
| Strodthoff et al., 2023, benchmark metodológico. [DOI](https://doi.org/10.1038/s41597-023-02153-8) | PTB-XL+, três extratores e comparação de conjuntos de medidas | Comparar extratores ou modelos já foi feito. A exige contraste específico de cobertura |
| Zhou, Luo e Du, 2026, estudo aplicado. [DOI](https://doi.org/10.3389/fcvm.2026.1825829) | Detecção de hipertrofia ventricular com medidas PTB-XL+, imputação e classificadores | Trocar o diagnóstico por CRBBB não estabelece novidade |
| Sisk et al., 2023, simulação e aplicação. [DOI](https://doi.org/10.1177/09622802231165001) | Imputação e indicadores dependem do mecanismo e da implantação | Fundamenta A/B, não demonstra qual política vence em ECG |
| Singh, Sato e Ohkuma, 2021, estudo de missingness. [DOI](https://doi.org/10.2196/25022) | Informação da ausência em dados de UTI e cenários de uso | Forte antecedente de D. Generalização não assegurada |
| Ribeiro et al., 2020, rede e referência médica. [DOI](https://doi.org/10.1038/s41467-020-15432-4) | CODE e teste com leitores, fonte de escores fixos | Comparação com médicos já existe. C deve focar sensibilidade da avaliação à referência |
| Van Calster et al., 2019, metodologia. [DOI](https://doi.org/10.1186/s12916-019-1466-7) | Calibração requer avaliação própria | Motivação transversal, não evidência de ganho local |
| Avula, Wu e Carrick, 2023, revisão sistemática. [DOI](https://doi.org/10.1016/j.jacadv.2023.100686) | Aplicações e qualidade do relato em ECG profundo | Busca até julho de 2022, não inventário atual de todas as lacunas |
| Collins et al., 2024, diretriz TRIPOD+AI. [DOI](https://doi.org/10.1136/bmj-2023-078378) | Transparência de desenvolvimento e avaliação | Diretriz não substitui experimento nem garante novidade |
| Kapoor e Narayanan, 2023, análise metodológica. [DOI](https://doi.org/10.1016/j.patter.2023.100804) | Vazamento ameaça reprodução em ML científico | E é requisito de qualidade com contribuição isolada incerta |
| Elhussain et al., 2026, revisão sistemática aceita. [DOI](https://doi.org/10.1186/s12872-026-06234-5) | PRISMA, busca até maio de 2026 e PROBAST | Versão antecipada de artigo aceito. Heterogeneidade clínica impede extrapolar para nosso contraste |

Já respondido em termos gerais — dados ausentes podem selecionar populações, indicadores podem transportar rotinas e discriminação não garante calibração. Em aberto neste projeto — magnitude e direção dos contrastes pareados para CRBBB com políticas explícitas de atendimento. Isso é uma pergunta local ainda não respondida por nossos dados, não prova de lacuna universal.

Resultados aparentemente divergentes podem decorrer de tarefas, mecanismos de ausência, populações ou métricas diferentes. Não comparar AUCs de artigos como competição direta.

Limitações da busca — revisão direcionada, sem dupla triagem, busca bibliográfica exaustiva ou extração integral de todos os suplementos. Acesso direto à Nature apresentou erro 500/redirecionamento de cookies. Usados trechos indexados, documentação oficial e código dos autores. PMC apresentou desafios de acesso na busca anterior. Resultados secundários de páginas reescritas não fundamentam conclusões. Preprints de transferência de sepse não foram tratados como evidência consolidada.
