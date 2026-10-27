# Future invariance at ε = 1e-3

**Question.** Does the end of training in the ε = 1e-3 campaign (engine v2.3.1, 18 of 18 layers) lie
in a domain Q from which every future pulse is transmitted exactly, as at ε = 1e-4?

**Answer, conditional on entry.** Yes. Both future-wave checkers of the published dossier, adapted
to ε, pass on the 216 terminal enclosures of the campaign:

| | ε = 1e-4 (published, v3.3) | ε = 1e-3 (this folder, v2.3.1) |
|---|---|---|
| Active / inactive cells, masked ports | 191 / 25, 15 | 191 / 25, 15 |
| Influential active ports | 525 | 525 |
| Whole network at rest after each pulse, before | 12.79036 | 12.79068 |
| Idle margin before the next pulse (gap ≥ 20) | > 7.209 | > 7.209 |
| Smallest margin (masked arrival after firing) | 0.0491 | 0.0489 |
| Margin before the first error actuation | 0.184 | 0.173 |

Every one of the 191 active cells fires exactly once per pulse, the network is at rest before
12.791, and it returns to Q. The cells with wide enclosures at layer 18 ((18, 4), (18, 8), learned
gain in about [1.47, 1.90]) pass as well.

## Files

| File | Content |
|---|---|
| `extract_terminal.py` | extraction of the 216 terminal enclosures from the campaign outputs (needs the engine and the full `result.json` files, not in the repository) |
| `terminal_eps1e-3.json` | the extracted enclosures (input of both checkers) |
| `certify_future_eps.py` | `proof/provenance_audit/certify_future.py` with ε as third argument; only ε-derived constants change, and the counts 191/25/15 are reported instead of imposed |
| `future_eps1e-3.json` | its certificate at ε = 1e-3: PASS |
| `check_v33_eps1e-4.json` | non-regression: at ε = 1e-4 on the published v3.3 states, identical to the published certificate on every common field |
| `verify_future_certificate_eps.py` | `proof/provenance_audit/verify_future_certificate.py` (the independent checker: directed Decimal, own series, no root search) with ε as fourth argument; the four ε-derived constants are the only change |
| `independent_check_eps1e-3.json` | its result at ε = 1e-3: PASS (191, 15, 525) |
| `independent_check_v33_eps1e-4.json` | non-regression: identical to `proof/provenance_audit/output/future_independent_check.json` |
| `NOTE_AUTHOR_FR.txt` | the author's note (French) |

Replay, standard library only, about two minutes each:

```sh
python3 -I certify_future_eps.py terminal_eps1e-3.json out.json 1e-3
python3 -I verify_future_certificate_eps.py terminal_eps1e-3.json future_eps1e-3.json check.json 1e-3
```

## What this does not establish

- **Entry.** Both checkers take the terminal enclosures as given. That they enclose every admissible
  device rests on the learning-coverage argument, written for the v3.3 program. Its extension to
  v2.3.1 is the subject of [`../../AUDIT_ENGINE_V231.md`](../../AUDIT_ENGINE_V231.md) and
  [`../../proof_extension/LEMMAS_EN.md`](../../proof_extension/LEMMAS_EN.md): no false-acceptance
  path found, ten lemmas proposed.
- **The text of `proof/FUTURE_INVARIANCE_PROOF_EN.txt`** names ±1e-4 in two places: the definition of
  Q (section A) and the phase durations (section B). The rest of its argument does not depend on ε, and
  its numerical conclusions (12.791, 7.209) still hold at 1e-3 according to both checkers. The
  general-ε wording is in [`../../../v33_c7/FUTURE_INVARIANCE_GENERAL_EPS_EN.txt`](../../../v33_c7/FUTURE_INVARIANCE_GENERAL_EPS_EN.txt).
- **The auxiliary charge `m` is not stored** in the scenario state. The extraction sets it to exactly
  r_m for a READY auxiliary that has received input: in READY, ṁ = κ(r_m − m) has r_m as exact fixed
  point after the section reset. Ports that never received input keep the initial box r_m ± 1e-5.
- The extraction itself was not rerun here (it needs Python 3.12 and the full outputs). For layer 18,
  the 12 `payload_sha256` in `terminal_eps1e-3.json` match the campaign receipts.
