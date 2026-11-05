# Fase 6 — limitações
Consolidação em 05/11/2026.

1. **Referência do alvo.** CRBBB é anotação produzida pela interpretação do mesmo ECG que fornece as medidas. Pode haver dependência dos critérios morfológicos. A ausência de variáveis do laudo nos preditores não transforma o alvo em padrão-ouro externo.
2. **Desenho operacional.** E3 versus E2-fallback muda variáveis e manejo da ausência ao mesmo tempo. Não identifica efeito causal da imputação.
3. **Precisão.** Há 54 exames positivos em 45 pacientes. O IC da diferença principal abrange efeitos em ambos os sentidos. Não foi fixada margem clínica de equivalência ou não inferioridade.
4. **Intervalos condicionais.** O bootstrap agrupa pacientes e mantém todos os seus exames. Considera os modelos como fixos, sem capturar seleção de hiperparâmetros ou variabilidade de um novo treinamento.
5. **Degenerescência na sensibilidade.** Todos os positivos observados foram identificados nos limiares congelados, dentro do suporte de cada modelo. O bootstrap só reamostra esses acertos e retorna [1;1]. Esse intervalo não prova sensibilidade perfeita fora da amostra. Não foi substituído por outro método escolhido após observar o teste.
6. **Calibração.** Algumas faixas têm poucos registros ou positivos. Intercepto e inclinação são diagnósticos amostrais. Nenhum calibrador foi ajustado para modificar as previsões finais. Média prevista próxima da prevalência não assegura calibração local.
7. **Fallback não exercitado.** E2-fallback coincide com E2 em 9 e 10. A política não foi avaliada sob falta frequente das oito medidas. No desenvolvimento só um exame acionava a regra alternativa.
8. **Seleção.** E1 atende apenas completos. A relação entre completude e positividade se inverte entre 9 e 10. Não generalizar uma direção de viés. Pessoas podem ter exames em ambos os estratos.
9. **Escolhas exploratórias anteriores.** O painel foi escolhido após análise de disponibilidade no desenvolvimento. As contagens estruturais do teste já tinham sido vistas na Fase 4. O desempenho do fold 9 influenciou a interpretação exploratória, mas hashes comprovam preservação do protocolo desde o congelamento. Não há cegamento total nem pré-registro externo.
10. **Multiplicidade.** Híbrida, indicadores, controles C=1 e estratos são secundários. Seus intervalos não foram corrigidos para múltiplas comparações. Um contraste secundário abaixo de zero não substitui a hipótese primária inconclusiva.
11. **Regularização e representação.** Os modelos completos escolheram o menor C da grade congelada. Não se demonstrou ótimo global. Algumas variáveis de morfologia/eixo foram tratadas numericamente. Nenhuma dessas decisões foi modificada pelo teste.
12. **Dependência da fonte.** PTB-XL+ deriva de PTB-XL. São a mesma população, não duas validações independentes. Dados históricos, equipamentos e protocolos específicos limitam transporte.
13. **Qualidade upstream.** A whitelist, unidades e integridade foram auditadas, mas a extração ECGDeli não foi reproduzida integralmente. Não houve nova adjudicação clínica independente dos rótulos.
14. **Comparação entre folds.** Ordenações diferentes e mudanças de prevalência não bastam para inferir data drift. Não foi feito teste causal ou formal de mudança entre populações.
15. **Rastreabilidade.** Logs mostram uma execução e arquivos de probabilidades consistentes. Não permitem garantir ausência de qualquer atividade fora do ambiente documentado.
16. **Originalidade.** O resultado é incremental. Comparar medidas e imputação já foi estudado. A revisão disponível é direcionada, sem inventário exaustivo de classificação seletiva e de todos os suplementos.

Nenhuma dessas limitações foi tratada por alteração posterior dos modelos. Elas delimitam a conclusão científica e precisam acompanhar qualquer apresentação.
