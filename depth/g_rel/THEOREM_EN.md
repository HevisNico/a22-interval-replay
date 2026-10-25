# A common relative gain domain across learning-dose patterns

This is a manual theorem for the declared A22 physical kernel, under its
execution and arithmetic assumptions. Directed numerical checks establish
membership of explicit saved decimal vectors. They do not establish physical
training reachability. No independent mathematical review is claimed.

## 1. Response after a raw pulse ends

For a port whose gain is constant before the head, the canonical raw current
lasts exactly one unit. Its contribution to READY charge is g H(t-s), where

    H(u) = 0                          for u <= 0,
    H(u) = h(u)                       for 0 < u <= 1,
    H(u) = h(1) exp(-kappa (u-1))      for u >= 1.

The maximum near age 1.15 of the untruncated formula h would correspond to
an untruncated current. Each physical finite-pulse response H reaches its
maximum at age 1. A sum of several ports can still rise after the first raw
current ends and before the last one ends.

Between successive arrivals and raw endings, free READY charge has the form
r+C exp(-kappa u)-D exp(-a u), with D>=0. Its derivative has at most one zero,
a maximum when C,D>0. A first crossing can therefore be proposed piecewise.
The generator verifies both bracket signs with directed arithmetic and
excludes every earlier crossing: by monotonicity before the first raw ending,
or by a directed cover of the entire earlier interval. The read-only checker
also requires a strictly positive charge derivative on the complete head bracket.

The first head need no longer precede the first raw ending. However, every
gain contributing to the head must still be constant until that head. Passing
an influential ERROR onset without accounting for plasticity is not allowed.

## 2. Definition of G_rel(theta,beta)

Fix the active mask M of the 191 reachable cells in the 18-layer network.
The per-port physical constants theta belong to their independent relative
±1% boxes. Require 0<g_p<=C_p(theta) and 0<beta_v<=b_v<=1.1.
At the entry section, active principal cells are READY exactly at r; silent
principals are READY and subthreshold; all auxiliaries are READY exactly at rm;
reserves belong to [50,100]; no incoming, outgoing, delayed or pending current
is hidden in the state.

Define latencies recursively from the source by the first upward crossing of

    r + sum_p g_p H(t-d_parent,p) = 1.

For each cell, let a_v be its first parent arrival. Write x_p=d_parent,p-a_v
and y_v=d_v-a_v. These relative phases define the constraints; no gain centre
or learning-dose pattern is used. A driven port is influential if x_p<=y_v
and masked otherwise. A port without an active parent is silent.

Require an isolated first upward crossing, together with:

1. Every influential port satisfies x_p+Estart_p>y_v and
   x_p+Eend_p<y_v+Pmin, where Pmin=1+ln(2.5)/1.1.
2. Every driven port satisfies x_p+1<y_v+Pmin.
3. Every masked port satisfies x_p>y_v strictly. Its gain is allowed all the
   way to C_p, rather than confined near its learned entry value.
4. y_v+Pmax_v<20+min_p x_p, where Pmax_v=1+ln(2.5)/beta_v.
5. Each auxiliary cycle ends before the next arrival on its own port:
   Eend_p<20. Estart_p>1 ensures that the same gain does not change while its
   own raw current is active in the fixed-gain head formula.
6. A silent cell has no active parent. An active cell has the required
   crossing. The uniform reserve barrier holds.

Here Estart and Eend are obtained from the physical auxiliary threshold and
drain equations, not prescribed event offsets.

The numerical checker uses relative brackets for x_p and y_v and verifies
the sufficient inequalities at adverse endpoints. It recomputes latencies
from the declared gains; measured probe dates are not premises. Its small
verification brackets enclose implicitly defined phases. They are not one
uniform physical tube propagated for all gains in G.

G_rel is the nonlinear set of gain vectors satisfying these conditions,
with existence of the recursively defined latencies and relative witnesses.
The same inequalities apply across different dose patterns. G_rel is not the
Cartesian envelope of the accepted vectors. Widely different gains are admitted
when their relations with other gains and arrival offsets preserve the guards.

## 3. Invariance and temporal-fidelity theorem

For every admissible theta and every regenerated entry state with
g in G_rel(theta,beta), every canonical source word with successive gaps at
least 20 produces exactly one firing per cell of M per source pulse, and no
firings in the other cells. For every active cell,

    F_v,k = s_k + d_v.

Source intervals are therefore preserved exactly. Influential gains remain
physically constant. Masked gains and b may grow. The inequalities remain
valid and local states regenerate before their next incoming wave. The result
covers all admitted finite or infinite source words.

Proof. Induct on feedforward layers. Parents have fixed latencies. Before the
child's proposed first head, all influential ERROR phases start later and
masked inputs have not arrived. The fixed-gain formula is therefore the
physical charge equation up to that head. The first-crossing certificate
isolates its physical upward threshold crossing.

Protection after firing lasts between Pmin and Pmax even while b evolves.
Every influential ERROR is entirely protected, so the corresponding gain
does not change. Every raw input ends before the earliest possible reopening.
Thus the principal returns exactly to r and cannot fire a second time from
that wave. A masked ERROR may continue after reopening, but it changes only
a masked gain; it carries no direct principal charge current. On subsequent
waves that port is still absent before the same head. Gains stay between
their lower bounds and physical caps, and b stays between beta and 1.1.

Each auxiliary resets before the next arrival on its own port. The reserve
barrier ensures that required actuations remain powered. A single induction
over layers and source waves thus preserves the invariant: fixed influential
gains, admissible relative phases, regenerated charges before each local wave,
permitted b and masked-gain intervals, and no raw current at reopening.
Every subsequent head is the time translation of the same first upward root.

Source gaps prevent source-wave accumulation in finite time; the finite graph
and finite auxiliary cycles cannot create internal Zeno behavior. The induction
therefore applies to infinite as well as finite source words.

This does not require the whole network to be globally at rest between source
pulses at arbitrary depth: regeneration is local and permits pipelining. The
provided numerical instantiation remains at 18 layers.

## 4. Numerical scope

MEMBERSHIP.json tests 40 decimal vectors from saved simulations. Any one-ulp
excess of a saved exp(log(C)) over its cap is projected to C before testing;
gains below their caps are unchanged. An accepted witness establishes membership
of that declared vector for its own declared physical parameters, under the
regenerated-state premise. Neither the simulation's exact physical endpoint
nor the same gains at every other theta in the ±1% box are thereby certified.

The theorem quantifies over every theta and every g satisfying
G_rel(theta,beta). Point membership tests must not be converted into a gain
box independent of theta. An entry proof must retain the relations used by
these inequalities; coarse independent per-gain bounds may still be inadequate.

The reserve and auxiliary-drain assumptions are checked uniformly at ±1%.
Other kernel data are unchanged. The read-only audit checks saved phase brackets
without a head search or learning-simulator import, but shares directed arithmetic
and some evaluators with the generator. It is not independent arithmetic
validation or proof-assistant verification.
