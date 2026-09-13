---
name: hyper-armor
description: Use when specific move windows should ignore or alter selected hit reactions without owning a persistent poise meter or globally pausing combat.
---

# Hyper armor

Persistent poise belongs to `poise-stagger`. This skill owns move-local armor.

| Column | Reaction rule |
|---|---|
| none | no armor override |
| armor-frames | published logical interval ignores selected reactions |
| super-armor-once | one eligible contact consumes the armor |
| armor-count | authored number of eligible contacts before armor ends |

## Rules

1. Publish which reaction classes armor suppresses and which still apply: damage, hitstop, knockback, status, grabs/throws and guard effects are independent decisions.
2. Grab/throw interaction is data, not a universal “throws always beat armor” rule.
3. Armor interval/count is tied to the logical move state, not animation playback time.
4. Consuming armor has a stable hit/contact identity so one overlap cannot consume multiple charges accidentally.
5. Visual tells communicate armor but do not create immunity.

## Accept

Test one tick before/inside/after armor, every relevant attack class, multi-hit overlap and same-tick contacts. Confirm the published damage/hitstop/reaction split and armor-count consumption. A visually armored pose outside the logical interval receives normal reaction.
