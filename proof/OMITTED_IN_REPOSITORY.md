# What is omitted from this folder

This folder is the proof dossier `A22_v33_manual_learning_coverage_proof_EN.zip`, unchanged, except
for one directory: `provenance_audit/source/A22_fresh_launch_v3_3_EN/`.

That directory is the exact program used by the campaign. It is omitted here to avoid duplicating it:
- its 87 source files are byte-identical to [`../engine/`](../engine/);
- its two compiled extensions (`affine/_rounding_native…so`, `kernel/native/_a22_native…so`) are
  not stored in the repository tree; their hashes are in [`../results/HASHES.md`](../results/HASHES.md).

Consequences:
- `SHA256SUMS` in this folder still lists the omitted files; those lines cannot be checked here;
- the scripts `learning_justification/verify_build_identity.py`,
  `learning_justification/verify_source_witnesses.py` and `kernel_soundness/extract_effective_source.py`
  read that directory and therefore need the complete dossier.

**To run every check**, download the complete dossier from the GitHub Release `v3.3-proof`
(SHA-256 in [`../results/HASHES.md`](../results/HASHES.md)), unzip it, and follow its `README_EN.txt`.
None of the scripts imports the engine, loads a compiled extension, or runs a campaign.

## Historical statements kept unchanged

Some files of the dossier record the status *before* the learning-coverage theorem, and say that the
training entry H_entry is open: `GLOBAL_THEOREM_AND_WORD_PRESERVATION_EN.txt` (one sentence, which
points to `TRAINING_ENTRY_REVIEW_EN.txt`), `TRAINING_ENTRY_REVIEW_EN.txt`, and `historical_status/`.
These statements are superseded. The current status is in `STATUS.json`: H_entry is proved by the
manual argument of `learning_justification/output/LEARNING_COVERAGE_THEOREM_EN.txt`, under A1–A4, and
that argument has not yet been reviewed independently. The files are kept byte-identical, because
their hashes are cited by `SHA256SUMS`, by `../results/HASHES.md` and by `../depth/`.
