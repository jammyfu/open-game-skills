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

默认文档是 [English README](README.md)。中英一行索引：[docs/SKILL-INDEX.md](docs/SKILL-INDEX.md)。

## 先说话

装包后让 agent 读 [`skills/SKILL.md`](skills/SKILL.md) → [`dispatcher`](skills/dispatcher/SKILL.md)：

```
USE:
- <skill> / <列>
ENGINE: none | unknown | custom | threejs | pixijs | phaser | cocos | godot | unity | unreal
ASK: <最多一句>
DEFER: <后续阶段或留空>
```

每阶段最多 3 个专项技能（含资产/2D）+ 1 个必要引擎，后续任务分阶段继续。`none` 表示纯策划无需引擎，`unknown` 表示尚未确定，`custom` 表示真正的自定义运行时，不能拿来代替猜测。不用背文件名。

先读[共用执行约定](skills/CONTRACT.md)，了解职责和证据边界。[自动生成的完整目录](skills/catalog.json)包含全部技能；下方表格与中英索引是常用项导航，不是完整清单。

| 你说 | 应该装 |
|---|---|
| 卡普空街霸式 3D | `fighting-design` / grounded-footsies · `action-feel` / short-special |
| 开放世界别画任务箭 | `world-map` · `camera-anti-clip` |
| 跳得飘 | `platform-jump` · `jump-leniency` |
| 陌生人能不能通 | `gameplay-validation` / real-input |
| 硬直太长 / 精英没反击 | `hitstun-recover` · `enemy-kit-balance` |
| 过场把摇杆还回来 | `cutscene-handoff` |
| 移动平台 + 岩浆 | `moving-platform` · `hazard-volume` |
| 关卡教学 / 先教后考 | `level-teach` / safe-try |
| 冒烟 / 回归 / 浸泡 | `test-matrix` · `soak-stability` |

## 怎么叠

```
引擎 adapter     custom / three.js / PixiJS / Phaser / Cocos / Godot / Unity / Unreal
        ↓
学科         feel · kit · traversal · camera · world · validate
        ↓
一列         short-special · consume · drift-kart · region-tier
```

一个演员一套战斗时钟。一个物件一列耐久。工作室名只选列。

引擎绑定：`poll_input` · `now_logical_frame` · `play_pose` · `query_hits` · `apply_knockback` · `juice_hook`。

## 铁律

1. **卡肉 ≠ 硬直。** 优势帧 = 受击方首次可行动 tick − 攻击方首次可行动 tick。
2. **不要靠偷玩家无敌或拉长玩家硬直来平衡怪。** 先调起手、收招、冷却，最后 HP。
3. **传送 / 改解锁 / 调试场 不是自然通关。**
4. **内购和外观不改取消窗口、不改判定盒。**
5. **不把成品关卡或帧表写进铁律。** 只选列。

帧数和验收标准在各份 `SKILL.md` 里。

## 常用技能目录（每个 skill 一句话）

### 手感与时钟

| Skill | 用来干什么 |
|---|---|
| [action-feel](skills/disciplines/action-feel/SKILL.md) | 缓冲、取消、卡肉、战斗时钟 |
| [combo-design](skills/disciplines/combo-design/SKILL.md) | 连段路线。无限硬直是 bug |
| [hitstun-recover](skills/disciplines/hitstun-recover/SKILL.md) | 卡肉解冻后，被打方还有几帧不能动 |
| [knockback-launch](skills/disciplines/knockback-launch/SKILL.md) | 击飞 / 浮空，不是第二套重力 |
| [knockback-body](skills/disciplines/knockback-body/SKILL.md) | 击飞走胶囊，不穿墙 |
| [landing-lag](skills/disciplines/landing-lag/SKILL.md) | 空中招落地。空跳短，攻击落地长 |
| [juice-vfx](skills/disciplines/juice-vfx/SKILL.md) | 逻辑命中之后才闪 |
| [audio-feel](skills/disciplines/audio-feel/SKILL.md) | 音效跟同一拍。重试不叠旧曲 |
| [haptic-rumble](skills/disciplines/haptic-rumble/SKILL.md) | 震动可关，关了窗口不变 |
| [super-meter](skills/disciplines/super-meter/SKILL.md) | 气槽。不暗改卡肉 |

### 战斗套装

