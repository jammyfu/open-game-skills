---
name: scene-assembly
description: Use when modular assets must become a playable scene, when individually valid props do not fit together, or when set dressing blocks spawns, doors, sightlines or traversal space.
---

# Scene assembly

Own **placement and kit compatibility** between validated assets and an approved blockout. Do not become a second level designer, procedural generator, mesh exporter or resource manager.

## Modes

| Mode | Work |
|---|---|
| modular-kit | fit compatible modules to an explicit layout |
| dress-existing | replace/decorate an existing blockout without changing its gameplay metrics |

## Procedure

1. Inspect the target layout, movement/camera metrics, engine version and asset locks. Missing kit pieces remain explicit; do not replace a rig with a static prop or invent an unlicensed donor. [Open asset fixture](../../assets/open-asset-fixture/SKILL.md) owns acquisition.
2. Build a kit manifest: asset ID/version/hash, role, physical dimensions, pivot/contact plane, connection sockets, material family, collision proxy and available variants. Measure imported bounds; authored dimensions are declarations until checked. [Model pipeline](../../assets/model-pipeline/SKILL.md) owns unit/axis conversion. Do not independently rescale every wall until it looks plausible.
3. Use [level-blockout](../level-blockout/SKILL.md)'s metrics as constraints. Name floor/wall/door/cover/spawn/exit roles, walkable lanes, camera corridors and no-decoration zones. Keep required collider/gate identity when replacing greybox visuals.
4. Align compatible sockets using a single documented parent/local-to-world transform. Check facing, contact height and seam tolerance after hierarchy transforms. Visual bounds, placement envelopes and colliders are distinct. Reject incompatible connector sizes instead of stretching doors or deleting collision.
5. Preflight declared world-space bounds with [scene_preflight.py](scripts/scene_preflight.py) and the [v1 contract](reference/layout-contract.md). Then import and test the actual scene: spawn, door crossing in both directions, collision, camera, occlusion, exit and retry. A room graph is not a navmesh, puzzle solution or natural clear.
6. Stage required floor/collision assets before activation. [Asset runtime](../asset-runtime/SKILL.md) owns leases; [world-streaming](../world-streaming/SKILL.md) owns residency. Replacing decorations must not release shared geometry still used elsewhere.

## Outputs

Deliver an assembly manifest, asset-to-instance mapping, placement transforms, protected gameplay zones, unresolved kit mismatches and preflight/runtime evidence. Preserve original locks. Record layout version, actual build, adapter, configuration and any debug setup.

## Acceptance

Normal: assemble two connected rooms and retain collision/gate identity after visual replacement. Boundary: a narrow door, large player, elevated threshold or missing module reports a specific blocked requirement. Adversarial: a crate obstructs spawn/door, two room volumes overlap, or a pretty screenshot is offered as playability proof; do not approve it.

The bundled CLI checks a deliberately limited static AABB layout. `pass` means that preflight only; engine and human checks remain `not-run`. Work in phases of at most three specialized skills plus one engine, with dependencies deferred rather than recursively loaded.

## Asset preparation entry

In the full pack, `prepare_assets.py --skill scene-assembly` selects a starting pool of static environment candidates. It does not assert that walls, floors and doors form a complete compatible kit. `--pinned-only` without usable locks stays blocked. Override the broad discovery request for the actual art direction via the asset owner's documented request interface; pure layout tests need no downloaded art.
