---
name: parry-guard
description: Use when blocking or parrying needs explicit input windows, guard arcs, chip/guard-break rules, and deterministic same-tick interaction with incoming attacks.
---

# Parry and guard

Choose the defense model:

| Column | Input |
|---|---|
| hold-block | held state with published damage/reaction rules |
| tap-parry | short authored success window |
| both | held guard plus an explicit parry window |
| none | no guard/parry mechanic |

## Rules

1. Guard/parry windows use the same published logical clock as combat.
2. Contact eligibility is evaluated at the contact tick before applying reaction effects; same-tick attack/defense transitions follow the project's declared priority rule.
3. Chip, chip-kill, guard damage, guard break and stamina cost are explicit data or explicitly absent.
4. Guard direction uses a published arc/facing rule. Do not universally make “back attacks” unblockable; the selected arc decides.
5. A successful parry causes authored logical states/reactions, not only a flash or sound.
6. Focus loss or device reset cannot leave a synthetic held-block input stuck.

Invulnerability belongs to `dodge-iframe`; persistent poise belongs to `poise-stagger`.

## Accept

Test contacts one tick before, at both parry boundaries and one tick after, including simultaneous attack/guard transitions and multiple attack classes. Reversing actor iteration order must not change the outcome. The debug view shows guard arc, window and resulting logical state without relying on juice.
