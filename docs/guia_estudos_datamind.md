# Guia de estudos da pesquisadora — DataMind

Roteiro de aprendizagem associado ao estudo PTB-XL/PTB-XL+. Versão de 16/11/2026. Use cada módulo para produzir uma explicação própria e identificar dúvidas. As respostas-modelo são pontos de partida para estudo. A compreensão será demonstrada pela capacidade de justificar escolhas e reconhecer seus limites.

## 1. Pergunta, hipótese e contribuição

**Conceito.** A pergunta delimita o que se deseja saber. A hipótese especifica uma expectativa testável. A contribuição é o conhecimento que o trabalho efetivamente acrescenta.

**No DataMind.** A comparação principal pergunta se E3 tem menor Brier que E2-fallback nos mesmos exames. A hipótese previa vantagem de E3. O IC final admite vantagem e desvantagem. A contribuição candidata é a caracterização de políticas de disponibilidade e da incerteza nessa comparação.

**Para defender.** Explique a diferença entre ter uma hipótese plausível e obter suporte para ela. Um estudo pode ser informativo ao limitar o que se pode afirmar.

**Para o especialista.** Esta quantificação contextual acrescenta informação suficiente aos estudos próximos para o formato de publicação considerado?

**Exercício.** Escreva três frases separadas com pergunta, hipótese e conclusão. Confira se a conclusão usa apenas o que foi observado.

## 2. Unidade de análise e estimando

**Conceito.** Unidade de análise é o objeto contado. Estimando é a quantidade que se pretende estimar, com sua população e ponderação.

**No DataMind.** Há uma linha por ecg_id e exames repetidos por patient_id. O Brier principal dá peso igual a cada exame. Um paciente com mais exames contribui mais. O paciente é a unidade de separação entre folds e de reamostragem.

**Para defender.** O agrupamento corrige a abordagem da dependência, mas não muda automaticamente o peso de cada paciente na média.

**Para o bioestatístico.** A pergunta por exame é a mais adequada ao objetivo? Quais consequências tem a repetição de exames para a interpretação?

**Exercício.** Em uma tabela fictícia, Ana tem três exames e Bia tem um. Mostre quais linhas entram em COUNT(ecg_id) e COUNT(DISTINCT patient_id). Explique quem pesa mais na média por exame.

## 3. Anotação CRBBB e validade da referência

**Conceito.** O alvo supervisionado é a resposta usada no aprendizado. Sua qualidade e seu significado delimitam a tarefa.

**No DataMind.** O alvo é a presença da chave CRBBB em scp_codes. Ausência da chave identifica ausência da anotação. As medidas e a referência derivam do mesmo ECG. A classificação reconhece esse padrão anotado.

**Para defender.** Explique por que discriminar bem essa anotação não estabelece capacidade de prever eventos futuros ou benefício clínico. A proximidade entre medidas e referência também pode ajudar a entender AUC elevada.

**Para o especialista em ECG.** A referência é adequada à pergunta? Coanotações, origem automática e validação humana mudam sua interpretação?

**Exercício.** Descreva a variável-alvo como se estivesse documentando uma coluna no catálogo de dados, incluindo regra, fonte e limitação.

## 4. Seleção e significado das medidas

**Conceito.** Uma coluna numericamente válida pode ter significado diferente do sugerido pelo nome. Plausibilidade exige entender como a medida foi obtida.

**No DataMind.** O painel foi escolhido exploratoriamente. RR_Mean_Global corresponde a RRi_max e QRS_Dur_Global a QRSd_max no dicionário. Amplitudes usam mV e durações ms. As 531 colunas incluem resumos e contagens.

**Para defender.** Separe correspondência de nomes, unidade publicada e interpretação clínica confirmada. Explique a contribuição pretendida de cada campo apenas até onde houver evidência.

**Para o especialista.** Qual agregação define os campos globais? Como R, R′ e S são representados? Qual a razão clínica para RR no painel?

**Exercício.** Leia a tabela de oito medidas e marque cada definição como compreendida, parcialmente compreendida ou pendente. Registre a fonte usada.

## 5. Ausência de dados e imputação

**Conceito.** Imputar é aplicar uma regra para preencher valores ausentes. MCAR significa ausência independente dos dados, MAR admite dependência de valores observados e MNAR envolve dependência de valores não observados mesmo após considerar os observados.

