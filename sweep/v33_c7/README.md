# The whole chain at ε = 1e-3 with program v3.3 + C7

**Result.** At relative half-width ε = 1e-3 on the physical constants (ten times the proved box;
initial states ±1e-5), the v3.3 program extended by two short lemmas encloses the complete training
transient of all 18 layers. The end of training lies in a quiescent domain Q, and both future-wave
checkers prove that every admissible pulse word is then transmitted exactly.

| | ε = 1e-4 (published, v3.3) | ε = 1e-3 (this folder, v3.3 + C7) |
|---|---|---|
| Layers accepted | 18 / 18 | 18 / 18 |
| Network emissions during training¹ | 21 302 | 21 302 |
| Active cells at exact rest; auxiliary ports at exact rest; gain caps | 191; 540; 4 | 191; 540; 4 |
| Future regime from Q | 191 cells fire once per pulse; at rest before 12.791 | same; at rest before 12.791 |
| Smallest future margin | 0.0491 | 0.0489 |
| Additions to the proof | — | lemmas C7, C6 and remark P ([`LEMMAS_C7_C6_EN.txt`](LEMMAS_C7_C6_EN.txt)), machine-checked in Lean ([`PeakBounds.lean`](../../proof/lean/PeakBounds.lean)) |

¹ Output spikes of all 216 cells together while the source emits its 128 training pulses.

The v3.3 program alone stops at layer 18, cell (18, 6), at this ε ([`../README.md`](../README.md)).

## Verify everything with one command

[`verify_release.py`](verify_release.py) checks, from the repository and the downloaded release
assets: the asset hashes, the engine identity (the campaign `kernel_id` recomputed from the as-run
engine), every output record against the manifest, the chain of receipts and payloads, the
engine-independent terminal extraction, and both future-wave certificates.

```sh
python3 -I sweep/v33_c7/verify_release.py <folder with the v4.4 release assets>
```

The `kernel_id` step needs Python 3.12 with numpy 2.3.5 and scipy 1.17.0 (it imports the engine);
with another Python it is reported as skipped and the other steps still run. The extraction and the
two future checkers take about six minutes in total.

## Release assets (v4.4)

Download from [Release v4.4](https://github.com/HevisNico/a22-interval-replay/releases/tag/v4.4):

| Asset | Content |
|---|---|
| `A22_v33c7_1em3_layers_01-06_part1of5.zip` … `layers_16-18_part5of5.zip` | the complete campaign outputs (3.6 GB unzipped): every receipt and result of the 216 cells, layer completion and verification records |
| `A22_v33c7_engine_as_run.zip` | the program exactly as run, with its native binaries; it reproduces the campaign `kernel_id`. Its tests and validation note predate the 16 targeted tests, which are in the fresh-launch zip; tests are not part of the program identity |

Unzipped together, the five output archives give one folder `A22_v33c7_1em3/`.

## The program

[`A22_fresh_launch_v3_3_C7.zip`](A22_fresh_launch_v3_3_C7.zip) is the v3.3 program with ε as a
parameter, plus three changes in `affine/engine.py`
([`ENGINE_CHANGES_FROM_V33.diff`](ENGINE_CHANGES_FROM_V33.diff)) and the module
`affine/cluster_memory_cover.py`:

- **C7.** When the READY peak-time logarithm has no certified positive argument, the charge is
  bounded with the kernel's own `peak_upper` (monotone in initial charge and current) instead of
  refusing. This is what unblocks cell (18, 6).
- **C6.** Second resort inside exterior clusters: the pulse-memory charge is bounded piece by piece.
- **P.** The strictly positive slope required on a root bracket [l, h] may be established on 8 or
  32 pieces of [l, h]. The acceptance predicate is unchanged, so section 6 of the coverage theorem
  applies as written. At (18, 6) the fire root lies anywhere in about [0.13, 0.34] over the box; the
  slope is positive on every piece but not provably so in one evaluation over [0, 0.64].

`tests/test_c7_c6_p.py` (16 tests) covers the three paths: threshold proximity, near-zero slope,
partition boundaries, and refusal whenever the bound is insufficient. The package passes 94 tests;
see `VALIDATION_EN.txt` inside the zip.

How these were found: v3.3 refused (18, 6) on the peak logarithm; v3.3 + C1 (a narrower first
auxiliary delay) refused at the same place; v3.3 + C7 refused there on a root bracket; a single-cell
replay with the bracket tests logged showed a correct guess, no tangency, and a slope bound lost in a
single wide evaluation. C1 was then dropped.

## Records in this folder

| Path | Content |
|---|---|
| `campaign/campaign.json` | identity: `kernel_id` d8fedb8d…, run 556d92bf…, ε = 0.001 |
| `campaign/layer_NN/complete.json`, `verification.json` | completion and independent re-read of each layer |
| `campaign/RUN_MANIFEST.json` | SHA-256 and size of all 469 JSON records of the output |
| `campaign/RUN_LOG.txt` | console log (1 h 15 min with 4 workers; (18, 4) and (18, 8) took about 29 min each) |
| `audit_campaign_dir.py` | engine-independent extraction of the 216 terminal states, same checks as `proof/provenance_audit/audit_all_layers.py` |
| `terminal/all_layers_audit.json`, `terminal/all_terminal_exact.json` | its outputs |
| `terminal/future_certificate_eps1e-3.json`, `terminal/independent_check_eps1e-3.json` | both future-wave checkers at ε = 1e-3: PASS |
| `COVERAGE_THEOREM_GENERAL_EPS_EN.txt` | the steps of the learning-coverage theorem that use ε, and what replaces them at 1e-3 |
| `certify_initial_section_eps.py`, `terminal/initial_section_eps1e-3.json` | the initial-section inequalities for any ε (byte-identical output to the published certificate at 1e-4): PASS at 1e-3 |
| `audit_commutations.py`, `terminal/commutation_usage_eps1e-3.json` | the 206 recorded commutations: 202 involve an input arrival, which Section 8(vi) of the theorem does not cover; lemma E of the addendum does |
| `FUTURE_INVARIANCE_GENERAL_EPS_EN.txt` | the two changes that state the future-invariance proof for general ε, and the certified values |
| `LEMMAS_C7_C6_EN.txt` | lemmas C7, C6 and remark P, placed in the coverage theorem |
| `verify_release.py`, `RELEASE_ASSETS_SHA256.json` | the one-command check and the asset hashes it uses |

## Not yet done

- The mathematical content of C7, C6 and remark P is machine-checked
  ([`proof/lean/PeakBounds.lean`](../../proof/lean/PeakBounds.lean)); that the program's interval
  evaluations meet their hypotheses has not been reviewed, like the rest of the proof.
- No run at ε = 3e-3 or 1e-2 with this program.
