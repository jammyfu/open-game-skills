---
name: party-follow
description: Use when AI companions follow, form up, split, catch up or recover around a leader and the project needs stable companion identity, navigation ownership and explicit recovery behavior.
---

# Party follow

Ask the follow model: leash, formation, combat-split, independent, off, or existing.

## Contract

Publish:
- stable `party_id` and party revision
- stable leader and `follower_id` values
- formation/follow target state
- locomotion/navigation owner references
- separation thresholds and `recovery policy`
- catch-up/warp/respawn rules if supported
- transition/request identity

## Ownership

This skill owns companion follow-state selection and recovery intent. Locomotion, nav/pathfinding, targeting and combat remain in their owning systems.

## Rules

1. Follower movement parameters are project/actor data; companions are not universally slower or identical to the leader.
2. Catch-up may wait, repath, warp, respawn, regroup or remain separated according to policy; no universal timer or teleport rule.
3. Recovery decisions use stable follower/party state and deterministic tie rules, not render/list order.
4. A repeated recovery request is idempotent and cannot warp/rebind a follower twice.
5. Path failures remain navigation evidence until controlled reproduction attributes another owner.

## Acceptance

Given the same `party_id`, revision, follower state and recovery request, the same follow/recovery decision occurs. A reviewer can separate follow policy from locomotion, navigation, targeting and presentation.
