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

<p align="center">
  <a href="https://github.com/jammyfu/open-game-skills/actions/workflows/skill-quality.yml"><img alt="Skill quality CI" src="https://img.shields.io/github/actions/workflow/status/jammyfu/open-game-skills/skill-quality.yml?branch=main&style=flat-square&logo=githubactions&logoColor=white&label=skill%20quality"/></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/github/license/jammyfu/open-game-skills?style=flat-square&color=2a9d8f"/></a>
  <a href="https://github.com/jammyfu/open-game-skills/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/jammyfu/open-game-skills?style=flat-square&logo=github&color=e76f51"/></a>
  <a href="skills/catalog.json"><img alt="194 skills" src="https://img.shields.io/badge/skills-194-264653?style=flat-square"/></a>
  <a href="skills/SKILL.md"><img alt="Agent Skills: SKILL.md" src="https://img.shields.io/badge/Agent%20Skills-SKILL.md-D97757?style=flat-square&logo=anthropic&logoColor=white"/></a>
  <img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <a href="https://jammyfu.github.io/open-game-skills/weighted-skinning/"><img alt="Live demo" src="https://img.shields.io/badge/demo-live-0a7ea4?style=flat-square&logo=githubpages&logoColor=white"/></a>
  <img alt="Docs: EN, 简, 繁, 日, 한" src="https://img.shields.io/badge/docs-EN%20%C2%B7%20%E7%AE%80%20%C2%B7%20%E7%B9%81%20%C2%B7%20%E6%97%A5%20%C2%B7%20%ED%95%9C-e9c46a?style=flat-square"/>
</p>

正式ドキュメントは [English README](README.md)。

## スターする価値

- **194 のゲームスキルと 1 つのディスパッチャー。** ゲームを普通の言葉で説明するだけ。エージェントはフェーズごとに最大 3 スキルと 1 つのエンジンアダプターを読み込みます。
- **エンジン非依存。** three.js、PixiJS、Phaser、Cocos、Godot、Unity、Unreal と独自ランタイムに対応。
- **テストできるルール。** 全スキルに通常・境界・敵対的のレビューケースがあり、CI が検証します。
- **実用的な 2D スキニングツール。** メッシュ、調和ウェイト、にじみとシームのチェック、IK トレース、折り返しと伸びの監査、Spine 風ボーン表示、検証済み rig-c 書き出し。依存は Python、numpy、Pillow のみ。
- **いつもの環境で動く。** Claude Code、Codex、Cursor、OpenClaw など `SKILL.md` を読むエージェントで使えます。

## 動かしてみる：自転車をこぐペリカン

<p align="center"><img src="examples/pelican-bicycle/docs/preview.gif" alt="魚をくわえたペリカンが自転車をこぎ、タイヤが石の上でつぶれる" width="680"/></p>

<table>
  <tr>
    <td align="center" width="33%"><img src="examples/pelican-bicycle/docs/rig.gif" alt="ボーンと IK 制約" width="100%"/><br/><sub>ボーンと IK 制約</sub></td>
    <td align="center" width="33%"><img src="examples/pelican-bicycle/docs/fish.gif" alt="くちばしで横にくわえた魚" width="100%"/><br/><sub>くちばしで横にくわえた魚</sub></td>
    <td align="center" width="33%"><img src="examples/pelican-bicycle/docs/wheel.gif" alt="石の上でつぶれるタイヤ" width="100%"/><br/><sub>石の上でつぶれるタイヤ</sub></td>
  </tr>
</table>

生成キャラクター 1 体、レイヤー 27 枚、ダウンロード不要。動きはすべてボーンとスキンウェイトによるものです：

- **翼でハンドルを握る。** 2 ボーン IK で、体がばねで揺れても誤差 2e-14 以内。
- **脚はペダルの上。** 骨長は固定、膝は 44° から 114° まで曲がり、折り返しはゼロ。
- **魚は横向きにくわえる。** 4 ボーンが挟む位置から伸び、両端がはね、閉じたくちばしが胴の中央を隠します。
- **柔らかいタイヤ。** 内側はリムに固定、トレッドは路面と石に触れた所だけつぶれます。
- **首・頭・尾。** なめらかな首、ペダルのリズムで揺れる頭、2 ボーンで震える尾。
- **証拠で示す。** 調和ウェイトの可視折り返しは 0。最近傍ボーンの剛体対照は折り返して不合格。

    python -m pip install -r requirements-dev.txt
    python examples/pelican-bicycle/run.py --out /tmp/pelican-review

