# open-game-skills

<p align="center">
  <img src="docs/1d3c92f2-8d52-412d-96e0-7b0e67be4f4f.png" alt="open-game-skills" width="640"/>
</p>

<p align="center">
  <a href="README.md">English</a> · <b>简体中文</b> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a>
</p>

<p align="center">
  <strong>做游戏用的通用 Agent Skill。</strong><br/>
  直接说话。dispatcher 选 skill、选列。<br/>
  工作室和引擎是可叠的列，不是要你照抄的成品。
</p>

默认文档仍是 [English README](README.md)。这份与英文同等详细。

## 先说话

装包后让 agent 读 [`skills/SKILL.md`](skills/SKILL.md) → [`dispatcher`](skills/dispatcher/SKILL.md)：

```
USE:
- <skill> / <列>
ENGINE: custom | threejs | pixijs | godot | unity | unreal
ASK: <最多一句>
```

最多 3 个学科 + 1 个引擎。不用背文件名。

| 你说 | 应该装 |
|---|---|
| 卡普空街霸式 3D | `fighting-design` / grounded-footsies · `action-feel` / short-special |
| 开放世界别画任务箭 | `world-map` · `camera-anti-clip` |
| 跳得飘 | `platform-jump` |
| 陌生人能不能通 | `gameplay-validation` / real-input |
| 硬直太长 / 精英没反击 | `hitstun-recover` · `enemy-kit-balance` |
| 过场把摇杆还回来 | `cutscene-handoff` |
| 移动平台 + 岩浆 | `moving-platform` · `hazard-volume` |
| 关卡教学 / 先教后考 | `level-teach` / safe-try |
| 回归 / 浸泡 / QA | `game-qa` / regression |

## 铁律

1. **卡肉 ≠ 硬直。** 优势 = 硬直 − 攻击方收招。
2. **不要靠偷玩家无敌或拉长玩家硬直来平衡怪。** 先调起手、收招、冷却，最后 HP。
3. **传送 / 改解锁 / 调试场 不是自然通关。**
4. **内购和外观不改取消窗口、不改判定盒。**
5. **不把成品关卡或帧表写进铁律。** 只选列。

## 目录（每个 skill 一句）

### 手感与时钟

| Skill | 用来干什么 |
|---|---|
| [action-feel](skills/disciplines/action-feel/SKILL.md) | 缓冲、取消、卡肉和战斗时钟。先问列。 |
| [combo-design](skills/disciplines/combo-design/SKILL.md) | 连段路线和衰减。无限硬直是 bug。 |
| [hitstun-recover](skills/disciplines/hitstun-recover/SKILL.md) | 卡肉结束后，挨打方还有多久不能动。 |
| [knockback-launch](skills/disciplines/knockback-launch/SKILL.md) | 击飞 / 浮空表，不是第二套重力。 |
| [knockback-body](skills/disciplines/knockback-body/SKILL.md) | 用走路胶囊扫，击飞不要塞进墙。 |
| [landing-lag](skills/disciplines/landing-lag/SKILL.md) | 空中攻击落地硬直。空跳短，攻击落地长。 |
| [juice-vfx](skills/disciplines/juice-vfx/SKILL.md) | 逻辑命中之后才闪白、抖屏。 |
| [audio-feel](skills/disciplines/audio-feel/SKILL.md) | 背景与一次性音效跟同一拍。重试不叠旧曲。 |
| [haptic-rumble](skills/disciplines/haptic-rumble/SKILL.md) | 手柄震动跟 juice 同拍。关掉不改窗口。 |
| [super-meter](skills/disciplines/super-meter/SKILL.md) | 气槽 / 大招是明面条。不暗改卡肉。 |

### 战斗套装

| Skill | 用来干什么 |
|---|---|
| [fighting-design](skills/disciplines/fighting-design/SKILL.md) | 对波、空间、贴地 vs 浮空连段。 |
| [enemy-kit-balance](skills/disciplines/enemy-kit-balance/SKILL.md) | 一具身体一个职务。先调预警和反击，最后 HP。 |
| [attack-tell](skills/disciplines/attack-tell/SKILL.md) | 起手要能看见。闪白不能当唯一预警。 |
| [hyper-armor](skills/disciplines/hyper-armor/SKILL.md) | 霸体写在招上，从预警之后才开。 |
| [parry-guard](skills/disciplines/parry-guard/SKILL.md) | 防御 / 拦切窗口是招表上的行。 |
| [dodge-iframe](skills/disciplines/dodge-iframe/SKILL.md) | 无敌帧写在翻滚行上。 |
| [throw-tech](skills/disciplines/throw-tech/SKILL.md) | 投技 vs 段打。投技盒不是拳盒。 |
| [wakeup-oki](skills/disciplines/wakeup-oki/SKILL.md) | 倒地与起身。无限倒地是 bug。 |
| [boss-design](skills/disciplines/boss-design/SKILL.md) | 阶段换职务，不是暗加伤害。 |
| [hitbox-hurtbox](skills/disciplines/hitbox-hurtbox/SKILL.md) | 攻击盒 / 受击盒 / 投技盒跟逻辑帧。 |
| [collision-layers](skills/disciplines/collision-layers/SKILL.md) | 谁碰谁。渲染网格不是受击盒。 |

### 移动与关卡

