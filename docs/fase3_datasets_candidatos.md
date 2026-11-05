# Fase 3 — dados e acesso efetivo
Consolidado em 04/11/2026. Evidência em [manifesto](../reports/phase3/entradas.json), [log de acesso](../reports/phase3/acesso.jsonl) e [auditoria](../reports/phase3/auditoria.json). São 17 arquivos em cache, verificados por SHA-256 na Fase 4. Nenhum download repetido.

| Fonte | O que foi realmente obtido | Adequação e limitações |
|---|---|---|
| [PTB-XL 1.0.3](https://physionet.org/content/ptb-xl/1.0.3/) | Metadados 6.594.879 bytes, dicionário, licença e 3 pares de sinais/cabeçalhos de desenvolvimento | 21.799 exames, 18.869 pacientes. Identificadores e folds permitem separar pessoas. Não se auditou todo o sinal bruto |
| [PTB-XL+ 1.0.1](https://physionet.org/content/ptb-xl-plus/1.0.1/) | ECGDeli 62.235.868 bytes, descrição de campos, licença | 531 medidas, correspondência integral por ecg_id. Mesmos exames de PTB-XL, não segunda população |
| [CODE-test](https://doi.org/10.5281/zenodo.3765780) | Metadados Zenodo e últimos 65.536 bytes do ZIP, HTTP 206. Anotações pequenas lidas integralmente com verificação CRC | 827 linhas. Sinal bruto não baixado. ZIP completo 218.189.452 bytes |
| [Escores CODE dos autores](https://github.com/antonior92/automatic-ecg-diagnosis/tree/403934867cea25a85b54faca025ac65b1ac18a45/dnn_predicts) | model.npy 19.976 bytes, README e licença, commit fixo | Matriz 827 × 6, probabilidades contínuas entre 0 e 1. Inferência original não reproduzida |
| [PhysioNet 2019](https://physionet.org/content/challenge-2019/1.0.0/) | Apenas cache da Fase 2, 24 arquivos e 866 horas | Sem positivos na amostra. Granularidade horária aninhada em permanência. Divergência documental de licença continua pendente |

PTB-XL/PTB-XL+ e CODE-test têm licença CC BY 4.0 declarada nas fontes. Código/escores do repositório CODE acompanham licença MIT. Conservar atribuições e versões. A licença de dados não resolve automaticamente a avaliação ética institucional.

No desenvolvimento PTB há 17.418 exames de 15.023 pacientes, 432 registros CRBBB em 370 pacientes. Exigir 531 campos completos mantém 8.874 exames e 212 positivos. O painel exploratório de oito campos mantém 17.417 e 432. Não há ecg_id duplicado ou sem correspondência. Há 2.111 pacientes com mais de um exame no total. Ausência de perfis textuais idênticos no desenvolvimento não prova ausência de sinais duplicados.

CODE-test tem 34 RBBB positivos. As duas leituras cardiológicas discordam da referência em 3 e 2 registros. A referência adjudicada depende dessas leituras. O README declara pacientes distintos, mas os CSVs não oferecem ID que permita verificação independente. dnn.csv contém decisões binárias, inadequadas para calibração contínua. A matriz model.npy foi obtida separadamente.

Tentativas malsucedidas — endpoint de conteúdo interno do ZIP Zenodo devolveu HTTP 403. Leitura parcial do arquivo público por HTTP Range funcionou, sem credenciais. Uma consulta Europe PMC não retornou o PMID pesquisado, consultado em PubMed. Não confundir essas falhas com impossibilidade de obter dados.

O download da tabela ECGDeli completa, aproximadamente 60 MiB, permitiu verificar cobertura de todos os exames sem baixar gigabytes de sinais. O experimento tabular não precisa de MATLAB para recalcular medidas. Dependências e recursos futuros estão no [protocolo da Fase 4](../reports/fase4_protocolo_cientifico.md).
