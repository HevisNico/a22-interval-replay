"""One directed heterogeneous endpoint assignment, not a cover of the box."""
import json,sys
from pathlib import Path
from directed_high import I,A,exp,log,h,require
from pruning_high import enclosed_root,width


def parameters(factor,eta,b):
    f=I(factor);lm=log('1.25')/I('.02')*f;le=A/I('.15')*f
    aux_equivalent=I('.3')/h('.02')*f
    d=enclosed_root([aux_equivalent]*3,[I(0)]*3,'.02')
    return {'factor':f,'eta':I(eta),'b':I(b),'lm':lm,'le':le,'d':d,
            'dm':I('.02')/f,'ds':I('1.06')/f,'de':I('.15')/f,
            'g':[I(v)*exp(eta) for v in ['.3','1.2','.3']]}


def cell(x,p):
    g=p['g'];b=p['b'];d=p['d'];dm=p['dm'];ds=p['ds'];de=p['de'];lm=p['lm'];le=p['le'];B=b+I('.3')
    first=enclosed_root(g,x,'.6666')
    R=(log('2.5')+b*(first+1)+I('.1')*sum((8+t+d for t in x),I(0))-I('1.2')*dm+I('.3')/lm)/B
    gamma=[]
    for t in x:
        v=I('.8')*exp(-le*(R-t-8-d-dm-ds))-I('.2')
        gamma.append(I(max(I(0).lo,min(I('.6').lo,v.lo)),max(I(0).hi,min(I('.6').hi,v.hi))))
    gs=[gi*exp(ga) for gi,ga in zip(g,gamma)]
    out=enclosed_root(gs,x,'.27');xmin=I(min(t.lo for t in x));xmax=I(max(t.hi for t in x))
    markend=d+dm;errorstart=markend+ds;errorend=errorstart+de
    margins={'first_marks_before_fire':first-xmax-markend,
       'first_errors_protected':first+1+log('2.5')/b-xmax-errorend,
       'fast_phase_before_second_marks':8+xmin+d-first-1,
       'second_marks_begin_before_unadjusted_reopening':first+1+log('2.5')/b-8-xmax-markend,
       'second_marks_end_before_reopening':R-8-xmax-markend,
       'second_raw_fully_blocked':R-9-xmax,
       'reopening_before_second_errors_end':8+xmin+errorend-R,
       'errors_finish_before_third':8+xmin-xmax-errorend,
       'later_marks_before_fire':out-xmax-markend,
       'later_fire_before_errors':xmin+errorstart-out,
       'later_errors_protected':out+1+log('2.5')/B-xmax-errorend,
       'later_regenerated':8+xmin-out-1-log('2.5')/B,
       'new_gap_exceeds_15_5':16+out-first-I('15.5'),
       'b_cap':I('1.1')-B,'gain_cap':I('3.9996')-I(max(gi.hi for gi in gs))}
    for name,value in margins.items():require(value.lo>0,name)
    return out,{k:str(v.lo) for k,v in margins.items()}


def main():
    late=parameters('1.0001','-.00001','.07999');early=parameters('.9999','.00009','.08001')
    ps=[late]*6+[early]*6;x=[I(0)]*12;history=[]
    for n in range(1,64):
        require(width(x)[1].hi<I('.08').lo,'local input domain')
        cells=[cell([x[(j-1)%12],x[j],x[(j+1)%12]],ps[j]) for j in range(12)]
        x=[v[0] for v in cells];lo,hi=width(x)
        require(hi.hi<I('.012').lo,'selected history stays below .012')
        history.append({'layer':n,'output_profile':[v.pair() for v in x],'diameter':[str(lo.lo),str(hi.hi)],
          'minimum_cell_event_margins':{k:str(min(I(v[1][k]).lo for v in cells)) for k in cells[0][1]}})
        if n%6==0 or n==63:print(json.dumps({'layer':n,'diameter_upper':str(hi.hi)}),flush=True)
    require(I(*history[11]['diameter']).lo>I('.01044').hi,'width at layer12')
    require(I(*history[-1]['diameter']).lo>I('.01110').hi,'width at layer63')
    summary=[]
    for p in [late,early]:summary.append({k:(v.pair() if isinstance(v,I) else [a.pair() for a in v]) for k,v in p.items()})
    report={'status':'PASS_ONE_FULL_PARAMETER_ENDPOINT_ASSIGNMENT','scope':'One admissible assignment with parameters coherent within each cell and within each half-ring; not all independent combinations. Complete synchronized 128-cohort boundary, first time >=20. Not the original lane-0 source.',
      'parameters_for_lanes_0_to_5_and_6_to_11':summary,
      'initial_state_realization':'q=r and E=75 everywhere. Lanes0..5: z=ln(g_nom)-1e-5, auxiliaries READY at rm. Lanes6..11: z=ln(g_nom)+1e-5 and auxiliaries initially in final ERROR at rm+1e-5, producing +8e-5 log-gain before first input. C may be nominal; M,LM,LS,LE use the recorded factor.',
      'history':history,'universal_original_source_entry':'NOT_PROVED'}
    out=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent/'results/full_corner_certificate.json'
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'layer12':history[11]['diameter'],'layer63':history[-1]['diameter']}))
if __name__=='__main__':main()
