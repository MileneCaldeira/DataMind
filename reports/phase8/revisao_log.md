
# Registro de execução da revisão
05/11/2026.

1. Leitura integral da v1, pareceres da Fase 7, protocolo/desenho da Fase 4, auditoria e fontes das Fases 5–6. Leitura do código de pré-processamento, limiar, métricas e bootstrap, sem executá-lo.
2. Snapshot: 125 arquivos únicos referenciados nos três manifestos anteriores, todos íntegros. V1 e figuras incluídos.
3. Leitura documental das medidas e aprofundamento de literatura; downloads novos em sources, separados dos dados brutos.
4. Revisão editorial por scripts/fase8_revise.py, criando v2. Inclusão dos controles existentes; nenhuma análise inferencial nova.
5. Primeiro verificador da revisão falhou por pressupor que scores_E1.csv tivesse apenas linhas atendidas. Inspeção mostrou 2.198 linhas, com campos vazios para 1.110 abstenções, correspondentes a predictions.csv. Corrigido apenas o novo verificador para distinguir número de linhas e probabilidades presentes. Não havia discrepância nos dados e nenhum artefato anterior foi modificado.
6. Verificação corrigida passou: hashes, 17 entradas brutas, IDs/join, pacientes separados, sete arquivos individuais de probabilidades, contagens e resultados da v2.
7. V2 relida integralmente. Figuras/tabelas preservadas e reconciliadas pelas fontes/hashes; nenhuma renderização ou predição nova. Todos os números experimentais permanecem os originais.
8. Resultado: revisão automatizada concluída; parecer humano independente segue necessário. Manifesto desta fase separado.

Ocorrências menores: busca inicial com glob PowerShell em argumentos rg falhou e foi refeita com filtro -g; tentativa de ler requirements.lock sem extensão falhou, arquivo correto requirements.lock.txt identificado e lido. Falhas de acesso bibliográfico estão documentadas em docs/fase8_originalidade.md. Não houve instalação de novas dependências nesta fase; verificação usa biblioteca padrão do ambiente existente.
