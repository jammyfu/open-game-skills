# open-game-skills

<p align="center">
  <img src="docs/open_game_logo.png" alt="open-game-skills" width="640"/>
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh.md">简体中文</a> · <b>繁體中文</b> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a>
</p>

<p align="center">
  <strong>做遊戲用的通用 Agent Skill。</strong><br/>
  直接說話。dispatcher 選 skill、選列。<br/>
  工作室與引擎是可疊的列，不是拿來抄的成品。
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

預設文件是 [English README](README.md)。

## 為什麼值得收藏

- **194 個遊戲技能，一個調度器。** 用白話描述你的遊戲，agent 每個階段最多載入三個技能和一個引擎適配器。
- **不綁定引擎。** 適配 three.js、PixiJS、Phaser、Cocos、Godot、Unity 和 Unreal，也支援自研執行環境。
- **規則可以測試。** 每個技能都附正常、邊界和對抗三類評審案例，CI 自動檢查。
- **真正可用的 2D 蒙皮工具鏈。** 網格、調和權重、漏染與接縫檢查、IK 軌跡、折疊與拉伸審計、Spine 風格骨骼疊加圖，以及經過驗證的 rig-c 匯出。只依賴 Python、numpy 和 Pillow。
- **在你已有的工具裡就能用。** Claude Code、Codex、Cursor、OpenClaw，以及任何讀取 `SKILL.md` 的 agent。

## 看它跑起來：鵜鶘騎自行車

<p align="center"><img src="examples/pelican-bicycle/docs/preview.gif" alt="鵜鶘橫叼著魚騎自行車，輪胎壓過石頭時壓平" width="680"/></p>

<table>
  <tr>
    <td align="center" width="33%"><img src="examples/pelican-bicycle/docs/rig.gif" alt="骨骼與 IK 約束" width="100%"/><br/><sub>骨骼與 IK 約束</sub></td>
    <td align="center" width="33%"><img src="examples/pelican-bicycle/docs/fish.gif" alt="魚橫叼在喙裡" width="100%"/><br/><sub>魚橫叼在喙裡</sub></td>
    <td align="center" width="33%"><img src="examples/pelican-bicycle/docs/wheel.gif" alt="輪胎壓過石頭" width="100%"/><br/><sub>輪胎壓過石頭</sub></td>
  </tr>
</table>

一個程式生成的角色，27 個圖層，無需下載素材。所有動作都由骨骼和蒙皮權重驅動：

- **翅膀扶車把。** 雙骨 IK 讓翼尖貼住握把，身體在彈簧上起伏時誤差也在 2e-14 以內。
- **雙腳踩踏板。** 骨長固定，膝關節在 44° 到 114° 之間擺動，從不折疊。
- **魚橫叼在喙裡。** 四根骨從夾持點出發，兩端撲騰，閉合的喙擋住魚身中段。
- **軟輪胎。** 內圈貼住輪圈不動，胎面只在接觸路面和石頭的地方壓平。
- **脖子、頭和尾巴。** 脖子是平滑曲線，頭隨每次踩踏擺動，雙骨尾羽會抖動。
- **用證據說話。** 調和權重的可見折疊像素為 0，最近骨剛性對照組會折疊並被拒絕。

    python -m pip install -r requirements-dev.txt
    python examples/pelican-bicycle/run.py --out /tmp/pelican-review

[閱讀案例](examples/pelican-bicycle/README.md) · [查看 skin-weights Skill](skills/2d/skin-weights/SKILL.md)

### 用 skill 自己做一個

裝好技能包後，給 agent 這樣一段提示：

    使用 open-game-skills。做一隻騎自行車的 2D 鵜鶘，嘴裡橫叼一條魚。
    分圖層繪製，共用一套固定骨架。雙腿用雙骨 IK 踩住踏板，翅膀用雙骨 IK
    扶住車把，骨長保持不變。脖子、魚、尾巴和輪胎用蒙皮權重；頭、喙、腳和
    輪圈保持剛性。輪胎只在接觸路面的地方壓平。證明沒有可見折疊，然後給我
    一個 GIF 和一張骨骼與 IK 疊加圖。

調度器應該給出這樣的路由：

    USE:
    - skin-weights / n/a
    - spine-skeletal / existing
    ENGINE: none
    ASK:
    DEFER: 接入 PixiJS 執行環境

接著 agent 依技能流程執行：build_mesh.py → solve_weights.py → lint_weights.py → pose_trace.py → audit_skin.py + measure_surface.py → render_skin.py → export_rigc.py。圖層、骨架和動作可以參考 [`make_art.py`](examples/pelican-bicycle/make_art.py)。

想要效果好，提示裡寫清四件事：

