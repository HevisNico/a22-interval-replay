# A22 — validated interval replay of the full 128-pulse learning transient

**Contribution.** This is a computer-assisted enclosure of **all admissible trajectories** of a learning
spiking network during its full 128-pulse training transient. The network has 216 coupled hybrid cells
(18 layers × 12 lanes) with:
- uncertain physical parameters (±1e-4 relative), **independent for each input port of each cell**,
  as the model specifies;
- uncertain initial states (±1e-5);
- evolving learned gains and a recovery actuator;
- threshold crossings;
- events whose order may vary.

In concrete terms, for every parameter vector in the box:
- the learned gains after training are determined to within ±2.4 % in the worst cell;
- spike dates are determined to within 7.3e-3 time units for the median cell at the last layer.

So in this realization, the outcome of learning is fixed by the input protocol up to small, quantified
margins, despite physical variability. Point simulations can suggest this, but they cannot establish it.

**State of the work.** The computation is complete and cross-checked:
- all 18 layers completed, with no forced decision;
- every layer was re-read by a separate verifier process;
- every spike decision in the four hardest or most sensitive cells was re-proved by an independent
  script;
- the independent A14 reference gains fall inside the computed enclosures in **648 of 648** cases.

The proof that the program is correct is not finished. Specialists can help with short, self-contained
review tasks: see **[REVIEW.md](REVIEW.md)**.

> **Status: experimental, not a qualified all-trajectories proof.** The computation is complete and
> reproducible. The proof that the program is correct is not complete yet (see
> [docs/DETAILS.md](docs/DETAILS.md#path-to-qualification)).

| | |
|---|---|
| Layers completed / cells | 18 / 216, each layer re-read by a separate verifier process |
| A14 reference gain boxes inside our enclosures | **648 / 648** (exact rational test) |
| Independent H1/H2 re-check, layer 18 lanes 1, 4, 8, 11 | 418 / 418 spikes and 3,600 / 3,600 "no spike" decisions re-proved |
| Output-date width, median cell, layer 18 | 7.3e-3 time units (worst cell: 3.8e-2) |
| Learned gains, worst relative half-width (all cells) | ±2.4 % (cell 18,6); widest absolute: 7.5e-2 on a gain of 1.69 (cells 18,4 and 18,8) |
| Computation-remainder share of the widest date, median cell | ≈ 0 up to layer 10, 45 % at layer 18 |
| Critical-path time, 8 workers | 49 min in total (layer 18: 24 min) |

![Output-date enclosure width by layer](figures/date_width_by_layer.png)

*Median output-date width per layer. v3.3 treats each port's constants as independent, as the model
specifies; v3.2 shared them across the three ports of a cell. The more general model costs at most 5 %
of width (layer 18: 7.28e-3 against 6.91e-3).*

## What was closed

The A14 reference (`results/reference_A14_gain_boxes.json`) lists one item as **unclosed**: *"A validated
interval replay of the complete 128-pulse learning transient from the initial state."* This campaign is
that replay. It agrees with the reference on all 648 learned-gain boxes. Those reference gains were
observed numerically with parameters within 1e-8, a set that lies inside the parameter box used here.

## Version history in one paragraph

The **v3.2** campaign (kept in [`history/v3.2/`](history/v3.2/)) completed, but it gave the auxiliary
constants of a cell (LM, LS, LE, M, C) **one** symbol shared by its three ports. The author found, with
an exact counterexample, that the model makes them independent per port; v3.2 therefore covered only a
sub-family. A first correction replaced the shared symbols by plain interval boxes. That is sound, but
it forgets that a port keeps the same constant at every pulse: enclosures grew 3–10× and the campaign
stopped at layer 18 ([`history/plain_box_package/`](history/plain_box_package/)). **v3.3** gives each
port its own symbol, used only for that port's quantities. It is the campaign reported here.

## Reproduce

Requirements: Linux x86-64, CPython 3.12, a C compiler, OpenSSL development headers, NumPy 2.3.5,
SciPy 1.17.0.

```
cd engine
python -m pip install -r requirements.txt
python build_all_native.py
python -B -m unittest discover -s tests                 # 77 tests
python launch_fresh.py --out results/A22_v33_001        # 8 workers by default, ~12 GiB RAM
```

Then the checks (`--out` files must be outside the campaign directory):

```
python -B tools/verif_h1h2.py --campaign results/A22_v33_001 --layer 18 --lane 4 --out ../h1h2_18_04.json
python -B tools/bilan_campagne.py --campaign results/A22_v33_001 \
       --reference ../results/reference_A14_gain_boxes.json --out ../summary.json
```

The native extensions are built on the target machine, so the kernel_id of a new campaign differs from
ours (it includes the built binaries and the environment). The program-source identity before the
build is fixed; see [results/HASHES.md](results/HASHES.md).

## Contents

| Path | What it is |
|---|---|
| `engine/` | The exact v3.3 program package used for the campaign (physics kernel unchanged since the first release) |
| `tools/` | The read-only check scripts (same files as `engine/tools/`) |
| `results/campaign_summary.json` | Per-layer and per-cell summary of the campaign (timings, widths, gains, A14 inclusion) |
| `results/h1h2_layer18_lanes_1_4_8_11.json` | Independent re-check of every spike decision in four layer-18 cells |
| `results/layers_cells_and_timings.json` | Per-layer `cells.tsv` rows and `complete.json` of the campaign, in one file |
| `results/campaign_identity.json` | Campaign identity (run_id, kernel_id, environment): the campaign's `campaign.json` |
| `results/reference_A14_gain_boxes.json` | Independent reference gains (exact fractions) |
| `results/v2_refusal_layer18_lane4.json` | The layer-18 refusal of the v2 engine, kept for the record |
| `results/HASHES.md` | Identities, provenance evidence, file hashes |
| `history/` | The v3.2 campaign (engine ZIP, summary, checks) and the plain-box refusal records |
| `docs/DETAILS.md` | Method, the changes that made layer 18 pass, checks, limitations, path to qualification |
| `docs/AUDIT_EN.txt`, `docs/MODEL_BOUNDARY_EN.txt` | Earlier arithmetic audit; scope of the model |
| `REVIEW.md` | Call for review: five self-contained tasks (1–2 h each) |
| `figures/` | Figures (PNG and SVG) |

## How this was built

The model and the research questions are the author's. The code was developed with AI assistants
(Claude and others) under the author's direction; the author designed the model, found the
port-independence gap with an exact counterexample, and directed and validated the work. This is why
the repository does not ask to be taken on trust. The campaign identity is bound to the exact code by
hashes, every layer is re-read by a separate process, critical decisions are re-proved by independent
scripts, and the results are compared with an independent reference.

## License and citation

Code (`engine/`, `tools/`, the engine ZIP in `history/v3.2/`): MIT, see `LICENSE`. Documentation,
figures and results: CC BY 4.0, see `LICENSE-docs.md`. To cite, use `CITATION.cff` (GitHub's "Cite this
repository" button).

Scope: the result is about the A22 realization and its parameter box. It is not a statement about the
reset-operator hypothesis R in general (see `docs/MODEL_BOUNDARY_EN.txt`).
