---
name: crafting-loop
description: Use when recipes, stations, fusion, cooking, schematics, or material transforms can consume the wrong inputs, grant twice, overflow inventory, hide requirements, or duplicate another progression system.
---

# Crafting Loop

This skill owns **recipe identity and the atomic transform from validated inputs to outputs**. `inventory-economy` owns containment/overflow, `equipment-progression` owns gear progression state, and `durability-economy` owns wear/repair condition.

## Modes

| Mode | Transform context |
|---|---|
| hand-craft | direct recipe transform without a required station |
| station-craft | recipe additionally requires an authored station/context |
| fuse-two | authored input instances transform into an output |
| cook-buff | ingredients transform into a consumable/timed result |
| schematic-unlock | recipe availability depends on an authored unlock |

Gathering, vendors, discovery and experimentation may support crafting, but none is universally required. A quest-specific recipe is valid when intentionally authored and recoverable.

## Recipe and transaction contract

Every recipe has a stable recipe ID, version/schema, required input definitions/quantities, optional context requirements and declared output(s). Localized names are presentation, not save identity.

Craft execution is one transaction:
1. validate recipe/version/context and all inputs;
2. reserve or atomically consume inputs;
3. create/update outputs exactly once;
4. hand outputs to `inventory-economy` using its overflow policy;
5. commit a stable transaction ID so retry/duplicate callbacks are idempotent.

On failure or interruption, either nothing commits or a documented resumable state is restored. Never silently consume inputs with no output/evidence.

Craft duration, queueing, walk-away behavior and station UI are project choices. Long-running jobs need inspectable state if they persist across scene/session boundaries.

## Acceptance

Test exact resources, one-missing input, full inventory, duplicate submit/callback, interruption between consume/output, save/reload of a persistent job and recipe migration. Resource totals reconcile and one transaction ID produces at most one committed transform.
