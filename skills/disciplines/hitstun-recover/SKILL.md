---
name: hitstun-recover
description: How long the victim cannot act after a hit. Hitstop freezes two clocks. Hitstun is only the victim. Ask light-stun vs knockdown vs juggle vs none. Tune so a punish exists and a combo still ends.
---

# Hitstun and recover

Ask the column:

| Column | After the hit |
|---|---|
| none | flinch pose only |
| light-stun | short no-act, then turn |
| knockdown | downed + wakeup |
| juggle | air state until ground |

Hitstop ≠ hitstun. Hitstop is the freeze on both colliding ActorClocks (`action-feel`). Hitstun starts when that freeze hits 0.

## Numbers are data, not a franchise

Write on the attack: hitstop, hitstun, blockstun, knockdown time, wakeup invuln.
A starting band at 60 Hz (change per column):

- light poke: hitstop 6-10f, hitstun 10-16f
- medium: hitstop 10-14f, hitstun 16-24f
- heavy / launcher: hitstop 12-20f, hitstun or launch 24-40f
- wakeup: 4-10f invuln then punishable

If hitstun ≥ attacker recovery + walk-in, the victim never gets a turn. That is only legal on a published combo column with an ender.

## Rules

1. Same logic frame as pose, box, and SFX.
2. Blockstun is shorter than hitstun unless the column is guard-crush.
3. Armor / hyper-armor cuts or ignores hitstun. Publish which moves have it. See enemy-kit-balance.
4. Status freeze is not hitstun. See status-ailment.
5. Do not balance an enemy by secretly growing player hitstun. Patch the enemy kit.

## Accept

A light hit lets the victim block or walk before the next heavy. A dropped combo returns turn inside published recovery. Turning juice off does not change the counts.
