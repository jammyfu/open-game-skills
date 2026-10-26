# Rigid source-part baking

Use this path for hard frame-to-frame identity, especially after coherent strip generation still changes a face. A stronger text prompt cannot promise identical pixels. Do not silently discard source actions or replace a whole animation with duplicated idle images.

1. Pin a model/face sheet. Generate or author a transparent **master-part set once** at a common character scale: head/neck, torso, pelvis, upper/lower arms, hands, thighs, calves/feet and needed overlays. Use the available image tool for creative raster edits; the baker only assembles those approved existing source parts. Pin their hashes, measured pivots and fixed densities/scales. Inspect a reconstructed rest pose against the approved model; bad master proportions must be redrawn before posing.
2. Define a fixed bone hierarchy and local rest offsets. Author joint rotations and root trajectories from the project's existing pose references. Foot planting/contact positions are a pose-authoring constraint, not a post-hoc bottom alignment. This tool does forward kinematics; it does not infer poses, solve IK or retarget a donor game.
3. Bake each authored gameplay sample as a PNG on a fixed canvas. Bone offsets and each part's scale remain constant across the strip. No frame-specific image replacement, X/Y stretch, deformation or scale is accepted. Layer order may change only as an explicit complete permutation of parts for authored occlusion.
4. Use a separately pinned part bank/recipe for another view. Never regenerate the same view's face independently for each frame. Part reuse preserves source geometry; rotation/resampling and intentional occlusion can still change the visible pixel box. Validate projected landmarks against the appropriate view and inspect seams/occlusions in motion.
5. Run the independent [measurement harness](measurement-contract.md) and actual engine import/playback checks. Generated FK coordinates may supply **expected pose guides**, never fabricated actual-image observations. A deterministic bake does not certify facial style, correct anatomy, seamless joints or fidelity to the reference actions.

```sh
python scripts/bake_rig.py --root /path/to/master-art --rig character-rig.json --out /path/to/new-bake
```

## Recipe fields

`schema` is `ogs.locked-sprite-rig/1`.

- `canvas`: `size` `[width,height]` in logical units, `pivot` `[x,y]` in those units and a fixed physical `density`.
- `logical_tick_hz`: explicit project clock rate, used for provenance; there is no simulation or interpolation here.
- `nodes`: named objects with `parent` (another node or null) and fixed `offset` `[x,y]` in parent-local logical coordinates. Node rotation is accumulated from its parents. The hierarchy must be acyclic. A node's position is its parent's position plus its fixed offset rotated by the parent's world angle.
- `parts`: named objects with `image`, `sha256`, `density`, source `pivot` in physical pixels, positive fixed uniform `scale`, optional fixed `bind_angle` aligning the source bone axis to the rig, optional fixed `mirror_x` for a source part/view, and attachment `node`. The alignment angle is fixed for the entire recipe, never a per-frame correction. These assets are immutable for the bake.
- `frames`: stable IDs, each with `angles` mapping node names to degrees, optional actor-space `root` translation `[x,y]`, optional `consumer_offset` taken from the existing renderer/action sample, and optional `order` listing every part exactly once. Positive angle rotates clockwise in the image coordinate system. The baker subtracts `consumer_offset` from the source frame so the existing renderer can add that same offset once without moving planted contacts twice. It records both source-space and actor-space joints; do not guess or use this offset to hide bad art. Unsupported fields, including per-frame `scale` or `image`, are rejected.
- `clips`: named objects containing `frames`, positive integer `ticks` of the same length, and boolean `loop`. Every baked frame needs an authored clip. These durations remain data for the existing game timeline; do not replace native durations to make the pictures look smooth.

Paths stay beneath the input root. The output must be new/empty and cannot contain source files. All frame geometry is checked before any PNG is written; a clipped part, changed source bytes, missing action, cyclic rig or forbidden transform blocks the bake. `bake.json` records source hashes, fixed part scales, recipe/code hashes, world joints and output image hashes. Its status is deliberately **baked-not-accepted**.

The executable fixtures prove a specific useful invariant: moving an arm leaves the stationary head region **byte-for-byte identical**, while fixed bone lengths survive joint rotation. They do not prove that a project's master art or authored moves are visually correct. A character-wide promotion gate must still require every required pose, density, facing/view and contact/loop review; one passing idle clip cannot certify all actions.
