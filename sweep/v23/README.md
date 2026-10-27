# Box-width sweep with the scenario launcher (engine v2.3 / v2.3.1)

**See also** [`../v33_c7/`](../v33_c7/README.md): at ε = 1e-3 the v3.3 program with two added lemmas
reaches the same result, which is the shorter route to a proof. This folder keeps the scenario
launcher, which also goes further on wider boxes.

**Question.** The [v3.3 sweep](../README.md) stopped at layer 18 for ε = 1e-3, layer 8 for 3e-3 and
layer 5 for 1e-2. How far does a newer engine get on the same boxes?

**Engine.** The Fast Scenario Launcher keeps each possible output history of a cell as a separate
*scenario* (one job per compatible triple of parent histories) instead of joining them. The physical
kernel is the same as v3.3. Two versions were used:

| Engine | `source_identity` | Sources | Used for |
|---|---|---|---|
| v2.3 | `549f6726…eb544` | [`SOURCE_V23_FOR_REPLAY.zip`](SOURCE_V23_FOR_REPLAY.zip) (sha256 `c79af2fe…caec3d`) | ε = 1e-2, layers 1–9 |
| v2.3.1 | `d892d759…8ad2ce` | [`SOURCE_V231_FOR_REPLAY.zip`](SOURCE_V231_FOR_REPLAY.zip) (sha256 `bef16cd5…d944e24`) | ε = 1e-3, ε = 3e-3, diagnostic rerun at 1e-2 |

v2.3.1 differs from v2.3 by one guard in `engine/affine/scenario_engine.py`: an ambiguous READY
advance (p ≠ 2) is no longer sent to the slow-recovery resolver, where it crashed, but returns the
original refusal to the documented READY continuation. Only a path that always crashed changes. The
launcher still prints the banner "Fast Scenario Launcher v2.1"; the identity that counts is
`source_identity` in each `campaign.json`. The initial-state uncertainty stays at ±1e-5.

These are research campaigns (`experimental_not_qualified`). **The manual proof in `proof/` covers
ε = 1e-4 only; nothing here extends it.**

## Results

| ε | v3.3 sweep (published) | Scenario launcher | First refusal / status |
|---|---|---|---|
| 1e-4 | 18 of 18 (proved) | not run | control campaign still to do |
| 1e-3 | 17 | **18 of 18** (v2.3.1) | none; enclosures wide at the mirror cells (18, 4) and (18, 8) |
| 3e-3 | 7 | **at least 12** (v2.3.1) | campaign stopped by the author during layer 13 (estimated ~24 h to finish); not a refusal |
| 1e-2 | 4 | **9** (v2.3) | layer 10 computed but never verified; layer 11, lane 0: "Local-cycle branch budget exceeded" (v2.3.1 diagnostic) |

### ε = 1e-3: all 18 layers ([`eps_1em3/`](eps_1em3/))

- Run `769c6794…`, layer 18 `research_scenario_layer_complete`, independent verification of the whole
  prefix (`"through": 18`). The hashes of `manifest.json` and of the 12 receipts match `complete.json`
  and `verification.json`.
- One history per cell at every layer (12 jobs at layer 18): no scenario split.
- **Agreement with v3.3.** On layers 1–17, the per-layer widths ([`WIDTHS_BY_LAYER.csv`](eps_1em3/WIDTHS_BY_LAYER.csv),
  same column definitions as [`../WIDTHS_BY_LAYER.csv`](../WIDTHS_BY_LAYER.csv)) agree with the v3.3
  campaign at the same ε: identical to four digits on layers 1–3; median date width within −18 % / +6 %
  and usually within 3 %; maximum date width and maximum gain width equal or smaller, except the known
  isolated layer-10 date (0.41 against 0.22, see the v3.3 sweep notes). Two independent engines giving
  the same enclosures is a consistency check, not a proof that v2.3.1 is sound.
- **Layer 18 is at the edge of the method.** Median date width 0.0305 (0.0073 at 1e-4). The mirror
  cells (18, 4) and (18, 8) end with date widths 0.446 and 0.437 and a learned gain in about
  [1.47, 1.90]; each took about 46 min, against about 40 s for the other cells. Cell (18, 6), refused
  by v3.3, is accepted with date width 0.218. Per-cell values: [`CELLS_LAYER_18.txt`](eps_1em3/CELLS_LAYER_18.txt).
- Layer 18 took 2789 s, of which 13 s verification.
- **Future invariance** ([`eps_1em3/future/`](eps_1em3/future/README.md)). The 216 terminal
  enclosures pass both published future-wave checkers, adapted to ε: 191 active cells firing once per
  pulse, whole network at rest before 12.791, idle margin above 7.209, and a return to Q. Both
  adapted checkers reproduce the published 1e-4 outputs exactly.
