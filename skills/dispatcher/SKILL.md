---
name: dispatcher
description: Hear ZH, EN, JA, KO, or ZH-Hant. Pick 1–3 skills and one column. Do not ask for file names.
---

# Dispatcher

Load this first. Everyday speech. Match **any** language in the first column. You pick the skills. Never dump the catalog.

繁體中文 uses the same sense as 简体 (鏡頭=镜头, 過場=过场, 硬直=硬直). Match it even when glyphs differ.

## Output (always this shape)

```
USE:
- <skill> / <column>
ENGINE: <custom|threejs|pixijs|godot|unity|unreal>
ASK: <only if a required column is missing, one short question>
```

Max 3 disciplines + 1 engine. Then work.

## How to hear them

Phrases are `ZH · EN · JA · KO`. One hit is enough.

| They say something like | Load | Default |
|---|---|---|
| 脚滑、贴地 · foot slip, planted feet · 足が滑る、足を着ける · 발미끄럼, 발 붙음 | ik-foot-locking | — |
| 镜头穿模、贴墙 · camera clip, through the wall · カメラが壁を負ける · 카메라 끝투 | camera-anti-clip | orbit-third |
| 手感、连击、取消、卡普空 · game feel, combo, cancel, Capcom · 手応じ、コンボ、キャンセル · 손맛, 콤보, 캔슬 | action-feel + combo-design | ask short-special / long-cancel / commit-whitelist |
| 硬直、优势帧 · hitstun, frame advantage · ヒットスタン、有利フレーム · 히트스턴, 프레임 이점 | hitstun-recover | light-stun |
| 卡肉 · hitstop, freeze frames · ヒットストップ · 히트스톱 | action-feel | keep combat column |
| 怪不公平、起手看不见 · unfair enemy, no telegraph · 敵が公平じゃない、予告が見えない · 적이 불공정, 예고 없음 | enemy-kit-balance + attack-tell | poke-guard |
| 霸体、超甲 · poise, super armor, hyper armor · 超装甲、スーパーアーマー · 포이즈, 슈퍼아머 | hyper-armor | hyper-frames |
| 击飞、击退、浮空 · launch, knockback, juggle · 浮かせ、ノックバック · 발사, 반동, 떨굴 | knockback-launch + knockback-body | pop-up |
| 格斗、对战、出招、投 · fighter, versus, throw · 格闘、対戦、投げ · 격투, 대전, 던지기 | fighting-design + action-feel + kb-mouse-map | grounded-footsies + fighter-plane |
| 跳得飘、土狼、跳缓冲 · floaty jump, coyote time, jump buffer · ジャンプが浮く、コヨーテタイム · 점프가 떠다, 코요테 타임 | platform-jump + jump-leniency | snap-run |
| 移动平台、电梯 · moving platform, elevator · 動く足場、エレベーター · 이동 플랫폼, 엘리베이터 | moving-platform | kinematic-ride |
| 过场、把摇杆还回来 · cutscene, give the stick back · 演出、操作を戻す · 컷씬, 조이스틱 환원 | cutscene-handoff | — |
| 对话分支、旗帜 · branching dialogue, flags · セリフ分岐、フラグ · 대화 분기, 플래그 | dialogue-flags | quest-flag |
| 音游、判定窗 · rhythm game, timing window · 音ゲー、判定ウィンドウ · 리듬게임, 판정창 | rhythm-judge | tap-window |
| 卡组、构卡 · deckbuilder · デッキビルド · 덱빌더 | deck-build | — |
| 碰撞层、子弹穿自己 · collision layers, friendly fire · 衝突レイヤー · 충돌 레이어 | collision-layers | — |
| 地刺、岩浆 · spikes, lava, hazard · 次の矩、溶岩 · 가시, 용암 | hazard-volume | tick-dot |
| 键位、WASD、鼠标瞄准 · keybinds, mouse look · キー設定、マウス視線 · 키설정, 마우스 조준 | kb-mouse-map + input-design | pick genre |
| 手机能走不能转 · phone move no look, pointer lock · 携帯で歩けるが視線が回らない · 휴대로 우는데 시점이 안 돌아감 | browser-input + menu-flow | fallback-relative |
| 试玩、通关、验收 · playtest, can they finish · プレイテスト、通破できるか · 플레이테스트, 깨는가 | gameplay-validation | real-input |
| 传送、清怪、调试场 · teleport, debug stage · テレポート、デバッグ · 텔레포트, 디버그 | debug-slate + gameplay-validation | scripted-scene |
| 多语言、豆腐字 · localization, tofu glyphs · 多言語、豆腐文字 · 다국어, 두부 글자 | game-localization | ui-layout |
| 录屏、预告 · capture, trailer · 録画、トレーラー · 녹화, 트레일러 | gameplay-capture | live-challenge |
| 开放世界、揭雾 · open world, map pins · オープンワールド · 오픈월드 | world-map | region unlock + pins |
| 难度、关卡 · difficulty, level design · 難易度、レベル設計 · 난이도, 레벨 디자인 | difficulty-design + level-design | region-tier |
| 装备、升级、掉落 · gear, loot · 装備、ドロップ · 장비, 룩 | equipment-progression | ask A/B/C |
| 耐久、碰碎 · durability, breaks · 耐久、壊れる · 내구도, 부서짐 | durability-economy | consume |
| 背包、装不下 · inventory full · アイテムが入らない · 가방 가득 | inventory-economy | page-grid |
| Boss、王 · boss · ボス · 보스 | boss-design | duel |
| 跑车、卡丁、飘移 · racing, kart, drift · レース、カート、ドリフト · 레이싱, 카트, 드리프트 | racing-feel + kb-mouse-map | drift-kart |
| 解谜、火水 · puzzle, fire and water · パズル、火と水 · 퍼즐, 불과 물 | puzzle-design + chemistry-verbs | authored-reactions |
| 怪、AI、追人 · enemy AI, chase · 敵AI、追う · 적 AI, 추격 | enemy-ai | patrol-hunt |
| 潜行、锥形 · stealth, vision cone · 潜入、視界コーン · 잠행, 시야원뿔 | stealth-info | cone-alert |
| 任务、主线 · quest, main story · クエスト、本編 · 퀘스트, 메인 스토리 | quest-graph | one-hook |
| 存档、死了回哪 · save, checkpoint · セーブ、チェックポイント · 세이브, 척포인트 | save-checkpoint | auto-region |
| 卡顿、帧数 · hitch, framerate · フレームレート、残像 · 걸림, 프레임 | performance-budget + platform-targets | lock-60 |
| 联机、回滚 · netcode, rollback · ネットコード、ロールバック · 넷코드, 롤백 | netcode-feel | delay |
| 按键、手柄 · buttons, gamepad · ボタン、パッド · 버튼, 패드 | input-design | few-buttons-context |
| 走跑跳爬 · walk run jump climb · 歩く走る跳ぶ登る · 걷기 달리기 점프 등반 | locomotion | analog-8way |
| 教程、新手 · tutorial · チュートリアル · 튜토리얼 | tutorial-design | diegetic |
| 竖切、策划 · vertical slice · バーティカルスライス · 버티컬 슬라이스 | game-planning | — |
| 付费墙、内购 · paywall, IAP, cosmetics · 課金壁、内部購入 · 결제벽, 인앱 | game-monetization | cosmetic-shop |
| three.js / pixi / godot / unity / 虚幻 / Unreal | matching engines/* | — |
| 骨骼 / Spine / 像素 / rig, pixel art · リグ、ピクセル · 리그, 픽셀 | assets/* or 2d/* | — |
| 任天堂、卡普空、暗黑 / Nintendo, Capcom, Diablo, indie · 任天堂、キャプコン · 닌텐도, 캅콤 | studio name = column pick only | — |

If they say 通用 / generic / 汎用 / 범용 / don't clone: keep defaults.
Unlock-flag clip → gameplay-capture / adjusted-challenge.
Auto-play lost lock or tab → harness failure, not difficulty.

## Do not

- Ask six questions up front.
- List the whole repo.
- Load two combat columns on one actor.
- Mix consume + town-repair on one item.
- Wait for a skill file name.
- File a teleported boss kill as a natural clear.
- Sell a cancel window or iframe as an IAP.
