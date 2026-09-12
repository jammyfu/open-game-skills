---
name: gameplay-capture
description: Honest gameplay recording. Label real challenge vs debug vs feature demo. Use before publishing a clear or a trailer.
---

# Gameplay capture

## Trigger

You need a clip of a move, an enemy answer, a full route, or a store trailer.

## Inputs / columns

Ask: real-challenge | feature-demo | debug-stage.
Need: build id, difficulty, loadout, whether debug is on, device, input method.

## Flow

1. Name the column on the slate. A debug teleport is never a real-challenge.
2. Shot list: the verb, the enemy answer, the actual result.
3. Preflight: picture, sound, resolution, save folder, browser session stable.
4. Pause the game and pause the recorder as two buttons. Land takes in parts.
5. Wait out loads and fades. Keep the source take. A cut or speed-up is labeled on the edit.

## Constraints

Altered unlock flags → label **challenge clip with altered unlocks**, not a natural ending.
Automation failures (lock flip, navmesh, lost session) are capture-setup, not difficulty proof (`gameplay-validation`).

## Output

Playable file + slate + note of cuts.

## Accept

The file plays, has sound, and the timeline matches the slate. An ending or difficulty claim has a frame that shows it.

## Cases

`docs/cases/playtest-lessons.md`
