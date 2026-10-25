"""Common nonlinear relative G predicate; directed membership of decimal states.
No training-entry claim and no per-centre gain boxes.
"""
import math,json,time,concurrent.futures
from pathlib import Path
from directed import I,A,K,h,dh,exp,log,require
ROOT=Path(__file__).resolve().parent;a=math.log(4);k=.5
def hf(u):return 0 if u<=0 else a/(a-k)*(math.exp(-k*u)-math.exp(-a*u)) if u<=1 else hf(1)*math.exp(-k*(u-1))
def H(x):
    x=I(x)
    def end(v):return I(0) if v<=0 else h(I(v)) if v<=1 else h(1)*exp(-K*(I(v)-1))
    lo,hi=end(x.lo),end(x.hi)
    return I(min(lo.lo,hi.lo),h(1).hi if x.lo<=1<=x.hi else max(lo.hi,hi.hi))
def first_root(arr,g):
    edges=sorted(set(arr+[s+1 for s in arr]));t=edges[0];q=.1;raw={}
    for end in edges:
        dt=end-t;J=sum(g[p]*a*math.exp(-a*(t-s)) for p,s in raw.items());C=q-.1+J/(a-k);D=J/(a-k)
        peak=math.log(a*D/(k*C))/(a-k) if C>0 and D>0 else 0.
        up=min(dt,max(0,peak))
        def val(u):return .1+C*math.exp(-k*u)-D*math.exp(-a*u)
        if up>0 and val(up)>=1:
            lo,hi=0.,up
            for _ in range(55):
                m=(lo+hi)/2
                if val(m)>=1:hi=m
                else:lo=m
            return t+(lo+hi)/2
        q=val(dt);t=end
        for p,s in enumerate(arr):
            if s==end:raw[p]=s
            if s+1==end:raw.pop(p,None)
    return None
def bisect_aux(M):
    lo,hi=0.,.1
    for _ in range(50):
        m=(lo+hi)/2
        if .025+M*hf(m)>=1:hi=m
        else:lo=m
    r=(lo+hi)/2;D=I(str(r))-I('1e-12')+I(0,'2e-12')
    require((I('.025')+I(str(M))*h(I(D.lo))).hi<1 and (I('.025')+I(str(M))*h(I(D.hi))).lo>1,'aux root signs')
    return D
def q(t,arr,g):return I('.1')+sum((I(str(v))*H(I(t)-x) for x,v in zip(arr,g)),I(0))
def early_cover(Flo,arr,g):
    # Before the first raw end every summand is nondecreasing.
    earliest=min(x.lo for x in arr);end=min(x.lo for x in arr)+I(1).lo
    if Flo<=end:return {'method':'live_monotonicity','pieces':0}
    stack=[(earliest,Flo,0)];count=0
    while stack:
        lo,hi,depth=stack.pop();v=q(I(lo,hi),arr,g)
        if v.hi<1:count+=1;continue
        if depth>=48:return None
        mid=(I(lo)+I(hi))/2;stack.extend([(lo,mid.lo,depth+1),(mid.lo,hi,depth+1)])
    return {'method':'directed_entire_prefix_cover','pieces':count}
def check(doc):
    start=time.monotonic();phase={(0,j):I(0) if j==0 else None for j in range(12)};records=[];fail=None
    for c in doc['cells']:
        n,j=c['layer'],c['lane'];pp=[phase[n-1,(j+s)%12] for s in [-1,0,1]];ports=[p for p in range(3) if pp[p] is not None]
        if not ports:phase[n,j]=None;records.append({'cell':[n,j],'active':False,'silent_margin':'0.9'});continue
        # Gauge out the first parent. Only relative intervals enter every guard.
        origin=min(pp[p].lo for p in ports);arr=[pp[p]-I(origin) for p in ports];g=[min(c['after_training']['g'][p],c['parameters'][p][0]) for p in ports]
        proposed=first_root([float((x.lo+x.hi)/2) for x in arr],g)
        if proposed is None:fail={'cell':[n,j],'reason':'no frozen head crossing'};break
        # Radius follows parent-date uncertainty, rather than an assumed uniform tube.
        spread=max(float(x.hi-x.lo) for x in arr);rad=max(1e-10,.6*spread)
        bracket=None
        for _ in range(8):
            lo=I(str(proposed-rad));hi=I(str(proposed+rad));qm=q(lo,arr,g);qp=q(hi,arr,g)
            if qm.hi<1 and qp.lo>1:bracket=(lo,hi,qm,qp);break
            rad*=2
        if bracket is None:fail={'cell':[n,j],'reason':'root signs unresolved'};break
        lo,hi,qm,qp=bracket;prefix=early_cover(lo.lo,arr,g)
        if prefix is None:fail={'cell':[n,j],'reason':'earlier-root exclusion unresolved'};break
        infl=[ii for ii,x in enumerate(arr) if x.lo<=hi.hi];masked=[ii for ii in range(len(arr)) if ii not in infl]
        es=[];ee=[]
        for p in ports:
            C,LM,LS,LE,M=c['parameters'][p];D=bisect_aux(M);E=D+log('1.25')/I(str(LM))+3*log(2)/I(str(LS));es.append(E);ee.append(E+A/I(str(LE)))
        beta=I(str(c['after_training']['b']));Pmin=1+log('2.5')/I('1.1');Pmax=1+log('2.5')/beta
        margins={'head_lower':1-I(qm.hi),'head_upper':I(qp.lo)-1,
          'error_after_head':I(min((I(arr[ii].lo)+I(es[ii].lo)-hi).lo for ii in infl)),
          'error_end_protected':I(min((lo+Pmin-I(arr[ii].hi)-I(ee[ii].hi)).lo for ii in infl)),
          'raw_end_protected':I(min((lo+Pmin-I(x.hi)-1).lo for x in arr)),
          'local_return':20+I(min(x.lo for x in arr))-hi-Pmax,
          'aux_own_return':I(min((20-ee[ii]).lo for ii in range(len(arr))))}
        if masked:margins['masked_after_head']=I(min((I(arr[ii].lo)-hi).lo for ii in masked))
        if any(v.lo<=0 for v in margins.values()):fail={'cell':[n,j],'reason':'relative guard fails','margins':{kk:v.pair() for kk,v in margins.items()}};break
        phase[n,j]=I(origin)+I(lo.lo,hi.hi)
        records.append({'cell':[n,j],'active':True,'relative_parents':[x.pair() for x in arr],'relative_head':[str(lo.lo),str(hi.hi)],'influential_ports':[ports[ii] for ii in infl],'masked_ports':[ports[ii] for ii in masked],'after_first_raw_end':hi.hi>min(x.lo for x in arr)+1,'prefix_certificate':prefix,'margins':{kk:v.pair() for kk,v in margins.items()}})
    result={'case':doc['case'],'status':'PASS_COMMON_RELATIVE_G' if fail is None else 'OPEN_MEMBERSHIP','failure':fail,'records':records,'seconds':time.monotonic()-start,'scope':'Membership of explicit saved decimal gain and physical-parameter vectors with regenerated charges; no certified training endpoint or universal basin claim'}
    print(doc['case']['name'],result['status'],fail,flush=True);return result
def main():
    t=time.monotonic();docs=json.load(open(ROOT/'INPUT_STATES.json'))
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as ex:rows=list(ex.map(check,docs))
    (ROOT/'MEMBERSHIP.json').write_text(json.dumps({'rows':rows,'seconds':time.monotonic()-t,'passing':sum(r['status'].startswith('PASS') for r in rows)},indent=2)+'\n')
if __name__=='__main__':main()
