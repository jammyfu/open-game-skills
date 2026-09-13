# Open game asset sources and test suitability

Primary pages checked 2026-09-13. Recheck terms at acquisition. "Open" here refers to asset licenses; CC0 assets are not necessarily editable source projects, and free downloads are not automatically openly licensed. No binaries, paid packs, credentials or site preview images are bundled.

## Preferred sources

| Source | Use in tests | License and acquisition boundary |
|---|---|---|
| [Kenney](https://kenney.nl/assets) | 2D tiles/sprites, UI glyphs, low-poly scenes, sound effects, particle textures | Asset-page files are CC0; [support/license FAQ](https://kenney.nl/support) distinguishes assets from the reserved logo. Individual packs can be downloaded free; the convenience bundle is not required. |
| [Quaternius](https://quaternius.com) | Animated low-poly actors, environments and humanoid animation | Check the exact pack/edition. [Universal Animation Library](https://quaternius.itch.io/universal-animation-library) has a free Standard subset and paid Pro/Source editions; the [author's Standard upload](https://opengameart.org/content/universal-animation-library) distinguishes the subset from the full library. Required clips and root-motion variants need file inspection. |
| [Poly Haven](https://polyhaven.com/license) | PBR surfaces and HDRI lighting; photorealistic models when appropriate | Assets are CC0. [Live API terms](https://polyhaven.com/our-api) separately require visible source credit and a unique User-Agent. No blanket permission to scrape website content or copy preview renders. Prefer official file metadata and bounded selected variants. |
| [ambientCG](https://docs.ambientcg.com/license/) | PBR maps, paving/ground/material tests | Downloadable assets and its own material previews are CC0. Use [official API documentation](https://docs.ambientcg.com/api/) or individual downloads. A 1K smoke fixture is a default budget choice, not adequate proof of high-resolution behavior. |
| [OpenGameArt](https://opengameart.org/node/5571) | Author-published sprite, sound and music packs | Licenses are per submission, sometimes multi-licensed; choose and record one applicable license. [FAQ](https://opengameart.org/node/5571) warns that previews may be differently licensed. A CC0 collection title is not proof for each member. |
| [Game-icons.net](https://game-icons.net/faq.html) | Inventory/HUD SVG and PNG icons | Usually CC-BY-3.0; record the individual creator and edits. The initial opt-in entry is [Lorc's Heart bottle](https://game-icons.net/1x1/lorc/heart-bottle.html). SVG requires sanitization; it is not trusted executable content. |
| [Effekseer](https://effekseer.github.io/Help_Tool/en/overview.html) | Actual effect data and textures when native VFX-runtime integration is the test | Official overview distinguishes MIT runtime from CC0 bundled texture/effect data. Pin the [official release](https://effekseer.github.io/en/download.html); verify individual data and dependencies. Do not generalize this license to third-party effects. Kenney textures are simpler for billboard/alpha tests and do not prove native Effekseer support. |
| [Freesound](https://freesound.org/help/faq/#licenses) | Long-tail environmental/foley recordings after individual review | Per-sound CC0, CC-BY or CC-BY-NC and some older licenses. Not in default auto-select catalog. [API terms](https://freesound.org/docs/api/terms_of_use.html) separate commercial API use from sound licenses; [authentication](https://freesound.org/docs/api/authentication.html) requires credentials and some actions OAuth2. Do not bypass login or quotas. |

## Concrete seed candidates

The machine-readable [catalog](../assets/catalog.json) contains stable local IDs, primary URLs, edition, observed formats and inspection notes. Its capabilities are **pack-level discovery hints**, not file measurements. Empty formats means unknown. Matching may identify a pack whose particular file still fails the required import or clip test.

| Test input | Reviewed creator entry | Suggested inspection |
|---|---|---|
| Modern 2D platformer | [New Platformer Pack](https://kenney.nl/assets/new-platformer-pack) | Actual state frames, alpha, sprite anchors and sheets |
| Pixel sheet | [Platformer Art: Pixel Redux](https://opengameart.org/content/platformer-art-pixel-redux) | Slice dimensions/margins; do not invent an atlas manifest |
| Top-down pixels | [Tiny Dungeon](https://kenney.nl/assets/tiny-dungeon) | 16-pixel tile scale, seams and sampling |
| Controls | [Input Prompts](https://kenney.nl/assets/input-prompts) | Device glyph mapping and locale changes; no font redistribution here |
| Particle billboards | [Particle Pack](https://kenney.nl/assets/particle-pack) | Alpha/blend mode and texture boundaries |
| Smoke/explosion | [Smoke Particles](https://kenney.nl/assets/smoke-particles) | Pick the right texture; do not infer an animation sequence |
| Light cookies | [Light Masks](https://kenney.nl/assets/light-masks) | Color space, sampling and light-mask support |
| UI audio | [Interface Sounds](https://kenney.nl/assets/interface-sounds) / [author's OGG listing](https://opengameart.org/content/interface-sounds) | Decode, event identity, focus/resume and duplicate playback |
| Foley | [Impact Sounds](https://kenney.nl/assets/impact-sounds) | Selected collision sample, channels and level |
| Retro laser audio | [Digital Audio](https://kenney.nl/assets/digital-audio) | Actual codec, channels and clip duration |
| 3D platform blocks | [Platformer Kit](https://kenney.nl/assets/platformer-kit) | Real units, axes, pivots and independent collision proxies |
| Static environment | [Nature Kit](https://kenney.nl/assets/nature-kit) | Draw/instance tests; not skinning evidence |
| Animated platformer | [Platformer Game Kit](https://quaternius.com/packs/ultimateplatformer.html) | Select character rather than static prop; inspect skin and clips |
| Animated creatures | [Ultimate Monsters](https://quaternius.com/packs/ultimatemonsters.html) | Bone mapping, skin weights, animation and bounds |
| Humanoid animation | [Universal Animation Library Standard](https://quaternius.itch.io/universal-animation-library) | Free subset only; no promise of every advertised animation or Blend source |
| Environment light | [Kloppenheim 06 Pure Sky](https://polyhaven.com/a/kloppenheim_06_puresky) | HDR/EXR decoder, dynamic range and projection |
| PBR concrete | [Concrete Floor 01](https://polyhaven.com/a/concrete_floor_01) | Normal GL/DX, roughness and channel packing |
| PBR paving | [Paving Stones 036](https://ambientcg.com/view?id=PavingStones036) | Scale/tiling and chosen file resolution |
| Retro audio events | [512 Sound Effects](https://opengameart.org/content/512-sound-effects-8-bit-style) | Only this free CC0 submission, not linked paid collections |
| Music-loop tests | [5 Chiptunes](https://opengameart.org/content/5-chiptunes-action) | Decoded loop boundary; not an input-timing oracle |
| Attributed UI | [Heart bottle](https://game-icons.net/1x1/lorc/heart-bottle.html) | Author/license credit and SVG sanitization |
| Native effect data | [Effekseer official downloads](https://effekseer.github.io/en/download.html) | Runtime compatibility, data version and all referenced textures |

## Selection policy and reproducibility

The matcher never fetches data. It filters by kind, required features, known accepted format, free edition and license; among matches it orders by CC0, query token overlap, access friction and stable ID. Relevance is lexical (including a small Chinese synonym map), not perceptual similarity, legal assurance or benchmark evidence. An unusual style in the query is a preference, while `requires` is a hard capability requirement.

Reuse a verified local lock before discovery when its requirements still match. Obtain only the minimum selected files through an authorized download tool; keep the original license evidence, URLs, creator, edition, check date, hashes and transformation log. Resolve external glTF buffers/textures and effect dependencies explicitly. No wildcard whole-library fetches or automatic archive execution. CI should be offline and use a pinned fixture or label missing inputs `blocked`, not silently download a different version.

For generic save/RNG/transaction logic, synthetic data is usually a better fixture than art. For failure-injection tests (bad alpha, absent texture, missing bone, invalid sound), derive a labeled test copy while preserving the pristine original and its hash. A parse failure expected by a negative test is not a production-asset defect.

Do not assume a repository's MIT code license covers its art. TheLegendOfTrump stays user-authorized, fixed-SHA, asset-only input under its separate fixture policy; do not relabel it CC0, redistribute it as an open pack or reuse its unfinished gameplay implementation. None of this is a grant to train a model on third-party content.
