"""Referência de integridade do piloto. --create uma vez; --check é somente leitura."""
import argparse
import hashlib
import json
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"reports/phase5/run001"
MANIFEST=OUT/"freeze.json"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(create):
    if create:
        if MANIFEST.exists():raise FileExistsError("Referência já congelada")
        verification=json.loads((OUT/"verification.json").read_text())
        if verification["unit_tests"]!="OK" or verification["fold10_predictions"]!=0:
            raise ValueError("Verificação insuficiente")
        files=set()
        for pattern in ["src/datamind/*.py","scripts/fase5*.py","tests/*.py","experiments/fase[45].json",
                        "docs/fase[45]*.md","reports/fase[45]*.md","reports/phase5/run001/**/*"]:
            files.update(p for p in ROOT.glob(pattern) if p.is_file())
        files.update([ROOT/"docs/decisoes.md",ROOT/"reports/phase3/entradas.json"])
        entries={str(p.relative_to(ROOT)).replace("\\","/"):sha(p) for p in sorted(files) if p!=MANIFEST}
        data={"frozen_utc":datetime.now(timezone.utc).isoformat(),
              "status":"piloto_congelado_teste_final_nao_autorizado",
              "primary":"Brier(E3)-Brier(E2-fallback), operational comparison, not isolated causal imputation",
              "files":entries}
        MANIFEST.write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding="utf-8")
    data=json.loads(MANIFEST.read_text())
    bad=[name for name,h in data["files"].items() if not (ROOT/name).exists() or sha(ROOT/name)!=h]
    if bad:raise ValueError("Mudanças após congelamento: "+str(bad))
    # Validate raw inputs against preserved original manifest, without parsing holdout.
    for name,info in json.loads((ROOT/"reports/phase3/entradas.json").read_text()).items():
        if sha(ROOT/"data/raw/phase3"/name)!=info["sha256"]:raise ValueError("Raw alterado: "+name)
    print("PASS frozen files:",len(data["files"]),"; raw hashes: 17; no predictions executed")
if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--create",action="store_true")
    g.add_argument("--check",action="store_true")
    main(p.parse_args().create)
