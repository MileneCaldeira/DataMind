# Fase 4 — riscos e limites
| Risco | Controle e limite remanescente |
|---|---|
| Circularidade do alvo | CRBBB é anotado a partir do ECG e medidas de QRS reproduzem aspectos dos critérios morfológicos. É reconhecimento do padrão anotado. Não é previsão independente de doença futura nem demonstração de benefício clínico |
| Vazamento do laudo | Excluir qualquer código/diagnóstico/confiança/laudo da matriz de preditores. Medidas extraídas sem usar rótulo são preditores legítimos, mas a independência clínica do desfecho continua limitada |
| Pacientes repetidos | Folds disjuntos e bootstrap por paciente. Identidade depende dos IDs fornecidos, não verificação biométrica |
| Seleção de completos | C tem população distinta. Separar comparação pareada, cobertura e desempenho condicional |
| Confusão de treino e variáveis | Acrescentar E2-C. Comparar apenas E1 com E2 treinado em amostra maior não isolaria painel |
| Ausência estrutural | Uma onda pode não ser delineada. Imputação mediana é aproximação, não reconstrução verdadeira. Não assumir MCAR nem converter zeros |
| Rótulo imperfeito | Presença de CRBBB não é padrão-ouro externo. Confianças variam. Manter regra explícita e revisar clinicamente |
| Classe rara | 54 exames positivos de teste limitam calibração e subgrupos. IC largo não comprova equivalência |
| Uso prévio do teste | Disponibilidade e contagens consultadas antes do treino. Não afirmar cegamento total ou validação externa |
| Benchmark reutilizado | Conhecimento público e escolhas após exploração limitam confirmação independente. Replicação externa ainda necessária |
| Transporte | Dados históricos e equipamento/local associados. PTB-XL+ é derivação da mesma população. CODE tem outra referência, não réplica direta |
| Software e recursos | Treino ainda sem ambiente instalado/lock. Verificação de integridade não testa pipeline preditivo que ainda será implementado |
| Novidade | Comparar variáveis e imputar já são práticas publicadas. Contribuição candidata é decomposição de políticas e denominadores, sujeita à revisão |
| Generalização clínica | Maior cobertura pode incluir exames mais difíceis. Sem validação prospectiva/custo clínico, não afirmar segurança |

Antes de qualquer treino, aprovar pergunta, alvo e painel e revisar unidades. Antes de testar, congelar pipeline, limiares e análise, verificar inexistência de ajuste no fold 10 e registrar versões. Avaliação ética institucional aplicável deve ser definida pela equipe responsável. Não houve redistribuição de dados, inferência clínica individual ou contratação de recursos.
