---
name: training-dummy
description: Use when an existing integration requests the legacy training-dummy entry or its dummy-block, record-replay, frame-display, or off modes and must map them to the canonical practice-room owner.
---

# Training dummy compatibility entry

This is a **compatibility entry**. [training-mode](../training-mode/SKILL.md) owns the practice-room contract, dummy state, record/replay, reset policy and training evidence.

## Legacy mapping

| Legacy mode | Canonical request |
|---|---|
| dummy-block | `training-mode`: dummy-block |
| record-replay | `training-mode`: dummy-record |
| frame-display | `training-mode` with frame/input display enabled by project data |
| off | no training-mode runtime behavior requested |

Preserve the live combat owners (`action-feel`, `hitbox-hurtbox`, `hitstun-recover`, etc.). Do not evolve cancel windows, hitboxes, dummy AI, reset behavior or frame formulas here.

## Accept

The legacy request resolves to `training-mode` plus the same live gameplay contracts; this alias adds no second training ruleset.
