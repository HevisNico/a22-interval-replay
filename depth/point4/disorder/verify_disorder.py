"""Directed b-only half-ring witness; not an original-source campaign."""
import json,sys
from pathlib import Path
from directed_high import I,require
from pruning_high import cell,width

def main():
    x=[I(0)]*12;b=[I('.07999')]*6+[I('.08001')]*6;history=[]
    for n in range(1,64):
        require(width(x)[1].hi<I('.08').lo,'input in local physical tube')
        x=[cell([x[(j-1)%12],x[j],x[(j+1)%12]],b[j]) for j in range(12)]
        lower,upper=width(x)
        require(upper.hi<I('.008').lo,'this witness stays below width .008')
        history.append({'layer':n,'output_profile':[v.pair() for v in x],'diameter':[str(lower.lo),str(upper.hi)]})
        if n%6==0 or n==63:print(json.dumps({'layer':n,'diameter_upper':str(upper.hi)}),flush=True)
    require(I(*history[11]['diameter']).lo>I('.00685').hi,'twelve-step diameter above .00685')
    require(I(*history[62]['diameter']).lo>I('.00781').hi,'sixty-three-step diameter above .00781')
    report={'status':'PASS_DIRECTED_NONALTERNATING_B_WITNESS','scope':'Exact synchronized complete boundary X+8k, k=0,...,127, common initial time >=20; nominal physical parameters and charges except b. The same half-ring b pattern is used in every fresh layer. Not the original single-lane source.',
       'b_by_lane':[str(v.lo) for v in b],'initial_profile':['0']*12,'history':history,
       'conclusion':'An invariant diameter cap .0058 cannot include the synchronized boundary and all independent admissible b patterns. This witness does not leave the local .08 pruning tube and does not refute universal entrance.',
       'universal_original_source_entry':'NOT_PROVED'}
    out=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent/'results/disorder_certificate.json'
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'layer12':history[11]['diameter'],'layer63':history[62]['diameter']}),flush=True)
if __name__=='__main__':main()
