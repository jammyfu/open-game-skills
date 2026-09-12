---
name: dispatcher
description: Listen in Chinese or English. Pick 1–3 existing open-game-skills and one column each. Do not ask the user to name skills.
---

# Dispatcher

Load this first. The user will speak in everyday Chinese or English. Match either side of the phrase column. You pick the skills. Never dump the catalog.

## Output (always this shape)

```
USE:
- <skill> / <column>
- <skill> / <column>
ENGINE: <custom|threejs|pixijs|godot|unity|unreal>
ASK: <only if a required column is missing, one short question>
```

Max 3 disciplines + 1 engine. Then stop picking and start doing the work.

## How to hear them

Phrases are `ZH / EN`. Either language is enough.

| They say something like | Load | Default column |
|---|---|---|
| 脚滑、贴地、脚步 / foot slip, planted feet, footsteps | ik-foot-locking | — |
| 镜头穿模、贴墙、绕背 / camera clips, wall clip, camera through mesh | camera-anti-clip | orbit-third |
| 手感、连击、取消、缓冲、卡普空 / game feel, combo, cancel, buffer, Capcom | action-feel + combo-design | ask short-special / long-cancel / commit-whitelist |
| 硬直、被打不能动、优势帧 / hitstun, can't act after hit, frame advantage | hitstun-recover | light-stun |
| 卡肉、hitstop / hitstop, freeze frames | action-feel | keep current combat column |
| 怪不公平、起手看不见、敌人套装 / unfair enemy, no telegraph, enemy kit | enemy-kit-balance + attack-tell | poke-guard |
| 霸体、超甲 / poise, super armor, hyper armor | hyper-armor | hyper-frames |
| 击飞、击退、浮空 / launch, knockback, juggle | knockback-launch + knockback-body | pop-up |
| 格斗、对战、出招、投 / fighter, versus, specials, throw | fighting-design + action-feel + kb-mouse-map | grounded-footsies + fighter-plane |
| 跳得飘、土狼、跳缓冲 / floaty jump, coyote time, jump buffer | platform-jump + jump-leniency | snap-run |
| 移动平台、电梯、踏板 / moving platform, elevator, ride | moving-platform | kinematic-ride |
| 过场、把摇杆还回来 / cutscene, give the stick back | cutscene-handoff | — |
| 对话分支、旗帜 / dialogue branch, flags | dialogue-flags | quest-flag |
| 音游、判定窗 / rhythm game, timing window | rhythm-judge | tap-window |
| 卡组、构卡 / deckbuilder, deck build | deck-build | — |
| 碰撞层、子弹穿自己 / collision layers, bullets hit self | collision-layers | — |
| 地刺、岩浆、场地伤害 / spikes, lava, hazard volume | hazard-volume | tick-dot |
| 键位、键鼠、WASD、鼠标瞄准 / keybinds, mouse look, WASD | kb-mouse-map + input-design | pick genre column |
| 手机能走不能转、Pointer Lock / phone move no look, pointer lock | browser-input + menu-flow | fallback-relative |
| 试玩、通关、验收 / playtest, can a stranger finish, validation | gameplay-validation | real-input |
| 传送、清怪、调试场 / teleport, clear room, debug stage | debug-slate + gameplay-validation | scripted-scene |
| 多语言、豆腐字 / localization, tofu glyphs, missing font | game-localization | ui-layout |
| 录屏、预告 / capture, trailer, gameplay footage | gameplay-capture | live-challenge |
| 开放世界、揭雾、插销 / open world, fog of war, map pins | world-map | region unlock + player pins |
| 难度、关卡 / difficulty, level design | difficulty-design + level-design | region-tier |
| 装备、升级、掉落 / gear, upgrade, drops | equipment-progression | ask A/B/C |
| 耐久、碰碎 / durability, break on hit | durability-economy | consume |
| 背包、装不下 / inventory full, bag slots | inventory-economy | page-grid |
| Boss、王 / boss, phase | boss-design | duel |
| 跑车、卡丁、飘移 / racing, kart, drift | racing-feel + kb-mouse-map | drift-kart |
| 解谜、火水 / puzzle, fire and water | puzzle-design + chemistry-verbs | authored-reactions |
| 怪、AI、追人 / enemy AI, chase | enemy-ai | patrol-hunt |
| 潜行、锥形 / stealth, vision cone | stealth-info | cone-alert |
| 任务、主线 / quest, main story | quest-graph | one-hook |
| 存档、死了回哪 / save, where do I wake | save-checkpoint | auto-region |
| 卡顿、帧数 / hitch, framerate, 60 fps | performance-budget + platform-targets | lock-60 |
| 联机、回滚 / netcode, rollback | netcode-feel | delay |
| 按键、手柄 / buttons, gamepad | input-design | few-buttons-context |
| 走跑跳爬 / walk run jump climb | locomotion | analog-8way |
| 教程、新手 / tutorial, onboarding | tutorial-design | diegetic |
| 竖切、策划 / vertical slice, planning | game-planning | — |
| 付费墙、内购、化妆 / paywall, IAP, cosmetics | game-monetization | cosmetic-shop |
| three.js / pixi / godot / unity / 虚幻 / Unreal | matching engines/* | — |
| 骨骼 / Spine / 像素 / 贴图 / rig, pixel art, textures | assets/* or 2d/* | — |
| 任天堂、卡普空、暗黑、独立 / Nintendo, Capcom, Diablo, indie | studio name = column pick only | — |

If they say 通用 / generic / don't clone a title: keep defaults, do not copy a franchise layout.
If a clip used unlock or difficulty flags: gameplay-capture is adjusted-challenge.
If auto-play lost lock-on, nav, or the tab: validation bucket is harness failure, not difficulty.

## Do not

- Ask six questions up front.
- List the whole repo.
- Load two combat columns on one actor.
- Mix consume + town-repair on one item.
- Wait for the user to type a skill name.
- Bind look and motion-gestures to the same actor.
- File a teleported boss kill as a natural clear.
- Sell a cancel window or iframe as an IAP.
