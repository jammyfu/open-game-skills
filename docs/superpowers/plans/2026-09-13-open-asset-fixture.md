# Open asset fixture implementation plan

## Goal and boundaries

Add a reusable, offline-first asset-selection skill for test fixtures. Prefer fit-for-purpose, primary-source CC0 assets; allow reviewed CC-BY only when attribution is explicitly accepted. TheLegendOfTrump remains a separately authorized asset-only fixture, never a gameplay oracle or a presumed CC0 library.

Baseline: e3d31d94fa314869daeb756ef79d1750c7602b23. The actual baseline has 188 skills, 254 passing unit tests and TWO seeded manifests (dialogue-beat and input-combo-test). Prior chat's 188/188 reviewed statement was incorrect; this task will not silently relabel them.

## Design

Keep SKILL.md, curated metadata, source notes, request examples and standard-library scripts inside skills/assets/open-asset-fixture so copy installs remain self-contained. Curated pack capabilities are discovery hints, not assertions that every member satisfies them. Asset selection cannot prove decoding, engine import, gameplay behavior, authorship or legal authenticity.

Alternatives: online scraping on every test is fragile and may violate service terms; automatic generation before library lookup costs tokens and weakens reproducibility. Use deterministic metadata matching and verified local locks first, official acquisition only for missing inputs, synthetic fixtures for exact edge cases, generation last.

## Commit sequence

1. Write and run failing selection and integrity tests. Add primary-source registry, deterministic matcher, bounded local file locks, request examples and source guide. The tools can run independently before skill registration. Run the exact staged tree before a coherent main commit.
2. Register the skill and per-skill scenarios; update catalog/coverage. Add routing, test preparation hooks, five-language README links and integration tests. Run full tests and verify exact remote tree and CI.

## Acceptance

- Kind, required capability, format and license filters are hard constraints; no unrelated fallback.
- Distinguish free Standard from paid Pro/Source. Keep unsupported/unknown licenses out of automatic selection.
- Return explanations, source URLs, version observations, inspection requirements and not-run runtime status.
- Use normal/boundary/adversarial case definitions; do not report them as executed model tests.
- Fixture locks hash every selected file and license evidence, preserve attribution, reject traversal/symlinks/executable extensions and detect stale metadata/tampering.
- Do not download whole catalogs, bypass login/rate limits, copy previews, train models, run external project code or change gameplay to match an asset.
- Write directly to main as authorized, using fast-forward updates only; re-read main before each publish.
