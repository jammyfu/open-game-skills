# open-game-skills

<p align="center">
  <img src="docs/logo-banner.svg" alt="open-game-skills" width="640"/>
</p>

<p align="center">
  <strong>Generic Agent Skills for making games.</strong><br/>
  Systems first. Studios and engines are presets you stack, not templates you copy.<br/>
  通用系统优先；工作室与引擎只是可叠加的一列。
</p>

<p align="center">
  <a href="https://github.com/jammyfu/open-game-skills"><img alt="repo" src="https://img.shields.io/badge/github-jammyfu%2Fopen-game-skills-e76f51?style=flat-square"/></a>
  <img alt="license" src="https://img.shields.io/badge/license-MIT-2a9d8f?style=flat-square"/>
  <img alt="skills" src="https://img.shields.io/badge/skills-generic%20%2B%20presets-e9c46a?style=flat-square"/>
</p>

Open-source skill cluster for OpenClaw / Claude Code / Codex / Cursor.
Ask the column first, then write code. Never start from `Animator`, `SpringArm3D`, a Sheikah Tower, or a Street Fighter buffer window.

给 OpenClaw / Claude Code / Codex / Cursor 用的开源游戏 Skill 集群。
**先问列，再写代码。** 不从引擎 API 或某款成品游戏倒着拷。

## Logo

Three stacked tiles + a facing chevron.

| Tile | Meaning |
|---|---|
| Teal bottom | Engine adapter — input, clock, pose, hit, juice |
| Gold middle | Discipline — map, difficulty, gear, wear, feel, camera |
| Coral top | Preset — one studio / one genre column |
| Chevron | Player-facing plan (pins, not a carpet of quest arrows) |

Files: [`logo.svg`](logo.svg) · [`docs/logo-banner.svg`](docs/logo-banner.svg)

## Stack

```
engine adapter          three.js / PixiJS / Godot / Unity / Unreal / custom
        ↓
discipline              world-map · difficulty · equipment · durability
                        action-feel · camera · foot lock · planning
        ↓
one studio column       nintendo-zelda · capcom · konami · blizzard · indie
one genre column        action-adventure · fighting · platformer · …
        ↓
juice                   shake / flash / particles (optional market pack)
```

One combat preset per actor. One wear column per item slot. Studio may pick columns; it may not invent a second clock.

## Ask before coding

| System | Question |
|---|---|
| Map | How is information earned? Who may drop pins? |
| Difficulty | Space, resources, or numbers — and which scaler? |
| Equipment | Replace, tree, affix, fuse, or eternal — *per slot*? |
| Durability | Consume, sharpness, repair, or unbreakable? |
| Combat | SF / DMC / MH / platformer — pick one |
| Engine | Which six primitives? |

Default when the user says 「通用」: **no** world-level-sync, **no** full-map quest arrows, **no** mixing shatter + endgame tree on the same instance.

## Disciplines on main

| Skill | Forces this question |
|---|---|
| [world-map](skills/disciplines/world-map/SKILL.md) | What does the player know, and how did they earn it? |
| [difficulty-design](skills/disciplines/difficulty-design/SKILL.md) | Which layer is the hard part? |
| [equipment-progression](skills/disciplines/equipment-progression/SKILL.md) | Does this item survive the ending? |
| [durability-economy](skills/disciplines/durability-economy/SKILL.md) | What happens at wear = 0? |

More in the tree as they land: `action-feel`, `camera-anti-clip`, `ik-foot-locking`, `level-design`, `puzzle-design`, `game-planning`, `input-design`, studios, engines, assets.

## Install

```bash
git clone https://github.com/jammyfu/open-game-skills.git
ln -sfn "$(pwd)/skills" ~/.openclaw/workspace/skills/open-game-skills
# or
ln -sfn "$(pwd)/skills" ~/.claude/skills/open-game-skills
```

Then say things like:

- 「world-map 用区域揭雾 + 玩家插销，不要任务箭」
- 「difficulty 区域固档，不要等级同步全世界」
- 「武器走装备 A，防具走 B，耐久走碎换」
- 「action-feel 预设 MH，引擎 threejs」

Pair engine API details with [awesome-gamedev-agent-skills](https://github.com/gamedev-skills/awesome-gamedev-agent-skills) if you need node names. This repo owns the questions and the clocks.

## Recipe table (columns, not clones)

| Feel you want | Map | Difficulty | Gear | Wear |
|---|---|---|---|---|
| Big field, tools run out | region unlock + player pins | region-tier or kill-rank | weapons A, armor B | consume |
| Ability-gated rooms | room graph | honest-fixed | B or none | unbreakable / sharpness |
| Hunt / expedition | hub-spoke | hunt-rank | B tree | sharpness |
| Hotbar ARPG | hub + events | chosen tier page | C affix | unbreakable / repair |
| Honest platform | optional / none | honest-fixed | few B or E | unbreakable |
| Stealth info-war | cone / radar | region-tier | few pieces | unbreakable |

Zelda is one filling of row one. Your game may mix row-one map with row-four gear. Legal. Mixing two wear columns on one sword is not.

## Accept (player behavior, not likeness)

- Can point at the next destination without opening the UI.
- Can say in one sentence how an item gets stronger.
- Resource loop closes in a session: next tool in reach, or hone, or repair, or no wear bar at all.
- Same geometry stays the same; variants or gates may change.

## Layout

```
skills/
  disciplines/     generic systems
  studios/         column picks named after houses
  genres/          column picks named after forms
  engines/         six primitives only
  assets/          model / material / rig / Spine
```

## License

MIT. Game names belong to their owners. Skills describe public design principles and selectable columns, not ripped assets or private source.

by jammyfu / PaintingCoder
