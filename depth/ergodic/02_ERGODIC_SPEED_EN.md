# A22: deterministic speed in a stationary ergodic medium

23 October 2026 — application of Kingman's subadditive ergodic theorem to
the heterogeneous contract in `01_HETEROGENEOUS_TAIL_EN.md`.

**Status.** A manual derivation developed in this package, based on a
classical ergodic theorem and the attached verifiable inequalities. It
has not received independent expert review. No random sampling or new
propagation campaign is used as a proof.

## 1. Precise statement

Let (Ω,F,P,θ) be a probability-preserving **ergodic** dynamical system.
The environment of layer n is the field of its 12 cells and 3 ports given
by ω_n=θ^{n−1}ω. Constants and effective gains belong to the boxes of the
heterogeneous-tail theorem. The law concerns the complete field, including
initial states when variant B is used.

Assume measurable parameters. Layers may be dependent: stationarity and
ergodicity suffice. Independent identically distributed layers satisfy
these assumptions. Correlations between ports or lanes within a layer are
allowed. Independent cells with fixed laws for each port type are a
particular case.

For almost every environment ω, there is one **deterministic constant**
γ(P)>0 such that, for every finite preparation whose entrance satisfies
the contract, every lane j and each admissible cohort p,

\[
\lim_{n\to\infty}\frac{t_{n,j}^{p}}{n}=\gamma(P),
\qquad v(P)=\frac1{\gamma(P)}.
\]

Depth n is measured from tail entry; adding a finite prefix depth or
subtracting a finite entrance date does not change the limit. Speed v
is measured in layers per model time unit.

The same probability-one event works for **all** entrance profiles with
diameter ≤D. This is not an unjustified uncountable intersection of
almost-sure events. It also accommodates entry at a random finite depth,
after intersecting over the integer shifts of the environment.

The deterministic bounds are u_−≤γ(P)≤u_+, with the roots of the relevant
variant. Existence is established without selecting a specific numerical
law. A single value of γ is not asserted for all laws.

## 2. Regenerated maps and admissible orbits

For a fixed environment, let T_ω be its layer's regenerated head map and set

\[
F_n(\omega,x)=T_{\theta^{n-1}\omega}\circ\cdots\circ T_\omega(x).
\]

For x∈K_D, the tail proof makes this composition well-defined at every
depth, with osc(F_n(ω,x))≤W. Each six-layer block returns the diameter
to D. This is uniform over **every** admissible sequence of parameters,
not just over typical realizations.

Roots are simple and uniformly separated from pulse endings, and the
coefficients are measurable. The implicit head map is continuous in its
parameters and dates on the tube; consequently F_n is measurable.

The maps T are needed only on K_W. We do not assume an unproved physical
order-preserving extension to all of R¹². Comparisons below use only two
orbits both certified to remain in K_W. This domain is convex and invariant
under common translation, so derivative-based and order comparisons are valid.

## 3. Explicit subadditive construction

For the reference orbit starting at x=0, define

\[
U_n(\omega)=\max_j F_n(\omega,0)_j,\qquad
L_n(\omega)=\min_j F_n(\omega,0)_j.
\]

Since L_m1≤F_m(ω,0)≤U_m1, order preservation and translation, propagated
along the two admissible orbits, give

\[
U_{m+n}(\omega)\le U_m(\omega)+U_n(\theta^m\omega),
\]
\[
L_{m+n}(\omega)\ge L_m(\omega)+L_n(\theta^m\omega).
\]

The shifted orbit F_n(θ^mω,0) is admissible because it starts in K_D. The
other orbit continues the original orbit, so it too stays in K_W, even
when section m is not a block boundary. This avoids falsely assuming that
K_W is invariant from every arbitrary starting point in K_W.

The synchronized bounds imply

\[
n u_-\le L_n\le U_n\le n u_+,
\qquad 0\le U_n-L_n\le W.
\]

Thus U_n is integrable and satisfies Kingman's hypotheses: stationarity
through θ, subadditivity, an integrable upper bound and an integrable linear
lower bound. Kingman's theorem gives U_n/n→γ(ω) almost surely and in L¹.
Ergodicity makes γ(ω) constant almost surely.

Since (U_n−L_n)/n≤W/n→0, L_n/n has the same limit, as does every
coordinate F_n(ω,0)_j/n. Contraction establishes the bounded tube. Once
that tube is available, no additional random-product theorem is needed
for this law of large numbers.

The proof uses the **one-layer** shift θ. It does not assume that
ergodicity of θ implies ergodicity of θ⁶; that implication would be false
in general.

## 4. Every admitted preparation and every lane

For every x∈K_D, the deterministic comparisons

\[
\min(x)1+F_n(\omega,0)
\le F_n(\omega,x)
\le\max(x)1+F_n(\omega,0)
\]

hold simultaneously for all x. On the single event where the reference
orbit converges, they therefore give the limit for every entrance profile,
even one selected as a function of the environment. Independence of the
preparation and the tail is unnecessary.

For two profiles x,y in the same environment, moreover,

