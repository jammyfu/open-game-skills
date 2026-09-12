---
name: attack-tell
description: >
  Readable startup. Use when a swipe kills with no pose, when a red flash
  replaces animation, or when juice is the only warning. Stacks on
  enemy-kit and hitstun-recover.
---

# Attack tell

Ask the column.

| Column | What the player sees |
|---|---|
| pose-only | windup silhouette is enough |
| pose-audio | pose + one locked sound |
| marked-aoe | floor / beam mark before active |
| color-flash | extra flash — never the only channel |

One-shot and grab tells default to marked-aoe or pose-audio. Pokes may be pose-only.

## Clock

Tell frames = startup on the move row. The tell must be on screen before active.
A flash that starts on the same frame as the hitbox is not a tell.
Juice-vfx may accent the tell. It may not *be* the tell.

## Iron rules

- Color-safe: shape + audio, not red-only (a11y-controls).
- Camera must keep the tell in frame (camera-shots / lock-on). Off-screen one-shots are a camera bug.
- Player and enemy use the same rule: if the player has a 4f jab with no pose, enemies do not get a 4f wipe.
- Training-mode can freeze on the last startup frame.

## Accept

A first death to that move, the player can point at the pose that meant "move". Sound off still reads marked-aoe.
