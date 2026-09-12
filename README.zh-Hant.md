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
  工作室與引擎是可疊的列，不是拿來抄的成品。
</p>

預設文件是 [English README](README.md)。

## 先說話

裝包後讀 [`skills/SKILL.md`](skills/SKILL.md) → [`dispatcher`](skills/dispatcher/SKILL.md)：

```
USE:
- <skill> / <列>
ENGINE: none | unknown | custom | threejs | pixijs | godot | unity | unreal
ASK: <最多一句>
DEFER: <後續階段或留空>
```

每階段最多 3 個專項技能 + 1 個必要引擎，其餘工作分階段繼續。

| 你說 | 應該裝 |
|---|---|
| 卡普空街霸式 3D | `fighting-design` / grounded-footsies · `action-feel` / short-special |
| 開放世界別畫任務箭 | `world-map` · `camera-anti-clip` |
| 跳得飄 | `platform-jump` · `jump-leniency` |
| 陌生人能不能通 | `gameplay-validation` / real-input |
| 硬直太長 / 精英沒反擊 | `hitstun-recover` · `enemy-kit-balance` |
| 過場把搖桿還回來 | `cutscene-handoff` |
| 移動平台 + 岩漿 | `moving-platform` · `hazard-volume` |

## 鐵律

1. **卡肉 ≠ 硬直。** 優勢幀 = 受擊方首次可行動 tick − 攻擊方首次可行動 tick。
2. **不要靠偷玩家無敵或拉長玩家硬直來平衡怪。** 先調起手、收招、冷卻，最後 HP。
3. **傳送 / 改解鎖 / 調試場 不是自然通關。**
4. **內購與外觀不改取消窗口、不改判定盒。**
5. **不抄成品關卡或幀表進鐵律。** 只選列。

分簇鏈結以 [英文 README](README.md) 為準。

## 安裝

```bash
git clone https://github.com/jammyfu/open-game-skills.git
cd open-game-skills
python3 tools/install.py --target "$HOME/.openclaw/workspace/skills"
```

目標應設為實際設定的 Agent skills 目錄。安裝器建立父目錄，不覆蓋既有檔案或其他連結。用 `--dry-run` 預覽，無符號連結權限時加 `--copy`，複製更新需手動處理。需要 Python 3.10+；Windows 使用 `python`。保留完整目錄，自動探索機制需另外驗證。

## License

MIT。by jammyfu / PaintingCoder
