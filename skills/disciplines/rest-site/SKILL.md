---
name: rest-site
description: Generic rest / bonfire / bench. Heal, save, maybe respawn foes. Not a free win.
---

# Rest site

Ask: heal-only | heal-and-save | heal-save-repop | off.
Rest writes `save-checkpoint`. Difficulty flags do not flip (`debug-slate`).
Repop is a column. If on, nearby trash returns; bosses stay dead unless the column says so.
Sitting is a published window. Hits during sit use the current combat column.

Accept: the player can rest, quit, reload, and stand at the same site with the same unlocks.
