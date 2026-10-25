# v4.3: future invariance on a relative gain domain

This release adds a **conditional manual theorem**, not a training-entry proof.
The physical kernel is unchanged. Start with the [one-page reviewer note](reviewer/ONE_PAGE_EN.pdf)
or its [text source](reviewer/ONE_PAGE_EN.md), then [THEOREM_EN.md](THEOREM_EN.md).

For any admissible fixed device and a regenerated state satisfying the local
gain-arrival constraints G_rel(theta,beta), all future canonical pulse words with
gaps at least 20 are transmitted exactly through the 18-layer network. The same
191-cell mask fires once per pulse. Influential gains remain constant because
their ERROR phases stay under protection; masked gains and b may remain plastic.
Latencies need not be the same for different learned states or devices.

The head formula includes the finite raw-current tail after age one. Conditions
use relative parent phases and permit different dose patterns in one nonlinear
set, without certifying their Cartesian envelope.

## Numerical evidence and limitations

- `MEMBERSHIP.json`: 35/40 declared decimal states pass, including all ten at alpha=0.01.
- `AUDIT.json`: separate read-only verification of those 35 witnesses, including
  upward root slopes; it shares arithmetic/evaluation helpers with the generator.
- `INPUT_STATES.json`: complete declared gains, physical parameters and probe diagnostics.
- `REPORT_EN.md`: five exclusions, gain spreads, and exact scope.
- `FACTOR_TWO_COUNTERCHECK.json`: why an independent [g/2,2g] box can contain a
  cell unable to answer its first isolated pulse.

These are **not certified endpoints of a whole learning campaign at ±1 %**.
Membership is for each state at its own declared physical parameters, with
regenerated charges as a premise. Initial-error memory is not silently reset
during training. Universal training entry, independent-gain envelopes, and
arbitrary-depth certification remain open. No new learning campaign or event
order claim is included in the v4.3 theorem.

Proof level: manual argument with directed computations under explicit runtime
assumptions; not machine-checked or independently reviewed. Simulations that
supplied the decimal vectors remain exploratory.

## Replay

Python 3, standard library only, no `-O` restriction needed by the numerical guards:

```sh
python3 verify_manifest.py
python3 audit.py
```

`audit.py` takes a few minutes with four worker processes. To regenerate proposed
head brackets, run `python3 check.py`. This rewrites `MEMBERSHIP.json`; durations
will differ. Keep a pristine copy if you want to preserve the release hashes.

The one-page reviewer note and the complete dossier are also attached to the
GitHub release `v4.3`. The code and the mathematical/data documents retain the
repository's respective MIT and CC BY 4.0 licenses. The work was prepared with
ChatGPT/Codex under the author's direction; no claim of independent peer review
is made.
