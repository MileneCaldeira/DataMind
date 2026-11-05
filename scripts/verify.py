"""Verify original bytes and deterministic audit against the initial baseline."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main():
    baseline = ROOT/'reports/baseline'
    events = [json.loads(line) for line in (baseline/'access_log.jsonl').read_text(encoding='utf-8').splitlines()]
    checked = 0
    for event in events:
        if event['status'] != 'downloaded':
            continue
        path = ROOT / Path(event['path'].replace('\\', '/'))
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != event['sha256']:
            raise SystemExit(f'FAIL: source bytes changed: {path}')
        checked += 1
    current = json.loads((ROOT/'reports/audit.json').read_text(encoding='utf-8'))
    expected = json.loads((baseline/'audit.json').read_text(encoding='utf-8'))
    if current != expected:
        raise SystemExit('FAIL: audit differs from initial baseline; review changes before accepting')
    if current['failures'] or len(current['datasets']) != 8:
        raise SystemExit('FAIL: incomplete audit')
    for name, result in current['datasets'].items():
        if sum(result['target_counts'].values()) != result['rows']:
            raise SystemExit(f'FAIL: target counts do not reconcile: {name}')
        if result['profiles'][result['target']]['missing']:
            raise SystemExit(f'FAIL: missing target: {name}')
    print(f'PASS: {checked} source hashes; identical audit; 8 dataset views; target counts reconciled.')

if __name__ == '__main__':
    main()
