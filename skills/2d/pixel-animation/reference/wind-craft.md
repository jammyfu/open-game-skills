# Wind craft beyond a single tree

These notes extend the [tree workflow](tree-wind.md). Sources below were read on 2026-11-15; summaries are independent, with no copied artwork or implementation. Source techniques and proposed project checks are separated deliberately.

## Hand-authored secondary motion

Source: Raymond Schlitter, [Pixelblog 33: Wind Effects](https://www.slynyrd.com/blog/2021/7/16/pixelblog-33-wind-effects).

- Sequence small foliage displacements across neighboring groups to produce flow. Refine individual leaf shapes after the broad motion works.
- Start falling leaves as tiny particles with consistent pixel steps, then vary their visible shape to suggest tumbling. Position and silhouette are separate animation decisions.
- For hair and fabric, establish moving control points with growing waves toward the free end. Establish major forms before secondary strands; avoid shading changes that obscure motion.
- Dust and abstract swirls can communicate wind where foliage is absent, but choose particles appropriate to the environment.

### Project adaptation and acceptance

Keep attached leaf rustle and detached leaf particles in separate tracks. Reuse the shared wind field, with separately authored gravity and lifetimes for detached leaves. Pin attachment points for flags and hair, rather than moving the whole silhouette. Publish pose durations and the start/end state of each loop.

Inspect the animation at native resolution, with texture detail temporarily replaced by flat cluster colors. Motion should remain legible. Check attachment coordinates over every frame, deliberate loop closure without duplicated endpoint holds, particle pool return after emission stops, and stable bounded counts during sustained wind. Include a negative control: all groups moving in lockstep should visibly lose the traveling flow. These checks are proposed acceptance tasks, not results from the existing tree demo.

## Separate force, response and fine motion

Source: Tiago Sousa (Crytek), [GPU Gems 3, Chapter 16](https://developer.nvidia.com/gpugems/gpugems3/part-iii-rendering/chapter-16-vegetation-procedural-animation-and-shading-crysis).

The chapter separates major vegetation bending from leaf detail, combines world-space wind sources per instance, and exposes stiffness and phase controls. Its GPU deformation and shading address 3D vegetation, not pixel sprites.

For this 2D skill, adapt the separation into explicit metadata: plant anchor, cluster rest position, response gain, stiffness, and an optional fixed detail-phase offset. Keep phase variation stable across frames; do not draw new random phases each update. A thick oak's wood remains rigid. Quantize the final visible cluster offset after combining permitted motion, rather than importing 3D vertex bending unchanged.

### Project adaptation and acceptance

Treat the world field as input, the spring as state, and stepped poses as presentation output. Use one declared simulation step and clock. Disabling gust force should not instantly erase stored spring velocity; resetting a scene should intentionally clear it. Detail-phase variation must remain small enough to retain a coherent main wave.

Test two trees at different world positions as the same gust passes, and compare their traces after moving only the camera. Pausing, background catch-up and reduced-motion settings need explicit policies. Check disable/re-enable transitions for pops. Keep CPU/GPU timing claims under [performance-budget](../../../disciplines/performance-budget/SKILL.md); a working offline GIF is not performance evidence.

## Evidence boundary

The committed GPT-tree case demonstrates fixed wood, stepped groups, one traveling gust and spring response. It does not yet demonstrate falling leaves, fabric, hair, dust, multiple simultaneous wind sources, multiple trees or lifecycle controls. Do not promote these newly documented techniques to tested capabilities until their own capture and acceptance record exist.
