---
name: pixel-animation
description: Use when sprite animation disagrees with attack timing, hitstop skips cells, pixel-art clips need an explicit gameplay-frame mapping, or pixel foliage needs stepped wind motion.
---

# Pixel animation

A hitbox is the attack volume; a hurtbox is the vulnerable volume. Do not switch vulnerability on only because a slash is active. Author each volume independently on the gameplay timeline; sprites illustrate those decisions.

## Implementation

Map each cell to a pose and a positive duration in logical ticks. A cell may last several ticks; sheet FPS is not the simulation frequency. Publish startup, active and recovery intervals independently of presentation blends. The visible contact pose must agree with the active hitbox on the same gameplay tick.

Hitstop holds the current pose for the affected actor. Input sampling continues under [action-feel](../../disciplines/action-feel/SKILL.md). Smears and palette swaps do not change active intervals, vulnerability or invulnerability unless explicitly authored as gameplay data.

## Accept

Step through the attack with both volumes visible: startup and recovery have the declared hurtboxes, and the attack hitbox is active only in its interval. Hold a cell for multiple ticks without producing duplicate hits. Change render FPS and confirm the logical contact tick is unchanged. Hitstop resumes the held pose without skipping to idle.

## Environmental pixel motion

For tree and bush wind, use the [foliage workflow](reference/tree-wind.md). Keep environmental presentation independent of combat timing. Reuse the project wind service when present. Request a source sprite or generate an explicitly labeled visual prototype, then validate layer reconstruction and motion in the target renderer.

For uneven pixels, blurry movement or fractional window scaling, apply the [pixel-grid contract](reference/pixel-grid.md) before authoring more animation frames.
