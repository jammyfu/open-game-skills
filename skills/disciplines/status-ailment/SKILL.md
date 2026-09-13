---
name: status-ailment
description: Use when burn, poison, slow, stun, silence, buffs/debuffs or other actor statuses need stable instance identity, stacking, ticking/timebase, cleanse, expiry and gameplay-effect ownership.
---

# Status ailment

## Compatible modes

`none` | `timed-dot` | `crowd-control` | `mixed`

## Status instance contract

Each applied effect gets a stable **status instance ID** or deterministic key and publishes status type/source, magnitude, **stack** policy, duration/expiry, tick policy and declared **timebase**, affected gameplay properties, cleanse/dispel categories and end reason.

## Stack policy examples

`replace` | `refresh-duration` | `add-duration` | `add-stack-to-cap` | `independent-instances` | project-defined

The project chooses per status; do not infer stacking from repeated callbacks.

## Rules

1. Tick/duration timebase is explicit and defines pause/hitstop/slow/suspend behavior; statuses do not automatically use the combat logic clock.
2. Crowd-control/action denial routes to the authoritative movement/action/input-state owners through named effects rather than freezing arbitrary presentation systems.
3. Re-applying, cleansing and expiring are idempotent by status identity; duplicate network callbacks cannot double a tick or cleanse unrelated instances.
4. `cleanse` specifies target categories/instances and resulting legal state; presentation/HUD follows status events and is not the source of truth.
5. Chain/lock behavior is project balance data with explicit immunity/diminishing/escape policy where desired; do not mandate one universal anti-lock rule.

## Accept

Replay exact-boundary apply/tick/stack/refresh/cleanse/expiry plus duplicate callback and pause/timebase cases. Status instance IDs explain every resulting property/state change and end reason.
