"""Directed decimal intervals; finite series with explicit remainder bounds.

No binary floats, Decimal.exp/ln, NumPy, SciPy or A22 engine imports.
The arithmetic trusts Python's decimal directed basic operations.
"""
from decimal import Decimal, Context, ROUND_FLOOR, ROUND_CEILING

LOW = Context(prec=70, rounding=ROUND_FLOOR)
HIGH = Context(prec=70, rounding=ROUND_CEILING)


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


class I:
    def __init__(self, lo, hi=None):
        if isinstance(lo, I):
            self.lo, self.hi = lo.lo, lo.hi
            return
        require(not isinstance(lo, float) and not isinstance(hi, float), "No float endpoints")
        self.lo = Decimal(str(lo))
        self.hi = self.lo if hi is None else Decimal(str(hi))
        require(self.lo.is_finite() and self.hi.is_finite() and self.lo <= self.hi,
                "Invalid finite interval")

    def __add__(a, b):
        b = I(b)
        return I(LOW.add(a.lo, b.lo), HIGH.add(a.hi, b.hi))

    __radd__ = __add__

    def __neg__(a):
        return I(a.hi.copy_negate(), a.lo.copy_negate())

    def __sub__(a, b):
        return a + -I(b)

    def __rsub__(a, b):
        return I(b) + -a

    def __mul__(a, b):
        b = I(b)
        pairs = [(x, y) for x in (a.lo, a.hi) for y in (b.lo, b.hi)]
        return I(min(LOW.multiply(x, y) for x, y in pairs),
                 max(HIGH.multiply(x, y) for x, y in pairs))

    __rmul__ = __mul__

    def __truediv__(a, b):
        b = I(b)
        require(not b.lo <= 0 <= b.hi, "Division through zero")
        pairs = [(x, y) for x in (a.lo, a.hi) for y in (b.lo, b.hi)]
        return I(min(LOW.divide(x, y) for x, y in pairs),
                 max(HIGH.divide(x, y) for x, y in pairs))

    def __pow__(a, n):
        require(isinstance(n, int) and n >= 0, "Only nonnegative integer powers")
        result = I(1)
        for _ in range(n):
            result = result * a
        return result

    def pair(a):
        return [str(a.lo), str(a.hi)]


def rational(x):
    return I(x.numerator) / I(x.denominator)


def _exp_small_nonnegative(x):
    require(0 <= x.lo <= x.hi <= 1, "Exponential series domain")
    term = total = I(1)
    for k in range(1, 91):
        term = term * x / k
        total = total + term
    # First omitted term x^91/91!, all subsequent ratios at most x/92.
    tail = term * x / 91 / (I(1) - x / 92)
    return I(total.lo, HIGH.add(total.hi, tail.hi))


def _exp_endpoint(x):
    if x < 0:
        return I(1) / _exp_endpoint(x.copy_negate())
    y, squares = I(x), 0
    while y.hi > 1:
        y = y / 2
        squares += 1
    answer = _exp_small_nonnegative(y)
    for _ in range(squares):
        answer = answer * answer
    return answer


def exp(x):
    x = I(x)
    return I(_exp_endpoint(x.lo).lo, _exp_endpoint(x.hi).hi)


def log(x):
    x = I(x)
    require(1 <= x.lo <= x.hi <= 4, "Logarithm series domain")
    y = (x - 1) / (x + 1)
    y2, term, total = y * y, y, I(0)
    for k in range(250):
        total = total + term / (2*k + 1)
        term = term * y2
    tail = term / 501 / (I(1) - y2)
    return I((2*total).lo, (2*(total + tail)).hi)


A = 2 * log(2)
K = I('.5')


def h(u):
    u = I(u)
    require(0 <= u.lo <= u.hi <= 1, "Pulse response domain")
    return A/(A-K) * (exp(-K*u) - exp(-A*u))


def dh(u):
    u = I(u)
    require(0 <= u.lo <= u.hi <= 1, "Pulse derivative domain")
    return A/(A-K) * (A*exp(-A*u) - K*exp(-K*u))
