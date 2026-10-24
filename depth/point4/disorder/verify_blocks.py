"""Directed six-layer results. Decimal Newton is ONLY a candidate generator.

Every root is enclosed by strict signs checked with the independent finite-series
interval arithmetic in directed.py. No assertion is used as a proof check.
"""
import json
import sys
from decimal import Decimal as D,localcontext
from fractions import Fraction as F
from pathlib import Path
from directed import I,A,K,exp,log,h,dh,require,rational
from verify_desync import nominal_invariant_tube


def guess(g,x,start):
    with localcontext() as ctx:
        ctx.prec=75
        a=D(4).ln();k=D('.5');f=sum(x)/3+D(start)
        for _ in range(25):
            v=[f-t for t in x]
            hv=[a/(a-k)*((-k*t).exp()-(-a*t).exp()) for t in v]
            dv=[a/(a-k)*(a*(-a*t).exp()-k*(-k*t).exp()) for t in v]
            f-=(sum(gi*hi for gi,hi in zip(g,hv))-D('.9'))/sum(gi*di for gi,di in zip(g,dv))
        return f


def mono_h(age):
    require(0<=age.lo<=age.hi<=1,'head ages in monotone response interval')
    return I(h(I(age.lo)).lo,h(I(age.hi)).hi)


def enclosed_root(g,x,start):
    low_guess=guess([z.hi for z in g],[z.lo for z in x],start)
    high_guess=guess([z.lo for z in g],[z.hi for z in x],start)
    lo=(I(low_guess)-I('1e-30')).lo
    hi=(I(high_guess)+I('1e-30')).hi
    lower=I('.1')+sum((gi*mono_h(I(lo)-xi) for gi,xi in zip(g,x)),I(0))
    upper=I('.1')+sum((gi*mono_h(I(hi)-xi) for gi,xi in zip(g,x)),I(0))
    require(lower.hi<1 and upper.lo>1,'strict finite-series root signs')
    require(lo>max(t.hi for t in x) and hi<min(t.lo for t in x)+1,'root lies between last start and first raw ending')
    return I(lo,hi)


LM=log('1.25')/I('.02');LE=A/I('.15')
G=[I('.3'),I('1.2'),I('.3')]


def cell(x,b):
    first=enclosed_root(G,x,'.6666')
    R=(log('2.5')+b*(first+1)+I('.1')*sum((8+t+I('.02') for t in x),I(0))-I('.024')+I('.3')/LM)/(b+I('.3'))
    gamma=[]
    for t in x:
        v=I('.8')*exp(-LE*(R-t-I('9.1')))-I('.2')
        gamma.append(I(max(D(0),min(D('.6'),v.lo)),max(D(0),min(D('.6'),v.hi))))
    learned=[gi*exp(ga) for gi,ga in zip(G,gamma)]
    require((b+I('.3')).hi<D('1.1'),'b cap inactive')
    require(max(gi.hi for gi in learned)<4,'gain caps inactive')
    out=enclosed_root(learned,x,'.27')
    # Direct event clearances validate every witness, including varying b.
    require((first-max(t.hi for t in x)-I('.04')).lo>0,'first marks before firing')
    require((first+1+log('2.5')/b-max(t.hi for t in x)-I('1.25')).lo>0,'first errors protected')
    require((8+min(t.lo for t in x)+I('.02')-first-1).lo>0,'first fast phase before second marks')
    require((R-max(t.hi for t in x)-9).lo>0,'second raw pulses fully blocked')
    require((8+min(t.lo for t in x)+I('1.25')-R).lo>0,'reopening before second errors end')
    require((8+min(t.lo for t in x)-max(t.hi for t in x)-I('1.25')).lo>0,'errors finish before third input')
    require((out-max(t.hi for t in x)-I('.04')).lo>0,'later marks before firing')
    require((min(t.lo for t in x)+I('1.1')-out).lo>0,'later firing before errors')
    require((out+1+log('2.5')/(b+I('.3'))-max(t.hi for t in x)-I('1.25')).lo>0,'later errors protected')
    require((8+min(t.lo for t in x)-out-1-log('2.5')/(b+I('.3'))).lo>0,'later regeneration')
    require((16+out-first).lo>D('15.5'),'new safe gap')
    return out


