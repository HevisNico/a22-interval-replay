"""Directed numerical lemmas for a local pruning theorem and its nominal iteration.

This does NOT certify entry of the original A22 source for the full parameter box.
No production engine or campaign is imported. No checks use assert.
"""
import json
import sys
from fractions import Fraction as F
from pathlib import Path
from directed import I, A, K, exp, log, h, dh, rational, require


def root(g, offset=0):
    lo, hi = F(0), F(1)
    require((I('.1')+offset+g*h(0)).hi < 1, 'lower root sign')
    require((I('.1')+offset+g*h(1)).lo > 1, 'upper root sign')
    for _ in range(90):
        mid = (lo+hi)/2
        value = I('.1')+offset+g*h(rational(mid))
        if value.hi < 1:
            lo = mid
        elif value.lo > 1:
            hi = mid
        else:
            raise ArithmeticError('Unresolved root sign')
    return I(rational(lo).lo, rational(hi).hi)


def build(full_box):
    f = I('.9999','1.0001') if full_box else I(1)
    delta = I('.00001') if full_box else I(0)
    LM, LS, LE = log('1.25')/I('.02')*f, 3*log(2)/I('1.06')*f, A/I('.15')*f
    M, C = I('.975')/h('.02')*f, 4*f
    dm, ds, de = I('.02')/f, I('1.06')/f, I('.15')/f
    d0 = I('.01999','.02001') if full_box else I('.02')
    if full_box:
        require((I('.025')+delta+I(M.hi)*h(I(d0.lo))).hi < 1, 'auxiliary lower bracket')
        require((I('.025')-delta+I(M.lo)*h(I(d0.hi))).lo > 1, 'auxiliary upper bracket')
        require((I(M.lo)*dh(I(d0.hi))-K*delta).lo > 0, 'auxiliary crossing increasing')
        require((delta/(I(LE.lo)*I('.025'))).hi < I('.001').lo, 'initial ERROR clears')
    mark_end, es, ee = d0+dm, d0+dm+ds, d0+dm+ds+de
    b = I('.07999','.08001') if full_box else I('.08')
    eta = I('-.00001','.00009') if full_box else I(0)
    G0 = I('1.8')*exp(eta)
    memory = delta*exp(-10)  # first input at T >= 20 in the full-box theorem
    lower = root(I(G0.hi), I(memory.hi))
    upper = root(I(G0.lo), -I(memory.hi))
    u0 = I(lower.lo, upper.hi)
    require((I(G0.lo)*dh(1)-K*memory).lo > 0, 'first crossing increasing')
    margins = {}
    def positive(name, x):
        require(x.lo > 0, name)
        margins[name] = x.pair()
    positive('first_marks_before_first_fire', u0-I(mark_end.hi))
    positive('first_fire_before_raw_end', 1-u0)
    positive('first_fire_before_errors', I(es.lo)-u0)
    positive('first_errors_end_during_protection', u0+1+log('2.5')/b-I(ee.hi))
    positive('first_fast_phase_ends_before_second_marks', 8+I(d0.lo)-u0-1)
    positive('second_marks_start_under_protection', u0+1+log('2.5')/b-8-I(mark_end.hi))
    # Once all second marks have ended, integrate b from first slow entry.
    # Each full mark adds .1 to b. For port i the integral contribution is
    # .1*(t-(8+d0_i))+.4*dm_i-.1/LM_i.
    B = b+I('.3')
    R = (log('2.5')+b*(u0+1)+I('.3')*(8+d0)-I('1.2')*dm+I('.3')/LM)/B
    positive('reopening_after_all_second_marks', R-8-I(mark_end.hi))
    positive('second_raw_pulse_entirely_blocked', R-9)
    positive('reopening_after_every_second_error_start', R-8-I(es.hi))
    positive('reopening_before_every_second_error_end', 8+I(ee.lo)-R)
    positive('b_cap_inactive', I('1.1')-B)
    gamma = I('.8')*exp(-LE*(R-8-es))-I('.2')
    positive('each_second_error_changes_gain', gamma)
    positive('second_errors_end_before_third_input', 8-I(ee.hi))
    G1 = I('1.8')*exp(eta+gamma)
    positive('all_gain_caps_inactive', I(C.lo)-I('1.2')*exp(eta+gamma))
    u1lo, u1hi = root(I(G1.hi)), root(I(G1.lo))
    u1 = I(u1lo.lo, u1hi.hi)
    positive('later_marks_before_fire', u1-I(mark_end.hi))
    positive('later_fire_before_raw_end', 1-u1)
    positive('later_fire_before_errors', I(es.lo)-u1)
    positive('later_errors_end_during_protection', u1+1+log('2.5')/B-I(ee.hi))
    positive('later_recovery_before_next_input', 8-u1-1-log('2.5')/B)
    positive('auxiliaries_clear_between_inputs', 8-I(ee.hi))
    gap = 16+u1-u0
    positive('first_output_gap_exceeds_15_5', gap-I('15.5'))
    # This permits repetition of the safe prefix in the nominal induction.
    positive('first_gap_allows_unlearned_recovery', gap-u0-1-log('2.5')/b)
    require(max(LS.hi,LE.hi) < LM.lo, 'largest auxiliary drain')
    work = (3*I(C.hi)+3*I(M.hi)+1)*A+I('1.1')+I('4.5')*I(LM.hi)+I('2.4')*I(LE.hi)
    positive('energy_50_lower_barrier', 500-work)
    return {'scope':'full initial and independent physical parameter box; synchronized input' if full_box else 'nominal synchronized input',
            'u0':u0.pair(), 'second_pulse_reopening_R':R.pair(),
            'second_error_log_gain_increment':gamma.pair(), 'u1':u1.pair(),
            'first_output_gap':gap.pair(), 'b_after_second_marks':B.pair(),
            'aux_mark_end':mark_end.pair(), 'aux_error_start':es.pair(),
            'aux_error_end':ee.pair(), 'positive_margins':margins}


def main():
    require(dh(1).lo > 0, 'h increasing')
    require((A*A*exp(-A)-K*K*exp(-K)).lo > 0, 'h concave on [0,1]')
    result = {'status':'PASS_NUMERICAL_LEMMAS', 'original_source_universal_entry':'NOT_PROVED',
              'proof_status':'Manual argument; directed numerical checks; no proof-assistant verification',
              'nominal':build(False), 'full_box_local':build(True)}
    out = Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent/'results/pruning_certificate.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'], 'original_source_universal_entry':result['original_source_universal_entry'],
                      'full_box_first_gap':result['full_box_local']['first_output_gap'], 'output':str(out)}))


if __name__ == '__main__': main()
