# open-game-skills

<p align="center">
  <img src="docs/1d3c92f2-8d52-412d-96e0-7b0e67be4f4f.png" alt="open-game-skills" width="640"/>
</p>

<p align="center">
  <b>English</b> · <a href="README.zh.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a>
</p>

<p align="center">
  <strong>Generic agent skills for making games.</strong><br/>
  Speak normally. The dispatcher picks skills and columns.<br/>
  Studios and engines are columns you stack — not games you clone.
</p>

<p align="center">
  <a href="https://github.com/jammyfu/open-game-skills"><img alt="repo" src="https://img.shields.io/badge/github-jammyfu%2Fopen-game-skills-e76f51?style=flat-square"/></a>
  <img alt="license" src="https://img.shields.io/badge/license-MIT-2a9d8f?style=flat-square"/>
  <img alt="lang" src="https://img.shields.io/badge/docs-EN%20ZH%20ZH--Hant%20JA%20KO-e9c46a?style=flat-square"/>
</p>

Open-source skill cluster for OpenClaw, Claude Code, Codex, Cursor, and anything that reads `SKILL.md`.

## Speak first

Install the pack. Point the agent at [`skills/SKILL.md`](skills/SKILL.md). It loads [`dispatcher`](skills/dispatcher/SKILL.md) and answers in this shape:

```
USE:
- <skill> / <column>
ENGINE: custom | threejs | pixijs | godot | unity | unreal
ASK: <one question or empty>
```

You do not name files. Max three disciplines + one engine, then work.

| You say | Agent should load |
|---|---|
| Capcom-like 3D fighter | `fighting-design` / grounded-footsies · `action-feel` / short-special · `kb-mouse-map` / fighter-plane |
| Open world, no quest arrows | `world-map` / region-unlock + pins · `camera-anti-clip` / orbit-third |
| Jump feels floaty | `platform-jump` · `jump-leniency` |
| Can a stranger finish this? | `gameplay-validation` / real-input |
| Stun is too long / elite has no punish | `hitstun-recover` · `enemy-kit-balance` |
| Cutscene should give the stick back | `cutscene-handoff` |
| Moving platform + lava | `moving-platform` · `hazard-volume` |
| Branching dialogue | `dialogue-flags` |
| Rhythm timing / deckbuilder | `rhythm-judge` or `deck-build` |

## How it stacks

```
engine adapter     custom / three.js / PixiJS / Godot / Unity / Unreal
        ↓
discipline         feel · kit · traversal · camera · world · validate …
        ↓
one column         short-special · consume · drift-kart · region-tier …
```

One combat clock per actor. One wear column per item. A studio name (Nintendo, Capcom, …) only picks columns.

Engine adapters bind six primitives: `poll_input` · `now_logical_frame` · `play_pose` · `query_hits` · `apply_knockback` · `juice_hook`.

## Iron laws

1. **Hitstop ≠ hitstun.** Hitstop freezes both colliding clocks. Hitstun is what the victim cannot do after that. Advantage = hitstun − attacker recover.
2. **Do not balance a monster by stealing player i-frames or stretching player stun.** Tune tell, recover, cooldown, then damage, then HP.
3. **A teleported / unlocked / debug session is not a natural clear.** Label it. See `gameplay-validation` and `gameplay-capture`.
4. **IAP and cosmetics do not change cancel windows or hurtboxes.**
5. **Do not copy a finished stage or frame table into the rules.** Columns only.

## Catalog (by cluster)

**Feel & clock** — [action-feel](skills/disciplines/action-feel/SKILL.md) · [combo-design](skills/disciplines/combo-design/SKILL.md) · [hitstun-recover](skills/disciplines/hitstun-recover/SKILL.md) · [knockback-launch](skills/disciplines/knockback-launch/SKILL.md) · [knockback-body](skills/disciplines/knockback-body/SKILL.md) · [landing-lag](skills/disciplines/landing-lag/SKILL.md) · [juice-vfx](skills/disciplines/juice-vfx/SKILL.md) · [audio-feel](skills/disciplines/audio-feel/SKILL.md) · [haptic-rumble](skills/disciplines/haptic-rumble/SKILL.md) · [super-meter](skills/disciplines/super-meter/SKILL.md)

