# 28 training pulses and terminal time 230, certified at ε = 1e-3

**Result.** On the box of v4.4 (relative half-width ε = 1e-3 on the physical constants, initial
states ±1e-5), training with **28 source pulses** (lane 0, times 0, 8, …, 216) is enclosed through all
18 layers, and the enclosure is cut at **T = 230** instead of 1116. At T = 230 the network is in a
quiescent domain Q28 from which both future-wave checkers prove that every admissible pulse word is
transmitted exactly.

| | 128 pulses (v4.4) | 32 pulses (v4.5) | 28 pulses (this folder) |
|---|---|---|---|
| Terminal time | 1116 | 1116 | **230** |
| Layers accepted | 18 / 18 | 18 / 18 | 18 / 18 |
| Active cells; silent cells | 191; 25 | 191; 25 | 191; 25 |
| Network emissions during training | 21 302 | 2 966 | 2 202 |
| Fire/event commutations (all covered by lemma E) | 206 | 14 | 6 |
| Future regime from Q (two independent checkers) | at rest before 12.791; smallest margin 0.0489 | the same | the same (0.04895) |

The program is the v3.3 + C7 package of v4.4 with two changes ([`calendar28_T230.patch`](calendar28_T230.patch)):
in `run.py` the source emits 28 pulses and the schedule and terminal time enter the campaign identity;
in `validation_A15.py` the terminal end event is at 230 and the relaxation of silent auxiliaries is
evaluated at 230. [`test_calendar28.py`](test_calendar28.py) checks the dates, the shared source clock,
the terminal clock, the silent relaxation at the shorter horizon and the refusal of an input whose cycle
would extend past the cut. Physics kernel, learning rule, guards and macros are unchanged.

## How the proof carries over

As for v4.5, the coverage theorem, its general-ε addendum and lemmas C7, C6, P and E do not depend on
the number of source pulses. The new point is the earlier cut: nothing assumes that 14 time units after
the last pulse suffice. The terminal end event must be the last event of every cell queue, the passive
terminal audit requires every retained terminal time to be exactly 230 with no uncertain term, and
each cell must end READY with no active input; any of these failing would refuse the campaign. The
argument is written out in [`CALENDAR_COVERAGE_BRIDGE.md`](CALENDAR_COVERAGE_BRIDGE.md); like the rest of
the proof it is manual and not yet independently reviewed. The initial section at ε = 1e-3 is the one of
v4.4 (`terminal/initial_section_eps1e-3.json` is byte-identical to `sweep/v33_c7/terminal/`).

**Erratum v4.6.1.** The campaign was rerun with the corrected lemma-E widening (exact negation; the
case found was cell (18, 4) of this campaign; see [`erratum_v4.6.1/`](../../erratum_v4.6.1/README.md)).
Terminal bounds, the 6 commutations, Q28 and both future certificates are identical; the records below
are those of the rerun. The 28-pulse result now has its own repository,
[a22-28-pulses](https://github.com/HevisNico/a22-28-pulses).

## What it does not say

- **Not the same learned state.** The future theorem holds for Q28, built from this campaign's own
  terminal enclosures by the same definition (`terminal/invariant_domain_Q28.json`); Q28 is not
  identified with Q32 or Q128.
- **Not a minimum.** 28 pulses and T = 230 come from a sampled point-simulation sweep (8 to 32 pulses,
  uniform and non-uniform); fewer pulses or an earlier cut are not excluded. At 24 pulses the sampled
  terminal states fail a sufficient condition of the current future theorem (the head window), not a
  finite transmission test.

## Checks

| Check | How |
|---|---|
| Patched engine: the C7 tests and `test_calendar28.py` (101 tests) | CI, engine job `v4.6-calendar28` |
| Future-wave certificate and independent check regenerated and compared | CI, `tools/check_certificates.py` |
| Terminal extraction from the outputs (byte-identical to `terminal/`) | the extractor of `sweep/v33_c7/audit_campaign_dir.py` with 1116 replaced by 230 |
| Commutation kinds (6, all covered by lemma E) | `python3 -I sweep/v33_c7/audit_commutations.py <outputs>/campaign28_T230_eps1e-3 <file>` |
| Every output file against the manifest | `campaign/RUN_MANIFEST.json` (SHA-256 and size of all 487 files) |

The extraction, the commutation audit, the initial section and both future checkers were rerun from the
raw outputs with the tools of this repository; all matched the delivered results byte for byte (the
independent check without its certificate hash, which matches the regenerated certificate). The engine
of the delivery is exactly the C7 package plus the patch and the test. These reruns read the recorded
outputs; they do not replay the dynamics.

## Release assets

The corrected rerun is in two archives of Release `v4.6.1` (the campaign outputs
`campaign28_T230_eps1e-3/`, and the engine exactly as run with its binaries); their hashes are in
[`RELEASE_ASSETS_SHA256.json`](RELEASE_ASSETS_SHA256.json). The three archives of Release `v4.6` hold
the original run.

## Records in this folder

| Path | Content |
|---|---|
| `campaign/campaign.json` | identity: `kernel_id` b49dca10…, run 25e6fa5f…, ε = 0.001, 28 pulses, T = 230 (corrected rerun) |
| `campaign/layer_NN/` | completion and independent re-read of each layer, per-cell rows |
| `campaign/RUN_MANIFEST.json` | SHA-256 and size of every output file |
| `campaign/RUN_LOG.txt` | console log of the rerun |
| `terminal/` | terminal extraction, layer audit, commutations, future certificate and independent check, Q28, lineage and clock audit |
| `protocol.json`, `RESULT.json` | specification and summary of the campaign |
