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
| 手感、连击、硬直、取消、缓冲、卡普空 | action-feel + combo-design | ask one of short-special / long-cancel / commit-whitelist |
| 格斗、对战、出招、投 | fighting-design + action-feel + kb-mouse-map | grounded-footsies + fighter-plane |
| 键位、键鼠、WASD、鼠标瞄准、键盘映射 | kb-mouse-map + input-design | pick genre column |
| 开放世界、地图、揭雾、插销 | world-map | region unlock + player pins |
| 难度、关卡、打不过 | difficulty-design + level-design | region-tier |
| 装备、掌门、升级、掉落 | equipment-progression | ask A/B/C per slot |
| 耐久、碰碎、磨刀、修 | durability-economy | consume unless they say 修 / 磨 |
| 背包、栏位、装不下 | inventory-economy | page-grid |
| Boss、王、阶段 | boss-design | duel |
| 跑车、飘移、卡丁、速度感 | racing-feel + kb-mouse-map | drift-kart + race-line |
| 解谜、机关、物性、火水 | puzzle-design + chemistry-verbs | authored-reactions |
| 怪、AI、追人 | enemy-ai | patrol-hunt |
| 潜行、锥形、被发现 | stealth-info | cone-alert |
| 任务、主线、支线 | quest-graph | one-hook |
| 存档、死了回哪 | save-checkpoint | auto-region |
| 卡顿、帧数、优化、手机/主机 | performance-budget + platform-targets | lock-60 + named class |
| 联机、延迟、回滚 | netcode-feel | delay |
| 按键、手柄、A键 | input-design | few-buttons-context |
| 走跑跳爬 | locomotion | analog-8way |
| 教程、新手 | tutorial-design | diegetic |
| 竖切、策划、做什么游戏 | game-planning | — |
| three.js / pixi / godot / unity / 虚幻 | matching engines/* | — |
| 骨骼 / Spine / 像素 / 贴图 | assets/* or 2d/* | — |
| 任天堂、卡普空、暗黑、独立 | studio name = column pick only, never a second clock | — |

If they say 通用 / 别抄某款: keep defaults above, do not copy a franchise layout.

## Do not

- Ask six questions up front.
- List the whole repo.
- Load two combat columns on one actor.
- Mix consume + town-repair on one item.
- Wait for the user to type a skill name.
- Bind look and motion-gestures to the same actor.
