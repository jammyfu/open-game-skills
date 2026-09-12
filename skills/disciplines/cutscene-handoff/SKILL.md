---
name: cutscene-handoff
description: >
  How play gives the camera to a scene and takes it back. Use when skip
  drops the player in a wall, or when a scene steals a buffered special.
  Stacks on camera-shots and menu-flow.
---

# Cutscene handoff

Ask the column.

| Column | Player control |
|---|---|
| lock-watch | none, skip allowed |
| walk-and-talk | move only |
| fight-insert | short lock then combat |
| none | no authored scenes |

## Order

```
play → fade or hard cut → scene owns camera
skip / end → place actor on a marked nav point → restore look + verbs
```

Skip is a Menu job. It does not fire Primary.
Teach-only scenes follow tutorial-design: skip does not skip the verb test that lives in space.

## Iron rules

- Exit transform is authored. Never spawn inside collision.
- Buffered moves die on enter unless fight-insert says they persist.
- Audio-feel beds do not stack across the cut.
- A visual-only skip must not grant boss-clear flags (save-integrity).

## Accept

Skip lands on walkable ground with look restored. A combo started before the cut does not swing after.
