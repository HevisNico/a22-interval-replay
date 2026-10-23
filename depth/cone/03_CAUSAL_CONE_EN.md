# A22: speed ceilings and forward cones

23 October 2026. Point 3, extending the previously delivered points 1–2.

**Status:** manual proofs with numerical lemmas checked by two arithmetic
implementations. Independent expert review is still pending. No new campaign
is used, and production files are unchanged.

## 1. The statement must identify the front being bounded

There are two different results:

1. A tight **cohort-front cone inside the certified heterogeneous tail**.
   This directly complements the limiting speed in point 2.
2. A more conservative **first-activation cone for the original initial
   box**, valid even during learning and without assuming entry into the
   tail contract.

Neither statement is automatically a cone for arbitrary information-bearing
perturbations of an already active, precharged network. In particular, a
lower bound measured from the earliest arrival of a cohort is not the same
as a lower bound measured from every individual parent arrival.

Depth is counted in layers and time in A22 model units. These are directed
graph cones, not isotropic or relativistic light cones.

## 2. Cohort-front cone in the regenerated tail

Use the point-1 entrance contract and its fixed effective gains. Let

\[
h(u)=\frac{a}{a-\kappa}(e^{-\kappa u}-e^{-au}),
\quad a=\log 4,\quad\kappa=\tfrac12,\quad r=0.1.
\]

For independently chosen effective log-gain offsets η_i≤η_max,

\[
\sum_i g_i\le G_{\max}=1.8e^{\eta_{\max}}.
\]

Define u_min as the unique root, in the certified increasing part of h, of

\[
r+G_{\max}h(u_{\min})=1.
\]

This is the smallest synchronized regenerated delay in this gain box.
The cone does not require the three ports' gains to be equal or correlated.

Let m_n^p=min_j t_{n,j}^p be the earliest date of cohort p at tail depth n.
Point 1 ensures that the cell has regenerated, gains remain fixed, and no
previous cohort supplies a residual current. At a time m_{n-1}^p+u with
0≤u<u_min, every contributing age lies in [0,u], while a not-yet-arrived
port contributes zero. Since h is increasing and u_min<1,

\[
q(m_{n-1}^p+u)
\le r+G_{\max}h(u)<1.
\]

No cell can fire before m_{n-1}^p+u_min. Therefore

\[
m_n^p\ge m_{n-1}^p+u_{\min},\qquad
\boxed{\ t_{n,j}^p\ge m_0^p+n u_{\min}\ }.
\]

Equivalently, by elapsed time τ measured from the earliest boundary arrival,
a cohort cannot have reached a depth greater than τ/u_min. Its depth-speed
ceiling is 1/u_min. This is a finite-depth statement, not just an asymptotic
limit and not an estimate from a fitted slope.

The synchronized state with all gains at their allowed upper endpoints
attains the scalar delay in this local response family. This does not
assert that a particular published upstream preparation attains that state.

### Directed numerical bounds

| Tail variant | η_max | Enclosure of u_min | Strict speed ceiling |
|---|---:|---|---:|
| Exact-rest variant A | 10⁻⁵ | [0.666556597072780, 0.666556597072782] | 1.500248 |
| Regenerated responses in full-initial-box variant B | 9·10⁻⁵ | [0.666423402950283, 0.666423402950286] | 1.500548 |

The displayed speed ceilings are rounded upward. Both root signs and
reciprocal bounds are checked in `verify_cone.py`, using directed Decimal
arithmetic and a separate integer fixed-point implementation.

## 3. The first physical cohort of the full initial box

Variant B does not replace q(0) by exact rest. Point 1 proves, when its first
incoming cohort arrives at time ≥20, that the first response at tail layer k
differs from the regenerated map by at most

\[
\varepsilon_k=2\cdot10^{-9}e^{-0.33(k-1)},
\qquad
\sum_{k\ge1}\varepsilon_k<10^{-8}.
\]

Consequently the sharper first-cohort cone is

\[
\boxed{\ t_{n,j}^{1}\ge m_0^{1}+n u_{\min}
-\sum_{k=1}^{n}\varepsilon_k\ }.
\]

A simple linear cone with no additive offset follows from
d_B=u_min−2·10⁻⁹>0:

\[
t_{n,j}^{1}\ge m_0^{1}+n d_B,
\qquad \frac1{d_B}<1.500548.
\]

