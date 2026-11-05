
# Figuras da versão 1
Geradas por scripts/fase7_materials.py exclusivamente a partir de agregados existentes. Formatos PNG (leitura), SVG/PDF (vetoriais). Unidades e denominadores constam nos eixos/legendas.
- 01_fluxograma: partições e estratos. Pacientes dos estratos podem se sobrepor.
- 02_cobertura: proporção atendida entre 2.198 exames e 54 positivos.
- 03_brier_pareado: diferença adimensional e IC95% por paciente, primário destacado; secundários sem interpretação confirmatória.
- 04_calibracao: cinco faixas fixas, fração observada e probabilidade média; rótulos das faixas e n/positivos. Não há suavização, novos ajustes ou IC inventados.
- 05_composicao: prevalência da anotação por completude e fold; comparação descritiva, não teste de drift.

Reprodução PowerShell na raiz:
```
python -m venv .venv-phase7
.venv-phase7/Scripts/python -m pip install -r reports/phase7/requirements-render.lock
.venv-phase7/Scripts/python scripts/fase7_materials.py
```
O script verifica os hashes congelados antes de renderizar e falha se houver divergência. Não importa módulos de modelos. Regenerar materiais não repete inferência preditiva.
