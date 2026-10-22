# History

## `v3.2/` — previous campaign (shared constants per cell)

Complete 18-layer campaign (run_id `872e032a…`), 648/648 A14 boxes inside. Its engine gave the auxiliary
constants LM, LS, LE, M, C of a cell **one** symbol shared by its three ports. The model makes them
independent per port (exact counterexample found by the author: a mark-duration gap of
400/99,999,999 that the shared symbol cannot represent). This campaign therefore covers only the
sub-family where the three ports of a cell share their constants. Kept for comparison: engine ZIP,
summary, H1/H2 re-check, hashes (`HASHES_v3_2.md`; file paths there are those of the v3.2 repository).

## `plain_box_package/` — first correction, stopped at layer 18

The shared symbols were replaced by plain interval boxes. Sound, but every evaluation then forgot that
a port keeps the same constant at every pulse: layer-17 enclosures were 3–10× wider than in v3.3, and
cells (18,1) and (18,11) refused ("recovery guard overlaps external boundary (actuation history)").
Kept: the campaign identity (`campaign_identity.json`), the two refusal records with their tracebacks, and the stop record.
v3.3 (per-port symbols) removed the refusal.
