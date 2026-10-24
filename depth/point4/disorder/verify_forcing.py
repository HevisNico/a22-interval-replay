"""Uniform local full-parameter perturbation bounds for regenerated pruning."""
import json,sys
from pathlib import Path
from directed import I,A,K,exp,log,dh,require
from verify_desync import tube
from baselines import baseline


def forcing(w,pruning,tail):
    w=I(w);eta=I('-.00001','.00009');b=I('.07999','.08001');B=b+I('.3');fac=I('.9999','1.0001')
    u=I(tail['profiles'][1]['maximum_synchronized_delay'][1]);Gmin=I('1.8')*exp('-.00001')
    K0=I('.9')/(Gmin*dh(u+w))
    Fdiff=I((-I('.00009')*K0).lo,(I('.00001')*K0).hi)
    n=pruning['nominal'];u0=I(*n['u0']);R0=I(*n['second_pulse_reopening_R'])
    f0minusR=u0+1-R0+I(-w.hi,w.hi)
    L25=log('1.25');LM=L25/I('.02');LE=A/I('.15');alpha=I('.1')-I('.4')*L25
    di=I('-.00001','.00001')
    invLM=(I(1)/fac-1)/LM
    DS=I('1.06')*(I(1)/fac-1)
    phase=(b/B)*Fdiff+((b-I('.08'))/B)*f0minusR
    phase+=(I('.1')/B-1)*di+2*(I('.1')/B)*di
    phase+=(alpha/B-L25)*invLM+2*(alpha/B)*invLM-DS
    nominalphase=R0-I('9.1')+I(-w.hi,w.hi)
    exponent=(LE*fac)*phase+(LE*(fac-1))*nominalphase
    # z -> clip(.8 exp(-z)-.2,0,.6) is decreasing and globally .8-Lipschitz.
    gamdiff=I((-I('.8')*I(max(exponent.hi,I(0).hi))).lo,
              (-I('.8')*I(min(exponent.lo,I(0).lo))).hi)
    logdiff=eta+gamdiff
    local=tube(pruning['full_box_local'],str(w.lo))
    gamma_min=I(local['log_gain_increment'][0]);agehi=I(local['later_firing_relative_to_T_plus_16'][1])
    learned_min=I('1.8')*exp(I('-.00001')+gamma_min)
    K1=I('.9')/(learned_min*dh(agehi))
    require(logdiff.lo<0<logdiff.hi,'log-gain comparison straddles zero')
    error=I((-K1*I(logdiff.hi)).lo,(-K1*I(logdiff.lo)).hi)
    allowance=I(error.hi)-I(error.lo)
    memory_slope=Gmin*dh(u+w+I('.000000002'))-K*I('.00001')
    require(memory_slope.lo>0,'positive slope including initial charge')
    first_memory=I('.00001')*exp(-10)/memory_slope
    require(first_memory.hi<I('.000000002').lo,'first-head memory bracket')
    memory_out=K1*I('.8')*I((LE*fac).hi)*I((b/B).hi)*I(first_memory.hi)
    fresh_error=error+I(-memory_out.hi,memory_out.hi)
    fresh_allowance=I(fresh_error.hi)-I(fresh_error.lo)
    return {'input_width':str(w.lo),'unlearned_head_log_gain_sensitivity':K0.pair(),
       'first_head_difference':Fdiff.pair(),'reopening_minus_error_start_difference':phase.pair(),
       'error_exponent_difference':exponent.pair(),'log_learning_increment_difference':gamdiff.pair(),
       'learned_log_gain_difference':logdiff.pair(),'learned_head_log_gain_sensitivity':K1.pair(),
       'pointwise_S_theta_minus_S_nominal':error.pair(),'extra_diameter_allowance':allowance.pair(),
       'initial_charge_head_error_bound':first_memory.pair(),'initial_charge_pruning_error_bound':memory_out.pair(),
       'fresh_pointwise_error':fresh_error.pair(),'fresh_extra_diameter_allowance':fresh_allowance.pair(),
       'local_event_checks':local['positive_margins']}


def main():
    p,rp=baseline('results/pruning_certificate.json');t,rt=baseline('comparison_and_bounds.json')
    rows=[]
    for w in ['.0058','.01','.02','.04','.08']:
        v=forcing(w,p,t);rows.append(v)
        print(json.dumps({'w':w,'pointwise_error':v['pointwise_S_theta_minus_S_nominal'],'diameter_allowance':v['extra_diameter_allowance']}),flush=True)
    report={'status':'PASS_UNIFORM_LOCAL_PARAMETER_PERTURBATION_BOUNDS','scope':'Same input profile on both sides; effective independent eta_i in [-1e-5,9e-5], independent physical C,M,LM,LS,LE variations +/-1e-4 and b in [.07999,.08001]. Regenerated and fresh-state versions are reported separately. The fresh version requires first arrival >=20 and includes initial-charge memory; initial auxiliary ERROR tails are included in eta.',
       'rows':rows,'baseline_routes':[rp,rt],'universal_original_source_entry':'NOT_PROVED',
       'warning':'These bounds compare heterogeneous and nominal pruning at the same profile. They are not contraction estimates for the nominal map or for successive profiles.'}
    out=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent/'results/forcing_certificate.json'
    out.write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
