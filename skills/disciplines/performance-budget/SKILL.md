---
name: performance-budget
description: >
  Engine-neutral frame and memory budget. Measure first. Never drop the
  logical clock to fake weight. Use when a build stutters, hitch-loads,
  or ships different feel per platform by accident.
---

# Performance budget

Ask the target column first.

| Column | Frame goal | Notes |
|---|---|---|
| lock-60 | 16.6 ms render + 16.6 ms logic | default for action / race / fight |
| lock-30 | 33.3 ms render, logic still 60 | last resort on handheld |
| adaptive-res | keep logic 60, scale pixels | prefer this over dropping tick |
| cinematic-uncapped | cutscenes only | never for gameplay clocks |

Logic tick and render fps are different clocks. Hitstop, input, physics, boost, and race ranking stay on the logic clock.

## Measure before cutting

Order: hitch (frame-time spikes) → average GPU → average CPU → memory → disk/IO.
A 20 ms spike on a camera cut is a stream/load bug, not an LOD problem.

Publish a budget table. Numbers move with the platform column; the *shape* does not:

```
CPU main     ≤ 8 ms
CPU jobs     ≤ 6 ms
GPU          ≤ 13 ms @ target res
GC / alloc   0 in combat / race / duel
Main mem     cap per platform column
IO hitch     0 during input-heavy scenes
```

## Levers (cheap → expensive)

1. Resolution scale / dynamic res
2. Shadow, reflection, particle caps
3. LOD distances and impostors
4. Object pooling (VFX, shells, pickups, items)
5. Streaming bounds — no load during boost / swing / drift
6. Bake what does not move
7. Cut overlapping post-process

Do not start by rewriting the renderer.

## Iron rules

- Gameplay does not run only at render rate if a fixed step exists.
- Do not hide hitch by slowing timeScale.
- Pool before spawning 200 decals a swing.
- Profile on the lowest shipped column, not the dev tower.
- Quality sliders map to the budget table. They do not invent a second combat clock.

## Accept

One minute of combat or race on the lowest column holds the frame goal with no hitch on camera cuts. Feel is identical at 60 and 30 render because logic did not move. Memory does not climb across three encounters.
