"""Consistency checks: general kernel reduces to nominal and obeys derived envelopes.
These finite checks supplement, not replace, the interval/domain arguments.
"""
import json
from pathlib import Path
from directed_high import I,require
from pruning_high import cell as nominal
from verify_full_corner import parameters,cell

def main():
    root=Path(__file__).parent;rows=json.loads((root/'results/forcing_certificate.json').read_text())['rows']
    profiles=[['0','0','0'],['.01','0','.01'],['0','.005','.01'],['.08','0','.08'],['0','.04','.08']]
    neutral=parameters('1','0','.08');late=parameters('1.0001','-.00001','.07999');early=parameters('.9999','.00009','.08001');checks=[]
    for xs in profiles:
        x=[I(v) for v in xs];n=nominal(x,I('.08'));g,_=cell(x,neutral)
        require(max(n.lo,g.lo)<=min(n.hi,g.hi),'general kernel agrees with nominal reduction')
        key='.08' if max(v.hi for v in x)>I('.02').lo else '.02'
        row=next(v for v in rows if v['input_width']==str(I(key).lo));bound=I(*row['pointwise_S_theta_minus_S_nominal'])
        differences=[]
        for p in [late,early]:
            y,_=cell(x,p);diff=y-n
            require(diff.lo>=bound.lo and diff.hi<=bound.hi,'selected extreme is within uniform derived forcing bound')
            differences.append(diff.pair())
        checks.append({'profile':xs,'nominal_reduction_intersection':[str(max(n.lo,g.lo)),str(min(n.hi,g.hi))],'extreme_differences':differences})
    out={'status':'PASS_NUMERICAL_CONSISTENCY_CHECKS','checks':checks,'scope':'Finite diagnostic checks, not the proof of the uniform forcing bound.'}
    (root/'results/kernel_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
if __name__=='__main__':main()
