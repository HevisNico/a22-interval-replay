# Changelog

Each version is a GitHub release with the same tag. The main result and how to check it are in the
[README](README.md); this file keeps the history of what each version added.

## v3.2 → v3.3: one symbol per port

The **v3.2** campaign (kept in [`history/v3.2/`](history/v3.2/)) completed, but it gave the auxiliary
constants of a cell (LM, LS, LE, M, C) **one** symbol shared by its three ports. An exact counterexample
showed that the model makes them independent per port; v3.2 therefore covered only a
sub-family. A first correction replaced the shared symbols by plain interval boxes. That is sound, but
it forgets that a port keeps the same constant at every pulse: enclosures grew 3–10× and the campaign
stopped at layer 18 ([`history/plain_box_package/`](history/plain_box_package/)). **v3.3** gives each
port its own symbol, used only for that port's quantities. It is the campaign reported and proved here.

The 18-layer result of v3.3 (release `v3.3-proof`) is the one stated at the top of the README.

## v4.0-depth: arbitrary depth (six prescribed preparations)

The 18-layer result of v3.3 extends to **arbitrary depth** ([`depth/README.md`](depth/README.md)). For
six prescribed realizations, the complete training transient is certified through 68 layers (128 for a
connected two-region case). The learned state enters a tail contract that manual theorems carry through
every deeper layer. As a result:

- **one limiting duration per layer, common to all lanes** of a medium;
- **independence from the preparation**: two different upstream preparations followed by the same medium
  reach exactly the same limiting duration (u₀ = 0.666573250880782846…), and keep only a bounded phase offset;
- **the speed belongs to the medium**: homogeneous media with gains shifted by ±1e-5 have the distinct
  durations u₊ < u₀ < u₋;
- **exact transmission of every admissible future pulse word, at any depth**.

## v4.1: speed as a property of the medium

Details in [`depth/README.md`](depth/README.md#new-in-v41-speed-as-a-statistical-property-of-the-medium-and-speed-ceilings).

- **the real parameter box in the tail**: the tail theorem holds with every perturbed constant chosen
  independently per port, cell and layer, and also for fresh cells anywhere in the complete initial box;
- **a deterministic speed for random media**: for any stationary ergodic law of the medium (for example
  i.i.d. layers), almost every realization has the same limiting speed 1/γ(P), common to all lanes and to
  every preparation that enters the contract (Kingman's subadditive ergodic theorem). The speed is a
  property of the medium's statistical class;
- **speed ceilings**: no admitted cohort in the tail travels faster than 1.500248 layers per time unit
  (1.500548 for the complete-initial-box variant). During learning, without any entry assumption, the
  front of first activation travels at most 18.23 layers per time unit.

## v4.2: the open entry problem, and the box-width sweep

**Entry of every preparation** ([`depth/point4/README.md`](depth/point4/README.md)): whether *every*
preparation of the original source enters the tail is still **open**, and is now posed precisely. Proved so far: a wider
tail contract (D = 0.195), the pruning mechanism that stops learning in depth, a conditional bridge to
the tail, and the fate of the leading precursor at layer 18. There are also certified obstructions
showing what any complete proof must overcome.

**How wide can the box be?** ([`sweep/README.md`](sweep/README.md)). Fresh campaigns with wider
parameter boxes cover all 18 layers at ±3e-4 (three times the v3.3 box) and 17 layers at ±1e-3,
then stop earlier (7 layers at ±3e-3, 4 at ±1e-2). The enclosures stay roughly proportional to the box
width; what fails first is the certification of an event order. These campaigns are research runs; the
manual proof covers ±1e-4 only.

## Proof level of the depth results

The proof level is the same as for v3.3: a manual proof under A1–A4, with directed-rounding computations,
not yet independently reviewed. Entry into the tail contract is certified for six prescribed
preparations, not for the whole uncertainty box.
To check the release assets, run `python3 -I tools/verify_depth_assets.py <assets folder>`.

## v4.3: future invariance on a common relative gain domain

The physical kernel is unchanged. The new [G_rel dossier](depth/g_rel/README.md)
provides a conditional manual theorem for regenerated learned states: one firing
per source pulse in the 191-cell mask and exact preservation of all future source
intervals for gaps at least 20. The head formula includes the finite raw-current
tail; local relative guards preserve influential gains while allowing masked
gains and recovery to evolve. Directed checks accept 35/40 declared decimal
states; the generator and read-only reader share arithmetic. Training entry,
large-basin attraction and arbitrary-depth certification are not established.

## Exploratory addition: joint parameter uncertainty and link noise

The completed [six-seed pilot](exploratory/joint_uncertainty_noise_130/README.md)
combines independent per-cell/per-port auxiliary parameters and gain caps at
relative ±1e-4 with link amplitude noise (log σ = 0.05) and jitter (SD 0.015).
Four paired regimes give 24 acquisitions and 48 frozen-state baseline/decoy tests
at 130 layers. All six uncertain/noisy baseline words are complete; with 24 lateral
decoys, three of six remain perfect. Every scheduled outcome is retained and no
simulator failure is recorded. This is exploratory sampling, with no initial-state
uncertainty, parameter-box coverage, gate-superiority or lifecycle-energy claim.
The exact completed package is attached to Release `exploratory-data-1`.
