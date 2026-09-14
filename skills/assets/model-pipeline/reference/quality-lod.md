# Identity-preserving LOD and asset fit

## Import preflight, before reduction

Preserve source bytes. Record asset/variant IDs, source hashes, importer and conversion recipe, physical dimensions after parent transforms, pivot/contact plane, render bounds versus collision envelope, required sockets, material/texture dependencies and animation capabilities. glTF node transforms compose as T*R*S and may include hierarchy transforms; accessor bounds are not automatically world bounds or animated skinned bounds. Imported measurements must be distinguished from declared metadata.

List required glTF extensions and the target loader/decoder support. A downloaded GLB can still need a Draco/Meshopt decoder or KTX2 transcoder; successful byte pinning is not a decode test. Keep decoder versions/resources in the reproducibility record. Do not silently drop a material, skin or clip to mark the asset ready.

## Reduction as a constrained search

A tier table records actual triangles (not an ambiguous polygon count), vertices, material/draw partitions, texture memory, skin/morph capabilities, screen-use range, and acceptance measurements. Budgets come from `performance-budget`; this skill owns the exported tier recipe. A 100-triangle cube-style character is an explicit art variant, not automatically an acceptable final LOD of a detailed humanoid.

Rank importance by intended cameras and poses: recognizable silhouette, face/hair outline, hands/held prop, articulating joints and gameplay-critical sockets. Preserve UV/material boundaries, normals and deformation where required. Detail that survives projected size can move to maps when baking is supported; preserve shape that still changes the silhouette. Do not uniformly decimate every region by the same ratio merely to hit a number.

Generate each tier from a retained source or a documented dependency chain. Validate every tier against the source; successive reduction must not hide accumulated damage. Compression and simplification are separate steps with separately pinned settings. A smaller transfer file does not prove lower GPU memory or faster rendering.

## Runtime switch contract

Choose tiers by projected size/error or an explicitly calibrated distance rule, with enter/exit hysteresis to avoid toggling near thresholds. Treat cross-fade cost, temporary double residency and alpha/overdraw as budget items. A snap switch is valid when tested at the intended projected size; fades are not mandatory.

LOD changes presentation, not gameplay hitboxes, damage, targeting legality or input windows. Required sockets retain semantic identity; lower tiers either retain skin/morph features or declare a tested fallback. Runtime quality policy may select tiers but cannot invent altered gameplay.

## Acceptance evidence

Compare identical cameras, projection/resolution, lighting and representative poses. Record screen-space silhouette error, recognizable feature review, deformation/contact/socket errors and measured performance/memory. A triangle target alone is not acceptance. Different art branches need explicit art-direction approval rather than a misleading pixel match.

Test camera movement across thresholds, rapid reversals, crowds, material changes and low-memory switching. Keep visual snapshots and runtime measurements separately classified. This reference provides a production protocol; it does not ship a simplifier, baker, LOD runtime or measured visual pass.

## Primary references

[glTF 2.0 transforms/accessors](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html), [Three.js GLTFLoader](https://threejs.org/docs/pages/GLTFLoader.html), and [Three.js LOD](https://threejs.org/docs/pages/LOD.html). Confirm exact installed versions and extension support before choosing an adapter implementation.
