# Soundness audit of engine v2.3.1 against v3.3

**Scope.** Every source change between `engine/` (v3.3, covered by the manual proof) and
`sweep/v23/SOURCE_V231_FOR_REPLAY.zip` (`source_identity` `d892d759…`), read for one question: can
the change make the engine *accept* an enclosure that misses some admissible device? Step A covers
the kernel files, native arithmetic, clock sums, scenario joining and refusal continuation. Step B
covers `affine/engine.py` and the new modules. It is a code reading, not a proof.

**Result.** No path to a false acceptance was found. Each new acceptance rule relies on a short
argument that the manual proof does not contain yet: lemmas B1, B2 (step A) and C1–C8 (step B).
Two items are execution assumptions (A2, A5). Serialization (`artifacts.py`) was not audited.

**Consequence for ε = 1e-3.** If lemmas B1, B2 and C1–C8 are added to the learning-coverage argument
and the execution assumptions are accepted, the coverage argument written for v3.3 would apply to the
v2.3.1 campaign. Together with the future-wave certificate checked by two programs at ε = 1e-3, this
would give the same chain as the published 1e-4 result at a box ten times wider.

# Step A

## Kernel files

| File | Change | Verdict |
|---|---|---|
| `kernel/.../depot_A19.py` | the offered-deposit expression moved into `completed(h)`; same operations | no semantic change |
| `kernel/.../retour_file_A22.py` | the return solver becomes a parameter (default: the original `return_with_marks`) | sound if the injected solver is (see `recovery_tightening`) |
| `kernel/.../cycle_relatif_A22.py` | same parameter, plus optional `contract_order` | sound, lemma **B1** |

**B1 (weak-order contraction).** For each enumerated weak order, the branch only covers
trajectories in which every earlier event date is ≤ the return and every later event date is ≥ the
return. Then `return ≥ max(lower ends of earlier dates, start)` and `return ≤ min(upper ends of later
dates, upper)` are necessary conditions. Intersecting the return box with them keeps every trajectory
of that order, and an empty intersection removes only that order. This relies on the existing
property that the enumeration covers every admissible order (unchanged kernel, already in the proof).
The restricted date keeps the original affine expression, as the v3.3 code already does
(`:restricted`).

## Return solver `affine/recovery_tightening.py`

`contract_return` starts from the root enclosure certified by `return_with_marks` / `v.root`, then
bisects inside it on the sign of the protected ledger `ell`, evaluated over the whole state box with
`live=False`, the same convention as the root solver.

**B2 (sign contraction).** `v.root` proves a strictly positive slope of `-ell` on its bracket, and
Newton steps stay inside it. So `ell` is strictly decreasing there for every admissible device, and
its zero is unique there. If `ell(mid) > 0` for the whole box, every device returns after `mid`; if
`ell(mid) < 0`, before. Contracting to the remaining part is sound. `window()` returns `None` (no
claim) on any refusal or on any branch that fires or does not end READY.

## Native arithmetic and clock sums

- `rounding_native.c`: `add` is split into `add_into` (same operations, in place on a private
  dictionary) and `add`. `multiply_coeff` now accumulates into its own fresh scaled copy. New
  `time_sum_parts`, `time_sum_centers`, `time_sum_key` and `accumulate_coeff`: centers use the directed
  Decimal contexts (`DOWN.add`, `UP.add`, endpoints swapped and negated for multiplier −1); scaling by
  −1 is exact; binary64 coefficient sums add their rounding bound; input remainders are added upward;
  other multipliers go through the original affine `__mul__`. Sound.
- `affine/time_sum.py`: the cache key holds the input affine objects themselves. `I` defines no
  `__eq__` or `__hash__`, so keys compare by identity, and the cache keeps the objects alive (no reuse
  of ids). Centers are recomputed on every hit; only the coefficient reduction is reused. `I.make`
  still allocates a fresh noise symbol on every call, and the native `new_form` copies the dictionary,
  so a cached dictionary is never shared or mutated. Sound.
- **A2.** That the shipped `_rounding_native` binary (`3dcf376b…`) is compiled from this source is an
  assumption (the binary contains the four new entry points). It falls under A1–A4, as in v3.3.

