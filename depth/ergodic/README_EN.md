# A22 — Heterogeneous tail and ergodic speed

23 October 2026. This package is separate from the repository and production
campaigns. All newly written documentation is in English. Source snapshots
retain their original language and bytes so their hashes remain verifiable.

The two requested steps are addressed by manual proofs with directed
numerical checks. **No new learning or propagation campaign has been run.**
No particular random law has been selected or simulated.

## Results

**1. Heterogeneous tail.** The physical constants actually perturbed in A22
are independent across ports and cells, throughout their relative ±10⁻⁴
box. The three gain offsets are independent as well. Protection,
regeneration and six-layer contraction are established under an explicit
entrance contract.

| Variant | Width contract | Recovery slack | Block-closure slack |
|---|---|---:|---:|
| Exact rest; log-gain offsets ±10⁻⁵ | 0.11 at block boundaries; <0.110200 between them | >2.2681 | >0.0008225 |
| Complete initial box of fresh cells; first arrival ≥20 | 0.11 at boundaries; <0.111000 between them | >2.2673 | >0.00000520 |

The second variant includes initial ERROR tails, which can move effective
log-gain offsets up to +9·10⁻⁵. Initial principal charge is not artificially
reset: its effect on the first head is bounded and summable over depth.

**2. Speed in a disordered medium.** For a stationary **ergodic** law of
layers, there is a deterministic limiting duration γ shared by all lanes,
almost surely equal across realizations, and independent of every finite
preparation that enters the contract. Speed is 1/γ. The proof explicitly
constructs subadditive quantities and applies Kingman's theorem. It also
treats the first unregenerated response in the second variant through a
comparison error totaling <10⁻⁸.

The joint law, including correlations, matters. Equal parameter means
alone are not asserted to determine the speed. If gains remain nominal
and only auxiliary constants vary, the limiting duration stays exactly
nominal: those auxiliary constants no longer enter the head map once
protection and regeneration are guaranteed.

## Files and reproduction

- `01_HETEROGENEOUS_TAIL_EN.md`: assumptions, statements and physical proof.
- `02_ERGODIC_SPEED_EN.md`: probabilistic statement, proof and scope.
- `directed.py`, `verify.py`: 70-digit directed decimal arithmetic, finite
  series with explicit remainders, and checks of the numerical lemmas.
- `verify_integer.py`: separate checks of root brackets, contraction,
  closure and recovery using directed integer arithmetic, without reading
  the first verifier's results.
- `comparison_and_bounds.json`, `integer_crosscheck.json`: results.
- `STATUS.json`, `REVIEW_NOTES_EN.md`: proof status and review targets.
- `sources/`: unchanged source snapshots, repository commit and hashes.
- `SHA256SUMS`: hashes of the delivered contents, excluding this list itself.

From this directory, using Python 3 and its standard library only:

```bash
python3 verify.py
python3 verify_integer.py
```

Expected results: `PASS_NUMERICAL_LEMMAS`, then
`PASS_INDEPENDENT_INTEGER_CRITICAL_CHECKS`.

Neither program depends on NumPy, SciPy or the A22 native binaries. The
actual execution environment is recorded in the first JSON report.
Checks do not rely on `assert`; they remain active under Python `-O`.

To check the packaged files before recomputation, on systems with sha256sum:

```bash
sha256sum -c SHA256SUMS
```

Recomputing a JSON result on another Python version may change its environment
metadata and therefore its file hash, without changing the numerical bounds.

## Essential limitation

This package **does not establish entry into the contract for every
admissible upstream preparation**. “Complete initial box” refers to fresh
cells **downstream of an already conforming entrance**, with the stated
additional timing hypothesis. Requested point 4 therefore remains separate.

Proof status: **manual derivations submitted for review, supported by
rechecked numerical lemmas**. Two arithmetic implementations written in
the same work are not two independent scientific reviews or a formal proof.
