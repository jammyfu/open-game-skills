# open-game-skills

<p align="center">
  <img src="docs/1d3c92f2-8d52-412d-96e0-7b0e67be4f4f.png" alt="open-game-skills" width="640"/>
</p>

<p align="center">
  <b>English</b> · <a href="README.zh.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a>
</p>

<p align="center">
  <strong>Generic agent skills for making games.</strong><br/>
  Speak in plain language. The pack picks columns. It does not clone a title.
</p>

<p align="center">
  <a href="https://github.com/jammyfu/open-game-skills"><img alt="repo" src="https://img.shields.io/badge/github-jammyfu%2Fopen-game-skills-e76f51?style=flat-square"/></a>
  <img alt="license" src="https://img.shields.io/badge/license-MIT-2a9d8f?style=flat-square"/>
  <img alt="lang" src="https://img.shields.io/badge/docs-EN%20ZH%20ZH--Hant%20JA%20KO-e9c46a?style=flat-square"/>
</p>

Open-source skill cluster for OpenClaw, Claude Code, Codex, and Cursor.
**Talk first. The dispatcher picks skills. Then write code.**

## Speak first

Load [`skills/SKILL.md`](skills/SKILL.md) → [`skills/dispatcher/SKILL.md`](skills/dispatcher/SKILL.md).
Do not recite the catalog. Answer in this shape, then work:

```
USE:
- <skill> / <column>
- <skill> / <column>
ENGINE: custom | threejs | pixijs | godot | unity | unreal
ASK: one question only if a required column is missing
```

Max three disciplines + one engine.

| You say | Pack loads |
|---|---|
| Capcom / Street Fighter-like 3D | `fighting-design / grounded-footsies` + `action-feel / short-special` + `kb-mouse-map / fighter-plane` |
| Jump feels late or floaty | `platform-jump / snap-run` |
| Hitstun too long / enemy too tanky | `hitstun-recover` + `enemy-kit-balance` |
| Can a stranger actually finish | `gameplay-validation / real-input` |
| This clip used a debug unlock | `gameplay-capture` labeled adjusted-challenge |

Studio names pick columns. They do not add a second clock.

## Stack

```
engine adapter     three.js / PixiJS / Godot / Unity / Unreal / custom
        ↓
discipline         feel · camera · kit · map · validation …
        ↓
one studio column  nintendo-zelda · capcom · konami · blizzard · indie
one genre column   fighting · platformer · racing · action-adventure …
```

Engine adapters bind six primitives:
`poll_input` · `now_logical_frame` · `play_pose` · `query_hits` · `apply_knockback` · `juice_hook`.

## Iron laws

1. One combat column per actor. One wear column per item instance.
2. **Hitstop ≠ hitstun.** Hitstop freezes the two colliding clocks. Hitstun is how long the victim stays locked after the freeze. Advantage = hitstun − attacker recover.
3. Teleport / wipe / forced boss = `scripted-scene`. It is not a natural clear. Debug flags write a lab slot (`save-integrity`).
4. Money does not buy cancel windows, shorter hitstop, or bigger hitboxes (`game-monetization`).
5. Do not copy a franchise layout, movelist, or frame chart. Columns are reusable; stages are yours.
6. Do not steal player i-frames or stretch player hitstun to “balance” an enemy. Patch the enemy row (`enemy-kit-balance`).

Frame windows, HP tables, and accept matrices live in each `SKILL.md`. This page does not reprint them.

## Clusters

Sibling files sit next to these entries under `skills/disciplines/`.

**Feel & traversal** — [action-feel](skills/disciplines/action-feel/SKILL.md) · [platform-jump](skills/disciplines/platform-jump/SKILL.md) · [locomotion](skills/disciplines/locomotion/SKILL.md) · [moving-platform](skills/disciplines/moving-platform/SKILL.md) · [ik-foot-locking](skills/disciplines/ik-foot-locking/SKILL.md) · [climb-vault](skills/disciplines/climb-vault/SKILL.md) · [cutscene-handoff](skills/disciplines/cutscene-handoff/SKILL.md)

