# A22: a heterogeneous tail with independent parameters

23 October 2026 — manual proof with reproducible numerical lemmas.

**Status.** The inequalities in this package have been recomputed using
outward rounding; critical inequalities have also been checked using a
second arithmetic implementation. The mathematical argument below remains
subject to independent expert review. This is not a proof-assistant verification.

## 1. Model, parameters and quantifiers

We retain the A22 equations, its directed graph with 12 periodic lanes, and
the three parents j−1, j, j+1. The tail may have arbitrary depth. Exact source
snapshots, their repository commit and their SHA-256 hashes are included in
`sources/`. Historical status statements in those sources must not be confused
with the status of the v4 release.

The physical constants **C_i, M_i, L_m,i, L_s,i and L_e,i** can be chosen
independently within their relative ±10⁻⁴ intervals, at every port, cell and
layer. They remain fixed in time for a given device. No equality across ports,
lanes or layers is assumed. In this deterministic theorem, “independently”
means that every combination in the Cartesian product of the intervals is
covered; no probability distribution is required.

The principal constants a=ln 4, κ=1/2, r=1/10 and r_m=1/40, the thresholds
and actuation coefficients remain fixed, **as specified by the actual A22
parameter box**. This theorem does not introduce additional perturbations
of those constants.

Set g_nom=(0.3, 1.2, 0.3), δ=10⁻⁵, H=15.5 and D=0.11. Each cell has its
own b∈[0.07999,0.08001] and E∈[50,100]. We establish two variants.

**A — Exact rest.** Initially, all principal and auxiliary units are READY,
q=r and m_i=r_m, with no pending currents. The gains are
g_i=g_nom,i exp(η_i), with independently chosen η_i∈[−δ,δ]. The first input
occurs at a nonnegative time. This directly extends the previously studied tail.

**B — The complete initial box of fresh cells.** At t=0, states satisfy
section 5 of the reference model: q∈r±δ, z_i∈ln(g_nom,i)±δ, b∈0.08±δ;
each auxiliary is either READY with m_i∈r_m±δ, or in its final ERROR phase
with m_i∈[r_m,r_m+δ]. No other earlier pulse or current is allowed. We impose
the additional condition that the **first arrival at the tail is at time ≥20**.
This is an explicit hypothesis, not a conclusion from a new campaign.

In both variants, the upstream boundary supplies the **entire history** as
complete cohorts xᵖ∈R¹², satisfying osc(xᵖ)≤D and xⱼᵖ⁺¹−xⱼᵖ≥H. A
precursor, isolated pulse or incomplete cohort must not be removed to make
an actual history appear to satisfy this contract.

**Conclusion.** Each cohort produces exactly one firing per cell. After any
initial ERROR tails in B have ended, gains and b never change. The cohort
diameter is ≤D at six-layer block boundaries and ≤W at intermediate layers,
with W specified below. Same-lane gaps are ≥15.5 in A and >15.49999999 in B.
Principal and auxiliary units regenerate before the next cohort. The
contract propagates through arbitrarily many layers.

The regenerated head maps contract differences of profiles modulo a common
time translation, in six-layer blocks. Future words whose incoming cohorts
are exact translations of a single profile preserve their intervals exactly,
provided they follow a first cohort that has regenerated the cells. In A,
this holds from the first cohort. In B, the very first response can retain
a small effect of q(0); this effect is bounded rather than set to zero.

## 2. Head equation and uniform bounds

Write

\[
h(u)=\frac{a}{a-\kappa}(e^{-\kappa u}-e^{-au}).
\]

For a regenerated cell, its firing time F=T_j(x) is the first crossing of
1 by r+Σ_i g_i h(F−x_{j+i−1}). The checks below place this crossing after
the last arrival and before the first raw-current ending. Thus the formula
applies to all three ports, without extending a pulse beyond its physical end.

For effective log-gain offsets in [η_−,η_+], define u_− and u_+ by

\[
r+1.8e^{\eta_+}h(u_-)=1,\qquad
r+1.8e^{\eta_-}h(u_+)=1.
\]

Then u_−≤u_+. If l=min x and v=max x,

\[
l+u_-\le T_j(x)\le v+u_+.
\]

The positivity of h' on [0,1], its decrease, strict root-bracket signs and
the absence of an earlier crossing are checked. In particular,
r+δ+G_max h(W)<1 excludes a firing before the last arrival, including the
first input in B.

For A, η_−=−10⁻⁵ and η_+=10⁻⁵. For B, the initial ERROR tails yield
effective offsets in [−10⁻⁵,9·10⁻⁵], as shown in section 6.

