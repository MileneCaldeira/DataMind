# Verificação após migração manual — 05/11/2026

Raiz atual: `C:\Users\Administrador\OneDrive\Documentos\DataMind`. A origem anterior não existe. Movimentação realizada pela pesquisadora; esta verificação não executou a migração.

## Evidências e correções

- `python -B scripts/verify_preservation.py`: PASS antes e depois da manutenção. Manifestos ativos: F5 57 entradas, F6 31, F7 37, F8 16, F9 9; F2 44; originais F3 17. Sete arquivos de scores correspondem às probabilidades salvas em `reports/phase6/final001/predictions.csv` (538333 bytes). Nenhum novo cálculo de métricas.
- `python -B scripts/verify.py`: seis hashes de origem, auditoria idêntica e oito visões verificadas.
- `python -B scripts/fase5_freeze.py --check`: 57 arquivos congelados e 17 hashes de origem aprovados.
- `python -B -m unittest discover -s tests -p test_maintenance.py -v`: nove testes passaram, exclusivamente fixtures de preservação/backup. Não foi executada a suíte científica antiga.
- Git: master; três commits e 129 arquivos rastreados; HEAD `55b35088b139d91da7d4ae3118addddf5d4a258f`. `git ls-remote origin refs/heads/master` confirmou o mesmo SHA em `https://github.com/MileneCaldeira/DataMind.git`. Nenhum push ou commit. `git fsck --full` não encontrou corrupção; informou objetos dangling, que foram preservados.
- Ambientes movidos: Python/importações/versões ainda funcionavam, mas ambos os pip.exe retornavam código 1 e activate.bat apontava ao caminho antigo. Preservados integralmente como `.venv-phase5-pre-migration` e `.venv-phase7-pre-migration`, ignorados pelo Git. Não são backup independente.
- Reconstrução nos nomes operacionais `.venv-phase5` e `.venv-phase7` com Python 3.13.7 (`python -m venv`) e `python -B -m pip install -r` usando, respectivamente, `reports/phase5/run001/requirements.lock.txt` e `reports/phase7/requirements-render.lock`. Nenhuma atualização de versões dos locks.
- Nos dois ambientes novos: `scripts/inspect_environment.py --kind phase5|phase7`, `python -m pip check`, `pip.exe --version` e ativação via activate.bat passaram. As 11 versões de cada lock conferem; imports aprovados. Sete modelos joblib carregados no ambiente phase5 sem fit, transform ou predict. Pip 25.2. Ativação aponta para a raiz nova. pyvenv.cfg registra o destino correto.
- README atualizado apenas quanto à localização operacional e uso dos ambientes. Código usa raiz relativa ao script; pesquisa de `ChatGPT` em scripts/src/tests/configurações não identificou caminho operacional antigo. Referências históricas em relatórios/manifestos e ambientes preservados não foram substituídas.

## Limites e estado final

Os quatro desvios históricos já registrados continuam documentados; nenhum manifesto foi regravado. Não existe nesta verificação um inventário completo pré-migração de todos os arquivos do disco: a integridade comprovada é a coberta pelos manifestos e verificações acima. Reprodução integral do experimento NÃO RETESTADA. Nenhum treinamento, nova previsão, avaliação do fold 10 ou geração de figuras.

Pronto para consulta e manutenção não preditiva no novo caminho. Modelos, dados e resultados congelados permaneceram íntegros. Ambientes antigos preservados ocupam espaço adicional; não foram excluídos. Permanecem os dois arquivos previamente não rastreados `reports/phase2/verification.txt` e `reports/verification.txt`. Alterações locais desta manutenção: README, este registro e ambientes ignorados. Backup independente e revisão científica humana continuam pendentes; a migração não resolve essas questões.
