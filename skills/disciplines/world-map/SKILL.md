---
name: world-map
description: Use when a game needs a map information policy with stable regions and markers, discovery provenance, travel-node visibility, or different map presets without letting the UI become authoritative world state.
---

# World map

Choose or define an information policy. Examples may include open-air, metroidvania, hub-spoke, blank-chart, radar-hud, or a project-specific policy. They are presets, not universal laws.

## Ownership

The world, quest, and travel systems own source truth. `world-map` owns how authorized information is revealed, represented, and persisted. A marker presentation change must not mutate the underlying quest, object, or travel-node state.

## Stable information model

Every map object uses stable IDs:
- `region_id`
- `marker_id`
- `source_owner`
- `visibility_predicate`
- discovery/reveal provenance
- optional `travel_node_id`
- map/fog revision

Separate geometry/topography, discovered chart data, icons/pins, and travel affordances when the project needs those layers. Their visibility is project policy, not an automatic four-layer requirement.

Player-pin capacity, landmark density, height/readability rules, and how long the player can travel without opening the map are project parameters, not fixed values.

## Runtime rules

1. Reveal/discovery operations are idempotent by stable ID.
2. Loading an old save maps known IDs through explicit migration; translated labels are never identity.
3. Fog/recon changes publish a revision so map and minimap can reject stale presentation.
4. Information appears only when its source visibility predicate resolves true.
5. World-space guidance and pause-map guidance may differ without changing world truth.

## Acceptance

Given the same world/quest/travel state and information-policy revision, the map resolves the same authorized regions, markers, and travel nodes. Turning map presentation off does not alter world state, and an unrecognized or stale marker remains non-authoritative rather than becoming a new objective.
