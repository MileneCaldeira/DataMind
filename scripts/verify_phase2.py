"""Integrity, semantic boundary and cohort-accounting checks; no network."""
import hashlib
import json
from pathlib import Path
import phase2
import verify

ROOT=Path(__file__).resolve().parents[1]

def require(condition,message):
    if not condition:raise SystemExit('FAIL: '+message)

def main():
    verify.main()
    manifest=json.loads((ROOT/'reports/phase2/manifest.json').read_text(encoding='utf-8'))
    for relative,expected in manifest['sha256'].items():
        actual=hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()
        require(actual==expected,'bytes changed: '+relative)
    h=json.loads((ROOT/'reports/phase2/heart_analysis.json').read_text(encoding='utf-8'))
    for center,result in h['centers'].items():
        sets={}
        for key,p in result['policies'].items():
            require(p['eligible']['n']+p['excluded']['n']==result['n'],f'partition accounting {center}/{key}')
            require(sum(p['eligible']['target_counts'].values())==p['eligible']['n'],f'target accounting {center}/{key}')
            sets[key]=set(p['row_numbers_1based'])
            require(len(sets[key])==p['eligible']['n'],f'row trace {center}/{key}')
            require(all(1<=v<=result['n'] for v in sets[key]),f'row bounds {center}/{key}')
        require(sets['P3']<=sets['P2']<=sets['P0'],f'fixed-schema nesting {center}')
        require(sets['P3']<=sets['P4']<=sets['P0'],f'relaxed-schema nesting {center}')
        require(sets['P1']<=sets['P2'],f'complete-case nesting {center}')
    require(phase2.value('0')==0,'zero must remain observed')
    require(phase2.value('-9.') is None,'raw sentinel must be recognized')
    require(not phase2.flagged('sex',0) and not phase2.flagged('oldpeak',0),'valid zero codes')
    require(not phase2.flagged('oldpeak',-0.5),'unadjudicated negative ST must not be rejected')
    require(h['reprocessed_hungarian']['matches_raw_projection_multiset'],'Hungarian raw/reprocessed relationship')
    require(not h['raw_structure']['cleveland']['usable_for_projection'],'corrupt Cleveland must stay excluded')
    p=json.loads((ROOT/'reports/phase2/physionet_sample.json').read_text(encoding='utf-8'))
    require(not p['failures'],'sample audit incomplete')
    for site,s in p['sets'].items():
        require(s['sampled_files']==12 and len(s['columns'])==41,'sample contract '+site)
        require(sum(m['rows'] for m in s['members'])==s['rows'],'hour/file accounting '+site)
        require(sum(s['hourly_target_counts'].values())==s['rows'],'label accounting '+site)
        require(all(0<=v<=s['rows'] for v in s['missing_by_column'].values()),'missingness bounds '+site)
    print(f"PASS Phase 2: {len(manifest['sha256'])} hashes; cohorts and denominators reconcile; semantic boundaries; offline outputs unchanged.")

if __name__=='__main__':main()
