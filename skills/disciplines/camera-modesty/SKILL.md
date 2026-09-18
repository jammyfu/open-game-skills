---
name: camera-modesty
description: Use when a camera pose, boom-sweep sample or close-up may invade private body zones and the project needs a default-modest dignity framing policy.
---

# Camera modesty

This skill owns **modesty / dignity framing policy**. It rejects or clamps camera poses that invade private body zones. `camera-shots` owns presentation grammar; `camera-anti-clip` owns collision; `fov-comfort` owns comfort and accessibility FOV. Gameplay targeting stays with owners such as `lock-on-target`.

## Modes

| Mode | Work |
|---|---|
| modest | default; reject or clamp invasive framing |
| adult | project opt-in; each pose still needs matching `authored_intent` |
| medical-exam | project opt-in clinical/exam framing; each pose still needs matching `authored_intent` |

A mode may not be inferred from genre, studio name or a cinematic label. Absent an explicit opt-in, use `modest`.

## Contract

Publish policy mode, camera pose IDs, character proxy/landmarks, private-zone class, violated rule IDs and a suggested clamp (raise pitch, pull back, raise boom). Neighboring camera owners remain loaded only when the active phase needs them.

Run the offline checker [modesty_check.py](scripts/modesty_check.py) against the [v1 framing contract](reference/framing-contract.md). `pass` is static pose/proxy evidence only; engine, render and human review remain `not-run`.

## Rules

1. Default policy is modest. `adult` and `medical-exam` never apply from a global flag alone; the pose must carry a matching `authored_intent`.
2. Treat below-hem, between-legs, extreme upward look under a character, near-plane contact with a private zone, and close/high-FOV occupancy of groin or chest as invasive unless that pose is an explicit opt-in.
3. Collision-safe or grammatically valid shots can still fail this policy. Do not “fix” a modesty fail by deleting collision, changing FOV comfort bounds or rewriting shot grammar.
4. Character proxies are AABB or capsule declarations plus optional hem/hip/chest landmarks. They are not a body mesh, clothing sim or medical diagnosis.
5. Boom-sweep sample batches, if provided, are evaluated per sample. One violating sample fails the sweep.
6. Suggested clamps are conservative static hints (raise pitch / pull back / raise boom), not an auto-applied camera solve and not a collision sweep.

## Outputs

Deliver a pass/fail report with pose IDs, violated rule IDs, suggested clamp, input/tool SHA-256 and explicit `runtime_validation: not-run`. Preserve authored adult or medical-exam intent when the project opted in; do not silently reclassify it as modest, and do not silently treat modest content as adult.

## Acceptance

Normal: an orbit-third pose that stays above the hem and outside private-zone zoom limits records `pass` for this static check. Boundary: a boom-sweep batch that includes one low under-hem sample fails that pose/sweep and returns a clamp hint; `adult` or `medical-exam` without matching pose intent stays modest. Adversarial: a request to skip the check because the shot is “cinematic,” or to fold this policy into collision or shot grammar, is not approved.

This skill occupies one specialized slot. Keep the three-skill-plus-one-engine phase limit; defer `camera-shots`, `camera-anti-clip` and `fov-comfort` unless the same phase must also change those owners.
