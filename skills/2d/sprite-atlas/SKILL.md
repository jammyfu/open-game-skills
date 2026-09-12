---
name: sprite-atlas
description: Full 2D image set for a game. Sheets, tiles, UI, portraits, projectiles. Image 2.5 generates plates. Boxes stay in other skills.
---

# Sprite atlas

Ask: char-cycle | tileset | ui-kit | portrait | projectile | prop.
Generate one family per image. Style lock `art-bible`. Timing `pixel-animation`. Paint `sprite-skin`. VFX plates `vfx-generate`. Hurtboxes never come from the PNG.

## Families (generate these; do not invent a folder per pose)

| Family | Typical plates |
|---|---|
| char-cycle | idle, walk, run, jump, fall, land, crouch, climb, swim, dash |
| combat-pose | attack-light, attack-heavy, hurt, death, block, parry, charge |
| facing | 4-dir or 8-dir of the same cycle; east may be a flip |
| companion | same cycle, slimmer set |
| enemy | idle, walk, telegraph, attack, hurt, death |
| projectile | bullet, arrow, magic bolt, bomb, plus empty shell |
| weapon-overlay | sword/gun layer aligned to sockets |
| tileset | floor, wall, platform, slope, water, hazard, door, ladder |
| prop | chest, crate, torch, plant, breakable |
| pickup | coin, heart, key, ammo, weapon drop |
| ui-kit | button 4-state, panel, frame, cursor, slider |
| hud-icon | hp, mp, stamina, status, item, quest pin |
| portrait | bust, talk blink, emotion row |
| shadow | blob or contact shadow, separate layer |
| vehicle | hull + wheel or mount cycle |
| background | sky, parallax far/mid, fog plate |
| vfx | route to vfx-generate columns |

## Image 2.5 contract

1. Name the artefact: "N-frame sprite sheet in one row" or "tileset grid 8x8".
2. Even cell size. Same pivot. Flat chroma or transparent.
3. Neutral pose first. Do not bake VFX into walk.
4. No readable UI words unless this family is ui-kit and the words are specified.
5. One facing per sheet unless asked for a turnaround.

Accept: a walker sheet slices without re-aligning feet. Combat poses do not change hitstop (`juice-vfx`).
