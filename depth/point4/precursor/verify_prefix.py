"""Finite inequalities for an analytic precursor lemma, not a layer campaign.

Inputs: authenticated layer-18 data extracted by inspect_boundary.py.
Uses the unchanged finite-series interval arithmetic supplied in point4_disorder_EN.
"""
import hashlib, json
from pathlib import Path
from fractions import Fraction as F
from inspect_boundary import EXPECTED, pair, need
from directed import I, exp, log, h, dh, require

ROOT=Path(__file__).resolve().parent

def main():
    data=json.loads((ROOT/'results/boundary.json').read_text())
    need(data['archive_sha256']==EXPECTED,'source identity')
    rows=data['cells'];tr=[[tuple(map(F,p)) for p in c['dates']] for c in rows]
    lanes=(0,1,11);p=[tr[j][0] for j in lanes]
    early_lo=min(x[0] for x in p);early_hi=max(x[1] for x in p)
    aligned=[t[int(j in lanes):] for j,t in enumerate(tr)]
    need(all(len(t)==104 for t in aligned),'complete cohort counts')
    windows=[]
    for k in range(104):
        ps=[t[k] for t in aligned]
        need(k==0 or max(t[k-1][1] for t in aligned)<min(x[0] for x in ps),'disjoint cohort windows')
        local=[]
        for j in range(12):
            qq=[ps[i%12] for i in (j-1,j,j+1)]
            local.append(pair((max(a for a,b in qq)-min(b for a,b in qq),max(b for a,b in qq)-min(a for a,b in qq))))
        windows.append({'index':k,'date_window':pair((min(a for a,b in ps),max(b for a,b in ps))),
                        'diameter':pair((max(a for a,b in ps)-min(b for a,b in ps),max(b for a,b in ps)-min(a for a,b in ps))),
                        'local_triplet_diameters':local})
    safe_gaps=[(t[k+1][0]-t[k][1],t[k+1][1]-t[k][0]) for t in aligned for k in range(3)]
    min_safe=min(a for a,b in safe_gaps)
    need(min_safe>F('15.5'),'first four complete cohorts have safe same-lane gaps')
    next_lo=min(t[0][0] for t in aligned)
    W=I(*pair((early_hi-early_lo,early_hi-early_lo)))
    tmin=I(*pair((early_lo,early_lo)));tmax=I(*pair((early_hi,early_hi)))
    eta=I('-.00001','.00009');gainfac=exp(eta);delta=I('.00001')
    # Inherited auxiliary threshold bracket is checked directly here.
    # Initial READY auxiliary error after time >=20 is bounded by delta*exp(-10).
    # Initial terminal ERROR states have returned exactly to r_m long before.
    nominal_M=I('.975')/h(I('.02'))
    M=nominal_M*I('.9999','1.0001');auxmem=delta*exp(-10)
    d=I('.01999','.02001')
    require((M*h(I(d.lo))+auxmem).hi<I('.975').lo,'auxiliary lower root sign')
    require((M*h(I(d.hi))-auxmem).lo>I('.975').hi,'auxiliary upper root sign')
    # For h', a*exp(-a*u)/(k*exp(-k*u)) decreases in u; dh(1)>0
    # therefore proves positivity throughout [0,1].
    require(dh(I(1)).lo>0,'pulse response is increasing on [0,1]')
    require((M*dh(1)-auxmem/2).lo>0,'auxiliary first crossing is strictly increasing on [0,1]')
    LM=log(I('1.25'))/I('.02')*I('.9999','1.0001')
    LS=3*log(2)/I('1.06')*I('.9999','1.0001')
    LE=log(4)/I('.15')*I('.9999','1.0001')
    dm=log(I('1.25'))/LM;ds=3*log(2)/LS;de=log(4)/LE
    error_start=d+dm+ds;error_end=error_start+de
    require((2*delta/(LE*I('.025'))).hi<I('.001').lo,'initial ERROR over by .001')
    # These are excess charges above r, compared with threshold excess .9.
    charge_two=I('1.5')*gainfac*h(1)+delta
    charge_side=I('.3')*gainfac*h(1)+delta
    charge_one=I('1.2')*gainfac*h(1)+delta
    require(charge_two.hi<I('.9').lo,'two fresh ports cannot fire')
    require(charge_one.hi<I('.9').lo,'one fresh port cannot fire')
    early_head=I('1.8')*gainfac*h(I('.6'))+delta
    late_head=I('1.8')*gainfac*h(I('.8'))-delta
    require(early_head.hi<I('.9').lo,'three-port head later than min arrival + .6')
    require(late_head.lo>I('.9').hi,'three-port head before max arrival + .8')
    require((I('1.8')*I(gainfac.lo)*dh(1)-delta/2).lo>0,'head strictly increasing on live-pulse interval')
    require((W+I('.8')).hi<1,'all pulses live at upper head bracket')
    require((W+d+dm).hi<I('.6').lo,'all marks finish before first possible firing')
    require(error_start.lo>(1+W).hi,'all raw pulses end before any error')
    require(error_start.lo>(W+I('.8')).hi,'all errors start after firing')
    require((W+error_end).hi<I('1.6').lo,'all errors end during the FAST phase')
    F19=I((tmin+I('.6')).lo,(tmax+I('.8')).hi)
    b=I('.07999','.08001');reopen19=F19+1+log(I('2.5'))/b
    section=I(174)
    require(reopen19.hi<section.lo,'lane 0 regenerated before the section')
    require((tmax+error_end).hi<section.lo,'all layer-19 auxiliaries regenerated')
    require((F19+error_end).hi<section.lo,'all layer-20 precursor errors completed')
    require(section.hi<I(*pair((next_lo,next_lo))).lo,'section before any later boundary arrival')
    adapted_max=I('1.2')*exp(eta+I('.6'))
    require(adapted_max.hi<I('3.9996').lo,'no gain cap can clip the .6 increment')
    # For silent cells after every raw end: exact convolution + decaying q(0)-r.
    # A common time section gives outer bounds for residual charge, not a reset.
    mem=delta*exp(-section/2)
    def residual(gain_sum,arrival):
        tail=I(gain_sum)*gainfac*h(1)*exp(-(section-arrival-1)/2)
        return tail+I(-mem.hi,mem.hi)
    arrival19=I(tmin.lo,tmax.hi)
    q19_two=residual('1.5',arrival19);q19_side=residual('.3',arrival19)
    q20_center=residual('1.2',F19);q20_side=residual('.3',F19)
    for name,q in [('19_two',q19_two),('19_side',q19_side),('20_center',q20_center),('20_side',q20_side)]:
        require(q.lo>I('.00001').hi,'positive charge memory outside fresh box: '+name)
    report={
      'status':'MANUAL_PRECURSOR_LEMMA_WITH_PASSING_FINITE_INEQUALITIES; OBLIGATION_B_OPEN',
      'archive_sha256':EXPECTED,'boundary_json_sha256':hashlib.sha256((ROOT/'results/boundary.json').read_bytes()).hexdigest(),
      'scope':'No engine import or layer campaign. Only leading precursor consequences; later complete cohorts are not propagated.',
      'precursor_lanes':[11,0,1],'precursor_window':pair((early_lo,early_hi)),
      'first_complete_arrival_lower':pair((next_lo,next_lo))[0],
      'minimum_same_lane_gap_among_first_four_complete_cohorts':pair((min_safe,min_safe))[0],
      'complete_cohort_count':104,'cohorts':windows,
      'intervals':{name:value.pair() for name,value in {
        'precursor_width':W,'h1':h(1),'dh1':dh(1),'auxiliary_first_delay':d,
        'auxiliary_error_start':error_start,'auxiliary_error_end':error_end,
        'two_port_max_excess_charge':charge_two,'one_side_max_excess_charge':charge_side,
        'one_center_max_excess_charge':charge_one,'three_port_charge_at_lower_head_bound':early_head,
        'three_port_charge_at_upper_head_bound':late_head,'only_precursor_firing_time_at_19':F19,
        'reopening_at_19_lane_0':reopen19,'maximum_adapted_gain':adapted_max,
        'q_minus_r_at_174_layer19_two_ports':q19_two,'q_minus_r_at_174_layer19_side_port':q19_side,
        'q_minus_r_at_174_layer20_center_port':q20_center,'q_minus_r_at_174_layer20_side_port':q20_side,
        'gain_multiplier':exp(I('.6'))}.items()},
      'layer19_precursor_spikes':[0], 'layer20_precursor_spikes':[],
      'layer19_log_gain_increments':{'0':[0,0,0],'1':['.6','.6',0],'2':['.6',0,0],'10':[0,0,'.6'],'11':[0,'.6','.6']},
      'layer20_log_gain_increments':{'0':[0,'.6',0],'1':['.6',0,0],'11':[0,0,'.6']},
      'b_increment_from_precursor_all_cells_both_layers':0,
      'unlisted_gain_increments':0,
      'not_proved':['Processing of the later complete cohorts by layers 19 or 20.',
                    'Recovery of a fresh-state bridge interface after the prefix.',
                    'A <= .08 dense-front tube or universal entry.']}
    (ROOT/'results/prefix_certificate.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('status','precursor_window','first_complete_arrival_lower','minimum_same_lane_gap_among_first_four_complete_cohorts','intervals')},indent=2))
if __name__=='__main__':main()
