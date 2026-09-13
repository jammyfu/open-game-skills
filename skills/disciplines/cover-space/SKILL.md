---
name: cover-space
description: Use when level geometry needs explicit cover affordances, stable anchors, stance/peek capabilities, occupancy and clearance evidence. It owns cover-space data, not input bindings, shooting, or the actor's cover state machine.
---

# Cover space

Ask: `geometry-only | stick-cover | none`.

## Ownership

`cover-space` owns authored/queryable cover affordances. `cover-shooter` consumes them for actor state transitions; `projectile-hitscan` owns shot resolution; `input-design` / `kb-mouse-map` own actions and bindings.

## Contract

Each cover affordance publishes:
- stable `cover_anchor_id`
- source geometry/collision revision
- supported stance/peek/fire-side capabilities
- usable approach/exit regions
- clearance and occupancy policy
- optional neighbor/link IDs

High/low, blind-fire, lean, vault or other capabilities are project data. Do not infer them only from rendered mesh height.

## Runtime rules

1. A cover query returns anchor ID + revision + capabilities.
2. Streaming/destruction/geometry changes invalidate or revise affected anchors.
3. Occupancy is explicit where required; two actors cannot silently claim an exclusive slot.
4. Input keys and mouse buttons never live in this skill.
5. Cover affordance does not grant invulnerability, alter health, or resolve shots.

## Acceptance

For one geometry revision and actor capability profile, the same query resolves the same valid cover anchors. A stale or blocked anchor is rejected before attachment, and cover presentation cannot make non-cover geometry authoritative.