\[
\operatorname{osc}\big(F_{6k}(\omega,x)-F_{6k}(\omega,y)\big)
\le(1-\beta)^k\operatorname{osc}(x-y).
\]

Contraction concerns the relative front profile, not its time origin. A
common phase displacement can survive. In a random medium, the normalized
profile can keep changing between layers; convergence to a fixed spatial
profile is neither required nor claimed.

The preparations being compared change the finite upstream prefix or the
entrance profile. Changing the gain law throughout the downstream tail
changes the statistical medium and can change γ. Different realizations
drawn from the same ergodic law have the same speed almost surely.

## 5. First cohort for the complete initial box

In variant B, the map of the very first physical response depends on
absolute time through q(0)−r. It therefore does not commute exactly with
translations. **Kingman is not applied to that map.**

Kingman is applied to the regenerated cocycle T, with local effective gains
g_i*=g_nom,i exp(ζ_i+8χ_i). This field is a measurable factor of the initial
stationary ergodic field and is itself stationary ergodic.

Let z_n be the first cohort's physical orbit, and y_n=F_n(ω,z_0) its
regenerated comparison orbit. The first proof gives

\[
z_n=T_{\theta^{n-1}\omega}(z_{n-1})+e_n,
\quad\|e_n\|_\infty\le\varepsilon_n,
\quad\sum_n\varepsilon_n<10^{-8}.
\]

Both orbits remain in the tube. Nonexpansiveness yields
||z_n−y_n||∞≤Σ_{k≤n}ε_k<10⁻⁸. Their difference divided by n tends to zero,
so they have the same speed. Later cohorts follow the regenerated maps
exactly, and section 4 applies directly.

The minimum time 20 and the entire-history entrance condition remain
necessary hypotheses of this variant; this comparison does not remove them.

## 6. What “a statistical property of the medium” means

Kingman's characterization gives

\[
\gamma(P)=\inf_{n\ge1}\frac{\mathbb E_P U_n}{n}
=\sup_{n\ge1}\frac{\mathbb E_P L_n}{n},
\qquad
\frac{\mathbb E_P L_n}{n}\le\gamma(P)\le
\frac{\mathbb E_P U_n}{n}.
\]

The enclosing bounds differ by at most W/n. These formulas characterize γ;
they do not claim to evaluate expectations for an unspecified law.

Here the “statistics” mean the **joint law of the medium**, including
spatial and inter-layer correlations. Equal means or equal marginal laws
do not generally identify two media's dynamics. For i.i.d. layers, the
law of one complete layer determines the process and therefore γ.

An A22-specific simplification must be explicit. Inside the contract,
T depends on the **effective gains**, h and the graph. Auxiliary constants
and b no longer enter the head date; they guarantee protection and
regeneration. If only C,M,L_m,L_s,L_e are disordered while all gains stay
nominal, then γ=u_0 exactly. Disorder in effective gains is needed here
for a nontrivial statistical speed different from that of the nominal
medium. In variant B, initial auxiliary ERROR tails can change those gains.

## 7. Why ergodicity matters; counterexamples

Stationarity alone does not imply a deterministic constant. For example,
flip one coin at the outset and choose either the entirely homogeneous
η=+δ medium or the entirely homogeneous η=−δ medium. This process is
stationary but not ergodic. Its limiting duration is the corresponding
homogeneous duration, and the certificate separates those two values strictly.

Deterministic alternating blocks of dominating lengths are not automatically
covered by a stationary ergodic law, and their mean duration can fail to
converge. However, “deliberately constructed” is not the mathematical
criterion: a periodic structure with a uniformly random initial phase can
be stationary ergodic. The distinction is the precise probabilistic
hypothesis and the almost-sure nature of the conclusion.

## 8. Limits and references

This proof does not establish entry into the contract for all upstream
initial preparations. It does not compute γ for an unspecified distribution,
give a central limit theorem, or establish isotropy or Lorentz invariance.
Speed is propagation speed on the directed graph in model units.

The probabilistic tool is classical. This package's contribution is to
verify its hypotheses for the A22 tail, including the restricted domain of
the head map and the first unregenerated response. It is not a new general
ergodic theorem.

- J. F. C. Kingman, *The Ergodic Theory of Subadditive Stochastic Processes*,
  JRSS B 30 (1968), 499–510.
  https://doi.org/10.1111/j.2517-6161.1968.tb00749.x
- J. Michael Steele, *Kingman's subadditive ergodic theorem*, Ann. IHP
  Probabilités et Statistiques 25 (1989), 93–98.
  https://www.numdam.org/item/AIHPB_1989__25_1_93_0/
- Glenn Merlet, *Limit theorems for iterated random topical operators*,
  arXiv:math/0503634v2, particularly §1.2 for the law-of-large-numbers context.
  https://arxiv.org/abs/math/0503634v2
  Stronger results in that paper require additional hypotheses, including
  a memory-loss property; those results are not automatically invoked here.
- Stéphane Gaubert and Zheng Qu, *Dobrushin's ergodicity coefficient for
  Markov operators on cones*, IEOT 81 (2015), 127–150.
  https://arxiv.org/abs/1307.4649
  The row-overlap argument used here is the classical stochastic-matrix case.
