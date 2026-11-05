
"""Editorial revision only; reads v1 and writes a distinct v2. No statistics/model calls."""
from pathlib import Path
r=Path(__file__).resolve().parents[1]
t=(r/"artigo/manuscrito_v1.md").read_text(encoding="utf-8")
t=t.replace("# Disponibilidade de medidas eletrocardiográficas e avaliação de classificadores da anotação de bloqueio completo do ramo direito","# Completude de medidas eletrocardiográficas, cobertura e avaliação de classificadores da anotação de bloqueio completo do ramo direito",1)
t=t.replace("**Versão 1, para revisão científica — 05/11/2026. Não submetido.**","**Versão 2 — revisão documental automatizada, 05/11/2026. Pronta para revisão especializada externa; não submetida nem clinicamente validada.**")
start=t.index("Títulos alternativos:");end=t.index("Autores, afiliações")
t=t[:start]+t[end:]
t=t.replace("Os resultados sustentam um estudo metodológico incremental, sem estabelecer utilidade clínica ou generalização externa.","A observação é contextual e não estabelece utilidade clínica ou generalização externa.",1)
anchor="### Desenho, dados e alvo"
intro="""A escolha de CRBBB foi pragmática e exploratória: uma anotação binária disponível, relacionada a características de condução ventricular e compatível com um piloto tabular de baixo custo. Não houve comparação prospectiva entre diagnósticos que demonstrasse ser o alvo mais relevante. A relação estreita com o QRS facilita a interpretação da tarefa, mas também restringe a novidade e a independência clínica.

CRBBB corresponde a bloqueio completo do ramo direito. Critérios eletrocardiográficos em adultos incluem QRS alargado e morfologia característica em derivações direitas e laterais [9]. Não aplicamos esses critérios para criar ou validar os rótulos. Trabalhos anteriores já examinam marcadores de bloqueios de ramo em bases que incluem PTB-XL [11]; reconhecer essa anotação não é, por si, contribuição nova.

"""
t=t.replace("## Metodologia",intro+"## Metodologia",1)
t=t.replace("As 531 colunas ECGDeli resumem medidas extraídas do sinal, incluindo estatísticas e contagens; não representam 531 quantidades fisiológicas independentes.","As 531 colunas ECGDeli correspondem à expansão de 177 medidas por mediana entre batimentos, intervalo interquartil e contagem de batimentos utilizados. Portanto, incluem características morfológicas e de disponibilidade, não 531 quantidades fisiológicas independentes. As contagens não são anotações diagnósticas, mas podem carregar informação sobre detecção de ondas.")
panel="""O dicionário harmonizado requer cautela: QRS_Dur_Global mapeia QRSd_max; RR_Mean_Global, embora descrito como intervalo RR médio, mapeia RRi_max. Mantivemos os valores distribuídos, sem reinterpretar RRi_max como média aritmética nem recalcular medidas. Os seis campos de V1/V6 mapeiam QRSd_X, RPa_X e SPa_X. As amplitudes já estão em mV; não aplicamos fatores de conversão de outros extratores. A equivalência com medidas clínicas convencionais permanece pendente de especialista. Não foram aplicados cortes clínicos de QRS aos valores globais.

"""
t=t.replace("### Partições e desenvolvimento",panel+"### Partições e desenvolvimento",1)
t=t.replace("As anotações derivam da interpretação do próprio ECG; não houve nova adjudicação clínica.","Segundo a documentação original, os registros foram adquiridos entre 1989 e 1996; laudos humanos ou automáticos foram convertidos em códigos SCP, com validação cardiológica em parte dos registros. Não houve nova adjudicação clínica neste estudo.")
t=t.replace("Regressões logísticas L2 utilizaram lbfgs e padronização aprendida no treino.","Regressões logísticas L2 utilizaram lbfgs, máximo de 3.000 iterações, tolerância 10⁻⁶ e semente 20261104. Medianas, médias e desvios foram aprendidos no treino. Colunas constantes foram preservadas com escala unitária; a regra congelada para coluna totalmente ausente era preenchimento zero, sem estimar parâmetros fora do treino. E3-I adicionou indicadores para todas as 531 colunas, inclusive quando constantes.")
t=t.replace("Os controles E1/E2-C distinguem conjuntos de variáveis na mesma população de treinamento; E2-C/E2 investigam mudança de treinamento.","Os controles E1/E2-C com C selecionado comparam estratégias com diferentes variáveis e regularizações, embora treinadas na mesma população. O controle adicional C=1 mantém o valor nominal da penalização, mas não iguala complexidade efetiva ou geometria entre painéis de dimensões distintas. E2-C/E2 investigam mudança de treinamento sob o mesmo painel; não se presume isolamento causal.")
t=t.replace("Brier é a média do erro quadrático entre probabilidade e alvo binário; menor é melhor.","Brier é a média do erro quadrático entre probabilidade e alvo binário; menor é melhor. Seu nível depende da prevalência e da composição. Reportamos B0, constante igual à prevalência do treino, e evitamos interpretar Brier pequeno como utilidade clínica. AP designa Average Precision, não integração trapezoidal da curva precisão–revocação.")
t=t.replace("A incerteza é condicional aos modelos treinados, sem refazer seu desenvolvimento.","A incerteza é condicional aos modelos, imputadores e limiares congelados, sem refazer desenvolvimento ou seleção do limiar. Os pacientes são tratados como unidades independentes de reamostragem; não há ajuste para dependência adicional por local ou aparelho.")
cal="""Calibração foi descrita nas faixas fixas [0; 0,02; 0,05; 0,10; 0,20; 1], e pelo ajuste diagnóstico logit Pr(Y=1) = a + b logit(p), com a e b estimados conjuntamente. Clipping em [10⁻⁶; 1−10⁻⁶] foi usado apenas nesse logit. O intercepto a não é calibration-in-the-large estimada com inclinação fixada em 1. Não há IC reportado para a e b; não foram usadas essas estimativas para corrigir probabilidades.

"""
t=t.replace("A Fase 6 gerou",cal+"A Fase 6 gerou",1)
t=t.replace("A Fase 7 somente leu agregados existentes para redação e figuras.","As Fases 7 e 8 utilizaram resultados existentes para redação, auditoria documental e figuras, sem nova inferência preditiva.")
t=t.replace("A idade mediana foi 62 e 64 anos, respectivamente, com as regras de valores indisponíveis da análise original.","A idade mediana entre valores abaixo de 90 anos foi 62 e 64 anos, respectivamente; valores elevados sujeitos à anonimização não entraram nesse resumo.")
t=t.replace("|E1, população completa|1.088|0,005830|0,998616|0,953360|\n","")
t=t.replace("Fonte: reports/phase6/final001/metrics.json, overall.","**Resultado em população restrita:** E1, nos 1.088 completos, teve Brier 0,005830, ROC-AUC 0,998616 e AP 0,953360. Esse resultado não pertence à ordenação da tabela de cobertura integral.\n\nFonte: reports/phase6/final001/metrics.json, overall.",1)
controls="""#### Controles secundários de treinamento e regularização
Os três contrastes abaixo utilizam os mesmos 1.088 exames completos. Foram previstos no protocolo; sua inclusão nesta versão corrige omissão de relato, sem realizar nova análise.

|Contraste secundário|ΔBrier|IC95% por paciente|
|---|---:|---|
|E1 − E2-C, C selecionado|−0,003409|[−0,006613; −0,000498]|
|E1_C1 − E2-C_C1, C=1|+0,000465|[−0,003872; +0,005073]|
|E2-C − E2|+0,000842|[−0,000126; +0,001830]|

Fonte: metrics.json, paired_secondary e bootstrap.paired_brier. O contraste ajustado E1/E2-C tem IC abaixo de zero, mas combina painel e regularização; o controle C=1 é inconclusivo. Não se conclui que a diferença seja causada pela penalização, nem que o painel completo seja superior em geral. Multiplicidade e incerteza impedem promover esse resultado à hipótese primária.

"""
t=t.replace("Nos completos, Brier",controls+"Nos completos, Brier",1)
t=t.replace("## Discussão","## Discussão",1)
t=t.replace("Estudos sobre dados ausentes demonstram a importância de alinhar desenvolvimento e aplicação [3,4].","Estudos sobre dados ausentes discutem alinhamento entre desenvolvimento, validação e aplicação [3,4,10]. O suplemento de Sisk diferencia calibração global com offset de inclinação e descreve condições em que indicadores e imputação mudam de desempenho. Não inferimos um mecanismo de ausência a partir de nossos resultados.")
t=t.replace("Nossa seleção por disponibilidade difere","O trabalho de Rueda et al. [11], cujo manuscrito público descreve exclusão de segmentos sem batimentos suficientes e imputação de parâmetros de batimentos, aproxima-se do tema disponibilidade em ECG. Entretanto, seus marcadores, regras, unidades de processamento e comparações de bloqueios diferem do contraste probabilístico aqui estudado. Não comparamos numericamente seus resultados aos nossos nem atribuímos à versão final detalhes não confirmados no texto público.\n\nNossa seleção por disponibilidade difere",1)
t=t.replace("O bootstrap não incorpora a variabilidade de todo o desenvolvimento e apresenta degeneração para sensibilidade.","O bootstrap não incorpora a variabilidade de todo o desenvolvimento e apresenta degeneração para sensibilidade. Não foram produzidos novos intervalos, testes de interação, métricas ou análises de poder após a revisão.")
t=t.replace("Variáveis codificadas numericamente e a interpretação clínica de algumas medidas globais exigem revisão especializada.","Os códigos P_Morph e HA__Global foram tratados numericamente, sem demonstrar adequação de sua ordem/distância. A interpretação clínica de QRSd_max e RRi_max exige revisão especializada. A auditoria da tabela não reexecutou a extração do sinal, nem exclui duplicação de sinais não investigada ou falhas upstream.")
t=t.replace("Arquivos vetoriais e PDF correspondentes disponíveis.","Para comunicação curta, priorizar fluxograma e contraste pareado; cobertura, calibração e composição podem permanecer como suplemento. Todos os materiais mantêm os valores da versão 1.\n\nArquivos vetoriais e PDF correspondentes disponíveis.",1)
t=t.replace("Repositório público/DOI de arquivamento: **pendente**.","Repositório público/DOI de arquivamento: **pendente**. Configuração: experiments/fase5.json; versões: reports/phase5/run001/environment.json e arquivo de dependências listado em freeze.json; entradas: reports/phase3/entradas.json; resultados: reports/phase6/final001/metrics.json; controle da revisão: scripts/fase8_verify.py. A reprodução da extração original depende de ECGDeli/MATLAB; a análise tabular reutiliza CSVs públicos. Licença dos dados não licencia automaticamente nosso código ou artigos de terceiros; a licença de distribuição do código precisa ser definida. Não executar novamente o preditor final no diretório preservado.")
t+= """
9. Surawicz B et al. AHA/ACCF/HRS recommendations for the standardization and interpretation of the electrocardiogram: part III: intraventricular conduction disturbances. J Am Coll Cardiol. 2009;53:976–981. https://doi.org/10.1016/j.jacc.2008.12.013
10. Hoogland J et al. Handling missing predictor values when validating and applying a prediction model to new patients. Statistics in Medicine. 2020;39:3591–3607. https://doi.org/10.1002/sim.8682
11. Rueda C et al. Compelling new electrocardiographic markers for automatic diagnosis. Computer Methods and Programs in Biomedicine. 2022;221:106807. https://doi.org/10.1016/j.cmpb.2022.106807. Métodos e apêndices consultados na versão pública https://arxiv.org/abs/2112.12196v2; equivalência integral à versão publicada não verificada.

## Pendências humanas antes de submissão
Cardiologista: semântica das medidas, validade do alvo e limites da interpretação. Bioestatístico: estimando, inferência condicionada, degeneração e interpretação dos controles. Pesquisador externo: originalidade e adequação editorial. Esta revisão automatizada não substitui pareceres independentes. Não há recomendação de uso clínico.
"""
# Keep bibliography contiguous.
t=t.replace("\nRelato orientado por TRIPOD+AI [8], ainda sem declaração de conformidade integral.\n","")
t=t.replace("## Pendências humanas antes de submissão","Relato orientado por TRIPOD+AI [8], ainda sem declaração de conformidade integral.\n\n## Pendências humanas antes de submissão")
t=t.replace("arquivo de dependências listado em freeze.json","reports/phase5/run001/requirements.lock.txt (Python 3.13.7; scikit-learn 1.9.1; NumPy 2.5.4; pandas 3.1.1; SciPy 1.18.1)")
t=t.replace("Estudo retrospectivo secundário do PTB-XL 1.0.3 e PTB-XL+ 1.0.1, distribuídos sob CC BY 4.0.","Estudo retrospectivo secundário do [PTB-XL 1.0.3](https://doi.org/10.13026/kfzx-aw45) e [PTB-XL+ 1.0.1](https://doi.org/10.13026/g6h6-7g88), distribuídos sob CC BY 4.0.")
(r/"artigo/manuscrito_v2.md").write_text(t,encoding="utf-8")
print("Created v2; v1 untouched.")
