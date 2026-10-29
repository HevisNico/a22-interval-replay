# Erratum v4.6.1: outward rounding of the lemma-E widening

## The defect

Lemma E (fire against an event group) widens the fire-time enclosure downward by
δ = κ·w: F ∈ [f₀ − δ, f₀]. The program computed the widened interval as

```python
rho = r0 + I(-delta, D(0)) if delta > 0 else r0
```

`delta` is a 160-digit value rounded upward, but Python's unary minus on a `Decimal` rounds to the
ambient context, 28 digits. The lower end of the widening could therefore move **inward**, so the
computed enclosure was not guaranteed to contain f₀ − δ. In the 28-pulse campaign of v4.6, cell
(18, 4), batch 89, the loss is 6.215e-30 on a widening of 0.2518.

The fix ([`commutation_fix.diff`](commutation_fix.diff)) uses `delta.copy_negate()`, which is exact:

```python
rho = r0 + I(delta.copy_negate(), D(0)) if delta > 0 else r0
```

The mathematics of lemma E (and its Lean formalization) is unchanged; only the implementation of the
interval was not outward.

## Regression test

[`test_commutation_rounding.py`](test_commutation_rounding.py), now in `tests/` of the corrected
package, reads the widening line actually present in `affine/commutation.py`, evaluates it on the
archived δ of (18, 4) and requires the lower end to be at most 0.5 − δ computed at 400 digits.

- Program as run in v4.4 to v4.6: [`regression_test_unfixed_engine.txt`](regression_test_unfixed_engine.txt), **FAIL** (exit code 1).
- Corrected program: [`regression_test_fixed_engine.txt`](regression_test_fixed_engine.txt), **OK**.

Check it yourself with the old and new packages:

```sh
unzip A22_fresh_launch_v3_3_C7.zip && cp erratum_v4.6.1/test_commutation_rounding.py A22_fresh_launch_v3_3_C7/tests/
cd A22_fresh_launch_v3_3_C7 && python3 build_all_native.py && python3 -B -m unittest -v tests.test_commutation_rounding
```

## Reruns with the corrected program

The three campaigns that use lemma E with a nonzero widening were rerun from scratch with the corrected
program (ε = 1e-3, initial states ±1e-5).

| Campaign | `kernel_id` / run before | `kernel_id` / run after | Commutations | Terminal bounds | Future certificates |
|---|---|---|---|---|---|
| [`sweep/v33_c7/`](../sweep/v33_c7/README.md), 128 pulses (v4.4) | d8fedb8d… / 556d92bf… | d59fe056… / 96f175d2… | 206 = 206 | identical | identical; at rest before 12.79068 |
| [`sweep/schedule32/`](../sweep/schedule32/README.md), 32 pulses (v4.5) | d67c8f16… / 300ca4ad… | 03f33af9… / 3fb88908… | 14 = 14 | identical | identical; at rest before 12.79068 |
| [`sweep/schedule28_T230/`](../sweep/schedule28_T230/README.md), 28 pulses, T = 230 (v4.6) | 886d1c5c… / c6e073d7… | b49dca10… / 25e6fa5f… | 6 = 6 | identical | identical; at rest before 12.79068 |

"Identical" is checked field by field: the regenerated terminal extractions, lineage audits,
commutation audits, initial sections, future certificates, independent checks and the Q28 domain differ
from the published ones only in identity fields (`kernel_id`, `run_id`, the interpreter and native
binary of the run, and the payload, state and input hashes that depend on them). Every enclosed value and
every margin is the same. The tests of the corrected packages: 97 (C7), 99 (32-pulse calendar), 101
(28-pulse calendar).

The 128- and 28-pulse campaigns were rerun with CPython 3.13; the 32-pulse campaign with CPython 3.12
on another machine. The records in the three folders and `RESULT.json` are those of the reruns, and
each `campaign/RUN_MANIFEST.json` gives the SHA-256 of every output file. The full outputs of the
28-pulse rerun are the release assets of [a22-28-pulses](https://github.com/HevisNico/a22-28-pulses). Those of the 128- and 32-pulse reruns are not
published; their archive hashes are in `RELEASE_ASSETS_SHA256.json` of each folder, and the archives are
available on request. The archives of releases v4.4, v4.5 and v4.6 remain the record of the original
runs; they do not match the records now committed.

## Not affected

- The v3.3 program in [`engine/`](../engine/) has the same line, but its published campaign (ε = 1e-4)
  recorded only zero widenings ([`proof/evidence/commutation_usage.json`](../proof/evidence/commutation_usage.json),
  `all_widenings_zero: true`), so the expression is never evaluated with δ > 0. It is kept byte-identical
  so that its `kernel_id` stays reproducible.

## Second checker: silent cells

The decimal future checkers (`proof/provenance_audit/verify_future_certificate.py` and
`sweep/v23/eps_1em3/future/verify_future_certificate_eps.py`) skipped cells without inputs. They now
check the structural premises of every cell (phases, no pending event, no raw input, E in [50, 100],
positive gains, the bound on m) and, for silent cells, no pulse and q around 0.1; they also require 216
distinct cells ([`silent_cells_checker_fix.patch`](silent_cells_checker_fix.patch)). Their output is
unchanged on the five published domains, and the patched checker rejects a corrupted silent cell.
