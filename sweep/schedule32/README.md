# A 32-pulse training schedule, certified at ε = 1e-3

**Result.** On the box of v4.4 (relative half-width ε = 1e-3 on the physical constants, initial
states ±1e-5), training with **32 source pulses** instead of 128 (lane 0, times 0, 8, …, 248) is
enclosed through all 18 layers. At T = 1116 the network is in a quiescent domain Q32 from which both
future-wave checkers prove that every admissible pulse word is transmitted exactly.

| | 128 pulses (v4.4, `sweep/v33_c7/`) | 32 pulses (this folder) |
|---|---|---|
| Layers accepted | 18 / 18 | 18 / 18 |
| Active cells; silent cells | 191; 25 | 191; 25 |
| Network emissions during training | 21 302 | 2 966 |
| Fire/event commutations (all covered by lemma E) | 206 | 14 |
| Future regime from Q (two independent checkers) | at rest before 12.791; smallest margin 0.0489 | the same |
| Terminal horizon | 1116 | 1116 |

The program is the v3.3 + C7 package of v4.4 with one change, in `run.py`: the source emits 32
pulses instead of 128, and the schedule is bound into the campaign identity
([`calendar32.patch`](calendar32.patch)); [`test_calendar32.py`](test_calendar32.py) checks the dates,
the shared source clock and the horizon. Physics kernel, learning rule, guards and macros are
unchanged.

## How the proof carries over

The coverage theorem, its general-ε addendum and lemmas C7, C6, P and E do not depend on the number
of source pulses: their arguments are local to the events present, the source spacing is still 8,
and after the last pulse the queue is still run to the terminal event at 1116. The argument is
written out in [`CALENDAR_COVERAGE_BRIDGE.md`](CALENDAR_COVERAGE_BRIDGE.md); like the rest of the
proof it is manual and not yet independently reviewed. The initial section at ε = 1e-3 is the one of
v4.4 (`terminal/initial_section_eps1e-3.json` is byte-identical to `sweep/v33_c7/terminal/`).

**Erratum v4.6.1.** The campaign was rerun with the corrected lemma-E widening (exact negation; see
[`erratum_v4.6.1/`](../../erratum_v4.6.1/README.md)). Terminal bounds, the 14 commutations and both future
certificates are identical; the records below are those of the rerun.

## What it does not say

- **Not the same learned state.** The terminal box is not contained in the published Q128 domain:
  11 of 2 160 componentwise bounds exceed it (gains and b; `terminal/original_Q128_comparison.json`).
  The future theorem holds for Q32, built from this campaign's own terminal enclosures by the same
  definition. A failed box inclusion is not a physical counterexample to membership in Q128.
- **Not a shorter horizon.** Training ends at 248 but the terminal check stays at 1116; entry into
  Q32 earlier than 1116 is not claimed.
- **Not a minimum.** 32 is the schedule selected by an earlier point-simulation search; fewer pulses
  are not excluded.

## Checks

| Check | How |
|---|---|
| Future-wave certificate and independent check regenerated and compared | CI, `tools/check_certificates.py` |
| Patched engine: the C7 tests and `test_calendar32.py` (99 tests) | CI, engine job `v4.5-calendar32` |
| Terminal extraction from the outputs (byte-identical to `terminal/`) | `python3 -I sweep/v33_c7/audit_campaign_dir.py <outputs>/campaign32_eps1e-3_fixE <dir>` |
| Commutation kinds (14, all covered by lemma E) | `python3 -I sweep/v33_c7/audit_commutations.py <outputs>/campaign32_eps1e-3_fixE <file>` |
| Every output file against the manifest | `campaign/RUN_MANIFEST.json` (SHA-256 and size of all 487 files) |

The extraction, the commutation audit and both future checkers were rerun from the raw outputs with
the tools of this repository; all matched the delivered results. These reruns read the recorded
outputs; they do not replay the dynamics.

## Release assets

The complete delivery of the corrected rerun (campaign outputs in
`A22_rerun32_fixE_results/campaign32_eps1e-3_fixE/`, engine hashes, logs including the regression test
and the run console) is `A22_schedule32_fixE_run.zip` of Release `v4.6.1`; its hash is in
[`RELEASE_ASSETS_SHA256.json`](RELEASE_ASSETS_SHA256.json). The three archives of Release `v4.5` hold the
original run.

## Records in this folder

| Path | Content |
|---|---|
| `campaign/campaign.json` | identity: `kernel_id` 03f33af9…, run 3fb88908…, ε = 0.001, the 32-pulse schedule (corrected rerun) |
| `campaign/layer_NN/` | completion and independent re-read of each layer, per-cell rows |
| `campaign/RUN_MANIFEST.json` | SHA-256 and size of every output file |
| `campaign/RUN_LOG.txt` | console log of the rerun |
| `terminal/` | terminal extraction, commutations, Q128 comparison, future certificate and independent check, lineage and clock audit |
| `protocol.json`, `RESULT.json` | specification and summary of the campaign |
