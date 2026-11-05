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

- Track values are offsets added to the setup value. Properties: `rotate`, `x`, `y`. Key `curve`: `linear` (default), `smooth`, `stepped`; a key's value applies from its own timestamp, and `stepped` holds it until the next key.
- IK runs after tracks in list order. The child must start at the parent's tip, and both bones must inherit rotation (the analytic solver rejects `inheritRotation: false` chains). A target is `{"bone", "point"}` or `{"fixed": [x, y]}`.
- `contacts` measure effector-to-target distance on frames `first..last`; the effector point defaults to the bone tip.
- `fixedContacts` passes through to the audit's `contacts` field for planted world targets.

## Idle config for `idle_motion.py` (authored)

```json
{"duration": 4.0, "sampleRate": 30, "breaths": 2, "inhale": 0.4,
 "channels": [{"bone": "chest", "property": "y", "amplitude": -0.55},
              {"bone": "spine", "property": "rotate", "amplitude": 1.2, "lag": 0.05},
              {"bone": "head", "property": "rotate", "amplitude": -2.5, "lag": 0.14}],
 "fixedContacts": [{"bone": "ground", "first": 0, "last": 120, "target": [22.25, 64.06], "tolerance": 1e-6}]}
```

- Each channel's offset is `amplitude * breath(breaths*t/duration - lag)`. `breath` is 0 at phase 0, 1 at `inhale`, eased both ways and periodic. `amplitude` is degrees for `rotate` and world units for `x`/`y` (negative `y` is up).
- Refused, not clamped: `breaths` not an integer in 1..8, `inhale` outside 0.2..0.8, `lag` outside 0..0.5, `|rotate amplitude|` above 15, unknown bones, duplicate channels, scale/shear properties, a duration that is not a whole number of samples. `ik`, `contacts` and `fixedContacts` pass through to the motion.

## Generated files

- `ogs.skin-mesh/1`: per part `vertices` (setup world), `uvs`, `triangles`, `hull` (outline vertex count, listed first), `sha256` of the image, `rigSHA256`.
- `ogs.skin-weights/1`: per part `weights[vertex] = [{bone, weight, x, y}]` with setup-local `x,y`, `handles` (rigid vertex indices), the options used, `rigSHA256`, `meshSHA256`.
- The pose report adds `rigidityDeviation[part][bone] = {softLengthFraction, maxDeviation}` over vertices the bone dominates inside its handle tube. `softLengthFraction` is the share of the bone's length that leaves rigid motion by more than 0.05 world units; on a thin limb it is how much of it bends like rubber.
- `ogs.skin-anatomy/1` (`measure_anatomy.py`): `box`, `axisX`, `neckRow` with `neckSource` (`bottleneck` or `manual`), `neckHalfWidth`, `headCentreX`, `headHalfWidth`, `torsoHalfWidth`, `hipRow`, `footRow`, `feetSpan`, `appendages[{rows, side, reachPx}]` and the smoothed `halfWidthProfile`, all in source pixels, plus the image `sha256`. `--rig-out` writes an `ogs.skin-rig/1` proposal (bones `root`, `ground`, `spine`, `chest`, `head`; one part `figure`) to review before solving.
- `ogs.skin-motion-qa/1` (`motion_qa.py`): `status`, `limits` (`seam`, `pop`, `jitter`, `stillTolerance`, `minMotion`), `failures`, and per mesh and per bone `maxDisplacement`, `maxStep`, `medianStep`, `pop` (largest step / median step), `jitter` (speed-weighted share of samples that reverse direction), `seam` (wrap acceleration / 95th percentile elsewhere), `resets` for `--allow-reset` parts, or `static`/`still`. Exit 0 PASS, 1 FAIL, 2 invalid.
- `pose_trace.py` writes `ogs.skin-trace/1` per the [spine-skeletal audit contract](../../spine-skeletal/references/audit-contract.md), plus `drawOrder` and provenance with `runtimeTrace: false`. It also carries review-only `skeleton` (`[{name, parent, length}]`) and `constraints` (`{ik, contacts}` copied from the motion) so `render_skin.py --bones --constraints` can draw Spine-style bones, IK chains, IK targets and contact targets; the audit ignores both.