| Skill | 用来干什么 |
|---|---|
| [fighting-design](skills/disciplines/fighting-design/SKILL.md) | 对波、地面踏步 |
| [enemy-kit-balance](skills/disciplines/enemy-kit-balance/SKILL.md) | 一体一职。先调起手和反击 |
| [attack-tell](skills/disciplines/attack-tell/SKILL.md) | 起手要能读。闪白不能当唯一预警 |
| [hyper-armor](skills/disciplines/hyper-armor/SKILL.md) | 霸体写在招上 |
| [parry-guard](skills/disciplines/parry-guard/SKILL.md) | 格挡与招架 |
| [dodge-iframe](skills/disciplines/dodge-iframe/SKILL.md) | 无敌帧写在躲避这招 |
| [throw-tech](skills/disciplines/throw-tech/SKILL.md) | 投破防。投技盒不是拳盒 |
| [wakeup-oki](skills/disciplines/wakeup-oki/SKILL.md) | 倒地起身。无限倒地是 bug |
| [boss-design](skills/disciplines/boss-design/SKILL.md) | 阶段换职务 |
| [hitbox-hurtbox](skills/disciplines/hitbox-hurtbox/SKILL.md) | 攻击盒 / 受击盒 |
| [collision-layers](skills/disciplines/collision-layers/SKILL.md) | 谁碰谁。渲染网格不是受击盒 |

### 移动

| Skill | 用来干什么 |
|---|---|
| [locomotion](skills/disciplines/locomotion/SKILL.md) | 走跑、模拟 vs 快贴 |
| [platform-jump](skills/disciplines/platform-jump/SKILL.md) | 跳高、土狼、跳缓冲。不用土狼也要能过 |
| [moving-platform](skills/disciplines/moving-platform/SKILL.md) | 站上会走的板，继承速度 |
| [climb-vault](skills/disciplines/climb-vault/SKILL.md) | 翻越与爬，有体力代价 |
| [grapple-swing](skills/disciplines/grapple-swing/SKILL.md) | 钩锁是一招，不是飞 |
| [swim-water](skills/disciplines/swim-water/SKILL.md) | 浮水 / 潜水、呼吸 |
| [hazard-volume](skills/disciplines/hazard-volume/SKILL.md) | 地刺、岩浆。第一跳前要能看见 |
| [ik-foot-locking](skills/disciplines/ik-foot-locking/SKILL.md) | 脚贴斜坡。IK 是表演 |

### 镜头与输入

| Skill | 用来干什么 |
|---|---|
| [camera-anti-clip](skills/disciplines/camera-anti-clip/SKILL.md) | 身体留在画面里，镜头不钻墙 |
| [lock-on-target](skills/disciplines/lock-on-target/SKILL.md) | 锁定记号、朝向、镜头一致 |
| [kb-mouse-map](skills/disciplines/kb-mouse-map/SKILL.md) | 键鼠按品类映射 |
| [browser-input](skills/disciplines/browser-input/SKILL.md) | Pointer Lock 降级、手指分工 |
| [cutscene-handoff](skills/disciplines/cutscene-handoff/SKILL.md) | 过场结束要还视线和动词 |
| [input-design](skills/disciplines/input-design/SKILL.md) | 按键少，按上下文换动词 |

### 世界与成长

| Skill | 用来干什么 |
|---|---|
| [world-map](skills/disciplines/world-map/SKILL.md) | 信息怎么挣。玩家插销，不要满图任务箭 |
| [ability-gate](skills/disciplines/ability-gate/SKILL.md) | 门的安全侧把动词教完 |
| [level-teach](skills/disciplines/level-teach/SKILL.md) | 先看、安全试、考、混搭。一拍一个新动词 |
| [skill-tree](skills/disciplines/skill-tree/SKILL.md) | 买选项，不是暗加帧 |
| [difficulty-design](skills/disciplines/difficulty-design/SKILL.md) | 空间、资源还是数值——只选一个刻度 |
| [equipment-progression](skills/disciplines/equipment-progression/SKILL.md) | 换件 / 树 / 词缀 / 融合 / 永久 |
| [durability-economy](skills/disciplines/durability-economy/SKILL.md) | 碰碎 / 磨刀 / 修 / 不坏。一件一列 |
| [dialogue-flags](skills/disciplines/dialogue-flags/SKILL.md) | 选项写旗帜，不改硬直 |

### 验收与测试

