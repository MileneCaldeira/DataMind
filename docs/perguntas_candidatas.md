# Perguntas científicas candidatas — decisão ainda aberta

03/11/2026. Nenhuma pergunta abaixo tem originalidade estabelecida. Resultados do Heart já foram explorados e não podem virar confirmação independente por receberem um novo nome ou hipótese depois da análise. Reamostrar o mesmo benchmark não cria validação externa.

## Q1 — Como decisões semânticas mudam a coorte, além do que informa a completude?

**Pergunta:** mantendo um esquema de variáveis fixo, quanto a adição de regras de conformidade/plausibilidade documentadas modifica retenção por centro e composição de registros em relação a considerar somente ausência explícita?

- Unidade: registro dentro de cada centro; esquema fixo de oito campos para o contraste P2↔P3. P1↔P2 e P3↔P4 são análises de escopo, não o mesmo contraste, pois mudam as variáveis exigidas.
- Quantidades: diferença de retenção em pontos percentuais por centro; mudança da participação dos centros; diferença de frequência do alvo e sexo codificado; distribuição de idade dos retidos e excluídos. Relatar contagens e denominadores e sobreposição das listas de linhas elegíveis.
- Hipótese candidata para dados ainda não examinados: regras semânticas alteram a elegibilidade diferencialmente por centro. A igualdade de retenção seria uma referência nula; efeitos devem ser relatados mesmo se pequenos ou nulos, sem selecionar políticas após observar resultados.
- Testabilidade: alta no Heart, mas resultado atual é apenas exploratório. Para inferência futura, pré-especificar família de regras, estimando e limiar de relevância com justificativa; usar base independente e incerteza respeitando unidade de amostragem, se essa unidade puder ser estabelecida. Não há justificativa para p-valores tratando os quatro centros como amostra aleatória de hospitais.
- Originalidade: **baixa como pergunta genérica**; casos completos e seleção são conhecidos. Contribuição possível seria avaliação comparativa de um relatório rastreável frente a uma abordagem existente, com benefício mensurável de identificação/explicação de decisões, e não apenas mais uma contagem de ausentes.
- Critério de descarte: se for apenas aplicação de regras conhecidas sem ganho de avaliação, enquadrar como estudo de reprodução ou material de ensino, não como novo método.

## Q2 — Quanto a definição temporal de disponibilidade altera elegibilidade em dois sistemas de UTI?

**Pergunta:** para um conjunto fixo de sinais vitais, exigir disponibilidade simultânea em uma hora e exigir ao menos uma observação de cada variável em uma janela produz coortes diferentes nos sistemas A e B do PhysioNet 2019?

- Unidade primária proposta: arquivo/registro de internação disponibilizado; a fonte o descreve como sujeito, mas não demonstramos unicidade de pessoas entre arquivos. Horas são medidas repetidas dentro do arquivo, não observações independentes.
- Desenho candidato: janelas de 6, 12 e 24 horas **a partir do início do registro disponibilizado**, com análise separada por `ICULOS` para distinguir início observado de admissão à UTI; esclarecer truncamento antes de congelar protocolo. Comparar definições de disponibilidade com igual conjunto de variáveis e mesma janela. Definir previamente tratamento de registros curtos; exigir 24 horas exclui altas/óbitos/transferências precoces e pode selecionar duração de permanência.
- Desfechos da auditoria: retenção, composição etária/sexo, duração observada e proporção de arquivos com algum rótulo positivo; esta última é descritiva e retrospectiva. O `SepsisLabel` é antecipado seis horas, portanto não representa simplesmente “sepse presente agora”. Não usar medidas futuras para caracterizar disponibilidade passada.
- Evidência atual: apenas 12 arquivos por sistema inspecionados; nenhum positivo. A comparação exploratória `ICULOS<=24` implementada na Fase 2 não confirma esta pergunta e não equivale necessariamente a primeiras 24 horas observadas.
- Originalidade: **incerta e sobreposição relevante** com missingness informativa, seleção temporal e trabalhos de 2021/2026. O efeito de missingness em modelos já foi estudado. Revisar esses protocolos integralmente antes de reivindicar contribuição por uma nova parametrização de janela.
- Testabilidade: condicionada a download completo, investigação de início de observação, revisão clínica e disponibilidade de eventos. Não juntar estes arquivos com Heart nem chamar o resultado de replicação clínica da doença coronariana.

## Q3 — Uma auditoria com proveniência torna decisões mais verificáveis que um relatório de qualidade convencional?

**Pergunta:** anexar a cada regra sua fonte, escopo, ambiguidade e impacto na elegibilidade melhora a capacidade de revisores reproduzirem e justificarem decisões frente a um relatório contendo apenas completude, domínios e distribuições?

- Objeto: protocolo/relatório e tarefas de revisão, não predição clínica. Definir comparador a partir de ferramentas e frameworks existentes (OHDSI/dataquieR/Maelstrom), sem alegar que não documentam proveniência.
- Avaliação proposta: tarefas pré-especificadas de identificar alteração de alvo, denominador incorreto, domínio não documentado e perda de centro; referência adjudicada por especialistas independentes. Medir acertos, decisões justificáveis e tempo, com ordem aleatorizada ou contrabalançada. Testes controlados com erros inseridos devem ser claramente rotulados como simulação, além de casos reais.
- Hipótese candidata: o protocolo aumenta decisões corretamente justificadas sem aumento desproporcional de esforço. Definir o que é acerto, esforço aceitável e tamanho amostral antes do estudo. Nenhum participante foi recrutado e nenhuma avaliação foi conduzida.
- Originalidade: potencialmente mais identificável do que Q1 isolada, porém **não demonstrada**; documentação rastreável já é exigida em harmonização. Pode ser reformulação de práticas existentes, não novo método.
- Limites: exige comparação justa, expertise clínica, protocolo de avaliação e avaliação ética institucional se envolver participantes. Não inferir melhor segurança clínica de melhor desempenho em uma tarefa documental.

## Prioridade proposta

Usar **Q1 como piloto exploratório**, Q3 como possível eixo metodológico somente após revisão de sobreposição, e Q2 como avaliação de aplicabilidade em uma segunda granularidade, se fizer sentido para a pergunta final. Não transformar as três em um projeto excessivamente amplo. A condição mínima para avançar é uma pergunta/estimando claro, comparador existente e avaliação que possa falhar; simplesmente construir um dashboard não basta.
