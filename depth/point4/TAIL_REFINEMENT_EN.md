# A22: a wider full-box heterogeneous tail by sharper Jacobian bounds

23 October 2026

**New working contract: D=0.195 at five-layer block boundaries.** All physical parameter variations and fresh initial states covered by the earlier heterogeneous-tail theorem remain covered. The same entrance hypotheses remain necessary: the entire input history consists of complete cohorts, same-lane gaps are at least 15.5, and the first arrival is at time at least 20. This is not an entrance proof for the original source.

The earlier optimization in `TAIL_BUDGET_EN.md` found a maximum near 0.12143 for the coarse minorization J>=gamma P. A sharper entrywise bound extends that result. The new certificate's width supremum is in

    [0.1950798211, 0.1950798214].

Five is the optimal block length within the new minorization family. The working width 0.195 is below this supremum and has strictly positive closure margin. Neither supremum is claimed to be a physical maximum or the best width attainable by any proof.

## 1. The sharper bound

Retain the pulse response h, synchronized delay upper bound u_plus, gain-offset bounds eta_minus=-0.00001 and eta_plus=0.00009, and intermediate width W from the heterogeneous-tail proof. Let

\[
 \gamma=e^{-0.0001}\frac{h'(u_++W)}{h'(u_+)}.
\]

The previous proof establishes a common bound on the ratio between any two port response derivatives. In particular, for every pair of ports k,i,

\[
 \frac{g_kh'(F-x_k)}{g_ih'(F-x_i)}
 \le\frac{g_{\mathrm{nom},k}}{g_{\mathrm{nom},i}}\frac1\gamma.
\]

The independent gain factors are retained. The ratio estimate for h' follows because the three ages span at most W, their youngest age is at most u_plus, and log h' is strictly concave.

Instead of bounding the denominator by a single common maximum, use the exact normalized derivative:

\[
 J_{ji}=\frac{g_ih'(F-x_i)}{\sum_k g_kh'(F-x_k)}
 \ge\frac{p_i\gamma}{1-p_i+p_i\gamma},
\qquad p=(1/6,2/3,1/6).
\]

Thus every Jacobian dominates the circulant nonnegative matrix Q with stencil

\[
 (a,b,a)=\left(\frac\gamma{5+\gamma},
                 \frac{2\gamma}{1+2\gamma},
                 \frac\gamma{5+\gamma}\right).
\]

Here b denotes a **matrix coefficient**, not the recovery actuator. This notation is used only in this derivation. The recovery actuator retains its independently chosen initial value in [0.07999,0.08001] throughout the frozen tail.

Q is substochastic. Its row sum is larger than gamma for 0<gamma<1, so it retains more of each Jacobian's mass than gamma P. The proof does not assume that all three lower bounds can be attained simultaneously. They need only hold entrywise.

## 2. Variable layers and block closure

Set c0=Delta+2 epsilon, with epsilon=2e-9 and the same directed delay-spread bound Delta as before. For m layers use W=D+m c0. Every intermediate profile and segment used in differentiation remains inside that width by the one-step diameter-growth estimate.

For arbitrary successive media within the independent box, J_m...J_1>=Q^m. The uniform row overlap is therefore at least

\[
 \widehat\beta_m(D)=\min_{r,s}\sum_j
          \min((Q^m)_{rj},(Q^m)_{sj}).
\]

The same common-row-mass argument and integration along profile segments give

\[
 \operatorname{osc}(T_m\cdots T_1(X)-T_m\cdots T_1(Y))
 \le(1-\widehat\beta_m(D))\operatorname{osc}(X-Y).
\]

Including spatial gain disorder and the first-cohort memory errors,

\[
 d_{n+m}\le(1-\widehat\beta_m(D))d_n+mc_0.
\]

It suffices that D beta_hat_m(D)>mc0. The checker evaluates Q^m, row overlaps, closure and physical inequalities with directed interval arithmetic.

## 3. Certified bounds and usable contract

| Block length | Upper closure-root bracket |
|---|---|
| 4 | [0.1852227796, 0.1852227799] |
| 5 | [0.1950798211, 0.1950798214] |
| 6 | [0.1891293631, 0.1891293635] |

For the working choice D=0.195, m=5:

