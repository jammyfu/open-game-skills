# Engineering skills implementation plan

Baseline: `a38072a5f9e0c5c23325603b5efdd17b49eef70c`.
Branch: `feat/engineering-skills-2026-09-13`.

## Approved scope

Implement the six engineering gaps identified in the preceding review, without adding another engine or claiming unperformed runtime/model tests. Preserve existing public skill names and all unrelated upstream changes.

## Commit sequence

1. Record this plan and retain a credential-free tracked-source artifact even when quality checks fail, so a failing baseline can be reproduced. Keep test failures fatal and CI permissions read-only.
2. Repair pack-contained references, refresh the catalog, clarify sprite/VFX ownership through compatibility entries, and remove the combat-only assumption from generic planning. Add tests for a copy-installed pack and the actual defects before their fixes.
3. Add `game-state-flow` and `asset-runtime`, each with scope, modes, outputs, failure cases, primary-source references and normal/boundary/adversarial evaluation scenarios.
4. Add `procedural-generation`, `terrain-surface`, `world-streaming` and `physics-interaction` with the same contracts. Separate generation, surfaces, streaming decisions and resource ownership.
5. Add an explicitly scoped engineering registry and an offline evaluation-evidence validator. It must reject missing evidence and fabricated completeness; authored test scenarios are not model results. Update dispatcher, catalog, shared ownership and all five README locales.
6. Re-run the full test suite, inspect the exact uploaded tree and current main, publish the commits and a PR with exact test results and remaining limitations. Merge only under applicable user authorization and passing branch/merge checks; otherwise leave a reviewable branch.

## Verification boundaries

- Unit tests validate repository tooling and regression fixtures.
- Static checks validate metadata, references, catalog, registry and evaluation-document consistency within their documented parser scope.
- Evaluation cases specify what an agent should do; results remain `not-run` until there is a real model invocation and inspectable output.
- No game engine, human playtest, GPU resource measurement or cross-platform determinism is implied by documentation tests.
- Re-read remote heads before updates, use non-force ref changes, preserve concurrent edits, and record each remote commit. A tree object alone is not a synchronized commit.

## Deferred

LOD/baking, animation retargeting, turn resolution, build/release and the remaining semantic audit of older skills are not part of the six-skill batch.
