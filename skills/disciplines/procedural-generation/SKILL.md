---
name: procedural-generation
description: Use when generated maps, rooms or terrain must be reproducible and playable, when some seeds trap players, or when chunk generation order changes the world.
---

# Procedural generation

## Scope

Own world construction and validity, not map UI, surface shading or streaming residency. [World map](../world-map/SKILL.md) owns discovered information; [rng-seed](../rng-seed/SKILL.md) owns random streams. Preserve authored areas and player edits. A decoration generator need not become a full world generator.

## Modes

| Mode | Representation |
|---|---|
| room-graph | connected rooms and progression constraints |
| heightfield | single-valued elevation over a plane |
| voxel | volumetric occupancy or density, including caves |
| tile-constraint | local adjacency plus separately validated global goals |

## Procedure

1. Specify the generator/version, configuration hash, seed encoding, units, bounds and player traversal kit. Separate hard validity constraints from visual preferences: safe spawn, reachable exit, prerequisites before locks, required resources and legal return/reset paths. A heightfield cannot represent arbitrary overhangs; choose another representation when required.
2. Derive named random streams with a documented stable algorithm. Use seed + subsystem + global chunk coordinates, not runtime-randomized language hashes or request order. Store stream state for continuation and a versioned recipe plus edit deltas for saves. A seed alone does not guarantee reproducibility across algorithms, versions or physics backends.
3. Generate coarse topology before decoration. Enforce progression-aware reachability, including collected abilities/keys and resource costs where relevant. A geometric flood fill does not prove a key puzzle or a jump is solvable. Validate with the actual movement metrics and collision representation.
4. Sample shared borders in global coordinates, including negative coordinates, and coordinate ownership of boundary objects. Do not independently reseed each chunk edge. Merge authored/player changes by explicit precedence rather than regenerating them away.
5. Bound attempts, time and repair scope. Log the original failing seed/configuration before deterministic repair or a declared fallback. Unsatisfiable tile constraints must terminate with a useful diagnostic; do not silently remove required progression gates to claim success.

## Outputs

Adapt the [generation contract](assets/contract.example.json): recipe and versions, constraints, seed corpus, per-seed diagnostics, edit precedence and repair/fallback record. Keep expensive generation off the critical input path through the engine's supported job system; commit finished data at an owned boundary.

## Acceptance

Re-run saved failures and a stated sampled seed corpus; compare topology/data hashes for the same version/configuration and for different chunk request orders. Test unreachable exits, locked keys, negative coordinates and exhausted retry budgets. Report coverage and failures; sampled success is not proof for every seed. [Cases](assets/evals.json) remain not-run until executed. Runtime reachability needs more than a source review.

## References

[Tiled terrain constraints](https://doc.mapeditor.org/en/stable/manual/terrain/) illustrate local edge/corner matching. They do not establish global puzzle solvability. [Godot RandomNumberGenerator](https://docs.godotengine.org/en/stable/classes/class_randomnumbergenerator.html) documents seed/state behavior; inspect the installed version before promising compatibility.
