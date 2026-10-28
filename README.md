# A22 — enclosing every learning trajectory of a 216-cell spiking network, with a manual proof

**Contribution.** This repository contains a computer-assisted enclosure of **all admissible
trajectories** of a learning spiking network during its full 128-pulse training transient, together with
a written proof that the computation covers them and that the learned state is then **invariant for
every admissible future input**. The network has 216 coupled hybrid cells (18 layers × 12 lanes) with:
- uncertain physical parameters (±1e-4 relative), **independent for each input port of each cell**;
- uncertain initial states (±1e-5);
- evolving learned gains and a recovery actuator;
- threshold crossings, and events whose order may vary.

**The result**, for every fixed device in the parameter box and every admissible initial state (proof in
[`proof/`](proof/), under the execution assumptions A1–A4 stated there):

1. **Training.** After the 128 training pulses (times 8k, horizon 1116), the network is in an explicit
   quiescent domain Q. The learned gains are determined to within ±2.4 % in the worst cell, and the
   training spike dates to within 7.3e-3 time units for the median cell of the last layer.
2. **Afterwards, forever.** From Q, for every future sequence of source pulses spaced by at least 20:
   each of the 191 active cells fires **exactly once** per pulse, the whole network is back at rest
   within 12.791 time units, and the network returns to Q.
3. **Exact transmission.** Each active cell answers with a fixed latency, so the intervals between
   pulses are transmitted **exactly** through all 18 layers. The latencies depend on the device and on
   the learned gains; they are not claimed to be equal across devices.

So in this realization, local learning rules install, for every device in the box, a regime that
transmits temporal patterns exactly. The box is much smaller than the variability of real
components.

> **Made with AI.** The code, the diagnostics and the written proof were produced with Claude
> (Anthropic) and ChatGPT (OpenAI) under the author's direction (see [How this was built](#how-this-was-built)).
>
> **Status.** The computation is complete, reproducible and bound to its exact code by hashes. The
> coverage and invariance argument is a manual proof under explicit execution assumptions (A1–A4:
> authentic execution of the recorded program, correct arithmetic runtime and native binary,
> fail-closed assertions, namespace discipline), not yet reviewed by an independent expert, and
> machine-checked only in parts: the abstract core of the strict-root lemma, the lemmas added in
> v4.4, the first-crossing facts and the number-free steps of the future proof (Lean 4, [`proof/lean/`](proof/lean/README.md)). This applies to every result in the repository. Review is welcome:
> **[REVIEW.md](REVIEW.md)**.

| | |
|---|---|
| Layers completed / cells | 18 / 216, each layer re-read by a separate verifier process |
| Campaign identity | `kernel_id` **reproduced exactly** from the published sources and the two archived binaries |
| A14 reference gain boxes inside our enclosures | **648 / 648** (exact rational test) |
| Independent H1/H2 re-check, layer 18 lanes 1, 4, 8, 11 | 418 / 418 spikes and 3,600 / 3,600 "no spike" decisions re-proved |
| Output-date width, median cell, layer 18 | 7.3e-3 time units (worst cell: 3.8e-2) |
| Learned gains, worst relative half-width | ±2.4 % (cell 18,6) |
| Future regime (from Q) | 191 active cells, one spike each per pulse; network at rest within 12.791; margin > 7.209 before the next pulse |
| Future-domain inequalities | checked by two independent programs (different arithmetic, no engine import) |
| Critical-path time, 8 workers | 49 min in total (layer 18: 24 min) |

![Output-date enclosure width by layer](figures/date_width_by_layer.png)

*Median output-date width per layer during training. v3.3 treats each port's constants as independent,
as the model specifies; v3.2 shared them across the three ports of a cell. The more general model costs
at most 5 % of width (layer 18: 7.28e-3 against 6.91e-3).*

## Start here

- **Every result with its scope, status and check, in one table**: [`RESULTS_STATUS.md`](RESULTS_STATUS.md).
- **Why this network matters**, what is already known and where the method stops working:
  [`WHY_A22_MATTERS.md`](WHY_A22_MATTERS.md).
- **The most useful single check**: Task 1 of [`REVIEW.md`](REVIEW.md), the strict-root lemma on which
  the whole event-order argument rests (one to three hours, no need to know the rest). Its abstract
  core is machine-checked in Lean 4 ([`proof/lean/`](proof/lean/README.md)); the bridge to the code
  is what remains to review.