**No DataMind.** A mediana de cada coluna foi estimada no treino. E3-I acrescentou indicadores. O mecanismo de ausência não foi identificado. NaN pode estar ligado a detecção de ondas, processamento ou características do sinal.

**Para defender.** A imputação fornece entradas para o modelo. Seu valor não deve ser tratado como medição recuperada do exame. O uso da mediana não demonstra MAR ou MCAR. Alterações do processo de ausência podem afetar o desempenho em outra população.

**Para o especialista.** Há medidas estruturalmente indefinidas? Contagens e códigos ajudam a distinguir falha de processamento e ausência fisiológica de onda?

**Exercício.** Relacione a operação a COALESCE em SQL, acrescentando a exigência de aprender a mediana apenas nas linhas de treino. Explique o que daria errado ao calcular a mediana no conjunto inteiro.

## 6. Regressão logística e regularização

**Conceito.** A regressão logística combina entradas ponderadas e transforma a soma em probabilidade entre zero e um. A penalização L2 limita coeficientes. C controla inversamente a força dessa penalização.

**No DataMind.** As entradas foram padronizadas com parâmetros de treino. O ajuste minimiza perda logística penalizada. O Brier fora do fold escolheu C. Os painéis amplos escolheram C=0,01, a borda inferior da grade.

**Para defender.** Diferencie função usada para ajustar pesos e métrica usada para selecionar configuração. A escolha na borda limita a afirmação de ótimo. Mesmo C em dois painéis não significa mesma complexidade efetiva.

**Para o revisor de ML.** Os controles sustentam a interpretação operacional? Que limitação decorre de códigos categóricos tratados como números?

**Exercício.** Explique por que 531 entradas podem aumentar informação disponível e também a dificuldade de estimação. Evite concluir antecipadamente qual painel deveria vencer.

## 7. Desenvolvimento, validação e teste

**Conceito.** Cada partição tem uma função. Usar resultados para tomar decisões faz parte do desenvolvimento, mesmo quando a tabela recebe o nome de validação.

**No DataMind.** Folds 1–8 foram usados para treino e seleção, 9 para limiares e interpretação exploratória, 10 para avaliação preditiva única. Pacientes foram separados. As contagens do teste já eram conhecidas no preflight. Os folds 9/10 têm revisão humana de rótulos documentada pela fonte.

**Para defender.** Explique que a avaliação é interna. A leitura prévia de contagens deve ser relatada. OOF usado para escolher C pode apresentar otimismo como diagnóstico do procedimento selecionado.

**Para o bioestatístico.** O histórico de seleção e a diferença na qualidade dos rótulos estão descritos com alcance adequado?

**Exercício.** Desenhe uma tabela com as decisões tomadas em cada fold e identifique qual resultado autorizou cada decisão registrada.

## 8. Brier, AUC, AP e calibração

**Conceito.** Brier é a média de (probabilidade − resposta)². AUC mede ordenação entre positivos e negativos. AP resume precisão ao recuperar positivos e depende da composição. Calibração avalia concordância entre probabilidades e frequências observadas.

**No DataMind.** Brier é a métrica principal, comparada ao B0. AUC/AP e calibração são secundárias. O ajuste de calibração estima intercepto e inclinação conjuntamente, com poucos eventos.

**Para defender.** Uma boa ordenação pode coexistir com probabilidades inadequadas. Brier pequeno precisa de contexto de prevalência e baseline. A diferença primária usa a mesma população.

**Para o bioestatístico.** Qual grau de interpretação é sustentável para os gráficos e os parâmetros de calibração com poucos positivos?

**Exercício fictício.** Para y=1, p=0,8 produz perda 0,04. Para y=0, a mesma probabilidade produz 0,64. Esses números apenas ilustram a fórmula e não são resultados do projeto.

## 9. Intervalo de confiança e bootstrap por paciente

**Conceito.** O intervalo depende de um procedimento de estimação e seus pressupostos. O bootstrap aproxima variação amostral reamostrando unidades observadas.

**No DataMind.** Foram 2.000 sorteios de pacientes, preservando seus exames e o pareamento dos comparadores. O intervalo de Δ vai de −0,002380 a +0,001133. Os modelos e limiares são tratados como congelados.

