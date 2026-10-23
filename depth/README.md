# A22 at arbitrary depth: certified learning entry and a preparation-independent limiting speed

Release `v4.0-depth`. The v3.3 result ([main README](../README.md)) covers 18 layers. This extension
goes to **arbitrary depth**.

**Result.** For six prescribed realizations, the complete training transient is certified through 68
layers (128 for the connected interface case). The learned state then enters a tail contract, and manual
theorems carry that contract through every deeper layer. Consequences:

- every lane of a medium propagates with **one common limiting duration per layer**;
- two **different upstream preparations** followed by the **same medium** reach **exactly the same
  limiting duration**, and keep only a bounded phase offset of their history;
- different media have different durations, so the speed is a **property of the medium**, not of the
  preparation;
- every admissible future pulse word is transmitted with its intervals preserved exactly, at any depth.

Proof level: as for v3.3, a manual mathematical and source-level proof under the execution
assumptions A1–A4, combined with directed-rounding computations. It has not yet been reviewed
independently.

## What was computed

Six prescribed realizations of the A22 model. Physical constants are at their nominal values. Each cell
starts in an authorized initial state with gains `ln g = ln g_nom + η`, where η depends on the case:

| Case | η in layers 1–18 | η in deeper layers |
|---|---|---|
| `nominal` | 0 | 0 |
| `plus` / `minus` | +1e-5 / −1e-5 | +1e-5 / −1e-5 |
| `plus_prefix18` / `minus_prefix18` | +1e-5 / −1e-5 | 0 |
| `interface` | +1e-5 on lanes 0–5, −1e-5 on lanes 6–11 | same |

Each case was computed with the **unchanged v3.3 interval engine** through the complete 128-pulse training,
layer after layer, every emitted pulse being fed to the next layer (68 layers; 128 for `interface`). The
engine sources are byte-identical to commit `94f499c` of this repository. The only addition is an adapter
(`ADAPTATION_PROOF.md`) that sets the uncertainty to zero, sets η, and moves the observation end time from
1116 to 4096. The new program identity is `3ecdb7bd2e618c19…`; it differs from the v3.3 campaign identity.

## What was proved

**Finite part (computed and checked).** At the boundary layer of each case, all 54 training cohorts on
all 12 lanes, all 53 successive gaps on each lane, and the future-word contract are checked with directed
arithmetic:

| Case | Boundary layer | Max cohort diameter (bound) | Min same-lane gap (bound) | Limiting duration per layer |
|---|---:|---:|---:|---|
| nominal | 68 | 0.1041972 (≤ 0.11) | 15.586447 (≥ 15.5) | u₀ = 0.666573250880782846… |
| plus_prefix18 | 68 | 0.1041940 | 15.586447 | **u₀**, same enclosure |
| minus_prefix18 | 68 | 0.1042004 | 15.586447 | **u₀**, same enclosure |
| plus | 68 | 0.1041916 | 15.586453 | u₊ = 0.666556597072781… |
| minus | 68 | 0.1042028 | 15.586441 | u₋ = 0.666589905698710… |
| interface | 128 | 0.0069639 (≤ 0.01) | 15.586705 | one duration for all lanes, in [u₊, u₋] |

For every case, the future contract holds for every source word whose first pulse is at time ≥ 1116 and
whose later gaps are ≥ 20, with a local margin above 86.6 at the first future wave. It does not require
the network to be globally at rest at 1116.

**Infinite part (manual theorems, conditional on the finite part).** Beyond the boundary, fresh cells never
change their gains or recovery, regenerate locally before each wave, and preserve the cohort diameter
and spacing (`theory/LEARNING_SPEED_SELECTION_EN.txt`, sections 4–5). Every lane therefore has the same
asymptotic duration per layer. For `interface`, a six-layer contraction (row-overlap bound β > 0.057)
forces one common duration for both half-rings, with a fixed spatial phase profile.

**Reading.**
- *Independence from the preparation.* `plus_prefix18` and `minus_prefix18` prepare layers 1–18
  differently. Followed by the same nominal medium, both reach the nominal limiting duration u₀. Their
  history survives only as a bounded phase offset.
- *The duration belongs to the medium.* The homogeneous media `plus` and `minus` have two distinct
  durations, u₊ < u₀ < u₋.
