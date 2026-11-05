"""Download and audit public research data; Python standard library only. No models."""
import argparse
import csv
import hashlib
import io
import json
import platform
import shutil
import time
import urllib.request
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEART = 'age sex cp trestbps chol fbs restecg thalach exang oldpeak slope ca thal num'.split()
ADULT = 'age workclass fnlwgt education education-num marital-status occupation relationship race sex capital-gain capital-loss hours-per-week native-country income'.split()
MISSING = {'', '?', 'NA', 'NaN', 'nan', 'null'}

def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')

def fetch(url, path, offline=False):
    event = {'utc': datetime.now(timezone.utc).isoformat(), 'url': url, 'path': str(path.relative_to(ROOT))}
    start = time.perf_counter()
    try:
        if not offline:
            req = urllib.request.Request(url, headers={'User-Agent': 'DataMind-research-audit/1.0'})
            with urllib.request.urlopen(req, timeout=60) as response:
                body = response.read(100_000_001)
                if len(body) > 100_000_000:
                    raise ValueError('Download exceeds 100 MB safety limit')
                event.update(http_status=response.status, final_url=response.url,
                             content_type=response.headers.get('Content-Type'))
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
        body = path.read_bytes()
        event.update(status='cache' if offline else 'downloaded', bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
        return body
    except Exception as exc:
        event.update(status='failed', error=repr(exc))
        return None
    finally:
        event['elapsed_seconds'] = round(time.perf_counter()-start, 3)
        log = ROOT/'reports/access_log.jsonl'
        log.parent.mkdir(parents=True, exist_ok=True)
        with log.open('a', encoding='utf-8') as out:
            out.write(json.dumps(event, ensure_ascii=False)+'\n')

def audit(name, cols, rows, target, ids=()):
    if not rows or any(len(r) != len(cols) for r in rows):
        raise ValueError(f'{name}: empty data or inconsistent row width')
    profiles = {}
    for j, col in enumerate(cols):
        counts = Counter(r[j] for r in rows)
        valid = [v for v in counts if v not in MISSING]
        numeric = []
        try:
            numeric = [float(v) for v in valid]
            dtype = 'integer' if all(v.is_integer() for v in numeric) else 'real'
        except ValueError:
            dtype = 'categorical'
        profiles[col] = {'storage_type_inferred': dtype, 'missing': sum(counts[v] for v in MISSING),
                         'unique_nonmissing': len(valid), 'top_values': counts.most_common(6)}
        if numeric and dtype != 'categorical':
            profiles[col].update(min=min(numeric), max=max(numeric))
    keep = [j for j,c in enumerate(cols) if c not in ids]
    features = [j for j in keep if cols[j] != target]
    signatures = defaultdict(set)
    t = cols.index(target)
    for row in rows:
        signatures[tuple(row[j] for j in features)].add(row[t])
    result = {'rows': len(rows), 'columns': cols, 'target': target, 'id_columns': list(ids),
              'missing_cells': sum(p['missing'] for p in profiles.values()),
              'rows_any_missing': sum(any(v in MISSING for v in r) for r in rows),
              'exact_duplicate_excess': len(rows)-len(set(map(tuple, rows))),
              'duplicate_excess_without_ids': len(rows)-len({tuple(r[j] for j in keep) for r in rows}),
              'feature_patterns_multiple_targets': sum(len(v)>1 for v in signatures.values()),
              'target_counts': dict(Counter(r[t] for r in rows)), 'profiles': profiles}
    groups = {}
    for group in ['sex','Sex','race','Age']:
        if group in cols:
            j = cols.index(group)
            groups[group] = {v: {'rows': sum(r[j]==v for r in rows),
                                  'target_counts': dict(Counter(r[t] for r in rows if r[j]==v)),
                                  'rows_any_missing': sum(r[j]==v and any(x in MISSING for x in r) for r in rows)}
                             for v in sorted({r[j] for r in rows})}
    result['groups'] = groups
    sample = ROOT/f'data/samples/{name}.csv'
    sample.parent.mkdir(parents=True, exist_ok=True)
    with sample.open('w', newline='', encoding='utf-8') as out:
        writer = csv.writer(out); writer.writerow(cols); writer.writerows(rows[:20])
    return result

def parse(text):
    return [[v.strip() for v in r] for r in csv.reader(io.StringIO(text)) if r and not r[0].startswith('|')]

def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--offline', action='store_true')
    args = parser.parse_args()
    start = time.perf_counter(); results = {}; failures = []
    for ident in [45, 2, 891]:
        fetch(f'https://archive.ics.uci.edu/api/dataset?id={ident}', ROOT/f'data/raw/metadata_{ident}.json', args.offline)
    sources = [('heart','https://archive.ics.uci.edu/static/public/45/heart+disease.zip'),
               ('adult','https://archive.ics.uci.edu/static/public/2/adult.zip'),
               ('diabetes','https://archive.ics.uci.edu/static/public/891/data.csv')]
    for name,url in sources:
        try:
            body = fetch(url, ROOT/f'data/raw/{name}{".csv" if name=="diabetes" else ".zip"}', args.offline)
            if body is None:
                failures.append(name+': download/cache failure'); continue
            if name == 'diabetes':
                rows = parse(body.decode('utf-8-sig')); cols = rows.pop(0)
                results[name] = audit(name, cols, rows, 'Diabetes_binary', ['ID'])
            else:
                with zipfile.ZipFile(io.BytesIO(body)) as archive:
                    save(ROOT/f'reports/{name}_archive.json', [{'name': i.filename, 'bytes': i.file_size} for i in archive.infolist()])
                    if name == 'heart':
                        for center in ['cleveland','hungarian','switzerland','va']:
                            member = f'processed.{center}.data'
                            rows = parse(archive.read(member).decode())
                            results['heart_'+center] = audit('heart_'+center, HEART, rows, 'num')
                    else:
                        sets = []
                        for split,member in [('train','adult.data'),('test','adult.test')]:
                            rows = parse(archive.read(member).decode())
                            for row in rows: row[-1] = row[-1].removesuffix('.')
                            results['adult_'+split] = audit('adult_'+split, ADULT, rows, 'income')
                            sets.append(rows)
                        results['adult_all'] = audit('adult_all', ADULT, sets[0]+sets[1], 'income')
                        results['adult_all']['exact_patterns_shared_train_test'] = len(set(map(tuple,sets[0])) & set(map(tuple,sets[1])))
        except Exception as exc:
            failures.append(name+': '+repr(exc))
    save(ROOT/'reports/audit.json', {'datasets': results, 'failures': failures})
    save(ROOT/'reports/runtime.json', {'python': platform.python_version(), 'platform': platform.platform(),
         'elapsed_seconds': round(time.perf_counter()-start,3), 'free_disk_bytes': shutil.disk_usage(ROOT).free,
         'offline': args.offline, 'utc': datetime.now(timezone.utc).isoformat()})
    for name,r in results.items():
        print(name, json.dumps({k:r[k] for k in ['rows','missing_cells','rows_any_missing','duplicate_excess_without_ids','target_counts']}))
    print('Failures:', failures)
    if failures: raise SystemExit(1)

if __name__ == '__main__': main()
