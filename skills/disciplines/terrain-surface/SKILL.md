---
name: terrain-surface
description: Use when terrain chunks crack, slopes and materials disagree, shorelines look detached, or water entry and collision fail to match the visible surface.
---

# Terrain surface

## Scope

Own geometry/surface boundaries and their shared data contract. Do not replace world topology, swimming moves or camera rules. Coordinate with [swim-water](../swim-water/SKILL.md), [locomotion](../locomotion/SKILL.md) and [materials](../../assets/materials/SKILL.md) only when needed. Fix geometry and gameplay boundaries before hiding defects under foam or particles.

## Modes

| Mode | Boundary model |
|---|---|
| heightfield | elevation samples with shared tile edges |
| voxel-surface | extracted surface with explicit neighbor/LOD boundaries |
| tilemap | edge/corner-matched terrain tiles and authored shapes |

## Procedure

1. Record coordinate axes, units, cell resolution, border ownership, collision representation and the authoritative water level/volume. Publish surface IDs and gameplay properties separately from visual color. Name an allowable render/collision error with units and a reason.
2. Derive neighboring boundaries from shared global samples. A heightfield with N cells needs N+1 edge samples; normals may require a neighbor halo. Treat negative coordinates consistently. Preserve intended cliff discontinuities; continuity does not mean smoothing every hard edge.
3. Define geometry stitching/transition rules at each supported LOD boundary. Skirts can hide a visual gap but do not repair collider cracks or navigation holes. Test collision continuity separately; do not change gameplay slope/step limits to cover a rendering defect.
4. Derive slope/height material transitions and shoreline placement from the same canonical data. Smooth appearance without silently moving the ground or water trigger. Set explicit enter/exit hysteresis where needed to prevent walk/swim flapping. Visible waves may be cosmetic; disclose any difference from the gameplay water surface.
5. For tilemap mode, author edge/corner variants plus collision/navigation metadata, including empty and diagonal neighbors. A correctly matched picture is not a generated collider. Terrain/water edits invalidate dependent mesh, collision and navigation versions before the region becomes traversable again.

## Outputs

Adapt the [surface contract](assets/contract.example.json): representations, border/LOD policy, surface table, water transition thresholds, error tolerances, regeneration dependencies and debug overlays. Measure signed heights/normals and collision crossings; a screenshot alone cannot establish walkability.

## Acceptance

Walk across four-chunk corners, steep boundaries, water entry/exit and mixed LODs; repeat at low quality and after a terrain edit. Record collision continuity, visible seam error and swim transitions against chosen tolerances. Keep valid cliffs and deliberate water behavior. [Cases](assets/evals.json) remain not-run until target-engine checks and visual review are performed.

## References

[Godot TileSets](https://docs.godotengine.org/en/stable/tutorials/2d/using_tilesets.html) separates terrain matching from collision/navigation shapes. [Tiled terrain sets](https://doc.mapeditor.org/en/stable/manual/terrain/) documents edge/corner variants for the 2D mode. These do not supply a universal 3D shoreline shader or collider.