- **什麼必須貼住：** 腳踩踏板，翼尖抓握把。
- **哪裡剛性、哪裡彎：** 頭和喙剛性，脖子和魚柔軟。
- **動作幅度多大：** 小幅擺動可以整圖蒙皮；大幅換姿勢要分圖層或重繪影格。
- **要什麼證據：** 折疊審計、GIF、骨骼疊加圖。

### 更多可執行案例

- **關節權重：失敗與修正對照。** 同一原畫和骨骼，修正前 2,529 個可見折疊像素，修正後為 0。[互動展示](https://jammyfu.github.io/open-game-skills/weighted-skinning/) · [重現案例](examples/weighted-skinning/README.md)
- **綁定前發現圖集串色。** 像素完全一致的裁切仍可能帶進相鄰部件的顏色。[重現](examples/attachment-ownership/README.md) · [查看圖示](docs/cases/attachment-ownership.md)

[![蒙皮權重修正前後對照](docs/demos/weighted-skinning/preview.gif)](https://jammyfu.github.io/open-game-skills/weighted-skinning/)

## 先說話

裝包後讀 [`skills/SKILL.md`](skills/SKILL.md) → [`dispatcher`](skills/dispatcher/SKILL.md)：

```
USE:
- <skill> / <列>
ENGINE: none | unknown | custom | threejs | pixijs | phaser | cocos | godot | unity | unreal
ASK: <最多一句>
DEFER: <後續階段或留空>
```

每階段最多 3 個專項技能（含資產/2D）+ 1 個必要引擎，其餘工作分階段繼續。`none` 表示純策劃無需引擎，`unknown` 表示尚未確定，`custom` 表示真正的自訂執行環境，不能用來代替猜測。

先讀[共用執行約定](skills/CONTRACT.md)，了解職責與證據界線。[自動產生的完整目錄](skills/catalog.json)包含全部技能；範例表格僅列出常用項目。

| 你說 | 應該裝 |
|---|---|
| 卡普空街霸式 3D | `fighting-design` / grounded-footsies · `action-feel` / short-special |
| 開放世界別畫任務箭 | `world-map` · `camera-anti-clip` |
| 跳得飄 | `platform-jump` · `jump-leniency` |
| 陌生人能不能通 | `gameplay-validation` / real-input |
| 硬直太長 / 精英沒反擊 | `hitstun-recover` · `enemy-kit-balance` |
| 過場把搖桿還回來 | `cutscene-handoff` |
| 低機位侵入角色私密區 | `camera-modesty` / modest |
| 移動平台 + 岩漿 | `moving-platform` · `hazard-volume` |

## 引擎適配器

[custom](skills/engines/custom/SKILL.md) · [threejs](skills/engines/threejs/SKILL.md) · [pixijs](skills/engines/pixijs/SKILL.md) · [phaser](skills/engines/phaser/SKILL.md) · [cocos](skills/engines/cocos/SKILL.md) · [godot](skills/engines/godot/SKILL.md) · [unity](skills/engines/unity/SKILL.md) · [unreal](skills/engines/unreal/SKILL.md)

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
python3 tools/install.py --target "$HOME/.claude/skills"
```

上述路徑僅為範例，目標應設為實際設定的 Agent skills 目錄。安裝器建立父目錄，不覆蓋既有檔案或其他連結。用 `--dry-run` 預覽，無符號連結權限時加 `--copy`，複製更新需手動處理。需要 Python 3.10+；Windows 使用 `python`。保留完整目錄，自動探索機制需另外驗證。

## 更新既有安裝

在儲存庫目錄內執行；先提交或另外儲存自己的未提交變更。分支有分歧時先處理分歧，不要強制重設。

```bash
git switch main
git pull --ff-only origin main
```

符號連結安裝會直接使用更新後的原始檔。使用 `--copy` 的安裝，需先明確備份或移走舊安裝目錄，再重新複製；安裝器不會覆蓋它。更新技能包不會自動升級遊戲，也不會重新設定 Agent。

## 開發檢查

使用 Python 3.10+，建議在虛擬環境中操作。以下指令在儲存庫根目錄執行；Windows 將範例中的 `python3` 換成 `python`。

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m unittest discover -s tests -v
python3 tools/skill_quality.py --check-catalog
```

新增、刪除或重新命名 skill 後，重新產生目錄，再執行測試：

```bash
python3 tools/skill_quality.py --write-catalog --check-catalog
```

這些指令檢查中繼資料、本地引用、目錄一致性、安裝器行為與多語言 README 的共用事實，不代表 LLM 路由準確性、引擎相容性、真人可玩性或翻譯品質已獲驗證。詳細範圍見[貢獻說明](CONTRIBUTING.md)。其餘技能的深度審查仍不應視為完成。

## 工程能力技能

每項附設定範例，以及正常、邊界、反例三類評測情境。寫好情境不代表已經實測。

| Skill | 負責什麼 |
|---|---|
| [game-state-flow](skills/disciplines/game-state-flow/SKILL.md) | 整局狀態轉換、過期非同步任務與冪等結算。 |
| [asset-runtime](skills/disciplines/asset-runtime/SKILL.md) | 資源載入、共享引用、取消與釋放。 |
| [procedural-generation](skills/disciplines/procedural-generation/SKILL.md) | 版本化生成、流程可達性與有上限的修復。 |
| [terrain-surface](skills/disciplines/terrain-surface/SKILL.md) | 區塊接縫、坡面、岸線與碰撞一致性。 |
| [world-streaming](skills/disciplines/world-streaming/SKILL.md) | 區塊就緒、駐留、傳送與世界改動保存。 |
| [physics-interaction](skills/disciplines/physics-interaction/SKILL.md) | 推拉、搬運、投擲與物理控制權。 |

[組合工作流程](skills/references/engineering-workflow.md) · [專項登記表](skills/engineering-registry.json) · [評測紀錄說明](docs/EVALUATION.md)

```bash
python3 tools/engineering_quality.py
```

登記表僅涵蓋這六項工程約定。此指令檢查結構及匯入紀錄的一致性，不呼叫模型；未匯入真實結果時，18 個情境全部為 `not-run`。靜態通過不等於模型行為或引擎實作通過。

## License

MIT。by jammyfu / PaintingCoder

## 測試優先重用開放素材

使用 [open-asset-fixture](skills/assets/open-asset-fixture/SKILL.md) 尋找適合 2D、3D、動畫、音效、特效、PBR 與 HDRI 測試的現成素材。參閱[來源與授權](skills/assets/open-asset-fixture/reference/sources.md)和[使用及狀態說明](skills/assets/open-asset-fixture/reference/usage.md)。優先重用符合要求且通過雜湊檢查的本機素材，再匹配免費 CC0 候選；CC-BY 須明確接受署名要求。腳本不會自動下載、購買或呼叫生成模型。

```sh
python3 skills/assets/open-asset-fixture/scripts/prepare_assets.py --skill materials
python3 skills/assets/open-asset-fixture/scripts/prepare_assets.py --all-skills skills/catalog.json --output asset-plan.json
python3 skills/assets/open-asset-fixture/scripts/prepare_assets.py --skill juice-vfx --root /absolute/fixtures --locks /absolute/fixture.lock.json --pinned-only
```

未設定需求的技能保留為 `needs-requirements`。`--pinned-only` 用於離線 CI，缺少素材即阻擋測試，不暗中替換。`needs-acquisition` 只是候選計畫，`ready-for-import` 也不代表解碼或引擎測試通過。TheLegendOfTrump 仍僅提供另外授權的素材，其未完成的遊戲實作不作為正確性依據，也不被改標為 CC0。

## 素材包

專案收到成品類型素材包（圖集、圖塊集、Tiled 地圖、手感與音訊資料，由 `pack.json` 描述）時，使用 [asset-pack-intake](skills/assets/asset-pack-intake/SKILL.md)：驗證清單、把每個資料夾對應到負責它的技能，並規劃引擎內的搭建階段；它不修改美術。[清單契約](skills/assets/asset-pack-intake/reference/pack-manifest.md)是通用的，不綁定某個生成器。

```sh
python3 skills/assets/asset-pack-intake/scripts/validate_pack.py --root /absolute/pack --plan --engine godot --style pixel-16bit
```

檢查是靜態的（雜湊、圖集矩形與 PNG 尺寸、地圖 gid、手感數值來源、包內無程式碼、各畫風宣告的 1080p 整數縮放畫布，以及必須把每個資產鍵對應到每個畫風的 `styles.json` 換皮表）。引擎匯入、通關與聽感在有證據前維持 `not-run`。

## 實用製作能力補充

新增模組化場景裝配，並加強跨骨骼動作相容、保留形象的分級減模、圖形資源恢復與回放首次偏差定位。見[能力說明](docs/PRACTICAL-CAPABILITIES.md)。兩個離線工具只檢查宣告佈局與匯出軌跡，不等於執行遊戲，也不證明模型能力提升。

[scene-assembly](skills/disciplines/scene-assembly/SKILL.md) · [character-rig](skills/assets/character-rig/SKILL.md) · [model-pipeline](skills/assets/model-pipeline/SKILL.md) · [asset-runtime](skills/disciplines/asset-runtime/SKILL.md) · [gameplay-harness](skills/disciplines/gameplay-harness/SKILL.md)

### 高清人物序列

[hd-sprite-sequence](skills/2d/hd-sprite-sequence/SKILL.md): 鎖定臉部大小、頭身與四肢比例；以圖片雜湊、獨立關鍵點及循環門檻校對，失敗影格必須重繪。

提供固定角色部件與骨架烘焙，禁止逐格縮放或換臉；烘焙結果仍須獨立美術與動作驗收。
