# open-game-skills

<p align="center">
  <img src="docs/logo-banner.svg" alt="open-game-skills" width="640"/>
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh.md">中文</a> · <b>日本語</b> · <a href="README.ko.md">한국어</a>
</p>

<p align="center">
  <strong>ゲーム制作のための汎用 Agent Skill。</strong><br/>
  システムが先。スタジオとエンジンは重ねる列であり、コピーする型ではない。列を選んでからコードを書く。
</p>

OpenClaw / Claude Code / Codex / Cursor 向けのオープンソース Skill 群。
デフォルト文書は [English README](README.md)。

## これは何か

- **学科** が情報・難易度・装備・耐久・戦闘・カメラ・レース・Boss の法則を決める
- **エンジン適応** は 6 原語だけを結ぶ
- **スタジオ名** は列を選ぶだけ

## 書く前に聞く

| 系 | 質問 |
|---|---|
| 地図 | 情報はどう稼ぐ？誰がピンを打てる？ |
| 難易度 | 空間、資源、数値のどれから？ |
| 装備 | 置き換え / 強化木 / 付魔 / 融合 / 永続 |
| 耐久 | 壊して換える / 砕ぐ / 修理 / 壊れない |
| 戦闘 | 短バッファ / 長キャンセル / 承諾白名単 / コヨーテ |
| レース | drift-kart / boost-rail / grip-weight / combat-arena |
| 平台 | フォン / 手持ドック / 客間 / 手持 PC / デスクトップ |

「汎用」と言われたら：世界をプレイヤーレベルに追従させない、地図全面にクエスト矢印を散らかさない、同じ一振を「壊れる」と「最後まで強化」にしない。

## インストール

```bash
git clone https://github.com/jammyfu/open-game-skills.git
ln -sfn "$(pwd)/skills" ~/.openclaw/workspace/skills/open-game-skills
```

## ライセンス

MIT。作品名は権利者に帰属。Skill は公開された設計原理と選択列だけを述べる。

by jammyfu / PaintingCoder
