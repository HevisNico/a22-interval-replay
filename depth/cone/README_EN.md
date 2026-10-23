# A22 point 3 — speed ceilings and forward cones

23 October 2026. English-language supplement; no new campaign.

The package contains a manual proof, a numerical certificate and a verifier
using two arithmetic implementations. It also includes the exact English
points 1–2 ZIP as a dependency, so the required tail assumptions and their
proofs are available without another download.

## Results

| Scope | Certified speed ceiling, in layers per model time unit |
|---|---:|
| Cohorts in the exact-rest heterogeneous tail | <1.500248 |
| Cohorts in the full-fresh-initial-box tail, including the first-cohort correction | <1.500548 |
| First activation from the original initial box, including learning, without a tail-entry assumption | <18.234831 |

The first two ceilings require the point-1 contract. The full-initial-box
variant additionally requires the first input at time ≥20. The third bound
is a conservative gain-cap/current-envelope bound, not a sharp estimate of
the fastest physically attainable device.

The cone is a first-arrival or cohort-front statement. It is not an
unqualified information-speed bound for arbitrary perturbations of an
already active network. The proof explains this distinction.

## Reproduce

Using Python 3 and its standard library:

```bash
python3 verify_cone.py
```

Expected: `PASS_DECIMAL_AND_INTEGER_CONE_CHECKS`.

The program checks source/dependency hashes, root brackets, reciprocal
speed bounds, the first-cohort correction and the global comparison formula.
It does not execute an A22 campaign. No NumPy, SciPy or A22 native binary
is required. Checks remain active with Python `-O`.

Files:

- `03_CAUSAL_CONE_EN.md`: statements, derivations, assumptions and scope.
- `verify_cone.py`: new numerical checks.
- `directed.py`: directed 70-digit Decimal intervals with explicit series tails.
- `integer_support.py`: the earlier independent integer arithmetic implementation;
  imported as support, not required to be run directly for this supplement.
- `cone_certificate.json`: numerical results and exact execution environment.
- `SOURCE_MANIFEST.json`: source and dependency identity.
- `sources/model_reference.md`: unchanged original-language model snapshot.
- `dependencies/`: the previously delivered points 1–2 English ZIP, unchanged.
- `SHA256SUMS`: hashes of the package contents, excluding this list itself.

Before recomputation, integrity can also be checked with:

```bash
sha256sum -c SHA256SUMS
```

The earlier ZIP can be unpacked separately to rerun its two verifiers.
Regenerating a report under a different Python version can change its
environment metadata and hash while leaving numerical bounds unchanged.

**Proof level:** manual arguments with verified numerical lemmas; independent
expert review pending. The two arithmetic implementations are not two
independent scientific reviews. Point 4, universal entry into the tail
contract, remains open.
