# Extending the learning-coverage argument to engine v2.3.1

**Status.** Proposed from the code audit [`../AUDIT_ENGINE_V231.md`](../AUDIT_ENGINE_V231.md),
awaiting review. It is not part of the proof dossier in [`proof/`](../../../proof/), whose statements
remain those for ε = 1e-4 and the v3.3 program.

**Purpose.** The learning-coverage theorem
(`proof/learning_justification/output/LEARNING_COVERAGE_THEOREM_EN.txt`) shows that every successful
step of the v3.3 program preserves its relational invariant (I1–I5). Engine v2.3.1 runs the same
kernel with additional acceptance rules. Each rule below is stated as a lemma: *if the program accepts
by this rule, the produced state encloses every admissible continuation that the replaced step would
have had to enclose*. With these lemmas, and under assumptions A1–A5 below, the v3.3 argument would
cover v2.3.1 step by step.

**Notation.** θ is an admissible device (per-port constants within ±ε) and an admissible initial
state. All dates are affine `Time` objects; `X.lo`, `X.hi` are certified bounds over θ. In READY,
q̇ = κ(r − q) + Σ g_j p_j. h(u) = a/(a − κ)(e^{−κu} − e^{−au}), a = ln 4, κ = 1/2, r = 1/10,
r_m = 1/40.

## B1. Weak-order contraction of the return (`cycle_relatif_A22`, `contract_order=True`)

*Setting.* The local-cycle resolver enumerates weak orders ω of an exterior group and the return R.
For ω, let E⁻ be the events placed before R and E⁺ those after it.

*Lemma.* If θ follows ω, then
R(θ) ∈ [max(t₀.lo, B.lo, max_{e∈E⁻} T_e.lo), min(U.hi, B.hi, min_{e∈E⁺} T_e.hi)], where B is the
already certified box of R. If this interval is empty, no θ follows ω.

*Proof.* T_e(θ) ≤ R(θ) for e ∈ E⁻, and T_e(θ) ≥ T_e.lo. The upper bound is symmetric. The kernel
enumeration already covers every admissible weak order, so dropping an order that no θ follows loses
nothing. ∎

## B2. Sign contraction of the return (`recovery_tightening.contract_return`)

*Setting.* `v.root` returned [l, h] for the zero of −ℓ, where ℓ is the protected ledger (q = r·e^ℓ). It
certified sign(−ℓ(l)) ≤ 0 ≤ sign(−ℓ(h)) and inf_{[l,h],θ} ∂_t(−ℓ) > 0, and Newton steps keep the
enclosure inside the bracket.

*Lemma.* For m ∈ (l, h): if inf_θ ℓ(m; θ) > 0, then R(θ) > m for every θ; if sup_θ ℓ(m; θ) < 0,
then R(θ) < m.

*Proof.* For each θ, ℓ(·; θ) is strictly decreasing on [l, h] and its unique zero there is R(θ). ∎
The probes use the same ledger convention (`live=False`: no mark is assumed finished before its end)
as the root solver.

## C1. Correlated first auxiliary delay (`correlated_first_delay`)

*Setting.* Port j receives its first pulse at a ≥ t₀ > U₀, where U₀ is the kernel's initial slab
end. Before a, the auxiliary charge is READY with |m(t) − r_m| ≤ Δ·e^{−κt}: an initial READY
deviation decays at rate κ, and an initial ERROR tail ends by U₀ exactly at r_m. Let D₀ be the root
of F(u) = r_m + M_j·h(u) − 1 in (0, 0.1).

*Lemma.* Put μ = Δ·e^{−κt₀} and σ = M_j.lo·h′(0.1) − κμ. If σ > 0 and D₀ ± μ/σ ⊂ (0, 0.1), the first
threshold delay D satisfies |D − D₀| ≤ μ/σ.

*Proof.* D is the root of G(u) = F(u) + δe^{−κu} with |δ| ≤ μ. On [0, 0.1], h″ < 0 because
(a/κ)² > e^{(a−κ)·0.1}, so h′ ≥ h′(0.1) and G′ ≥ σ > 0. Since |G(D₀)| ≤ μ, the mean-value theorem
gives |D − D₀| ≤ μ/σ. ∎ The engine also requires the new interval to lie inside the previous one.

## C2. Monotone pulse-memory root (`memory_root`)

*Setting.* READY at t, next external event B (aux transitions are external queue events), pulse
memory Q(u) giving q(t + u) with all admitted pulses.

*Lemma.* Suppose Q(0) < 1, Q(h) ≥ 1, Q′ > 0 on [0, h], h ≤ (B − t).lo, `v.root` certifies the root
F, and (B − F).lo > 0. Then for every θ the first event after t is the fire at F(θ).

*Proof.* Q is strictly increasing on [0, h], so it has one crossing there, the first. In READY the
only internal guard is the fire. Deposits only change gains of ports without raw input (kernel
invariant), so they do not affect Q before B. ∎

## C3. Commuting READY group (`ready_commuting`)

*Setting.* READY, no open deposit gate, no fire in any actuation ledger. The group contains only
raw_on/raw_off/mark_on/mark_off events, at most one raw_on per port, each port's events in certified
order, all before U.

*Lemma.* If the complete pulse memory (zero response before each arrival) satisfies sup Q < 1 on
[t, U], then every admissible interleaving reaches at U the same state: per-port final flags, the
actuation ledger with all marks, and charge Q(U).

