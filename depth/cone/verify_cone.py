"""Directed numerical checks for point 3. Standard-library only.

Checks use both directed Decimal intervals and integer fixed-point intervals.
This verifies numerical lemmas, not the accompanying manual proof.
"""
import hashlib
import json
import platform
import sys
from pathlib import Path
from directed import I, A, K, h, dh, exp, log, require
from integer_support import Q, S, a as ia, k as ik, h as ih, expo, ln, need

ROOT = Path(__file__).resolve().parent


def main():
    manifest = json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    for name, expected in manifest['files'].items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==expected,
                'Dependency hash: '+name)
    require(dh(1).lo>0, 'h increasing up to raw pulse end')
    require((A*A*exp(-A)-K*K*exp(-K)).lo>0, 'h concavity on [0,1]')
    profiles=[]
    for name,eta,low,high,coarse_speed in [
        ('exact_rest_tail','0.00001','0.666556597072780','0.666556597072782','1.500248'),
        ('full_initial_box_regenerated_tail','0.00009','0.666423402950283','0.666423402950286','1.500548')]:
        G=I('1.8')*exp(eta)
        require((I('.1')+G*h(low)).hi<1, name+' lower root sign')
        require((I('.1')+G*h(high)).lo>1, name+' upper root sign')
        u=I(low,high)
        v=I(1)/u
        require(v.hi<I(coarse_speed).lo, name+' coarse speed bound')
        iG=Q('1.8')*expo(eta)
        need((Q('.1')+iG*ih(low)).b<S, name+' integer lower root sign')
        need((Q('.1')+iG*ih(high)).a>S, name+' integer upper root sign')
        need((Q(1)/Q(low,high)).b<Q(coarse_speed).a, name+' integer speed bound')
        row={'name':name,'max_total_effective_gain':G.pair(),
             'minimum_synchronized_delay_enclosure':u.pair(),
             'uniform_cohort_front_speed_ceiling_enclosure':v.pair(),
             'strict_coarse_speed_ceiling':coarse_speed,
             'scope':'Regenerated cohort fronts under the point-1 entrance contract; not a delay from every individual parent arrival.'}
        if eta=='0.00009':
            error=I('.000000002')
            first_delay=u-error
            first_speed=I(1)/first_delay
            total_error=error/(1-exp('-.33'))
            require(first_delay.lo>0, 'Positive physical first-cohort advance')
            require(first_speed.hi<I('1.500548').lo, 'Physical first-cohort speed ceiling')
            require(total_error.hi<I('.00000001').lo, 'Total first-cohort error')
            need((Q(1)/(Q(low,high)-Q('.000000002'))).b<Q('1.500548').a,
                 'Integer physical first-cohort speed ceiling')
            need((Q('.000000002')/(1-expo('-.33'))).b<Q('.00000001').a,
                 'Integer total first-cohort error')
            row['first_physical_cohort']={
                'first_input_time_minimum':'20',
                'per_layer_error_upper':'2e-9',
                'uniform_delay_bound_enclosure':first_delay.pair(),
                'speed_ceiling_enclosure':first_speed.pair(),
                'strict_coarse_speed_ceiling':'1.500548',
                'total_error_enclosure':total_error.pair(),
                'sharper_cone':'min_j t[n,j] >= min_j t[0,j] + n*u_min - sum_{k=1}^n epsilon_k; sum epsilon_k < 1e-8'}
        profiles.append(row)

    # No tail contract is used for this first-activation bound.
    # q' <= kappa*(r-q)+J; q at an input-free boundary <= r+delta.
    J=3*I('4.0004')*A
    delta=I('.00001')
    d=log((J-K*delta)/(J-K*I('.9')))/K
    v=I(1)/d
    require(d.lo>I('0.05484010375122').hi and d.hi<I('0.05484010375123').lo,
            'Global activation delay bracket')
    require(v.hi<I('18.234831').lo, 'Global first-activation speed ceiling')
    iJ=3*Q('4.0004')*ia
    idelay=ln((iJ-ik*Q('.00001'))/(iJ-ik*Q('.9')))/ik
    need(idelay.a>Q('0.05484010375122').b and idelay.b<Q('0.05484010375123').a,
         'Integer activation delay bracket')
    need((Q(1)/idelay).b<Q('18.234831').a, 'Integer activation speed ceiling')
    # Fixed coarse endpoints independently satisfy the comparison guards.
    def envelope(t):
        e=exp(-K*I(t))
        return I('.1')+delta*e+(J/K)*(1-e)
    require(envelope('0.05484010375122').hi<1, 'Activation envelope lower sign')
    require(envelope('0.05484010375123').lo>1, 'Activation envelope upper sign')

    result={
        'status':'PASS_DECIMAL_AND_INTEGER_CONE_CHECKS',
        'proof_status':'Manual cone proofs with verified numerical lemmas; independent expert review pending',
        'units':{'time':'A22 model time','depth':'layers','speed':'layers per model time unit'},
        'tail_profiles':profiles,
        'global_first_activation':{
            'scope':'Entire original initial box, no hidden incoming currents, original graph and per-port non-overlap; no tail entrance hypothesis.',
            'max_port_gain':'4.0004','max_admitted_current':J.pair(),
            'delay_lower_bound_enclosure':d.pair(),
            'speed_ceiling_enclosure':v.pair(),
            'strict_coarse_speed_ceiling':'18.234831',
            'cone':'First emission at layer n is no earlier than s0+n*d_global, with s0 the first source pulse time.',
            'sharpness':'Conservative current-envelope bound; not claimed to be the fastest physically attainable device.'},
        'not_claimed':['A universal per-edge waiting time from every arriving parent pulse',
                       'A general information cone for perturbations of an already active network',
                       'Universal entry into the tail contract','Isotropy or a relativistic light cone'],
        'new_campaign':False,
        'source_commit':manifest['source_commit'],
        'environment':{'python':sys.version,'implementation':platform.python_implementation(),
                       'platform':platform.platform(),'external_dependencies':[]},
        'arithmetic':['70-digit directed Decimal, explicit series remainders',
                      '50-decimal-place integer fixed point, separate explicit series remainders'],
        'code_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                       for name in ['directed.py','integer_support.py','verify_cone.py']}
    }
    target=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'cone_certificate.json'
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'])
    for row in profiles:
        print(row['name'], 'speed <', row['strict_coarse_speed_ceiling'])
    print('global_first_activation speed < 18.234831')


if __name__=='__main__':
    main()
