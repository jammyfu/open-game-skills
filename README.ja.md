# open-game-skills

<p align="center">
  <img src="docs/open_game_logo.png" alt="open-game-skills" width="640"/>
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <b>日本語</b> · <a href="README.ko.md">한국어</a>
</p>

<p align="center">
  <strong>ゲーム制作向けの汎用 Agent Skill。</strong><br/>
  普段の言葉で依頼すると、dispatcher が skill とモードを選びます。
</p>

正式ドキュメントは [English README](README.md)。

## まず話す

[`skills/SKILL.md`](skills/SKILL.md) → [`dispatcher`](skills/dispatcher/SKILL.md)。

```text
USE:
- <skill> / <モード>
ENGINE: none | unknown | custom | threejs | pixijs | phaser | cocos | godot | unity | unreal
ASK: <必要な質問を 1 つ、または空欄>
DEFER: <後続の段階、または空欄>
```

各段階で最大 3 件の専門 skill（アセット/2D を含む）と、必要な engine 1 件を読み込みます。残りは DEFER に記録して次の段階で扱います。`none` は設計のみで engine 不要、`unknown` は未確定、`custom` は実際の独自ランタイムを意味します。推測で custom を選びません。

担当範囲と検証の扱いは[共通実行ルール](skills/CONTRACT.md)を参照してください。[自動生成の完全なカタログ](skills/catalog.json)に全 skill を掲載しています。例の表は主な項目のみです。

| 言い方 | 読ませるもの |
|---|---|
| ストリートファイター風 3D | `fighting-design` / grounded-footsies · `action-feel` / short-special |
| クエスト矢印のないオープンワールド | `world-map` · `camera-anti-clip` |
| ジャンプが浮く | `platform-jump` · `jump-leniency` |
| 初心者が通れるか | `gameplay-validation` / real-input |
| ヒットスタンが長すぎる | `hitstun-recover` · `enemy-kit-balance` |
| 演出後に操作を戻す | `cutscene-handoff` |

## エンジンアダプター

[custom](skills/engines/custom/SKILL.md) · [threejs](skills/engines/threejs/SKILL.md) · [pixijs](skills/engines/pixijs/SKILL.md) · [phaser](skills/engines/phaser/SKILL.md) · [cocos](skills/engines/cocos/SKILL.md) · [godot](skills/engines/godot/SKILL.md) · [unity](skills/engines/unity/SKILL.md) · [unreal](skills/engines/unreal/SKILL.md)

## 鉄則

1. ヒットストップ ≠ ヒットスタン。有利フレーム = 相手の最初の行動可能 tick − 自分の最初の行動可能 tick。
2. プレイヤーの i-frame や stun を盗んで敵をバランスしない。
3. テレポート／解除フラグ／デバッグは自然クリアではない。
4. IAP や外観でキャンセル窓や hurtbox を変えない。
5. 既成ステージやフレーム表を規則にしない。

目次は [English README](README.md)。

## インストール

```bash
git clone https://github.com/jammyfu/open-game-skills.git
cd open-game-skills
python3 tools/install.py --target "$HOME/.openclaw/workspace/skills"
python3 tools/install.py --target "$HOME/.claude/skills"
```

上記は保存先の例です。実際の Agent skills ディレクトリを指定してください。既存ファイルや別のリンクは上書きしません。`--dry-run` で確認でき、必要なら `--copy` を使えます。コピーの更新は手動です。Python 3.10+ が必要です。Windows は `python` と明示的なパスを使ってください。各 Agent の自動検出は別途検証が必要です。

## 既存のインストールを更新

リポジトリ内で実行してください。先に未コミットの変更をコミットするか別途保存します。ブランチが分岐している場合は差分を調整し、強制リセットしないでください。

```bash
git switch main
git pull --ff-only origin main
```

シンボリックリンクでのインストールは更新後のソースをそのまま参照します。`--copy` を使った場合は、旧インストール先を明示的にバックアップまたは移動してから再コピーしてください。インストーラーは上書きしません。この操作はゲームの更新や Agent の再設定を行いません。

## 開発時のチェック