**Para defender.** O procedimento não inclui a variabilidade de repetir todo o desenvolvimento. O IC que cruza zero não prova igualdade. Em repetição idealizada do procedimento sob os pressupostos, intervalos de 95% teriam cobertura nominal de 95%. Isso não atribui 95% de probabilidade frequentista ao parâmetro fixo neste intervalo específico.

**Para o bioestatístico.** O método percentil e o agrupamento são adequados à precisão desejada e ao estimando por exame?

**Exercício.** Explique o sinal negativo e positivo do Δ. Diga quais conclusões o intervalo permite e quais exigiriam uma margem de equivalência definida previamente.

## 10. Sensibilidade, limiar e poucos positivos

**Conceito.** Sensibilidade é a proporção de positivos classificados como positivos. Especificidade usa os negativos. Ambas dependem do limiar.

**No DataMind.** O limiar foi escolhido no fold 9 para atingir especificidade empírica de pelo menos 95%. No teste, algumas estratégias acertaram todos os 54 exames positivos, de 45 pacientes. Reamostrar somente esses acertos produziu intervalo [1;1].

**Para defender.** O bootstrap observado não cria falsos negativos que não existem na amostra. Esse intervalo degenerado não demonstra certeza sobre novos pacientes. Métricas do fold 9 no limiar escolhido nele são aparentes.

**Para o bioestatístico.** Como apresentar a incerteza sem ignorar repetição de exames ou introduzir uma análise oportunista?

**Exercício.** Aponte no manuscrito a amostra que sustenta a sensibilidade e a limitação que deve acompanhar o número.

## 11. Cobertura, seleção e causalidade

**Conceito.** Cobertura descreve a fração atendida. Uma regra de elegibilidade muda quem entra no denominador. Uma comparação causal exigiria um desenho e pressupostos que isolassem o efeito de interesse.

**No DataMind.** Completude de 531 medidas atende 49,50% dos exames e 64,81% dos positivos. E3/E2-fallback muda painel e tratamento de ausência. O fallback teve zero acionamentos no teste. A cobertura já estava no preflight.

**Para defender.** E1 e os modelos integrais representam populações diferentes. Nos mesmos exames, o contraste compara estratégias, sem identificar o efeito isolado da imputação. A caracterização da cobertura não é descoberta independente posterior ao teste.

**Para o revisor.** O estimando e a descrição da composição deixam claros os limites da comparação?

**Exercício.** Imagine um WHERE exigindo todas as colunas preenchidas. Explique por que o dashboard gerado depois desse filtro representa outra população.

## 12. Autoria, contribuição e publicação

**Conceito.** Autoria envolve contribuição real, responsabilidade e concordância. Uma contribuição incremental pode ser científica se pergunta, método, evidências e limites estiverem claros.

**No DataMind.** O resultado primário é inconclusivo. Há um caso auditável de comparação de estratégias. A originalidade específica e a adequação editorial dependem de revisão. Ferramentas computacionais apoiaram o trabalho e sua proveniência está registrada.

**Para defender.** Reconstrua quais decisões adotou, o que compreende e quais questões ainda estão abertas. Uma justificativa formulada agora deve ser identificada como interpretação atual quando não estava registrada antes.

**Para o pesquisador experiente.** O estudo justifica trabalho curto ou artigo empírico conciso? Que sobreposição com a literatura precisa ser explicada? Quais declarações e contribuições devem ser confirmadas?

**Exercício.** Produza um resumo em suas palavras, sem consultar o manuscrito, com pergunta, métodos, resultado e limitação principal. Depois confronte com as fontes.

## Leituras associadas e uso

Comece pelos documentos do próprio projeto para ligar conceitos a decisões concretas. O parecer atual reúne referências verificadas sobre imputação, calibração, benchmarks e relato. O guia anterior oferece perguntas de defesa complementares. A leitura pode seguir o cronograma existente.

- [Parecer científico e fontes](../reports/parecer_cientifico_v3.md)
- [Plano de evolução integrado](plano_evolucao_cientifica.md)
- [Emendas pré-treino](fase5_emendas_pre_treino.md)
- [Guia anterior de defesa](guia_defesa_pesquisa.md)

## Como reconhecer progresso

Ao final de cada semana, explique uma decisão por três minutos e registre a fonte que sustenta sua explicação. Distingua o que consegue demonstrar, o que é uma interpretação plausível e o que depende de parecer. Registre dúvidas sem tentar preenchê-las com vocabulário técnico. O objetivo é compreender e assumir as decisões científicas do projeto.
