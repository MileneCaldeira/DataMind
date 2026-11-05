
# Guia para compreender e defender a pesquisa
Versão de 05/11/2026. Use como apoio; não substitui compreensão dos métodos nem revisão por especialistas.

## A pesquisa em linguagem simples
O problema não é apenas “qual modelo acerta mais?”. Antes disso, precisamos perguntar: **em quais exames ele consegue funcionar e em quais exames foi avaliado?** Um modelo que exige todas as medidas pode deixar muitos exames de fora. Se avaliarmos cada modelo em um grupo diferente, a comparação pode favorecer um deles por causa da população, não do algoritmo.

Escolhemos ECG porque havia dados públicos acessíveis e medidas prontas para análise tabular. Isso permitiu um estudo reproduzível compatível com experiência em dados/SQL e desenvolvimento em estatística/Python. Essa conveniência não demonstra que ECG seja o tema de maior relevância clínica. O PTB-XL+ fornece medidas dos mesmos exames PTB-XL: não é uma segunda validação independente.

CRBBB é a sigla inglesa para bloqueio completo do ramo direito, um padrão de alteração da condução elétrica ventricular. O diagnóstico eletrocardiográfico envolve duração e forma das ondas. Nosso estudo não diagnosticou pacientes: tentou reconhecer uma anotação já presente na base. A anotação foi feita a partir do próprio ECG, por isso medidas desse sinal podem estar muito próximas dos critérios usados para rotulá-lo.

## Como os modelos funcionam
A regressão logística combina medidas com pesos aprendidos no treinamento e converte o resultado em uma probabilidade entre zero e um. A penalização L2 limita a magnitude dos pesos e ajuda a controlar ajustes excessivos. Não torna o modelo automaticamente válido ou causal.

Escolhemos uma família simples e auditável porque a pergunta é sobre disponibilidade e avaliação, não sobre criar um algoritmo. Mais complexidade não resolveria a falta de validação externa ou a incerteza do rótulo.

E1 usa todas as 531 medidas e só atende exames completos. E2 usa oito medidas. E2-fallback usaria a prevalência do treino caso faltasse alguma das oito. E3 preenche medidas ausentes com medianas aprendidas no treino. E3-I também informa quais campos estavam ausentes. A híbrida usa E1 quando possível, E2 no restante elegível e baseline se necessário. **No teste, o fallback não precisou ser usado.**

As 531 colunas incluem medianas, dispersões e contagens de batimentos; não são 531 informações fisiológicas independentes. Oito medidas não significam oito critérios diagnósticos validados. Há uma ambiguidade documental importante: RR_Mean_Global corresponde a RRi_max, que exige esclarecimento especializado.

## Como avaliamos
Folds 1–8 foram usados para desenvolver os modelos; fold 9 escolheu limiares; fold 10 foi reservado para uma execução preditiva final. O mesmo paciente não aparece em duas dessas partições. Um paciente pode ter vários exames.

Brier Score é a média de (probabilidade prevista − resultado observado)². Quanto menor, menor o erro probabilístico. Em uma condição rara, prever probabilidades pequenas para todos já pode produzir Brier baixo; por isso mostramos o baseline B0. Brier não é porcentagem de acerto.

O contraste principal é Brier(E3) menos Brier(E2-fallback), nos mesmos exames. Valor negativo favorece E3. A estimativa foi −0,000613, com IC95% de −0,002380 a +0,001133. O intervalo atravessa zero: os dados não distinguem com a precisão exigida qual estratégia tem menor erro. Isso não prova que sejam iguais.

O IC foi obtido reamostrando pacientes e carregando seus exames juntos, respeitando a repetição. Em termos frequencistas, o procedimento busca produzir intervalos que cubram o parâmetro em 95% de repetições sob suas condições; não significa que 95% dos exames estejam nesse intervalo ou que haja 95% de probabilidade atribuída ao parâmetro fixo. O cálculo considera os modelos já treinados e não toda a variação possível de um novo desenvolvimento.