Python 3.10+ を仮想環境で使用し、リポジトリのルートで実行してください。Windows では例の `python3` を `python` に置き換えます。

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m unittest discover -s tests -v
python3 tools/skill_quality.py --check-catalog
```

skill の追加・削除・名前変更後はカタログを再生成し、テストを再実行してください。

```bash
python3 tools/skill_quality.py --write-catalog --check-catalog
```

このチェックはメタデータ、ローカル参照、カタログの整合性、インストーラーの動作、多言語 README の共通情報を対象とします。LLM のルーティング精度、engine の互換性、人によるプレイの可否、翻訳品質を保証するものではありません。範囲は[貢献ガイド](CONTRIBUTING.md)を参照してください。残りの skill の詳細レビューは未完了です。

## エンジニアリング技能

各技能に設定例と通常・境界・誤用を誘う評価ケースがあります。ケースの作成は実測の完了を意味しません。

| Skill | 担当範囲 |
|---|---|
| [game-state-flow](skills/disciplines/game-state-flow/SKILL.md) | ゲーム全体の状態遷移、古い非同期処理、重複しない結果確定。 |
| [asset-runtime](skills/disciplines/asset-runtime/SKILL.md) | リソースの読込、共有参照、キャンセルと解放。 |
| [procedural-generation](skills/disciplines/procedural-generation/SKILL.md) | 生成バージョン、進行の到達可能性、回数制限付き修復。 |
| [terrain-surface](skills/disciplines/terrain-surface/SKILL.md) | チャンク境界、斜面、水際と衝突形状の整合性。 |
| [world-streaming](skills/disciplines/world-streaming/SKILL.md) | セルの準備、常駐管理、転送と変更データの保存。 |
| [physics-interaction](skills/disciplines/physics-interaction/SKILL.md) | 押す・持つ・投げる操作と物理制御の所有権。 |

[組合せ手順](skills/references/engineering-workflow.md) · [対象レジストリ](skills/engineering-registry.json) · [評価記録](docs/EVALUATION.md)

```bash
python3 tools/engineering_quality.py
```

レジストリの対象はこの6技能のみです。このコマンドは構造と取り込んだ記録の整合性を検査し、モデルは呼び出しません。結果未登録時は18ケースすべてが `not-run` です。静的検査の成功はモデル動作やエンジン実装の合格ではありません。

MIT. by jammyfu / PaintingCoder

## テストでは既存の公開アセットを優先

[open-asset-fixture](skills/assets/open-asset-fixture/SKILL.md) は、2D・3D・アニメーション・音声・VFX・PBR・HDRI のテスト入力を選びます。[配布元とライセンス](skills/assets/open-asset-fixture/reference/sources.md)、[操作とステータス](skills/assets/open-asset-fixture/reference/usage.md)を参照してください。要件に合うハッシュ検証済みのローカル素材を優先し、次に無料 CC0 候補を探します。CC-BY は帰属表示への明示的な同意が必要です。スクリプトはダウンロード、購入、生成モデルの呼び出しを自動実行しません。

```sh
python3 skills/assets/open-asset-fixture/scripts/prepare_assets.py --skill materials
python3 skills/assets/open-asset-fixture/scripts/prepare_assets.py --all-skills skills/catalog.json --output asset-plan.json
python3 skills/assets/open-asset-fixture/scripts/prepare_assets.py --skill juice-vfx --root /absolute/fixtures --locks /absolute/fixture.lock.json --pinned-only
```

未定義の要件は `needs-requirements` のまま残します。`--pinned-only` はオフライン CI 用で、素材がなければテストをブロックします。`needs-acquisition` は候補の発見のみ、`ready-for-import` もデコードやエンジン検証の成功ではありません。TheLegendOfTrump は別途許可された素材のみに使い、未完成のゲーム実装を正解としたり CC0 と見なしたりしません。

## 制作向け機能の拡張

モジュール型シーン構築、リグ間のクリップ互換性、シルエットを保つLOD、描画リソース復旧、リプレイの初回差分診断を追加・強化しました。[機能ガイド](docs/PRACTICAL-CAPABILITIES.md)を参照してください。オフラインツールは宣言された配置と出力済みトレースを検査するだけで、ゲーム実行やLLMの改善を証明しません。

[scene-assembly](skills/disciplines/scene-assembly/SKILL.md) · [character-rig](skills/assets/character-rig/SKILL.md) · [model-pipeline](skills/assets/model-pipeline/SKILL.md) · [asset-runtime](skills/disciplines/asset-runtime/SKILL.md) · [gameplay-harness](skills/disciplines/gameplay-harness/SKILL.md)
