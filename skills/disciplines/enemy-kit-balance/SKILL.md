---
name: enemy-kit-balance
description: Each foe is a small moveset with tells, punish windows, and cooldowns. Ask poke-guard vs burst-duelist vs swarm-chaff vs artillery. Do not balance by shrinking player iframes or growing silent hitstun.
---

# Enemy kit balance

Ask the column:

| Column | Kit shape |
|---|---|
| poke-guard | short hits, long idle |
| burst-duelist | one big commit, long recover |
| swarm-chaff | weak, many, no armor |
| artillery | safe at range, weak up close |

## Budget (write these four numbers per move)

1. Telegraph / startup — must be readable.
2. Active — box on.
3. Recovery — punish window.
4. Cooldown / stamina — how soon it repeats.

Plus: damage, hitstun column, armor or none, range.

A kit gets **one** scary move. The rest are pokes or movement. Two unreactable heavies on one body is a bug unless the column is a raid-clock boss.

## How to tune instead of cheating

| Problem | Do | Do not |
|---|---|---|
| player dies too fast | cut damage or overlap | grow player hitstun |
| player never punished | lengthen recover or shorten armor | delete dodge-iframe |
| move unreadable | grow startup / add pose+sfx tell | add more HP |
| same move loops | add cooldown or a whiff punish | shrink input buffer |
| crowd is unfair | cap alive (spawn-wave) | give every chaff a grab |

HP and damage follow difficulty-design. Feel columns stay still. See balance-design rule 5.

## Tells

Startup must show on pose, audio, or a published wind-up. Juice-only red flash is not a tell if a11y flash-off is on.

Player punish: walk-in or a published light that fits inside recovery. If the player cannot complete a 2-hit confirm on a whiffed heavy, the recover is too short for that column.

## Accept

- Designer can name the scary move and its punish
- Two adjacent foes prefer different player answers (dodge vs poke vs close the gap)
- A patch note changes kit numbers, not the player's clock
