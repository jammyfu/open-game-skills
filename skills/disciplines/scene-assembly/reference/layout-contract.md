# Static layout preflight v1

Run from the repository root (both tools also work through absolute paths):

```sh
python skills/disciplines/scene-assembly/scripts/scene_preflight.py skills/disciplines/scene-assembly/assets/layout.example.json
```

Python 3.10+, standard library only. No network, execution of donor code, engine modification or automatic repair. `--output /new/report.json` creates a new report and refuses existing files, including a symlink at that output path. The parent directory must already exist and be trusted. Reports include input/tool SHA-256. Exit 0 = preflight pass, 1 = valid layout with failed checks, 2 = invalid/unsupported input or I/O failure. Never interpret exit 2 as a skip/pass.

## Exact input fields

The [example](../assets/layout.example.json) is synthetic design data, not measured mesh evidence.

| Field | Meaning |
|---|---|
| schema_version | integer 1, not boolean |
| layout_id | explicit layout revision |
| units / basis | `m` / `right-handed-y-up` only |
| player | positive radius/height; nonnegative clearance/max_step, in meters |
| rooms | 1..128 entries: unique id and positive-volume bounds `[minXYZ,maxXYZ]` |
| solids | 0..512 unique id/bounds entries for blocking props, not room shell planes |
| spawns | 1..64 entries: id, room, position at feet on the declared floor |
| portals | 0..256 entries: id, two room IDs, x/z crossing axis, bottom-center, width, height |
| required_rooms | nonempty unique IDs reachable from every declared spawn |

All object IDs are globally unique. Unknown keys, unsupported basis/units, non-finite values, duplicate JSON keys, dangling IDs and invalid extents are rejected. Input is limited to 4 MiB.

Rooms represent flat, unobstructed rectangular floor envelopes before solids, with floors at minY and ceilings at maxY. Interiors may not overlap; adjacent faces may touch. Portals must lie on a shared x/z face, fit both lateral envelopes and ceilings, and have their bottom at the higher floor. Step differences must fit the declared step budget. A bidirectional centered crossing uses a conservative AABB footprint of `radius + clearance` and a height of `height + clearance`.

Solids must fit inside a room. Spawn and doorway-crossing boxes must not intersect solids. The accepted portal graph must connect each spawn room to all required rooms. Equality at a clearance boundary passes within 1e-7 m arithmetic tolerance; this is not a suggested gameplay clearance.

## Explicit limits

This is **static-layout-preflight**, not engine integration. It consumes final world-space AABBs, not GLB/OBJ files. Rotated geometry requires conservative world bounds from the actual adapter; skewed/curved/sloped rooms need other checks. AABB corner false positives are possible. No collision mesh import, within-room pathfinding, stairs, jumping, one-way links, key/ability gates, camera volumes or dynamic blockers are simulated. Empty floors and door openings are assumptions, not verified facts. Report `runtime_validation: not-run` even when a source claims its dimensions were measured.

A positive graph result proves only room-graph connectivity under this schema. A wall spanning a room can still disconnect its interior. Require a real runtime traversal probe before accepting an assembled scene as playable. Use `procedural-generation` for progression-aware generated topology rather than extending this preflight into a second generator.

Non-finite derived widths or spawn AABBs are rejected, even when the input scalars were individually finite. This is an unsupported-input result, not a layout pass.
