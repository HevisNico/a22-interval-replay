# Box-width sweep

**Question.** How much wider can the parameter box be before the campaign stops certifying?

**Method.** Four fresh 18-layer campaigns of the same program, from layer 1, each in its own output
folder with its own program identity. The only change is the relative half-width ε of the physical
constants (LM, LS, LE, M and C, per port as in v3.3). The initial-state uncertainty stays at ±1e-5,
so that a single quantity varies. The 1e-4 row is the published v3.3 campaign.

These are research campaigns with the same status as v3.3 (`experimental_not_qualified`). The manual
proof in `proof/` is written for ε = 1e-4 only; nothing here extends it to other boxes.

## Results

| ε | Layers accepted | First refusal | Median output-date width, layer 17 | Layer 18 |
|---|---|---|---|---|
| 1e-4 (v3.3) | 18 of 18 | none | 0.00385 | 0.00728 |
| 3e-4 | 18 of 18 | none | 0.00535 | 0.0120 |
| 1e-3 | 17 | layer 18, lane 6: a logarithm argument no longer proved positive (time of maximal charge in a READY segment) | 0.0132 | not accepted |
| 3e-3 | 7 | layer 8, lane 0: the end of a slow phase cannot be separated from an external event group | — | — |
| 1e-2 | 4 | layer 5 | — | — |

Per-layer medians and maxima of the date widths, and the largest learned-gain width, are in
[`WIDTHS_BY_LAYER.csv`](WIDTHS_BY_LAYER.csv), rebuilt from the run summaries by
`python3 sweep/make_width_table.py`.

## What it shows

- **The enclosures stay roughly proportional to ε.** Write the median width of a layer as a + b·ε and
  fit a and b on the 1e-4 and 3e-4 campaigns. At ε = 1e-3, the observed median agrees with this fit
  to within 25 % on every accepted layer, and within 5 % on most of them. At ε = 3e-3, the largest
  widths of layer 3 (dates 0.0073, gains 0.073) are within about 6 % of the same fit. The first
  layers do not depend on ε at all: their width comes from the initial-state uncertainty and from
  the source.
- **What fails first is an order decision, not the size of the enclosures.** The program must decide
  the order of nearby events (a threshold crossing, the end of a slow phase, an arrival). Once the
  enclosures, though still linear in ε, become comparable to the gaps between such events, an order
  can no longer be certified and the cell is refused. The wider the box, the earlier this happens.
- **The first refusal at 1e-3 is at lane 6**, the lane opposite the source, where the two fronts that
  travel round the ring meet. The exploratory layer-19 computation of the open entry problem
  stopped at the same lane, cell (19, 6).

A refusal is a limit of the computation, not a physical counterexample.

## Files

| Folder | Content |
|---|---|
| `SOURCE_FOR_REPLAY.zip` | The exact sources of the sweep program and its two compiled extensions. It differs from `engine/` only by the ε setting (`affine/experiment_parameters.py`, used in `affine/engine.py`, `affine/port_symbols.py`, `affine/port_box_adapter.py`, `run.py`, `launch_fresh.py`) and one added test. ε enters the campaign identity. `_rounding_native` is byte-identical to v3.3; `_a22_native` was rebuilt. |
| `eps_3em4/` | ε = 3e-4: campaign identity, run status and summary, run log, receipt, manifest of the full output, replay instructions |
| `eps_1em3/` | ε = 1e-3: the same records (the manifest includes the refusal record of layer 18) |
| `eps_3em3/` | ε = 3e-3: the same records (refusal at layer 8) |

The full campaign outputs (several GB) are not in the repository. Each `RUN_MANIFEST.json` lists every
output file with its SHA-256, and each `SETUP_AND_REPLAY_EN.txt` explains how to verify an archived run
or recompute it from scratch. For ε = 3e-4, the files `eps_3em4_MANIFEST.json`, `eps_3em4.log`,
`eps_3em4_summary.json`, `eps_3em4_RUN_STATUS.json` and `eps_3em4_PACKAGE_RECEIPT.json` of the delivery
are stored here as `RUN_MANIFEST.json`, `RUN_LOG.txt`, `RUN_SUMMARY.json`, `RUN_STATUS.json` and
`PACKAGE_RECEIPT.json`, with their bytes unchanged. The ε = 1e-2 records are not yet included.

The campaigns were run with ChatGPT under the author's direction. Claude checked the sources
against the published engine, the delivered hashes and identities, and computed the comparisons above.
