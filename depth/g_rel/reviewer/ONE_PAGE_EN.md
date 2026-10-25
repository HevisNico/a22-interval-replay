# A22 v4.3 - Learned memory can preserve temporal intervals exactly

**Question.** Learning can produce different gains while preserving the same transmitting network. Can we characterize those transmitting states without requiring a common learning dose or a common latency?

**Conditional result.** For the A22 network of 18 layers and 12 lanes, we define a relational set G_rel of gains and arrival phases. From a regenerated state in this set, each canonical source pulse produces exactly one firing in each of the 191 active cells and none in the others. Every future pulse word with source gaps at least 20 preserves its intervals exactly. Latencies may depend on the device and its learned history.

**What defines the set.** Each cell is described relative to its first parent arrival. Before firing, its charge is a sum of explicit pulse responses. The formula includes the tail after a raw pulse ends: H(u)=h(1) exp[-κ(u-1)] for u≥1. A first upward crossing is isolated. Influential ERROR phases begin after that crossing and finish under protection; every raw current ends before reopening; principal and auxiliary states regenerate before their next incoming wave. These are local gain-arrival constraints, rather than independent boxes around one centre.

**Mechanism.** Influential gains physically stop changing because their ERROR phases remain protected. Masked gains and the recovery actuator b may still grow without affecting the head. A joint induction over layers and waves preserves these guards. For a fixed device, each head therefore solves the same time-translated equation on every wave: F(v,k)=s(k)+d(v). Exact fidelity follows from this identity, rather than from a numerical tolerance.

**Computed evidence.** An outward-rounded generator and a separate read-only checker accept 35 of the 40 saved decimal vectors, including all ten with initial log-gain radius α=0.01. Across those ten states, 217 influential-port positions have gain ratios above 1.6; the largest ratio is about 6.16. Five states remain outside the sufficient criterion. Both programs share the same directed-arithmetic library.

**Boundary of the claim.** Membership is established for the declared vectors at their respective physical parameters, within the ±1% family. This does not certify that training reaches those states, that their Cartesian envelope works, or that the certificate extends to arbitrary depth. The proof is manual, under explicit execution and arithmetic assumptions; it is neither proof-assistant checked nor independently reviewed. Universal entry from an initial-state box remains open.

**First review question.** Do the local guards, including cases after a raw pulse ends, suffice to preserve the first crossing, influential-gain freezing and regeneration simultaneously for every future word? Read THEOREM_EN.md, then the response and first-crossing evaluators in check.py and audit.py. The 35 membership witnesses can be replayed without running the learning engine.

Prepared by ChatGPT/Codex under the model author's direction. This release does not contact or claim endorsement by any reviewer.
