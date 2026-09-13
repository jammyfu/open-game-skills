# Engineering workflow

Load only the phase relevant to the reported defect. Existing project decisions and the three-specialized-skill working-set limit still apply. Consult the [registry](../engineering-registry.json) for this batch's modes; do not treat a registry default or example value as an approved project choice.

| Phase | Skill | Handoff |
|---|---|---|
| Session boundary | [game-state-flow](../disciplines/game-state-flow/SKILL.md) | accepted transition, session/round ID, task epoch |
| Resource boundary | [asset-runtime](../disciplines/asset-runtime/SKILL.md) | versioned manifest, consumer leases, readiness/failure |
| Construction | [procedural-generation](../disciplines/procedural-generation/SKILL.md) | recipe, constraints, global coordinates, failure seeds |
| Surface agreement | [terrain-surface](../disciplines/terrain-surface/SKILL.md) | shared geometry/water data, collider and LOD agreement |
| Residency | [world-streaming](../disciplines/world-streaming/SKILL.md) | active cells, dirty deltas, safe transfer gates |
| Interaction | [physics-interaction](../disciplines/physics-interaction/SKILL.md) | one body-motion owner, release/restore policy |

For a new world prototype, settle session/resource ownership first, then generation/surfaces, then residency/interaction. This is an incremental recipe, not a demand to rebuild an existing game. A shoreline-only repair usually loads terrain-surface and its one relevant neighbor, not all six skills.

Every new skill contains `assets/contract.example.json` and `assets/evals.json`. Adapt the example to the actual project; placeholder IDs, radii and retry counts are not measurements. The three case classes are normal use, a boundary failure, and an adversarial request that tempts the agent to violate the contract. Cases specify evaluation work; they do not contain model scores.

The repository's offline `tools/engineering_quality.py` checks this scoped registry and imported evaluation records. Development tooling is in the repository, not copied by the skill-only installer. Run model evaluations with an available authorized runner, preserve responses and identify the evaluator before assigning results. Static document checks, model judgments, engine integration and human playtests remain separate evidence levels.
