---
name: aim-assist
description: Use when raw look or aim input needs an explicit, bounded assist transform such as friction, rotation or magnetism with stable profile/target identity and evidence that does not alter hit geometry or damage truth.
---

# Aim assist

Ask: `off | friction | rotation | magnet`.

## Ownership

`aim-assist` transforms **aim intent**. Target eligibility/visibility comes from the project's targeting/perception owner; `projectile-hitscan` resolves the shot; hitboxes and damage stay with their owners. Assist never enlarges hit geometry or rewrites a resolved hit.

## Contract

Publish:
- stable `assist_profile_id` and revision
- input class/profile
- candidate/selected `target_id` when applicable
- raw aim vector/angle
- assisted aim vector/angle
- bounded strength/cone/friction parameters from project data
- acquire/retain/drop reason

Mouse, stick, gyro or accessibility profiles may use different authored values. ADS/hip values are project data, not universal relative speeds.

## Runtime rules

1. Candidate changes use deterministic project tie-break/hysteresis rather than render iteration order.
2. A stale or no-longer-eligible target is dropped before a new assist result is committed.
3. Accessibility variants may widen or strengthen assist only through an explicit profile; they still do not modify damage, collision or target health.
4. Presentation reticles may visualize the selected target but are not the source of target truth.
5. Replay evidence records profile revision, raw intent, assisted intent and selected target ID.

## Acceptance

Given the same raw aim, candidate set, target state and assist-profile revision, the same assisted intent is produced. Disabling assist changes only that transform; the same authoritative shot query still owns hit/no-hit resolution.
