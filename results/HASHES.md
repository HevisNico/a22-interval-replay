# Identities and hashes

## Campaign (v3.3)

| Item | Value |
|---|---|
| run_id | `f29efeaf7ff44d09bbce1e149630f39a` |
| kernel_id (program identity after build + environment) | `65cf7b7776347fa8de24fa5e1c357e98ee0f90c4bb8d65f694610fb26db3b25c` |
| Program-source identity **before** the native build (`run.identity()` with no built extension) | `426eefc40a4c77e8649827b06e3d3cb6e40832b3f678f48c146535c24c60d944` |
| Engine package ZIP as delivered (`A22_fresh_launch_v3_3_EN.zip`; its contents are `engine/`) | `9939b189f687bad28244edb96c23b0366d7af9a93efa750ac98b68748834ae16` |
| Environment | CPython 3.12.14, NumPy 2.3.5, SciPy 1.17.0, native backend (`_rounding_native` sha256 `29b1d226d6576e418c38d476cb050a20b37f6db67b6f70ca734423cac6985c57`) |
| Symbols per affine form / Decimal precision | 256 / 160 |
| Physical model reference (`engine/reference/full_model_reference.md`) | `6f8462431cd43714af99d2181d5d017b2de910381690665ba7875659c061fecf` |

The program identity includes the native extensions, which are built on the target machine. So the
kernel_id cannot be recomputed from this repository alone; it is specific to the machine and build
that ran the campaign. The source identity before the build is machine-independent: unpack the ZIP (or
use `engine/`), and hash as `run.identity()` does before running `build_all_native.py`.

**Provenance evidence.**
- `tools/verif_h1h2.py` recomputes the program identity of the package it is run from (sources, built
  extensions, environment) and refuses to run unless it equals the campaign kernel_id. It ran to
  completion on cells (18,1), (18,4), (18,8) and (18,11) and reports kernel_id `65cf7b77…`
  (`results/h1h2_layer18_lanes_1_4_8_11.json`). The campaign was therefore produced by the package the
  checker was run from.
- That checker and `tools/bilan_campagne.py` have exactly the hashes of the v3.3 package (below), and
  the summary records the v3.3-only counter `recovery_group_resolutions`.
- The widths match the per-port design (equal to v3.2 up to layer 11, ≤ 5 % above it later), not the
  plain-box package (3–10× wider at layer 17).

For a complete, machine-independent check, the campaign owner can publish the two built extensions
(`engine/affine/_rounding_native*.so`, `engine/kernel/native/_a22_native*.so`) as Release assets; with
them, `run.identity()` and the kernel_id can be recomputed from this repository.

## Files in this repository (SHA-256)

| File | SHA-256 |
|---|---|
| `history/v3.2/A22_Affine_Fast_Start_v3_2_clean.zip` | `355ec62c581e3dfc970f45683bbe33436f9ba7d0084cd9ef49c260cd9335ee0b` |
| `tools/verif_h1h2.py` | `bd13eff1458c7f7834834b6b7254d539325742eb92e1d963832eb9e5022fab0f` |
| `tools/bilan_campagne.py` | `f02aefc2b72d1c8e6ffe20e33ae9c4039a41ddf79eeb045246313c37c438a707` |
| `results/campaign_identity.json` | `9b6fbd980c76110856f90ac7326d66af305c042df7f8a33c7db03d74fc22cdd4` |
| `results/campaign_summary.json` | `3cfc206b282247b6b4db3690ba799fe1a32faa0cbd9d747a1fdbf39f465e3fec` |
| `results/h1h2_layer18_lanes_1_4_8_11.json` | `3b5350f91eb5f8dde3bd836855fb7c95a0ff70afc50b0e9afc1cc88bb503b4c2` |
| `results/layers_cells_and_timings.json` | `423fec93e8865c8d98e8fda42d1b10cc78d65d85af907114ba5247d5f38e76bf` |
| `results/reference_A14_gain_boxes.json` | `e382fae8de2ce851c08106983e47e6550bdfe2c990601ea253fb9a502f6ccca4` |
| `results/v2_refusal_layer18_lane4.json` | `d5b45e245c0761d83950135eb2dc2d45260d71e38b79bd35e8f8e8a86522cf69` |
| `engine/SHA256SUMS` | `fab83b7418665fa53a8d60cbb526fcae758f3ee552b83fa8ce850e86192bd022` |
| `engine/PACKAGE_MANIFEST.json` | `5c7b1c005d2d404315801b5bb01a8e97f469cae36ca54ff8a08fe26070a37bf7` |

`engine/SHA256SUMS` lists the hash of every file of the engine package.

## Not included

The campaign itself (all `result.json` files, several hundred MB). Keep it with its per-layer
`verification.json` hashes; for a public release, attach it to a GitHub Release and add its SHA-256
here.

## Previous campaign

The v3.2 campaign (run_id `872e032a…`, kernel_id `8f67e092…`, shared constants per cell) is documented
in `history/v3.2/HASHES_v3_2.md`, with its engine ZIP and summary.
