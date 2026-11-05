"""Inspect isolated environment and frozen objects; never fit, transform or predict.
Run with python -B. Matplotlib cache is confined to a new OS temporary directory.
"""
import argparse
import hashlib
import importlib
import importlib.metadata as metadata
import json
import os
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main(kind):
    if sys.version_info[:3] != (3, 13, 7):
        raise ValueError("Expected recorded Python 3.13.7")
    lock = ROOT / ("reports/phase5/run001/requirements.lock.txt" if kind == "phase5"
                   else "reports/phase7/requirements-render.lock")
    versions = {}
    for line in lock.read_text().splitlines():
        if not line.strip():
            continue
        name, expected = line.split("==")
        actual = metadata.version(name)
        if actual != expected:
            raise ValueError("Version mismatch: " + name)
        versions[name] = actual
    models = {}
    if kind == "phase5":
        for name in ["numpy", "pandas", "scipy", "sklearn", "joblib", "psutil", "threadpoolctl"]:
            importlib.import_module(name)
        sys.path.insert(0, str(ROOT / "src"))
        import joblib
        frozen = json.loads((ROOT / "reports/phase5/run001/freeze.json").read_text())
        # Verify ALL frozen code and model files before trusted local deserialization.
        for name, expected in frozen["files"].items():
            if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
                raise ValueError("Frozen file mismatch: " + name)
        for path in sorted((ROOT / "reports/phase5/run001/models").glob("*.joblib")):
            model = joblib.load(path)
            lr = model.pipeline["lr"]
            if lr.l1_ratio != 0 or lr.solver != "lbfgs":
                raise ValueError("Unexpected estimator")
            models[path.name] = {"C": model.C, "input_columns": len(model.columns),
                                 "coefficient_shape": list(lr.coef_.shape)}
    else:
        os.environ["MPLCONFIGDIR"] = tempfile.mkdtemp(prefix="datamind-mpl-cache-")
        for name in ["numpy", "matplotlib", "matplotlib.backends.backend_agg", "PIL", "contourpy", "kiwisolver"]:
            importlib.import_module(name)
    return {"kind": kind, "python": sys.version.split()[0], "versions": versions,
            "lock_sha256": hashlib.sha256(lock.read_bytes()).hexdigest(),
            "imports": "PASS", "models_deserialized_without_prediction": models,
            "new_training": 0, "new_predictions": 0, "new_figures": 0,
            "full_experiment_reproduction": "NOT_RETESTED"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", choices=["phase5", "phase7"], required=True)
    print(json.dumps(main(parser.parse_args().kind), indent=2))
