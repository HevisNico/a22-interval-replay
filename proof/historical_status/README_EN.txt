A22 v3.3 — LOCAL COVERAGE PROOF DEVELOPMENT AND INVARIANCE DOSSIER
22 October 2026

Current conclusion

Future invariance from Q remains established under its stated entry
hypothesis. The unconditional link from EVERY admissible training trajectory
to the stored terminal domain, H_entry, is still OPEN. This dossier must not
be presented as a completed global training-plus-future invariance proof.

This update develops the missing local proof. It specifies a relational
invariant, distinguishes physical states from counterfactual calculations,
gives macro covering arguments, and isolates a strict-root obligation needed
for coincident events and some memory joins. Exact countermodels demonstrate
why two weaker contracts are insufficient. They are NOT demonstrated failures
of the A22 campaign. There is no confirmed campaign counterexample here.

Read first

1. kernel_soundness/output/LOCAL_COVERAGE_PROOF_DRAFT_EN.txt
2. kernel_soundness/output/STRICT_ROOT_LEMMA_EN.txt
3. STATUS.json
4. GLOBAL_THEOREM_AND_WORD_PRESERVATION_EN.txt
5. TRAINING_ENTRY_REVIEW_EN.txt and FUTURE_INVARIANCE_PROOF_EN.txt

The last two are supporting documents retained from the previous dossier.
Their broad open local-proof obligation is refined, not discharged, by the
new documents. All authored reports are English. The supplied reference
source is preserved byte-for-byte, including its original comments/names.

New reproducible checks, from the extracted dossier directory

  python3 kernel_soundness/check_contract_countermodels.py
  python3 kernel_soundness/extract_effective_source.py

Use Python without -O so the check assertions are active. These scripts use
the standard library. Neither imports nor executes the A22 engine. The first
checks exact rational inequalities in two abstract countermodels. The second
reconstructs eight source views from 17 checked literal substitutions and
parses their syntax. This establishes textual correspondence, not semantic
soundness of the reconstructed functions. Other installed adapters remain
part of the proof target.

The matching reference source is included at
provenance_audit/source/A22_fresh_launch_v3_3_EN/ so the static reconstruction
is reproducible. All 87 files were checked against the supplied source ZIP.
source_unchanged.json records their hashes. No supplied program was changed,
no new campaign was launched, and no cell replay was performed.

Earlier independent certificate checks

  python3 provenance_audit/certify_future.py provenance_audit/output/all_terminal_exact.json future_recheck.json
  python3 provenance_audit/verify_future_certificate.py provenance_audit/output/all_terminal_exact.json future_recheck.json independent_recheck.json
  python3 final_entry_audit/certify_initial_section.py initial_recheck.json

These are finite inequality checks, not training simulations. The existing
certificates and passive audit outputs are included. The full campaign
results and native binaries are not duplicated. The passive full-payload
and clock audit scripts additionally require the original supplied result
ZIPs; the dossier includes their earlier recorded findings and input hashes.

What would close the remaining link

A validated source-level local simulation proof could close H_entry without
another campaign. One current route is the strict-center/root-order lemma
and reachable memory-join argument developed here. Alternatively, complete
authenticated transition certificates could establish the necessary local
predicates for this run. Terminal DAGs and truncated profiles are not such
a complete trace. The four H1/H2 reports do not cover every transition of
all 216 cells. A repeated pass count alone would not discharge the proof.

SHA256SUMS authenticates every included file except itself. The package
manifest is an integrity aid, not a mathematical proof certificate.