- **How the proof fits together**: [`PROOF_WALKTHROUGH.md`](PROOF_WALKTHROUGH.md), a guided tour of
  the v3.3 argument in five propositions, from learning coverage to exact interval preservation, with
  the three most delicate points and a map to the source documents.
- **The proof itself**: start with
  [`proof/learning_justification/output/REVIEW_GUIDE_EN.txt`](proof/learning_justification/output/REVIEW_GUIDE_EN.txt).

## Beyond the 18 layers

Later releases extend the result; each is described in [`CHANGELOG.md`](CHANGELOG.md).

- **Arbitrary depth** ([`depth/`](depth/README.md)). For six prescribed preparations, training is
  certified through 68 layers (128 in one case), and tail theorems carry the learned regime to any
  depth: one limiting duration per layer, common to all lanes and to different preparations of the
  same medium, with exact transmission of every admissible pulse word.
- **Random media.** For any stationary ergodic medium, almost every realization has the same limiting
  speed, with proved speed ceilings.
- **Open problem** ([`depth/point4/`](depth/point4/README.md)). Whether *every* preparation of the
  original source enters that regime is open; the partial results and obstructions are recorded.
- **Box width** ([`sweep/`](sweep/README.md)). Research campaigns cover all 18 layers at ±3e-4; with the
  newer scenario engine ([`sweep/v23/`](sweep/v23/README.md)), all 18 at ±1e-3, at least 16 at ±3e-3 and 9
  at ±1e-2. With three added lemmas (C7, C6, E) the proof extends to ±1e-3 (v4.4 section below).

To check the depth release assets, run `python3 -I tools/verify_depth_assets.py <assets folder>`.

## v4.4: the same result on a box ten times wider (±1e-3)

The v3.3 program, extended by lemmas C7 and C6 (with remark P), gives the whole chain at ±1e-3 on
the physical constants (initial states still ±1e-5): training enclosed through all 18 layers, end of
training in Q, and exact transmission of every admissible pulse word afterwards
([`sweep/v33_c7/`](sweep/v33_c7/README.md)).

| | ±1e-4 (v3.3) | ±1e-3 (v3.3 + C7) |
|---|---|---|
| Layers accepted | 18 / 18 | 18 / 18 |
| Network emissions during training (all cells, over the 128 source pulses); active cells at exact rest | 21 302; 191 | 21 302; 191 |
| Future regime from Q (two independent checkers) | 191 cells fire once per pulse, at rest before 12.791 | the same |
| Smallest future margin | 0.0491 | 0.0489 |
| Additions to the proof | — | lemmas C7, C6 and remark P ([`LEMMAS_C7_C6_EN.txt`](sweep/v33_c7/LEMMAS_C7_C6_EN.txt)), machine-checked in Lean ([`PeakBounds.lean`](proof/lean/PeakBounds.lean)); lemma E, the commutation macro with an input arrival ([`CommutationE.lean`](proof/lean/CommutationE.lean) for its mathematical part), and the initial-section certificate rechecked at ±1e-3 ([coverage addendum](sweep/v33_c7/COVERAGE_THEOREM_GENERAL_EPS_EN.txt)); general-ε wording of the future proof ([future addendum](sweep/v33_c7/FUTURE_INVARIANCE_GENERAL_EPS_EN.txt)) |

