---
name: dispatcher
description: Use when a game request needs skill routing, several symptoms overlap, or the user speaks ZH, EN, JA, KO or ZH-Hant without naming files.
---

# Dispatcher

Read [the shared contract](../CONTRACT.md) once. Interpret meaning, not literal keyword hits. Traditional and simplified Chinese share intents. Preserve the user's language.

## Resolve before loading

Inspect current code/configuration. Explicit choices outrank existing settings, which outrank the seeds below. Prioritize the reported blocker over broad genre words. Do not silently switch an existing engine or ask for facts already supplied.

Use at most three specialized skills (including assets/2D) plus one necessary engine **per phase**. Deduplicate equivalent owners; record remaining work in DEFER and continue phase by phase. A linked skill is loaded only when its subject is needed, not recursively.

Each pair names a skill and its own mode. `select` means resolve from evidence or one consequential question; `existing` means preserve its current mode; `n/a` means no selector. These are routing directives, never game configuration values. Replace unresolved directives before implementation. Never invent a column to fill the output.

ENGINE is `none` for design-only work, `unknown` when unresolved, or the actual adapter. `custom` is a real custom runtime, not a guess. For uncovered intents, look up paths in `../catalog.json`, inspect candidate descriptions, then load only matching bodies. The six engineering-core selectors and optional dependencies are scoped by [`../engineering-registry.json`](../engineering-registry.json); the registry narrows ownership but does not make `select` a gameplay mode. Studio names route through studio-columns only when the design direction is unresolved; release that picker before a three-discipline implementation phase.

## Output

```text
USE:
- <skill> / <resolved column or n/a>
ENGINE: <none|unknown|custom|threejs|pixijs|phaser|cocos|godot|unity|unreal>
ASK: <one necessary question or empty>
DEFER: <remaining phases or empty>
```

Then do the requested work. Do not dump the catalog. A missing tool means blocked/not-run, not success.

## Routing seeds

These are examples, not permission to overwrite a chosen mode. Match semantic equivalents in all supported languages.

