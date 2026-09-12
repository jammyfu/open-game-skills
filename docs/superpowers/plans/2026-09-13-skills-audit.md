# Skills audit and hardening plan

Baseline: `fd1157b137dea18d3d38c45011d27227ddd481d8`.
Work branch: `improve/skills-audit-2026-09-13`. Do not force-push or change main.

## Goal and boundaries

Review every existing SKILL.md, preserve the engine-neutral architecture, fix incorrect routing and technical contracts, and add reproducible repository checks. This is a skills/documentation repository, not an executable game. Static checks do not establish engine compatibility, agent behavior, or human playability.

## Deliverables and commit sequence

1. Establish a reproducible, read-only CI source snapshot and baseline inventory. No repository credentials belong in the artifact.
2. Add tested skill validation and safe installation; fix installation instructions in every README locale. Preserve existing unrelated files and artwork.
3. Repair dispatcher modes, priority, alias handling, and bounded progressive loading. Add a complete generated catalog and routing evaluation cases.
4. Correct timing, collision, camera, networking, engine and asset contracts. Add focused counterexamples and regression checks.
5. Improve persistence, entitlement, accessibility and evidence handling. Document the individual review outcome and a concrete verification scenario for every skill.
6. Run the full checks against the actual repository, inspect the changed files, and open a reviewable PR. Report exact commit hashes, checks, and remaining untested runtime behavior.

Each implementation batch must run its focused tests before commit. Verification records distinguish pass, fail, blocked and not-run; no fabricated playtest or model-evaluation results. When a direct checkout is unavailable, use the connected GitHub API for writes and GitHub Actions for full-tree checks.

## Design decisions

- Keep concise specialized skills rather than loading the entire catalog on each task.
- A common contract owns shared execution and evidence rules; referenced dependencies are not an instruction to recursively load every skill.
- Preserve intentional game-design choices, but label tuning seeds as recommendations rather than universal engine facts.
- Use normal fast-forward branch updates. Stop on concurrent changes rather than overwriting them.
- CI uses contents:read and pinned official actions. It never pushes changes, executes model-generated remote instructions, or publishes a release.
