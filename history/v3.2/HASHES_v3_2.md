# Identities and hashes

## Campaign

| Item | Value |
|---|---|
| run_id | `872e032aa01546c79a447cbf2f558989` |
| kernel_id (program identity + environment) | `8f67e092f4275915adda5465739a61ad2be9dd381ea18dc7177028ef5b20019a` |
| Program-source identity (`run.identity()`: run.py, build_native.py, affine/, kernel/) | `3d4438c05a08151239b6d930015b7a5871ba1a3f2b41e85f9f5e1264a246ac0d` |
| Environment | CPython 3.12.14, NumPy 2.3.5, SciPy 1.17.0, native backend (`_rounding_native` sha256 `f8745c6046e0ba84f0c8d6457d478d43bc041132ec67bb4484bb131e08f8941e`) |
| Symbols per affine form / Decimal precision | 256 / 160 |

The kernel_id includes the environment, so it is specific to the machine that ran the campaign. The
program-source identity is machine-independent.

**Provenance check (done):** we unpacked `A22_Affine_Fast_Start_v3_2_clean.zip` (Release asset), computed
`run.identity()`, and hashed it with the environment above using the runner's canonical rule
(`{'sources', 'environment', 'precision': 160, 'symbols': 256}`). The result reproduces the campaign
kernel_id `8f67e092…` exactly. The native binary in the ZIP has the recorded sha256 `f8745c60…`. The
campaign was therefore produced by exactly this package.

## Files (SHA-256)

| File | SHA-256 |
|---|---|
| `A22_Affine_Fast_Start_v3_2_clean.zip` (Release asset; `engine/` is its unpacked content, checked by `engine/verify_bundle.py`) | `355ec62c581e3dfc970f45683bbe33436f9ba7d0084cd9ef49c260cd9335ee0b` |
| `tools/verif_h1h2.py` (extended; produced the layer-18 check) | `bfff4ba18cdbcd7313d2c429f1b4cf935ee0898684d250022e826ffffa9c17a6` |
| `tools/bilan_campagne.py` (with `--reference`; produced the summary) | `df19337693e1f0b4f9139b01b23aa2c7511e64d2bf2b21a8d1642fd8e81c4337` |
| `results/campaign_summary.json` | `c8cea878a6ed1cd9fed6a2af13c434e82b956601087fedab31563a2c5534def7` |
| `results/h1h2_layer18_lanes_4_8.json` | `243d9e288ad0916950cb399e544b57762b3a7cd7bbd2512b3bfbef571022ccc7` |
| `results/reference_A14_gain_boxes.json` | `e382fae8de2ce851c08106983e47e6550bdfe2c990601ea253fb9a502f6ccca4` |
| `results/v2_refusal_layer18_lane4.json` | `d5b45e245c0761d83950135eb2dc2d45260d71e38b79bd35e8f8e8a86522cf69` |

The `tools/` scripts are newer than the copies inside the engine ZIP. `verif_h1h2.py` there
(`715d30f0…`) does not yet check spikes resolved by commutation. Neither script is part of the program
identity, and both are read-only with respect to a campaign.

## Not included

The campaign itself (all `result.json` files, several hundred MB). Keep it with its per-layer ZIPs and
their `delivery.json` hashes; for a public release, attach it to a GitHub Release and add its SHA-256
here.
