# Engineering skills implementation record

Baseline: `a38072a5f9e0c5c23325603b5efdd17b49eef70c` (181 SKILL.md files).
Branch: `feat/engineering-skills-2026-09-13`. This record describes delivered documentation/tooling, not a completed engine implementation or an LLM benchmark.

## Reproduced baseline defects

The unchanged baseline produced 41 unit tests with one failure, and six static errors: four missing/out-of-pack references, one malformed sprite table and a stale catalog. The recovery workflow retains a tracked-source ZIP even on failure, without credentials or write permissions and without suppressing failing checks.

## Delivered changes

| Area | Outcome |
|---|---|
| Packaging | Runtime references moved inside skills/references; old docs URLs remain redirects. A copy-installed pack is checked independently of the source tree. |
| Sprite/VFX ownership | sprite-catalog owns the inventory; sprite-atlas owns slicing/packing/import metadata; vfx-generate is the generator; vfx-prompt preserves old aliases through delegation. |
| Generic planning | Core challenge/decision replaces mandatory combat; validation includes noncombat games and unknown failure attribution. |
| Engineering | game-state-flow, asset-runtime, procedural-generation, terrain-surface, world-streaming and physics-interaction each have bounded responsibilities, selectable modes, procedures, outputs and acceptance scenarios. |
| Supporting data | Six JSON contract examples, 18 authored evaluation scenarios, 54 criterion descriptions; no generated example is labeled as a measured pass. |
| Registry | Six explicitly scoped engineering entries: modes must match their actual Modes tables, dependencies must exist, examples/cases must be consistent. Older skills are not implicitly registered or semantically certified. |
| Evidence tooling | Offline imported-record validation with suite/response hashes, full criteria, fixed denominator and explicit not-run/blocked states. No model call, automatic answer scoring or invocation authenticity guarantee. |
| Discovery/docs | Catalog, shared ownership and all five README locales expose the new skills and explain verification limits. Direct dispatcher seed updates are blocked. |

The originally separate runtime and world drafting steps were combined into one six-skill commit after verifying all local references together. Their outputs and test cases remain separate per skill.

## Remote checkpoints

- `2f415a6450ad58f2938c5f577f6834dd1759e021`: plan and diagnostic snapshot retention; baseline failures remain visible.
- `dd45fc17f35d7b071a2e9674dbfd280209a1c8a7`: packaging/ownership/noncombat repair; 47 unit tests and 181 static skill checks passed.
- `8f2d6d50d2d97fb4c6013a771885baf76227369c`: six engineering contracts and scenarios; 49 unit tests and 187 static skill checks passed.
- `9852016f63e9086fdbd81b40d3109d894915aba9`: scoped registry/evidence validator and CI integration; 70 unit tests passed.
- Documentation completion follows these commits; the PR records its exact final head and CI runs. The direct dispatcher seed write was blocked and was not published.

## Local final verification

`python -m unittest discover -s tests -v`: **73 tests run: 72 passed, 1 skipped**. The skipped test retains the expected direct dispatcher routes; it is explicitly pending because that write was blocked. It is not counted as a pass.

`python tools/skill_quality.py --check-catalog`: **187 skills inspected; 0 static errors**, within the documented Markdown/metadata/catalog scope.

`python tools/engineering_quality.py`: **6 registered skills, 18 cases; pass 0 / fail 0 / blocked 0 / not-run 18**. Exit 0 validates structure only.

`python tools/engineering_quality.py --require-passed`: **exit 1 as expected** because no real model results were supplied. The gate was not weakened to make CI claim behavioral success.

`git diff --check`: passed. Before every publish checkpoint, the uploaded Git tree is compared with the locally tested tree. Local scratch commit IDs are not presented as remote commits.

New packaging tests, missing-skill tests, evidence-validator tests and multilingual documentation tests were observed failing before their corresponding repairs. The direct dispatcher-route test also failed during development and remains explicitly skipped, not repaired, because the final dispatcher write was blocked. Synthetic evidence fixtures exercise validation only and are explicitly marked as such; they are not evaluations of a model. Changes to a skill or case invalidate previously imported results through the suite fingerprint.

## Blocked write

The final `skills/dispatcher/SKILL.md` write was rejected with: "This tool call was blocked by OpenAI because we couldn't determine the safety status of the request." No alternate write was attempted. The existing dispatcher remains unchanged; it can still discover the new skills through its catalog fallback or an explicit skill name. Broad-phrase direct routing to the six new contracts has not been delivered or behaviorally validated. Resume this narrowly scoped change only when the write is permitted, then remove the explicit skip and verify the preserved route expectations.

## Remaining evidence and scope

Real model routing/implementation comparisons, engine integrations, GPU-memory measurements, physics/world playtests and independent native-language review are **not-run**. Hash/record consistency cannot prove an evaluator told the truth or that an answer is correct. Follow [EVALUATION.md](../EVALUATION.md) for actual run records.

Deferred additions: LOD/baking, animation retargeting, turn resolution and build/release. The broader semantic audit of older skills also remains separate. The branch/PR is reviewable and must not be confused with an automatic merge into main.