| Skill | 用来干什么 |
|---|---|
| [locomotion](skills/disciplines/locomotion/SKILL.md) | 走跑、模拟或贴脱。 |
| [platform-jump](skills/disciplines/platform-jump/SKILL.md) | 跳高、土狼、缓冲。关卡不用土狼也要能过。 |
| [moving-platform](skills/disciplines/moving-platform/SKILL.md) | 承载平台速度。挤压要公布或让路。 |
| [level-teach](skills/disciplines/level-teach/SKILL.md) | 房间里教动词：先看、安全试、再考。 |
| [ability-gate](skills/disciplines/ability-gate/SKILL.md) | 能力墙。安全侧先教，对面再考。 |
| [climb-vault](skills/disciplines/climb-vault/SKILL.md) | 翻越 / 攀爬是动词。 |
| [grapple-swing](skills/disciplines/grapple-swing/SKILL.md) | 钩锁是一招，不是飞。 |
| [hazard-volume](skills/disciplines/hazard-volume/SKILL.md) | 地刺、岩浆。第一跳之前要有预警。 |
| [ik-foot-locking](skills/disciplines/ik-foot-locking/SKILL.md) | 斜坡贴地脚。IK 是表演。 |

### 镜头与输入

| Skill | 用来干什么 |
|---|---|
| [camera-anti-clip](skills/disciplines/camera-anti-clip/SKILL.md) | 人留在画面里，镜头不穿墙。 |
| [lock-on-target](skills/disciplines/lock-on-target/SKILL.md) | 锁定标、朝向、镜头一致。 |
| [kb-mouse-map](skills/disciplines/kb-mouse-map/SKILL.md) | 按品类把职务映到键鼠。 |
| [browser-input](skills/disciplines/browser-input/SKILL.md) | Pointer Lock 降级、触控分手。 |
| [cutscene-handoff](skills/disciplines/cutscene-handoff/SKILL.md) | 过场拿走镜头，结束还回视线和动词。 |
| [input-design](skills/disciplines/input-design/SKILL.md) | 少按键、分层上下文。 |

### 世界与成长

| Skill | 用来干什么 |
|---|---|
| [world-map](skills/disciplines/world-map/SKILL.md) | 信息怎么挣。玩家插销，不要满图任务箭。 |
| [skill-tree](skills/disciplines/skill-tree/SKILL.md) | 加点开选项，不暗改取消窗口。 |
| [difficulty-design](skills/disciplines/difficulty-design/SKILL.md) | 空间、资源或数值——只选一种缩放。 |
| [equipment-progression](skills/disciplines/equipment-progression/SKILL.md) | 换件 / 树 / 词缀 / 融合 / 永久，按槽位。 |
| [durability-economy](skills/disciplines/durability-economy/SKILL.md) | 碰碎 / 磨刀 / 修 / 不坏。一件东西一列。 |
| [dialogue-flags](skills/disciplines/dialogue-flags/SKILL.md) | 选项写旗帜，不改硬直。 |

### 验收与测试

| Skill | 用来干什么 |
|---|---|
| [gameplay-validation](skills/disciplines/gameplay-validation/SKILL.md) | 逻辑绿 ≠ 陌生人能通。 |
| [game-qa](skills/disciplines/game-qa/SKILL.md) | 冒烟 / 功能 / 回归 / 浸泡 / 设备矩阵。每次过测写 build card。 |
| [gameplay-capture](skills/disciplines/gameplay-capture/SKILL.md) | 实战 / 调过解锁的片段 / 功能演示，要打标。 |
| [game-planning](skills/disciplines/game-planning/SKILL.md) | 地图变大之前，先写最小可玩片段。 |
| [game-localization](skills/disciplines/game-localization/SKILL.md) | 术语、字体、布局。 |

### 其它品类

| Skill | 用来干什么 |
|---|---|
| [racing-feel](skills/disciplines/racing-feel/SKILL.md) | 飘移 / 增压 / 抓地。不要暗改极速。 |
| [rhythm-judge](skills/disciplines/rhythm-judge/SKILL.md) | 判定窗在逻辑帧。 |
| [deck-build](skills/disciplines/deck-build/SKILL.md) | 牌是动词。不卖取消窗口。 |
| [roguelike-run](skills/disciplines/roguelike-run/SKILL.md) | 一局一个种子。Meta 只开选项。 |
| [game-monetization](skills/disciplines/game-monetization/SKILL.md) | 先玩。外观不改判定。 |

### 引擎

| Skill | 用来干什么 |
|---|---|
| [custom](skills/engines/custom/SKILL.md) | 自己的循环上绑六个原语。 |
| [threejs](skills/engines/threejs/SKILL.md) | 浏览器 3D。 |
| [pixijs](skills/engines/pixijs/SKILL.md) | 浏览器 2D。 |
| [godot](skills/engines/godot/SKILL.md) | Godot 适配。 |
| [unity](skills/engines/unity/SKILL.md) | Unity 适配。 |
| [unreal](skills/engines/unreal/SKILL.md) | Unreal 适配。 |

## 安装

```bash
git clone https://github.com/jammyfu/open-game-skills.git
ln -sfn "$(pwd)/skills" ~/.openclaw/workspace/skills/open-game-skills
```

装好就说话，不要把目录贴进提示词。

## License

MIT。by jammyfu / PaintingCoder