- **Engine soundness** ([`AUDIT_ENGINE_V231.md`](AUDIT_ENGINE_V231.md),
  [`proof_extension/LEMMAS_EN.md`](proof_extension/LEMMAS_EN.md)). A reading of every change from
  v3.3 to v2.3.1 found no path to a false acceptance. The new acceptance rules need ten short lemmas
  to enter the learning-coverage argument.

So at ε = 1e-3 the computed chain has the same shape as the proved 1e-4 result (training enclosed,
terminal domain, exact transmission of every future pulse word). What it still lacks to be a
theorem is listed below.

### ε = 1e-2: 9 layers ([`eps_1em2/`](eps_1em2/))

- Run `518c080a…`, engine v2.3. Layers 1–9 complete and verified ([`layer_09/complete.json`](eps_1em2/layer_09/complete.json)).
- Layer 10: the 12 jobs were computed but the layer was never verified (no `manifest.json` /
  `complete.json`): **not accepted**.
- Layer 11, lane 0: the campaign stopped on a crash of the launcher
  ([`refusal_v23_crash_lane0.json`](eps_1em2/layer_11/refusal_v23_crash_lane0.json),
  `AttributeError` in `return_with_marks`). The underlying ambiguity is in READY state ("ready guard
  still overlaps external boundary or possible tangency"), the case fixed in v2.3.1.
- Rerunning the same job with v2.3.1 gives a clean refusal: "Local-cycle branch budget exceeded",
  2053 pending events ([`refusal_v231_diagnostic_lane0.json`](eps_1em2/layer_11/refusal_v231_diagnostic_lane0.json)).
  With an experimental budget of 4096 the job still refuses ("admissible event-order budget exceeded")
  after 973 s; that second record is not archived. This rerun is a diagnostic, not a campaign artifact:
  its engine identity differs from the campaign's.
- At this box width the limit is the number of admissible event orders, not a bug or the width of the
  enclosures.

### ε = 3e-3: at least 12 layers ([`eps_3em3/`](eps_3em3/))

- Engine v2.3.1. The run log ([`RUN_LOG_PARTIAL.txt`](eps_3em3/RUN_LOG_PARTIAL.txt)) shows layers 1–12
  complete with the prefix verified, and layer 13 in progress when the run was stopped. Its
  `campaign.json` and completion records are not archived here, so this row rests on the log only.
- Scenarios split from layer 11 on (67 jobs at layer 11, 133 at layer 12, against 12 without splits):
  this is where the event-order branching becomes visible.

## Not established

- **No control campaign at ε = 1e-4 with the scenario launcher.** It would show directly that the new
  engine reproduces the proved v3.3 campaign; the 1e-3 width comparison above is the available
  substitute.
- **Review of the lemmas B1, B2, C1–C8** and their insertion into the coverage theorem. Until then
  the v2.3.1 campaigns are computations, not proved enclosures.
- A general-ε wording of `proof/FUTURE_INVARIANCE_PROOF_EN.txt`.
- `affine/artifacts.py` (record serialization) was not audited.
- The memo flags used by the runs (assumption A5) are not recorded in `kernel_id`.
- The full outputs (`result.json`, about 80 MB for layer 18 at 1e-3 alone) are not in the repository.

## Files

| Path | Content |
|---|---|
| `SOURCE_V23_FOR_REPLAY.zip`, `SOURCE_V231_FOR_REPLAY.zip` | engine packages (sources, Linux CPython 3.12 binaries, tests, validation records) |
| `eps_1em3/` | `campaign.json`, layer 18 `complete.json` / `verification.json` / `manifest.json`, per-layer widths, layer-18 cells, run log |
| `eps_1em3/future/` | terminal enclosures, the two future-wave checkers adapted to ε, their results at 1e-3 and their non-regression checks at 1e-4 |
| `AUDIT_ENGINE_V231.md` | soundness audit of every change from v3.3 to v2.3.1 |
| `proof_extension/LEMMAS_EN.md` | lemmas B1, B2, C1–C8 and the assumptions needed to extend the coverage argument |
| `eps_1em2/` | `campaign.json`, layer 9 `complete.json`, layer 11 crash record, `stopped.json`, v2.3.1 diagnostic refusal, run log, author's note (French) |
| `eps_3em3/` | partial run log |
| `START_TIMES.txt` | start times of the 1e-2 and 1e-3 runs |
