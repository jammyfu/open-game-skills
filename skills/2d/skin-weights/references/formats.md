# File formats

World space is y-down (image-like); rotations are degrees, positive turns +x toward +y. Bone matrices are `[a,b,c,d,x,y]`, mapping local `(u,v)` to `(a*u+b*v+x, c*u+d*v+y)`. rig-c/Spine are y-up; `export_rigc.py` converts.

## `ogs.skin-rig/1` (authored)

```json
{"schema": "ogs.skin-rig/1",
 "bones": [{"name": "root"},
           {"name": "thigh", "parent": "root", "x": 2, "y": 4, "rotation": 80, "length": 20},
           {"name": "shin", "parent": "thigh", "x": 20, "y": 0, "rotation": 30, "length": 20},
           {"name": "foot", "parent": "shin", "x": 20, "inheritRotation": false, "length": 6}],
 "parts": [{"name": "leg", "image": "leg.png", "origin": [0, 0], "at": [-10, 2], "density": 4,
            "bones": ["thigh", "shin", "foot"],
            "mesh": {"spacing": 6, "alphaThreshold": 32, "margin": 2},
            "weights": {"handleRadius": {"thigh": 4.2, "shin": 2.4, "foot": 1.6},
                        "coreInset": {"thigh": 0.3, "shin": 0.3, "foot": 0.35},
                        "maxInfluences": 3, "pruneBelow": 0.01},
            "lint": {"maxReach": 14, "minTransition": 3}}],
 "drawOrder": ["leg"]}
```

- Parents are declared before children. `length` ≥ 0. `inheritRotation: false` keeps the bone's own world rotation.
- A part image pixel `p` sits at world `at + (p - origin) / density`. `bones` lists the only bones allowed to influence the part; one bone means rigid.
- `handleRadius` and `coreInset` take a number or a per-bone map. `handleRadius` is required for multi-bone parts.
- A bone's `coreInset` may be `[head, tail]` (fractions of its length kept free at the parent and child ends, `head + tail < 1`). Use it to put a joint's bend on the soft side: the pelican's knee uses `thigh: [0.1, 0.3]`, `shin: [0.06, 0.0]`, so the thin shin stays straight.
- `mesh.mode: "quad"` replaces the alpha-covering grid with one quad over the whole image. Use it for rigid single-bone parts (backdrops, props) that have several separate islands, since Spine and rig-c need one outline per attachment.
- `lint` bounds are optional and must be chosen before comparing candidates. `minTransition` defaults to two median edge lengths.

## `ogs.skin-motion/1` (authored)

```json
{"schema": "ogs.skin-motion/1", "sampleRate": 60, "duration": 2, "loop": true,
 "tracks": [{"bone": "crank", "property": "rotate", "keys": [{"t": 0, "v": 0}, {"t": 2, "v": 360}]}],
 "ik": [{"name": "leg", "bones": ["thigh", "shin"], "target": {"bone": "pedal", "point": [0, 0]}, "bend": 1}],
 "contacts": [{"name": "foot on pedal", "effector": {"bone": "shin"}, "target": {"bone": "pedal"},
               "first": 0, "last": 120, "tolerance": 0.0001}]}
```

- Track values are offsets added to the setup value. Properties: `rotate`, `x`, `y`. Key `curve`: `linear` (default), `smooth`, `stepped`.
- IK runs after tracks in list order. The child must start at the parent's tip. A target is `{"bone", "point"}` or `{"fixed": [x, y]}`.
- `contacts` measure effector-to-target distance on frames `first..last`; the effector point defaults to the bone tip.
- `fixedContacts` passes through to the audit's `contacts` field for planted world targets.

## Generated files

- `ogs.skin-mesh/1`: per part `vertices` (setup world), `uvs`, `triangles`, `hull` (outline vertex count, listed first), `sha256` of the image, `rigSHA256`.
- `ogs.skin-weights/1`: per part `weights[vertex] = [{bone, weight, x, y}]` with setup-local `x,y`, `handles` (rigid vertex indices), the options used, `rigSHA256`, `meshSHA256`.
- The pose report adds `rigidityDeviation[part][bone] = {softLengthFraction, maxDeviation}` over vertices the bone dominates inside its handle tube. `softLengthFraction` is the share of the bone's length that leaves rigid motion by more than 0.05 world units; on a thin limb it is how much of it bends like rubber.
- `pose_trace.py` writes `ogs.skin-trace/1` per the [spine-skeletal audit contract](../../spine-skeletal/references/audit-contract.md), plus `drawOrder` and provenance with `runtimeTrace: false`.