*Proof.* With no fire, P stays READY on [t, U], so every raw input is admitted with the constant gain
g_j. The charge is the sum of pulse terms, which does not depend on the interleaving. Mark events
only record per-port entries in the ledger; in READY they do not change b. Raw and mark flags are
port-local, so events on distinct ports commute. ∎

## C4. Commuting protected group (`protected_commuting`)

*Setting.* FAST phase with fire F shared by every ledger, no open deposit gate, U.lo ≥ (F + 1).hi.
Events raw/mark/error on/off, at most one on-event of each kind per port, certified per-port order,
all before U.

*Lemma.* If ℓ(U) > 0, computed with every mark (zero contribution before each mark starts), then no
θ and no interleaving returns to READY in [t, U]. The state at U is SLOW with q = r·e^{ℓ(U)}, b and z
from the ledgers at U, and the per-port final flags.

*Proof.* ℓ is non-increasing in time because q̇ = −b·q with b > 0, so ℓ(τ) ≥ ℓ(U) > 0 for τ ≤ U. Mark
doses are non-negative, additive and per port, so ℓ(U) does not depend on the interleaving. With
P ≠ READY, deposit gates stay closed and admission is closed: error and raw events change flags
only. ∎

## C5. Pointwise sparse hull (`sparse_hull`)

*Lemma.* For affine forms x_k = c_k + Σ_i d_{k,i}ε_i ± e_k, set m_i = midpoint of
{d_{k,i}} ∪ {0 if some form lacks ε_i} and ρ_k = e_k + Σ_i |d_{k,i} − m_i|, with d_{k,i} = 0 when
absent. Then H = [min_k(c_k − ρ_k), max_k(c_k + ρ_k)] + Σ_i m_i ε_i contains every x_k(ε), for every ε.

*Proof.* x_k(ε) − Σ m_i ε_i = c_k + Σ(d_{k,i} − m_i)ε_i ± e_k ∈ c_k ± ρ_k. ∎ The code sums the |m_i|
of the absent symbols exactly in integer units of 2⁻¹⁰⁷⁴ and rounds every term of ρ_k upward.

## C6. Piecewise no-fire cover (`cluster_memory_cover`)

*Lemma.* If [0, H] is covered by intervals P_k with sup_{θ, u∈P_k} Q(u) < 1 (the interval evaluation
of the pulse memory), and H ≥ (T − t).hi, then no fire occurs in [t, T].

*Proof.* Every time of the window lies in some P_k. ∎ This needs `dep.evaluate` to be an enclosure
over time intervals, a kernel property already used by v3.3.

## C7. Peak fallback (`engine.py` patches of `flowing`/`advance`)

*Lemma.* In READY with no input admitted on [t, T], q(u) = r + (q₀ − r)e^{−κu} + J(e^{−κu} − e^{−au})/(a − κ)
is non-decreasing in q₀ and in J ≥ 0. Hence `peak_upper`, which evaluates this formula at (q₀.hi,
J.hi), over [0, H] or at the endpoints and the stationary point, bounds q on the whole window. If it
is < 1, no fire occurs before T.

*Proof.* e^{−κu} ≥ e^{−au} for u ≥ 0 gives monotonicity in J; the coefficient of q₀ is positive. The
maximum over u is at an endpoint or at the unique stationary point when a − κ > 0 and the logarithm's
argument is positive; otherwise the interval evaluation over [0, H] is used. ∎

## C8. READY re-anchoring at a recovery join (`recovery_group`)

*Lemma.* Suppose all branches are READY at a common date T with identical raw flags, charge in Q_T
and gains in G. Then `new_memory`, built from (T, Q_T, G, active raw origins), encloses the future
charge of every branch until the next event.

*Proof.* After T, q is the kernel's affine-in-q(T) formula plus the remaining tails of the active
pulses with their gains. Using the enclosures Q_T and G covers every branch; only correlations with
earlier quantities are lost. ∎

## Implementation statements (not lemmas)

- **I1, prefix sharing and order enumeration** (`cluster_prefix`, `event_order_cache`). The same set of
  orders is produced. Pruning happens only on certified contradictions. A shared prefix state equals
  its recomputation, because `flowing` and `act` copy before updating.
- **I2, exact caches** (`time_sum`, `transfer_memo`; `temporal_memo` off by default). Keys hold the
  input objects themselves, which are immutable or frozen, plus lazy state and contexts. Fresh
  remainder symbols are allocated or renamed exactly as an uncached call would.
- **I3, scenario joining** (`run_scenarios`). Only combinations whose shared ancestors carry the same
  scenario are kept. Physical symbols are named per cell and rounding symbols per job. At ε = 1e-3
  every cell has one scenario.

## Execution assumptions

A1–A4 as in `proof/`, applied to the v2.3.1 program and binaries, plus:

- **A2′.** The shipped `_rounding_native` (sha256 `3dcf376b…`) is compiled from the shipped
  `rounding_native.c`.
- **A5.** The campaign ran with the default memo flags (`A22_TRANSFER_MEMO` on,
  `A22_EXACT_TIME_MEMO` off). These flags are not recorded in `kernel_id`.

## What remains before a statement at ε = 1e-3

1. Review of B1, B2, C1–C8 and of their insertion into the induction of the coverage theorem.
2. A general-ε wording of `proof/FUTURE_INVARIANCE_PROOF_EN.txt` (it names ±1e-4 in sections A and B;
   the checks at 1e-3 pass, see [`../eps_1em3/future/`](../eps_1em3/future/README.md)).
3. Audit of `affine/artifacts.py` (record integrity).
4. Optionally, a control campaign at ε = 1e-4 with v2.3.1 compared with v3.3.