C7 bounds the READY charge with the kernel's own monotone peak bound where v3.3 refused; C6 is a
piecewise version of the same bound; P establishes the root-bracket slope on a partition, without
changing the acceptance predicate. Lemma E is not a program change: at ±1e-3 the existing commutation
macro also handles input arrivals, which the v3.3 proof did not need, and lemma E proves that case.
The full outputs and the engine as run are assets of
[Release v4.4](https://github.com/HevisNico/a22-interval-replay/releases/tag/v4.4), and one command
checks everything, including the initial section and the commutations:
`python3 -I sweep/v33_c7/verify_release.py <assets folder> --strict`.

A newer engine, the scenario launcher v2.3.1 ([`sweep/v23/`](sweep/v23/README.md)), reaches the same
chain at ±1e-3 by another route, and goes further on wider boxes (at least 16 layers at ±3e-3, 9 at
±1e-2). Its coverage would need ten lemmas
([`LEMMAS_EN.md`](sweep/v23/proof_extension/LEMMAS_EN.md)).

## v4.3: conditional future invariance on a relative gain domain

The [G_rel dossier](depth/g_rel/README.md) characterizes regenerated learned states
that preserve the same 191-cell transmitting mask and exact temporal intervals.
Its common local gain-arrival inequalities admit different learning-dose patterns;
35 of 40 saved decimal vectors pass directed membership checks. Start with the
[one-page reviewer note](depth/g_rel/reviewer/ONE_PAGE_EN.pdf).
The theorem is conditional: it does not show that training reaches this domain.
The five unresolved cases are recorded.

## Origin of the model

The physical kernel of A22 is inspired by the **Reset Operator** of Nicolas Breuillaud (*The Reset
Operator: A Structural Constraint on Recursivity*, manuscript, 2026). The definition of the operator,
in particular of its coupling, is the one given in that paper; this repository does not restate it.

A22 is one concrete realization of a threshold–protection–return cycle: a READY phase in which inputs
charge the cell, a threshold crossing, protected fast and slow phases during which the principal
admission is closed, and a return to rest before admission reopens. The full model of the
realization is [`engine/reference/full_model_reference.md`](engine/reference/full_model_reference.md)
(in French). Its banner and its section 7 date from 18 October 2026, before the v3.3 campaign; read
[`engine/reference/STATUS_NOTE_EN.md`](engine/reference/STATUS_NOTE_EN.md) first. The physical
definition in that file is current; its status statements are historical.

The result concerns this realization only, not the Reset Operator hypothesis in general
([`docs/MODEL_BOUNDARY_EN.txt`](docs/MODEL_BOUNDARY_EN.txt)).

## How the proof is organized

The chain is: **initial section → every training step → terminal domain Q → every future wave.**

| Step | Where | How it is established |
|---|---|---|
| Initial section [0, U0] | `proof/final_entry_audit/` | analytic lemma + independent integer inequalities |
| Every training step of every cell | `proof/learning_justification/output/LEARNING_COVERAGE_THEOREM_EN.txt` | relational invariant (I1–I5) preserved by every successful program step; open-image lemma for strict root order; event coverage; memory joins |
| Entry into event groups | `proof/learning_justification/output/GROUP_ENTRY_CLOCK_LEMMA_EN.txt` | case split on the control paths |
| Composition over the 18 layers | same theorem, Section 10 | feedforward induction with shared parent identities |
| Training end ⊂ Q | same theorem, Sections 10–11 | exact terminal extraction (216 authenticated results) |
| Q → Q for every future pulse | `proof/FUTURE_INVARIANCE_PROOF_EN.txt` | analytic argument + two independent inequality checkers |
| Exact transmission of the pulse word | `proof/GLOBAL_THEOREM_AND_WORD_PRESERVATION_EN.txt`¹ | fixed influential gains + layer induction |

¹ Written before the learning-coverage theorem: its remark that H_entry is not discharged is
historical (H_entry is discharged by `LEARNING_COVERAGE_THEOREM_EN.txt`, see `proof/STATUS.json`). The
file, like `proof/TRAINING_ENTRY_REVIEW_EN.txt` and `proof/historical_status/`, is kept byte-identical
because its hash is cited.

## What was closed

The A14 reference (`results/reference_A14_gain_boxes.json`) lists one item as **unclosed**: *"A validated
interval replay of the complete 128-pulse learning transient from the initial state."* This campaign is
that replay. It agrees with the reference on all 648 learned-gain boxes. Those reference gains were
observed numerically with parameters within 1e-8, a set that lies inside the parameter box used here.

## Version history

**v3.3** is the campaign reported and proved here. It gives each port of a cell its own symbol for
each constant, as the model specifies; the earlier v3.2 campaign shared them across a cell's three
ports and therefore covered only a sub-family of the devices. The full history is in
[`CHANGELOG.md`](CHANGELOG.md).

## Reproduce

**The proof checks** (no engine import, no campaign): download the complete proof dossier from the
Release `v3.3-proof`, unzip it, and run from its folder, with Python 3 and without `-O`:

```
python3 learning_justification/verify_build_identity.py      # identities and kernel_id
python3 learning_justification/verify_source_witnesses.py    # 110 source facts
python3 kernel_soundness/extract_effective_source.py         # code as actually executed
python3 kernel_soundness/check_contract_countermodels.py
python3 provenance_audit/certify_future.py provenance_audit/output/all_terminal_exact.json future_recheck.json
python3 provenance_audit/verify_future_certificate.py provenance_audit/output/all_terminal_exact.json future_recheck.json independent_recheck.json
python3 final_entry_audit/certify_initial_section.py initial_recheck.json
```

**A new campaign** (requirements: Linux x86-64, CPython 3.12, a C compiler, OpenSSL development headers,
NumPy 2.3.5, SciPy 1.17.0):

```
cd engine
python -m pip install -r requirements.txt
python build_all_native.py
python -B -m unittest discover -s tests                 # 77 tests
python launch_fresh.py --out results/A22_v33_001        # 8 workers by default, ~12 GiB RAM
```

A new build produces new native binaries, so a new campaign has a different `kernel_id`; the proof is
about the recorded campaign. See [results/HASHES.md](results/HASHES.md) for both program identities.

## Contents

| Path | What it is |
|---|---|
| `WHY_A22_MATTERS.md` | Why this network matters: the question, related work, limits of the method |
| `PROOF_WALKTHROUGH.md` | Guided tour of the v3.3 proof: five propositions, three delicate points, source map |
| `CHANGELOG.md` | What each release added |
| `depth/` | The v4.0-depth extension: summary, certificates, theory, review records, layer index, verification replay; `depth/point4/` holds the open entry problem (v4.2) |
| `sweep/` | The box-width sweep: results, run records and the exact sweep program (v4.2) |
| `tools/verify_depth_assets.py` | Read-only integrity check of the v4.0-depth release assets |
| `proof/` | The proof dossier (theorems, lemmas, certificates, audit outputs, scripts); see `proof/OMITTED_IN_REPOSITORY.md` |
| `engine/` | The exact v3.3 program sources used for the campaign (physics kernel unchanged since the first release) |
| `tools/` | The read-only check scripts (same files as `engine/tools/`) |
| `results/campaign_summary.json` | Per-layer and per-cell summary of the campaign (timings, widths, gains, A14 inclusion) |
| `results/h1h2_layer18_lanes_1_4_8_11.json` | Independent re-check of every spike decision in four layer-18 cells |
| `results/layers_cells_and_timings.json` | Per-layer `cells.tsv` rows and `complete.json` of the campaign, in one file |
| `results/campaign_identity.json` | Campaign identity (run_id, kernel_id, environment) |
| `results/reference_A14_gain_boxes.json` | Independent reference gains (exact fractions) |
| `results/v2_refusal_layer18_lane4.json` | The layer-18 refusal of the v2 engine, kept for the record |
| `results/HASHES.md` | Identities, exact provenance reconstruction, file and Release-asset hashes |
| `history/` | The v3.2 campaign and the plain-box refusal records |
| `docs/DETAILS.md` | Method, fixes, results by layer, checks, limitations |
| `docs/AUDIT_EN.txt`, `docs/MODEL_BOUNDARY_EN.txt` | Earlier arithmetic audit; scope of the model |
| `REVIEW.md` | Call for review: self-contained tasks, most important first |
| `figures/` | Figures (PNG and SVG) |

## How this was built

This work was done with two AI assistants, **Claude** (Anthropic) and **ChatGPT** (OpenAI), under the
author's direction. The model, the Reset Operator and the research questions are the author's. Claude
and ChatGPT wrote and corrected the code, ran the diagnostics, drafted the proof (mainly ChatGPT) and
audited it (mainly Claude); each also re-checked the other's work. The author designed the model, ran
the campaigns and directed the work; he relied on the assistants for parts of the mathematics that he
has not checked in full himself. Hence the safeguards: the campaign is bound to its exact code by
reproducible hashes, every layer is re-read by a separate process, critical decisions are re-proved by
independent scripts, results are compared with an independent reference, and the proof states its
assumptions.

## License and citation

Code files anywhere in the repository or in its release assets: MIT, see `LICENSE`.
All other content (documents, proofs, figures, data, certificates, results): CC BY 4.0. The exact
scope is in `LICENSE-docs.md`. To cite, use
`CITATION.cff` (GitHub's "Cite this repository" button).

