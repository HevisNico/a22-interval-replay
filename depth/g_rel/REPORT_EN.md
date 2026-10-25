# Relative G: extended response, common criterion and 35/40 memberships

25 October 2026. The theorem is conditional and manual. Numerical membership
checks concern explicit declared decimal vectors and regenerated charges;
the learning simulations do not become certified physical endpoints.

## Result

One common local gain-arrival predicate accepts 35 of 40 states. It uses no
per-centre gain box and does not enumerate learning-dose patterns.

| Initial log-gain radius alpha | Accepted states, nominal and 1% devices combined |
|---|---:|
| 0.01 | 10/10 |
| 0.03 | 10/10 |
| 0.1 | 6/10 |
| 0.3 | 9/10 |

The target of accepting all but the two multiple-response cases (38/40)
has not been reached. A negative sufficient margin is not, on its own, a
physical counterexample.

## Five exclusions

| Declared state | First unresolved cell | Guard | Lower margin |
|---|---|---|---:|
| nominal parameters, alpha=0.1, coherent negative shift | (5,3) | raw current ends under protection | -0.369888057 |
| nominal parameters, alpha=0.1, random state 1 | (7,7) | raw current ends under protection | -0.024044782 |
| 1% parameters, alpha=0.1, coherent negative shift | (5,3) | raw current ends under protection | -0.372472336 |
| 1% parameters, alpha=0.1, random state 2 | (7,5) | raw current ends under protection | -0.043687347 |
| 1% parameters, alpha=0.3, coherent negative shift | (12,1) | ERROR starts after head | -1.3631e-9 |

The coherent negative alpha=0.1 simulations produced multiple responses per
probe. The two random alpha=0.1 cases already showed small probe-date drift.
The final case is near a head-ERROR equality at the scale of numerical witness
windows and simulated centres; no strict physical sign is inferred. None of
these guards was weakened or renamed PASS.

## Gain variations admitted by the common set

Compare a port only in states where it is classified as influential. Across
the ten accepted alpha=0.01 states, the union contains 533 port positions:
217 have gain ratios above 1.6, including 66 above 2; the maximum is about
6.15593. Across all 35 accepted states, 468 influential-port positions have
ratios above 2; the largest ratio is about 17.4436.

These extremes may come from different states. Their Cartesian product is
not certified. G_rel preserves relations between gains and relative phases.
It is not merely a union of small boxes around the saved centres.

## Extended response and relative coordinates

After a raw current ends, the physical response is
H(u)=h(1) exp(-kappa(u-1)), u>=1. The generator proposes a first crossing
piecewise, checks both signs with directed arithmetic, and excludes all
earlier crossings. The reader additionally checks a strictly positive slope
throughout the head bracket. Eleven accepted head instances occur after the
first raw ending.

Each cell subtracts its first parent arrival. Witness intervals enclose phases
defined by the declared gains, rather than representing one growing physical
tube for every state in G. The predicate keeps the relative arrival profile,
not only its diameter W. A further reduction to a scalar W and a few gain sums
has not been established and may be needed for a tractable entry proof.

## Why an independent factor-two box is invalid

For cell (1,0) of the nominal-device centre trained from initial shift +0.03,
only the central source port is driven. Its learned central gain is about
2.25313269511721. Dividing that gain by two gives a maximum READY charge below
0.728248019, strictly below threshold 1. ERROR occurs after the finite raw
current ends and cannot retroactively charge the principal. Thus the independent
box [g/2,2g] contains a state without a first response to an isolated pulse.
A useful large G must retain compensating gain-arrival constraints.

## Theorem and scope

THEOREM_EN.md defines G_rel(theta,beta) and proves its local invariance and
exact word fidelity. Influential gains remain physically constant; masked
gains and b may evolve. The proof uses one induction over layers and waves,
including regeneration, protection and the absence of a second firing.

The numerical tests establish membership of saved vectors at their respective
physical parameters. They do not show that each gain vector works for every
other physical device in the ±1% box. Regeneration is an entry premise, not
an artificial reset inserted into training. Universal training entry and
arbitrary-depth certification remain open.

## Verification

AUDIT.json records PASS for 35 witnesses and 6,685 active-cell checks. The
read-only reader does not run the learning simulator or search for heads;
it shares arithmetic and some evaluators with the generator. This is neither
independent arithmetic validation nor proof-assistant verification.

```sh
python3 verify_manifest.py
python3 audit.py
```

To regenerate proposed head brackets, run `python3 check.py`; timing fields
will differ. INPUT_STATES.json contains the complete declared inputs.
MEMBERSHIP.json retains both accepted and unresolved cases. The gain ranges,
physical-input validation and factor-two check are separate JSON records.

Recorded wall times on four workers: membership generation 191.54 seconds;
final release-directory read-only audit 221.71 seconds, excluding development and preliminary trials.
