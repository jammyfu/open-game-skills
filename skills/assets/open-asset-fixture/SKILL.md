---
name: open-asset-fixture
description: Use when game tests need reusable 2D sprites, 3D models, animations, sound, music, particle textures, native effects, PBR maps or HDRIs, or when missing assets are blocking reproducible fixtures.
---

# Open asset fixture

Match the **test requirement**, not merely the appearance. Prefer suitable existing assets over paid downloads or generation. This is fixture sourcing, not an instruction to replace deliberately commissioned artwork.

## Modes

| Mode | Use |
|---|---|
| library-first | Revalidate provided local locks, then discover suitable open-licensed candidates |
| pinned-only | Use only matching, byte-verified local locks; missing input blocks CI |

## Ownership

Own source selection, license/edition records, fixture identity and byte-integrity checks. Import belongs to the asset/engine skill; execution to `gameplay-harness`; validation claims to `gameplay-validation`. A source page, valid hash or completed plan does not prove decoding, dependency completeness, gameplay correctness or legal authenticity.

## Procedure

1. Read the test's required kind, format and capabilities. Static geometry cannot replace a rig; a particle bitmap cannot prove native effect playback. For pure logic or exact negative cases, prefer synthetic state/geometry. Do not require artwork unnecessarily.
2. Run [preparation](scripts/prepare_assets.py) for the active skill. Profiles are examples, not universal requirements. For unprofiled tests, use an explicit [request](assets/request.example.json) with [the matcher](scripts/asset_fixture.py). `query` is a soft lexical preference; `requires` and formats are hard filters. Keep unmatched requirements visible; never silently relax them.
3. Reuse matching verified local locks first. Otherwise select from the [curated catalog](assets/catalog.json) using the [source guide](reference/sources.md). Default to CC0. CC-BY-3.0/4.0 needs explicit attribution opt-in and retained creator/license/change records. Unknown, restricted, share-alike and paid entries are not automatic fallbacks; route separately for review. CC0 is not a trademark/personality-rights guarantee.
4. Acquire only selected files through available authorized download tools or official APIs. Recheck the exact edition and terms; free Standard is not Pro/Source. Respect service conditions independently of asset licenses, including API attribution, authentication and rate limits. No bulk catalog scrape, paywall bypass or preview substitution. If downloads are unavailable, return a plan and mark acquisition blocked.
5. Inspect selected files and dependencies in a safe importer, then [pin](scripts/fixture_lock.py) them using the [pin request](assets/pin.request.example.json). Preserve original bytes and license evidence. Mixed-format fixtures need `capability_formats` when format-specific capabilities matter. Never execute downloaded scripts or enable embedded Blender/SVG code. Label transformed/negative-test copies and retain their original hashes.
6. Revalidate locks before import. Run the target test with fixture ID, build, importer version and output evidence. Record import/engine/human checks separately. Generation is last for uncovered requirements, not a way to hide missing evidence.

## Commands

From this skill's directory (or use absolute script paths):

```sh
python3 scripts/prepare_assets.py --skill materials
python3 scripts/asset_fixture.py match --request assets/request.example.json
python3 scripts/fixture_lock.py --root /absolute/fixture-dir pin --request /absolute/pin.json --output /absolute/fixture.lock.json
python3 scripts/prepare_assets.py --skill juice-vfx --root /absolute/fixture-dir --locks /absolute/fixture.lock.json --pinned-only
```

See [usage and exit/status meanings](reference/usage.md). A `needs-acquisition` plan is not ready; `ready-for-import` is still not an engine pass.

## Acceptance

Normal: reuse an intact compatible lock ahead of a remote candidate. Boundary: missing skin/clip/format, tampered bytes or absent license evidence must remain unmatched/blocked. Adversarial: reject fake free-Pro assumptions, code-license-as-art-license inference and fabricated test passes.

`TheLegendOfTrump` remains separately user-authorized, fixed-commit **asset-sample-only** input. Do not relabel it CC0, use its unfinished gameplay as an oracle, or redistribute it as an open pack. Its existing fixture record remains unchanged.
