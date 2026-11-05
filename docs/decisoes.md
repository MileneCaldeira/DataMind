# Registro de decisões — 03/11/2026

1. **Escopo:** diagnóstico de acesso e qualidade; nenhuma modelagem, imputação, exclusão de registros ou estimação causal.
2. **Fontes:** arquivos diretamente hospedados na UCI, sem espelhos de procedência desconhecida. Três datasets completos pequenos, em vez de inferir viabilidade a partir de páginas de catálogo.
3. **Formato:** relatório Markdown e resultados JSON, para revisão e versionamento sem dependências de escritório.
4. **Ferramentas:** Python padrão, sem custo de nuvem ou GPU. Preservar bytes originais, URLs, status HTTP, SHA-256 e horários UTC; datas de interpretação em America/Sao_Paulo.
5. **Ausência:** contar apenas tokens explícitos `?`, vazio, `NA`, `NaN`, `nan`, `null`. Zeros suspeitos são sinalizados separadamente, sem conversão automática.
6. **Duplicidade:** contar excedentes de linhas idênticas, removendo apenas ID quando existente. Coincidência não identifica a mesma pessoa. Não deduplicar automaticamente.
7. **Normalização:** remover espaços nas extremidades; no Adult remover ponto final dos rótulos do arquivo de teste e ignorar a linha de comentário. Não modificar os arquivos originais. Não harmonizar categorias clínicas nesta etapa.
8. **Escolha provisória:** iniciar por qualidade de dados multicêntricos em saúde, com Heart Disease como piloto metodológico; condicionar tema definitivo à revisão e a uma segunda fonte de validação. Adult é alternativa fora da saúde, mas insuficiente sozinho para uma alegação de contribuição geral. Diabetes fica condicionado à proveniência/licença.
9. **Histórico:** MIMIC-IV/eICU são obstáculos relatados pela pesquisadora, não falhas reproduzidas nesta sessão. Não tentar contornar credenciamento.
10. **Git:** repositório inicialmente vazio e sem commits. Arquivos preparados para revisão; nenhum commit, push ou publicação realizado.

## Fase 2 — 03/11/2026

11. **Recomendação atual: reformular A**, ainda sem aprovação definitiva. Focar efeitos rastreáveis de regras sobre elegibilidade/composição e exigir benefício verificável frente a métodos existentes.
12. Preservar dados/scripts/referência da Fase 1. Reexecução offline confirmou resultados; análises novas isoladas em `scripts/phase2.py` e `reports/phase2/`.
13. Ler −9 numericamente nos brutos; manter zeros. Descartar bruto Cleveland da projeção por corrupção documentada. Não completar documentação clínica por inferência.
14. Diferenciar a explicação forense das transformações históricas das políticas de elegibilidade P0–P4. A primeira não substitui os processados nem prova identidade de pessoas.
15. P0–P4 são cenários exploratórios declarados; não imputar, deduplicar ou treinar ML. P2/P4 alteram o esquema exigido e não podem ser apresentados como a mesma regra de negócio.
16. PhysioNet 2019: candidato metodológico, não replicação clínica de Heart. Amostra de 12 arquivos por partição via ordenação de hashes; ambas as amostras já foram exploradas, sem positivos. Não concatenar granularidades.
17. Licença PhysioNet divergente entre catálogo CC BY e LICENSE ODbL: preservar as duas evidências e não redistribuir microdados. Acesso técnico da amostra confirmado, aprovação da segunda base pendente.
18. Revisão direcionada inclui trabalhos até outubro de 2026 e ferramentas existentes; não alegar novidade de harmonização, missingness ou dashboard de qualidade. Perguntas permanecem candidatas.
19. Migrar para C apenas com justificativa substantiva ou falha dos marcos de A; Adult sozinho não demonstrou vantagem de originalidade. ACS não foi baixado nesta fase.

## Consolidação da Fase 3 e protocolo da Fase 4 — 04/11/2026

20. Concluídas as quatro entregas documentais pendentes da Fase 3, preservando relatório de oportunidades, scripts, brutos e manifestos. A comparação favorece provisoriamente cobertura de medidas ECG. A/B/C da Fase 3 são novas alternativas, não os mesmos códigos das Fases 1–2.
21. Verificados offline os 17 arquivos da Fase 3. A auditoria de viabilidade consultou contagens de classes e disponibilidade no teste, sem previsões ou desempenho. Registrar essa exposição, sem alegar cegamento total.
22. Alvo candidato é presença de CRBBB em scp_codes. Não juntar IRBBB nem excluir confiança menor que 100. Painel de oito escolhido exploratoriamente antes do treino, sujeito à revisão clínica.
23. Separar E1/E2-C com mesma amostra de treino, E2 com amostra ampliada e E3 imputado. Contraste primário candidato é Brier E3 menos E2-fallback em toda a população de teste. Métricas condicionais e cobertura serão apresentadas separadamente.
24. Folds 1–8 para ajuste, 9 para limiares e 10 para teste interno reservado. Sem pós-calibração ajustada nesta versão. Reamostragem por paciente, estimando principal por exame.
25. Sem treinamento, instalação de pacotes, download repetido, GPU ou gastos. Aprovação da pergunta/desenho exigida explicitamente pela solicitação da Fase 4 antes de treinar. Protocolo ainda candidato, originalidade e utilidade clínica não demonstradas.

## Fase 5 — 04/11/2026

26. Autorização explícita da pesquisadora permite treinamento exploratório em 1–8 e avaliação/limiares em 9. Fold 10 permanece sem previsões. Emendas pré-treino registradas separadamente, preservando a Fase 4.
27. E3 versus E2-fallback compara estratégias operacionais. Não isola efeito causal da imputação. Mantidos E1/E2-C e E2-C/E2, além de controles C=1.
28. Ambiente isolado instalado e versões registradas. Apenas regressão logística L2 e prevalência constante. Ajuste de transformações e hiperparâmetros restrito ao desenvolvimento. Nenhum novo download de dados.
29. Realizados 160 ajustes CV, cinco finais de desenvolvimento e dois controles fixos. Sem avisos de convergência. OOF C=1 e OOF selecionado separados para explicitar otimismo de seleção. Limiar ajustado em 9 tem desempenho aparente nesse próprio conjunto.
30. No OOF selecionado, E3-I tem menor Brier entre políticas de cobertura integral. Em 9, E2-fallback tem menor Brier, e Δ E3−E2-fallback tem IC95% contendo zero. Não escolher vencedora definitiva nem alterar grade por resultado de 9.
31. 14 testes passaram, modelos recarregados reproduzem 9, partições/hashes reconciliados, fases anteriores preservadas. Congelar referência piloto, modelos e limiares. Nova autorização será necessária para avaliação final, com comando próprio separado do executor piloto.
32. Pergunta permanece pertinente como avaliação metodológica de reconhecimento de anotação. Não demonstrados originalidade, utilidade clínica, superioridade ou validação externa. Eventual expansão da grade ou mudança de codificação exige emenda explícita e novo congelamento antes do teste.
