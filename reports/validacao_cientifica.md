# DataMind — validação científica da direção A

**03/11/2026 — America/Sao_Paulo. Recomendação: reformular A.** O acesso e a reprodução do piloto Heart Disease estão demonstrados. A direção ainda não está aprovada como tema definitivo: não foi identificada contribuição original suficientemente sustentada para “avaliar qualidade e comparabilidade multicêntrica” em termos genéricos.

A reformulação proposta é **avaliar o impacto de decisões semânticas e de elegibilidade, com proveniência explícita, na composição de coortes de benchmarks clínicos públicos**. Heart seria estudo exploratório de desenvolvimento, não validação clínica. A contribuição candidata deve ser comparada com métodos existentes e avaliada em dados ainda não usados para escolher regras. Não há razão científica demonstrada para migrar imediatamente a C: Adult tem limitações e saturação semelhantes.

## 1. Revisão crítica e reprodução da Fase 1

Foram relidos `viabilidade.md`, código e decisões; executados `python scripts/audit.py --offline` e `python scripts/verify.py`. **Os seis hashes e as oito visões de dados coincidiram com a referência inicial**, incluindo as contagens dos quatro centros. Scripts e dados da Fase 1 não foram modificados; sua referência em `reports/baseline/` foi preservada. A execução oficial atualiza somente suas saídas rotineiras e acrescenta entradas de cache ao log.

Os números da Fase 1 estavam corretos para os arquivos **processados** e para a definição declarada de ausência. As principais qualificações são:

1. A lista de tokens da Fase 1 não serve diretamente aos arquivos brutos de 76 atributos: estes usam −9.0, com variações de escrita. Isso não invalida a auditoria anterior, mas restringe seu alcance.
2. Os brutos contêm datas e identificação local/artificial; os processados não. A ausência de datas afirmada na Fase 1 deve ser lida como restrita aos processados. Isso não demonstra longitudinalidade utilizável.
3. O bruto de Cleveland tem corrupção documentada. Não é possível verificar sua projeção de 76 campos com o mesmo nível de confiança dos demais.
4. Os processados já incorporam recodificações compatíveis com supressão de categorias fora do dicionário; o alvo húngaro foi binarizado nessa versão. Uma auditoria apenas de `?` não observa toda a história da informação perdida.
5. “Quatro centros” significa quatro arquivos nomeados; a documentação suíça menciona Zurich/Basel. Não há como reconstruir separadamente todas as instituições ou confirmar independência entre pessoas.
6. A classificação de relevância como alta na Fase 1 era julgamento de potencial, não evidência de originalidade ou publicabilidade.

Fontes e rastreabilidade completas em [heart_documentacao.md](../docs/heart_documentacao.md); resultados em [heart_analysis.json](phase2/heart_analysis.json).

## 2. O que a documentação original permite afirmar

Foram examinados o dicionário de 76 atributos, o aviso de corrupção e as perguntas históricas ao doador. Há um [inventário dos 76 campos](../docs/atributos_heart76.md), com ausências dos três brutos estruturalmente legíveis e identificação dos 14 selecionados.

O alvo é status angiográfico, não evento futuro. A documentação geral sustenta comparar 0 a valores positivos; a descrição detalhada não resolve completamente os níveis 1–4 nem a fronteira exatamente em 50% de estreitamento. Não há fundamento para presumir uma escala de gravidade clínica. `ask-detrano` registra dúvidas sobre ordenação do alvo, protocolo e códigos de exames.

Uma transformação candidata — reconhecer −9, aplicar os domínios categóricos declarados e binarizar o alvo húngaro — reproduz os multiconjuntos processados de Hungria, Suíça e VA. Isso é **evidência de compatibilidade de uma transformação, não prova da cadeia histórica de ETL**. Não se fez vinculação de pessoas pela posição das linhas; os arquivos húngaro e suíço têm ordenações diferentes.

