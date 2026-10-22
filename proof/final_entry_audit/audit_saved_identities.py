"""Passive artifact audit. No A22 imports, engine execution, or replay.
Checks retained clock atoms globally and authenticates every examined payload.
Does not reconstruct discarded intermediate states or attest physical time identity.
"""
import sys,json,re,hashlib
from pathlib import Path
from zipfile import ZipFile
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'provenance_audit'))
from audit_provenance import DAG,canonical,sha

def main(folder,dest):
 folder=Path(folder);dest=Path(dest);atoms={};categories=Counter();guards=Counter();rows=[];occurrences=0;time_nodes=0;contexts=Counter();maxhist=[0,0]
 authenticated=json.loads((Path(__file__).resolve().parents[1]/'provenance_audit/output/all_layers_audit.json').read_text())
 hashes={(r['layer'],r['lane']):r['sha256'] for r in authenticated['checks']}
 for path in sorted(folder.glob('A22_v33_layer*.zip')):
  with ZipFile(path) as z:
   for name in sorted(n for n in z.namelist() if n.endswith('/result.json')):
    m=re.fullmatch(r'A22_v33_001/layer_(\d+)/cell_(\d+)/result.json',name);assert m
    cell=tuple(map(int,m.groups()));raw=z.read(name);assert sha(raw)==hashes[cell]
    d=DAG(json.loads(raw));root=d.fields(d.doc['root']);state=d.fields(root['state']);profile=d.simple(state['width_profile'])
    cats={k:v['count'] for k,v in profile['categories'].items()};categories.update(cats)
    gs={k:v['count'] for k,v in profile['guard_dates'].items()};guards.update(gs)
    for t in profile['largest_increases']:
     ctx=t.get('context') or {}
     if isinstance(ctx,dict) and 'kind' in ctx:contexts[ctx['kind']]+=1
    maxhist=[max(maxhist[0],profile['maximum_distinct_actuation_histories']),max(maxhist[1],profile['maximum_distinct_deposit_histories'])]
    local=set();nt=0
    for n in d.ns:
     if n[0]!='time':continue
     nt+=1;time_nodes+=1
     terms=d.ns[n[4]];assert terms[0]=='tuple'
     for ti in terms[1]:
      term=d.ns[ti];assert term[0]=='tuple' and len(term[1])==3
      ai,ni,vi=term[1];a=d.simple(ai);mult=d.simple(ni);v=d.ns[vi]
      assert isinstance(a,str) and type(mult) is int and v[0]=='affine'
      h=sha(canonical(v));prior=atoms.setdefault(a,h)
      assert prior==h,(cell,a,'conflicting retained definition')
      local.add(a);occurrences+=1
    rows.append(dict(layer=cell[0],lane=cell[1],payload_sha256=sha(raw),time_nodes=nt,distinct_atoms=len(local),profile_categories=cats,profile_guards=gs))
    if cell[1]==11:print('Passive identities checked through layer',cell[0],flush=True)
 assert len(rows)==216
 report=dict(status='PASS',scope='Global equality of retained time-atom definitions and complete saved profile counters; no trajectory execution',cells=216,time_nodes=time_nodes,time_atom_occurrences=occurrences,distinct_time_atoms=len(atoms),conflicting_definitions=0,profile_categories=dict(categories),profile_guard_counts=dict(guards),largest_increase_sample_contexts=dict(contexts),maximum_retained_actuation_histories=maxhist[0],maximum_retained_deposit_histories=maxhist[1],limitations=['Only retained DAG nodes are covered; discarded intermediate expressions are not available.','Profile largest_increases contains only up to 12 records per cell and is not an exhaustive trace.','Equal atom definitions do not by themselves prove that each expression denotes its intended physical event.'],per_cell=sorted(rows,key=lambda r:(r['layer'],r['lane'])))
 dest.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='per_cell'}))
if __name__=='__main__':
 if not __debug__:raise RuntimeError('Run without -O')
 main(*sys.argv[1:])
