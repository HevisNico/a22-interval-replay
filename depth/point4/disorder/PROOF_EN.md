# A22: independent disorder, a wider pruning target, and bounded-input reduction

23 October 2026

**Status: partial mathematical progress. Universal original-source entrance is not proved.** This package establishes a conditional dense-front-to-tail reduction, two directed heterogeneous histories, and uniform local bounds for independent parameter perturbations. The histories start from a complete synchronized boundary train; they are not new original-source campaigns.

Original campaigns, receipts and repository files are unchanged. All intervals below are directed enclosures. Manual arguments accompany the numerical certificates; this is not proof-assistant verification or independent expert review.

## 1. A conditional reduction with front width 0.08

Consider an entire boundary history consisting of exactly 128 complete cohorts X+8k, k=0,...,127, with first arrival at time at least 20. Downstream cells have the full original independent parameter and initial-state box. No precursor, missing port or additional future input is omitted.

Suppose that the **actual dense-front profile at every one of the 63 pruning passages has diameter at most 0.08**, including the profile entering each passage and its surviving dense successor. This hypothesis is not proved here.

The previously established full-box local lemma then supplies a first safe output gap greater than

    G* = 15.50346376901117240912546753912549... .

It passes the first dense cohort, suppresses the second, and makes the remaining dense suffix a translated 8-spaced train. It tracks the three protected marks, the increase of the recovery actuator b by 0.3, clipped error integration, gain caps, protection and regeneration. It bounds only the newly created safe gap; it does not incorrectly replace all later dense gaps by 16.

For safe-prefix responses, use the full-box frozen-head bounds from the earlier tail theorem. Let Delta be the synchronized delay spread and epsilon=2e-9 the allowed first-head displacement from initial charge. A single safe passage increases spatial diameter by at most

\[
 c_0=\Delta+2\varepsilon
 =0.0001665067484259469514851840379\ldots .
\]

A cohort that has left the dense front undergoes at most 64 such passages by layer 64. Hence every surviving cohort has diameter at most

\[
 0.08+64c_0
 <0.090656432.
\]

This bound stays inside the older verified intermediate physical width 0.110999041, so the safe-prefix physical guards and memory estimate apply at every intermediate step. The enlarged tail width 0.195 is available but is not needed for this particular reduction.

The regenerated head preserves coordinatewise gaps by order preservation and time-translation equivariance. Allowing conservatively two epsilon errors per passage, any newly created safe gap remains greater than

\[
 G_*-64(2\varepsilon)
 >15.5034635130>15.5.
\]

Induction therefore works as follows. Existing safe cohorts pass without adaptation. Before the first dense cohort, the principal and auxiliary states regenerate, while the gains and b retain their effective initial values. The next local pruning transition is then valid. Its new gap joins the safe prefix. Initial auxiliary ERROR tails are already included in the effective log-gain offsets [-1e-5,9e-5]; they are not reset by assumption. Initial principal-charge memory is explicitly budgeted for the first cohort of each fresh cell.

At layer 64, the surviving original indices are 0,2,...,126. Cohort 2r has undergone r pruning passages followed by 64-r frozen passages. All 64 survivors satisfy the older D=0.11 tail entrance contract, and hence also the new D=0.195 contract. This finite train causes no further learning in fresh layers from layer 65 onward, after any allowed initial ERROR tails have ended.

This gives a useful sufficient target: **control the dense front within width 0.08 through its 63 pruning passages**. The earlier numerical budget 0.0058 is not required by this specific induction. This does not show that a different derivation of that smaller budget was erroneous; the conditions and width accounting here are stated explicitly.

It remains necessary to prove the front-width hypothesis and to establish reachability of an appropriate complete-cohort boundary from the original single-lane source. Additional future inputs require their own complete-history verification.

## 2. A nonalternating b-only witness

Start the complete boundary train in synchrony. Keep all physical constants and initial charges nominal, but set

\[
 b_j=0.07999\quad(j=0,\ldots,5),\qquad
 b_j=0.08001\quad(j=6,\ldots,11)
\]

in every fresh layer. This is an admissible spatial pattern in the independent initial box. It is not constant on each parity, so the earlier pure alternating envelope does not apply.

The checker propagates all 12 cells through 63 actual pruning maps with directed root brackets and physical event checks. It obtains

| Pruning passages | Directed diameter, rounded for display |
|---|---:|
| 12 | 0.006850742982469... |
| 63 | 0.007813337661411... |

