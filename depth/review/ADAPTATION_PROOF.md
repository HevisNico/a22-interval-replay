# A22 prescribed nominal prefixes: source specialization and proof obligations

This document accompanies the new computation. Its level is a manual source
argument under the original A1–A4, not a formal certificate or an independent
review. Upstream commit: `94f499c85bbc784c08c0d8bdb5e616360dc34863`.
No progress from the lost thread is imported.

## Exact physical family being computed

All physical constants take their nominal mathematical values, including
irrational logarithms computed with directed enclosures. Each port is fixed
to its own prescribed nominal value; this is a permitted point in the v3.3
independent-port family, not a shared uncertain parameter imposed on a family.
Initial q=r, auxiliaries READY at RM, b=.08, E in [50,100]. Each initial z is
ln(g_nom)+eta, where eta is exactly 0 or +/-1e-5 according to the declared case,
layer and lane. These are realizations inside the original initial family.

`adapter.py` installs this specialization after the unchanged affine engine
and per-port current wrappers have been installed. It calls settings(0,0),
which produces the nominal physical constants and retains the original
resource/separation checks. The `INIT` fields are exact prescribed offsets.
The first and subsequent auxiliary delays both start at exact RM and use the
same nominal equation. Each port's delay is computed independently. The
nominal identity M=(1-RM)/h(.02) makes the true delay exactly .02, but the
engine still uses its directed root enclosure, not a point substitution.
LM, LS, LE durations are likewise evaluated by the existing arithmetic.
Per-port current wrappers and their finally-restored contexts remain active.

## Initialization at zero

There is no terminal ERROR in these prescribed initial states, so the initial
slab endpoint is U0=0. The effective initial q expression is exactly r and the
initial b is exactly .08. The raw source pulse at zero is processed as raw_on
at zero, not discarded as an earlier pulse. Every auxiliary cycle is retained.
Starting at zero supplies the initial relational invariant I1–I5 directly;
the old uncertain-initial-state slab reduction is unnecessary. READY flow at
zero duration changes no physical charge. No positive-time propagation is
introduced by this specialization.

## Unchanged event transfer operations

The adapter does not replace any guard, event ordering, root acceptance,
commutation, history join, threshold reset, native arithmetic, lattice rule,
or interval budget. Equal marginal boxes do not identify physical phase
origins: `dep.shift` still allocates fresh nonpoint time atoms; copies and
exact translations preserve identities as in v3.3. Every complete incoming
train is loaded from three authenticated parent results; every pulse's six
exterior actions are generated. Optional-emission forests still cause refusal
under the single-train interface. There is no point-event tolerance.

The effective unit text differs only at its three end-time references:
the end event, its token assertion, and silent-auxiliary decay. They use
4096 instead of 1116. This is a later observation time, not a source pulse.
The unchanged code refuses if any exterior event lies after the end event
or if the end state is not READY with no raw inputs or auxiliary currents.
The new runner checks the actual terminal Time equals 4096. Thus the
observation endpoint is checked rather than inferred from point diagnostics.

## Composition in depth and persistence

The local cell theorem is indexed by its input histories; its event maps do
not depend on the index being at most 18. Its feedforward induction extends
to each finite prefix of the same 12-lane graph, provided every cell completes
under the same transfer contracts. The new controller does not extrapolate
outputs: it computes every layer from time zero with all inherited pulses.
Producer namespaces include run, layer and lane; each cell runs in a fresh
spawned process. All output dependencies, terminal ledgers and states are
encoded in the original typed DAG format. Re-reading checks five views;
a fresh process checks all twelve cells, parent receipts, and retained time
atom definitions before the next layer starts. Frozen code, native binary,
model and environment identities bind the new campaign; it has a different
identity from the original 18-layer campaign.

This argument uses the general local soundness reasoning in the manual
learning theorem. That theorem's empirical specialization to 202 mark_off
commutations does not automatically cover new commutation patterns. Every
successful new pattern must therefore be audited in the new outputs. Likewise
successful no-fire-cover or grouped-recovery fallbacks, unused in the original
campaign, need their own source-level argument before final proof closure.
Software layer completion alone is not advertised as resolving these points.

## Future boundary and tail composition

`contracts.py` uses the independent 70-digit finite-series arithmetic supplied
in the theory ZIP. For each cell it derives first head brackets from terminal
gain boxes and parent latency boxes, with strict signs and monotonicity of h
on [0,1]. It checks firing precedes influential ERROR currents and raw ends;
influential ERROR currents end during protection; all raw currents end before
reopening; local main and auxiliary regeneration occurs before the next wave.
The shortest protection is bounded using b<=1.1; the longest using the stored
positive lower b. Masked gains may increase to their physical cap without
affecting the head. These are local regeneration inequalities at source gaps
>=20, not a global settling bound. Fixed influential gains, exact resting q,
and layer induction give the exact mathematical equality t[j,p]=s[p]+d[j]
for every allowed future word, with first source at or after 4096.

At a candidate boundary, every complete output train must have exactly 54
emissions. Ordered disjoint slabs match all 54 cohorts, including the first.
All cohort diameters and all 53 successive same-lane gaps are checked by
outward bounds, with no trimming or replacement. The future latency diameter
and the training-to-first-future separation must satisfy the same contract.
Then the conditional homogeneous or connected-interface theorem in the ZIP
applies to fresh prescribed downstream cells. Until those checks pass and
new branch-pattern obligations are discharged, tail entry remains open.

## Interpretation of outcomes

A refusal means no certificate was produced by this abstraction. It is not
a physical counterexample. A completed software layer records validated
enclosures conditional on the retained arithmetic/execution contracts and
the manual local-coverage argument. Expert review and proof-assistant
verification are not represented as obtained. A final result must list any
new paths not covered by the old campaign specialization explicitly.
