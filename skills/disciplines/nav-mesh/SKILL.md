---
name: nav-mesh
description: Use when AI or companion pathfinding needs an explicit traversability graph, agent profile, dynamic obstacle update, or reproducible path/no-path evidence. It owns navigation data, not physics collision or world rules.
---

# Nav mesh

Ask: `baked-static | dynamic-carve | off`.

## Ownership

`nav-mesh` owns agent traversability, path requests, authored traversal links, and nav revisions. Physics/collision stays with the engine or `collision-layers`; hazards stay `hazard-volume`; door/quest truth stays with its gameplay owner.

## Contract

For every navigation profile publish:
- `agent_profile_id`
- radius / height / step / slope limits
- movement capabilities such as walk, jump-link, climb-link, swim-link
- current `nav_revision`

For every path request publish `request_id`, start/end, profile, nav revision, result and first failure reason.

Static geometry may be baked. Runtime changes may use carving, tiled rebuilds, authored links, or another engine-supported update strategy. **Opening a door does not universally require a full rebuild.** Update only the connectivity representation the project actually uses.

A gap is traversable only when the selected agent profile and authored traversal data say so. Do not globally mark all jump gaps unreachable.

## Runtime rules

1. Path queries read one coherent nav revision.
2. Dynamic obstacle updates publish a new revision before new queries use it.
3. Stale path results are rejected or revalidated after a relevant revision change.
4. Off-mesh/traversal links have stable IDs and explicit entry/exit conditions.
5. A stuck agent records nav revision, path ID, position and movement capability before attribution.

## Acceptance

For the same nav revision, agent profile and endpoints, the project returns the same canonical path/no-path result. Opening/closing a dynamic passage changes connectivity only according to the configured update strategy, and a failed path names the blocking reason rather than being treated as difficulty evidence.
