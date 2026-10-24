"""Numerical checks for a conditional dense-front-to-tail induction."""
import json,sys
from pathlib import Path
from directed import I,require
from baselines import baseline

def main():
    tail,rt=baseline('comparison_and_bounds.json');desync,rd=baseline('results/desync_certificate.json');refined,rr=baseline('results/tail_refinement_certificate.json')
    p=tail['profiles'][1];local=next(t for t in desync['tubes'] if t['width']=='.08')
    front=I('.08');eps=I(*p['first_cohort_per_layer_error_upper']);delta=I(*p['synchronized_delay_spread_upper']);c=delta+2*eps
    width64=front+64*c
    certified_physical_width=I(*p['expanded_intermediate_width'])
    require(width64.hi<certified_physical_width.lo,'all safe-prefix heads stay in the old certified physical domain')
    G=I(*local['first_output_gap']);gap64=I(G.lo)-64*2*eps
    require(gap64.lo>I('15.5').hi,'new safe gaps survive every possible prefix perturbation')
    require(width64.hi<I('.11').lo,'old heterogeneous tail already suffices for this reduction')
    require(width64.hi<I('.195').lo,'new heterogeneous tail also accepts output')
    for key,v in local['positive_margins'].items():require(I(*v).lo>0,'local event '+key)
    for key,v in p['margins'].items():require(I(*v).lo>0,'safe-prefix event '+key)
    rows=[]
    for r in range(64):
        n_frozen=64-r
        width=front+n_frozen*c
        rows.append({'original_cohort':2*r,'pruning_passages':r,'frozen_passages':n_frozen,'diameter_upper':str(width.hi)})
    report={'status':'PASS_CONDITIONAL_FRONT_TO_TAIL_REDUCTION',
      'hypotheses':['Entire boundary history is exactly 128 complete translated 8-spaced cohorts X+8k, k=0,...,127, with first arrival >=20; no omitted additional inputs.',
        'Fresh downstream cells in the original full independent parameter/state box.',
        'The actual successive dense-front profiles have diameter <=.08 for every one of the 63 pruning passages. This is a hypothesis, NOT established by this checker.'],
      'front_width_budget':front.pair(),'safe_prefix_one_step_diameter_allowance':c.pair(),
      'layer64_uniform_diameter_upper':str(width64.hi),'layer64_same_lane_gap_lower':str(gap64.lo),
      'available_tail_D':['.11','.195'],'final_cohort_bounds':rows,
      'conclusion':'Under these hypotheses, layer64 contains 64 safe cohorts satisfying a previously certified heterogeneous-tail contract. No learning from this finite train occurs in fresh layers starting at65.',
      'not_proved':['All full-box dense fronts remain in width .08.','Original single-lane-source reachability of this complete translated boundary family.','Additional future input histories.'],
      'baseline_routes':[rt,rd,rr]}
    out=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent/'results/bridge_certificate.json'
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'width64':str(width64.hi),'gap64':str(gap64.lo)}))
if __name__=='__main__':main()