On the convex domain K_W={x: osc(x)≤W}, T is order-preserving, commutes with
translations T(x+c1)=T(x)+c1, and is nonexpansive in the sup norm. These
statements concern this domain; we do not assume that the physical model
defines the same map on all of R¹².

## 3. A contraction bound allowing independent ports

Implicit differentiation gives, for the three parents,

\[
\frac{\partial T_j}{\partial x_i}
=\frac{g_{j,i}h'(T_j-x_i)}{\sum_k g_{j,k}h'(T_j-x_k)}.
\]

The Jacobian is positive on each row's three edges and is row-stochastic.
Independent gain factors do not cancel. We retain them through
g_i/Σg_k≥e^(η_−−η_+)p_i, with p=(1/6,2/3,1/6).

The useful improvement is that the ages of the three ports of a single
cell differ by at most W, not 2W. If v is the youngest age at firing, then
v≤u_+ and all other ages lie in [v,v+W]. Moreover,

\[
\frac{d^2}{du^2}\log h'(u)
=-\frac{(a-\kappa)^2a\kappa e^{-(a-\kappa)u}}
{(a e^{-(a-\kappa)u}-\kappa)^2}<0
\]

on the tube. Consequently h'(v+W)/h'(v) decreases with v. Every Jacobian
row dominates γP, where

\[
\gamma=e^{\eta_- -\eta_+}\frac{h'(u_++W)}{h'(u_+)},
\]

and P is the circulant matrix with weights (1/6,2/3,1/6). The code uses
directed upper bounds for u_+ and W, giving a safe lower bound on γ.

Exact rational convolution gives

\[
\rho_6=\min_{r,s}\sum_k\min((P^6)_{rk},(P^6)_{sk})
=\frac{971}{11664}.
\]

For any six layers, which may differ from one another, the Jacobian of
their composition dominates γ⁶P⁶. Its row-overlap coefficient is therefore
at least β=γ⁶ρ₆. Any row-stochastic matrix J with this overlap satisfies
osc(Jz)≤(1−β)osc(z): subtract min(z) and separate the common mass, of size
at least β, of two rows. Integrating the Jacobian along the segment between
two profiles preserves the bound.

**Identical media from one layer to the next are not assumed.**

## 4. Six-layer tube closure

Set Δ=u_+−u_−, bounded using directed endpoints, and ε=0 in A or
ε=2·10⁻⁹ in B. One step increases the diameter by at most Δ+2ε. Choose

\[
W=D+6(\Delta+2\varepsilon).
\]

Starting in K_D, all six steps and the segments used for differentiation
remain in K_W. For the regenerated block B₆=T₆∘⋯∘T₁,

\[
\operatorname{osc}B_6(x)
\le(1-\beta)\operatorname{osc}(x)+6\Delta.
\]

Indeed, osc(B₆(0))≤6Δ and the difference B₆(x)−B₆(0) satisfies the
contraction bound. For B's first cohort, six additional perturbations of
sup norm ≤ε add at most 12ε to the diameter. It therefore suffices to
check βD−6Δ−12ε>0.

The following displayed bounds are conservative. Full endpoints are in
`comparison_and_bounds.json`.

| Quantity | A: exact rest | B: complete fresh initial box |
|---|---:|---:|
| Block-boundary diameter D | 0.11 | 0.11 |
| Intermediate diameter W, upper bound | 0.110200 | 0.111000 |
| u_−, informative approximation | 0.666556597073 | 0.666423402950 |
| u_+, informative approximation | 0.666589905699 | 0.666589905699 |
| Overlap β, strict lower bound | 0.0092949 | 0.0091295 |
| Block-closure slack, strict lower bound | 0.0008225 | 0.00000520 |
| Recovery slack, strict lower bound | 2.2681 | 2.2673 |

The width 0.11 is **not** asserted to be invariant at each individual layer.
The proven invariance is at block boundaries; intermediate excursions are
explicitly included in every physical inequality.

## 5. Protection, regeneration and physical induction

An auxiliary reaches threshold after D_i∈[0.01999,0.02001], even when its
initial READY charge lies in r_m±δ. Both strict root guards and monotonicity
up to that crossing are checked directly. The remaining durations are exactly

\[
D_{m,i}=0.02/(1+\xi_{m,i}),\quad
D_{s,i}=1.06/(1+\xi_{s,i}),\quad
D_{e,i}=0.15/(1+\xi_{e,i}),\qquad |\xi|\le10^{-4}.
\]

