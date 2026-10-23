"""Recompute the finite inequalities for the heterogeneous-tail theorems.

Usage: python3 verify.py [output.json]
All decisions use directed interval bounds or exact Fraction arithmetic.
This checks numerical lemmas, not the manual proof or Kingman's theorem.
"""
import hashlib
import json
import platform
import sys
from fractions import Fraction as F
from pathlib import Path
from directed import I, A, K, exp, log, h, dh, rational, require

ROOT = Path(__file__).resolve().parent


def root(total_gain):
    lo, hi = F(1, 2), F(4, 5)
    require((I('.1') + total_gain*h(rational(lo))).hi < 1, 'Root lower sign')
    require((I('.1') + total_gain*h(rational(hi))).lo > 1, 'Root upper sign')
    for _ in range(90):
        mid = (lo + hi)/2
        q = I('.1') + total_gain*h(rational(mid))
        if q.hi < 1:
            lo = mid
        elif q.lo > 1:
            hi = mid
        else:
            raise ArithmeticError('Unresolved root sign')
    return I(rational(lo).lo, rational(hi).hi)


def overlap():
    # Exact convolution for P with weights (1/6, 2/3, 1/6) on Z/12Z.
    row = [F(int(j == 0)) for j in range(12)]
    for _ in range(6):
        row = [(row[(j-1) % 12] + 4*row[j] + row[(j+1) % 12])/6
               for j in range(12)]
    rho = min(sum((min(row[j], row[(j-i) % 12]) for j in range(12)), F(0))
              for i in range(12))
    return rho, [str(x) for x in row]


