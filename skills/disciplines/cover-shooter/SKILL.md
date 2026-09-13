---
name: cover-shooter
description: Use when an actor enters, occupies, peeks, fires from, and exits authored cover and needs one cover-session state machine with explicit interruption and ownership handoff.
---

# Cover shooter

Ask: `stick-cover | tap-cover | soft-cover`.

## Ownership

`cover-shooter` owns the actor's cover-session state. `cover-space` owns valid anchors/capabilities; `projectile-hitscan` owns shots; `aim-assist` / `fps-feel` own aim/handling; `input-design` owns bindings.

## Contract

Publish:
- stable `cover_session_id`
- actor ID and `cover_anchor_id` + revision
- state: enter / attached / peek / fire / exit / aborted
- movement-control owner
- authored transition/cancel conditions
- optional stance/fire-side selected from anchor capabilities

Exactly one system owns the actor's cover locomotion at a time. Duplicate enter/exit requests for one session are idempotent. Cover state does not imply invulnerability unless another gameplay rule explicitly grants it.

Blind/peek fire produces a normal shot request with declared origin/direction/handling state; it does not maintain a second shooting truth.

## Acceptance

If the anchor becomes stale, blocked, destroyed, or the actor is interrupted, the session exits or re-resolves without leaving two movement owners. Firing from cover produces one authoritative shot path through `projectile-hitscan`, and exiting cover cannot replay a stale fire input.