## O que efetivamente descobrimos
No teste havia 2.198 exames de 1.904 pacientes; 54 exames positivos pertenciam a 45 pacientes. Exigir todas as medidas deixou utilizáveis 49,50% dos exames e 64,81% dos positivos. Portanto, positivos foram proporcionalmente menos excluídos que a população geral nesse teste. No fold 9 a direção da seleção era diferente.

E2-fallback teve Brier 0,006655; E3, 0,006042. A híbrida teve o menor valor pontual integral, 0,005384, mas esse resultado é secundário. Não demonstramos superioridade definitiva de qualquer estratégia. O resultado mais defensável é a importância de explicitar cobertura e denominadores neste caso concreto.

## Dez perguntas difíceis
1. **“A hipótese falhou; a pesquisa não serve?”**  
Não houve suporte à superioridade de E3. Um resultado inconclusivo continua informativo se a pergunta, a incerteza e as limitações forem relatadas. Não devemos trocar a hipótese por uma secundária mais favorável.

2. **“Vocês provaram que oito medidas são suficientes?”**  
Não. O painel estava disponível em todos os exames do teste e teve desempenho numericamente competitivo. Não houve teste de equivalência, margem definida ou validação externa.

3. **“Por que usar CRBBB?”**  
Foi um caso exploratório acessível e relacionado a medidas de condução. Não demonstramos ser o melhor alvo clínico. A proximidade com medidas do QRS limita a novidade de reconhecer essa anotação.

4. **“A AUC quase perfeita significa diagnóstico confiável?”**  
Não. AUC mede ordenação entre anotações positivas e negativas nesta amostra. O alvo vem da interpretação do mesmo ECG; não há padrão-ouro independente, benefício clínico demonstrado ou validação em outro serviço.

5. **“Sensibilidade de 100% com IC [100%;100%] não é certeza?”**  
Não. Todos os positivos observados foram acertados nos limiares congelados. Reamostrar apenas esses acertos nunca cria um falso negativo. Há só 45 pacientes positivos; o intervalo empírico é degenerado.

6. **“A imputação melhorou o modelo?”**  
Não isolamos esse efeito. E3 usa 531 colunas e E2-fallback usa oito; também muda a estratégia de treinamento. A diferença primária é operacional, inconclusiva e não causal.

7. **“Por que não escolher a híbrida, que teve menor Brier?”**  
É o menor valor pontual entre estratégias integrais, mas secundário. Seu IC de diferença para E2-fallback também inclui zero. Escolhê-la como vencedora após olhar o teste seria exagerar a evidência.

8. **“O controle de variáveis realmente controla tudo?”**  
Não. E1/E2-C com ajuste selecionaram C diferentes. O controle C=1 foi incluído e é inconclusivo; o mesmo C nominal também não garante a mesma complexidade efetiva em painéis diferentes.

9. **“Qual é a contribuição se seleção e imputação já são conhecidas?”**  
Uma demonstração empírica e reproduzível, para este recurso/target, de cobertura, composição e contraste pareado com resultado inconclusivo. Não é nova teoria nem algoritmo. O interesse editorial precisa ser avaliado externamente.

10. **“O que falta antes de publicar?”**  
Revisão clínica do alvo e das medidas, revisão bioestatística e de originalidade, declarações institucionais e pacote público reproduzível. Para afirmar generalização, seria necessária validação externa planejada; não é preciso treinar novos modelos apenas para melhorar a narrativa.

## Frase curta para apresentação
“Estudamos como a exigência de medidas completas muda quem é avaliado. No teste, ela excluiu cerca de metade dos exames; comparar estratégias na mesma população não mostrou vantagem estatisticamente sustentada das 531 medidas imputadas sobre o painel reduzido.”

Fontes: artigo/manuscrito_v2.md, reports/fase8_auditoria_estatistica.md e reports/fase8_pendencias_especialistas.md. Para detalhes clínicos, consultar as referências e o especialista, não transformar este guia em orientação diagnóstica.
