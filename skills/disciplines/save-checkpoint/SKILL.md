---
name: save-checkpoint
description: When the run is allowed to persist. Ask auto-region vs bonfire-commit vs sleep-anywhere vs roguelike-run. Death policy is a column, not a moral stance.
---

# Save and checkpoint

Ask the column:

| Column | Persist |
|---|---|
| auto-region | entering a region or rest writes |
| bonfire-commit | player chooses a sit, world may reset |
| sleep-anywhere | player writes when idle and safe |
| roguelike-run | only meta progress persists |
| suspend-sku | platform suspend is a full save |

## Rules

1. The player must be able to name when the last write happened.
2. A hardcore wipe is opt-in, never the silent default.
3. Mid-boss checkpoints are data. Soft-lock after a wipe with a spent key is a bug.
4. Platform suspend (handheld-dock) stacks with this skill. See platform-targets.
5. Cloud vs local is a target concern, not a design column.

## Accept

- Quitting from the pause menu does not drop an unsaved 20-minute fight unless the column is roguelike-run and that was published
- A death returns the player to a place they recognize
