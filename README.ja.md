# open-game-skills

<p align="center">
  <img src="docs/1d3c92f2-8d52-412d-96e0-7b0e67be4f4f.png" alt="open-game-skills" width="640"/>
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <b>日本語</b> · <a href="README.ko.md">한국어</a>
</p>

<p align="center">
  <strong>ゲーム制作向けの汎用 Agent Skill。</strong><br/>
  日常言葉で話す。dispatcher が skill と列を選ぶ。
</p>

正式ドキュメントは [English README](README.md)。

## まず話す

[`skills/SKILL.md`](skills/SKILL.md) → [`dispatcher`](skills/dispatcher/SKILL.md)。出力は `USE / ENGINE / ASK / DEFER`。各段階で最大 3 専門 skill + 必要な engine 1 件。残りは次の段階で扱います。

| 言い方 | 読ませるもの |
|---|---|
| ストリートファイタ風 3D | `fighting-design` / grounded-footsies · `action-feel` / short-special |
| クエスト矢印のないオープンワールド | `world-map` · `camera-anti-clip` |
| ジャンプが浮く | `platform-jump` · `jump-leniency` |
| 初心者が通れるか | `gameplay-validation` / real-input |
| ヒットスタンが長すぎる | `hitstun-recover` · `enemy-kit-balance` |
| 演出後に操作を戻す | `cutscene-handoff` |

## 鉄則

1. ヒットストップ ≠ ヒットスタン。有利フレーム = 相手の最初の行動可能 tick − 自分の最初の行動可能 tick。
2. プレイヤーの i-frame や stun を盗んで敵をバランスしない。
3. テレポート／解除フラグ／デバッグは自然クリアではない。
4. IAP や外観でキャンセル窓や hurtbox を変えない。
5. 既成ステージやフレーム表を規則にしない。

目次は [English README](README.md)。

```bash
git clone https://github.com/jammyfu/open-game-skills.git
cd open-game-skills
python3 tools/install.py --target "$HOME/.openclaw/workspace/skills"
```

実際の Agent skills ディレクトリを指定してください。既存ファイルや別のリンクは上書きしません。`--dry-run` で確認でき、必要なら `--copy` を使えます。コピーの更新は手動です。Python 3.10+ が必要です。Windows は `python` と明示的なパスを使ってください。各 Agent の自動検出は別途検証が必要です。

MIT. by jammyfu / PaintingCoder