**Combat kit** — [fighting-design](skills/disciplines/fighting-design/SKILL.md) · [enemy-kit-balance](skills/disciplines/enemy-kit-balance/SKILL.md) · [attack-tell](skills/disciplines/attack-tell/SKILL.md) · [hyper-armor](skills/disciplines/hyper-armor/SKILL.md) · [parry-guard](skills/disciplines/parry-guard/SKILL.md) · [dodge-iframe](skills/disciplines/dodge-iframe/SKILL.md) · [throw-tech](skills/disciplines/throw-tech/SKILL.md) · [wakeup-oki](skills/disciplines/wakeup-oki/SKILL.md) · [boss-design](skills/disciplines/boss-design/SKILL.md) · [hitbox-hurtbox](skills/disciplines/hitbox-hurtbox/SKILL.md) · [collision-layers](skills/disciplines/collision-layers/SKILL.md)

**Traversal** — [locomotion](skills/disciplines/locomotion/SKILL.md) · [platform-jump](skills/disciplines/platform-jump/SKILL.md) · [moving-platform](skills/disciplines/moving-platform/SKILL.md) · [climb-vault](skills/disciplines/climb-vault/SKILL.md) · [grapple-swing](skills/disciplines/grapple-swing/SKILL.md) · [swim-water](skills/disciplines/swim-water/SKILL.md) · [hazard-volume](skills/disciplines/hazard-volume/SKILL.md) · [ik-foot-locking](skills/disciplines/ik-foot-locking/SKILL.md)

**Camera & input** — [camera-anti-clip](skills/disciplines/camera-anti-clip/SKILL.md) · [lock-on-target](skills/disciplines/lock-on-target/SKILL.md) · [kb-mouse-map](skills/disciplines/kb-mouse-map/SKILL.md) · [browser-input](skills/disciplines/browser-input/SKILL.md) · [cutscene-handoff](skills/disciplines/cutscene-handoff/SKILL.md)

**World & growth** — [world-map](skills/disciplines/world-map/SKILL.md) · [ability-gate](skills/disciplines/ability-gate/SKILL.md) · [skill-tree](skills/disciplines/skill-tree/SKILL.md) · [difficulty-design](skills/disciplines/difficulty-design/SKILL.md) · [equipment-progression](skills/disciplines/equipment-progression/SKILL.md) · [durability-economy](skills/disciplines/durability-economy/SKILL.md) · [dialogue-flags](skills/disciplines/dialogue-flags/SKILL.md)

**Validation** — [gameplay-validation](skills/disciplines/gameplay-validation/SKILL.md) · [gameplay-capture](skills/disciplines/gameplay-capture/SKILL.md) · [game-planning](skills/disciplines/game-planning/SKILL.md) · [game-localization](skills/disciplines/game-localization/SKILL.md)

**Other genres** — [racing-feel](skills/disciplines/racing-feel/SKILL.md) · [rhythm-judge](skills/disciplines/rhythm-judge/SKILL.md) · [deck-build](skills/disciplines/deck-build/SKILL.md) · [roguelike-run](skills/disciplines/roguelike-run/SKILL.md) · [game-monetization](skills/disciplines/game-monetization/SKILL.md)

**Engines** — [custom](skills/engines/custom/SKILL.md) · [threejs](skills/engines/threejs/SKILL.md) · [pixijs](skills/engines/pixijs/SKILL.md) · [godot](skills/engines/godot/SKILL.md) · [unity](skills/engines/unity/SKILL.md) · [unreal](skills/engines/unreal/SKILL.md)

Ask in speech if a name is missing. Dispatcher maps synonyms. Frame windows and accept tests live in each `SKILL.md`, not here.

## Install

```bash
git clone https://github.com/jammyfu/open-game-skills.git
ln -sfn "$(pwd)/skills" ~/.openclaw/workspace/skills/open-game-skills
ln -sfn "$(pwd)/skills" ~/.claude/skills/open-game-skills
```

Then talk. Do not paste the catalog into the prompt.

## License

MIT. Game names belong to their owners. Skills describe public principles and selectable columns, not ripped stages or private source.

by jammyfu / PaintingCoder
