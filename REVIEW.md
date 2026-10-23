# Call for review

This repository contains a complete, reproducible computation and a **manual proof** that it covers
every admissible trajectory, under stated execution assumptions. The proof has **not yet been reviewed
by an independent expert**. The fastest way to check it is for specialists to take small,
self-contained pieces. Each task below can be read in **one to three hours** without knowing the rest.

**What helps most:** one of three answers, given as a GitHub issue titled `Review: <task>`:
- "the argument holds";
- "there is a gap at <file:section or file:line>, because …";
- "here is a counterexample".

Partial reviews are welcome. Tasks are listed **most important first**.

Background for every task: the [README](README.md), the method section of
[docs/DETAILS.md](docs/DETAILS.md#method), and the review guide
[proof/learning_justification/output/REVIEW_GUIDE_EN.txt](proof/learning_justification/output/REVIEW_GUIDE_EN.txt).
In what follows, *affine form* means *c + Σ dₖ εₖ + [−e, e]*, valid for every ε in [−1, 1]^N, and
"the theorem" means `proof/learning_justification/output/LEARNING_COVERAGE_THEOREM_EN.txt`.

The code actually executed differs from the files in places: some functions are rewritten when the
engine is loaded. Their final text is in `proof/kernel_soundness/output/effective_source/`.

---

## Task 1 — Open-image lemma and strict root order (most load-bearing)

**Claim.** Every computed threshold root is enclosed *strictly*: with the old parameters and dates
fixed, the computed enclosure contains an open interval around the true root (theorem, Sections 4–6;
also `proof/kernel_soundness/output/STRICT_ROOT_LEMMA_EN.txt`). Consequently, when the engine accepts
an order from a weak test *x − t ≥ 0*, the physical order is strict, and an exact simultaneity between a
spike and an event can never pass the ordinary order test.

**Where:** `engine/affine/engine.py` (`affine_refine`, `root`, `ready_root`), the effective `advance`
(`proof/kernel_soundness/output/effective_source/advance_inner.txt`), `engine/affine/temporal.py`
(`minus`, `shift`), `engine/affine/affine_iv.py` (`_unary`, exp/ln).

**Questions.**
1. Is the open-image lemma correct as stated, for the operations actually used after the fresh
   exponential (products, sums, hulls, truncation, error promotion)?
2. In `affine_refine`, does every retained output (not only the last bracket) keep the true root
   strictly inside, including the case where the rounded midpoint is 0?
3. Is there any exp/ln evaluation on these paths whose result is exact (no adjacent-number expansion)
   and would remove the strict margin?

## Task 2 — Event coverage and every successful exit (theorem, Section 8)

**Claim.** For every physical order of events, including equal times, the program keeps a branch that
covers it, through every successful path: ordinary advance, external groups, protected FAST/SLOW
groups, recovery/auxiliary groups, the local-cycle resolver, and the 202 recorded commutations (all a
spike against one end of mark, including the fallback `_first_crossing_cover`). Entry into event groups
is always forward in time (`proof/learning_justification/output/GROUP_ENTRY_CLOCK_LEMMA_EN.txt`).

**Where:** effective `unit` (`proof/kernel_soundness/output/effective_source/unit.txt`),
`validation_A15.py` (`admissible_orders`, `protected_section_cluster`, `recovery_auxiliary_cluster`),
`cycle_local_A20.py`, `engine/affine/commutation.py`.

**Questions.**
1. Can a physical branch be lost at a group boundary, an equal-time order, or a FAST/SLOW boundary of
   zero duration?
2. Is the first-crossing property (unimodality of the READY charge between events, Section 7) used
   correctly at every place a spike is accepted?

## Task 3 — Unions: memory anchors and the fields kept from the first branch (theorem, Section 9)

**Claim.** `join_states` keeps the discrete fields (current mark and error origins, fire date, raw
inputs) of its first branch, and `dep.join` keeps the first branch's memory anchor. At every reachable
successful caller, these are common to all branches, or the memory is dropped (which is conservative).

**Where:** `validation_A15.py` (`join_states`), `dependances_A17.py` (`join`), the callers in the
effective `unit`, `engine/affine/commutation.py`.

**Questions.**
1. Is there a reachable union whose branches differ in a mark or error origin, or in the fire date?
2. Is it true that separately recomputed returns always get distinct time atoms, so that their memories
   can never be wrongly merged under an equal token?

## Task 4 — Future invariance and exact transmission

**Claim.** From the quiescent domain Q, every source pulse spaced by at least 20 makes each of the 191
active cells fire exactly once, the network is at rest within 12.791, and the state returns to Q. Active
cells have fixed latencies, so the pulse word is transmitted exactly.

**Where:** `proof/FUTURE_INVARIANCE_PROOF_EN.txt`, `proof/GLOBAL_THEOREM_AND_WORD_PRESERVATION_EN.txt`,
the two checkers `proof/provenance_audit/certify_future.py` and `verify_future_certificate.py`.

**Questions.**
1. Is the "influential / masked / silent" classification of ports enough to keep the head response
   identical from wave to wave?
2. Are the strict margins (reopening, end of raw pulse, end of error) the right ones, and are the two
   checkers' series and tail bounds correct?

## Task 5 — Outward-rounded affine arithmetic

**Claim.** Each affine operation is valid pointwise, for arbitrary represented operand values:
- the multiplication remainder covers every term (`__mul__`, line 182);
- in the mean-value form for exp, ln and reciprocal, the slope domain includes the expansion point
  (`_unary`, line 201);
- a union keeps a common coefficient and absorbs the spread (`_dev_up` line 285, `hull` line 308);
- truncation to 256 symbols bounds the dropped mass upward (`truncate_coeff`: Python reference in
  `engine/affine/rounding.py` line 51, C in `engine/affine/rounding_native.c`).

**Where:** `engine/affine/affine_iv.py`, `engine/affine/rounding.py`, `engine/affine/rounding_native.c`,
`engine/affine/sound_lattice.py`, the theorem's Section 4, and the earlier audit `docs/AUDIT_EN.txt`.

## Task 6 — Per-port parameter symbols (fix P)

**Claim.** Each port *j* of a cell gets one symbol per constant (LM, LS, LE, M), used only where the
kernel evaluates a quantity of port *j*; every other occurrence keeps a plain interval (C is plain
everywhere). Hence every trajectory of the model is represented, and no correlation the model does not
have is imposed.

**Where:** `engine/affine/port_symbols.py` (`settings` line 49, `with_port` line 93, `raw_dose` line 107,
`with_deposit_port` line 133), `engine/affine/engine.py` (event durations line 155, coefficients
line 222), tests in `engine/tests/test_v33_ports.py`.

**Questions.**
1. Does every port-dependent use of LM, LS, LE, M receive that port's value, and every other use keep
   the plain box?
2. Is the per-mark `raw_dose` identical to the kernel's for a single-port history, and correct for a
   history that mixes ports?

---

## Depth extension (v4.0-depth)

These tasks concern [`depth/`](depth/README.md). Several of the cited documents are in French; their
formulas and tables can be read directly.

## Task 7 — Masked late parent and local regeneration (boundary checker)

**Claim.** The frozen checker required every parent to arrive before the first raw-pulse end, which is
stronger than the model needs. The supplementary checker `certify_contracts.py` replaces that
requirement with five explicit conditions. With them, a parent that arrives after the first firing
(during protection) does not change the head equation. All raw currents end before reopening, and the
cell regenerates locally before the next wave, even if the masked port's gain keeps changing. Hence
`t_j^p = s_p + d_j` for every admissible future word.

**Where:** `depth/review/REVIEW_V1_FR.md` §2; `certify_contracts.py` in each case certificate
(`review_tools/`); the model's recovery law in `engine/reference/full_model_reference.md` (ḃ ≥ 0, b ≤ 1.1).

**Questions.**
1. Are the two protection bounds, with `b_entry` and 1.1, valid with partial MARK phases?
2. Can a masked ERROR that lasts past reopening ever cause an extra firing before the next wave?

## Task 8 — Finite-to-infinite composition and tail theorems

**Claim.** If the boundary cohorts satisfy diameter ≤ W and same-lane gaps ≥ 15.5, then fresh downstream
cells never change their gains or recovery, regenerate locally, and preserve diameter and spacing. The
min/max translation bounds then give one asymptotic duration per layer for all lanes. For the interface,
a six-layer row-overlap contraction (β > 0.057) gives one common duration with a fixed phase profile.

**Where:** `depth/theory/LEARNING_SPEED_SELECTION_EN.txt` §4–5;
`depth/review/FINITE_TO_INFINITE.md`; `depth/theory/conditional_tail_certificate.json`;
`compose_tail.py` in each case certificate.

**Questions.**
1. Is the tail tube (head ages within u ± W) enough for every protection and regeneration margin used?
2. In the interface argument, is Lipschitz control of the scalar advance correctly obtained from the
   stochastic Jacobian?

## Task 9 — First future wave at time 1116 without global rest

**Claim.** For each cell, the last training recovery and the last auxiliary completion are bounded above
(using b ≥ 0.08), and they precede the earliest possible arrival of the first future wave. Exact rest at
the 4096 observation time then implies exact rest on the whole preceding current-free interval.

**Where:** `depth/review/REVIEW_V1_FR.md` §3; `depth/review/FIRST_FUTURE_FINAL_V2.json`.

**Question.** Does "exact rest at 4096" correctly imply exact rest from each cell's own bound Q_v onward,
for every state variable used by the head equation?

---

## What is out of scope here

- The scientific hypothesis behind the model (the Reset Operator; see `docs/MODEL_BOUNDARY_EN.txt`).
- Whether the parameter box is physically meaningful.
- The correctness of the compiler and of the two native binaries (identified by hash; assumption A2).

The question in every task is whether the proof is correct for the model and the program as recorded.
The proof status, and what remains beyond review, are in
[docs/DETAILS.md](docs/DETAILS.md#proof-status).
