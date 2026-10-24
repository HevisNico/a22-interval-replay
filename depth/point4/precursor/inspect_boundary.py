"""Read-only exact-rational inspection of the authenticated layer-18 DAGs.
No engine import, native load, trajectory computation, or campaign mutation.
"""
import hashlib, json, sys, zipfile
from fractions import Fraction as F
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from pathlib import Path

EXPECTED='e516c4a56ef7295798203e5985e9b7606d1690976b52fc7a794149a61d727d59'
def need(ok,msg):
    if not ok: raise ValueError(msg)
def dec(x,up=False):
    with localcontext() as c:
        c.prec=35;c.rounding=ROUND_CEILING if up else ROUND_FLOOR
        return str(Decimal(x.numerator)/Decimal(x.denominator))
def pair(b):return [dec(b[0]),dec(b[1],True)]
def fh(x):return F(float.fromhex(x))
class DAG:
    def __init__(self,d):
        need(d['schema']=='A22-affine-research-DAG-1','schema')
        self.ns=d['nodes'];self.root=d['root'];self.cache={}
    def fields(self,i):
        n=self.ns[i];need(n[0]=='dict','dict');return {self.simple(k):v for k,v in n[1]}
    def simple(self,i):
        n=self.ns[i]
        if n[0] in ('scalar','decimal'):return n[1]
        if n[0] in ('list','tuple'):return [self.simple(j) for j in n[1]]
        if n[0]=='dict':return {k:self.simple(v) for k,v in self.fields(i).items()}
        raise ValueError(n[0])
    def affine(self,i):
        if i not in self.cache:
            n=self.ns[i];need(n[0]=='affine','affine')
            d={k:fh(v) for k,v in n[3]};need(len(d)==len(n[3]),'symbols')
            e=fh(n[4]);need(e>=0,'negative error')
            self.cache[i]=(F(n[1]),F(n[2]),d,e)
        return self.cache[i]
    def timebox(self,i):
        n=self.ns[i];need(n[0]=='time','time')
        lo,hi,d,e=self.affine(n[2]);r=sum(map(abs,d.values()),e);o=F(n[3])
        return lo-r+o,hi+r+o

def main():
    src=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
    raw=src.read_bytes();need(hashlib.sha256(raw).hexdigest()==EXPECTED,'archive hash')
    rows=[];trains=[]
    with zipfile.ZipFile(src) as z:
        v=json.loads(z.read('A22_v33_001/layer_18/verification.json'))
        cfg=json.loads(z.read('A22_v33_001/campaign.json'))
        for j in range(12):
            pre=f'A22_v33_001/layer_18/cell_{j:02d}/'
            rb=z.read(pre+'receipt.json');r=json.loads(rb);p=z.read(pre+'result.json')
            need(hashlib.sha256(rb).hexdigest()==v['receipts'][j],'receipt hash')
            need(hashlib.sha256(p).hexdigest()==r['payload_sha256']==v['payloads'][j],'payload hash')
            need(r['case']['run_id']==cfg['run_id'] and r['case']['kernel_id']==cfg['kernel_id'],'campaign identity')
            need(r['case']['layer']==18 and r['case']['lane']==j,'cell identity')
            d=DAG(json.loads(p));top=d.fields(d.root);st=d.fields(top['state'])
            ids=d.ns[top['outputs']][1];ts=[d.timebox(i) for i in ids];trains.append(ts)
            need(len(ts)==r['metrics']['pulses'],'count')
            gaps=[(b[0]-a[1],b[1]-a[0]) for a,b in zip(ts,ts[1:])]
            row={'lane':j,'count':len(ts),'dates':[pair(t) for t in ts],'gaps':[pair(t) for t in gaps],
                 'terminal':{k:d.simple(st[k]) for k in ('q','g','b','main_phase','aux_phases','pending')}}
            rows.append(row)
            print(j,len(ts),'first',*[f'{float((a+b)/2):.6f}' for a,b in ts[:8]],'b',row['terminal']['b'])
    report={'archive_sha256':EXPECTED,'method':'Exact rational bounds of stored affine base plus exact offset; no new dynamics. Decimal outputs rounded outwards.',
            'cells':rows}
    (out/'boundary.json').write_text(json.dumps(report,indent=2)+'\n')
    with (out/'dates.tsv').open('w') as f:
        f.write('lane\tindex\tlo\thi\n')
        for r in rows:
            for i,(a,b) in enumerate(r['dates']):f.write(f"{r['lane']}\t{i}\t{a}\t{b}\n")
if __name__=='__main__':main()
