# Open Game Assets plugin package

This directory stores release metadata for the **skills-only** Open Game Assets plugin.
The canonical skill source remains at:

`skills/assets/open-asset-fixture/`

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
