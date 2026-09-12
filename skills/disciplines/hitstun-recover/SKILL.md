---
name: hitstun-recover
description: >
  How long the victim cannot act after a hit. Distinct from hitstop.
  Use when combos never drop, when a jab knocks down, or when an enemy
  attack has no punish. Stacks on action-feel and combo-design.
---

# Hitstun / recover

Hitstop freezes both colliding clocks. Hitstun is the *victim's* locked pose after the freeze ends. Do not collapse the two numbers.

Ask the column.

| Column | Light hitstun | Heavy | Knockdown |
|---|---|---|---|
| footsie-tight | 10–14f | 16–22f | rare, on dedicated moves |
| brawler-juggle | 12–18f | launch table | combo owner is air state |
| souls-poise | short unless stance breaks | hyperarmor eats lights | death or down, not juggle |
| hit-and-run | very short | knockback > stun | space is the punish |

Numbers are starting bands at 60 logic. Tune to the column, not to a franchise frame chart.

## Stack

```
hit confirmed
  → hitstop N (both clocks)
  → victim hitstun H, attacker recover R
  → advantage = H - R   (after freeze)
```

If H ≤ R on every light, confirms do not exist.
If H ≫ R on every jab, the opponent never takes a turn.
Blockstun is a second pair (Hb, Rb). A blocked poke should not equal a hit confirm unless the column is brawler-juggle.

## Iron rules

- Publish H and R on the move row next to damage. Juice length does not author stun.
- Wakeup / knockdown recovery is its own row (okizeme is a column, default off).
- Hitstun decay on long strings lives in combo-design. Infinite stun is a bug.
- Enemies use the same units. A boss may have *poise* (souls-poise), not secret 0-stun.
- Training-mode must display advantage after hit and after block.

## Accept

A jab leaves a small plus or minus that a lab dummy can show. A heavy that looks slow is minus on block. The player can act on the first frame after H.
