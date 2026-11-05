"""Non-destructive local backup. Explicit authorized destination required.
Production CLI refuses the same physical disk on Windows. No network or model code.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
CRITICAL = ["reports/phase5/run001/freeze.json",
            "reports/phase5/run001/models/E3.joblib",
            "reports/phase6/final001/predictions.csv",
            "artigo/manuscrito_v2.md"]


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def inventory(source, essential=False):
    result = {}
    for p in source.rglob("*"):
        if p.is_symlink() or p.is_junction():
            raise ValueError("Symbolic links/junctions require manual review: " + str(p))
        rel = p.relative_to(source)
        if essential and rel.parts[0] in (".venv-phase5", ".venv-phase7"):
            continue
        if p.is_file():
            result[rel.as_posix()] = {"bytes": p.stat().st_size, "sha256": sha(p)}
    return result


def verify_copy(folder, expected):
    actual = inventory(folder)
    if actual != expected:
        raise ValueError("Backup inventory/hash mismatch")
    return len(actual)


def copy_snapshot(source, destination, essential=False, critical=CRITICAL):
    source, destination = source.resolve(), destination.resolve()
    if not destination.is_dir():
        raise ValueError("Destination root must already exist")
    if destination.is_relative_to(source) or source.is_relative_to(destination):
        raise ValueError("Source/destination cannot contain each other")
    before = inventory(source, essential)
    size = sum(v["bytes"] for v in before.values())
    if shutil.disk_usage(destination).free < size * 2 + 1024 * 1024:
        raise ValueError("Insufficient space for copy and restore check")
    snapshot = destination / ("DataMind_" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid4().hex[:8])
    snapshot.mkdir(exist_ok=False)
    payload = snapshot / "project"
    payload.mkdir()
    for rel in before:
        target = payload / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / rel, target)
    verify_copy(payload, before)
    if inventory(source, essential) != before:
        raise ValueError("Source changed during backup; snapshot is not approved")
    restore = snapshot / "restore_check"
    restored = []
    for rel in critical:
        if rel not in before:
            raise ValueError("Critical file not in backup: " + rel)
        target = restore / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(payload / rel, target)
        if sha(target) != before[rel]["sha256"]:
            raise ValueError("Restore hash mismatch")
        restored.append(rel)
    # Read restored text as well; never deserialize a model or run predictions.
    for rel in restored:
        if Path(rel).suffix in (".json", ".md", ".csv"):
            with (restore / rel).open(encoding="utf-8-sig") as f:
                f.read(1024)
    receipt = {"utc": datetime.now(timezone.utc).isoformat(),
               "source": str(source), "destination": str(snapshot),
               "mode": "essential" if essential else "full",
               "files": len(before), "bytes": size, "hashes": before,
               "restored_and_read": restored, "status": "PASS"}
    (snapshot / "receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    return snapshot, receipt


def physical_disk(path):
    drive = path.resolve().drive
    if len(drive) != 2 or drive[1] != ":" or not drive[0].isalpha():
        raise ValueError("Only local Windows drive destinations supported")
    # Only a validated drive letter is interpolated.
    command = "(Get-Partition -DriveLetter '" + drive[0] + "' -ErrorAction Stop).DiskNumber | ConvertTo-Json -Compress"
    output = subprocess.check_output(["powershell", "-NoProfile", "-NonInteractive", "-Command", command])
    number = json.loads(output.decode("utf-8-sig"))
    if not isinstance(number, int):
        raise ValueError("Physical disk could not be uniquely established")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--authorized-destination", action="store_true", required=True,
                        help="Affirm this exact destination was authorized by the owner")
    parser.add_argument("--essential", action="store_true")
    args = parser.parse_args()
    if not args.destination.is_dir():
        parser.error("Existing authorized destination directory required")
    if physical_disk(ROOT) == physical_disk(args.destination):
        parser.error("Not independent: source and destination are on the same physical disk")
    snapshot, receipt = copy_snapshot(ROOT, args.destination, args.essential)
    print(json.dumps({"snapshot": str(snapshot), "files": receipt["files"],
                      "bytes": receipt["bytes"], "status": receipt["status"]}))


if __name__ == "__main__":
    main()