| Skill | 用来干什么 |
|---|---|
| [gameplay-validation](skills/disciplines/gameplay-validation/SKILL.md) | 逻辑绿 ≠ 陌生人能通 |
| [gameplay-capture](skills/disciplines/gameplay-capture/SKILL.md) | 标清实战 / 改过解锁 / 功能演示 |
| [test-matrix](skills/disciplines/test-matrix/SKILL.md) | 先选列：冒烟 / 功能 / 回归 / 组合 / 试玩 |
| [soak-stability](skills/disciplines/soak-stability/SKILL.md) | 长时会话看泄漏和卡顿 |
| [input-combo-test](skills/disciplines/input-combo-test/SKILL.md) | 单键绿 ≠ 走+瞄+攻同时绿 |
| [cert-handoff](skills/disciplines/cert-handoff/SKILL.md) | 休眠恢复 / 拔手柄 / 坏档。不搬 TRC 原文 |
| [game-planning](skills/disciplines/game-planning/SKILL.md) | 地图变大之前的最小可玩片段 |
| [game-localization](skills/disciplines/game-localization/SKILL.md) | 术语、字体、排版 |

### 其它品类 / 引擎

| Skill | 用来干什么 |
|---|---|
| [racing-feel](skills/disciplines/racing-feel/SKILL.md) | 飘移 / 加速轨。不要暗追赶 |
| [rhythm-judge](skills/disciplines/rhythm-judge/SKILL.md) | 判定窗对齐明确的音乐或动作时钟 |
| [deck-build](skills/disciplines/deck-build/SKILL.md) | 牌是动词。不卖取消窗口 |
| [roguelike-run](skills/disciplines/roguelike-run/SKILL.md) | 一局一种子。Meta 开选项 |
| [game-monetization](skills/disciplines/game-monetization/SKILL.md) | 先玩后付。外观不改判定 |
| [custom](skills/engines/custom/SKILL.md) · [threejs](skills/engines/threejs/SKILL.md) · [pixijs](skills/engines/pixijs/SKILL.md) · [phaser](skills/engines/phaser/SKILL.md) · [cocos](skills/engines/cocos/SKILL.md) · [godot](skills/engines/godot/SKILL.md) · [unity](skills/engines/unity/SKILL.md) · [unreal](skills/engines/unreal/SKILL.md) | 绑定六个原语 |

名字对不上就说人话。dispatcher 认简中 / 繁中 / 英 / 日 / 韩。

## 安装

```bash
git clone https://github.com/jammyfu/open-game-skills.git
cd open-game-skills
python3 tools/install.py --target "$HOME/.openclaw/workspace/skills"
python3 tools/install.py --target "$HOME/.claude/skills"
```

装好就说话，不要把目录贴进提示词。

目标应设为实际配置的 Agent skills 目录；上述路径只是示例。安装器创建父目录，不覆盖已有文件或其他链接。可用 `--dry-run` 预览；无软链接权限时加 `--copy`，复制安装需手动更新。需要 Python 3.10+；Windows 使用 `python` 和明确的目标路径。请保留完整目录，各 Agent 的自动发现需单独验证。参见[开发检查](CONTRIBUTING.md)。

## 更新已有安装

在仓库目录内执行；先提交或另行保存自己的未提交改动。分支有分歧时先处理分歧，不要强制重置。

```bash
git switch main
git pull --ff-only origin main
```

软链接安装会直接使用更新后的源文件。使用 `--copy` 的安装，需先明确备份或移走旧安装目录，再重新复制；安装器不会覆盖它。更新技能包不会自动升级游戏，也不会重新配置 Agent。

## 开发检查

使用 Python 3.10+，建议在虚拟环境中操作。以下命令在仓库根目录执行；Windows 将示例中的 `python3` 替换为 `python`。

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m unittest discover -s tests -v
python3 tools/skill_quality.py --check-catalog
```

新增、删除或重命名 skill 后，重新生成目录，再运行测试：

```bash
python3 tools/skill_quality.py --write-catalog --check-catalog
```

这些命令检查元数据、本地引用、目录一致性、安装器行为和多语言 README 的共用事实，不代表 LLM 路由准确性、引擎兼容性、真人可玩性或翻译质量已经验证。详细范围见[贡献说明](CONTRIBUTING.md)。其余技能的深度审查仍不应视为完成。

## License

MIT。by jammyfu / PaintingCoder
