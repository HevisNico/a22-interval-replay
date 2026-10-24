# Why A22 matters

**Who this is for:** people working on validated numerics and hybrid-system verification,
computational neuroscience (temporal coding, plasticity), and neuromorphic computing. Reviewers
from the first group are the most needed.

## The question

Take a spiking network that **learns** while it runs. Its components are not perfect: every
constant can be off by a little, independently in every cell, and so can every initial state.
Can you say what the network will do **for every one of those possible devices**, not just for
the few you happened to simulate?

A22 answers that question for one concrete network: 18 layers of 12 cells, trained by 128 pulses
with a local learning rule, for every device in a small parameter box (±1e-4 on the constants,
±1e-5 on the initial states). The same computation also covers all 18 layers with ±3e-4 on the
constants (see "Where the method stops working").

## The core result: learning reaches the same regime for every device

The hard part is the **training transient**. During it:

- the gains change, and how they change depends on spike timing, so a small timing difference
  early on can change what is learned;
- cells fire when a threshold is crossed and then close their input for a while, so **the order of
  events can differ from one device to another**, and each order leads to a different continuation;
- the uncertainty is independent in every input port of every cell: thousands of dimensions.

A22 encloses all admissible trajectories of this transient at once, with outward-rounded affine
arithmetic and a symbol per port and constant, and comes with a written proof that the enclosure
covers every event order. The conclusion: **for every device in the box, training ends inside one
explicit quiescent domain Q**, with every learned gain known to within ±2.4 % in the worst cell.

## What follows from it, and why that part is easy

Once the network is in Q, the gains are frozen and the network is back at exact rest. Each future
pulse then produces the same response, shifted in time. So the next two statements are close to
immediate, and their proofs are short compared with the training proof:

- from Q, for every future pulse sequence spaced by at least 20 time units, each active cell fires
  exactly once per pulse and the network returns to Q;
- the intervals between pulses are therefore transmitted exactly through all 18 layers.

The point is not that a frozen network transmits timing; it is that **learning, under varying event
orders, provably lands every device in a state where it does**.

The depth extensions add a result about **speed**: deep in the network, the time a pulse takes to
cross one layer converges to one value common to all lanes. This is established for six prescribed
preparations, and, for random media with stationary ergodic statistics, for every preparation that
enters the deep-layer regime. In that restricted sense the speed belongs to the medium rather than
to how the signal was prepared.

## What is already known, and what A22 adds

- **Synfire chains.** Stable propagation of synchronous volleys through layers of spiking neurons is
  a classical result (Diesmann, Gewaltig and Aertsen, *Nature*, 1999), established by simulation and
  mean-field analysis. It is also known that such chains can emerge through spike-timing-dependent
  plasticity, in simulations (for example Fiete, Senn, Wang and Hahnloser, *Neuron*, 2010). A22 is
  close in spirit to these results. What it adds is that the transmitting regime is reached by
  learning **for every device in the box, with a certificate**, rather than observed in simulations.
- **Speeds of fronts in random media.** Fronts in excitable media, and the use of Kingman's
  subadditive ergodic theorem to get deterministic speeds in first-passage percolation (Hammersley
  and Welsh, 1965; Kingman, 1968), are classical. A22 uses the same theorem. What it adds is the
  verification of the hypotheses for a concrete learning network, with explicit speed ceilings.
- **Certified reachability of hybrid systems.** Tools such as Flow*, CORA, JuliaReach and DynIbex
  enclose the trajectories of hybrid systems. A22 uses the same family of methods. Its contribution
  is scale and setting: 216 coupled hybrid cells with **plasticity**, event orders that vary inside
  the enclosure, and a 128-pulse transient.
- **Verification of neural networks, including spiking ones.** Methods such as Reluplex (Katz et al.,
  2017) verify properties of a network whose weights are already trained. The same holds for formal
  verification of spiking networks, for example of the adversarial robustness of a trained SNN
  (Seong, Kim and Ko, 2024, arXiv:2408.10900), or of small neuronal archetypes modelled as timed
  automata (De Maria et al.). A22 certifies the **learning dynamics** itself.

The claim, then, is narrow: certified enclosure of a learning spiking network through its whole
training transient, with variable event orders and per-port uncertainty. We are not aware of
earlier work that does exactly this, and pointers are welcome.

## Where the method stops working

This is a proof of concept of the method, on a small box. The box is far tighter than the
variability of real components, and in such a box much of the dynamics is close to linear, which is
part of why affine arithmetic succeeds. What is known about its limits:

- **How far the box can be widened** ([`sweep/README.md`](sweep/README.md)). Four fresh campaigns,
  identical to the v3.3 campaign except for the relative half-width ε of the physical parameters
  (initial states stay at ±1e-5):

  | ε | Layers accepted | First refusal |
  |---|---|---|
  | 1e-4 (the v3.3 result) | 18 of 18 | none |
  | 3e-4 | 18 of 18 | none |
  | 1e-3 | 17 | layer 18, lane 6 |
  | 3e-3 | 7 | layer 8, lane 0 |
  | 1e-2 | 4 | layer 5 |

  The enclosures stay roughly proportional to ε: at 1e-3, the median output-date width agrees
  with a linear fit through the 1e-4 and 3e-4 campaigns to within 25 % on every accepted layer, and
  within 5 % on most of them. What fails first is the decision of an event order: once the enclosures, though still
  linear, become comparable to the gaps between events, an order can no longer be certified, and
  the campaign refuses. A refusal is a limit of the computation, not a counterexample.

- **Correlations are essential.** Giving each constant a plain interval instead of a symbol per port
  made the enclosures grow 3 to 10 times, and that campaign stopped at layer 18. With one symbol per
  port, the enclosures are at most 5 % wider than in the earlier campaign that shared one symbol
  across a cell's three ports, even though that earlier campaign covered only a sub-family of the
  devices.
- **Wider fronts break single-step enclosures.** Past layer 18, when the arrival times of a cell's
  parents differ by a large fraction of a time unit, one-step enclosures stop contracting and their
  width grows layer after layer. This is the obstacle in the open step below.
![Output-date enclosure width by layer](figures/date_width_by_layer.png)

*Median width of the enclosure of the output dates, per layer, during training (v3.3 campaign).*

## What it does not show

- It is **one model**. The equations, topology and learning rule are fixed choices of this
  realization, inspired by the author's Reset Operator. Nothing here proves that hypothesis in
  general ([`docs/MODEL_BOUNDARY_EN.txt`](docs/MODEL_BOUNDARY_EN.txt)).
- **The proof is not yet reviewed.** It is a manual proof under explicit execution assumptions
  (A1–A4), not machine-checked and not yet read by an independent expert.
- **One step is open.** Entry into the deep-layer regime is certified for six prescribed
  preparations. Whether every preparation of the original source enters it is open
  ([`depth/point4/README.md`](depth/point4/README.md)).

## How you can help

The most useful single check is **Task 1** of [`REVIEW.md`](REVIEW.md): the lemma that every
threshold root is enclosed strictly, on which the whole event-order argument rests. It can be read
in one to three hours without knowing the rest. "It holds", "there is a gap here" or "here is a
counterexample" are all useful answers.

*This work was produced with Claude (Anthropic) and ChatGPT (OpenAI) under the author's direction.
The model and the research questions are the author's.*
