# Tool adapters

## Spine editor and PixiJS

Use the installed editor/runtime's official documentation to verify current compatibility and features before integrating. Weighted meshes require the appropriate Spine editor edition; official runtime integration has its own licence terms. A community skill or MIT compiler does not grant that licence. Match editor/export and runtime major.minor versions. Primary references: [weights](https://esotericsoftware.com/spine-weights), [PixiJS runtime](https://esotericsoftware.com/spine-pixi), [editions](https://esotericsoftware.com/spine-purchase).

Export the evaluated world bone matrices and attachment vertices, after IK/deformation, at the required times. Preserve source UV/image mapping and weighted bindings. For shared atlases, identify each attachment's actual image rectangle, trim, rotation and density; a local0..1UV cannot be sampled against an unrelated full atlas page. Do not invoke a parser-only check as proof the mesh poses correctly.

## rig-c optional compiler

[rig-c](https://github.com/rig-c/core) can compile named weighted meshes and animation specs. It is an optional adapter, not a required dependency of this skill. Pin the reviewed version and integrity/source identity; inspect its shipped skill/docs. Do not silently install an official Spine runtime beside it.

The demonstrated Chu toolchain used rig-c 2.79.0, isolated Bun 1.4.0, `cli_core.ts`, and rig-c's own MIT poser. Its official parser roundtrip was SKIP. Reports must retain that distinction. Its own runtime and experimental import surfaces are not assumed production-ready just because the compiler passes.

A rig-c adapter can call its supported core entry to export evaluated matrices/vertices, rather than reimplementing the skinning formulas inside the auditor. Tool-specific dependency fetching, compiler invocation and PixiJS bundling remain project adapters. The portable audit consumes ordinary JSON plus images and needs no Bun, proprietary editor, game ROM or installed rig-c.

## Preview

Use the actual target renderer with a fixed view, play/pause, time scrubbing, bone overlay and wireframe. Display unplanned growth, seams and folds at full resolution and game scale. Save actual browser/engine evidence. A common-view rendered animation can complement the live rig but does not replace runtime validation. Expose per-actor hitstop and attachment switch times when those are being tested.
