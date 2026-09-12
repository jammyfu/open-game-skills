# open-game-skills

<p align="center">
  <img src="docs/logo-banner.svg" alt="open-game-skills" width="640"/>
</p>

<p align="center">
  <strong>English</strong>
  &nbsp;·&nbsp; <a href="README.zh.md">中文</a>
  &nbsp;·&nbsp; <a href="README.ja.md">日本語</a>
  &nbsp;·&nbsp; <a href="README.ko.md">한국어</a>
</p>

<p align="center">
  <strong>Generic Agent Skills for making games.</strong><br/>
  Systems first. Studios and engines are columns you stack, not games you copy.
</p>

<p align="center">
  <a href="https://github.com/jammyfu/open-game-skills"><img alt="repo" src="https://img.shields.io/badge/github-jammyfu%2Fopen--game--skills-e76f51?style=flat-square"/></a>
  <img alt="license" src="https://img.shields.io/badge/license-MIT-2a9d8f?style=flat-square"/>
  <img alt="lang" src="https://img.shields.io/badge/docs-EN%20%C2%B7%20ZH%20%C2%B7%20JA%20%C2%B7%20KO-e9c46a?style=flat-square"/>
</p>

Open-source skill cluster for OpenClaw / Claude Code / Codex / Cursor.
**Ask the column first, then write code.** Never start from an engine node, a finished game, or a copied item table.

## Stack

```
engine adapter        three.js / PixiJS / Godot / Unity / Unreal / custom
        ↓
discipline            map · difficulty · gear · wear · feel · camera · race · fight
        ↓
one studio column     named house as a preset row only
one genre column      action-adventure · fighting · platformer · racing · …
        ↓
juice                 shake / flash / particles (optional)
```

One combat preset per actor. One wear column per item slot. Logic tick does not follow render fps.

## Ask before coding

| System | Question |
|---|---|
| Map | How is information earned? Who may drop pins? |
| Difficulty | Space, resources, or numbers — and which scaler? |
| Equipment | Replace, tree, affix, fuse, or eternal — *per slot*? |
| Durability | Consume, sharpness, repair, or unbreakable? |
| Combat | short-buffer / long-cancel / commit / coyote |
| Race | drift-kart / boost-rail / grip-weight / combat-arena |
| Fight | grounded-footsies / air-dash / tag / platform-fighter |
| Boss | duel / puzzle-body / hunt / spectacle / raid |
| Platform | desktop / docked-home / handheld-dock / handheld-pc |
| Engine | Which six primitives? |

When the user says "generic": **no** world-level-sync, **no** carpet of quest arrows, **no** shatter + endgame tree on the same instance, **no** silent rubber-band of top speed.

## Disciplines on main

**Feel / camera / body**
[action-feel](skills/disciplines/action-feel/SKILL.md) ·
[input-design](skills/disciplines/input-design/SKILL.md) ·
[camera-anti-clip](skills/disciplines/camera-anti-clip/SKILL.md) ·
[ik-foot-locking](skills/disciplines/ik-foot-locking/SKILL.md) ·
[locomotion](skills/disciplines/locomotion/SKILL.md)

**World**
[world-map](skills/disciplines/world-map/SKILL.md) ·
[level-design](skills/disciplines/level-design/SKILL.md) ·
[puzzle-design](skills/disciplines/puzzle-design/SKILL.md) ·
[difficulty-design](skills/disciplines/difficulty-design/SKILL.md)

**Growth**
[equipment-progression](skills/disciplines/equipment-progression/SKILL.md) ·
[durability-economy](skills/disciplines/durability-economy/SKILL.md)

**Contest**
[fighting-design](skills/disciplines/fighting-design/SKILL.md) ·
[combo-design](skills/disciplines/combo-design/SKILL.md) ·
[racing-feel](skills/disciplines/racing-feel/SKILL.md) ·
[racing-design](skills/disciplines/racing-design/SKILL.md) ·
[boss-design](skills/disciplines/boss-design/SKILL.md) ·
[balance-design](skills/disciplines/balance-design/SKILL.md) ·
[netcode-feel](skills/disciplines/netcode-feel/SKILL.md)

**Engineering**
[performance-budget](skills/disciplines/performance-budget/SKILL.md) ·
[performance-optimization](skills/disciplines/performance-optimization/SKILL.md) ·
[platform-targets](skills/disciplines/platform-targets/SKILL.md) ·
[save-checkpoint](skills/disciplines/save-checkpoint/SKILL.md)

**Router** · [engines](skills/engines) · [assets](skills/assets) · [2D / Spine](skills/2d)

Recipes: [docs/PRESETS.md](docs/PRESETS.md)

## Install

```bash
git clone https://github.com/jammyfu/open-game-skills.git
ln -sfn "$(pwd)/skills" ~/.openclaw/workspace/skills/open-game-skills
# or
ln -sfn "$(pwd)/skills" ~/.claude/skills/open-game-skills
```

Then talk in columns, not titles:

- `world-map` region unlock + player pins, no quest-arrow carpet
- `difficulty-design` region-tier, no world-level-sync
- weapons column A, armor column B, wear consume
- `action-feel` commit-whitelist + `engines/threejs`
- `racing-feel` drift-kart, catch-up `item-pressure` published
- `platform-targets` handheld and dock share one simulation

Pair engine node names with [awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) if you need APIs. This repo owns the questions and the clocks.

## Recipe table (columns, not clones)

| Feel you want | Map | Difficulty | Gear | Wear |
|---|---|---|---|---|
| Big field, tools run out | region unlock + player pins | region-tier or kill-rank | weapons A, armor B | consume |
| Ability-gated rooms | room graph | honest-fixed | B or none | unbreakable / sharpness |
| Hunt / expedition | hub-spoke | hunt-rank | B tree | sharpness |
| Hotbar ARPG | hub + events | chosen tier page | C affix | unbreakable / repair |
| Honest platform | optional / none | honest-fixed | few B | unbreakable |
| Pack racer | track sightlines | pack pressure | kart stats | boost as verb |
| Grounded fight | stage | honest-fixed | none | unbreakable |

A named studio is one filling of a row. Mixing row-one map with row-four gear is legal. Mixing two wear columns on one sword is not.

## Accept (player behavior, not likeness)

- Can point at the next destination without opening the UI.
- Can say in one sentence how an item gets stronger.
- Resource loop closes in a session.
- Same geometry stays the same; variants or gates may change.
- Feel is identical at 60 and 30 render fps because the logic tick did not move.
- Catch-up, if any, can be explained in one sentence.

## Layout

```
skills/
  router/          pick columns first
  disciplines/     generic systems
  engines/         six primitives only
  assets/          model / material / rig
  2d/              spine / pixel
```

## License

MIT. Game names belong to their owners. Skills describe public design principles and selectable columns, not ripped assets or private source.

by jammyfu / PaintingCoder
