# Identities and hashes

## Campaign (v3.3)

| Item | Value |
|---|---|
| run_id | `f29efeaf7ff44d09bbce1e149630f39a` |
| kernel_id | `65cf7b7776347fa8de24fa5e1c357e98ee0f90c4bb8d65f694610fb26db3b25c` |
| Program identity **after** build (71 source files + 2 compiled extensions = 73 files; this is the identity of the campaign and of the theorem) | `ae1b515af494ef604526dbe8e651c325512b997f6e93f1d3aefb646b96e13256` |
| Source identity **before** build (the same 71 files, no extension; `source_identity_before_target_build` in `engine/PACKAGE_MANIFEST.json`) | `426eefc40a4c77e8649827b06e3d3cb6e40832b3f678f48c146535c24c60d944` |
| Environment | CPython 3.12.14, NumPy 2.3.5, SciPy 1.17.0, `arithmetic_backend=native` |
| Symbols per affine form / Decimal precision | 256 / 160 |
| Physical model reference (`engine/reference/full_model_reference.md`) | `6f8462431cd43714af99d2181d5d017b2de910381690665ba7875659c061fecf` |

**The two compiled extensions of the campaign** (Release assets; also inside the complete proof dossier):

| File (path inside the program tree) | Bytes | SHA-256 |
|---|---:|---|
| `affine/_rounding_native.cpython-312-x86_64-linux-gnu.so` | 21,880 | `29b1d226d6576e418c38d476cb050a20b37f6db67b6f70ca734423cac6985c57` |
| `kernel/native/_a22_native.cpython-312-x86_64-linux-gnu.so` | 41,032 | `9cf239a62f67859f3e3694ff929112f2034678aee97f0867a7391e9315cf6cb8` |

They were extracted unchanged from the `program_used/` snapshots stored with the campaign; the same
bytes appear in all thirteen snapshot archives.

## Exact provenance reconstruction

The identity algorithm (`run.identity()` in `engine/run.py`): sort the selected relative paths; hash
the concatenation, for each file, of its UTF-8 path, one NUL byte and its raw bytes. The `kernel_id` is
the SHA-256 of compact, sorted-key JSON of `{sources, environment, precision: 160, symbols: 256}`, where
`environment.native_sha256` is the hash of `_rounding_native…so`.

Applied to `engine/` plus the two extensions above, this gives the post-build identity `ae1b515a…` and
the campaign `kernel_id` `65cf7b77…` **exactly**. It was reproduced twice, independently:
- by `learning_justification/verify_build_identity.py` in the complete proof dossier (standard library
  only; it loads no extension and imports no engine code);
- by a separate re-implementation written during the audit, from `run.py`'s definition.

So the campaign was produced by exactly the published sources and these two binaries. This establishes
artifact identity; it is not a proof that the binaries implement their C sources (assumption A2 of the
theorem).

## Release assets

| Asset | SHA-256 |
|---|---|
| `A22_fresh_launch_v3_3_EN.zip` (the engine package as distributed; its sources are `engine/`) | `9939b189f687bad28244edb96c23b0366d7af9a93efa750ac98b68748834ae16` |
| `A22_v33_manual_learning_coverage_proof_EN.zip` (complete proof dossier, with the program tree and both binaries) | `bf9586996db601c4d0e56f2e4747b19c46597dbd5fc6b7ca0042fe5963e54952` |
| the two `.so` files | see the table above |

## Files in this repository (SHA-256)

| File | SHA-256 |
|---|---|
| `proof/learning_justification/output/LEARNING_COVERAGE_THEOREM_EN.txt` | `60188d4be21d98b69113e8e82d7c591560ffed37e945e606f4503cc41db1e5c7` |
| `proof/learning_justification/output/GROUP_ENTRY_CLOCK_LEMMA_EN.txt` | `9b864429fe58b2558863624fb9b1f1e041e0e1c158a2886cb368b200d9449df7` |
| `proof/FUTURE_INVARIANCE_PROOF_EN.txt` | `3963381ec78c6dc0ee0fc10a6ecaf0bc1238e277b6f46dd82418ef0c77580e3c` |
| `proof/GLOBAL_THEOREM_AND_WORD_PRESERVATION_EN.txt` | `dcdbdb03937b80b5256212ecf8e221bd6b72b94ee2660764a09b39c31f1a7134` |
| `proof/STATUS.json` | `1d5149a5cb39d578313495fbcb1bb3bf63d6f01b5c32688e24b53c0c80607e96` |
| `proof/SHA256SUMS` | `027abed7abd37c70fd807d0ba8b8ffbb7376c00c888a072564203063f605eff2` |
| `results/campaign_identity.json` | `9b6fbd980c76110856f90ac7326d66af305c042df7f8a33c7db03d74fc22cdd4` |
| `results/campaign_summary.json` | `3cfc206b282247b6b4db3690ba799fe1a32faa0cbd9d747a1fdbf39f465e3fec` |
| `results/h1h2_layer18_lanes_1_4_8_11.json` | `3b5350f91eb5f8dde3bd836855fb7c95a0ff70afc50b0e9afc1cc88bb503b4c2` |
| `results/layers_cells_and_timings.json` | `423fec93e8865c8d98e8fda42d1b10cc78d65d85af907114ba5247d5f38e76bf` |
| `results/reference_A14_gain_boxes.json` | `e382fae8de2ce851c08106983e47e6550bdfe2c990601ea253fb9a502f6ccca4` |
| `results/v2_refusal_layer18_lane4.json` | `d5b45e245c0761d83950135eb2dc2d45260d71e38b79bd35e8f8e8a86522cf69` |
| `tools/verif_h1h2.py` | `bd13eff1458c7f7834834b6b7254d539325742eb92e1d963832eb9e5022fab0f` |
| `tools/bilan_campagne.py` | `f02aefc2b72d1c8e6ffe20e33ae9c4039a41ddf79eeb045246313c37c438a707` |
| `engine/SHA256SUMS` | `fab83b7418665fa53a8d60cbb526fcae758f3ee552b83fa8ce850e86192bd022` |
| `engine/PACKAGE_MANIFEST.json` | `5c7b1c005d2d404315801b5bb01a8e97f469cae36ca54ff8a08fe26070a37bf7` |
| `history/v3.2/A22_Affine_Fast_Start_v3_2_clean.zip` | `355ec62c581e3dfc970f45683bbe33436f9ba7d0084cd9ef49c260cd9335ee0b` |

`engine/SHA256SUMS` lists every file of the engine package; `proof/SHA256SUMS` lists every file of
the proof dossier (see `proof/OMITTED_IN_REPOSITORY.md` for the lines that refer to the omitted
program tree).

## Not included

The campaign outputs themselves (all `result.json` files, several hundred MB). The proof dossier's
`provenance_audit/output/` holds their authenticated audit (216 payloads, receipts and parent lineage)
and the exact terminal extraction used by the theorem. The full outputs can be attached to a Release.

## Previous campaign

The v3.2 campaign (run_id `872e032a…`, kernel_id `8f67e092…`, shared constants per cell) is documented in
`history/v3.2/HASHES_v3_2.md`, with its engine ZIP and summary.
