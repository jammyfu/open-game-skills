# Pack manifest contract (v1)

An asset pack is a folder (or zip) with a root `pack.json`. Packs contain assets and data only: no gameplay code. Any generator may produce one; nothing here is tied to a tool or franchise.

## Required keys

| Key | Meaning |
|---|---|
| `schema` | string `<vendor>.asset-pack/1`; the validator accepts any vendor prefix |
| `name`, `genre`, `version` | identity strings; `genre` is free text such as platformer, topdown-adventure, run-and-gun, kart, fighter |
| `rights` | `originality` (what is original), `third_party` (list; empty or each with source and licence), `licence` |
| `logical` | `tick_hz`, `unit` (for example px16), `coordinate_system`, `facing`, `actor_pivot` |
| `targetResolution` | string `WxH`, the display the pack is authored for (for example `1920x1080`); also repeated in `display.targetResolution` |
| `display` | `targetResolution` and `profiles{styleId: {virtualResolution, integerScale, tile_px, ...}}`; 3D styles use `{kind: "3d"}` |
| `styles[]` | `id`, `tile_px`, `filter` (nearest, linear or n/a), `art_root`, `virtual_resolution` (`WxH`), `integer_scale` (whole number); 3D styles carry `kind: "3d"` instead; optional `level_root`, `palette_limits` |
| `characters[]` | `id`, `role`, `forms{}` each with `animations[]` and `atlas{style: {atlas, png}}` |
| `levels[]` | `id`, `tmj` (per style) or another declared map format, `data`, optional `validation` |
| `assets` | paths to the asset catalog, animation tables, feel data and audio cue files |
| `files[]` | every shipped file with `path`, `bytes`, `sha256`, `role`; `pack.json` itself is not listed |
| `acceptance_status` | `engine_import`, `human_playtest`, `audio_perception`; unrun items say `not-run` |

Optional: `default_style`, `normalization` (canonical body per genre, identity-only fields), `skills_map[]`, `docs{}`, `engines{}`.

## Conventions the validator checks

- **Resolution**: every 2D style is a virtual canvas that integer-scales to `targetResolution` (`virtual_width * integer_scale == target_width`, same for height, scale a whole number, tile size divides the virtual width). Art, tiles, UI, fonts and parallax layers are authored at the profile's size; nothing is scaled by a fraction. Pixel profiles use nearest filtering.
- **Style map** (`styles.json`, schema `<vendor>.styles/1`, listed in `assets.styles_map`): `default_style`, `styles{id: kind...}` equal to the manifest styles, and `assets{key: {animations[], styles{id: {type, paths{...}, node?, clips?}}}}`. Every asset key has an entry in every style; every path exists; 2D entries name an atlas whose animations include the listed names; 3D entries point at a `.glb` whose nodes and animation clips include the declared `node` and `clips`. A pack with more than one style must ship this map. Switching style = changing one style id; gameplay data (levels, tile-unit hitboxes, tick tables, feel, entity ids, cue names) is shared by all styles.

- **Atlas JSON** (`*.atlas.json`): `image`, `size{w,h}`, `frames{name: {frame{x,y,w,h}, source_size, trim_offset, pivot_px, ticks, duration_ms}}`, `animations[{name, frames[], loop, ticks[]}]`, `logical_tick_hz`. Every `frame` rectangle lies inside the real PNG; every animation frame name exists; `ticks` has one positive integer per frame. Aseprite and TexturePacker JSON may sit beside it as engine-specific views.
- **Tiled maps** (`*.tmj`) and tilesets (`*.tsj`): tile layers have `width*height` entries; every gid is 0 or lies inside a referenced tileset; external tileset sources exist; each tile that needs semantics has a `type`. A separate collision layer carries gameplay collision, not colour.
- **Feel data** (`data/feel/*.json`): numeric entries carry `unit` and `source` (measured reference or original suggestion); derived outcomes are stored beside the constants.
- **Animation tables**: ticks are logical frames at `tick_hz`; sheet fps only swaps pictures.
- **No code**: no scripts, shaders or binaries beyond images and audio.

## Folder to skill map (defaults when `skills_map` is absent)

| Folder or file | Skill |
|---|---|
| `catalog/asset-manifest.json` | sprite-catalog |
| atlas JSON, tileset files | sprite-atlas |
| `styles.json`, `data/display.json` | asset-pack-intake with the engine adapter |
| animation tables | pixel-animation |
| `art-bible.md` | art-bible |
| feel data | platform-jump, jump-leniency, racing-feel, action-feel |
| boxes and enemy tables | hitbox-hurtbox, attack-tell, boss-design |
| level data and maps | level-design, level-blockout, level-teach, moving-platform |
| audio cue files | audio-feel |
| `engines/<engine>/` | the matching engine adapter |
