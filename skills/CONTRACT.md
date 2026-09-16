# Shared execution contract

Inspect the current project, engine/version, dimension, units, target device, chosen modes and reproduction before editing. Explicit user choices outrank project defaults, which outrank tuning seeds. Ask at most one consequential unresolved question; never ask for facts already supplied.

A column is a mode within one design axis. Independent axes can combine; contradictory modes on the same actor/item cannot silently combine. Numeric examples are tuning seeds, not universal engine facts. Preserve intentional design choices.

Work in phases of at most three specialized skills plus one necessary engine. Asset/2D skills count; entry, dispatcher and reference documents do not. References are conditional, not recursive activation instructions. Record deferred work.

Every check records build/commit, configuration, scenario, driver, result and evidence. Use pass, fail, blocked or not-run. Separate static checks, tool tests, engine integration, model evaluation and human playtests. Do not call an untested game completable or label debug-assisted footage as a natural clear. Unknown failure attribution stays unknown until evidence separates game, harness, environment and strategy.

When Git writes are authorized, inspect current refs, preserve unrelated changes, test, review the diff, commit one coherent step and push without force. A remote branch SHA, not a scratch tree or local snapshot, is the synchronization checkpoint. Do not publish secrets, private certification matrices or assets without appropriate rights.

## Engineering and asset ownership

| Concern | Owner | Does not own |
|---|---|---|
| Whole-game transitions | game-state-flow | actor move frames |
| Resource lifetime | asset-runtime | which world cells should exist |
| Valid generated topology | procedural-generation | map UI or cell residency |
| Surface boundaries | terrain-surface | the swimming move graph |
| Cell residency/readiness | world-streaming | disposal of another owner's shared texture |
| Interactive body motion | physics-interaction | damage or chemistry rules |
| Image inventory | sprite-catalog | atlas packing |
| Atlas import | sprite-atlas | required asset families or combat timing |
| Effect generation | vfx-generate | gameplay authority; vfx-prompt is a compatibility entry |

The [engineering registry](engineering-registry.json) is a scoped repository extension, not new Agent Skills frontmatter or a complete mode registry for older skills. Optional dependencies are conditional; do not recursively load them. Follow the [engineering workflow](references/engineering-workflow.md) for phase boundaries and outputs. Authored scenarios and illustrative JSON contracts remain not-run until executed with evidence; a consistent record is not proof of authenticity or semantic correctness.

Scene-assembly owns placement/kit compatibility against approved blockout metrics. It consumes model-pipeline fit records, character-rig clip compatibility and asset-runtime leases; it does not create another topology generator, exporter, movement controller or claim taxonomy. Its static AABB preflight and gameplay-harness's offline trace comparator are tool-level evidence only.
