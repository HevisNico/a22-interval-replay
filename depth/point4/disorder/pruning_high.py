"""Directed six-layer results. Decimal Newton is ONLY a candidate generator.

Every root is enclosed by strict signs checked with the independent finite-series
interval arithmetic in directed.py. No assertion is used as a proof check.
"""
import json
import sys
from decimal import Decimal as D,localcontext
from fractions import Fraction as F
from pathlib import Path
from directed_high import I,A,K,exp,log,h,dh,require,rational


def guess(g,x,start):
    with localcontext() as ctx:
        ctx.prec=130
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
    lo=(I(low_guess)-I('1e-95')).lo
    hi=(I(high_guess)+I('1e-95')).hi
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

