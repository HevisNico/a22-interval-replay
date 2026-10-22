# Call for review

This repository contains a complete, reproducible computation whose correctness proof is **not
finished**. The fastest way to finish it is for specialists to check small, self-contained pieces.
Each task below can be read in **one to two hours** without knowing the rest of the code.

**What helps most:** one of three answers, given as a GitHub issue titled `Review: <task>`:
- "the argument holds";
- "there is a gap at <file:line>, because …";
- "here is a counterexample".

Partial reviews are welcome.

Background for every task: the [README](README.md) and the method section of
[docs/DETAILS.md](docs/DETAILS.md#method). In what follows, *affine form* means
*c + Σ dₖ εₖ + [−e, e]*, valid for every ε in [−1, 1]^N.

---

## Task 1 — Unimodality lemma (first crossing H1, no missed spike H2)

**Claim.** Between two events in READY, the charge obeys *q' = −K(q − R) + I(t)*. Here *I* is a sum of
currents *g·A·e^(−A·age)* with *g > 0*, and each current is cut off at age 1. Under these conditions
the charge is unimodal: it rises, then falls. Two consequences follow:
- **H1:** a crossing certified on a bracket [l, h] (sign at l and h, slope > 0 on [l, h]) is the
  first crossing after t₀;
- **H2:** the single-exponential "peak" bound, which extends every active current beyond its end with
  the current gain, dominates the true charge, because learned gains never decrease.

**Where:**
- `engine/kernel/R_cycle_local_A20_2026-10-18/validation_A15.py`, `advance`, lines 322–349 (decision);
- `engine/kernel/R_cycle_local_A20_2026-10-18/dependances_A17.py`, `pulse`, `tail`, `evaluate`
  (charge model);
- `docs/DETAILS.md`, "Independent checks" (the argument);
- `tools/verif_h1h2.py` (the bisection re-check used on the campaign).

**Questions.**
1. Does unimodality hold for the charge model exactly as coded, including the tail terms of pulses
   admitted before *t₀*?
2. Is "learned gains never decrease" true for the deposit model (`depot_A19.py`) and after the history
   unions of `engine/affine/engine.py` (fix H, line 319; fix S, line 383)?

## Task 2 — Commutation of a spike with input events (fix E)

**Claim.** In READY, an arrival adds a non-negative pulse response. An end of admission, a mark event
or an error event leaves the charge unchanged. So the true spike date *F* satisfies
*min(a, f₀) ≤ F ≤ f₀*, tightened to *f₀ − κ(f₀ − a)⁺* with *κ = G·A/(σ + G·A)*.

The engine computes every order with the unchanged kernel maps and joins the results at a common
clock *U*. *U* is before the next event and before the end of the fast phase.

**Where:**
- `engine/affine/commutation.py`: the module docstring states Lemmas 0, 0', 1 and 2; the rest is the
  implementation;
- `engine/affine/engine.py`: where it is hooked in (search `COMMUTE`).

**Questions.**
1. Are the preconditions checked in `_resolve` sufficient for the lemmas?
2. Is the join at *U* sound when the joined branches differ only in their actuation and deposit
   histories?

## Task 3 — Unions of branches (fixes C, H, S)

**Claim.**
- **C:** a union keeps one common coefficient per symbol and absorbs only the deviations, rounded
  upward. It is pointwise valid for any choice of the common coefficient.
- **H:** folding completed learning terms into the initial value is exact. Histories with the same
  structure that differ only in that additive initial value can be joined.
- **S:** intersecting a union with the plain envelope of its members is sound.

**Where:** `engine/affine/affine_iv.py` (`_dev_up` line 285, `hull` line 308) and
`engine/affine/engine.py` (fix H line 319, fix S line 383). The exact-rational tests are in
`engine/tests/test_v3_fixes.py`, `test_v31_histories.py` and `test_v32_caps.py`.

## Task 4 — Outward-rounded affine arithmetic

**Claim.** Each affine operation is valid pointwise:
- the multiplication remainder covers every term (`__mul__`, line 182);
- in the mean-value form for exp, ln and reciprocal, the slope domain includes the expansion point
  (`_unary`, line 201);
- truncation to 256 symbols bounds the dropped mass upward (`truncate_coeff`: Python reference in
  `engine/affine/rounding.py` line 51, C in `engine/affine/rounding_native.c`).

**Where:** `engine/affine/affine_iv.py`, `engine/affine/rounding.py`,
`engine/affine/rounding_native.c`, and the earlier audit in `docs/AUDIT_EN.txt`.

## Task 5 — Per-port parameter symbols (fix P)

**Claim.** The model gives each port *i* of a cell independent constants LM_i, LS_i, LE_i, M_i (and
C_i). The engine gives port *j* one symbol per constant and uses it **only** where the kernel evaluates a
quantity of port *j*; every other occurrence keeps a plain interval box (C is plain everywhere). Hence:
- every trajectory of the model is represented (a plain box only adds freedom);
- no correlation that the model does not have is imposed (a symbol never stands for two different
  physical quantities, and the symbols of two ports are distinct).

**Where:**
- `engine/affine/port_symbols.py`: `settings` (line 49) builds the per-port values; `with_port`
  (line 93) and `with_deposit_port` (line 133) set the kernel's module-level rate constant to the
  segment's port for one evaluation and restore it; `raw_dose` (line 107) re-implements the kernel's
  `actuations_A19.raw_dose` one mark at a time;
- `engine/affine/engine.py`: event durations of port *j* (line 155) and the coefficients of port *j*
  (line 222);
- tests in `engine/tests/test_v33_ports.py`.

**Questions.**
1. Does every kernel use of LM, LS, LE, M that depends on a port receive that port's value, and does
   every other use keep the plain box? (In particular: are all segments of a deposit history on one
   port, and is the fallback to the plain box correct when they are not?)
2. Is the per-mark `raw_dose` identical to the kernel's for a single-port history, and correct for a
   history that mixes ports?

Fix R (`engine/affine/recovery_group.py`) and the no-fire cover (`engine/affine/nofire_cover.py`) are
in the program but were not triggered in this campaign; reviewing them is welcome but not needed for
the reported result.

---

## What is out of scope here

- The scientific hypothesis behind the model (see `docs/MODEL_BOUNDARY_EN.txt`).
- Whether the parameter box is physically meaningful.

The question in every task is whether the computation encloses all admissible trajectories of the
model as coded. Correspondence between the code and the model's written definition is a separate
obligation, listed in [docs/DETAILS.md](docs/DETAILS.md#path-to-qualification).
