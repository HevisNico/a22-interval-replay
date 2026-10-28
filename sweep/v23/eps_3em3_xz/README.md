# ε = 3e-3: 16 layers with the scenario launcher v2.3.1 + xz storage

**Result.** At ε = 3e-3 (initial states ±1e-5), layers 1 to 16 are complete, each with the whole
prefix independently verified (`layer_16/verification.json`, `"through": 16`). **There was no
refusal and no error.** The run was stopped during layer 17 by decision of the author, because of
computing time: in that layer each job took about 4 to 7 minutes instead of 30 to 50 seconds and
returned 6 histories, so layers 17 and 18 would have needed more than a day of a 4-core cloud
session. The stop is a limit of the available computing time, not a limit found by the kernel or
the proof: nothing in the run refused an event order, a root or a bound.

These are research campaigns (`experimental_not_qualified`), like the rest of this folder.

## Engine

The scenario launcher v2.3.1 of [`../`](../README.md) with one storage change
([`../SOURCE_V231_XZ_FOR_REPLAY.zip`](../SOURCE_V231_XZ_FOR_REPLAY.zip), sha256
`260dc3b3…eebfcd631d`; see `README_XZ_STORAGE.md` and `CHANGES_XZ_STORAGE.diff` inside). Each
`result.json` is written xz-compressed; its hash is that of the uncompressed bytes, and a payload
that is not exactly one complete xz stream is refused. The physics kernel, the affine arithmetic,
the scheduler and the verification rules are unchanged. The change was needed because the
uncompressed outputs doubled from layer to layer (layer 14 alone was 7.5 GB in a first, uncompressed
run, more than the disk of a cloud session); with xz, layers 1 to 16 take 1.3 GB.

Checks of the change: the 188 tests of v2.3.1 pass, plus one new test of corrupted and extended xz
payloads; a two-layer run gives the same terminal states for all 24 cells as the uncompressed
engine; and layers 13 and 14, which an earlier uncompressed run also completed, have the same
numbers of jobs (231 and 360).

```
run_id          0c92786260c9482588c6403f7f1e1124
kernel_id       77974408551c93b53a735431add8c02d32ed13df13f2cb1c486ad05903d6955a
source_identity bc18c23f1f9468d126b593984d4523c63bbed7db061cff2f5092477bbeaca76f
environment     CPython 3.12.3, numpy 2.3.5, scipy 1.17.0, the packaged native binaries
```

## Layers

| Layer | Jobs | Seconds | Stored (MB) |
|---|---|---|---|
| 1–9 | 12, 12, 12, 12, 12, 12, 12, 12, 15 | 14 to 192 each | 21 in total |
| 10 | 17 | 679 | 12 |
| 11 | 67 | 866 | 38 |
| 12 | 133 | 1761 | 65 |
| 13 | 231 | 4087 | 136 |
| 14 | 360 | 5674 | 290 |
| 15 | 670 | 6053 | 320 |
| 16 | 850 | 4395 | 470 |
| 17 | 36 done, then stopped | — | — |

A job is one compatible triple of parent histories; the number of jobs is the number of event-order
scenarios the launcher keeps. Seconds are wall-clock times on 4 workers, so they include the
sharing of the machine with other checks during layer 13 and the resumes during layers 15 and 16. The run stopped twice with the
session's machine (17:19 UTC, the session went idle; 21:13 UTC, the machine restarted) and was
resumed at 18:02 and 21:14 UTC with the same program, binaries and
environment, which the launcher checks against `kernel_id`, and it re-verified the whole prefix
before continuing (`=== RESUME` lines in the log).

## Files

| Path | Content |
|---|---|
| `campaign.json` | campaign identity |
| `layer_16/complete.json`, `layer_16/verification.json` | completion record of layer 16 and the independent verification of layers 1–16 (hashes of every receipt and of the layer manifest) |
| `RUN_LOG.txt` | console log of the whole run, including the two resumes and the stop |

The complete outputs (every receipt and xz-compressed `result.json`, layers 1 to 16, about 1.3 GB)
are kept by the author outside the repository.
