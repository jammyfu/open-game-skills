# Per-skill test corpus

Every `skills/**/SKILL.md` has exactly one JSON case file under `tests/skills/cases/`.
`coverage.json` is deterministic and must match both `skills/catalog.json` and the actual filesystem.

Seeded cases reference a shared normal/boundary/adversarial scenario profile to avoid duplicating boilerplate. Reviewed cases expand to tailored scenarios. These are authored test inputs, not measured results. Generated cases begin as `review_state: seeded`; move a case to `reviewed` only after inspecting the skill and tailoring/confirming the scenario and criteria. Behavioral outcomes stay outside the case definition and must never be inferred from static checks.

Regenerate seeded coverage after adding or renaming a skill:

```bash
python3 tools/skill_case_seed.py --write
python3 -m unittest tests.test_all_skill_coverage -v
```

Do not use `--overwrite-seeded` after manually editing a seeded case unless regeneration is intentional. Reviewed cases are never overwritten by the generator.
