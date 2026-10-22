A22 v3.3 — MANUAL LEARNING-COVERAGE AND INVARIANCE PROOF
22 October 2026

Result and level of assurance

The current document gives a manual source-level proof that the authenticated
existing training campaign encloses every trajectory of the stated physical
family, under its explicit execution assumptions A1-A4. It derives
H_entry: Reach_training(1116) subset Q, then combines this with the previously
established future return theorem for canonical source pulses with gaps >=20.

This is a mathematical argument supplied for review. It has NOT been checked
by a proof assistant or by an independent expert. The static checks in this
package witness source facts; their PASS status is not semantic certification.
The archived software status remains experimental_not_qualified. The proof
does not qualify the compiler or native binary, and states its arithmetic,
runtime, provenance and namespace assumptions explicitly.

Read in this order

1. learning_justification/output/LEARNING_COVERAGE_THEOREM_EN.txt
2. learning_justification/output/GROUP_ENTRY_CLOCK_LEMMA_EN.txt
3. learning_justification/output/REVIEW_GUIDE_EN.txt
4. STATUS.json
5. FUTURE_INVARIANCE_PROOF_EN.txt and the previous independent certificates
6. learning_justification/output/BUILD_IDENTITIES_EN.txt

The new proof addresses the previously open root-order and memory-anchor
contracts with a fresh open-image argument, and includes the forward-entry
case split for exterior groups. Fixed FAST/SLOW boundaries are treated
separately from uncertain READY fires. Physical device parameters stay fixed;
the enclosing arithmetic may admit a larger varying-parameter family.

Correction incorporated: Section 8(vi) now explicitly proves the commutation
fallback _first_crossing_cover using continuity, endpoint signs and ordered
slice coverage. No slope assumption is needed. The saved records do not
identify whether this fallback served any of the 202 commutations.

Build identity clarification: the theorem targets the post-build program
identity ae1b515a..., which includes the two archived .so files. The original
manifest's 426eefc4... identity is for the same sources before compilation.
Both exact binaries are now included under the reference program directory
at affine/_rounding_native.cpython-312-x86_64-linux-gnu.so and
kernel/native/_a22_native.cpython-312-x86_64-linux-gnu.so. The original
PACKAGE_MANIFEST.json remains unchanged and retains its correct pre-build
label. BUILD_IDENTITIES_EN.txt explains the full hashes and file sets.

Scope of the result

The specified 128-pulse training protocol at times 8k leads to the terminal
section at 1116. The future theorem permits canonical source pulses with
gaps at least 20. It gives one firing per active cell per future pulse,
quiescence before 12.791, and exact word preservation for a fixed device
and its fixed influential entry gains. It does not assert identical latency
across different devices or different learned entry states. Continuous-time
invariance is for the between-section flow tube, not the resting section Q
alone during an active pulse.

Provenance and restrictions respected

All 87 supplied source files remain byte-for-byte unchanged. No new campaign,
cell simulation or cell replay was performed. The existing 216-cell audit,
terminal extraction, shared-clock audit and independent future inequalities
are retained. The complete heavy campaign payloads are not duplicated here.
The matching reference source is included solely for review/reproducibility.
The supplied four H1/H2 reports are not treated as a complete independent
transition proof for every cell.

Passive checks, from the extracted package directory

  python3 learning_justification/verify_source_witnesses.py
  python3 learning_justification/verify_build_identity.py
  python3 kernel_soundness/extract_effective_source.py
  python3 kernel_soundness/check_contract_countermodels.py

Use ordinary Python without -O. These scripts import no A22 engine and do
not launch training. The source checker has 40 function witnesses and 110
checks, including the 87 unchanged-source hashes. The other checks reconstruct
eight effective source views from 17 literal substitutions and verify two
exact abstract countermodels to weaker proof contracts. Those countermodels
remain useful; they are not demonstrated counterexamples to this campaign.

Earlier independent finite inequality checks are also reproducible:

  python3 provenance_audit/certify_future.py provenance_audit/output/all_terminal_exact.json future_recheck.json
  python3 provenance_audit/verify_future_certificate.py provenance_audit/output/all_terminal_exact.json future_recheck.json independent_recheck.json
  python3 final_entry_audit/certify_initial_section.py initial_recheck.json

Historical documents

Earlier local proof drafts, TRAINING_ENTRY_REVIEW_EN.txt,
GLOBAL_THEOREM_AND_WORD_PRESERVATION_EN.txt, and historical_status/ preserve
their previous OPEN statements. They record the state before the present
manual proof. Their numerical/future arguments remain supporting evidence;
their learning-proof status is superseded by the current theorem only at
the stated manual level. Original source and numerical evidence are unchanged.

SHA256SUMS authenticates all packaged files except itself. It is an integrity
manifest, not a mathematical proof certificate.
