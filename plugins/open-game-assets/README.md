# Open Game Assets plugin package

This directory stores release metadata for the **skills-only** Open Game Assets plugin.
The canonical skill source remains at:

`skills/assets/open-asset-fixture/`

## Usage

For installation, matching modes, common commands, fixture locking, CI usage, ChatGPT/Codex prompts, license handling, and practical 2D/3D/audio/VFX examples, see:

[`docs/OPEN_GAME_ASSETS_USAGE.md`](../../docs/OPEN_GAME_ASSETS_USAGE.md)

Quick examples:

```sh
# Prepare assets for one or more skills
python3 skills/assets/open-asset-fixture/scripts/prepare_assets.py --skill materials
python3 skills/assets/open-asset-fixture/scripts/prepare_assets.py --skill animation-blend audio-feel juice-vfx

# Scan all skills and keep unresolved requirements visible
python3 skills/assets/open-asset-fixture/scripts/prepare_assets.py --all-skills skills/catalog.json --output asset-plan.json

# Run offline/reproducible preparation using only pinned fixtures
python3 skills/assets/open-asset-fixture/scripts/prepare_assets.py \
  --skill juice-vfx \
  --root /absolute/fixtures \
  --locks /absolute/fixture.lock.json \
  --pinned-only
```

Typical natural-language invocation after installing/uploading the plugin:

```text
Use Open Game Assets to prepare suitable open-licensed test assets for this game project. Reuse verified local fixtures first and do not silently relax required formats or capabilities.
```

## Build the portable plugin

Do not hand-edit a second copy of the skill here. Build a portable package with:

```sh
python tools/build_open_game_assets_plugin.py --output dist/open-game-assets
python tools/build_open_game_assets_plugin.py --zip dist/open-game-assets.zip
```

The generated package has the submission-compatible layout:

```text
plugin.json
skills/
  open-asset-fixture/
    SKILL.md
    assets/
    reference/
    scripts/
```

This release layer intentionally contains no Marketplace manifest, MCP server configuration, `.app.json`, or hooks. Those are separate distribution/integration decisions.
