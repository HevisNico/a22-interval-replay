# Lean formalization

Two files, both without `sorry`; their `#print axioms` list only `propext`, `Classical.choice` and
`Quot.sound`.

## Strict-root core

[`StrictRoot.lean`](StrictRoot.lean) formalizes, in Lean 4 with Mathlib, the abstract mathematical
argument of Task 1 of [`REVIEW.md`](../../REVIEW.md): the strict-root lemma
(`proof/kernel_soundness/output/STRICT_ROOT_LEMMA_EN.txt`) and Sections 4–6 of
`proof/learning_justification/output/LEARNING_COVERAGE_THEOREM_EN.txt`.

| Result | Statement |
|---|---|
| `strict_of_encloses` | a sound enclosure of a set that straddles a value contains it strictly |
| `straddles_affine`, `straddles_image_strict*` | open-image lemma, two-point form: affine uses with nonzero coefficient, strictly monotone uses |
| `accepted_bracket_strict` | an accepted bracket (`f(l).hi ≤ 0`, `f(h).lo ≥ 0`) contains the root strictly |
| `newton_step_strict`, `newton_step_strict_slope` | the Newton image contains the root strictly, with freedom in `f(m)` or, when the rounded midpoint is a root, in the slope |
| `refine_strict` | every retained output of a finite refinement contains the root strictly and is not a point |
| `order_strict_after`, `order_strict_before`, `coincidence_never_passes` | a weak order test against a root date proves strict physical order; an exact coincidence passes neither test |
| `point_duration_countermodel` | without the fresh freedom, the weak test accepts a coincidence: the hypothesis is necessary |

**Scope.** Exact real arithmetic; outward rounding is a hypothesis. Every hypothesis of the form
`Encloses N (g '' S)` or `Straddles S v` is a claim about the code (fresh coordinates, no exact
shortcut in `exp`/`ln`, the slope evaluated before the guard, the fresh time atom of
`temporal.shift`). That bridge is not formalized; it is what remains of Task 1 for a reviewer.

## Lemmas C7, C6 and remark P (v4.4)

[`PeakBounds.lean`](PeakBounds.lean) proves the mathematical content of
[`sweep/v33_c7/LEMMAS_C7_C6_EN.txt`](../../sweep/v33_c7/LEMMAS_C7_C6_EN.txt), for the READY charge
`Q(u) = R + (q − R)e^{−Ku} + J(e^{−Ku} − e^{−Au})/(A − K)` with general `0 < K < A`.

| Result | Statement |
|---|---|
| `Q_mono_q`, `Q_mono_J`, `Q_le_corner` | C7, step 1: Q is monotone in the initial charge and in the current amplitude (`u ≥ 0`) |
| `c7_no_fire` | C7: a bound `B < 1` on the corner trajectory over `[0, H]` excludes a fire for every admissible device |
| `Q_le_peak` | C7, step 4: on `[0, H]`, Q is bounded by its values at 0, at H and at the stationary point clipped to `[0, H]` |
| `Q_mono_time` | C7, case `aa ≤ 0`: Q is nondecreasing in time, so its value at H bounds it on `[0, H]` |
| `c6_cover`, `bisect_cover` | C6: pieces covering `[0, H]`, each with an upper bound `< 1`, exclude a fire on `[0, H]`; bisection keeps a cover |
| `convex_comb_strict`, `hull_strict`, `remarkP_newton_strict` | remark P: a weighted average of values each strictly inside a piece enclosure is strictly inside the hull, so `newton_step_strict_slope` applies |

Same scope as above: that `peak_upper`, `dep.evaluate` and the derivative enclosures meet these
hypotheses is a claim about the code, not formalized.

## Build

Pinned to Lean `v4.35.0` and Mathlib `v4.35.0` (`lean-toolchain`, `lakefile.toml`). The GitHub
workflow `.github/workflows/lean.yml` builds both files and fails if any `#print axioms` mentions
`sorryAx`. Locally:

```sh
cd proof/lean
lake update             # resolves Mathlib v4.35.0, writes lake-manifest.json
lake exe cache get      # prebuilt Mathlib
lake build
lake env lean StrictRoot.lean   # prints the axioms
lake env lean PeakBounds.lean
```

`StrictRoot.lean` can also be pasted into <https://live.lean-lang.org> (current Mathlib), where it checks
without errors.
