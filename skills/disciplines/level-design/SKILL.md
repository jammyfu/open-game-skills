---
name: level-design
description: Use when rooms, hubs, overworld pockets, dungeons, or set pieces lack readable spatial choices, pacing, gating, landmarks, or measurable traversal structure before art polish.
---

# Level Design

This skill owns **spatial structure, pacing, gating, and navigation intent**. `level-blockout` owns greybox implementation; `level-teach` owns spatial teaching beats; `world-map` owns map UI.

## Modes

| Mode | Spatial emphasis |
|---|---|
| open-air | multiple routes, long sightlines, landmark navigation |
| room-gate | room sequence and authored gates |
| hub-spoke | safe hub with selectable spokes and returns |
| linear-setpiece | controlled pacing along a constrained route |

## Spatial contract

Write project metrics before decoration: traversal speeds, jump/climb reach, corridor/door widths, encounter footprint, camera clearance, sightline targets, checkpoint spacing, and any accessibility constraints that materially shape space.

Gates are explicit data: soft/resource, hard/key-or-ability, optional challenge, narrative/state, or project-specific variants. A gate should communicate why traversal is blocked through space, feedback, UI, or narrative according to the chosen presentation; invisible blockers are allowed only when the project deliberately uses them and validation supports the choice.

Decision density, rest spacing and landmark frequency are measured from the intended experience. Do not turn a heuristic such as “one decision every N seconds” into a universal law.

## Acceptance

Run representative routes without final art. Record path choice points, traversal time, gate reasons, dead ends, sightlines and recovery routes. Verify metrics against `locomotion`/`platform-jump` and observe players through `gameplay-validation`. A pretty screenshot or map overlay alone is not level-design evidence.
