# Open asset fixture recovery and integration

## Baseline and scope

The interrupted response had already published `86bdc0af0ad4a832992731179f3c8454aee9f072` (tree `e331929c17f2e3b17c713f5c6657e074528a7fec`). Its GitHub Actions run 34756733823 succeeded. The archive was restored and its complete tree matched that baseline before editing.

That commit provided a curated matcher and local byte locks but no registered SKILL.md, dispatcher entry or fixture-preparation hook. This continuation preserves those tools and completes the integration on main. The request is asset sourcing for tests, not replacement of deliberate artwork or an external game's implementation.

## Deliverables

- `open-asset-fixture`: library-first and pinned-only modes, packaged references/scripts, explicit acquisition/import boundaries.
- A 26-entry primary-source catalog: 25 CC0 candidates and one opt-in CC-BY-3.0 candidate. These are pack-level discovery leads, not 26 downloaded/decoded fixtures.
- 28 illustrative skill profiles and nine logic-only no-art defaults. Profiles never override a test's explicit requirements.
- An executable offline preparation report covering all requested skills, retaining missing profiles and requirements in the denominator.
- Local byte/license-evidence lock verification, with format-specific capability bindings and query-aware local ranking.
- Skill catalog/coverage/case registration; dispatcher and gameplay harness/validation preparation hooks; five README locales.

The primary source guide and commands are in [sources](../../skills/assets/open-asset-fixture/reference/sources.md) and [usage](../../skills/assets/open-asset-fixture/reference/usage.md). Exact editions matter: Quaternius Standard and KayKit FREE are distinct from paid Pro/Extra/Source downloads. Effekseer EffectMaterials explicitly targets 1.7. Asset licenses do not replace API/service terms.

## Regression evidence

The new preparation/registration suite first failed while the skill and hooks were absent. Three focused lock tests then failed on mixed-format capability leakage and irrelevant alphabetic local ordering. They passed after adding explicit capability-to-format bindings and deterministic relevance ranking. No tests were skipped or relaxed to hide an unimplemented runtime.

Final local commands:

```sh
python -m unittest discover -s tests -q
python tools/skill_quality.py --check-catalog
python tools/engineering_quality.py
python tools/skill_test_runner.py
python skills/assets/open-asset-fixture/scripts/prepare_assets.py --skill materials
python skills/assets/open-asset-fixture/scripts/prepare_assets.py --all-skills skills/catalog.json
python skills/assets/open-asset-fixture/scripts/prepare_assets.py --skill materials --pinned-only
git diff --check
```

Results at this change: 304 unit/contract tests pass, zero skips; 189 skill documents and zero static/hard contract errors. The all-skill preparation inventory retains 189 entries: 28 need acquisition, nine do not need artwork for their default logic tests, and 152 need explicit asset requirements. Its exit 2 is intentional: unresolved input requirements are not a successful readiness gate. Pinned-only with no local fixtures is blocked.

The separate six-engineering-skill evidence validator reports all 18 behavior scenarios as not-run. No game, image/audio decoder, browser renderer, external model, or human playtest was executed here. Local lock tests use explicitly synthetic bytes and license text; they prove tool behavior, not third-party asset authenticity. A binary retrieval attempt was unavailable in the execution environment, so no third-party asset binaries are bundled or reported as acquired. Acquisition requires an available authorized download tool and subsequent file-level inspection.

## Remaining review debt

The actual baseline had two seeded skill case manifests (`dialogue-beat`, `input-combo-test`), despite an earlier chat summary claiming all were reviewed. They remain unchanged. With the new skill the counts are 189 total, 187 reviewed specification manifests, two seeded. `studio-column` also retains an acceptance-signal review candidate. A reviewed manifest is not an executed behavior result.

`TheLegendOfTrump@8871ee8293f815eff848d1064f05735cfe45ced8` remains separately authorized asset-sample-only input. Its fixture record is unchanged; its unfinished gameplay, code/tests and presumed artwork rights are not imported into this catalog or used as an oracle.