Every checked input and output remains below diameter 0.008. Thus the example exceeds 0.0058 while remaining comfortably inside the 0.08 local domain. It disproves a universal cap of 0.0058 for a family containing this synchronized boundary and all admissible independent b patterns. It does not refute extinction or universal original-source entrance.

The larger contrast across two half-rings is why the pure alternating calculation alone does not control arbitrary spatial disorder. No claim that this pattern is globally worst is made.

## 3. One assignment using several parameter endpoints

A second directed history uses, on lanes 0,...,5,

    b=0.07999, effective eta=-0.00001,
    M, LM, LS, LE at their +0.0001 relative endpoints;

and on lanes 6,...,11,

    b=0.08001, effective eta=+0.00009,
    M, LM, LS, LE at their -0.0001 relative endpoints.

The same assignment is used in every fresh layer. Ports inside each selected cell share its endpoints. These are permitted choices within the independent box, but checking them is not a cover of all combinations.

The effective eta=+0.00009 is realized without changing the original initial box: choose initial z=ln(g_nom)+1e-5 and an auxiliary in its final ERROR phase with m=rm+1e-5. Its initial error tail contributes exactly 8e-5 to log gain before the first arrival. Choose q=r, E=75 and nominal C; the earlier resource and cap bounds apply. On the other half-ring choose z=ln(g_nom)-1e-5 and auxiliary READY states at rm.

The generalized cell verifier computes the auxiliary crossing time from the actual M, retains the actual LM, LS and LE durations, and checks the complete pruning event sequence including the b actuator. Directed results are

| Pruning passages | Directed diameter, rounded for display |
|---|---:|
| 12 | 0.010441853461835... |
| 63 | 0.011108857562706... |

All 63 checked diameters are below 0.012. The conditional bridge therefore applies to this particular complete-boundary history. This is a positive finite heterogeneous example and a stronger obstruction to the 0.0058 cap, not a universal full-box result.

## 4. A uniform local bound for every independent parameter choice

Unlike the preceding histories, this section quantifies over the entire independent parameter box. Compare the heterogeneous pruning output S_theta(X) with the nominal pruning output S_0(X) at the **same** input profile X of diameter at most w. First consider an exactly regenerated principal state; the fresh-state correction is included below.

Let F_theta and F_0 be their unlearned first heads. The independent effective gain offsets satisfy eta_i in [-1e-5,9e-5]. Implicit differentiation of the head equation gives

