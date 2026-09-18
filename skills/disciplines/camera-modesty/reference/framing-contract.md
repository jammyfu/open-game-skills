# Static modesty framing preflight v1

Run from the repository root (absolute paths also work):

```sh
python skills/disciplines/camera-modesty/scripts/modesty_check.py skills/disciplines/camera-modesty/assets/framing.example.json
```

Python 3.10+, standard library only. No network, mesh import, engine solve or automatic camera write-back. `--output /new/report.json` creates a new report and refuses existing files, including a symlink at that output path. The parent directory must already exist and be trusted. Reports include input/tool SHA-256. Exit 0 = static pass, 1 = valid input with failed checks, 2 = invalid/unsupported input or I/O failure. Never interpret exit 2 as a skip/pass.

## Exact input fields

The [example](../assets/framing.example.json) is synthetic design data, not a scanned body or an engine capture.

| Field | Meaning |
|---|---|
| schema_version | integer 1, not boolean |
| scene_id | explicit framing revision |
| units / basis | `m` / `right-handed-y-up` only |
| policy | `mode` plus four finite thresholds |
| characters | 1..32 proxies with landmarks and private zones |
| poses | 1..256 camera poses |
| boom_sweeps | 0..64 groups of existing pose IDs |

`policy.mode` is `modest`, `adult` or `medical-exam`. Thresholds: `max_upward_elevation_deg` (0..89), `min_private_clearance_m` (>0), `min_private_screen_distance_m` (>0), `max_private_fov_at_close_deg` (1..179).

Each character has `id`, `proxy`, `up`, `landmarks` (`hem`, `hip`, `chest`) and `private_zones` (1..16). Proxy `kind` is `capsule` (`origin`, `height`, `radius`) or `aabb` (`bounds`). Zone rows are `id`, `kind`=`aabb`, `bounds`, `class` in `groin` / `chest` / `under-hem`. Landmarks must be ordered hem ≤ hip < chest along character up.

Each pose has `id`, `position`, `forward`, `up`, `fov_v_deg`, `near_m`, `aspect`, `authored_intent` (`none` / `adult` / `medical-exam`). Forward and camera up must be nonzero and not parallel.

Boom sweeps list `id` and nonempty `pose_ids` that already exist in `poses`. All object IDs are globally unique. Unknown keys, non-finite values, duplicate JSON keys and invalid extents are rejected. Input is limited to 4 MiB.

## Checks

Evaluated per pose against every character unless `policy.mode` is a non-modest opt-in **and** `authored_intent` matches that mode:

| Rule ID | Fail when |
|---|---|
| under-hem-look | camera is at/below hem and the look ray hits the under-hem volume, or camera is below hem, looking up past the elevation cap, and near the vertical axis |
| between-legs | camera is inside the horizontal proxy and between the feet and hip |
| near-plane-private-zone | the near-plane rectangle overlaps a private-zone AABB |
| private-zone-proximity | camera-to-zone distance is below `min_private_clearance_m` |
| private-region-zoom | a groin/chest zone is in front, closer than `min_private_screen_distance_m`, and vertical FOV exceeds `max_private_fov_at_close_deg` |
| boom-sweep | any listed sample pose failed |

Failed poses include a suggested clamp: raise pitch (degrees), pull back (meters), raise boom (meters). These are static hints, not an applied solve.

## Explicit limits

This is **static-modesty-preflight**, not a renderer, cloth sim, animation retarget or collision sweep. Axis-aligned zone AABBs and declared landmarks are assumptions. Rotated bodies need conservative world bounds from the actual adapter. No skeletal mesh, skirt dynamics, gender inference or medical finding is computed. A boom-sweep group only aggregates already-declared poses; it does not sample an authored curve. Report `runtime_validation: not-run` even when a source claims the numbers came from an engine.