## Scenario joining (`run_scenarios.py`, `affine/scenario_engine.py`)

- A child job takes one scenario per parent. Combinations are kept only when the shared ancestor
  cells carry the same scenario. Every device has one true history per cell, and that history lies
  in at least one scenario of its cell, so a consistent combination exists for every device: dropping
  the inconsistent ones loses no device. Physical symbols are named per cell (same device in every
  job); rounding and remainder symbols are named per job (no false correlation). Sound as an outer
  cover.
- **For the ε = 1e-3 campaign every cell has exactly one scenario**, so the joining is never
  exercised there.
- Continuation after a refusal: the state is read from the local variables of the kernel loop at the
  refusal. `advance` raises before `flowing`, and `flowing` works on `s.copy()`. The state read back
  is therefore the state before the failed step. Checked for the READY-guard refusal that occurs at
  layer 11; the other refusal sites were not inspected one by one.
- v2.3.1 guard (`split` returns `None` unless `p == 2`): the original refusal is re-raised. It can
  only refuse or follow the documented READY continuation.

# Step B

## Patches applied by `affine/engine.py` to the kernel at run time

| Patch | What it does | Verdict |
|---|---|---|
| `flowing`, READY peak inside an exterior cluster | when the peak-time logarithm has no positive argument, bound the charge with the kernel's `ready_general_A22.peak_upper` (unchanged since v3.3), else with `cluster_memory_cover` | sound, lemma **C7** |
| `advance`, same case | if `peak_upper(s, boundary) < 1`, flow to the boundary; otherwise the original refusal | sound, **C7** (in READY the only internal guard is the fire) |
| Root search: previous root, `LazyGuess` | only change where a bracket is *tried*; acceptance still needs both endpoint signs and a positive slope | no effect on soundness |
| `h(u)` on symbolic ages | mean-value form `_unary(point value, derivative range)`, the same construction as `exp` and `ln` | sound |
| Exterior cluster: enumeration through `CLUSTER_STATES` | same enumeration, with identical prefixes shared (`cluster_prefix`) and the commuting shortcut (`ready_commuting`) | sound, see below |
| Exterior cluster: "slow section inside external cluster" | routed to the v3.3 recovery-group resolver (with the step-A tightening); `None` re-raises | sound (B1, B2) |
| `protected_section_cluster` | same enumeration through `cluster_prefix` (no guard-free flow), then the `protected_commuting` shortcut | sound, see below |
| `settings_cell`, `port_symbols`, `port_box_adapter`, `run.py` | ε read from `experiment_parameters` (ε enters `kernel_id`); physical symbols named per cell | consistent |
| `history_key` / `history_lookup_key` caching | key cached only on `Time` objects (frozen except the lazy box, which is not in the key) and on histories checked recursively immutable | sound |

## New modules

- **`cluster_prefix`.** Orders sharing an identical prefix (same event objects, compared by identity,
  kept alive during the generator) reuse the prefix state. `flowing` and `act` copy before updating,
  so this equals recomputation, except that the prefix shares its remainder symbols, which stand for
  the same computation in both branches. Every order is still yielded. Sound.
- **`event_order_cache`.** A reimplementation of `admissible_orders`. It prunes only on certified
  predicates: a remaining event certainly earlier must come first; an event certainly before its
  predecessor is impossible; an event whose upper date is below the largest lower date of the prefix
  is impossible; aux-stage and raw on/off transitions as in the original. Pruning only on certified
  contradictions cannot drop a real order. Budgets raise refusals. Sound.
- **`sparse_hull`** (replaces the hull everywhere). Common coefficient = midpoint of each symbol's
  range, with 0 included when a branch lacks the symbol. Each branch's radius adds, rounded upward,
  `|d − common|` for its own symbols and the exact integer sum (in units of 2⁻¹⁰⁷⁴) of `|common|` for
  the symbols it lacks. So every branch is enclosed for every ε, which is lemma **C5** (a pointwise
  union of affine forms). Sound.