def width(xs):
    return I(max(t.lo for t in xs))-I(min(t.hi for t in xs)), I(max(t.hi for t in xs))-I(min(t.lo for t in xs))


def orbit(xs,steps):
    x=[I(t) for t in xs];history=[]
    for n in range(steps):
        require(width(x)[1].hi<D('.08'),'witness remains in already validated local tube')
        x=[cell([x[(j-1)%12],x[j],x[(j+1)%12]],I('.08')) for j in range(12)]
        bounds=width(x)
        history.append({'layer':n+1,'profile':[v.pair() for v in x],
                        'diameter':[str(bounds[0].lo),str(bounds[1].hi)]})
        print(json.dumps({'verified_orbit_layer':n+1,'diameter_upper':str(bounds[1].hi)}),flush=True)
    return x,history


def contraction():
    tube=nominal_invariant_tube()
    q=[F(t[0]) for t in tube['pruning_jacobian_entries']]
    row=[F(int(k==0)) for k in range(12)]
    for _ in range(6):row=[q[0]*row[(k-1)%12]+q[1]*row[k]+q[2]*row[(k+1)%12] for k in range(12)]
    rho=min(sum((min(row[k],row[(k-i)%12]) for k in range(12)),F(0)) for i in range(12))
    require(rho>F('.11499'),'six-step common row mass')
    return {'nominal_tube_width':'.0001','lower_local_jacobian_row':[str(v) for v in q],
            'six_step_overlap':rational(rho).pair(),'six_step_oscillation_contraction_factor':rational(1-rho).pair(),
            'scope':'Two nominal profiles in the invariant width-1e-4 tube; no independently varying physical parameters.'}


def main():
    require(dh(1).lo>0,'response increasing on [0,1]')
    small=contraction()
    low=cell([I(0)]*3,I('.07999'));high=cell([I(0)]*3,I('.08001'))
    spread=low-high
    require(spread.lo>D('.0001'),'admissible b heterogeneity leaves narrow tube from a synchronized profile')
    x=['0','0','0','.01','.01','.01','.01','0','0','0','0','0']
    eps=I('.0000001');y=[I(t)+(eps if j%2==0 else I(0)) for j,t in enumerate(x)]
    xx,hx=orbit(x,6);yy,hy=orbit(y,6)
    d10=yy[10]-xx[10];d11=yy[11]-xx[11];amp=(d10-d11)/eps
    require(amp.lo>D('1.70'),'six-step expansion of a pair of profiles')
    report={'status':'PASS_NARROW_CONTRACTION_AND_WIDER_OBSTRUCTIONS','universal_original_source_entry':'NOT_PROVED',
            'narrow_nominal_contraction':small,
            'independent_b_forcing':{'input_profile':'synchronized','b_values':['.07999','.08001'],
                'nominal_other_parameters':True,'output_delays':[low.pair(),high.pair()],
                'output_diameter':spread.pair(),'scope':'Local complete-cohort boundary, not a demonstrated original-source realization.'},
            'six_step_pair_expansion':{'input_x':x,'input_y':[v.pair() for v in y],'input_difference_oscillation':eps.pair(),
                'output_row_pair':[10,11],'output_difference_oscillation_lower_bound':str((d10-d11).lo),
                'amplification_lower_bound':str(amp.lo),'amplification_row_pair_interval':amp.pair(),
                'orbit_x':hx,'orbit_y':hy,'does_not_refute_contraction_of_each_profile_toward_synchrony':True,
                'does_not_refute_universal_entry':True},
            'arithmetic':'Newton guesses use Decimal.exp/ln only for candidates. All root enclosures use strict directed finite-series signs.'}
    out=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent/'results/block_certificate.json'
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'b_forcing':spread.pair(),'six_step_pair_expansion':amp.pair()}))


if __name__=='__main__':main()
