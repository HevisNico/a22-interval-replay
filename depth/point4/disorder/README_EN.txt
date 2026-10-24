A22 — independent disorder and a conditional front-to-tail reduction

Read PROOF_EN.md. Universal original-source entrance is NOT PROVED.

New results:
1. If every dense front stays within diameter .08 through 63 pruning passages,
   the complete 128-cohort boundary reaches layer64 with diameter <.090656432
   and gaps >15.503463513. This is a conditional theorem, not front closure.
2. Directed 63-layer b-only and multi-parameter endpoint histories exceed .0058
   while remaining below .008 and .012 respectively.
3. Uniform local perturbation bounds cover all independent port/cell parameters,
   including an explicit fresh-charge correction. This reduces the problem to
   a nominal map with bounded additive inputs.

Reproduce (Python standard library):
  python3 verify_bridge.py
  python3 verify_forcing.py
  python3 verify_disorder.py
  python3 verify_full_corner.py
  python3 check_kernels.py
The long 63-layer histories may take several minutes. Their event checks use
130-digit intervals. The other numerical certificates use 70-digit intervals.
All proof checks use explicit exceptions, not Python assertions.

Exploratory only (NumPy and SciPy):
  python3 search_disorder.py
The search is not a certificate or a global maximization result.

The preceding delivered archive is included unchanged under dependencies/.
No original campaign, receipt, or repository source is modified.

STATUS.json states the exact scope and unresolved obligations.
ENVIRONMENT.json records Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0 and
SHA-256 hashes of the interpreter and installed numerical-library binaries.
Regenerate that environment inventory with python3 record_environment.py.
SOURCE_MANIFEST.json records checker hashes and the unchanged dependency.
SHA256SUMS covers every packaged file except itself.

Validation performed: all five current checkers passed; bridge and forcing
were also rerun with python3 -O, giving byte-identical certificate JSON.
Long interval histories were not rerun in optimized mode.