Os zeros de colesterol suíços e do VA já existem no bruto. Seu significado continua sem confirmação. Foram mantidos e sinalizados, não convertidos em ausência. `oldpeak` tem 11 valores negativos na Suíça e um no VA; não foram excluídos sem fundamento clínico. Domínio, plausibilidade e acurácia são coisas distintas.

## 3. Matriz de qualidade e políticas comparadas

A [matriz completa](../docs/matriz_qualidade.md) contém completude por centro/variável, alertas, distribuições, comparabilidade semântica, elegibilidade e composição por subgrupos. O JSON registra frequências de todos os campos, retidos/excluídos e números de linha para rastrear cada política.

As políticas são **cenários exploratórios documentados neste projeto**, inspirados em avaliação de completude/conformidade/plausibilidade e em harmonização orientada por esquema. Não são recomendações clínicas ou políticas copiadas de um artigo. Referências metodológicas: [Kahn](https://pubmed.ncbi.nlm.nih.gov/27713905/), [Schmidt](https://pubmed.ncbi.nlm.nih.gov/33810787/), [Maelstrom](https://mica.maelstrom-research.org/page/maelstrom-guidelines). Nenhuma fonte prescreve especificamente nosso núcleo de oito campos.

| Política | Regra e justificativa | Cleveland | Hungarian | Switzerland | VA | Total |
|---|---|---:|---:|---:|---:|---:|
| P0 | Preservar todos; referência descritiva | 303 | 294 | 123 | 200 | 920 |
| P1 | Exigir 14 campos completos, para quantificar custo da regra convencional de casos completos | 297 | 1 | 0 | 1 | 299 |
| P2 | Exigir `age, sex, cp, trestbps, chol, fbs, restecg, num`; cenário de menor escopo, sem medidas de exercício/imagem | 303 | 261 | 47 | 133 | 744 |
| P3 | P2 mais domínios categóricos e valores positivos de idade/pressão/colesterol; sensibilidade à plausibilidade mínima | 303 | 261 | 0 | 100 | 664 |
| P4 | P3 sem exigir colesterol; analisar custo de retirar uma variável problemática | 303 | 284 | 47 | 136 | 770 |

P2 não é “solução ótima”; foi definido depois da exploração inicial e precisa de justificativa em uma pergunta científica concreta. P3 exclui da elegibilidade uma linha com valor não positivo em campo exigido, **sem afirmar que zero é ausência e sem editar esse valor**. P4 muda a informação disponível e não pode sustentar a mesma análise que exige colesterol. Aumentar retenção não prova melhorar validade. P0 permite descrição por casos disponíveis com denominadores por variável; não produz uma matriz completa.

Não implementamos imputação, winsorização ou remoção de outliers por percentis: faltam pressupostos e validação clínica. Uma mediana imputada poderia apenas esconder uma coluna inteiramente inadequada em um centro. Deduplicação também não é justificada por coincidência de perfis. Não foi treinado nenhum modelo.

## 4. Seleção observada e possíveis vieses

**Entre centros:** Cleveland representa 32,93% dos registros em P0 e **99,33% em P1**. Esse contraste, já previsível pela Fase 1, mostra que a regra de completude quase elimina o caráter multicêntrico. Não é confirmação independente de hipótese.

**Contraste com esquema fixo P2→P3:** a retenção suíça cai de 47/123 (38,21%) para zero; no VA cai de 133/200 (66,5%) para 100/200 (50%). Cleveland e Hungria ficam iguais. O total perde 80 registros. Essa desigualdade decorre diretamente das regras e dos valores observados; não estima efeitos causais da qualidade da assistência.

**Composição interna:** na Suíça, P2 retém 46/115 registros com alvo positivo (40%) e 1/8 com alvo zero (12,5%); a proporção positiva passa de 93,50% a 97,87%. Também retém 3/10 registros de sexo 0 e 44/113 de sexo 1. No VA, P3 retém 5/6 de sexo 0 (83,33%) e 95/194 de sexo 1 (48,97%), enquanto a frequência positiva passa de 74,5% a 78%. Pequenos denominadores, sobretudo os seis registros de sexo 0 no VA, tornam esses contrastes instáveis para generalização.

Idade média suíça passa de 55,32 anos (P0) a 56,85 (P2); no VA, de 59,35 a 59,84 (P3). A matriz contém também todos os denominadores de retenção por idade ≥65 versus <65, alvo e sexo codificado. O limiar de 65 é estratificação exploratória explícita, não corte clínico validado.

Isso evidencia **mudança de composição da amostra disponível**, e é compatível com risco de seleção. Não identifica mecanismo MCAR/MAR/MNAR, não prova discriminação e não quantifica viés em relação a uma população-alvo externa desconhecida. Diferenças de medição, seleção original e caso clínico permanecem confundidas. O uso da expressão “viés de seleção” aqui é risco interpretativo, não estimativa causal obtida.

## 5. Segunda base: PhysioNet Challenge 2019

### Acesso, licença e tamanho

A [página oficial](https://physionet.org/content/challenge-2019/1.0.0/) descreve acesso aberto. O link histórico de download completo retornou **404** no navegador. A navegação pelo diretório oficial de arquivos funcionou sem login: foram obtidas listagens com 20.336 nomes PSV em A e 20.000 em B. Selecionamos os 12 menores hashes SHA-256 dos nomes em cada partição, regra fixada antes de ler valores. Todos os 24 downloads foram concluídos, totalizando **142.223 bytes de PSV**; com página, licença e listagens foram 28 GETs HTTP 200, 4.952.210 bytes. URLs finais, hashes e datas estão no [log](phase2/access_log.jsonl).

**Divergência documental:** o catálogo salvo anuncia CC BY 4.0, mas o [LICENSE.txt](https://physionet.org/files/challenge-2019/1.0.0/LICENSE.txt) efetivamente baixado contém ODC Open Database License (ODbL). Ambos foram preservados com hash. Não escolhemos silenciosamente uma licença. Acesso técnico está confirmado para a amostra; a licença aplicável a uma redistribuição/derivação precisa ser esclarecida junto ao mantenedor antes de publicar dados. Não foi enviada mensagem ao mantenedor. Os brutos permanecem locais e ignorados pelo Git.

Os 42 MB anunciados na página são tamanho declarado do pacote histórico, **não tamanho medido por download integral nesta fase**. Os tamanhos em bytes publicados nas listagens estão preservados; não foi feita ingestão completa nem benchmark de memória/tempo do conjunto integral. Os recursos locais identificados na Fase 1 e o processamento sequencial da amostra indicam viabilidade técnica provável, não prova de custo integral. Os 24 arquivos foram analisados sem GPU ou dependências externas.

### O que a amostra demonstrou

| Medida | A | B |
|---|---:|---:|
| Arquivos lidos | 12 | 12 |
| Linhas horárias lidas | 434 | 432 |
| Colunas | 41 | 41 |
| Comprimento mínimo–máximo por arquivo | 11–52 | 14–54 |
| Arquivos com algum `SepsisLabel=1` | 0 | 0 |
| Ausências `HR` / linhas | 44/434 | 37/432 |
| Ausências `Temp` / linhas | 272/434 | 334/432 |
| Ausências `EtCO2` / linhas | 434/434 | 370/432 |
| Arquivos com os 7 sinais escolhidos observados ao menos uma vez em `ICULOS<=24` | 11/12 | 12/12 |
| Arquivos com ao menos uma hora completa nesses mesmos 7 sinais e janela | 11/12 | 12/12 |

Sinais: HR, O2Sat, Temp, SBP, MAP, DBP, Resp; EtCO2 não faz parte desse cenário. Não foi exigida permanência de 24 horas. As duas definições de disponibilidade coincidiram em contagem nesta amostra; isso não demonstra equivalência geral. Em A, dois arquivos começam com ICULOS 4 e 2, portanto “primeiras 24 horas desde admissão” e “primeiras 24 linhas observadas” não são intercambiáveis. Resultados completos em [physionet_sample.json](phase2/physionet_sample.json).

A amostra determinística é de viabilidade, não desenho probabilístico para estimar frequências populacionais. A ausência de positivos limita a auditoria do desfecho e impede concluir sobre seleção por sepse. Não buscamos seletivamente arquivos positivos para melhorar a aparência dos resultados. O conjunto completo não foi avaliado.

### Adequação científica e independência

| Aspecto | Heart | Challenge 2019 | Consequência |
|---|---|---|---|
| Contexto | Investigação histórica de doença coronariana | Internação em UTI / sepse | Não replicam a mesma pergunta clínica |
| Unidade física | Registro estático de 14 campos | Linha horária dentro de arquivo | Não concatenar linhas nem usar horas como pessoas |
| Centro | Arquivo com identificação histórica | Partições A/B de sistemas hospitalares | Comparar separadamente; não presumir correspondência clínica com Heart |
| Alvo | Status angiográfico | Rótulo com antecipação de seis horas | Não harmonizar em um “alvo clínico” genérico |
| Ausência | `?` processado / −9 bruto | `NaN` em intervalos | Falta por hora não equivale a falta em toda internação |
| Variáveis parecidas | Frequência máxima de exercício e pressão em repouso | Frequência/pressão observadas em UTI | Mesmo nome/unidade não prova mesmo construto |
| Validação possível | Piloto de regras estáticas | Aplicabilidade de auditoria a medidas repetidas | Reutilizar princípios e rastreabilidade, não misturar os dados |

O recurso tem proveniência e finalidade distintas do Heart e é candidato independente em **origem de dataset**. Não foi demonstrada independência estatística entre pessoas de diferentes arquivos; não existe vinculação que a comprove aqui. Tampouco usar A para explorar e B para “confirmar” sem declarar o que já foi visto. As amostras de ambas já foram examinadas.

**Decisão sobre a segunda base:** candidata para testar aplicabilidade metodológica a outra granularidade, não escolhida como replicação clínica nem como validação confirmatória nesta fase. Requer esclarecimento de licença, auditoria integral, definição da janela e investigação do alvo. O terceiro sistema usado na avaliação original não foi obtido.

## 6. Literatura e contribuição identificável

A [revisão direcionada](../docs/revisao_literatura.md) prioriza revisões e métodos, inclui trabalhos de 2025 e outubro de 2026 e registra limites de leitura. A avaliação não se apoia apenas em artigos de classificação do Heart.

Já existem taxonomias, ferramentas automatizadas, diretrizes de harmonização, estudos de seleção por ausência e estudos de missingness no PhysioNet 2019. As revisões de Lewis, Hosseinzadeh e Kariuki apontam problemas de consistência/contexto de avaliação; isso **não demonstra um espaço inédito para qualquer novo dashboard**. Trabalhos recentes sobre transferência hospitalar e sensibilidade à imputação se sobrepõem a propostas genéricas de confiabilidade.

Uma contribuição candidata mais estreita seria avaliar se uma auditoria que vincula **regra → evidência semântica → ambiguidade → linhas elegíveis → mudança de composição** melhora a verificabilidade de decisões em relação a um comparador existente. Ainda não foi implementada uma avaliação desse benefício, escolhido um comparador justo ou demonstrada ausência de método equivalente.

As [três perguntas candidatas](../docs/perguntas_candidatas.md) especificam unidades, contrastes, hipóteses possíveis, avaliação e risco de sobreposição. Q1 é piloto exploratório; Q2 trata disponibilidade temporal; Q3 avalia o próprio processo de auditoria. Não há resultado confirmatório neste relatório.

## 7. Continuar A, reformular A ou migrar para C?

| Alternativa | Benefício | Custo/risco | Julgamento |
|---|---|---|---|
| Continuar A como inicialmente formulada | Mantém saúde e usa competência em dados | Formulação ampla, métodos conhecidos, Heart pequeno e histórico | Não aprovar como tema definitivo |
| **Reformular A** para impacto rastreável de regras sobre elegibilidade | Aproveita o piloto e permite contribuição avaliável sem começar por ML | Exige comparador, apoio clínico e validação em dados novos; licença da segunda base pendente | **Opção recomendada, condicionada** |
| Migrar para C com Adult | Acesso já validado; menor dependência de fisiologia | Fairness exige contexto social; benchmark saturado e histórico | Não demonstrou vantagem científica imediata |
| Migrar para C com ACS/Folktables | Potencial de variação temporal/geográfica | Acesso integral, recorte, licença e desenho amostral ainda não auditados neste projeto | Alternativa a investigar se A falhar nos critérios abaixo |

O esforço computacional não decide a escolha: o gargalo é a pergunta e sua avaliação. A migração para C faria sentido por interesse substantivo fora da saúde ou inviabilidade de apoio clínico/validação, não por supor que a mera troca de dataset cria novidade.

## 8. Critérios de avanço e o que não foi demonstrado

Antes de confirmar A, cumprir três marcos com resultados revisáveis:

1. **Contribuição:** matriz de comparação com métodos existentes e definição de um benefício verificável que não seja apenas “auditoria automatizada”. Revisar integralmente os estudos mais próximos e seus artefatos.
2. **Semântica e segunda base:** revisão das regras por alguém com conhecimento clínico; esclarecer a licença PhysioNet, obter/auditar o recorte completo escolhido e registrar granularidade, início de observação, seleção e alvo.
3. **Avaliação:** congelar protocolo antes de novos resultados; escolher comparador, unidades, métricas e critérios de interpretação. Reservar dados/tarefas ainda não explorados para avaliação, sem chamar o piloto conhecido de validação independente.

Se não houver benefício metodológico distinguível, não insistir em apresentar o piloto como inovação: enquadrá-lo como reprodução/metaciência aplicada ou avaliar C com novo recorte e pergunta específica. Nenhum dos marcos está automaticamente cumprido por este relatório.

**Ainda não demonstrado:** originalidade; utilidade clínica; acurácia contra prontuário/padrão-ouro; equivalência semântica entre centros; mecanismo de ausência; identificação de indivíduos únicos; viés causal de seleção; transportabilidade de modelos; superioridade de qualquer política; licença inequívoca da segunda base; auditoria integral do PhysioNet; validação independente das hipóteses. Nenhum modelo de ML foi treinado.

## 9. Falhas, fontes e reprodução

Falhas relevantes: link histórico PhysioNet 404, desafios de navegador em algumas páginas PMC, bruto Cleveland corrompido e divergência catálogo/licença. O navegador não conseguiu abrir o LICENSE redirecionado ao S3, mas o download Python **já havia sido concluído com HTTP 200** e seus bytes foram lidos. Uma inspeção manual do HTML com codificação Windows padrão falhou; repetida com UTF-8, confirmou a declaração CC BY no catálogo. Não foi uma falha do dataset ou do pipeline. Registro: [web_attempts.json](phase2/web_attempts.json), [access_log.jsonl](phase2/access_log.jsonl) e [fontes/limitações](../docs/fontes_limitacoes_fase2.md).

```powershell
python scripts/audit.py --offline
python scripts/verify.py
python scripts/phase2.py
python scripts/verify_phase2.py
```

`phase2.py` é offline por padrão. Para reconstruir seu cache numa cópia nova, `python scripts/phase2.py --download`; esse comando não substitui arquivos já presentes. Os originais da Fase 1 são obtidos pelos comandos já documentados no README. O manifesto da Fase 2 verifica entradas, código e saídas determinísticas; não atualiza sua referência automaticamente. Todos os brutos continuam fora do Git. Decisões foram acrescentadas ao registro sem apagar a Fase 1.
