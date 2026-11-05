"""Phase 2 descriptive audit. Standard library only. Never edits Phase 1 inputs.

Default is offline. --download fetches evidence and a deterministic 12-file
sample from each PhysioNet training partition, without replacing cached bytes.
"""
import argparse
import csv
import hashlib
import io
import json
import re
import statistics as st
import urllib.request
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import audit

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'reports/phase2'
RAW = ROOT/'data/raw/phase2'
COLS = audit.HEART
INDEX = [3,4,9,10,12,16,19,32,38,40,41,44,51,58]
CENTERS = ['cleveland','hungarian','switzerland','va']
DOMAINS = {'sex':{0,1},'cp':{1,2,3,4},'fbs':{0,1},'restecg':{0,1,2},
           'exang':{0,1},'slope':{1,2,3},'ca':{0,1,2,3},'thal':{3,6,7},'num':{0,1,2,3,4}}
CORE = ['age','sex','cp','trestbps','chol','fbs','restecg','num']
POLICIES = {
 'P0': {'description':'Todos os registros processados; preservar ausências e alertas', 'required':[],'valid':False},
 'P1': {'description':'Casos completos nos 14 campos; somente ausências explícitas', 'required':COLS,'valid':False},
 'P2': {'description':'Casos completos em 8 campos de repouso/demografia/alvo', 'required':CORE,'valid':False},
 'P3': {'description':'P2 mais domínios categóricos e idade/pressão/colesterol positivos', 'required':CORE,'valid':True},
 'P4': {'description':'P3 retirando colesterol do esquema exigido', 'required':[c for c in CORE if c!='chol'],'valid':True},
}

def save(path,obj): audit.save(path,obj)
def sha(body): return hashlib.sha256(body).hexdigest()

def get(url,path,download):
    if path.exists(): return path.read_bytes()
    if not download: raise FileNotFoundError(f'Offline cache missing: {path}')
    event = {'utc':datetime.now(timezone.utc).isoformat(),'url':url,'path':str(path.relative_to(ROOT))}
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'DataMind-audit/2.0'}),timeout=30) as response:
            body=response.read(10_000_001)
            if len(body)>10_000_000: raise ValueError('Evidence/sample limit 10 MB exceeded')
            event.update(http_status=response.status,final_url=response.url,bytes=len(body),sha256=sha(body),status='downloaded')
        path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(body)
        return body
    except Exception as exc:
        event.update(status='failed',error=repr(exc)); raise
    finally:
        OUT.mkdir(parents=True,exist_ok=True)
        with (OUT/'access_log.jsonl').open('a',encoding='utf-8') as f: f.write(json.dumps(event)+'\n')

def value(token):
    if token in audit.MISSING: return None
    n=float(token)
    return None if n==-9 else n

def numeric_profile(vals):
    vals=sorted(v for v in vals if v is not None)
    if not vals:return {'n':0}
    def quant(p):
        q=(len(vals)-1)*p; lo=int(q); hi=min(lo+1,len(vals)-1)
        return round(vals[lo]+(vals[hi]-vals[lo])*(q-lo),4)
    return {'n':len(vals),'min':vals[0],'q1':quant(.25),'median':quant(.5),'q3':quant(.75),'max':vals[-1],'mean':round(st.mean(vals),4)}

def flagged(c,v):
    if v is None:return False
    return (c in DOMAINS and v not in DOMAINS[c]) or (c in ['age','trestbps','chol','thalach'] and v<=0)

def composition(rows):
    n=len(rows)
    return {'n':n,'age':numeric_profile([r['age'] for r in rows]),
            'sex_counts':dict(Counter(str(int(r['sex'])) for r in rows)),
            'target_counts':dict(Counter(str(int(r['num'])) for r in rows)),
            'positive_pct':round(100*sum(r['num']>0 for r in rows)/n,4) if n else None,
            'female_pct':round(100*sum(r['sex']==0 for r in rows)/n,4) if n else None}

