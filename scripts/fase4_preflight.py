"""python scripts/fase4_preflight.py. Somente auditoria, sempre offline."""
import json
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from datamind.integrity import audit
result=audit(ROOT)
out=ROOT/"reports/phase4"
out.mkdir(exist_ok=True)
(out/"preflight.json").write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding="utf-8")
print(json.dumps(result,indent=2,ensure_ascii=False))
