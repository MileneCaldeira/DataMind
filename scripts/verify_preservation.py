"""Read-only integrity layers. Standard library only; no model imports or writes."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = [
    "reports/phase5/run001/freeze.json",
    "reports/phase6/final001/delivery_manifest.json",
    "reports/phase7/manifest.json",
    "reports/phase8/manifest.json",
    "reports/phase9/manifest.json",
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local(root, name):
    path = (root / name.replace("\\", "/")).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("Path outside repository")
    return path


def read(root, name):
    return json.loads(local(root, name).read_text(encoding="utf-8-sig"))


def verify_entries(root, entries):
    for name, expected in entries.items():
        if digest(local(root, name)) != expected:
            raise ValueError("Hash mismatch: " + name)
    return len(entries)


def verify_history(root, before, changes):
    observed = {}
    recovered = []
    for name, expected in before.items():
        name = name.replace("\\", "/")
        actual = digest(local(root, name))
        if actual == expected:
            continue
        item = changes.get(name)
        if not item or item["before_sha256"] != expected or item["current_sha256"] != actual:
            raise ValueError("Undocumented historical change: " + name)
        if "recovered_utf8" in item:
            if hashlib.sha256(item["recovered_utf8"].encode("utf-8")).hexdigest() != expected:
                raise ValueError("Recovered history mismatch: " + name)
            recovered.append(name)
        observed[name] = item["epoch"]
    if set(observed) != set(changes):
        raise ValueError("Historical registry no longer matches current differences")
    return {"unchanged": len(before) - len(observed), "documented_changes": observed,
            "old_bytes_recovered": recovered,
            "status": "DOCUMENTED_DIFFERENCES_NOT_IDENTICAL_TO_PRETRAIN"}


def rows(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main(root=ROOT):
    registry = read(root, "experiments/integrity_maintenance.json")
    verify_entries(root, registry["manifest_anchors"])
    active = {p: verify_entries(root, read(root, p)["files"]) for p in MANIFESTS}
    phase2 = verify_entries(root, read(root, "reports/phase2/manifest.json")["sha256"])
    raw = read(root, "reports/phase3/entradas.json")
    verify_entries(root, {"data/raw/phase3/" + p: v["sha256"] for p, v in raw.items()})
    historical = verify_history(root, read(root, "reports/phase5/run001/before_hashes.json"),
                                registry["documented_changes"])
    # Compare existing tables only. No inference or metric calculation.
    final = root / "reports/phase6/final001"
    saved = rows(final / "predictions.csv")
    index = {r["ecg_id"]: r for r in saved}
    if len(index) != len(saved):
        raise ValueError("Duplicate final IDs")
    score_files = sorted(final.glob("scores_*.csv"))
    if len(score_files) != 7:
        raise ValueError("Expected seven preserved score files")
    for path in score_files:
        arm = path.stem.removeprefix("scores_")
        scores = rows(path)
        if len(scores) != len(saved) or len({r["ecg_id"] for r in scores}) != len(saved):
            raise ValueError("Score cardinality")
        if any(r["probability"] != index[r["ecg_id"]][arm] for r in scores):
            raise ValueError("Saved probabilities differ")
    receipt = read(root, "reports/phase6/final001/prediction_receipt.json")
    if digest(final / "predictions.csv") != receipt["predictions_sha256"]:
        raise ValueError("Receipt mismatch")
    return {"active_integrity": "PASS", "active_manifest_entries": active,
            "phase2_entries": phase2, "raw_phase3_entries": len(raw),
            "history": historical, "saved_score_files_match": len(score_files),
            "new_training": 0, "new_predictions": 0, "new_metrics": 0,
            "writes": 0,
            "current_documentation": "Tracked separately in Git; not a scientific freeze"}


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=True, indent=2))