[ケースを読む](examples/pelican-bicycle/README.md) · [skin-weights Skill](skills/2d/skin-weights/SKILL.md)

### スキルで自分で作る

パックを入れたら、一言で頼めます：

    open-game-skills で、魚をくわえて自転車をこぐ 2D ペリカンを、ボーンとスキンウェイトでアニメーションさせて。

残りはスキルが補い、描く前に選んだ内容を見せます：

- **接触：** 足はペダル、翼の先はハンドル、魚はくちばしで挟む。
- **硬さと柔らかさ：** 頭・くちばし・足・リムは剛体、首・魚・尾・タイヤはウェイト。
- **動き：** 頭と尾はペダルのたびに揺れ、タイヤは路面でつぶれる。
- **証拠：** 折り返し監査、GIF、ボーンと IK の重ね表示。

ディスパッチャーの経路：

    USE:
    - skin-weights / n/a
    - spine-skeletal / existing
    ENGINE: none
    ASK:
    DEFER: PixiJS ランタイムへの組み込み

続いてエージェントが build_mesh.py → solve_weights.py → lint_weights.py → pose_trace.py → audit_skin.py + measure_surface.py → render_skin.py → export_rigc.py を実行します。参考ケースは [`make_art.py`](examples/pelican-bicycle/make_art.py)。変えたい所は「タイヤをもっと弾ませて」のように普通に伝えてください。

### ほかの実行できるケース

- **関節ウェイトの不合格と修正。** 同じ原画と骨で、修正前 2,529 可視折り返しピクセル、修正後 0。[デモ](https://jammyfu.github.io/open-game-skills/weighted-skinning/) · [再現手順](examples/weighted-skinning/README.md)
- **バインド前のアトラスにじみ。** ピクセル一致の切り出しでも隣のパーツの色が混ざることがあります。[再現](examples/attachment-ownership/README.md) · [図解](docs/cases/attachment-ownership.md)

[![スキニングの修正前後](docs/demos/weighted-skinning/preview.gif)](https://jammyfu.github.io/open-game-skills/weighted-skinning/)

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
| 低い角度で私的領域を侵すフレーミング | `camera-modesty` / modest |

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

## アセットパック

完成したジャンル別アセットパック（アトラス、タイルセット、Tiled マップ、手触りとオーディオのデータ。`pack.json` で記述）を受け取ったときは [asset-pack-intake](skills/assets/asset-pack-intake/SKILL.md) を使います。マニフェストを検証し、各フォルダを担当スキルへ対応づけ、エンジンでの構築フェーズを計画します。アートは編集しません。[マニフェスト契約](skills/assets/asset-pack-intake/reference/pack-manifest.md)は汎用で、特定のジェネレーターに依存しません。

```sh
python3 skills/assets/asset-pack-intake/scripts/validate_pack.py --root /absolute/pack --plan --engine godot --style pixel-16bit
```

検査は静的です（ハッシュ、アトラス矩形と PNG サイズ、マップの gid、手触り値の出典、パック内にコードがないこと、各スタイルが宣言する 1080p 整数倍キャンバス、すべてのアセットキーを全スタイルに対応づける `styles.json` の切り替え表）。エンジンへの取り込み、クリア、聴感は証拠が出るまで `not-run` のままです。

## 制作向け機能の拡張

モジュール型シーン構築、リグ間のクリップ互換性、シルエットを保つLOD、描画リソース復旧、リプレイの初回差分診断を追加・強化しました。[機能ガイド](docs/PRACTICAL-CAPABILITIES.md)を参照してください。オフラインツールは宣言された配置と出力済みトレースを検査するだけで、ゲーム実行やLLMの改善を証明しません。

[scene-assembly](skills/disciplines/scene-assembly/SKILL.md) · [character-rig](skills/assets/character-rig/SKILL.md) · [model-pipeline](skills/assets/model-pipeline/SKILL.md) · [asset-runtime](skills/disciplines/asset-runtime/SKILL.md) · [gameplay-harness](skills/disciplines/gameplay-harness/SKILL.md)

### HDスプライト連番

[hd-sprite-sequence](skills/2d/hd-sprite-sequence/SKILL.md): 顔・頭身・四肢の比率を固定し、画像ハッシュ、独立したランドマークとループの連続性を検証します。

固定パーツと骨格から連番をベイクし、フレームごとの拡縮や顔の差し替えを禁止します。独立した画像・動作検証は別途必要です。
