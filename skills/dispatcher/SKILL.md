---
name: dispatcher
description: Listen to how the user talks about a game. Pick 1–3 existing open-game-skills and one column each. Do not ask the user to name skills.
---

# Dispatcher

Load this first. The user will speak in everyday language. You pick the skills. Never dump the catalog.

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

| They say something like | Load | Default column |
|---|---|---|
| 脚滑、贴地、脚步 | ik-foot-locking | — |
| 镜头穿模、贴墙、绕背 | camera-anti-clip | orbit-third |
| 手感、连击、取消、缓冲、卡普空 | action-feel + combo-design | ask short-special / long-cancel / commit-whitelist |
| 硬直、被打不能动、优势帧 | hitstun-recover | light-stun |
| 卡肉、hitstop | action-feel | keep current combat column |
| 怪不公平、起手看不见、敌人套装 | enemy-kit-balance + attack-tell | poke-guard |
| 霸体、超甲 | hyper-armor | hyper-frames |
| 击飞、击退、浮空 | knockback-launch + knockback-body | pop-up |
| 格斗、对战、出招、投 | fighting-design + action-feel + kb-mouse-map | grounded-footsies + fighter-plane |
| 跳得飘、土狼、跳缓冲 | platform-jump + jump-leniency | snap-run |
| 移动平台、电梯、踏板 | moving-platform | kinematic-ride |
| 过场、把摇杆还回来 | cutscene-handoff | — |
| 对话分支、旗帜 | dialogue-flags | quest-flag |
| 音游、判定窗 | rhythm-judge | tap-window |
| 卡组、构卡 | deck-build | — |
| 碰撞层、子弹穿自己 | collision-layers | — |
| 地刺、岩浆、场地伤害 | hazard-volume | tick-dot |
| 键位、键鼠、WASD、鼠标瞄准 | kb-mouse-map + input-design | pick genre column |
| 手机能走不能转、Pointer Lock | browser-input + menu-flow | fallback-relative |
| 试玩、通关、验收 | gameplay-validation | real-input |
| 传送、清怪、调试场 | debug-slate + gameplay-validation | scripted-scene |
| 多语言、豆腐字 | game-localization | ui-layout |
| 录屏、预告 | gameplay-capture | live-challenge |
| 开放世界、揭雾、插销 | world-map | region unlock + player pins |
| 难度、关卡 | difficulty-design + level-design | region-tier |
| 装备、升级、掉落 | equipment-progression | ask A/B/C |
| 耐久、碰碎 | durability-economy | consume |
| 背包、装不下 | inventory-economy | page-grid |
| Boss、王 | boss-design | duel |
| 跑车、卡丁、飘移 | racing-feel + kb-mouse-map | drift-kart |
| 解谜、火水 | puzzle-design + chemistry-verbs | authored-reactions |
| 怪、AI、追人 | enemy-ai | patrol-hunt |
| 潜行、锥形 | stealth-info | cone-alert |
| 任务、主线 | quest-graph | one-hook |
| 存档、死了回哪 | save-checkpoint | auto-region |
| 卡顿、帧数 | performance-budget + platform-targets | lock-60 |
| 联机、回滚 | netcode-feel | delay |
| 按键、手柄 | input-design | few-buttons-context |
| 走跑跳爬 | locomotion | analog-8way |
| 教程、新手 | tutorial-design | diegetic |
| 竖切、策划 | game-planning | — |
| 付费墙、内购、化妆 | game-monetization | cosmetic-shop |
| three.js / pixi / godot / unity / 虚幻 | matching engines/* | — |
| 骨骼 / Spine / 像素 / 贴图 | assets/* or 2d/* | — |
| 任天堂、卡普空、暗黑、独立 | studio name = column pick only | — |

If they say 通用 / 别抄某款: keep defaults, do not copy a franchise layout.
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
