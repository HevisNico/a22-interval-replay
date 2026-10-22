# Publishing this repository

Nothing has been published yet, so publish this version directly.

1. **Create an empty repository** on github.com (`+` → New repository), for example
   `a22-interval-replay`, Private at first. Do not add a README, .gitignore or license: they are here.
2. **Upload the files** (`uploading an existing file`), dragging the *contents* of this folder, not the
   folder itself, in batches of at most 100 files:
   - batch 1: everything except `engine/` and `proof/` (`.gitignore` is hidden on Mac/Windows: you can
     skip it and create it later with Add file → Create new file);
   - batch 2: the `proof` folder;
   - batch 3: the `engine` folder.
3. **Create the Release** `v3.3-proof` (Releases → Create a new release → tag `v3.3-proof`) and attach:
   - `A22_fresh_launch_v3_3_EN.zip` (engine package as distributed);
   - `A22_v33_manual_learning_coverage_proof_EN.zip` (complete proof dossier, with the program tree and
     both binaries; needed to run every proof check);
   - the two `.so` files listed in `results/HASHES.md` (optional, they are also inside the dossier).

   Description: "Campaign run_id f29efeaf…, kernel_id 65cf7b77…; complete proof dossier. Hashes in
   results/HASHES.md." Optionally attach the compressed campaign outputs (≤ 2 GB per file) and add
   their SHA-256 to `results/HASHES.md`.
4. **Check** that the README displays with its figure, and that the links to `proof/`, `REVIEW.md` and
   `docs/DETAILS.md` work.
5. **Make it public** when ready (Settings → General → Danger Zone → Change visibility), and make sure
   Issues are enabled (Settings → General → Features): reviewers answer there.

This file can be deleted once the repository is published.
