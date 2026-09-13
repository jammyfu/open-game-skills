---
name: lock-on-target
description: Use when a character needs soft or hard target locking with stable target/session identity, deterministic candidate selection, retention/drop rules and explicit consumers for facing, attacks, HUD and camera.
---

# Lock-on target

Ask: `soft-lock | hard-lock | none`.

## Ownership

`lock-on-target` owns selected target identity and lock lifecycle. Target eligibility comes from authoritative target/perception state. Camera, facing, attack aim and HUD may consume the selected target according to their own modes; they are not required to share identical behavior in every project.

## Contract

Publish:
- stable `lock_session_id`
- selected `target_id`
- candidate-set / targeting revision
- acquire/retain/switch/drop reason
- authored ranking, tie-break and hysteresis policy
- consumer policy for camera/facing/attack/HUD

Cycle input is a semantic action from `input-design`; mouse/stick bindings are not hardcoded here.

## Runtime rules

1. Candidate ordering is deterministic for equal scores.
2. Visibility, range, state or other eligibility changes are evaluated from the targeting owner, not from the lock pip.
3. A stale target revision cannot restore a dropped target.
4. Switching produces one new selected target per committed request; duplicate cycle requests are idempotent when they share request identity.
5. Camera assistance still obeys camera ownership/collision; lock selection never bypasses `camera-anti-clip`.

## Acceptance

Given the same candidate revision, actor state and switch request, the same target is selected or no target is returned. HUD/camera presentation can change independently without changing target identity, and a removed/ineligible target cannot persist as a ghost lock.
