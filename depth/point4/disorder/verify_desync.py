"""Directed local desynchronization lemma and a nonmonotonicity witness.

Not a universal entrance proof. All checks survive python -O.
"""
import json
import sys
from pathlib import Path
from fractions import Fraction as F
from directed import I, A, K, exp, log, h, dh, rational, require
from verify_pruning import build, root


def tube(base, width):
    w=I(width)
    interval=lambda key:I(*base[key])
    u0=interval('u0'); R0=interval('second_pulse_reopening_R')
    b=I('.07999','.08001'); B=b+I('.3')
    marks=interval('aux_mark_end'); es=interval('aux_error_start'); ee=interval('aux_error_end')
    first=I(u0.lo,(w+I(u0.hi)).hi)
    reopen=I(R0.lo,(w+I(R0.hi)).hi)
    LE=A/I('.15')*I('.9999','1.0001')
    # Reopening may precede or follow each port's error start.
    relative=reopen-8-I(0,w.hi)-es
    raw_gamma=I('.8')*exp(-LE*relative)-I('.2')
    gamma=I(max(I(0).lo,min(I('.6').lo,raw_gamma.lo)),max(I(0).hi,min(I('.6').hi,raw_gamma.hi)))
    eta=I('-.00001','.00009')
    gains=I('1.8')*exp(eta+gamma)
    delaylo=root(I(gains.hi)); delayhi=root(I(gains.lo))
    later=I(delaylo.lo,(w+I(delayhi.hi)).hi)
    gap=16+later-first
    checks={}
    def pos(name,value):
        require(value.lo>0,name)
        checks[name]=value.pair()
    pos('first_fire_after_all_arrivals',first-w)
    pos('first_marks_end_before_fire',first-w-I(marks.hi))
    pos('first_fire_before_earliest_raw_end',1-first)
    pos('first_fire_before_every_error',I(es.lo)-first)
    pos('first_errors_finish_under_protection',first+1+log('2.5')/b-w-I(ee.hi))
    pos('first_fast_phase_ends_before_second_marks',8+I('.01999')-first-1)
    pos('reopening_after_all_second_marks',reopen-8-w-I(marks.hi))
    pos('second_raw_pulses_entirely_blocked',reopen-9-w)
    pos('reopening_before_every_second_error_end',8+I(ee.lo)-reopen)
    pos('second_errors_finish_before_third_input',8-w-I(ee.hi))
    pos('each_port_adapts_on_second_error',gamma)
    pos('b_cap_inactive',I('1.1')-B)
    pos('gain_caps_inactive',I('3.9996')-I('1.2')*exp(eta+gamma))
    pos('later_fire_after_all_arrivals',later-w)
    pos('later_marks_end_before_fire',later-w-I(marks.hi))
    pos('later_fire_before_earliest_raw_end',1-later)
    pos('later_fire_before_every_error',I(es.lo)-later)
    pos('later_errors_finish_under_protection',later+1+log('2.5')/B-w-I(ee.hi))
    pos('later_recovery_before_next_cohort',8-later-1-log('2.5')/B)
    pos('auxiliaries_regenerate_between_cohorts',8-w-I(ee.hi))
    pos('first_output_gap_exceeds_15_5',gap-I('15.5'))
    return {'width':width,'first_firing_relative_to_T':first.pair(),
            'reopening_relative_to_T':reopen.pair(),
            'R_minus_second_error_start':relative.pair(),
            'log_gain_increment':gamma.pair(),
            'later_firing_relative_to_T_plus_16':later.pair(),
            'first_output_gap':gap.pair(),
            'later_output_gaps':'exactly 8 only for a fixed translated profile; otherwise bounded by 8 +/- the output delay envelope width',
            'later_gap_lower_bound':str((8-I(later.hi)+I(later.lo)).lo),
            'crude_output_cohort_width_upper':str((I(later.hi)-I(later.lo)).hi),
            'positive_margins':checks}


def spatial_root(g,x):
    lo,hi=F(1,10),F(9,10)
    def value(t):return I('.1')+sum((gi*h(rational(t)-xi) for gi,xi in zip(g,x)),I(0))
    require(value(lo).hi<1 and value(hi).lo>1,'spatial root signs')
    for _ in range(90):
        mid=(lo+hi)/2; v=value(mid)
        if v.hi<1:lo=mid
        elif v.lo>1:hi=mid
        else:
            require(hi-lo<F(1,10**20),'spatial root enclosure too wide')
            # Keep the already certified bracket when parameter-interval
            # uncertainty prevents an additional midpoint sign decision.
            break
    return I(rational(lo).lo,rational(hi).hi)


