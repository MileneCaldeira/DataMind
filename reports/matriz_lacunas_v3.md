# Matriz priorizada de lacunas e ações

16/11/2026. Complementa o [parecer](parecer_cientifico_v3.md). P1 exige resolução ou limitação explícita antes de submissão. P2 melhora o relato e a auditabilidade. P3 é candidato a pesquisa futura. As prioridades representam julgamento desta revisão. Nenhuma linha representa comentário recebido de especialista.

|ID / prioridade|Lacuna e evidência|Risco e alcance|Ação recomendada / perfil necessário|Critério verificável de resolução|
|---|---|---|---|---|
|L01 P1|RR_Mean_Global→RRi_max e QRS_Dur_Global→QRSd_max; dicionário e v3|Interpretar agregação como medida clínica convencional sem comprovação|Consultar implementação/documentação do extrator; especialista ECGDeli e ECG|Definição, unidade, agregação e fonte, ou limitação explícita aceita pelos autores|
|L02 P1|Painel exploratório; Fase 4 e emendas|Justificativa retrospectiva de seleção, particularmente RR|Pesquisadora reconstruir razões efetivamente registradas e lacunas; especialista avaliar plausibilidade|Texto distingue motivo documentado, inferência posterior e conhecimento pendente|
|L03 P1|Alvo por chave CRBBB e medidas do mesmo sinal; pilot.py|Alegar diagnóstico independente ou confundir proximidade de construto com vazamento provado|Revisar descrição do alvo, negativos e rótulos com especialista ECG|Parecer sobre adequação ao reconhecimento de anotação e limites clínicos|
|L04 P1|45 pacientes positivos; IC de sensibilidade degenerado; metrics.json|Falsa certeza e subgrupos imprecisos|Bioestatístico avaliar estimando e interpretação; eventual proposta adicional separada|Parecer escrito e redação correspondente, sem inferência de perfeição populacional|
|L05 P1|Δ primário e IC incluem zero; primary.CI95|Declarar equivalência, efeito ausente ou vitória de outro braço|Manter interpretação de incerteza; pesquisadora explicar direções admissíveis|Conclusão coerente com o IC e distinção primária/secundária|
|L06 P1|Cobertura do teste já constava no protocolo Fase 4|Apresentar um número conhecido como descoberta confirmatória independente|Explicitar cronologia na discussão|Cronologia conferida e contribuição delimitada|
|L07 P1|Causas de NaN desconhecidas; MedianIndicators|Atribuir MAR/MCAR ou dizer que mediana recupera fisiologia|Revisar causas possíveis com extrator e textos de imputação|Pressupostos explicitados e mecanismo identificado como desconhecido|
|L08 P1|C selecionado em bordas, controles C distintos e OOF selecionado; Fase 5|Isolar efeito de imputação/painel sem desenho correspondente|Revisão metodológica dos contrastes existentes|Tabela de interpretação por contraste e ressalvas compreendidas|
|L09 P1|Documentação PTB-XL informa revisão humana em 9/10|Comparar folds como amostras com idêntica qualidade de rótulo|Explicar heterogeneidade documental e separar métricas ajustadas no fold 9|Texto com origem do fato e alcance da inferência|
|L10 P1|Literatura próxima já aborda imputação, medidas tabulares e seleção|Alegação de inovação baseada em combinação de termos|Pesquisadora e revisor científico confrontar estudos próximos|Frase de contribuição específica com sobreposições reconhecidas|
|L11 P2|Calibração com a/b livres e poucos eventos; evaluation.py|Confundir intercepto com calibração global ou média com calibração completa|Explicar ajuste e escassez de eventos; bioestatístico|Relato coerente com métodos e figuras existentes|
|L12 P2|E1 cobre subconjunto; pacientes podem estar em ambos os estratos|Ranking indevido e soma incorreta de pacientes|Conferir denominadores e sobreposição no texto|E1 separado da comparação integral e 130 pacientes compartilhados explicitados|
|L13 P2|Fallback zero no teste; final metrics|Generalizar desempenho a cenário onde painel falha|Delimitar evidência ao cenário observado|Ausência de uso efetivo do fallback destacada|
|L14 P2|V3 inicia com dois títulos; autoria e declarações pendentes|Dificuldade editorial e aparência de autoria institucional inexistente|Escolher título; confirmar contribuições e informações institucionais reais|Um título e declarações verificadas pelos autores|
|L15 P2|Checklist de relato parcial; acesso externo/licença pendentes|Confundir completude documental com prontidão de submissão|Usar mapeamento TRIPOD do parecer e confirmar informações institucionais|Itens aplicáveis resolvidos ou explicitamente limitados|
|L16 P2|Revisão humana ainda sem comentários registrados|Tratar revisão assistida como aprovação independente|Usar roteiros Fase 9 e matriz existente|Comentários reais com data, versão, resposta e responsável|
|L17 P3|Única população derivada, nenhuma avaliação externa|Generalização para hospitais e equipamentos|Avaliar futuro protocolo com equivalência de medidas e rótulo|Viabilidade e pergunta específicas antes de novo experimento|
|L18 P3|P_Morph/HA__Global numéricos e causas de ausência desconhecidas|Sensibilidade à representação e extrator|Discutir proposta de robustez apenas se mudar uma conclusão relevante|Justificativa e protocolo posterior identificados como tais|

## Questões que podem ser resolvidas por explicação

L05, L06, parte de L08–L09 e L11–L15 têm correções textuais apoiadas em evidência existente. L01–L04 e a interpretação clínica de L07 dependem de conhecimento especializado. L10 requer julgamento científico e aprofundamento focal de literatura, sem promessa de ineditismo. A v3 já contém várias ressalvas, mas sua presença não comprova que a pesquisadora consegue defendê-las ou que um especialista as considerou suficientes.

## Consequências para a conclusão

Não foi identificado nesta leitura um erro material comprovado que obrigue a descartar a comparação primária. L01 pode afetar a justificativa fisiológica e, se revelar erro material de medida, exigir reavaliação do escopo. L03, L04 e L17 restringem afirmações clínicas e de transporte. L06 e L10 restringem a contribuição reivindicada. A matriz distingue risco possível de falha demonstrada.

## Decisões da pesquisadora

Para cada ponto, registrar em suas palavras o que entendeu, qual alternativa considera defensável, que evidência usa e o que precisa perguntar. A aceitação de uma proposta não deve ser presumida a partir do silêncio. Usar a matriz de feedback da Fase 9 apenas para comentários efetivamente recebidos. Esta matriz de lacunas é um instrumento de planejamento, sem identificação de revisores fictícios.

Atualização editorial: a v4 corrige o título duplicado e identifica a pesquisadora responsável (parte de L14). Definições institucionais e revisão humana continuam pendentes. As demais lacunas não foram encerradas pela revisão de linguagem.
