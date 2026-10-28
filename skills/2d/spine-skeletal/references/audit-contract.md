# Portable posed-trace contract

`python3 scripts/audit_skin.py trace.json --out report.json` reads actual runtime exports, not authored pose controls substituted for observations. Exit0 means the declared technical checks pass;1 means measured failures;2 means invalid/missing evidence. Pillow and numpy are required. Paths are relative to the trace file. The script never changes art, weights, tolerances or project files.

The JSON object uses `schema: "ogs.skin-trace/1"` with these required fields:

| Field | Shape and meaning |
|---|---|
| `sampleRate` | Positive Hz; adjacent time gaps must not exceed one sample period plus floating-point slack. Export actual evaluated poses at this rate, including extremes and loop end. |
| `tolerances` | Nonnegative finite `length`, `scale`, `loop`, `weights`, `area`; integer `alphaThreshold`0..254. Select before comparing candidates. Units for length/loop/area are world units / squared world units. |
| `boneScales` | `{boneName: [expectedWorldScaleX, expectedWorldScaleY]}` for all observed bones. Root/depth/facing conventions must be explicit; prefer traces before display scaling, one view per trace. |
| `segments` | Nonempty `[{a: boneName, b: boneName, length: positiveNumber}]` with pinned expected origin-to-origin distances. They are not inferred from the evaluated result. |
| `meshes` | `{meshName: {image, sha256, uvs, triangles, weights, setupVertices}}`; image is the exact setup RGBA page/part whose local UVs are provided. `setupVertices` is the approved unanimated bind geometry in world units, independent of the first animation sample. Atlas UVs must be resolved into that image's coordinate system first. |
| `frames` | At least two `{t, bones, meshes}` records with strictly increasing finite seconds. Bones map names to `{a,b,c,d,x,y}` world affine matrices; mesh records map names to flat world-space vertex arrays. Every declared bone/mesh is required at every sample in this version. |
| `loops` | `[{first,last,firstImage?,lastImage?}]`, frame indices for declared identical endpoint poses. Mesh vertices and bone origins use `loop` tolerance; endpoint linear matrices use `scale` tolerance. Both image paths or neither. RGBA decoded loop images must be pixel-identical; use a shared fixed camera. An empty list declares that this trace does not claim a loop. |
| `contacts` | `[{bone,first,last,target:[x,y],tolerance}]` for explicitly planted intervals. Empty declares no contact check. Export separate traces or extend the adapter for moving targets; do not label walking/airborne phases as fixed plants. |

Each mesh has two UV numbers per vertex, all in0..1. Triangles are integer index triples. Every vertex has a nonempty weights array of `{bone, weight}`; adapters may retain bind-local x/y as additional fields. Bone names must resolve. The auditor checks normalization and computes setup-to-posed triangle winding and near-zero areas, then rasterizes the union of bad UV triangles against actual alpha. Visible bad pixels fail. Source file SHA256 must match; RGB hidden under zero alpha does not count as visible ink.

Length/scale checks use actual matrices and actual origins. The trace is not a detector: the harness cannot establish that a named shoulder bone sits on the painted shoulder or that its reference length is correct. It also cannot infer omitted animations or contacts. `technicalStatus` is separate from `characterAccepted`, which remains false. Visual anatomy, head/body ratios, required action coverage, attachment continuity, actual renderer shoe pixels and native timing require independent evidence.

For attachment swaps, this version accepts one stable mesh roster/topology per trace. Split the sweep into declared attachment intervals and review the boundaries separately. Do not silently drop disappearing attachments or treat those sub-traces as proof the switches are seamless.
