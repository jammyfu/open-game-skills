# Marketplace submission guide

This document describes how to publish the repository's portable plugins through a GitHub-backed plugin marketplace later. It does **not** create or register a marketplace by itself.

The current portable plugin source is:

```text
plugins/open-game-assets/
├── plugin.json
└── README.md
```

The distributable package is built from the canonical skill source with:

```bash
python tools/build_open_game_assets_plugin.py \
  --zip dist/open-game-assets.zip
```

The ZIP root must contain:

```text
plugin.json
skills/
  open-asset-fixture/
    SKILL.md
    assets/
    reference/
    scripts/
```

Do not include a nested `skills/assets/open-asset-fixture/` path in the portable plugin. Do not add MCP, App, or Marketplace files to the plugin ZIP unless the plugin actually uses those capabilities.

## 1. Marketplace vs public OpenAI directory

Two different distribution paths exist and should not be confused:

1. **GitHub Marketplace import for a ChatGPT workspace** — a workspace admin imports a GitHub repository containing a marketplace manifest. The workspace then controls installation policy, roles, required apps, and sync behavior.
2. **OpenAI public plugin directory submission** — the plugin itself is submitted through OpenAI's plugin submission process for public review and publication. This is separate from a private/workspace GitHub marketplace.

This document focuses on the first path: a GitHub-backed marketplace. Public directory submission should use a separate release checklist.

## 2. Recommended repository layout

When Marketplace support is enabled later, add:

```text
.agents/
└── plugins/
    └── marketplace.json
```

Keep the actual plugin source independent:

```text
plugins/
└── open-game-assets/
    ├── plugin.json
    └── README.md
```

Do not copy the canonical skill source by hand. Build the release package from:

```text
skills/assets/open-asset-fixture/
```

using `tools/build_open_game_assets_plugin.py`.

## 3. Marketplace manifest

The supported Codex marketplace manifest location is:

```text
.agents/plugins/marketplace.json
```

A future manifest should list each plugin and its source. Keep plugin names stable after users begin installing them.

Before committing the manifest:

- validate every referenced plugin path/repository;
- pin external plugin sources to a reviewed branch, tag, or commit when reproducibility matters;
- ensure every plugin has a valid `plugin.json`;
- ensure `skills/<name>/SKILL.md` directories are direct children of the plugin's `skills/` directory;
- do not reference paid, private, or unavailable resources as if they were bundled;
- review all new marketplace entries before merge, because a later marketplace sync can import newly added entries.

## 4. Versioning policy

Recommended policy:

```text
main         development and continuous verification
v0.1.0       first stable Open Game Assets release
v0.1.1       backwards-compatible fix
a fixed SHA  reproducible workspace rollout
```

`plugin.json` should use semantic versions. Increase the version whenever the distributable plugin behavior or package contents change materially.

For controlled company use, prefer a release tag or reviewed commit over continuously tracking `main`.

## 5. Build and verify before Marketplace import

Run the repository checks first:

```bash
python -m unittest discover -s tests -q
python tools/skill_quality.py --check-catalog
python tools/engineering_quality.py
```

Build the plugin:

```bash
rm -rf dist/open-game-assets
python tools/build_open_game_assets_plugin.py \
  --output dist/open-game-assets

python tools/build_open_game_assets_plugin.py \
  --zip dist/open-game-assets.zip
```

Inspect the result. At minimum verify:

- `plugin.json` is at the package root;
- exactly the intended Skill directories are under `skills/`;
- no `.git`, cache files, build junk, Marketplace manifest, MCP configuration, or `.app.json` was accidentally included;
- packaged Skill files match the canonical source;
- the plugin can be installed in a clean test environment;
- positive and negative user scenarios behave as documented.

Repository CI passing does not prove an external game runtime, downloaded asset, decoder, or human playtest succeeded.

## 6. Import a GitHub Marketplace into ChatGPT workspace

For a supported workspace, an admin can import a marketplace from GitHub:

1. Open **Workspace settings → Plugins**.
2. Select **Add → Import marketplace**.
3. Enter the repository URL, for example:

   ```text
   https://github.com/jammyfu/open-game-skills
   ```

