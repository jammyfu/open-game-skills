---
name: world-streaming
description: Use when worlds need incremental loading, fast travel reaches missing collision, boundary crossings thrash memory, or unloaded cells respawn collected objects.
---

# World streaming

## Scope

Own cell residency and activation, not generation algorithms or GPU resource disposal. [Asset runtime](../asset-runtime/SKILL.md) owns leases; [save-systems](../save-systems/SKILL.md) owns durable state. Cell coordinates are not asset IDs or entity identity.

## Modes

| Mode | Residency driver |
|---|---|
| region-gated | explicit doors or region transitions |
| distance-cells | streaming sources and load/unload ranges |
| portal-rooms | room/portal connectivity and visibility requirements |

## Procedure

1. Identify streaming sources, world/cell versions, residency budgets and dependencies. Plan prefetch for the authored maximum speed and measured load latency; radius alone does not guarantee readiness. Multiple sources share cells. Pinned quest or moving entities need explicit ownership.
2. Separate requested, data-ready, collision-ready, navigation-ready and active states; require only the gates relevant to that cell. Define one activation authority and epoch. Rendered scenery is not evidence that floor collision or interaction state is ready.
3. Use unload hysteresis and a bounded work queue to avoid edge thrashing. Prioritize essential collision/data before optional presentation. If budget/readiness cannot keep up, apply a published safe barrier, transition screen or reduced traversal policy, not an invisible floor or silent time dilation.
4. Fast travel first prepares and validates the destination, then commits the actor transfer. Keep the source recoverable until success. Cancellation/failed loads must leave one valid location. Invalidate stale requests; do not activate an abandoned destination when its load completes later.
5. Persist versioned edit/collection deltas before safe eviction, or pin dirty cells until the save policy resolves failure. Transfer cross-cell entities atomically under stable IDs. Never recreate a collected reward solely because a cell loaded again; do not discard unsaved state to meet a memory target.
6. Release cell leases, not every resource in the scene graph. Track resident versus active cells, queue backlog, peak usage and activation latency on the target. Coordinate destruction/rebuild of collider/navigation proxies with the simulation boundary.

## Outputs

Adapt the [streaming contract](assets/contract.example.json): sources, gates, budgets, hysteresis, dirty-cell policy, entity ownership, failure recovery and a residency trace. State the supported fast-travel/speed envelope and remaining device limits.

## Acceptance

Cross an edge repeatedly at maximum authored speed; teleport into an initially absent region; cancel a transfer; collect an item then evict/reload its cell. Verify no missing floor, duplicate entity/reward or unbounded churn. [Cases](assets/evals.json) remain not-run until measured; finite samples do not certify an unlimited world.

## References

[Unreal World Partition](https://dev.epicgames.com/documentation/unreal-engine/world-partition-in-unreal-engine) illustrates streaming sources, loaded versus activated cells and destination preloading. Bind to the actual engine/version; this skill is not a World Partition replacement.
