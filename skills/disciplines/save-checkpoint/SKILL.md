---
name: save-checkpoint
description: Use when a game needs explicit checkpoint timing, respawn anchors or run-persistence policy while storage integrity, cloud conflict and bytes remain owned elsewhere.
---

# Save checkpoint

Ask the policy: auto, authored-rest, manual-safe, run-boundary, suspend, hybrid, or existing.

## Contract

Publish:
- stable `checkpoint_policy_id` and revision
- checkpoint/anchor IDs and eligibility predicates
- write trigger and respawn selection policy
- pending/committed checkpoint state
- interaction with run/death policy
- evidence for quit/load/retry behavior

## Ownership

This skill decides **when and where** progression is checkpointed. `save-systems` owns atomic serialization/migration, `save-integrity` owns trust/recovery, and `cloud-save` owns remote revision/conflict behavior.

## Rules

1. Checkpoint timing and loss window are project policy; no universal duration is acceptable or unacceptable.
2. A checkpoint becomes authoritative only after the owning save transaction commits successfully.
3. Duplicate trigger callbacks with the same checkpoint request identity do not create multiple writes or advance twice.
4. Respawn/death carry uses stable checkpoint identity, not scene array order or UI labels.
5. Suspend can request a checkpoint or separate suspend snapshot according to platform/project policy.

## Acceptance

A reviewer can identify the active checkpoint policy/revision, last committed checkpoint ID, pending write state and respawn selection. Local/cloud/storage failures are attributed to their owning save systems rather than silently changing checkpoint rules.
