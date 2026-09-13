# Asset-first test preparation

The scripts use Python 3.10+ and only its standard library. They run offline and do not invoke an image model, download tool, game, decoder or importer. Run the commands below from the repository root; for a copied installation use the absolute path to the installed skill's `scripts/` directory.

## 1. Prepare inputs for an active skill

```sh
python3 skills/assets/open-asset-fixture/scripts/prepare_assets.py --skill materials
python3 skills/assets/open-asset-fixture/scripts/prepare_assets.py --skill animation-blend audio-feel juice-vfx
```

These profiles cover representative integration tests, not every test for those skills. A purely mathematical camera test can use synthetic geometry even though a camera import test may benefit from a model. A skill without a curated profile returns `needs-requirements`; the tool never selects random art.

Generate a report covering every registered skill:

```sh
python3 skills/assets/open-asset-fixture/scripts/prepare_assets.py --all-skills skills/catalog.json --output asset-plan.json
```

The report retains every skill in the denominator. Unknown requirements are blocked, not passed. The report file is exclusively created; choose a new path or explicitly manage the old file. This command can exit 2 while still producing a useful report. Do not upload private paths or full downloaded packs with that report.

## 2. Match an explicit test requirement

Copy and adjust [the request example](../assets/request.example.json), then run:

```sh
python3 skills/assets/open-asset-fixture/scripts/asset_fixture.py match --request /absolute/request.json
```

`kinds` is an any-of list. `requires` is an all-of list of required capabilities. `formats` is an any-of list of accepted lowercase formats; empty means format is not yet constrained, not that every format was verified. `query` is a soft lexical preference with a small Chinese synonym map, not an image-similarity model. Put indispensable properties in `requires`, and inspect files before use. Unsupported requirements stay `unmatched`.

A skinned animation requirement can use:

```json
{"kinds":["animation","model"],"requires":["skeletal-animation"],"formats":["glb","gltf"],"query":"humanoid locomotion","limit":3}
```

A static object from the same pack is not an animated fixture. The catalog records pack-level leads, not exact animation names, skin counts or decoder results. Request specific clip/rig requirements separately rather than assuming the whole pack qualifies.

## 3. Acquire and inspect the chosen files

Use the primary links in [sources](sources.md). Acquisition is handled by an available authorized download tool or by the operator. The Python scripts do not scrape websites, bypass login, download paid tiers, extract archives or run an external game. If the environment cannot retrieve a binary, keep the candidate plan and report acquisition as blocked.

For every selected member, retain creator, source, edition/release or commit, download URL, license evidence and original bytes. Resolve required textures, buffers and sound/effect dependencies. Record importer/decoder version, observed units/axes, alpha, channels, sample rate, clip names and skeleton information as appropriate. Unverified properties must not become claimed capabilities. Safe import settings must disable embedded scripts and unwanted external resources.

Do not replace a current fixture by a newer release behind the same URL. Inspect the change, pin a new identity and rerun the affected cases. CC0 asset rights do not cancel API attribution/authentication/usage conditions.

## 4. Pin a reviewed local selection

Modify [the pin example](../assets/pin.request.example.json) with paths relative to the explicit fixture root and an actual inspection note:

```sh
python3 skills/assets/open-asset-fixture/scripts/fixture_lock.py --root /absolute/fixtures pin --request /absolute/pin.json --output /absolute/fixture.lock.json
python3 skills/assets/open-asset-fixture/scripts/fixture_lock.py --root /absolute/fixtures verify --lock /absolute/fixture.lock.json
```

The tool hashes data and license evidence; it does not judge the legal authenticity of the evidence. It rejects symlinks, traversal, archives, executable extensions, empty files and oversized input. The total default hash budget is 128 MiB. No original files are modified. A lock is not overwritten automatically.

For a mixed-format selection, associate capabilities with the actual inspected format:

```json
{
  "kinds": ["model", "animation"],
  "capabilities": ["skeletal-animation"],
  "formats": ["obj", "glb"],
  "capability_formats": {"skeletal-animation": ["glb"]}
}
```

Without that association, a request for a specific format plus capabilities will not reuse an ambiguous multi-format lock. Even a valid format association does not prove every same-format member qualifies; isolate the smallest target asset/dependency set and inspect it.

## 5. Reuse locks before fetching anything else

```sh
python3 skills/assets/open-asset-fixture/scripts/prepare_assets.py --skill juice-vfx --root /absolute/fixtures --locks /absolute/fixture.lock.json --pinned-only
```

Local byte-verified matches come before remote candidates; ties use license policy, lexical relevance, then stable IDs. A tampered lock is recorded in `invalid_locks` and is not reused. Offline CI uses `--pinned-only`: no download or generation fallback. Run the actual import and game scenario only after preparation requirements are satisfied.

| Preparation status | Meaning |
|---|---|
| `not-needed` | The default regression profile uses synthetic state instead of art |
| `needs-requirements` | No curated test profile; supply actual requirements |
| `needs-acquisition` | Candidate metadata matched; bytes have not been prepared |
| `ready-for-import` | Suitable local bytes and metadata were revalidated; import still needs testing |
| `blocked` | Required inputs are absent/incompatible under the requested policy |

`prepare_assets.py` exits 0 for a complete plan (which can still need acquisition), 2 for blocked/unspecified requirements, and 1 for invalid input or I/O failure. Use `--pinned-only` as the CI availability gate. `runtime_validation` and `decoding_validation` remain `not-run` in these tools; a generated plan is never an engine test result.

## Donor-project boundary

The separately authorized `TheLegendOfTrump` fixture is not part of the CC0 catalog and is not handled by this open-license lock registry. Its existing fixed-commit manifest is the source of scope. Only permitted models, images, textures and audio may be used; its unfinished gameplay, tests and implementation are not correctness evidence. Keep the two provenance paths separate rather than changing the project's license classification.
