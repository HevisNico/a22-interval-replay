# Results and their status

One line per result. **Proved** means a manual proof under the execution assumptions A1–A4 (stated in
[`proof/README_EN.txt`](proof/README_EN.txt)), not yet independently reviewed. **Machine-checked**
means formalized in Lean 4 with Mathlib, without `sorry`. **Computed** means a reproducible certified computation whose coverage argument is not complete.

| Result | Scope and hypotheses | Status | Authoritative document | Check |
|---|---|---|---|---|
| Strict-root lemma, abstract core (open image, brackets, Newton steps, refinement, strict event order) | exact real arithmetic; the code's enclosure and freshness properties are hypotheses | machine-checked | [`proof/lean/StrictRoot.lean`](proof/lean/StrictRoot.lean) | `.github/workflows/lean.yml`, or paste into live.lean-lang.org |
| Lemmas C7, C6 and remark P (v4.4): monotone peak bound, where the charge peaks, piecewise cover, slope on a partition | exact real arithmetic; the program's interval evaluations are hypotheses | machine-checked | [`proof/lean/PeakBounds.lean`](proof/lean/PeakBounds.lean) | `.github/workflows/lean.yml` |
| Initial section [0, U0] | initial box δ = 1e-5, ε = 1e-4 | proved | `proof/final_entry_audit/` | `python3 proof/final_entry_audit/certify_initial_section.py out.json` |
| Training enclosed, 18 layers, end in Q | ε = 1e-4, δ = 1e-5, per-port constants, program v3.3 | proved | [`proof/learning_justification/output/LEARNING_COVERAGE_THEOREM_EN.txt`](proof/learning_justification/output/LEARNING_COVERAGE_THEOREM_EN.txt) | `verify_build_identity.py`, `verify_source_witnesses.py` (Release `v3.3-proof`, see README "Reproduce") |
| Q → Q for every future pulse (gaps ≥ 20) | from Q at ε = 1e-4 | proved | [`proof/FUTURE_INVARIANCE_PROOF_EN.txt`](proof/FUTURE_INVARIANCE_PROOF_EN.txt) | `proof/provenance_audit/certify_future.py`, `verify_future_certificate.py` |
| Exact transmission of every pulse word, 18 layers | from Q | proved | [`proof/GLOBAL_THEOREM_AND_WORD_PRESERVATION_EN.txt`](proof/GLOBAL_THEOREM_AND_WORD_PRESERVATION_EN.txt)¹ | follows from the two rows above |
| Arbitrary depth, one limiting duration per layer | six prescribed preparations; training certified to 68 layers (128 in one case), then tail theorems | proved | [`depth/README.md`](depth/README.md) | `python3 -I tools/verify_depth_assets.py <assets>` |
| Deterministic speed in random media | stationary ergodic media entering the tail contract | proved | [`depth/ergodic/README_EN.md`](depth/ergodic/README_EN.md) | `cd depth/ergodic && python3 verify.py && python3 verify_integer.py` |
| Every preparation enters the deep regime | original source, whole box | **open** | [`depth/point4/README.md`](depth/point4/README.md) | partial results only |
| Future invariance on the relative domain G_rel | regenerated states satisfying G_rel; does not show that training reaches G_rel | proved (conditional) | [`depth/g_rel/THEOREM_EN.md`](depth/g_rel/THEOREM_EN.md) | `cd depth/g_rel && python3 verify_manifest.py && python3 audit.py` |
| Box-width sweep, program v3.3 | ε = 3e-4: 18 layers; 1e-3: 17; 3e-3: 7; 1e-2: 4 | computed | [`sweep/README.md`](sweep/README.md) | `sweep/*/SETUP_AND_REPLAY_EN.txt` |
| Whole chain at ε = 1e-3 (training, end in Q, every future word) | ε = 1e-3, δ = 1e-5, program v3.3 + C7 | proved, by extension: lemmas C7, C6 and remark P added to the coverage theorem; their mathematical content machine-checked ([`proof/lean/PeakBounds.lean`](proof/lean/PeakBounds.lean)) | [`sweep/v33_c7/README.md`](sweep/v33_c7/README.md) | `python3 -I sweep/v33_c7/verify_release.py <v4.4 assets>` |
| Whole chain at ε = 1e-3, scenario engine v2.3.1 | 18 layers, end in Q, future checkers pass; coverage needs lemmas B1, B2, C1–C8 | computed | [`sweep/v23/README.md`](sweep/v23/README.md) | `sweep/v23/eps_1em3/future/README.md` |

¹ This file and `proof/TRAINING_ENTRY_REVIEW_EN.txt` predate the learning-coverage theorem and still
describe the training-entry premise as open. They are kept byte-identical because their hashes are
cited; the premise is discharged by the coverage theorem (`proof/STATUS.json`). The same holds for
`proof/historical_status/` and for the status banner of `engine/reference/full_model_reference.md`.
