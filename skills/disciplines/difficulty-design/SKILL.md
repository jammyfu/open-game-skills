---
name: difficulty-design
description: Engine-neutral difficulty — space, resources, then numbers. Use for curves, gates, scaling policy, optional walls, and avoiding HP-only inflation.
---

# Difficulty Design

Ask the scaling policy first. Then build the curve. Numbers come last.

## Three layers (always this order)

1. **Space** — terrain, vision cuts, weather, stamina/resource gates, verticality.
2. **Resources** — ammo, food, slots, tool wear. A loadout wipe is a *level rule*, not a stat.
3. **Numbers** — HP, damage, count, tell length. Use to confirm the space, not to replace it.

Raising only `hp *= 1.08` makes fights longer. It does not make them harder.

## Scaling policy (pick one)

| Policy | What grows | Map sentence |
|---|---|---|
| region-tier | The place has a rank | "This valley is dangerous" |
| kill-rank | Variants upgrade from kill points | Same camp, tougher hide |
| player-level-sync | World tracks the hero | Region identity fades |
| honest-fixed | Nothing scales | Mastery is the curve |
| hunt-rank | Quest/hunt rank | Rank is selected before the hunt; no silent mid-hunt scaling |
| session-DDA | Hidden adjust from deaths/accuracy | Flow, easy to feel like cheating |

Default for exploration games: **region-tier** or **kill-rank**. Use player-level-sync only if the user asked for an RPG.

## Curve shape (pick one per act)

- staircase wave: teach → test → twist → rest
- ramp: slow climb
- brick wall: optional elite, not a story gate unless you mean it
- flat: challenge is spatial/resource, numbers stay put

Main path may be easier than optional content.

## Tells

If a move can one-shot, its tell is *longer*, not shorter. Readable windup is difficulty you can learn. Invisible damage is not.

## Accept

A player who learned the verbs can point at a failure and say which layer beat them (cliff, empty bag, or number). Two visits to the same geometry can change variants under kill-rank; the geometry itself does not morph to match a level.
