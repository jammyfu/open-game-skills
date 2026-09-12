# open-game-skills

<p align="center">
  <img src="docs/logo-banner.svg" alt="open-game-skills" width="640"/>
</p>

<p align="center">
  <b>English</b> · <a href="README.zh.md">中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a>
</p>

<p align="center">
  <strong>Generic Agent Skills for making games.</strong><br/>
  Systems first. Studios and engines are columns you stack, not games you copy.
</p>

<p align="center">
  <a href="https://github.com/jammyfu/open-game-skills"><img alt="repo" src="https://img.shields.io/badge/github-jammyfu%2Fopen-game-skills-e76f51?style=flat-square"/></a>
  <img alt="license" src="https://img.shields.io/badge/license-MIT-2a9d8f?style=flat-square"/>
  <img alt="lang" src="https://img.shields.io/badge/docs-EN%20ZH%20JA%20KO-e9c46a?style=flat-square"/>
</p>

Open-source skill cluster for OpenClaw, Claude Code, Codex, and Cursor.
**Ask the column first, then write code.** Do not start from an engine API or from a finished title.

## What this is

Questions and clocks you can stack:

- **Disciplines** decide how information, difficulty, gear, wear, combat, cameras, races, and bosses work.
- **Engine adapters** only bind six primitives (`poll_input`, `now_logical_frame`, `play_pose`, `query_hits`, `apply_knockback`, `juice_hook`).
- **Studio / genre names** pick columns. They do not author a second rulebook.

Not an engine API manual. For node names, pair with [awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills).

## Logo

Three stacked tiles + a facing chevron.

| Tile | Meaning |
|---|---|
| Teal bottom | Engine adapter |
| Gold middle | Discipline |
| Coral top | Preset column |
| Chevron | The player's own plan |

[`logo.svg`](logo.svg) · [`docs/logo-banner.svg`](docs/logo-banner.svg)

## Stack

```
engine adapter     three.js / PixiJS / Godot / Unity / Unreal / custom
        ↓
discipline         map · feel · camera · gear · race · boss · budget …
        ↓
one studio column  nintendo-zelda · capcom · konami · blizzard · indie
one genre column   action-adventure · fighting · platformer · racing …
```

One combat column per actor. One wear column per item slot. A studio may pick columns; it may not invent a second clock.

## Ask before coding

| System | Question |
|---|---|
| Map | How is information earned? Who may drop pins? |
| Difficulty | Space, resources, or numbers — and which scaler? |
| Equipment | Replace, tree, affix, fuse, or eternal — per slot? |
| Durability | Consume, sharpness, repair, or unbreakable? |
| Combat | short-special / long-cancel / commit-whitelist / coyote-platform |
| Race | drift-kart / boost-rail / grip-weight / combat-arena |
| Platform | phone / handheld-dock / living-room / handheld-pc / desktop |
| Engine | Which of the six primitives? |

When the user says *generic*: no world-level-sync, no full-map quest arrows, no mixing shatter + endgame tree on the same instance, no silent rubber-band.

## On main

**Feel / camera / move:** [action-feel](skills/disciplines/action-feel/SKILL.md) · [input-design](skills/disciplines/input-design/SKILL.md) · [camera-anti-clip](skills/disciplines/camera-anti-clip/SKILL.md) · [ik-foot-locking](skills/disciplines/ik-foot-locking/SKILL.md) · [locomotion](skills/disciplines/locomotion/SKILL.md)

**World:** [world-map](skills/disciplines/world-map/SKILL.md) · [level-design](skills/disciplines/level-design/SKILL.md) · [puzzle-design](skills/disciplines/puzzle-design/SKILL.md) · [difficulty-design](skills/disciplines/difficulty-design/SKILL.md)

**Growth:** [equipment-progression](skills/disciplines/equipment-progression/SKILL.md) · [durability-economy](skills/disciplines/durability-economy/SKILL.md)

**Versus / race / boss:** [fighting-design](skills/disciplines/fighting-design/SKILL.md) · [combo-design](skills/disciplines/combo-design/SKILL.md) · [racing-feel](skills/disciplines/racing-feel/SKILL.md) · [racing-design](skills/disciplines/racing-design/SKILL.md) · [boss-design](skills/disciplines/boss-design/SKILL.md) · [balance-design](skills/disciplines/balance-design/SKILL.md) · [netcode-feel](skills/disciplines/netcode-feel/SKILL.md)

**Engineering:** [performance-budget](skills/disciplines/performance-budget/SKILL.md) · [performance-optimization](skills/disciplines/performance-optimization/SKILL.md) · [platform-targets](skills/disciplines/platform-targets/SKILL.md) · [save-checkpoint](skills/disciplines/save-checkpoint/SKILL.md)

**Engines:** [custom](skills/engines/custom/SKILL.md) · [threejs](skills/engines/threejs/SKILL.md) · [pixijs](skills/engines/pixijs/SKILL.md) · [godot](skills/engines/godot/SKILL.md) · [unity](skills/engines/unity/SKILL.md) · [unreal](skills/engines/unreal/SKILL.md)

**Assets / 2D:** [model-pipeline](skills/assets/model-pipeline/SKILL.md) · [materials](skills/assets/materials/SKILL.md) · [character-rig](skills/assets/character-rig/SKILL.md) · [spine-skeletal](skills/2d/spine-skeletal/SKILL.md) · [pixel-animation](skills/2d/pixel-animation/SKILL.md)

[router](skills/router/SKILL.md) · [docs/PRESETS.md](docs/PRESETS.md)

## Install

```bash
git clone https://github.com/jammyfu/open-game-skills.git
ln -sfn "$(pwd)/skills" ~/.openclaw/workspace/skills/open-game-skills
# or
ln -sfn "$(pwd)/skills" ~/.claude/skills/open-game-skills
```

Then say:

- `world-map`: region unlock + player pins, no quest arrows
- `difficulty-design`: region-tier, do not sync the world to player level
- weapons column A, armor column B, wear = consume
- `action-feel` column commit-whitelist, engine `threejs`
- `racing-feel` column boost-rail, catch-up = none
- `platform-targets` handheld-dock: same sim, two resolutions

## Recipe table (columns, not clones)

| Feel you want | Map | Difficulty | Gear | Wear |
|---|---|---|---|---|
| Big field, tools run out | region unlock + player pins | region-tier or kill-rank | weapons A, armor B | consume |
| Ability-gated rooms | room graph | honest-fixed | B or none | unbreakable / sharpness |
| Hunt / expedition | hub-spoke | hunt-rank | B tree | sharpness |
| Hotbar ARPG | hub + events | chosen tier | C affix | unbreakable / repair |
| Honest platform | optional / none | honest-fixed | few B or E | unbreakable |
| Chaos kart | course list | place-scaled items | few E | unbreakable |
| Boost-rail speed | ribbon / loops | honest-fixed | E | unbreakable |

Mixing row-one map with row-four gear is legal. Mixing two wear columns on one sword is not.

## Accept (player behavior)

- Can point at the next destination without opening the UI.
- Can say in one sentence how an item gets stronger.
- Resource loop closes in a session.
- A dropped render frame does not drop an input.
- Geometry stays; variants or gates may change.

## License

MIT. Game names belong to their owners. Skills describe public design principles and selectable columns, not ripped assets or private source.

by jammyfu / PaintingCoder
