# Pack manifest contract (v1)

An asset pack is a folder (or zip) with a root `pack.json`. Packs contain assets and data only: no gameplay code. Any generator may produce one; nothing here is tied to a tool or franchise.

## Required keys

| Key | Meaning |
|---|---|
| `schema` | string `<vendor>.asset-pack/1`; the validator accepts any vendor prefix |
| `name`, `genre`, `version` | identity strings; `genre` is free text such as platformer, topdown-adventure, run-and-gun, kart, fighter |
| `rights` | `originality` (what is original), `third_party` (list; empty or each with source and licence), `licence` |
| `logical` | `tick_hz`, `unit` (for example px16), `coordinate_system`, `facing`, `actor_pivot` |
| `styles[]` | `id`, `tile_px`, `filter` (nearest or linear), `art_root`; optional `level_root`, `native_screen`, `palette_limits` |
| `characters[]` | `id`, `role`, `forms{}` each with `animations[]` and `atlas{style: {atlas, png}}` |
| `levels[]` | `id`, `tmj` (per style) or another declared map format, `data`, optional `validation` |
| `assets` | paths to the asset catalog, animation tables, feel data and audio cue files |
| `files[]` | every shipped file with `path`, `bytes`, `sha256`, `role`; `pack.json` itself is not listed |
| `acceptance_status` | `engine_import`, `human_playtest`, `audio_perception`; unrun items say `not-run` |

Optional: `normalization` (canonical body per genre, identity-only fields), `skills_map[]`, `docs{}`, `engines{}`.

## Conventions the validator checks

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
| animation tables | pixel-animation |
| `art-bible.md` | art-bible |
| feel data | platform-jump, jump-leniency, racing-feel, action-feel |
| boxes and enemy tables | hitbox-hurtbox, attack-tell, boss-design |
| level data and maps | level-design, level-blockout, level-teach, moving-platform |
| audio cue files | audio-feel |
| `engines/<engine>/` | the matching engine adapter |
