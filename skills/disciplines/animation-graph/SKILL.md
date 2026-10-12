---
name: animation-graph
description: Use when multiple animation states, clips, layers, masks or requests compete for a character pose and need deterministic selection/composition tied to authoritative gameplay state without creating another gameplay clock.
---

# Animation graph

This skill owns the animation **state/layer composition graph**. It consumes gameplay state/events; it does not own attack legality, hit timing, movement decisions or global time.

## Compatible columns

`loco-base` | `overlay-attack` | `hit-react` | `cinematic`

They describe common layer/request roles and may be composed according to project data.

## Request/layer contract

Each animation request declares an ID, source gameplay state/event, layer/mask, priority or blend rule, weight/lifetime/end condition, root-motion contribution policy and interruption/transition rule.

Multiple clips may legitimately contribute to the **same bone channel through weighted blending**. Determinism comes from explicit layer/mask/weight/priority rules, not from banning overlap.

## Rules

1. Authoritative **gameplay state** decides which requests are valid; an animation completing cannot invent a new attack or cancel by itself.
2. Layers/masks/weights are presentation composition. Stable ordering/tie rules are explicit where multiple requests compete.
3. Hitstop/pause may freeze or hold an animation phase according to the project presentation policy; do not assume an engine-specific skeleton `timeScale` API or freeze the world ticker.
4. Root motion and locomotion/physics have one published displacement application path; extraction from blended clips must not double-move the body.
5. 2D skeletal tracks follow the same ownership principle: layered composition is allowed and named rather than mapped to one universal track layout.
6. IK/post-process systems consume the composed pose after graph evaluation unless the project explicitly defines another pipeline.

## Accept

For transition, interruption, overlapping-layer and pause/hitstop cases, log valid request IDs, layers/masks/weights and displacement owner. Reordering unrelated containers does not change selected logical animation requests, and animation presentation cannot change gameplay legality.

## Retargeted clip handoff

Consume [character-rig's retarget record](../../assets/character-rig/reference/retarget-protocol.md) when source clips change. Preserve its root policy and clip identity through graph composition; test loop wrap, interruption and collision-resolved displacement. This graph owns composition, not a second skeleton mapping or displacement integrator.