Thus the same displayed ceiling 1.500548 covers both the first physical
cohort and later regenerated cohorts in variant B. The tiny correction is
retained in the certificate rather than silently omitted.

The entrance contract and the first-arrival condition ≥20 are still
hypotheses. This result does not establish universal entrance into that
contract.

## 4. Relation to the ergodic speed

For any stationary ergodic medium law covered by point 2,

\[
u_{\min}\le\gamma(\mathbb P)\le u_{\max},
\qquad
v_{\mathrm{typ}}(\mathbb P)=\frac1{\gamma(\mathbb P)}
\le\frac1{u_{\min}}.
\]

The same ceiling applies to every law supported in the stated box. The
typical speed can depend on the joint law and its correlations. The
ceiling comes from the allowed box, not from a chosen random distribution.
The summable first-cohort correction disappears after division by depth.

Thus the two statements fit together: a law-dependent typical speed and
a distribution-independent upper bound within the specified tail class.
The speed need not attain the upper bound.

## 5. A first-activation cone valid during learning

This separate bound needs no cohort matching, no six-layer contraction,
no frozen gains and no learning-entry certificate.

Assume the original complete initial box at t=0, no hidden incoming pulses
or delayed principal currents, and the A22 feedforward graph. Let s_0≥0
be the first external source-pulse time. Each port carries at most one
active canonical pulse; this is part of the model's input class. The
original source and principal refractory dynamics obey this restriction.

All gains are capped by C_max=4(1+10⁻⁴)=4.0004, even during learning.
Each canonical current is bounded by a=ln 4, so total admitted current is
at most

\[
J=3C_{\max}a.
\]

Before any incoming current, the main charge remains below threshold and
relaxes toward r. Initial auxiliary ERROR tails can alter gains but do not
directly charge the principal. Hence at any input-free boundary time b,
q(b)≤r+δ, where δ=10⁻⁵, and the principal has not fired autonomously.

Until its first firing, comparison with
Q'=κ(r−Q)+J, Q(0)=r+δ gives

\[
q(b+\tau)\le Q(\tau)
=r+\delta e^{-\kappa\tau}
+\frac J\kappa(1-e^{-\kappa\tau}).
\]

This envelope reaches 1 at

\[
d_{\mathrm{global}}
=\frac1\kappa\log\!left(
\frac{J-\kappa\delta}{J-\kappa(1-r)}\right)>0.
\]

For τ<d_global, Q(τ)<1, so the physical first firing cannot yet occur.
Learning cannot invalidate the comparison because the gain cap is retained.

Induct on layers. No layer-1 current can arrive before s_0, so its first
emission is no earlier than s_0+d_global. If layer n−1 emits nothing before
s_0+(n−1)d_global, layer n receives no current before that boundary, and
the same comparison applies. Thus

\[
\boxed{\ \text{no layer-}n\text{ emission before }
s_0+n d_{\mathrm{global}}\ }.
\]

Layers that never fire satisfy the statement trivially. In particular,
first activation cannot reach infinite depth in finite time.

The numerical checks give

\[
0.05484010375122<d_{\mathrm{global}}<0.05484010375123,
\qquad
\frac1{d_{\mathrm{global}}}<18.234831.
\]

This ceiling is intentionally conservative. It replaces decaying pulses
and actual gains by the maximum sustained admissible current. It is not
claimed to be the fastest physically attainable A22 device. Its advantage
is that it holds over the original initial box even before the tail regime
has been established. It does not prove that the regime will be reached.

## 6. Why “no signal is faster” needs qualification

The cohort cone is measured from the cohort's **earliest boundary arrival**.
It does not assert T_j(x)−x_i≥u_min for every individual parent i. Earlier
parents can have charged the cell before a later parent arrives.

More generally, outside the regenerated contract, a READY principal may
already be close to threshold. From q=1−ε, an arriving positive current
with positive net slope can cause a crossing in a time tending to zero
with ε. The original initial box is far from threshold, but an already
active trajectory need not be. A fresh-cell delay bound therefore cannot
simply be reused as a universal waiting time for arbitrary interventions
in an active network.

The valid wording is:

> Every admitted cohort in the certified tail obeys the stated forward
> cone. Separately, first activation from the original input-free initial
> box obeys the global gain-cap cone.

No general information cone for perturbations of an active network,
isotropy or Lorentz invariance is established here.
