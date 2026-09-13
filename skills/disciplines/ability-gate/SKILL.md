---
name: ability-gate
description: Use when access depends on a capability, story predicate, or both, and the project needs a stable gate identity, deterministic predicate evaluation, unlock migration, and explicit soft-lock/recovery evidence.
---

# Ability gate

Ask: `none | tool-gate | story-flag | both`.

## Ownership

The gate consumes capability/story state from their true owners. It does not own tutorials, map pins, save storage or rest-site placement.

## Contract

Each gate publishes:
- stable `gate_id`
- required capability IDs and/or story predicate IDs
- predicate version
- open/closed/blocked result
- optional authored feedback/reference IDs

Evaluate the gate from authoritative state. Duplicate unlock notifications are idempotent. A save or patch migration preserves stable capability/story identity rather than keying by localized text or scene index.

Soft-lock policy is project-specific: the project may require an exit, recovery point, alternate route, or intentionally irreversible commitment. Do not force every hard gate to have a rest site or every ability lesson to be nonlethal.

## Acceptance

For one predicate version and authoritative state, the gate resolves deterministically. Gaining or losing relevant capability state updates only gates that depend on it, stale notifications cannot override a newer result, and a blocked player can identify the missing authored requirement without the gate inventing world truth.
