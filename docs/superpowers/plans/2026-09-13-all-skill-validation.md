# All-Skill Validation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a complete per-skill validation corpus and repair loop covering every skill in `open-game-skills`, with immutable real-project fixtures and evidence-honest results.

**Architecture:** Generate a deterministic one-to-one case inventory from the real skill catalog, validate each case with Python unittest gates, and keep behavioral scenarios/evidence separate from static checks. Use `TheLegendOfTrump@8871ee8` as a pinned real-game fixture for applicable browser/3D/runtime skills.

**Tech Stack:** Python 3.12, stdlib `unittest`, JSON, existing `tools/skill_quality.py` and `tools/engineering_quality.py`, GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-09-13-all-skill-validation-design.md`

## Global Constraints

- Baseline branch is `feat/engineering-skills-2026-09-13`; do not implement directly on `main`.
- Every actual `SKILL.md` has exactly one case file; no orphan case files.
- Behavioral results are `not-run` unless response evidence and criterion judgments exist.
- External fixture refs are pinned to immutable commits; no live-branch dependency in deterministic CI.
- Do not mass-rewrite legacy descriptions without reviewing the affected skill cluster.
- Commit coherent repair batches and run the full suite after each batch.

---

### Task 1: Full-coverage case index and generator

**Files:**
- Create: `tests/skills/README.md`
- Create: `tests/skills/coverage.json`
- Create: `tests/skills/cases/**/<skill>.json`
- Create: `tools/skill_case_seed.py`
- Create: `tests/test_all_skill_coverage.py`

**Interfaces:**
- Consumes: `skills/catalog.json` and actual `skills/**/SKILL.md` files.
- Produces: deterministic `coverage.json`; `seed_cases(root: Path) -> dict[str, dict]`; one case file per skill.

- [ ] Write `test_all_skill_coverage.py` first so the baseline fails because `tests/skills/coverage.json` and case files do not exist.
- [ ] Run the focused test and capture the expected failure.
- [ ] Implement `skill_case_seed.py` with deterministic path/category mapping and three scenario classes.
- [ ] Generate all current case files and coverage index.
- [ ] Re-run the focused test and full unittest suite.
- [ ] Commit the harness and generated corpus.

### Task 2: Pinned real-game fixture support

**Files:**
- Create: `tests/skills/fixtures/the-legend-of-trump.json`
- Modify: `tools/skill_case_seed.py`
- Modify: applicable `tests/skills/cases/**.json`
- Test: `tests/test_all_skill_coverage.py`

**Interfaces:**
- Consumes: immutable fixture commit `8871ee8293f815eff848d1064f05735cfe45ced8` and known repository paths.
- Produces: validated fixture IDs and per-case optional `fixtures` references.

- [ ] Add a failing fixture test requiring immutable 40-hex commit and repository/path declarations.
- [ ] Add the manifest for the React/Three.js project and path groups for runtime, assets, UI, tests and build.
- [ ] Seed relevant skills with the fixture ID; do not force unrelated skills onto the fixture.
- [ ] Run focused and full tests.
- [ ] Commit fixture integration.

### Task 3: Deterministic per-skill contract checks

**Files:**
- Create: `tools/skill_test_runner.py`
- Create: `tests/test_all_skill_contracts.py`
- Modify: `tests/skills/coverage.json` only if schema needs deterministic metadata.

**Interfaces:**
- Produces: `load_case(path)`, `check_skill_case(root, case) -> list[str]`, `check_all(root) -> dict`.
- Checks structure/package links/catalog identity/acceptance signals and reports legacy trigger-description candidates without automatically rewriting them.

- [ ] Write failing tests for missing acceptance signals, path mismatch, orphan references and malformed scenario classes.
- [ ] Implement the minimal runner.
- [ ] Run against all skills and save the first real failure set.
- [ ] Fix systemic parser/harness defects before editing skills.
- [ ] Commit the contract runner when the harness itself is green.

### Task 4: Routing coverage

**Files:**
- Create: `tests/test_all_skill_routes.py`
- Modify: `tools/skill_test_runner.py`
- Modify: `skills/dispatcher/SKILL.md` only for demonstrably missing high-value direct routes.

**Interfaces:**
- Explicit skill-name routing must resolve via catalog for every skill.
- Dispatcher direct-route tests are only required for authored shortcuts; ambiguous natural-language selection stays behavioral/not-run.

- [ ] Write failing route tests for catalog fallback and known engineering shortcuts.
- [ ] Verify the existing pending dispatcher shortcut failure before editing.
- [ ] Implement/fix routing without changing project modes implicitly.
- [ ] Run focused and full tests.
- [ ] Commit routing repairs.

### Task 5: First full audit and repair batches

**Files:**
- Modify: failing `skills/**/SKILL.md` files in small coherent clusters.
- Modify: corresponding case files, changing `review_state` from `seeded` to `reviewed` only after manual inspection.
- Create/modify: `docs/audits/2026-09-13-all-skill-validation.md`.

**Interfaces:**
- Canonical processing order is case path order.
- Each audit row records skill, failure class, repair, deterministic result, behavioral evidence status.

- [ ] Run the full runner and group real failures by root cause.
- [ ] Repair the first cluster, starting with package/reference and route ownership defects, then discovery-description defects.
- [ ] Re-run focused tests before and after each fix so the defect is demonstrated.
- [ ] Re-run the complete unittest/static suite after each cluster.
- [ ] Commit each coherent cluster separately.

### Task 6: CI gate and PR evidence

**Files:**
- Modify: `.github/workflows/skill-quality.yml`
- Modify: `README*.md` only for test commands/coverage policy if needed.
- Modify: PR #2 body and audit record.

**Interfaces:**
- CI fails if skill/case coverage drifts or deterministic checks fail.
- CI must not claim behavioral passes from absent evidence.

- [ ] Add CI commands for all-skill coverage and runner tests after a failing workflow-level regression test if needed.
- [ ] Run the full local suite and static checker.
- [ ] Push a coherent final branch commit and verify branch + PR merge CI.
- [ ] Update PR #2 with exact counts, remaining `not-run` evidence and repaired skill clusters.