- *Coordination.* In the connected `interface` medium, the two half-rings cannot run at different
  asymptotic speeds.

## New in v4.1: speed as a statistical property of the medium, and speed ceilings

Three further results extend the tail (`ergodic/` and `cone/`). They are manual proofs with
directed-rounding lemmas, checked by two arithmetic implementations. No new campaign was run.

**1. Heterogeneous tail** (`ergodic/01_HETEROGENEOUS_TAIL_EN.md`). The tail theorem now covers
the real A22 parameter box: the perturbed constants C, M, L_m, L_s and L_e are chosen independently
at every port, cell and layer (±1e-4 relative), and gain offsets independently per port. Protection,
regeneration and a six-layer contraction (row overlap ρ₆ = 971/11664, β > 0.0092) hold with diameter
0.11 at block boundaries. A second variant admits the *complete* initial box for the fresh tail
cells, without resetting them to exact rest: initial ERROR tails, an initial charge memory bounded
and summable over depth, and a first input at t ≥ 20. All six certified boundaries satisfy that
condition: their first cohort arrives at t ≈ 209 (layer 68) or t ≈ 249 (layer 128).

**2. Deterministic speed of a random medium** (`ergodic/02_ERGODIC_SPEED_EN.md`). Suppose the layer
environments form a stationary ergodic sequence, for example i.i.d. layers; correlations inside a
layer are allowed. Then Kingman's subadditive ergodic theorem gives, for almost every realization of
the medium, **one deterministic limiting duration γ(P)**. It is shared by all lanes and by every
preparation that enters the contract. The speed 1/γ(P) is therefore a property of the *statistical
class* of the medium, not of its particular realization, nor of the preparation. Stationarity alone
does not suffice; a counterexample is included.

**3. Speed ceilings** (`cone/03_CAUSAL_CONE_EN.md`).

| Front | Ceiling, in layers per time unit | Hypothesis |
|---|---:|---|
| Every cohort in the tail (exact-rest variant) | < 1.500248 | tail contract |
| Every cohort in the tail (complete initial box, first cohort included) | < 1.500548 | tail contract, first input ≥ 20 |
| First activation, during learning | < 18.234831 | none beyond the original initial box |

In the exact-rest variant, the typical speed of every admissible tail medium lies between
1/u₊ ≈ 1.500173 and the ceiling 1/u₋ ≈ 1.500248 (up to 1.500548 in the complete-initial-box variant).
The narrowness of this window comes from the small gain box (±1e-5).

**Combined statement.** Each of the six certified preparations, followed by any stationary ergodic
random medium of the A22 box, propagates with the deterministic speed 1/γ(P), common to all lanes, and
no admitted cohort exceeds the ceiling of its tail class.

## What is not claimed

- Not the whole v3.3 uncertainty box upstream: entry into the tail contract is certified for six
  prescribed preparations only. Entry for every preparation remains open.
- Not one duration for all media. Different media, or different laws of random media, have different
  durations. A deterministic medium that varies with depth (for example long alternating blocks of
  η = ±1e-5) need not have a depth-average limit; stationary ergodic media do (v4.1).
- No information cone for arbitrary perturbations of an already active network. Outside the contract,
  a cell close to threshold can fire almost at once (`cone/03_CAUSAL_CONE_EN.md` §6).
- No numerical value of γ(P) for a particular law beyond the bounds above.
- No relativistic or Lorentz-invariance interpretation. A22 is oriented and inhomogeneous and cannot test one.
- No proof-assistant verification and no independent expert review yet.

## Assumptions, execution and incidents

- **A1–A4** as in the v3.3 proof. The campaigns ran in the execution environment of an AI assistant
  (Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0), not on the author's machine. The native module
  `_a22_native` was rebuilt there (SHA-256 `b968a17f…`, different from the v3.3 build). It was later
  reproduced byte for byte from its source. It encodes and hashes data; it does not implement the
  physics. The rounding module is identical to v3.3 (`29b1d226…`). Details: `review/REVIEW_V1_FR.md` §1.
