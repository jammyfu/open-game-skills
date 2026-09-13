---
name: skill-tree
description: Use when a progression graph unlocks verbs, modifiers or capabilities and the project needs stable node identity, prerequisites, cost transactions, respec rules and migration-safe revisions.
---

# Skill tree

Ask the graph model: linear, branch, web, loadout-grid, hybrid, or existing.

## Contract

Publish:
- stable `tree_id` and tree revision
- stable `node_id` for every node
- versioned `prerequisite graph`
- cost/resource references and unlock effects
- respec/refund policy
- persistence/migration behavior
- evidence for locked/unlocked boundary states

## Ownership

This skill owns progression graph eligibility and unlock transaction intent. Currency/inventory owners settle costs, gameplay skills own the unlocked effects, and save systems own persistence bytes.

## Rules

1. A node may unlock verbs, modifiers, recipes, permissions, slots or other authored effects; no single node type is universal.
2. Spend plus unlock is atomic from the player's perspective: failure cannot consume cost without the corresponding committed node state.
3. Duplicate unlock requests for the same transaction/node identity are idempotent.
4. Prerequisite evaluation uses stable node IDs and revision, never UI position or translated names.
5. Tree revisions include migration rules so existing profiles are not silently invalidated.

## Acceptance

Given the same `tree_id`, revision, resource state and unlock request, the same eligibility and committed node result occurs. A reviewer can identify prerequisites, cost owner, effect owner and refund/respec behavior.
