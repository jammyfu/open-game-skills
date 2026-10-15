---
name: asset-pack-intake
description: Use when a project receives a pre-built genre asset pack (sprite atlases, tilesets, level maps, feel/animation/audio data) described by a pack manifest and must validate it, map every folder to the owning skill, and plan the engine build without editing the art.
---

# Asset pack intake

Own **accepting an external asset pack as input**: validate its manifest and files, map each folder to the skill that owns it, and hand the build a phase plan. Do not generate, repaint, repack or edit the art, and do not become a second owner of atlas packing, animation playback, level design or feel tuning.

## Modes

| Mode | Output |
|---|---|
| validate | integrity and consistency report with pass / fail / blocked / not-run per check |
| plan | phase plan for the chosen engine and art style, at most three specialised skills plus one engine per phase |
| import-check | record of the actual engine import and what it loaded, kept separate from `validate` |

## Procedure

1. Resolve engine, version, target resolution and one art style from the user or project; ask at most one question if the engine or style is unknown. A pack may ship several styles; use exactly one art root per build.
2. Read the [manifest contract](reference/pack-manifest.md). Run [validate_pack.py](scripts/validate_pack.py) on the pack root. It checks hashes, referenced paths, atlas rectangles against real PNG sizes, animation tables, Tiled map layers and tile ids, feel provenance, rights fields and that no executable code ships in the pack. It never decodes pixels, runs an engine or judges art.
3. Map folders with the manifest's `skills_map`; if absent use the table in the contract. [sprite-catalog](../../2d/sprite-catalog/SKILL.md) reads the asset manifest, [sprite-atlas](../../2d/sprite-atlas/SKILL.md) owns atlas and tileset import, [pixel-animation](../../2d/pixel-animation/SKILL.md) owns tick-based playback, [platform-jump](../../disciplines/platform-jump/SKILL.md) / [racing-feel](../../disciplines/racing-feel/SKILL.md) / [action-feel](../../disciplines/action-feel/SKILL.md) own feel tables, [level-design](../../disciplines/level-design/SKILL.md) and [level-blockout](../../disciplines/level-blockout/SKILL.md) own levels, [art-bible](../art-bible/SKILL.md) owns palette lock, [audio-feel](../../disciplines/audio-feel/SKILL.md) owns cue mapping.
4. Respect the pack's declared rules. If `normalization` says characters are re-proportioned to one canonical body per genre, character swaps are cosmetic: gameplay must not read a character's height, build or motion style, and hitboxes come from the data files, never from sprite alpha. Feel is per genre, not per character.
5. Keep statuses honest. Rows stay `draft` until imported in the target engine; a packed atlas is not an import, an import is not a playthrough, and a debug-assisted run is not a natural clear. A generated beatability proof is tool-level evidence under the stated assumptions only.
6. Emit the plan: the validated style and files, unresolved gaps, deferred phases, and the engine adapter's import notes ([godot](../../engines/godot/SKILL.md), [phaser](../../engines/phaser/SKILL.md), [unity](../../engines/unity/SKILL.md), [custom](../../engines/custom/SKILL.md)). Hand other engines the same data through the custom adapter.

## Output

Intake report (checks, evidence, assumptions), skill mapping, chosen style root, phase plan, DEFER list, and a record of build/commit, configuration, scenario, driver and result for every check that ran.

## Accept

A pack with a missing file, a changed hash, an atlas rectangle outside its PNG, a map tile id past the tileset, an animation without frames, feel numbers without provenance or a shipped script reports `fail` and blocks the plan. A pack that passes `validate` still reports engine import, playthrough and audio perception as `not-run` until evidence exists. Re-running on the same bytes gives the same report.
