# Fase 5 — implementação e treinamento piloto
04/11/2026. Execução concluída em CPU, sem previsões no fold 10.

## O que foi implementado
Baseline B0 de prevalência, regressões logísticas L2 E1, E2-C, E2, E3 e E3-I, composição E2-fallback e híbrida. E1/E2-C compartilham exatamente os exames de treinamento completos. E2 usa o painel em todos os elegíveis. E3/E3-I usam todos os exames. Dois controles adicionais mantêm C=1 para E1/E2-C.

Emendas registradas antes do treino em [fase5_emendas_pre_treino.md](../docs/fase5_emendas_pre_treino.md). O contraste principal foi preservado e interpretado como comparação operacional, sem efeito causal isolado da imputação.

Nenhum identificador ou informação de laudo entrou nos preditores. As 531 colunas correspondem exatamente à expansão do dicionário ECGDeli, incluindo medianas, IQRs e contagens. A auditoria de origem e suas limitações estão em [fase5_auditoria_leakage.md](../docs/fase5_auditoria_leakage.md).

## Execução e ambiente
Ambiente isolado .venv-phase5, Python 3.13.7, scikit-learn 1.9.1, numpy 2.5.4, pandas 3.1.1, scipy 1.18.1. Dependências transitivas e versões exatas preservadas em [requirements.lock.txt](phase5/run001/requirements.lock.txt).

Foram 160 ajustes de validação cruzada, cinco ajustes finais em 1–8 e dois controles C=1. Tempo do executor de treinamento, incluindo auditoria e gravação, 175,7 segundos. Pico de working set 748.986.368 bytes, aproximadamente 714 MiB. Uma thread BLAS, sem GPU. A avaliação/bootstrap é etapa separada desse tempo.

Nenhum aviso de convergência, máximo de 624 iterações, limite 3.000. Duas colunas constantes nos braços completos foram preservadas com escala 1. Os indicadores introduzem outras colunas constantes, documentadas por ajuste. Nenhuma coluna inteiramente ausente nos treinos reais exigiu o fallback zero, mas esse caso está testado.

No scikit-learn 1.9.1, l1_ratio=0,0 corresponde à penalização L2, com solver lbfgs. Os parâmetros completos estão nos modelos serializados. A configuração não usou L1, elastic net ou pesos de classe.

C selecionado por Brier OOF em 1–8 foi 0,01 para E1/E3/E3-I e 10 para E2-C/E2. Não se usou desempenho de 9 para escolher C. OOF com C selecionado permanece diagnóstico com possível otimismo de seleção. OOF C=1 e avaliação de probabilidades em 9 são apresentados separadamente.

## Integridade e reprodução
14 testes automatizados passaram. Reconciliados os IDs de treino/avaliação dos 160 ajustes. Modelos recarregados reproduziram probabilidades de 9 com tolerância 1e-12. Verificados os hashes dos dados e a reprodução das Fases 1–2. Os artefatos anteriores permanecem preservados.

Ocorrências corrigidas — leitura inicial do dicionário com BOM exigiu utf-8-sig. Um aviso de dtype do pandas foi resolvido com leitura textual explícita antes do treino. Na revisão final, o verificador sinalizou a atualização autorizada de docs/decisoes.md porque comparava separadores de caminho Windows com barra normal. A normalização foi corrigida e a verificação repetida. Não foi necessário refazer nenhum treinamento.

A guarda rejeita fold 9/10 no ajuste e fold 10 nas previsões, além de pacientes já vistos no treino. O loader só monta a matriz de modelagem para 1–9. Fold 10 participa apenas de verificação estrutural de IDs/folds e hashes do arquivo original. Não houve avaliação preditiva do teste.

Executar da raiz para verificar a execução preservada

```powershell
.venv-phase5/Scripts/python scripts/fase5_verify.py
```

Para reproduzir treinamento em cópia separada do projeto, com reports/phase5/run001 ainda inexistente

```powershell
python -m venv .venv-phase5
.venv-phase5/Scripts/python -m pip install -r CAMINHO_DO_LOCK_PRESERVADO
.venv-phase5/Scripts/python -m unittest discover -s tests -v
.venv-phase5/Scripts/python scripts/fase5_train.py
.venv-phase5/Scripts/python scripts/fase5_evaluate.py
.venv-phase5/Scripts/python scripts/fase5_reports.py
.venv-phase5/Scripts/python scripts/fase5_verify.py
```

O executor recusa sobrescrever run001. Não apagar a execução original para reproduzir. Copiar o lock para a nova cópia antes da instalação. Modelos estão em phase5/run001/models, incluindo B0 e os controles. Estratégias compostas usam os mesmos modelos, sem novo treinamento. Logs registram cada ajuste, semente, IDs por hash, duração, iterações e memória. CSVs guardam todas as previsões fora do treino, incluindo a grade completa.

A avaliação e seus relatórios podem ser regenerados sem treino. A verificação gera logs novamente e pode mudar hashes de arquivos de log por duração. Para validar uma entrega congelada sem modificá-la, usar scripts/fase5_freeze.py --check.

## Congelamento e decisão
O manifesto freeze.json referencia protocolo original, emendas, configuração, scripts, testes, dependências, modelos, limiares e resultados. A avaliação final não está implementada como opção deste executor, que rejeita fold 10. Será necessário um comando específico autorizado, mantendo intacta a referência piloto.

O contraste está tecnicamente pronto para uma avaliação final única do protocolo congelado, após nova autorização. Não recomendamos ampliar modelos ou alterar regras para perseguir o desempenho de 9. Se a equipe optar por ampliar a grade de regularização, fazê-lo como nova emenda de desenvolvimento e novo congelamento antes de abrir o teste.

[Resultados](fase5_resultados_validacao.md) · [Limitações](../docs/fase5_limitacoes.md) · [Verificação](phase5/run001/verification.json)