The ξ values are independent. Directed endpoints place mark completion
before 0.040013, ERROR onset in [1.099882,1.100119], and ERROR completion
in [1.249867,1.250134]. These displayed intervals are enclosing bounds;
the verifier retains more digits.

Principal protection lasts exactly P(b)=1+ln(2.5)/b when b is unchanged.
Using the head-age interval [u_−−W−ε,u_++W+ε], the verifier establishes
strictly that:

1. every mark ends before firing;
2. firing precedes every raw-pulse ending and every ERROR onset;
3. all ERROR phases and raw currents end before reopening;
4. principal recovery, auxiliary cycles and the outgoing pulse end before
   the relevant next-cohort arrival.

These guards justify the proposed constant-gain, constant-b cycle without
circularity: marks arrive while the principal is READY, so b cannot change;
ERROR currents arrive during protection, so gains cannot change. The
constructed trajectory therefore satisfies the original actuation laws.
Reopening sets q exactly to r, and ERROR completion sets m_i exactly to
r_m; no current survives until the next arrival.

The work bound is recomputed over the full independent parameter box and
remains <500. Hence [50,100] is invariant for E and power gates stay open.
The effective gains remain strictly below C_min.

For A, order preservation and translation yield
T(x^{p+1})≥T(x^p+H1)=T(x^p)+H1, preserving H. Together with tube closure,
these facts give induction over cohorts and layers. Strict margins separate
the transitions that could alter actuation; no arbitrary event priority is
introduced. The order of independent auxiliary events does not affect the
construction.

## 6. Complete fresh initial states without an artificial reset

An initial ERROR tail ends before δ/(L_e,min r_m)<0.001. While the principal
remains READY, its integral increases z_i by exactly 8χ_i, where
χ_i=m_i(0)−r_m∈[0,δ]. For an auxiliary initially READY, set χ_i=0. No gain
cap is reached. The effective gains are therefore fixed before the first
input and equal

\[
g_i^*=g_{\mathrm{nom},i}\exp(\zeta_i+8\chi_i),\quad
|\zeta_i|\le\delta,\quad
-\delta\le\zeta_i+8\chi_i\le9\delta.
\]

There is no initial mark and b does not change. Before any input, the
principal charge is exactly r+αe^(−κt), |α|≤δ. At a first arrival s≥20,
this memory is not zero: its contribution to the head equation is bounded
by δe^(−s/2). The verifier establishes a slope >0.3 throughout the root
tube, including the residual charge term. The first firing differs from
the regenerated head T by at most

\[
\delta e^{-s/2}/0.3<2\cdot10^{-9}.
\]

The root brackets and the guard before the last arrival make this an
estimate of the **first** crossing, not of a subsequently selected zero.
Section 5's guards include this displacement.

The first cohort advances by more than 0.66 per layer. At tail layer n,
s_n≥20+0.66(n−1). Thus ε_n=2·10⁻⁹ exp(−0.33(n−1)) is a valid bound and

\[
\sum_{n\ge1}\varepsilon_n
\le\frac{2\cdot10^{-9}}{1-e^{-0.33}}
<7.116\cdot10^{-9}<10^{-8}.
\]

After the first firing, charges regenerate exactly. Every subsequent
cohort follows T with the same effective gains g*. Only the gap between
cohorts 1 and 2 can lose part of H: at layer n it loses at most ε_n.
It therefore remains >15.49999999. All other gaps remain ≥15.5. Block
closure uses the uniform bound ε and remains strictly positive. This
completes the induction for B.

This extension covers fresh downstream cells in the complete initial box,
**conditional on the incoming history and the minimum time 20**. It does
not prove that every upstream preparation produces such a history.

## 7. Temporal fidelity, causality and scope

If future input cohorts are xᵖ=s_p1+d and follow initial regeneration,
then each T_n commutes with translations for the fixed device, even when
its parameters change between layers. At every depth the output is
s_p1+d_n. The intervals s_{p+1}−s_p are preserved exactly. Arbitrary
training cohorts are not thereby asserted to be translations of one another.

The strictly positive per-layer advance excludes propagation to infinite
depth in finite time. Positive cohort gaps exclude accumulated arrivals
on a port. The local construction therefore defines a consistent infinite
network under the stated entrance contract.

Existing entry certificates remain results about their six prescribed
preparations. This package can be composed with a boundary that actually
satisfies its hypotheses; it does not requalify a campaign over the entire
initial box and does not modify any production result.