- **`cluster_memory_cover`.** Splits [t, tt] into pieces and requires the kernel's pulse-memory
  charge `< 1` on each piece, refusing at depth 8. Lemma **C6** (a piecewise interval bound). Sound if
  `dep.evaluate` is a valid enclosure over time intervals (kernel, unchanged).
- **`memory_root`** (fallback when the READY guard is ambiguous). Requires `q(0) < 1`, `q(hi) ≥ 1`
  and `q' > 0` over the whole `[0, hi]`, then a certified root strictly before the next external
  boundary. In READY the fire is the only internal guard: aux transitions are external events in the
  queue. So the root is the first crossing and nothing happens before it. Lemma **C2**. Sound.
- **`correlated_first_delay`.** It narrows each port's first auxiliary delay once the first arrival
  is certainly after `U0`. The initial deviation of `m` is then at most `Δ·e^{−κ·t}`, since an initial
  ERROR tail ends exactly at `r_m`. Write `σ = M_lo·h'(0.1) − κ·Δ·e^{−κ·t₀}`, where `h'` is decreasing
  on [0, 0.1] because (a/κ)² > e^{(a−κ)·0.1}. The root then moves by at most `Δ·e^{−κ·t₀}/σ`. The new
  delay must also lie inside the old one. Lemma **C1**. Sound.
- **`ready_commuting`.** In READY with constant gains (no open deposit) and no protected ledger,
  and with only raw on/off and mark on/off events, each port's events are applied in their certified
  per-port order. The complete pulse memory (zero response before each arrival) must then be strictly
  below 1 over the whole window. `act` reads the synthetic clock only to date mark ends, the gains are
  constant by precondition, and the final charge comes from the memory. So every interleaving reaches
  the same endpoint. Lemma **C3**. Sound.
- **`protected_commuting`.** It starts in the FAST phase with closed gain gates and one fire in every
  ledger, requires U ≥ fire + 1, and allows at most one on-event per kind and port, in certified
  per-port order. The ledger `ell` is non-increasing, so `ell(U) > 0` excludes a return to READY in
  the window, and deposits stay closed because P ≠ READY. All interleavings share one SLOW endpoint.
  Lemma **C4**. Sound.
- **`recovery_group`** (changed). When the v3.3 resolver fails, it tries the step-A tightening and
  then re-anchors the joined READY state with the kernel's `new_memory` (the enclosing charge plus the
  active inputs). This drops correlations but loses no state. Lemma **C8**. Sound.
- **`transfer_memo`** (on by default). Exact replay of `flux.transfer` / `dz.completed`. That
  function is pure affine arithmetic on frozen `Segment`/`History`/`Time` objects. The key holds the
  objects alive (identity cannot be reused), adds the lazy numeric state of the inputs, the Decimal
  contexts and the affine configuration. Fresh remainder names are renamed to the positions an
  uncached call would allocate, and the counter is advanced accordingly. Sound, provided the replay
  is exact (**A5**).
- **`temporal_memo`**: off unless `A22_EXACT_TIME_MEMO=1`; with the default, `Time.minus` runs the
  reference path through `time_sum` (step A).

## Execution assumptions added

- **A5.** The campaigns ran with the default flags (`A22_TRANSFER_MEMO` on, `A22_EXACT_TIME_MEMO`
  off). These flags change the computation path but do not enter `source_identity` or `kernel_id`.
  Both paths are designed to give the same result, but the record does not prove which one ran.

## Not audited

- `affine/artifacts.py` (133 changed lines: serialization, typed views). It concerns the integrity
  of the records, not the arithmetic. The "independent verification" of a layer re-reads and checks
  records and their ancestry; like v3.3, it does not recompute the physics.
- The kernel functions used unchanged (`dep.evaluate`, `new_memory`, `peak_upper`, `v.ready`) are
  taken as covered by the existing proof.

## Lemmas to add to the learning-coverage argument

B1 weak-order contraction · B2 sign contraction of the return · C1 correlated first delay ·
C2 monotone pulse-memory root · C3 READY commuting group · C4 protected commuting group ·
C5 pointwise sparse hull · C6 piecewise no-fire cover · C7 peak fallback through `peak_upper` ·
C8 READY re-anchoring at a recovery join.
