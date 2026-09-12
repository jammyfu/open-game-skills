# open-game-skills

<p align="center">
  <img src="docs/1d3c92f2-8d52-412d-96e0-7b0e67be4f4f.png" alt="open-game-skills" width="640"/>
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh.md">简体中文</a> · <b>繁體中文</b> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a>
</p>

<p align="center">
  <strong>做遊戲用的通用 Agent Skill。</strong><br/>
  直接說話。dispatcher 選 skill、選列。<br/>
  工作室和引擎是可疊的列，不是要你照抄的成品。
</p>

預設文件是 [English README](README.md)。

## 先說話

裝包後讓 agent 讀 [`skills/SKILL.md`](skills/SKILL.md) → [`dispatcher`](skills/dispatcher/SKILL.md)：

```
USE:
- <skill> / <列>
ENGINE: custom | threejs | pixijs | godot | unity | unreal
ASK: <最多一句>
```

最多 3 個學科 + 1 個引擎。不用背檔名。

| 你說 | 應該裝 |
|---|---|
| 卡普空街霸式 3D | `fighting-design` / grounded-footsies · `action-feel` / short-special |
| 跳得飄 | `platform-jump` |
| 陌生人能不能通 | `gameplay-validation` / real-input |
| 硬直太長 / 精英沒反擊 | `hitstun-recover` · `enemy-kit-balance` |
| 過場把搖桿還回來 | `cutscene-handoff` |

## 鐵律

1. **卡肉 ≠ 硬直。** 優勢 = 硬直 − 攻擊方收招。
2. **不要靠偷玩家無敵或拉長玩家硬直來平衡怪。** 先調起手、收招、冷卻，最後 HP。
3. **傳送 / 改解鎖 / 調試場 不是自然通關。**
4. **內購和外觀不改取消窗口、不改判定盒。**
5. **不把成品關卡或帧表寫進鐵律。** 只選列。

分簷鏈結以 [English README](README.md) 為準。帧數和驗收標準在各份 `SKILL.md`。

## 安裝

```bash
git clone https://github.com/jammyfu/open-game-skills.git
ln -sfn "$(pwd)/skills" ~/.openclaw/workspace/skills/open-game-skills
```

裝好就說話，不要把目錄貼進提示詞。

## License

MIT。by jammyfu / PaintingCoder
