"""Second arithmetic: integer fixed-point outward bounds, no Decimal.

Verifies coarse, explicit root brackets and the critical closure/protection
claims independently of the Decimal result file and root search.
"""
from fractions import Fraction
from pathlib import Path
import json
import sys

S = 10**50


def need(condition, name):
    if not condition:
        raise ArithmeticError(name)


def ceildiv(a, b):
    return -((-a)//b)


class Q:
    def __init__(self, x, y=None, raw=False):
        if isinstance(x, Q):
            self.a, self.b = x.a, x.b
        elif raw:
            self.a, self.b = x, y
        else:
            x, y = Fraction(x), Fraction(x if y is None else y)
            self.a = (x.numerator*S)//x.denominator
            self.b = ceildiv(y.numerator*S, y.denominator)
        need(self.a <= self.b, 'interval order')

    def __add__(x, y):
        y = Q(y)
        return Q(x.a+y.a, x.b+y.b, True)
    __radd__ = __add__

    def __neg__(x):
        return Q(-x.b, -x.a, True)

    def __sub__(x, y):
        return x+-Q(y)

    def __rsub__(x, y):
        return Q(y)+-x

    def __mul__(x, y):
        y = Q(y)
        products = [a*b for a in (x.a,x.b) for b in (y.a,y.b)]
        return Q(min(products)//S, ceildiv(max(products),S), True)
    __rmul__ = __mul__

    def __truediv__(x, y):
        y=Q(y)
        need(y.a>0, 'positive divisor')
        values=[Fraction(a*S,b) for a in (x.a,x.b) for b in (y.a,y.b)]
        low, high=min(values),max(values)
        return Q(low.numerator//low.denominator,
                 ceildiv(high.numerator,high.denominator),True)


def expo(x):
    x=Q(x)
    if x.b <= 0:
        return Q(1)/expo(-x)
    need(x.a>=0,'unmixed exponential sign')
    squares=0
    while x.b>S:
        x=x/2
        squares+=1
    term=total=Q(1)
    for k in range(1,81):
        term=term*x/k
        total=total+term
    tail=term*x/81/(1-x/82)
    value=Q(total.a,total.b+tail.b,True)
    for _ in range(squares):
        value=value*value
    return value


def ln(x):
    x=Q(x)
    need(x.a>=S and x.b<=4*S,'log domain')
    z=(x-1)/(x+1)
    power=z
    total=Q(0)
    for k in range(160):
        total=total+power/(2*k+1)
        power=power*z*z
    tail=power/321/(1-z*z)
    return Q(2*total.a,2*(total.b+tail.b),True)


a=2*ln(2)
k=Q('0.5')


def h(t):
    t=Q(t)
    return a/(a-k)*(expo(-k*t)-expo(-a*t))


def dh(t):
    t=Q(t)
    return a/(a-k)*(a*expo(-a*t)-k*expo(-k*t))


def main():
    rows=[]
    for full,umin_l,umin_u,beta in [
        (False,'0.666556597072780','0.666556597072782','0.0092949'),
        (True,'0.666423402950283','0.666423402950286','0.0091295')]:
        umin=Q(umin_l,umin_u)
        umax=Q('0.666589905698709','0.666589905698712')
        etamax='0.00009' if full else '0.00001'
        glo=Q('1.8')*expo('-0.00001')
        ghi=Q('1.8')*expo(etamax)
        for gain,bracket in [(ghi,umin),(glo,umax)]:
            need((Q('0.1')+gain*h(Q(bracket.a,bracket.a,True))).b<S,'lower root sign')
            need((Q('0.1')+gain*h(Q(bracket.b,bracket.b,True))).a>S,'upper root sign')
        eps=Q('0.000000002' if full else '0')
        spread=Q(umax.b,umax.b,True)-Q(umin.a,umin.a,True)
        width=Q('0.11')+6*(spread+2*eps)
        umaxhi=Q(umax.b,umax.b,True)
        widthhi=Q(width.b,width.b,True)
        gamma=expo(Q('-0.00001')-Q(etamax))*dh(umaxhi+widthhi)/dh(umaxhi)
        product=Q('971')/11664
        for _ in range(6):
            product=product*gamma
        need(product.a>Q(beta).b,'six-step overlap')
        closure=Q(beta)*Q('.11')-6*(spread+2*eps)
        need(closure.a>0,'six-step closure')
        factor=Q('.9999','1.0001')
        endmark=Q('.01999','.02001')+Q('.02')/factor
        errstart=endmark+Q('1.06')/factor
        errend=errstart+Q('.15')/factor
        protection=1+ln('2.5')/Q('.07999','.08001')
        youngest=Q(umin.a,umin.a,True)-widthhi-eps
        oldest=umaxhi+widthhi+eps
        H=Q('15.49999999' if full else '15.5')
        for name,margin in [('mark',youngest-endmark),('raw',1-oldest),
                            ('error_onset',errstart-oldest),
                            ('error_end',youngest+protection-errend),
                            ('aux_clear',H-widthhi-errend)]:
            need(margin.a>0,name)
        recovery=H-widthhi-umaxhi-eps-protection
        need(recovery.a>Q('2.2').b,'recovery >2.2')
        if full:
            need((glo*dh(oldest)-k*Q('.00001')).a>Q('.3').b,'slope >.3')
            need((Q('.00001')*expo(-10)/Q('.3')).b<Q('.000000002').a,'initial charge error')
            need((eps/(1-expo('-.33'))).b<Q('.00000001').a,'summed error')
        rows.append({'profile':'full_fresh_initial_box' if full else 'exact_rest_tail',
                     'overlap_strict_lower':beta,
                     'closure_strict_lower_rational':str(Fraction(closure.a,S)),
                     'recovery_strict_lower_rational':str(Fraction(recovery.a,S))})
    result={'status':'PASS_INDEPENDENT_INTEGER_CRITICAL_CHECKS',
            'arithmetic':'integer fixed point at 50 decimal places; 80-term exp and 160-term atanh log with explicit remainders; no Decimal, floats, third-party libraries or main-result import',
            'profiles':rows,
            'scope':'Independent arithmetic checks of critical numerical inequalities; not an independent mathematical review.'}
    target=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('integer_crosscheck.json')
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'])


if __name__=='__main__':
    main()