\[
 \sum_i\left|\frac{\partial F}{\partial\eta_i}\right|
 =\frac{0.9}{\sum_i g_i h'(F-x_i)}.
\]

The denominator has a directed lower bound throughout the whole gain interpolation and profile domain. Consequently F_theta-F_0 lies in [-9e-5 K0,1e-5 K0], with K0 recorded in the certificate.

Write B=b+0.3, alpha=0.1-0.4 log(1.25), d_i for the second auxiliary threshold delay, and D_s,i for its SILENT duration. The reopening formula is

\[
 R=\frac{\log2.5+b(F+1)+0.1\sum_i(8+x_i+d_i)
               +\alpha\sum_i L_{m,i}^{-1}}B.
\]

This is the formula after all three protected marks; b has risen by exactly 0.3. It follows from the same integrated recovery law as the local pruning lemma.

Let e_i=d_i+log(1.25)/L_m,i+D_s,i. Subtract the nominal formula, keeping each repeated physical parameter correlated algebraically. The difference in reopening relative to port i's error start is exactly

\[
\begin{aligned}
 \Delta(R-e_i)={}&\frac bB\Delta F
 +\frac{b-0.08}B(F_0+1-R_0)\\
 &+\left(\frac{0.1}B-1\right)\Delta d_i
   +\frac{0.1}B\sum_{k\ne i}\Delta d_k\\
 &+\left(\frac\alpha B-\log1.25\right)\Delta L_{m,i}^{-1}
   +\frac\alpha B\sum_{k\ne i}\Delta L_{m,k}^{-1}
   -\Delta D_{s,i}.
\end{aligned}
\]

The checker encloses this expression using independent port intervals. In particular it does not impose a common error-start ordering. If z_i=L_e,i(R-8-x_i-e_i), then

\[
 \Delta z_i=L_{e,i}\Delta(R-e_i)
       +(L_{e,i}-L_{e,0})(R_0-8-x_i-e_0).
\]

The clipped error integral

\[
 \phi(z)=\operatorname{clip}_{[0,0.6]}(0.8e^{-z}-0.2)
\]

is decreasing and globally 0.8-Lipschitz. Its active derivative has magnitude at most 0.8; both flat branches are included. This gives a rigorous interval for the difference in learned log gains, including error starts on either side of reopening. A second implicit-head sensitivity bound K1 converts that log-gain interval into an interval [L(w),U(w)] for S_theta(X)-S_0(X), cell by cell.

The existing full-box local event inequalities are recomputed at every reported w. Thus the comparison uses the physical pruning branch, with inactive caps, rather than an unsupported algebraic continuation.

### Fresh initial charge is retained

For a first arrival at time at least 20, q-r contributes at most 1e-5 exp(-10) to the first-head equation. A directed derivative bound yields a first-head displacement epsilon_F<2e-9. Its effect on reopening is at most (b/B) epsilon_F; the same clipped-integral and learned-head bounds give an additional output error E(w). Initial auxiliary ERROR tails are included in eta. Initial READY charge affects the first auxiliary cycle, whose marks precede firing and whose errors are protected; the second auxiliary cycle has regenerated.

The fresh-state output interval is therefore [L(w)-E(w),U(w)+E(w)]. No artificial exact reset is used for the first fresh cohort. Later dense transitions following a safe prefix use the regenerated version.

Conservative rounded upper bounds on the **extra diameter allowance** F(w)=U(w)-L(w)+2E(w) are:

| Input diameter bound w | Fresh full-box extra diameter allowance, upper bound |
|---|---:|
| 0.0058 | 0.0018297 |
| 0.01 | 0.0019468 |
| 0.02 | 0.0022521 |
| 0.04 | 0.0029936 |
| 0.08 | 0.0052415 |

These are bounds on parameter-induced differences at a fixed input profile. They do not assert that the nominal map contracts that profile's diameter.

## 5. Reduction to a controlled nominal map

For every actual admissible heterogeneous transition, the preceding result gives

\[
 X_{n+1}=S_0(X_n)+e_n,
 \qquad e_{n,j}\in[L(w)-E(w),U(w)+E(w)].
\]

The nominal map commutes with common time translations. Removing a common offset at every layer yields the diameter-equivalent inclusion

\[
 Y_{n+1}=S_0(Y_n)+v_n,\qquad 0\le v_{n,j}\le F(w).
\]

Thus independent physical parameters can be overapproximated by independent bounded additive inputs to a single nominal map. A proof for all controls in this inclusion would cover the physical box. The converse is false: some additive control sequences may not correspond to any actual physical parameters.

The remaining finite target is to control this inclusion over the required pruning passages from a stated boundary family, while retaining all intermediate widths below 0.08. The uniform forcing estimates remove parameter dimensions from that task; they do not solve the nonlinear reachable-set problem.

A one-step diameter contraction cannot be assumed even in the nominal problem. Take six consecutive lanes at 0 and the other six at d. Interior cells of each plateau see three equal arrivals, so their output values differ by exactly d. After two layers there are still interior cells whose radius-two dependency cones stay entirely inside their respective plateaus. Hence a strict uniform radial diameter factor below one is impossible for one or two nominal layers on a family containing these profiles. With independent additive controls, a diameter ball alone is not a one-step invariant set: controls can raise the high interior output and leave the low one unchanged.

A block estimate with controlled intermediate widening, or a state set carrying spatial shape information, is therefore required. The earlier alternating-mode factor 0.95 must not be inserted as a one-step factor for arbitrary profiles.

## 6. Computation, assurance and limits

The two 63-layer histories use 130-digit directed intervals, explicit finite-series remainders and strict physical root brackets. Newton calculations only propose endpoints; the certificate is the directed sign check. Root padding is 1e-95 and is not trusted as an error bound. A proposed bracket that lacks the required signs fails. The longer histories needed higher precision to prevent interval wrapping from obscuring the margins; a wider computed enclosure would not itself be a physical escape.

The uniform perturbation and bridge checks use the previously established 70-digit arithmetic. Their baseline records are read only from the preceding delivered archive after its SHA-256 is checked. Numerical consistency tests compare the generalized kernel with its nominal specialization and check selected endpoint cases against the independently derived uniform perturbation envelope. These finite consistency tests are not a substitute for the uniform argument.

Exploratory searches are separately labelled. The b-only adjoint search found larger contrasts than the simple fixed half-ring pattern, but no global optimization guarantee is claimed. The finite certificates do not depend on the optimizer's output.

**Not established:** a uniform 63-passage bound for all independent disorder; entrance of every original single-lane-source preparation into the complete-cohort boundary family; or arbitrary additional future histories. No universal discovery claim follows from this package.
