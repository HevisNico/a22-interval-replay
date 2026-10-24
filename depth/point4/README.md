# Entry for every preparation: results and the open problem (v4.2)

The depth results ([`../README.md`](../README.md)) certify entry into the tail contract for six
prescribed preparations. The question here is whether **every** admissible preparation of the
**original A22 source** enters it. The source sends 128 pulses at times 8k on lane 0 only; initial
states vary by ±1e-5 and physical constants by ±1e-4, independently per port and per cell.

**Status: open.** This folder holds the proved partial results, the certified obstructions, and a
precise statement of what is missing. Everything here is a manual proof with directed-rounding
lemmas, not yet independently reviewed. No new campaign was run for these results, and no production
file was modified.

## 1. The target

The tail contract, widened in this release, asks for:
- the complete input history, as complete cohorts on all 12 lanes;
- a diameter **≤ 0.195** at the boundaries of 5-layer blocks;
- same-lane gaps ≥ 15.5;
- a first arrival ≥ 20.

(see [`TAIL_REFINEMENT_EN.md`](TAIL_REFINEMENT_EN.md), a byte-identical copy of the document in the
nested "modes and tail budget" package). This contains the earlier 0.11 contract, so all
published compositions remain valid. The bound D = 0.195 was recomputed independently: five-layer
factor 0.9957265788, closure slack 7.834e-7; blocks of 4 or 6 layers fail.

## 2. What is proved

**The pruning mechanism.**
- *Local pruning lemma, full box* (`extinction_progress`). Each port of a fresh cell receives pulses
  8 apart. The second pulse is blocked, and the first output gap lies in [15.58557, 15.58790]. This
  interval contains the certified boundary gap 15.5864 of all six depth cases. The recovery actuator
  is tracked: b rises from 0.08 to 0.38, so a single adapted cell then relays every 8-spaced pulse.
- *Extinction through fresh cells in series.* Each fresh layer passes the safe prefix unchanged and
  removes one pulse at the first dense transition, so (p, q) → (p + 1, q − 2). For a nominal
  synchronized boundary of 128 cohorts, training stops inducing learning from layer 65 on.
- *Desynchronized local lemma* (`desynchronization`). It holds for offsets w ≤ 0.08 on the full box. The
  gain increment is clipped, which covers both orders of reopening and ERROR onset. The first gap is
  at least 16 + u₁⁻ − u₀⁺ − w (> 15.50346 at w = 0.08). Extinction is proved on a nominal tube of width 1e-4.
- *Contraction results* (`multilayer`, `modes_and_tail_budget`). Six-layer contraction < 0.88501 on the
  nominal 1e-4 tube. A nonlinear factor of 0.95 per transition for pure alternating nominal profiles
  of width ≤ 0.08, from a cover of 94 intervals with b tracked.

**The reduction** (`disorder`).
- *Conditional bridge.* Suppose every dense front stays within diameter 0.08 through the 63 pruning
  passages. Then a complete 128-cohort boundary reaches layer 64 with diameter < 0.0907 and gaps
  > 15.50346, and no learning occurs afterwards. The tail takes over from there.
- *Uniform forcing.* All independent parameters together add at most 0.0022520 to the nominal
  transition's diameter for input width ≤ 0.02, and 0.0052414 for width ≤ 0.08. This reduces the
  question to a nominal map with bounded perturbations.
- *Two directed 63-passage histories* stay at 0.0078 (b only) and 0.0111 (several parameters). These
  are two realizations, not the whole box.

**The original source at layer 18** (`precursor`, built from the certified v3.3 layer-18 enclosures).
- *The precursor dies out.* A leading partial cohort on lanes {11, 0, 1} shrinks to {0}, then to
  nothing, in two layers, uniformly over the box, with b unchanged.
- *It leaves memory.* Its ERROR phases raise some gains by exactly +0.6 in log, a factor of 1.82. For
  example, cell (19, 1) can afterwards fire on a single central parent. Its residual principal charge
  also exceeds the fresh box at t = 174. This memory is recorded explicitly, never erased.

## 3. Certified obstructions

These are proved facts, not interval artefacts:

- **Non-monotone pruning.** On a wider nominal domain, delaying one input can advance the output
  (∂S/∂X_centre ≈ −0.294, with a finite witness).
- **One-step widening.** A 12-lane profile of diameter 0.01 can produce one wider than 0.01183.
- **Disorder leaves the narrow tube.** The admissible spread of b alone creates widths above 0.000946,
  outside the 1e-4 tube.
- **Sensitivity.** The difference between two wider profiles can grow by more than 1.70 over six
  pruning layers, even though each profile narrows.
- **The layer-18 boundary is far from the bridge.** Its first complete cohort has global diameter
  **> 1.0323** and a local three-parent spread **> 0.771**, as lower bounds valid for every realization.
  The bridge cannot start there.

## 4. The open problem

> **From the layer-18 regime to the bridge regime.** Starting from the certified v3.3 layer-18 history
> (diameter ≈ 1, local spread ≈ 0.77, pre-trained cells left by the precursor), prove that every admissible
> realization reaches a boundary that satisfies the bridge hypotheses (fronts ≤ 0.08), or a generalized
> bridge for the boundary actually reached. All events, partial cohorts, gain and b changes and charge
> memory must be retained.

The quantifiers must be stated: either an entry depth that depends on the realization, or one uniform
depth. In the regime to be crossed, parents can arrive up to about 0.77 apart, after the firing; the
pruning map is not monotone; and some cells are no longer fresh. The six certified depth cases do
cross it, reaching diameter 0.104 at layer 68, so their histories show how the desynchronization
decays. An exploratory interval computation of layer 19 on the full box, not included here, stopped
at cell (19, 6), the lane opposite the source. A refusal is not a counterexample.

## 5. How to verify

Each package has its own README, a `SHA256SUMS` file and its own verifiers, all using the Python
standard library only. From inside the folder:

```
cd disorder && python3 verify_bridge.py && python3 verify_forcing.py
cd precursor && python3 inspect_boundary.py /path/to/A22_v33_layer_18.zip results && python3 verify_prefix.py
```

The precursor analysis needs the v3.3 layer-18 archive `A22_v33_layer_18.zip`
(SHA-256 `e516c4a56ef7295798203e5985e9b7606d1690976b52fc7a794149a61d727d59`, 23,908,014 bytes). It is
attached to the release `v4.2`, and its hash is the one recorded in
`proof/provenance_audit/output/all_layers_audit.json`. With this archive, the two inspection outputs and
the prefix certificate were reproduced byte for byte. The longer 63-passage verifiers
(`verify_disorder.py`, `verify_full_corner.py`) take several minutes. The nested `dependencies/` ZIP files
contain the earlier point-4 packages unchanged, each with its own verifiers.

| Folder | Content |
|---|---|
| `disorder/` | Conditional bridge, uniform forcing, 63-passage histories. Its `dependencies/` nests, in order: modes and tail budget (D = 0.195), multilayer, desynchronization, extinction progress, and the v4.1 ergodic package |
| `TAIL_REFINEMENT_EN.md` | Readable copy of the D = 0.195 tail refinement (also inside the nested package) |
| `precursor/` | Layer-18 boundary inspection, lower bounds on its diameter, precursor lemma and its memory |

## 6. How this was built

The analyses were produced with ChatGPT under the author's direction. Claude reviewed each package
and recomputed the five-layer tail bound and the key numerical claims. It reproduced the precursor
inspection byte for byte from the authenticated layer-18 archive, ran the bridge and forcing
verifiers, and wrote this summary.
