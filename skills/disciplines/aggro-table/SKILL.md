---
name: aggro-table
description: Generic threat. Who the AI hits. Stack with enemy-ai and party-follow.
---

# Aggro table

Ask: nearest | damage-table | scripted | none.
Nearest is default. A table adds damage and heal weights. Scripted locks a phase target (`boss-design`).
Dropping aggro on death or stealth (`stealth-info`) is published. Do not snap to a companion behind a wall (`party-follow`).

Accept: two players can say why the boss turned. A stealth drop is visible on the AI state, not only the music.