| Quantity | Directed consequence |
|---|---:|
| Intermediate width W | <0.195832534 |
| Five-layer diameter factor | <0.995726579 |
| Additive five-layer allowance | <0.000832534 |
| Closure slack | >0.0000007834014 |
| Principal regeneration margin | >2.1825115 |
| Margin before first raw-current ending | >0.1375775 |
| Margin before earliest ERROR onset | >0.2374595 |
| Head slope | >0.2661557 |
| First-head displacement from initial charge | <1.705766e-9 |

The earlier convenient slope assertion >0.3 does not hold at this larger width. It is unnecessary: the actual required displacement bound is checked directly,

\[
 \frac{10^{-5}e^{-10}}{\text{certified slope}}<2\times10^{-9}.
\]

Consequently the same epsilon, summable memory loss and maintained same-lane gap >15.49999999 remain valid. Likewise, the earlier advertised recovery slack >2.2 is not retained; the required strict recovery margin is still comfortably positive. No physical margin is silently reused outside its checked domain.

All other D-dependent guards are recomputed: no early crossing before the last parent, marks before firing, firing before raw endings and errors, errors and raw currents protected, auxiliary regeneration, and positive first-head advance. The original auxiliary-cycle, gain-cap and resource bounds are independent of D and are inherited from the authenticated previous package.

This proves the same conditional tail conclusion at the larger working width: one firing per cohort per cell, no further learning after allowed initial ERROR tails, regeneration between cohorts, and propagation through arbitrarily many fresh layers. Independent choices at each port, cell and layer remain allowed.

## 4. Why five layers is optimal for this certificate family

The checker brackets an upper root for each displayed m. It also excludes every other positive integer block length above D0=0.1950798211.

For fixed m, write L=h''(u_plus+D+mc0)/h'(u_plus+D+mc0)<0. Logarithmic differentiation gives

\[
 \frac{a'}a=\frac5{5+\gamma}L,
 \qquad
 \frac{b'}b=\frac1{1+2\gamma}L.
\]

Since 5/(5+gamma)>=1/(1+2gamma), every degree-m monomial in an entry of Q^m satisfies

\[
 \frac{d}{dD}\log\big(D a^r b^{m-r}\big)
 \le \frac1D+\frac{mL}{1+2\gamma}.
\]

The right side is strictly negative at D0 for each m=3,...,15, as checked by directed bounds. It remains negative for larger D on the physical domain: 1/D decreases, L becomes more negative by concavity of log h', and gamma decreases. Therefore every D times matrix entry decreases there. Taking sums and minima preserves monotonicity, so D beta_hat_m(D) decreases as well. Every such length except five already fails closure at D0. Lengths one and two have zero overlap.

For m>=16, the physical age condition implies D<0.334. Put gamma0=e^-0.0001 h'(u_plus+D0)/h'(u_plus), omitting the positive mc0 to obtain an upper bound, and

\[
 s_0=2\frac{\gamma_0}{5+\gamma_0}
      +\frac{2\gamma_0}{1+2\gamma_0}<1.
\]

Since row overlap is at most row mass,

\[
 D\widehat\beta_m(D)\le0.334s_0^m<mc_0.
\]

The last inequality is checked at m=16. Its left side decreases and its right side increases thereafter. Thus no omitted block length admits D above the bracketed five-layer supremum in this proof family.

## 5. Relation to the pruning question

This improvement concerns the frozen head T. It increases the available entrance width by 0.085 relative to the old working contract, but it does not automatically establish a corresponding pruning-amplitude budget: that conversion must still retain every cohort and its gap margins.

The companion quantitative report proves that the constant affine estimate 0.95d+f cannot close the supplied 0.0058 budget. It also gives a nonlinear two-step result for a restricted b-only, parity-constant disorder family: 0.0058 -> 0.0038 -> 0.0030, followed by invariance. Full independent disorder in the pruning dynamics, mode transfer and entrance from the original source remain open.

## 6. Reproduction and scope

    python3 verify_tail_refinement.py
    python3 -O verify_tail_refinement.py results/tail_refinement_certificate_optimized.json

Normal and optimized runs are compared byte for byte. Both use the same arithmetic implementation; this comparison is not independent mathematical validation. Baseline input reports are checked against the hashes and exact members of the previous delivered ZIPs. Full endpoints, checks and environment details accompany this note. No production campaign, original receipt, or source repository file is modified.