| Signal (ZH / EN / JA / KO examples) | Initial selections |
|---|---|
| 脚滑 / foot slip / 足が滑る / 발 미끄럼 | `ik-foot-locking / n/a` |
| 镜头穿模、鏡頭穿模 / camera clip / 壁を貫通 / 벽 관통 | `camera-anti-clip / orbit-third` |
| 连击、取消 / combo, cancel / コンボ / 콤보 | `action-feel / select`, `combo-design / select` |
| 硬直、优势帧 / hitstun, advantage / 有利フレーム / 유리 프레임 | `hitstun-recover / light-stun` |
| 卡肉 / hitstop / ヒットストップ / 히트스톱 | `action-feel / existing` |
| 怪不公平、预警 / unfair enemy, tell / 予告 / 예고 | `enemy-kit-balance / poke-guard`, `attack-tell / pose-audio` |
| 霸体 / armor / スーパーアーマー / 슈퍼아머 | `hyper-armor / armor-frames` |
| 击飞、浮空 / launch / 浮かせ / 띄우기 | `knockback-launch / launch-arc`, `knockback-body / n/a` |
| 格斗、对战 / fighter / 格闘 / 격투 | `fighting-design / grounded-footsies`, `action-feel / short-special`, `kb-mouse-map / fighter-plane` |
| 跳得飘、土狼 / floaty jump, coyote / ジャンプ / 점프 | `platform-jump / snap-run`, `jump-leniency / generous-platform` |
| 移动平台 / moving platform / 動く足場 / 이동 플랫폼 | `moving-platform / stick-carry` |
| 过场、还操作 / cutscene / 演出後の操作 / 컷씬 조작 | `cutscene-handoff / select` |
| 对话分支 / dialogue flags / フラグ / 분기 | `dialogue-flags / select` |
| 音游、判定窗 / rhythm timing / 音ゲー / 리듬게임 | `rhythm-judge / song-clock` |
| 卡组 / deckbuilder / デッキ / 덱빌더 | `deck-build / select` |
| 碰撞层 / collision layers / 衝突レイヤー / 충돌 레이어 | `collision-layers / n/a` |
| 地刺、岩浆 / spikes, lava / トゲ、溶岩 / 가시、용암 | `hazard-volume / tick-damage` |
| 键位 / keybinds / キー設定 / 키 설정 | `kb-mouse-map / select`, `input-design / select` |
| 手机不能转向 / mobile look, pointer lock / 視点操作 / 시점 조작 | `browser-input / select`, `menu-flow / n/a` |
| 试玩、通关 / playtest / プレイテスト / 플레이테스트 | `gameplay-validation / real-input` |
| 传送、调试 / teleport, debug / デバッグ / 디버그 | `debug-slate / labeled-dev`, `gameplay-validation / scripted-scene` |
| 多语言、豆腐字 / localization / 多言語 / 다국어 | `game-localization / terms-locked` |
| 录屏、预告 / capture, trailer / 録画 / 녹화 | `gameplay-capture / select` |
| 开放世界、揭雾 / open world / オープンワールド / 오픈월드 | `world-map / open-air` |
| 难度、关卡 / difficulty, levels / 難易度 / 난이도 | `difficulty-design / select`, `level-design / select` |
| 装备、掉落 / gear, loot / 装備 / 장비 | `equipment-progression / select` |
| 耐久、破损 / durability / 耐久 / 내구도 | `durability-economy / select` |
| 背包装不下 / inventory full / 持ち物 / 가방 | `inventory-economy / page-grid` |
| Boss、王 / boss / ボス / 보스 | `boss-design / duel` |
| 赛车、漂移 / racing, drift / レース / 레이싱 | `racing-feel / select`, `kb-mouse-map / race-line` |
| 解谜、火水 / puzzle, chemistry / パズル / 퍼즐 | `puzzle-design / select`, `chemistry-verbs / authored-reactions` |
| 敌人追逐 / enemy chase / 追跡 / 추격 | `enemy-ai / patrol-hunt` |
| 潜行 / stealth / 潜入 / 잠입 | `stealth-info / cone-alert` |
| 任务、主线 / quest / クエスト / 퀘스트 | `quest-graph / one-hook` |
| 存档、重生 / save, respawn / セーブ / 세이브 | `save-checkpoint / select` |
| 卡顿、帧率 / hitch, framerate / フレームレート / 프레임 | `performance-budget / select`, `platform-targets / select` |
| 回滚 / rollback / ロールバック / 롤백 | `netcode-feel / rollback` |
| 联机 / online / オンライン / 온라인 | `netcode-feel / select` |
| 按键、手柄 / gamepad / パッド / 패드 | `input-design / select` |
| 走跑跳爬 / locomotion / 移動 / 이동 | `locomotion / select` |
| 教程 / tutorial / チュートリアル / 튜토리얼 | `tutorial-design / select` |
| 竖切、策划 / vertical slice / 企画 / 기획 | `game-planning / n/a` |
| 内购、付费墙 / IAP, paywall / 課金 / 결제 | `game-monetization / select` |
| 关卡教学 / teaching room / 学習の部屋 / 학습 방 | `level-teach / safe-try` |
| 冒烟、回归 / smoke, regression / 回帰テスト / 회귀 테스트 | `game-qa / select` |
| 浸泡、泄漏 / soak, leak / 長時間 / 장시간 | `soak-stability / select` |
| 游戏流程、重复结算 / game flow, duplicate settlement / ゲーム進行 / 게임 흐름 | `game-state-flow / select` |
| 资源重复加载、旧回调 / asset lifetime, stale load / リソース寿命 / 리소스 수명 | `asset-runtime / select` |
| 随机地图、种子不可达 / procedural map, bad seed / 自動生成 / 절차 생성 | `procedural-generation / select` |
| 地形裂缝、岸线 / terrain seam, shoreline / 地形の継ぎ目 / 지형 이음새 | `terrain-surface / select` |
| 区块加载、传送掉地板 / world streaming, missing floor / ストリーミング / 월드 스트리밍 | `world-streaming / select` |
| 推拉搬运、投掷物体 / push carry throw / 物理操作 / 물리 상호작용 | `physics-interaction / select` |
| 测试素材、免费素材 / test assets, open assets / テスト素材 / 테스트 에셋 | `open-asset-fixture / library-first` |
| 骨骼、绑定 / rig / リグ / 리그 | `character-rig / n/a` |
| 导出模型 / model export / モデル出力 / 모델 내보내기 | `model-pipeline / n/a` |
| 材质、贴图 / materials / マテリアル / 머티리얼 | `materials / n/a` |
| 像素动画 / pixel animation / ドット絵 / 픽셀 애니메이션 | `pixel-animation / n/a` |
| Spine / 二维骨骼 / スケルタル / 스켈레탈 | `spine-skeletal / n/a` |

Generic does not mean an automatic franchise preset. Debug-assisted footage is never a natural clear. Choose a declared gameplay-capture mode from evidence, not the word "trailer" alone; disclose altered unlocks separately.

## Acceptance

Given a request with an explicit engine or mode, preserve it unless evidence makes it impossible. For ambiguous engineering-core requests, route to the matching registered owner with `select`, then resolve that directive before implementation. Never emit more than three specialized skills plus one engine in one phase; overflow goes to DEFER. Test explicit-choice precedence, overlapping signals, uncovered-catalog fallback and all six engineering-core seeds. A routing-table match is deterministic contract evidence, not proof of LLM intent classification accuracy.

## Fixture preparation

When tests need external art/audio/effects, use [open-asset-fixture](../assets/open-asset-fixture/SKILL.md) in the preparation phase before generation. Preserve explicit asset requirements and already-authorized fixtures. It consumes one specialized slot; defer it to a separate phase rather than expanding the active set. Pure logic tests do not need an art download.
