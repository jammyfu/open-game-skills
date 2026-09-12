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

默认文档是 [English README](README.md)。

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
| 跳得飘 | `platform-jump` · `jump-leniency` |
| 陌生人能不能通 | `gameplay-validation` / real-input |
| 硬直太长 / 精英没反击 | `hitstun-recover` · `enemy-kit-balance` |
| 过场把摇杆还回来 | `cutscene-handoff` |
| 移动平台 + 岩浆 | `moving-platform` · `hazard-volume` |

## 铁律

1. **卡肉 ≠ 硬直。** 优势 = 硬直 − 攻击方收招。
2. **不要靠偷玩家无敌或拉长玩家硬直来平衡怪。** 先调起手、收招、冷却，最后 HP。
3. **传送 / 改解锁 / 调试场 不是自然通关。**
4. **内购和外观不改取消窗口、不改判定盒。**
5. **不把成品关卡或帧表写进铁律。** 只选列。

分簇链接以 [英文 README](README.md) 为准。帧数和验收标准在各份 `SKILL.md` 里。

## 安装

```bash
git clone https://github.com/jammyfu/open-game-skills.git
ln -sfn "$(pwd)/skills" ~/.openclaw/workspace/skills/open-game-skills
```

装好就说话，不要把目录贴进提示词。

## License

MIT。by jammyfu / PaintingCoder
