# All-Skill Validation Design

## Goal

Every installed `SKILL.md` must have an explicit, reviewable test definition. The repository must fail CI when a skill is added, renamed, removed, or materially changed without corresponding coverage. Deterministic checks and real behavioral evidence are separate: a static pass never becomes a claimed LLM, engine, or human-playtest pass.

## Baseline

- Implementation branch: `feat/engineering-skills-2026-09-13` at `4524316b92f789fb17b693983bed47767ab41230`.
- Skill inventory at baseline: 187 `SKILL.md` files.
- Existing suite at baseline: 73 tests, 72 pass, 1 explicitly skipped dispatcher-direct-route assertion.
- External real-project fixture: `jammyfu/TheLegendOfTrump` pinned to `8871ee8293f815eff848d1064f05735cfe45ced8`.
- External fixtures are references, not mutable dependencies: tests record immutable commit/path facts and do not silently follow a moving branch.

## Test layers

Each skill gets four independent layers.

1. **Structure** — frontmatter, name/path identity, local references, package boundaries, catalog inclusion.
2. **Contract** — trigger description, ownership/boundary signals, modes or explicit mode-less status, acceptance/evidence language, dependency targets.
3. **Routing** — explicit-name routing is always testable; direct natural-language routing is tested only where a deterministic route exists. Ambiguous model-selection behavior is a behavioral case, not a regex pass.
4. **Behavioral scenarios** — at least normal, boundary, and adversarial prompts. Results default to `not-run`. `pass` requires stored response evidence and criterion-by-criterion judgment.

## Repository layout

```text
tests/
  skills/
    README.md
    coverage.json
    fixtures/
      the-legend-of-trump.json
    cases/
      2d/<skill>.json
      assets/<skill>.json
      disciplines/<skill>.json
      engines/<skill>.json
      root/<skill>.json
      dispatcher/<skill>.json
      router/<skill>.json
    results/
  test_all_skill_coverage.py
  test_all_skill_contracts.py
  test_all_skill_routes.py
tools/
  skill_case_seed.py
  skill_test_runner.py
```

`coverage.json` is generated deterministically from `skills/catalog.json` plus the actual filesystem and names the exact case file for every skill. CI requires one-to-one equality: no missing cases, no orphan cases, no duplicate names.

## Case schema

Each case file records:

- schema version;
- skill name and canonical skill path;
- category;
- deterministic checks (`description_trigger`, `acceptance_signal`, `package_links`, `explicit_name_route`);
- three scenario classes: `normal`, `boundary`, `adversarial`;
- each scenario has a prompt and explicit criteria;
- optional fixture references. `TheLegendOfTrump` references use immutable commit + repository-relative paths.

Generated cases are seeds, not proof of semantic quality. A seeded case remains marked `review_state: seeded` until manually reviewed or repaired. This keeps complete coverage without pretending every scenario was hand-authored.

## Real-project fixture policy

`TheLegendOfTrump` is used where its actual stack or artifacts are relevant: React, Three.js / React Three Fiber, Vite, TypeScript, GSAP, model optimization, browser input, UI, camera, runtime assets, performance, gameplay capture and related skills. The fixture manifest records only paths and immutable hashes/commit identifiers needed to formulate scenarios; large assets are not copied into this repository.

A skill that does not apply to that game must not be forced onto it. Economy/IAP/network/fighting-specific skills use self-contained synthetic scenarios unless another real fixture is added later.

## Repair loop

For each skill in canonical path order:

1. run its deterministic focused checks;
2. inspect the three scenarios and current skill text;
3. if the test exposes an actual defect, record the failure before editing;
4. fix the owning skill or shared contract, not a downstream symptom;
5. rerun the focused case;
6. rerun the full deterministic suite;
7. commit a coherent cluster of fixes;
8. keep unexecuted behavioral scenarios as `not-run`.

No assertion is weakened merely to obtain green CI. If a rule is wrong, change the rule and explain why in the commit/audit record.

## Initial quality gates

The first full pass enforces these mechanical facts across all skills:

- exact catalog/case coverage;
- unique valid names and paths;
- no package-breaking references;
- frontmatter description is discoverable and nonempty;
- case schema has normal/boundary/adversarial coverage;
- explicit-name route exists through catalog fallback even if dispatcher has no special shortcut;
- fixture references are pinned and valid in manifest form;
- `pass` cannot be recorded without response evidence and a complete judgment.

Description wording (`Use when ...`) is reported as a repair candidate for legacy skills, then fixed in reviewed batches rather than mass-rewritten blindly.

## Success criteria

Phase 1 is complete when all 187 current skills have valid case files and the deterministic full-suite gate is green. Phase 2 is iterative semantic repair: every reviewed skill moves from `seeded` to `reviewed`, with behavioral evidence staying `not-run` until a model/engine/human run is actually captured. Future skills cannot merge without a case file.
