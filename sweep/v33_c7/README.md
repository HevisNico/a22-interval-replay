# The whole chain at ε = 1e-3 with program v3.3 + C7

**Result.** At relative half-width ε = 1e-3 on the physical constants (ten times the proved box;
initial states ±1e-5), the v3.3 program extended by two short lemmas encloses the complete training
transient of all 18 layers. The end of training lies in a quiescent domain Q, and both future-wave
checkers prove that every admissible pulse word is then transmitted exactly.

| | ε = 1e-4 (published, v3.3) | ε = 1e-3 (this folder, v3.3 + C7) |
|---|---|---|
| Layers accepted | 18 / 18 | 18 / 18 |
| Training pulses, active cells at exact rest | 21 302, 191 | 21 302, 191 |
| Auxiliary ports at exact rest, gain caps | 540, 4 | 540, 4 |
| Future regime from Q | 191 cells fire once per pulse; at rest before 12.791 | same; at rest before 12.791 |
| Smallest future margin | 0.0491 | 0.0489 |
| Additions to the proof | — | lemmas C7, C6 and remark P ([`LEMMAS_C7_C6_EN.txt`](LEMMAS_C7_C6_EN.txt)) |

The v3.3 program alone stops at layer 18, cell (18, 6), at this ε ([`../README.md`](../README.md)).

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

How these were found: v3.3 refused (18, 6) on the peak logarithm; v3.3 + C1 (a narrower first
auxiliary delay) refused at the same place; v3.3 + C7 refused there on a root bracket; a single-cell
replay with the bracket tests logged showed a correct guess, no tangency, and a slope bound lost in a
single wide evaluation. C1 was then dropped.

## Records

| Path | Content |
|---|---|
| `campaign/campaign.json` | identity: `kernel_id` d8fedb8d…, run 556d92bf…, ε = 0.001 |
| `campaign/layer_NN/complete.json` | completion record of each layer (independent re-read of each layer) |
| `campaign/RUN_MANIFEST.json` | SHA-256 and size of all 469 JSON records of the 3.6 GB output (receipts and results; not in the repository) |
| `campaign/RUN_LOG.txt` | console log (1 h 15 min with 4 workers; (18, 4) and (18, 8) took about 29 min each) |
| `audit_campaign_dir.py` | engine-independent extraction of the 216 terminal states, same checks as `proof/provenance_audit/audit_all_layers.py` |
| `terminal/all_layers_audit.json`, `terminal/all_terminal_exact.json` | its outputs |
| `terminal/future_certificate_eps1e-3.json`, `terminal/independent_check_eps1e-3.json` | both future-wave checkers at ε = 1e-3: PASS |
| `FUTURE_INVARIANCE_GENERAL_EPS_EN.txt` | the two changes that state the future-invariance proof for general ε, and the certified values |
| `LEMMAS_C7_C6_EN.txt` | lemmas C7, C6 and remark P, placed in the coverage theorem |

Replay: see `README_C7_EN.txt` inside the zip.

## Not yet done

- The lemmas C7, C6 and remark P have not been reviewed, like the rest of the proof.
- The full outputs exist only in the computing environment that produced them; the manifest
  identifies them.
- No run at ε = 3e-3 or 1e-2 with this program.
