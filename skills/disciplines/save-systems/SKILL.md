---
name: save-systems
description: Slots, schema version, and who may write. Ask single-slot vs three-slot vs cloud-merge. Checkpoints say when. Integrity says which file may lie. This skill says the file shape.
---

# Save systems

Ask the column:

| Column | Shape |
|---|---|
| single-slot | one file, confirm overwrite |
| three-slot | player picks 1–3 |
| cloud-merge | local vs cloud prompt |

Stacks with [save-checkpoint](../save-checkpoint/SKILL.md) (when) and [save-integrity](../save-integrity/SKILL.md) (which file may cheat).

## Rules

1. Header has schema version. Old files migrate or refuse, they do not silently drop flags.
2. Dialogue-flags and quest-graph write through this header. No second save format.
3. Load does not respawn elites the player already killed unless the checkpoint column says the room resets.
4. Cutscene mid-file: load returns to the published handoff point, not inside a locked camera.
5. Corrupt bytes go to cert-handoff / save-corrupt. Other slots stay.

## Accept

A v1 file on a v2 build either migrates or says why not. Slot 2 cannot clobber slot 1. Load after a cutscene gives the stick back.
