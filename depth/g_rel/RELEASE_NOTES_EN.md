# A22 v4.3 - Conditional future invariance on a relative gain domain

The physical kernel is unchanged. This release adds a manual conditional
theorem: from a regenerated state satisfying the local gain-arrival constraints
G_rel(theta,beta), the 191-cell active mask gives exactly one firing per future
canonical source pulse and preserves every source interval exactly, for source
gaps at least 20.

The response formula includes the finite-current tail after a raw pulse ends.
The invariant allows masked gains and the recovery actuator to remain plastic,
while influential gains physically stop changing under the protection guards.
Learned gains and latencies need not be common across states or devices.

Directed checks accept 35/40 saved decimal states, including all ten with
initial log-gain radius 0.01, across genuinely different dose patterns. A separate
reader checks the saved first-crossing and local-return witnesses. The reader
and generator share arithmetic and evaluators.

Start with `ONE_PAGE_EN.pdf`, then `THEOREM_EN.md` and the replay instructions.
This is not a certification of training at ±1%, not universal entry from a
large initial basin, and not an arbitrary-depth certificate. The five unresolved
membership cases are retained. The proof is manual, not independently reviewed
or machine-checked. Exploratory training simulations remain exploratory.

The separate layer-5 first-delay refinement is an entry-engineering experiment;
it is not a premise used to claim universal entry in this release.
