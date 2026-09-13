---
name: overwatch-fire
description: Use when an actor reserves a lane, cone or authored reaction region and needs deterministic trigger eligibility, stable overwatch-session/event identity, resource consumption and one authoritative ranged action when a valid target event occurs.
---

# Overwatch fire

Ask: `cone-hold | suppress-lane | none`.

## Ownership

`overwatch-fire` owns reaction readiness and trigger selection. `target-priority`/team/filter systems supply target eligibility, `projectile-hitscan` resolves the resulting shot, and `stealth-info` may present authorized threat information.

## Contract

Publish:
- stable `overwatch_session_id`
- reaction-region ID/revision
- eligible target/filter policy
- trigger event/request ID
- authored priority/tie-break when multiple targets qualify
- resource/cooldown/action owner state
- resulting shot/action request ID

Do not assume the first render callback inside a cone is the winner. Entry, visibility, movement, attack, or another project event may trigger overwatch according to authored policy.

## Runtime rules

1. One trigger event consumes readiness at most once.
2. Multiple eligible targets resolve deterministically from project priority/tie-break data.
3. Occlusion and team/friendly rules come from authoritative filtering/perception data; threat visualization is not target truth.
4. Interrupt/cancel/death/state-change invalidates stale trigger events before firing.
5. The actual projectile/hitscan result remains with `projectile-hitscan`.

## Acceptance

Given the same session, region revision, eligibility state and trigger events, the same reaction request is selected or none is fired. Replayed or duplicated trigger callbacks cannot spend readiness or emit the same shot twice.