- **Corrected boundary checker.** The frozen prototype checker had an assertion stronger than the model
  needs: it required every parent to arrive before the first raw-pulse end. The certificates use a
  supplementary checker that replaces it with explicit inequalities for a *masked late parent*
  (`review/REVIEW_V1_FR.md` §2). This argument needs independent review (see [REVIEW.md](../REVIEW.md), Task 7).
- **Counters.** 449,298 recorded firings and as many recoveries, equal to the emissions. No
  successful commutation, no-fire cover or grouped recovery was used (`review/REVIEW_FINAL_V2_FR.md` §5).
- **Corrupted local copy.** One local copy of the `plus_prefix18` certificate packet was truncated. It was
  not used. The packet was rebuilt from authenticated checkpoints as `…_v2_recovered.zip`
  (`review/DELIVERY_INTEGRITY_ADDENDUM_V1_FR.md`).
- **Six lost intermediate archives.** After the full chain had been authenticated
  (`review/RECOVERY_FINAL_V1.json`), six intermediate layer archives were lost: `minus` 67,
  `plus_prefix18` 66–67, `minus_prefix18` 65–67. Their original hashes remain recorded in
  `LAYER_INDEX.json`. They were recomputed in a separate **verification replay**, from the last
  authenticated parents and in the same environment. The replayed layer 68 reproduces the production
  `state`, `emissions` and `time_dependencies` hashes for all 36 cells (`replay_gap/`). Receipt and
  provenance hashes necessarily differ, because receipts record run times. The replayed files are never
  presented as the lost originals.

## How to verify

1. Download all assets of the release `v4.0-depth` into one folder. They are listed with their SHA-256
   in `RELEASE_ASSETS.json`.
2. From the repository root, with Python 3 and no extra package:

   ```
   python3 -I tools/verify_depth_assets.py /path/to/downloaded/assets
   ```

   It checks every asset, the 462 retained layer archives against their authenticated hashes, and the
   replay chain and its layer-68 comparison. Expected last line: `PASS`. It does not run the engine.
3. The finite inequalities themselves can be re-run from the case certificates inside
   `A22_final_reviewed_v3.zip` (`review_tools/` in each certificate, standard library only, without `-O`).
4. The v4.1 lemmas, from inside each folder (standard library only):

   ```
   cd depth/ergodic && python3 verify.py && python3 verify_integer.py
   cd depth/cone && python3 verify_cone.py
   ```

   Expected: `PASS_NUMERICAL_LEMMAS`, `PASS_INDEPENDENT_INTEGER_CRITICAL_CHECKS`,
   `PASS_DECIMAL_AND_INTEGER_CONE_CHECKS`. The verifiers rewrite their JSON result files, so run them in
   a copy if you want to keep the published bytes. Each folder's `SHA256SUMS` authenticates its files.

## Contents of this folder

| Path | What it is |
|---|---|
| `RELEASE_ASSETS.json` | Names, sizes and SHA-256 of the release assets |
| `LAYER_INDEX.json` | All 468 layer archives: authenticated hash, origin, location inside the assets |
| `certificates/` | For each case: campaign configuration and finite-to-infinite composition report |
| `theory/` | The two theory texts and the conditional tail certificate |
| `review/` | Adaptation note, review addenda, first-future and recovery records, integrity incident records |
| `replay_gap/` | Verification-replay result, comparison report, environment report |
| `ergodic/` | v4.1: heterogeneous tail and ergodic speed (proofs, verifiers, results, source snapshots) |
| `cone/` | v4.1: speed ceilings and forward cones (proof, verifier, certificate; includes the `ergodic/` package as a dependency ZIP) |

Several review documents were written in French (suffix `_FR`). The tables and JSON files are
language-neutral.

## How this was built

The campaigns, the boundary checkers, the theory dossiers and the review addenda were produced with
ChatGPT (OpenAI) under the author's direction. Claude (Anthropic) audited the packets, re-checked the
hashes, the replay chain and the layer-68 comparison with its own code, independently recomputed the
tail durations and the six-layer overlap bound, and wrote this summary and `tools/verify_depth_assets.py`.
For v4.1, the heterogeneous-tail, ergodic-speed and cone packages were produced with ChatGPT. Claude
reviewed them, independently recomputed ρ₆, β, both closure slacks, the tail roots and the global
first-activation delay, and ran the three verifiers. The author designed the questions and the preparations, and directed and validated the work.