def main():
    # No checks are implemented with assert: -O must not disable verification.
    require(dh(1).lo > 0, 'h increasing on [0,1]')
    require((A*A*exp(-A) - K*K*exp(-K)).lo > 0, 'h concave on [0,1]')
    delta = I('.00001')
    factor = I('.9999', '1.0001')
    M = I('.975')/h('.02')*factor
    LM = log('1.25')/I('.02')*factor
    LS = 3*log(2)/I('1.06')*factor
    LE = A/I('.15')*factor
    C = 4*factor
    Daux = I('.01999', '.02001')
    # Even the full READY auxiliary charge box is covered. No correlation
    # between M, LM, LS, LE or the three physical ports is assumed.
    require((I('.025')+delta+I(M.hi)*h(I(Daux.lo))).hi < 1,
            'Auxiliary first crossing lower guard')
    require((I('.025')-delta+I(M.lo)*h(I(Daux.hi))).lo > 1,
            'Auxiliary first crossing upper guard')
    require((I(M.lo)*dh(I(Daux.hi))-K*delta).lo > 0, 'Auxiliary crossing monotone')
    DM, DS, DE = I('.02')/factor, I('1.06')/factor, I('.15')/factor
    mark_end = Daux+DM
    error_start = mark_end+DS
    error_end = error_start+DE
    initial_error_end = delta/(I(LE.lo)*I('.025'))
    require(initial_error_end.hi < I('.001').lo, 'Initial ERROR ends before .001')
    require(error_start.lo > 1 and error_end.hi < I('1.3').lo, 'Auxiliary cycle')
    require(max(LS.hi, LE.hi) < LM.lo, 'Auxiliary drain maximum')
    work = (3*I(C.hi)+3*I(M.hi)+1)*A+I('1.1')+I('4.5')*I(LM.hi)+I('2.4')*I(LE.hi)
    require(work.hi < 500, 'Resource reserve remains positive')
    protection = 1+log('2.5')/I('.07999', '.08001')
    rho, row = overlap()
    profiles = []
    for full in (False, True):
        eta_lo, eta_hi = '-.00001', '.00009' if full else '.00001'
        gain_lo, gain_hi = I('1.8')*exp(eta_lo), I('1.8')*exp(eta_hi)
        u_min, u_max = root(gain_hi), root(gain_lo)
        # Outer width of the synchronized delays, not an inferred error bar.
        Delta = I(u_max.hi)-I(u_min.lo)
        D = I('.11')
        eps = I('.000000002') if full else I(0)
        gap = I('15.49999999') if full else I('15.5')
        W = D+6*(Delta+2*eps)
        age_lo = I(u_min.lo)-I(W.hi)-eps
        age_hi = I(u_max.hi)+I(W.hi)+eps
        require(age_lo.lo > 0 and age_hi.hi < 1, 'All parents active before head; no raw end')
        require((I('1.2')*exp(eta_hi)).hi < C.lo, 'Effective initial gains below every cap')
        require((I('.1')+delta+gain_hi*h(I(W.hi))).hi < 1,
                'No head before last parent, including perturbed initial q')
        # h' has decreasing logarithmic derivative. If youngest age is v,
        # v <= u_max and every other age is in [v,v+W], hence the ratio below.
        gamma = exp(I(eta_lo)-I(eta_hi))*dh(I(u_max.hi)+I(W.hi))/dh(I(u_max.hi))
        require(0 < gamma.lo <= gamma.hi < 1, 'Jacobian lower bound')
        beta = rational(rho)*(I(gamma.lo)**6)
        closure = I(beta.lo)*D-6*(Delta+2*eps)
        require(closure.lo > 0, 'Six-layer heterogeneous tube closure')
        margins = {
            'marks_end_before_head': age_lo-I(mark_end.hi),
            'head_before_first_raw_end': 1-age_hi,
            'head_before_first_error': I(error_start.lo)-age_hi,
            'all_errors_end_before_reopening': age_lo+I(protection.lo)-I(error_end.hi),
            'all_raw_currents_end_before_reopening': age_lo+I(protection.lo)-1,
            'main_ready_before_next_cohort': gap-I(W.hi)-I(u_max.hi)-eps-I(protection.hi),
            'all_auxiliaries_clear_before_next_cohort': gap-I(W.hi)-I(error_end.hi),
            'outgoing_pulse_ends_before_reopening': I(protection.lo)-1,
        }
        for name, value in margins.items():
            require(value.lo > 0, name)
        require(margins['main_ready_before_next_cohort'].lo > I('2.2').hi,
                'Recovery slack exceeds 2.2')
        profile = dict(
            name='full_fresh_initial_box' if full else 'exact_rest_tail',
            effective_log_gain_offsets=[eta_lo, eta_hi],
            entrance_width=D.pair(), entrance_same_lane_gap='15.5',
            maintained_gap=gap.pair(), expanded_intermediate_width=W.pair(),
            minimum_synchronized_delay=u_min.pair(), maximum_synchronized_delay=u_max.pair(),
            synchronized_delay_spread_upper=Delta.pair(),
            ages=[str(age_lo.lo), str(age_hi.hi)], gamma_lower=str(gamma.lo),
            six_layer_overlap_lower=str(beta.lo),
            six_layer_contraction_upper=(1-I(beta.lo)).pair(),
            block_closure_slack=closure.pair(),
            margins={name: value.pair() for name, value in margins.items()},
            first_cohort_per_layer_error_upper=eps.pair(),
        )
        if full:
            # Full initial q is not replaced by exact rest. Its influence on
            # the first head is bounded, and is summable over depth.
            slope = gain_lo*dh(I(age_hi.hi))-K*delta
            require(slope.lo > I('.3').hi, 'Uniform first-head slope > .3')
            first_error = delta*exp(-10)/I('.3')
            require(first_error.hi < eps.lo, 'First input at time >=20 gives error <2e-9')
            require((I(u_min.lo)-eps).lo > I('.66').hi, 'First-cohort advance > .66')
            ratio = exp('-.33')
            summed_error = eps/(1-ratio)
            require(summed_error.hi < I('.00000001').lo, 'Accumulated gap loss <1e-8')
            profile.update(first_input_absolute_time_lower='20',
                           first_head_slope_lower=str(slope.lo),
                           first_head_error_at_time_20=first_error.pair(),
                           first_head_error_geometric_ratio=ratio.pair(),
                           total_first_head_error_upper=summed_error.pair(),
                           initial_auxiliary_error_end_upper=initial_error_end.pair())
        profiles.append(profile)
    source_manifest = json.loads((ROOT/'sources/SOURCE_MANIFEST.json').read_text())
    for source in source_manifest['files']:
        require(hashlib.sha256((ROOT/'sources'/source['snapshot']).read_bytes()).hexdigest()
                == source['sha256'], 'Source snapshot hash')
    report = dict(
        status='PASS_NUMERICAL_LEMMAS',
        scope='Conditional heterogeneous tails and supporting bounds for a manual ergodic theorem; no new training campaign, no universal finite entry theorem, no proof-assistant verification.',
        arithmetic='70-digit directed Decimal basic operations; exponential degree 90 with geometric tail and range reduction; logarithm 250-term atanh series with explicit tail; exact rational ring convolution.',
        parameter_scope='Independent C_i, M_i, LM_i, LS_i, LE_i at relative +/-1e-4, independent per port/cell/layer. a,kappa,r,r_m and actuation constants stay fixed as in A22.',
        auxiliary_first_delay=Daux.pair(), mark_end=mark_end.pair(),
        error_start=error_start.pair(), error_end=error_end.pair(),
        principal_protection=protection.pair(), resource_work_upper=work.pair(),
        ring_six_step_row=row, ring_six_step_overlap_exact=str(rho), profiles=profiles,
        source_repository_commit=source_manifest['commit'],
        environment=dict(python=sys.version, implementation=platform.python_implementation(),
                         platform=platform.platform(), external_dependencies=[]),
        verifier_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                         for p in (ROOT/'directed.py', ROOT/'verify.py')},
    )
    output = Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'comparison_and_bounds.json'
    output.write_text(json.dumps(report, indent=2)+'\n')
    print(report['status'])
    for p in profiles:
        print(p['name'], 'beta >=', p['six_layer_overlap_lower'],
              'closure >=', p['block_closure_slack'][0],
              'recovery >=', p['margins']['main_ready_before_next_cohort'][0])


if __name__ == '__main__':
    main()
