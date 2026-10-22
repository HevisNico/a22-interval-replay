# Publishing this repository

1. Create an empty repository on GitHub (for example `a22-interval-replay`), private or public.
   If the v3.2 version is already published, commit this version on top of it instead
   (`git add -A && git commit -m "A22 v3.3: per-port parameters, full campaign"`).
2. For a new repository, from this folder:

   ```
   git init -b main
   git add .
   git commit -m "A22 v3.3: validated interval replay with independent per-port parameters"
   git remote add origin https://github.com/<you>/a22-interval-replay.git
   git push -u origin main
   ```

3. Create the Release and attach the exact engine ZIP (and, optionally, the campaign and the two
   built extensions, which make the kernel_id recomputable):

   ```
   gh release create v3.3-campaign A22_fresh_launch_v3_3_EN.zip \
       --title "A22 v3.3 campaign" \
       --notes "Exact engine package of campaign run_id f29efeaf…, kernel_id 65cf7b77… (see results/HASHES.md)."
   # optional:
   # tar czf campaign_v33.tar.gz results/A22_v33_001 && sha256sum campaign_v33.tar.gz
   # gh release upload v3.3-campaign campaign_v33.tar.gz
   ```

   Then add the campaign archive's SHA-256 to `results/HASHES.md` and commit it.

4. Before making the repository public: check `LICENSE` and `CITATION.cff` (author name, and add your
   papers under `references:` if you want them cited).

This file can be deleted once the repository is published.
