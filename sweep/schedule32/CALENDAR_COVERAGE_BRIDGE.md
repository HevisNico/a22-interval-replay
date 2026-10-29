# Connecting the 32-pulse schedule to the C7 enclosure engine

Project: **Training schedule search with a bounded meta-selection step**.
This campaign checks an already selected schedule. It performs no new
selection, rewriting, or search during certification.

## Exact target

The physical model, 216 cells, 18 layers, fixed independent per-port parameters,
and initial-state family are those of the main repository at commit
`d413423d65d45fc98c6f67f1e63af43ca983edc0`.
The relative physical parameter half-width is `1e-3` (±0.1%); initial
perturbations remain `1e-5`. The source is lane 0, at times `8k` for
`0 <= k < 32`, followed by no further source input through `T = 1116`.
The last source emission is at 248. This changes the pulse count, not the
terminal horizon.

## Program changes

The received C7 ZIP was authenticated by Git blob ID
`9f44aa482502a376b5a78b4d4bd62d2ec4392da5`. Its sources remain in `upstream/`.
In `engine32/`, the only modified original executable file is `run.py`:
the source emits 32 pulses instead of 128, and the schedule specification is
included in the parameters bound into the campaign identity. The exact diff
is `calendar32.patch`. Two additional tests check the dates, shared symbolic
source clock, and retained terminal horizon.

The physical kernel, learning histories, acceptance guards, and macros are
unchanged. The `128` in the historical `campagne_A22.py` source validator and
its legacy launcher is not used on the path
`run.py -> compute_cell -> unit`. The `limit=128` in `unique_histories`
limits histories rather than pulses and remains unchanged. Refusals and
resource limits remain certification failures, never permission to truncate
an unfinished physical trajectory.

## Proposed coverage transfer — independent review required

The manual `LEARNING_COVERAGE_THEOREM_EN.txt`, its general-epsilon addendum,
and lemmas C7/C6/P are retained in `review/`, together with the verification
sources. Their published target remains the original 128-pulse campaign;
they are not by themselves an already established certificate for this run.
The proposed transfer is as follows.

1. The initial construction is unchanged: the same source pulse is present
   at time zero, with the same uncertainties and no hidden past pulses.
   The fifteen initial-section inequalities are recomputed at `eps=1e-3`.
2. The number 128 occurs in the declared source and original campaign counts,
   rather than the local arguments preserving a physical witness. The new
   source is an exact prefix retaining spacing 8. First-threshold, auxiliary
   cycle separation, affine transport, and history arguments apply to the
   events actually present. No conclusion about the terminal state is
   inherited from the old run: the trajectory enclosure is recomputed.
3. After the last pulse, the queue and all internal consequences continue
   to the same terminal event at 1116. The absence of further inputs permits
   neither history deletion nor state reinitialization nor an unchecked time
   jump. Successful completion of `unit` requires queue consumption and
   terminal checks.
4. The local induction of Sections 4–9 applies to this finite queue; the
   feedforward induction of Section 10 applies to the same 216 cells.
   Parent witnesses are not resampled between children: common time and
   parameter definitions are loaded from authenticated parent results.
5. The actually used macro kinds and counts must be read from `terminal32/`.
   Commutations involving arrivals use Lemma E of the general-epsilon
   addendum, rather than only the initial text's `mark_off` specialization.
   The passive audit checks lineage and global equality of retained time-atom
   definitions; it does not replace the local physical soundness argument.

Under the same trust assumptions A1–A4 as the manual theorem, and subject to
validation of this transfer, complete authenticated execution gives
`Reach_32(1116) ⊆ S32`, where S32 is the extracted terminal enclosure.
This implication alone establishes neither `S32 ⊆ Q128` nor invariance of S32.

## Two distinct terminal-domain connections

`compare_original_Q.py` tests a sufficient componentwise enclosure inclusion
in the published Q128 domain for the same C7 box at ±0.1%. It retains that
domain's individual b and gain bounds, including masked-port gain lower
bounds. Failure of this sufficient box test does not establish physical
non-membership in Q128. The recorded comparison reports 11 failed bounds
out of 2,160 checks.

Independently, both unchanged upstream future-invariance checkers pass on
S32. They supply constants for Q32 constructed using the same domain
definition: READY modes, exact rest charges or certified silent intervals,
E in [50,100], b extended from its terminal lower bound to 1.1, influential
and silent gains in their terminal intervals, and masked gains extended to
their physical caps. The future theorem with its general-epsilon addendum
is still required. Q32 must not be called the numerical domain Q128.

The recorded audits cover 216 cells and 18 verified layers, 10,896 distinct
retained time atoms with no conflicting definitions, and 14 fire/exterior
commutations: 10 raw_on/mark_on/mark_off groups and four two-order groups
(two raw_off and two error_on). No no-fire-cover or recovery-group fallback
was recorded. Exact logs and certificates are retained in `terminal32/`.

All failed inclusion checks are preserved. Upstream Lean results remain
partial: neither full Lean verification of this new campaign nor independent
expert endorsement is claimed.