def heart():
    source=ROOT/'data/raw/heart.zip'; data=source.read_bytes()
    result={'source_sha256':sha(data),'policies':POLICIES,'centers':{},'raw_structure':{},'raw_processed_comparison':{},'raw76_profiles':{}}
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for name in ['heart-disease.names','WARNING','ask-detrano','Index']:
            destination=RAW/name; destination.parent.mkdir(parents=True,exist_ok=True)
            if destination.exists() and destination.read_bytes()!=z.read(name):raise ValueError('Changed evidence')
            destination.write_bytes(z.read(name))
        names=z.read('heart-disease.names').decode()
        attrs=re.findall(r'^\s+(\d+)\s+([a-z][a-z0-9]*)\b(.*)$',names.split('-- Complete attribute documentation:')[1].split('9. Missing Attribute')[0],re.M)
        if [int(a[0]) for a in attrs]!=list(range(1,77)):raise ValueError('76 attribute extraction failed')
        save(OUT/'attributes76.json',[{'index':int(i),'name':n,'selected14':int(i) in INDEX} for i,n,_ in attrs])
        for center in CENTERS:
            tokens=audit.parse(z.read(f'processed.{center}.data').decode())
            rows=[dict(zip(COLS,map(value,r))) for r in tokens]
            profiles={}
            for c in COLS:
                vs=[r[c] for r in rows]; freq=Counter(v for v in vs if v is not None)
                profiles[c]={'missing':vs.count(None),'missing_pct':round(100*vs.count(None)/len(vs),3),
                  'flagged':sum(flagged(c,v) for v in vs),'zero':freq[0],
                  'negative_nonmissing':sum(v is not None and v<0 for v in vs),
                  'distribution':numeric_profile(vs),'frequencies':{str(k):v for k,v in sorted(freq.items())}}
            pol={}
            for key,p in POLICIES.items():
                def eligible(r):return all(r[c] is not None and (not p['valid'] or not flagged(c,r[c])) for c in p['required'])
                retained=[r for r in rows if eligible(r)]; removed=[r for r in rows if not eligible(r)]
                groups={}
                for label,pred in [('female',lambda r:r['sex']==0),('male',lambda r:r['sex']==1),('age_ge65',lambda r:r['age']>=65),('age_lt65',lambda r:r['age']<65),('target0',lambda r:r['num']==0),('target_positive',lambda r:r['num']>0)]:
                    denominator=sum(pred(r) for r in rows); numerator=sum(pred(r) for r in retained)
                    groups[label]={'eligible':numerator,'total':denominator,'retention_pct':round(100*numerator/denominator,3) if denominator else None}
                pol[key]={'eligible':composition(retained),'excluded':composition(removed),'retention_pct':round(100*len(retained)/len(rows),3),'groups':groups,
                          'row_numbers_1based':[i+1 for i,r in enumerate(rows) if eligible(r)]}
            result['centers'][center]={'n':len(rows),'profiles':profiles,'policies':pol}
            rawname={'va':'long-beach-va'}.get(center,center)+'.data'
            chunks=[x.split() for x in z.read(rawname).decode(errors='replace').split('name') if x.strip()]
            widths=Counter(len(x)+1 for x in chunks)
            result['raw_structure'][center]={'member':rawname,'record_width_counts':dict(widths),'usable_for_projection':center!='cleveland' and set(widths)=={76}}
            if center!='cleveland' and set(widths)=={76}:
                result['raw76_profiles'][center]={name:{'missing_minus9':sum(value(r[int(i)-1]) is None for r in chunks),
                    'distribution':numeric_profile([value(r[int(i)-1]) for r in chunks])} for i,name,_ in attrs if int(i)<76}
                result['raw76_profiles'][center]['name']={'dummy_name_count':len(chunks)}
                projected=[tuple(value(r[j-1]) for j in INDEX) for r in chunks]
                processed=[tuple(r[c] for c in COLS) for r in rows]
                rawtarget=Counter(int(r[57]) for r in chunks)
                binary=lambda r:r[:-1]+(float(r[-1]>0),)
                def candidate_transform(row):
                    # Forensic hypothesis only, NOT used for policy analyses.
                    converted=tuple(None if c in DOMAINS and v is not None and v not in DOMAINS[c] else v for c,v in zip(COLS,row))
                    return binary(converted) if center=='hungarian' else converted
                result['raw_processed_comparison'][center]={'raw_target_counts':dict(rawtarget),
                    'exact_multiset_equal':Counter(projected)==Counter(processed),
                    'binary_target_multiset_equal':Counter(map(binary,projected))==Counter(map(binary,processed)),
                    'candidate_domain_filter_and_hungarian_binary_multiset_equal':Counter(map(candidate_transform,projected))==Counter(processed),
                    'field_frequency_differences':{c:{'raw_only':{str(k):v for k,v in (Counter(a[j] for a in projected)-Counter(b[j] for b in processed)).items()},
                        'processed_only':{str(k):v for k,v in (Counter(b[j] for b in processed)-Counter(a[j] for a in projected)).items()}} for j,c in enumerate(COLS)},
                    'rowwise_comparison_warning':'Positional diagnostic only. Reordered rows are not linked individuals.',
                    'rowwise_field_mismatches':{c:sum(a[j]!=b[j] for a,b in zip(projected,processed)) for j,c in enumerate(COLS)},
                    'same_row_count':len(projected)==len(processed)}
        rep=[[value(v) for v in r.split()] for r in z.read('reprocessed.hungarian.data').decode().splitlines() if r.strip()]
        rawh=[x.split() for x in z.read('hungarian.data').decode().split('name') if x.strip()]
        projh=[tuple(value(r[j-1]) for j in INDEX) for r in rawh]
        result['reprocessed_hungarian']={'n':len(rep),'widths':dict(Counter(map(len,rep))), 'matches_raw_projection_multiset':Counter(map(tuple,rep))==Counter(projh), 'target_counts':dict(Counter(int(r[-1]) for r in rep))}
    for key in POLICIES:
        total=sum(r['policies'][key]['eligible']['n'] for r in result['centers'].values())
        for r in result['centers'].values():r['policies'][key]['center_share_pct']=round(100*r['policies'][key]['eligible']['n']/total,4) if total else None
    save(OUT/'heart_analysis.json',result)
    lines=['# Inventário dos 76 atributos originais','',
        'Gerado do dicionário no ZIP UCI. Ausências são valores numéricos −9; não incluem zeros nem códigos fora de domínio. Cleveland bruto não auditado por corrupção documentada. H/S/V: Hungarian (294), Switzerland (123), VA (200).','',
        '| Posição | Nome original | Nos 14 processados? | Ausentes H | Ausentes S | Ausentes V |',
        '|---:|---|---|---:|---:|---:|']
    for i,name,_ in attrs:
        counts=[result['raw76_profiles'][s][name].get('missing_minus9','campo artificial') for s in ['hungarian','switzerland','va']]
        lines.append('| '+' | '.join(map(str,[i,name,'sim' if int(i) in INDEX else 'não',*counts]))+' |')
    lines+=['','Uma coluna preenchida com valores artificiais ou sem definição não se torna utilizável por ter completude alta. Definições, incertezas e grupos semânticos em [heart_documentacao.md](heart_documentacao.md). Valores observados e resumos numéricos dos 75 campos numéricos estão em `raw76_profiles` de [heart_analysis.json](../reports/phase2/heart_analysis.json).']
    (ROOT/'docs/atributos_heart76.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return result

def physionet(download):
    root='https://physionet.org/files/challenge-2019/1.0.0/'
    result={'sample_plan':'12 files per A/B; lowest SHA256 of filename among full listing; fixed before reading values; feasibility only','sets':{},'failures':[]}
    for key,url in [('license',root+'LICENSE.txt'),('catalog','https://physionet.org/content/challenge-2019/1.0.0/')]:
        try:get(url,RAW/(key+'.txt'),download)
        except Exception as exc:result['failures'].append({'source':key,'error':repr(exc)})
    for setname in ['A','B']:
        try:
            url=root+f'training/training_set{setname}/'
            listing=get(url,RAW/f'listing_{setname}.html',download).decode()
            files=sorted(set(re.findall(r'href="(p\d+\.psv)"',listing)))
            if not files:raise ValueError('No PSV files found in index')
            chosen=sorted(files,key=lambda n:sha(n.encode()))[:12]
            members=[]; missing=Counter(); hourly=Counter(); nrows=0; widths=Counter(); lengths=[]; first24=Counter()
            for filename in chosen:
                body=get(url+filename,RAW/f'physionet_{setname}'/filename,download)
                table=list(csv.DictReader(io.StringIO(body.decode()),delimiter='|'))
                columns=list(table[0]); lengths.append(len(table)); nrows+=len(table)
                for row in table:
                    widths[len(row)]+=1
                    for c,v in row.items():missing[c]+=v=='NaN'
                    hourly[row['SepsisLabel']]+=1
                pos=any(r['SepsisLabel']=='1' for r in table)
                window=[r for r in table if float(r['ICULOS'])<=24]
                vitals=['HR','O2Sat','Temp','SBP','MAP','DBP','Resp']
                first24['files_with_all7_vitals_measured_at_least_once']+=all(any(r[c]!='NaN' for r in window) for c in vitals)
                first24['files_with_any_complete7_vital_hour']+=any(all(r[c]!='NaN' for c in vitals) for r in window)
                members.append({'file':filename,'rows':len(table),'sha256':sha(body),'has_positive_label':pos,'first_iculos':table[0]['ICULOS'],'last_iculos':table[-1]['ICULOS']})
            result['sets'][setname]={'listed_files':len(files),'sampled_files':len(chosen),'columns':columns,'rows':nrows,'width_counts':dict(widths),'lengths':numeric_profile(lengths),'missing_by_column':dict(missing),'hourly_target_counts':dict(hourly),'files_positive':sum(m['has_positive_label'] for m in members),'first24_availability':dict(first24),'members':members}
        except Exception as exc:result['failures'].append({'source':setname,'error':repr(exc)})
    save(OUT/'physionet_sample.json',result)
    return result

def matrix(result):
    lines=['# Matriz de qualidade e políticas — Heart Disease','',
     'Gerado por `python scripts/phase2.py`. Unidade: registro no arquivo processado; não pessoa comprovadamente única. Contagens integrais; nenhuma imputação ou deduplicação. Regras exploratórias, não protocolo clínico validado.','',
     '## Completude e alertas por variável','',
     'Cada célula: ausentes explícitos / alertas de domínio ou não positividade. Denominadores: Cleveland 303, Hungarian 294, Switzerland 123, VA 200. `oldpeak < 0` é relatado separadamente, sem ser declarado inválido.','',
     '| Variável | Cleveland | Hungarian | Switzerland | VA |','|---|---:|---:|---:|---:|']
    for c in COLS:lines.append('| '+c+' | '+' | '.join(f"{result['centers'][s]['profiles'][c]['missing']} / {result['centers'][s]['profiles'][c]['flagged']}" for s in CENTERS)+' |')
    lines+=['','Alertas: categorias fora do dicionário; `age`, `trestbps`, `chol` ou `thalach` ≤ 0. Alertas não são prova de erro nem códigos de ausência. As regras de elegibilidade P3/P4 só aplicam alertas às variáveis exigidas.','',
      '## Distribuições (todos os valores observados, inclusive alertas)','',
      '| Centro | Variável | n observado | Mínimo | Q1 | Mediana | Q3 | Máximo |','|---|---|---:|---:|---:|---:|---:|---:|']
    for s in CENTERS:
        for c in ['age','trestbps','chol','thalach','oldpeak']:
            p=result['centers'][s]['profiles'][c]['distribution']
            lines.append('| '+' | '.join(map(str,[s,c,p['n'],p['min'],p['q1'],p['median'],p['q3'],p['max']]))+' |')
    lines+=['','Quantis por interpolação linear em posição (n−1)p. Frequências completas de todas as variáveis, incluindo categorias, estão em [heart_analysis.json](../reports/phase2/heart_analysis.json). Não comparar medianas de variáveis ordinais como medidas contínuas.','',
      '## Políticas explícitas','']
    for k,p in POLICIES.items():lines.append(f"- **{k}**: {p['description']}. Exigidas: {', '.join(p['required']) or 'nenhuma'}.")
    lines+=['','P1 usa deleção por completude; P2 restringe a pergunta ao conjunto pré-exercício escolhido para sensibilidade; P3 acrescenta conformidade/plausibilidade mínima; P4 abandona a exigência de colesterol e muda o conjunto de informação. Não são tratamentos equivalentes da mesma pergunta. Referências e justificativas em [validação](../reports/validacao_cientifica.md).','',
      '## Elegibilidade e composição','',
      '| Política | Centro | Elegíveis / total | Retenção % | Participação do centro % | Idade média | Sexo 0 % | Alvo >0 % |','|---|---|---:|---:|---:|---:|---:|---:|']
    fmt=lambda v:'—' if v is None else str(round(v,2))
    for k in POLICIES:
        for s in CENTERS:
            r=result['centers'][s]; p=r['policies'][k]; e=p['eligible']
            lines.append('| '+' | '.join(map(str,[k,s,f"{e['n']} / {r['n']}",fmt(p['retention_pct']),fmt(p['center_share_pct']),fmt(e['age'].get('mean')),fmt(e['female_pct']),fmt(e['positive_pct'])]))+' |')
    lines+=['','A proporção `num>0` é uma sumarização derivada explícita; o alvo original não é substituído. Percentuais não são prevalência populacional. Com n=0 a composição é indefinida; com n=1 não há estabilidade inferencial.','',
      '## Retenção por subgrupo: numerador / denominador','',
      '| Política | Centro | Sexo 0 | Sexo 1 | Idade ≥65 | Idade <65 | Alvo 0 | Alvo >0 |','|---|---|---:|---:|---:|---:|---:|---:|']
    for k in ['P1','P2','P3','P4']:
        for s in CENTERS:
            g=result['centers'][s]['policies'][k]['groups']
            lines.append('| '+k+' | '+s+' | '+' | '.join(f"{g[x]['eligible']} / {g[x]['total']}" for x in ['female','male','age_ge65','age_lt65','target0','target_positive'])+' |')
    lines+=['','## Comparabilidade semântica','',
      '| Campos | Correspondência disponível | Limite |','|---|---|---|',
      '| age, sex | Mesmos nomes e códigos no dicionário | Mesma mensuração e seleção entre centros não verificadas; sex 0/1 é codificação histórica |',
      '| cp, fbs, restecg | Domínios documentados compartilhados | Não há adjudicação independente de diagnóstico ou padronização de procedimentos |',
      '| trestbps, chol | Unidades documentadas mmHg e mg/dl | Zeros requerem investigação; nenhum motivo de não coleta foi demonstrado |',
      '| thalach, exang, oldpeak, slope | Medidas ligadas ao exercício | Protocolo de exercício original #28 varia e possui dúvidas no arquivo ask-detrano; equivalência operacional não estabelecida |',
      '| ca, thal | Domínios documentados | Grande perda de dados em três centros; disponibilidade não implica comparabilidade clínica |',
      '| num | Status angiográfico; resumo permite 0 vs >0 | Dicionário não resolve interpretação ordinal 1–4, fronteira exata 50% e derivação histórica; versão húngara processada é binária |','',
      'Ver [documentação dos 76 atributos](heart_documentacao.md). Não se demonstrou acurácia por padrão-ouro, equivalência de instrumentos ou mecanismo MCAR/MAR/MNAR. Diferenças de retenção mostram seleção observada; viés relativo à população clínica não é identificável aqui.']
    (ROOT/'docs/matriz_qualidade.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--download',action='store_true'); args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    h=heart();matrix(h);p=physionet(args.download)
    for c,r in h['centers'].items():print(c,{k:v['eligible']['n'] for k,v in r['policies'].items()})
    print('Raw comparisons:',json.dumps(h['raw_processed_comparison']))
    print('PhysioNet:',{k:{x:v[x] for x in ['listed_files','sampled_files','rows','files_positive','first24_availability']} for k,v in p['sets'].items()},p['failures'])
    if p['failures']:raise SystemExit(1)

if __name__=='__main__':main()