4. If `.agents/plugins/marketplace.json` is at the repository root structure shown above, leave **Path** empty. If the marketplace is located inside a subdirectory, enter that directory only — not the manifest filename.
5. Optionally choose a branch, tag, or commit. For reproducible rollout, prefer a release tag or fixed commit.
6. Authorize GitHub access when prompted.
7. Review import results.
8. Open the imported plugin and configure its workspace installation policy and any required app access.
9. Test with an eligible workspace member before broad rollout.

The GitHub account used for import must be able to read the marketplace repository and every repository referenced by the manifest.

## 7. Sync behavior

Imported GitHub marketplaces can be synchronized as the repository changes. Workspace admins can use **Sync now** from the Marketplace settings instead of waiting for scheduled synchronization.

Important operational rule: review repository changes before merging them. Marketplace sync can introduce newly added plugin entries without a separate per-plugin source-review step.

If an updated plugin is invalid, the workspace should retain the last valid imported version while reporting the sync error. Fix the source and sync again.

Removing a plugin entry from the repository does not automatically mean that an already imported workspace copy is deleted. Treat marketplace source removal and workspace deletion as separate operations.

## 8. Workspace policies remain in ChatGPT

Repository metadata does not override workspace administrator policy.

After import, admins still decide:

- whether a plugin is Available or automatically Installed;
- which roles can use it;
- whether required apps/connectors are enabled;
- authentication and provider permissions;
- allowed actions and other workspace controls.

Importing or synchronizing a marketplace does not automatically connect an individual user's third-party accounts.

## 9. Open Game Assets rollout checklist

Before adding `open-game-assets` to a future Marketplace manifest:

- [ ] `plugin.json` version is correct.
- [ ] `python tools/build_open_game_assets_plugin.py --zip ...` succeeds.
- [ ] Full repository CI is green.
- [ ] The built ZIP contains `plugin.json` at root.
- [ ] The built ZIP contains `skills/open-asset-fixture/SKILL.md`.
- [ ] No nested `skills/assets/open-asset-fixture` path exists in the portable ZIP.
- [ ] No Marketplace, MCP, App, secret, credential, or cache file is inside the ZIP.
- [ ] CC0/CC-BY source metadata is still accurate for all curated entries.
- [ ] No paid Pro/Source asset is represented as the free edition.
- [ ] At least five positive usage scenarios have been manually exercised.
- [ ] At least three negative/adversarial scenarios have been exercised.
- [ ] Missing asset acquisition/import/runtime evidence remains `blocked` or `not-run`, not `pass`.
- [ ] A release tag or reviewed commit has been selected for rollout.

## 10. Suggested positive tests

1. Find a CC0 2D sprite/tileset fixture for a platformer test.
2. Find a rig/animation candidate and reject static-only geometry for a skeletal test.
3. Find an audio fixture for impact/UI feedback and retain license provenance.
4. Find a VFX/particle candidate while distinguishing particle textures from native effect data.
5. Reuse a byte-verified local lock ahead of a remote candidate.

## 11. Suggested negative tests

1. Request a paid Pro/Source asset while claiming it is free — reject the assumption.
2. Request an asset without sufficient license evidence — leave it unmatched or blocked.
3. Ask the plugin to mark an engine test as passed before decoding/import/runtime execution — keep it `not-run`.

## 12. Public OpenAI plugin directory is a separate step

A GitHub marketplace import is for controlled workspace distribution. It is not the same as public OpenAI directory publication.

When preparing for public publication later, maintain a separate checklist for:

- developer/organization identity;
- plugin listing metadata and icon;
- support contact;
- privacy policy and terms;
- positive and negative review scenarios;
- release notes;
- public submission and review state.

Do not add public-directory claims to the repository until the plugin has actually been approved and published.

## Official references

Current OpenAI documentation to re-check before creating the Marketplace manifest or importing it:

- OpenAI Help Center — **Importing and syncing plugin marketplaces from GitHub**
- OpenAI Help Center — **Plugins in ChatGPT and Codex**
- OpenAI Developers — Codex / Plugins documentation

These product flows can change. Re-check the official documentation immediately before release rather than treating this file as an immutable specification.