def exact_profile(xs):
    x=[I(t) for t in xs];g=[I('.3'),I('1.2'),I('.3')]
    first=spatial_root(g,x); LM=log('1.25')/I('.02'); LE=A/I('.15')
    reopen=(log('2.5')+I('.08')*(first+1)+I('.1')*sum((8+t+I('.02') for t in x),I(0))-I('.024')+I('.3')/LM)/I('.38')
    gamma=[];slope=[];branches=[]
    for xi in x:
        d=reopen-I('9.1')-xi
        if d.hi<0:
            gamma.append(I('.6'));slope.append(I(0));branches.append('ERROR starts after reopening: full increment')
        else:
            require(d.lo>0 and d.hi<I('.15').lo,'strict partial-error branch')
            gamma.append(I('.8')*exp(-LE*d)-I('.2'))
            slope.append(LE*I('.8')*exp(-LE*d));branches.append('ERROR starts before reopening: partial increment')
    learned=[gi*exp(ga) for gi,ga in zip(g,gamma)]
    out=spatial_root(learned,x)
    d0=[gi*dh(first-xi) for gi,xi in zip(g,x)];s0=sum(d0,I(0)); t=[v/s0 for v in d0]
    rk=[(I('.08')*v+I('.1'))/I('.38') for v in t]
    d1=[gi*dh(out-xi) for gi,xi in zip(learned,x)];s1=sum(d1,I(0))
    weights=[v/s1 for v in d1]
    c=[gi*h(out-xi)*si/s1 for gi,xi,si in zip(learned,x,slope)];total=sum(c,I(0))
    jac=[wi-ci+total*ri for wi,ci,ri in zip(weights,c,rk)]
    return {'input_profile':xs,'first_firing':first.pair(),'reopening':reopen.pair(),
            'branches':branches,'log_gain_increments':[v.pair() for v in gamma],
            'pruning_output_minus_16':out.pair(),'jacobian':[v.pair() for v in jac]}


def nominal_invariant_tube():
    base=build(False);w=I('.0001')
    u=I(*base['u0']);r=I(*base['second_pulse_reopening_R']);LE=A/I('.15')
    relative=r-I('9.1')+I(-w.hi,w.hi)
    require(relative.lo>0 and relative.hi<I('.15').lo,'all ports in strict partial-error regime')
    slope=LE*I('.8')*exp(-LE*relative)
    gamma=I('.8')*exp(-LE*relative)-I('.2')
    learned=[I(g)*exp(gamma) for g in ['.3','1.2','.3']]
    total=sum(learned,I(0));lo=root(I(total.hi));hi=root(I(total.lo))
    ages=I(lo.lo,(I(hi.hi)+w).hi)-I(0,w.hi)
    raw=[g*dh(ages) for g in learned];den=sum(raw,I(0))
    c=[g*h(ages)*slope/den for g in learned]
    firstages=I(u.lo,(I(u.hi)+w).hi)-I(0,w.hi)
    raw0=[I(g)*dh(firstages) for g in ['.3','1.2','.3']];den0=sum(raw0,I(0))
    rk=[(I('.08')*v/den0+I('.1'))/I('.38') for v in raw0]
    jac=[v/den-ci+sum(c,I(0))*ri for v,ci,ri in zip(raw,c,rk)]
    for j in jac: require(j.lo>0,'positive pruning-map derivative throughout nominal tube')
    gap=16+I(lo.lo)-w-I(u.hi)
    require(gap.lo>I('15.5').hi,'new safe gap')
    ready=I('15.5')-w-I(u.hi)-1-log('2.5')/I('.08')
    require(ready.lo>0,'safe-prefix regeneration')
    return {'width':'.0001','synchronized_output_delay':base['u1'],
            'scope':'Nominal physical parameters and exact nominal fresh states; complete initial cohorts X+8k with osc(X)<=.0001.',
            'R_minus_error_start':relative.pair(),'pruning_jacobian_entries': [v.pair() for v in jac],
            'new_safe_gap_lower_bound':str(gap.lo),'safe_prefix_regeneration_margin':ready.pair(),
            'conclusion':'The manual induction proves extinction after floor(M/2) layers for this boundary family; M=128 gives 64 safe output cohorts at layer 64 and no learning from layer 65 onward.',
            'full_independent_parameter_box':False,'original_single_lane_source':False}


def main():
    base=build(True)
    tubes=[tube(base,w) for w in ['.001','.01','.05','.08']]
    p=exact_profile(['.01','0','.01']);q=exact_profile(['.01','.000001','.01'])
    diff=I(*q['pruning_output_minus_16'])-I(*p['pruning_output_minus_16'])
    require(diff.hi<0,'larger input produces strictly earlier pruning output')
    require(I(*p['jacobian'][1]).hi<0,'negative central derivative')
    nominal=nominal_invariant_tube()
    spread=I(*p['pruning_output_minus_16'])-I(*nominal['synchronized_output_delay'])
    require(spread.lo>I('.01').hi,'one pruning step can increase cohort diameter')
    report={'status':'PASS_LOCAL_LEMMAS_AND_NONMONOTONICITY_WITNESS',
            'original_source_universal_entry':'NOT_PROVED',
            'scope':'Full independent fresh-cell box. Port i receives T+8k+x_i^k, with every x_i^k in [0,w], T>=20. No earlier input. Cohort profiles may change. A fixed profile gives exactly 8-spaced later outputs.',
            'not_covered':'Arbitrary learned initial states, unbounded temporal drift of cohort centers, iterative closure of the spatial tube, or reachability from the original source.',
            'tubes':tubes,'nominal_invariant_tube':nominal,
            'nonmonotonicity':{'baseline':p,'increased_central_arrival':q,'output_difference':diff.pair(),
            'scope':'Nominal preparation; a permitted local boundary profile, not demonstrated reachable from the original single-lane source.'},
            'diameter_amplification':{'input_ring_profile':['0','.01','0','0','0','0','0','0','0','0','0','.01'],
                                     'input_diameter':'.01','output_diameter_lower_bound':str(spread.lo),
                                     'reason':'Compare output lane 0, whose parents are [.01,0,.01], with lane 6, whose parents are [0,0,0].',
                                     'does_not_refute_multilayer_contraction':True}}
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent/'results/desync_certificate.json'
    path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'width_08_first_gap':tubes[-1]['first_output_gap'],
                      'central_derivative':p['jacobian'][1],'output_difference':diff.pair()}))


if __name__=='__main__':main()
