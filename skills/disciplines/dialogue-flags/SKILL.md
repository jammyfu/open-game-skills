---
name: dialogue-flags
description: Branching lines as flags, not a second quest graph. Use for 对话分支, 选项, 旗帜.
---

# Dialogue flags

Ask first: flavor-only, flag-alters-shop, or flag-alters-gate?

Rules: flags live beside `quest-graph`, they do not replace it. A line that teaches a verb still needs the next-minute test (`tutorial-design`). Skip and language follow `cutscene-handoff` and `game-localization`. Flags do not change hitstop.

Accept: the player can replay and see the other line. A flag never silently deletes a required verb.
