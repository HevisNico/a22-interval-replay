"""Read-only verification of relative head brackets and local invariant guards."""
import json,time,concurrent.futures
from check import ROOT,I,A,K,exp,log,h,dh,q,early_cover,bisect_aux
from directed import require
def slope(x):
    vals=[]
    if x.lo<=0:vals.append(I(0))
    if x.hi>=0 and x.lo<=1:
        vals += [dh(I(max(x.lo,I(0).lo))),dh(I(min(x.hi,I(1).hi)))]
    if x.hi>=1:
        vals += [-K*h(1)*exp(-K*(I(max(x.lo,I(1).lo))-1)),-K*h(1)*exp(-K*(I(x.hi)-1))]
    return I(min(v.lo for v in vals),max(v.hi for v in vals))
def verify(task):
    d,r=task;phase={(0,j):I(0) if j==0 else None for j in range(12)};active=0;late=0
    require=lambda b,m: (_ for _ in ()).throw(ArithmeticError(m)) if not b else None
    require(len(r['records'])==216,'cell count')
    for c,z in zip(d['cells'],r['records']):
        n,j=c['layer'],c['lane'];require(z['cell']==[n,j],'order');pa=[phase[n-1,(j+s)%12] for s in [-1,0,1]];ports=[p for p in range(3) if pa[p] is not None]
        if not z['active']:require(not ports,'silent driven');phase[n,j]=None;continue
        active+=1;origin=min(pa[p].lo for p in ports);arr=[pa[p]-I(origin) for p in ports];g=[min(c['after_training']['g'][p],c['parameters'][p][0]) for p in ports];F=I(*z['relative_head'])
        require([x.pair() for x in arr]==z['relative_parents'],'relative parents')
        require(q(I(F.lo),arr,g).hi<1 and q(I(F.hi),arr,g).lo>1,'root signs')
        require(sum((I(str(v))*slope(F-xx) for xx,v in zip(arr,g)),I(0)).lo>0,'strict upward root on entire bracket')
        require(early_cover(F.lo,arr,g) is not None,'first root exclusion')
        infl=[ii for ii,x in enumerate(arr) if x.lo<=F.hi];masked=[ii for ii in range(len(arr)) if ii not in infl]
        require([ports[ii] for ii in infl]==z['influential_ports'] and [ports[ii] for ii in masked]==z['masked_ports'],'port roles')
        Pmin=1+log('2.5')/I('1.1');Pmax=1+log('2.5')/I(str(c['after_training']['b']))
        for ii,p in enumerate(ports):
            C,LM,LS,LE,M=c['parameters'][p];D=bisect_aux(M);es=D+log('1.25')/I(str(LM))+3*log(2)/I(str(LS));ee=es+A/I(str(LE))
            require(es.lo>1 and ee.hi<20,'own pulse cycle')
            require((I(F.lo)+Pmin-I(arr[ii].hi)-1).lo>0,'raw protected')
            if ii in infl:
                require((I(arr[ii].lo)+I(es.lo)-I(F.hi)).lo>0,'ERROR after head')
                require((I(F.lo)+Pmin-I(arr[ii].hi)-I(ee.hi)).lo>0,'ERROR protected')
            else:require((I(arr[ii].lo)-I(F.hi)).lo>0,'masked')
        require((20+I(min(x.lo for x in arr))-I(F.hi)-Pmax).lo>0,'local return')
        phase[n,j]=I(origin)+F;late+=int(z['after_first_raw_end'])
    require(active==191,'mask');return {'case':r['case']['name'],'status':'PASS_READ_ONLY_MEMBERSHIP','active':active,'late_heads':late}
def main():
    t=time.monotonic();docs=json.load(open(ROOT/'INPUT_STATES.json'));m=json.load(open(ROOT/'MEMBERSHIP.json'));tasks=[(d,r) for d,r in zip(docs,m['rows']) if r['status'].startswith('PASS')]
    # Uniform resource/aux-drain assumptions from the unchanged physical kernel.
    f=I('.99','1.01');M=I('.975')/h('.02')*f;LM=log('1.25')/I('.02')*f;LE=A/I('.15')*f;LS=3*log(2)/I('1.06')*f
    require(dh(1).lo>0 and max(LE.hi,LS.hi)<LM.lo,'uniform physical guards')
    require((A*A*exp(-A)-K*K*exp(-K)).lo>0,'dh decreasing on live interval')
    work=(3*I('4.04')+3*I(M.hi)+1)*A+I('1.1')+I('4.5')*I(LM.hi)+I('2.4')*I(LE.hi)
    require(work.hi<500,'resource reserve')
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as ex:rows=list(ex.map(verify,tasks))
    (ROOT/'AUDIT.json').write_text(json.dumps({'status':'PASS','rows':rows,'seconds':time.monotonic()-t,'resource_work':work.pair(),'scope':'Separate read-only control flow, shared directed arithmetic and response helpers; not independent arithmetic or proof-assistant verification'},indent=2)+'\n')
    print('PASS',len(rows),flush=True)
if __name__=='__main__':main()