**Combat kit** — [hitstun-recover](skills/disciplines/hitstun-recover/SKILL.md) · [attack-tell](skills/disciplines/attack-tell/SKILL.md) · [fighting-design](skills/disciplines/fighting-design/SKILL.md) · [combo-design](skills/disciplines/combo-design/SKILL.md) · [parry-guard](skills/disciplines/parry-guard/SKILL.md) · [throw-tech](skills/disciplines/throw-tech/SKILL.md) · [wakeup-oki](skills/disciplines/wakeup-oki/SKILL.md) · [knockback-launch](skills/disciplines/knockback-launch/SKILL.md)

**Enemies & space** — [enemy-kit-balance](skills/disciplines/enemy-kit-balance/SKILL.md) · [enemy-ai](skills/disciplines/enemy-ai/SKILL.md) · [boss-design](skills/disciplines/boss-design/SKILL.md) · [spawn-wave](skills/disciplines/spawn-wave/SKILL.md) · [hazard-volume](skills/disciplines/hazard-volume/SKILL.md) · [balance-design](skills/disciplines/balance-design/SKILL.md)

**Camera & input** — [camera-anti-clip](skills/disciplines/camera-anti-clip/SKILL.md) · [lock-on-target](skills/disciplines/lock-on-target/SKILL.md) · [kb-mouse-map](skills/disciplines/kb-mouse-map/SKILL.md) · [input-design](skills/disciplines/input-design/SKILL.md) · [browser-input](skills/disciplines/browser-input/SKILL.md)

**World & growth** — [world-map](skills/disciplines/world-map/SKILL.md) · [ability-gate](skills/disciplines/ability-gate/SKILL.md) · [equipment-progression](skills/disciplines/equipment-progression/SKILL.md) · [durability-economy](skills/disciplines/durability-economy/SKILL.md) · [roguelike-run](skills/disciplines/roguelike-run/SKILL.md)

**Proof** — [gameplay-validation](skills/disciplines/gameplay-validation/SKILL.md) · [gameplay-capture](skills/disciplines/gameplay-capture/SKILL.md) · [game-localization](skills/disciplines/game-localization/SKILL.md) · [save-integrity](skills/disciplines/save-integrity/SKILL.md)

**Engines / assets** — [custom](skills/engines/custom/SKILL.md) · [threejs](skills/engines/threejs/SKILL.md) · [pixijs](skills/engines/pixijs/SKILL.md) · [godot](skills/engines/godot/SKILL.md) · [unity](skills/engines/unity/SKILL.md) · [unreal](skills/engines/unreal/SKILL.md) · [model-pipeline](skills/assets/model-pipeline/SKILL.md) · [spine-skeletal](skills/2d/spine-skeletal/SKILL.md)

Presets: [docs/PRESETS.md](docs/PRESETS.md). Cases: [docs/cases/playtest-lessons.md](docs/cases/playtest-lessons.md).

## Install

```bash
git clone https://github.com/jammyfu/open-game-skills.git
ln -sfn "$(pwd)/skills" ~/.openclaw/workspace/skills/open-game-skills
ln -sfn "$(pwd)/skills" ~/.claude/skills/open-game-skills
```

Then talk. Do not start by naming files.

- Street Fighter-like 3D, keyboard, training dummy
- Jump is a frame late; coyote ok, but the level must work without it
- This swipe has no startup; do not buff HP first
- Clip used a debug unlock — label it, do not call it a clear

## Recipe table (columns, not clones)

| Feel you want | Map | Difficulty | Gear | Wear |
|---|---|---|---|---|
| Big field, tools run out | region unlock + player pins | region-tier | weapons A, armor B | consume |
| Ability-gated rooms | room graph | honest-fixed | B or none | unbreakable |
| Honest platform | optional | honest-fixed | few | unbreakable |
| Grounded fighter | stage list | honest-fixed | none | unbreakable |
| Chaos kart | course list | place-scaled items | few E | unbreakable |

Mixing a field map with ARPG gear is legal. Mixing two wear columns on one sword is not.

## Accept

- A new player can name the next goal without a wiki.
- A dropped render frame does not drop an input.
- Advantage after hit and after block is visible in training-mode.
- A scripted-scene green is not written as “the game is completable”.

## License

MIT. Game names belong to their owners. Skills describe public principles and selectable columns, not ripped assets or private source.

by jammyfu / PaintingCoder
