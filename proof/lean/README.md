# Lean formalization of the strict-root core

[`StrictRoot.lean`](StrictRoot.lean) formalizes, in Lean 4 with Mathlib, the abstract mathematical
argument of Task 1 of [`REVIEW.md`](../../REVIEW.md): the strict-root lemma
(`proof/kernel_soundness/output/STRICT_ROOT_LEMMA_EN.txt`) and Sections 4–6 of
`proof/learning_justification/output/LEARNING_COVERAGE_THEOREM_EN.txt`. It has no `sorry`; the six
`#print axioms` at the end list only `propext`, `Classical.choice` and `Quot.sound`.

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

**Remark P (v4.4).** `newton_step_strict_slope` needs a slope enclosure open about the true mean
slope. With the slope established on a partition (`sweep/v33_c7/LEMMAS_C7_C6_EN.txt`, remark P),
the enclosure is the hull of the pieces' enclosures. If each piece encloses its derivative values
strictly (the open-image lemma applied to the derivative), every average of those values lies
strictly inside the hull, so the hypothesis holds.

## Build

Pinned to Lean `v4.35.0` and Mathlib `v4.35.0` (`lean-toolchain`, `lakefile.toml`). The GitHub
workflow `.github/workflows/lean.yml` builds the file and fails if any `#print axioms` mentions
`sorryAx`. Locally:

```sh
cd proof/lean
lake update             # resolves Mathlib v4.35.0, writes lake-manifest.json
lake exe cache get      # prebuilt Mathlib
lake build
lake env lean StrictRoot.lean   # prints the axioms
```

The file can also be pasted into <https://live.lean-lang.org> (current Mathlib), where it checks
without errors.
