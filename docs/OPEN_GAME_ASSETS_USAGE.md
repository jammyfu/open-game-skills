# Open Game Assets 使用指南

`Open Game Assets` 是 `open-game-skills` 中面向游戏测试素材准备的 skills-only 插件发行包。它的核心 Skill 是 `open-asset-fixture`。

它解决的是：**测试需要 2D、3D、动画、音效、特效、PBR、HDRI 等素材时，优先复用已经验证的本地素材，其次匹配开放授权素材，并把许可证、版本、文件哈希和未完成检查明确记录下来。**

它不负责证明游戏逻辑正确，也不会把素材页、下载完成或哈希校验误判成引擎测试通过。

---

## 1. 适合什么时候使用

以下情况优先使用 Open Game Assets：

- 2D 动画、Sprite、Tileset 测试缺素材
- 3D 模型、静态场景、角色或动画测试缺素材
- 材质、PBR、HDRI、环境光测试需要真实输入
- 音效、音乐、UI 声音测试缺素材
- 粒子贴图、VFX、原生 Effect 数据测试缺素材
- 想让 CI 或回归测试固定使用同一份素材
- 想知道一个测试到底是“素材缺失”还是“游戏逻辑失败”
- 希望避免每次测试都重新生成 AI 素材

纯逻辑测试如果不需要美术输入，不应为了使用这个 Skill 强行下载素材。

---

## 2. 核心工作顺序

默认顺序：

```text
读取测试需求
    ↓
检查是否已有满足要求的本地 fixture lock
    ↓
有 → 校验 hash / license / capability / format
    ↓
没有 → 从已审核开放素材目录中匹配候选
    ↓
CC0 优先
    ↓
CC-BY 只有明确接受署名要求后才进入候选
    ↓
仍不满足 → 明确返回缺失项，不偷偷降级要求
    ↓
获取素材后检查文件与依赖
    ↓
生成 fixture lock
    ↓
交给目标 Skill / 引擎执行真正测试
```

关键原则：**按测试能力匹配，不按“看起来差不多”匹配。**

例如：

- 需要带骨骼动画时，静态 GLB 不能替代
- 需要原生粒子效果时，一张烟雾 PNG 不能证明 Effect Runtime 工作
- 需要 PBR 材质时，要确认 BaseColor / Normal / Roughness 等通道，而不是只看预览图

---

## 3. 两种工作模式

### `library-first`

推荐日常开发使用。

行为：

1. 优先检查并复用已锁定的本地素材
2. 本地没有合适素材时，再查开放授权候选
3. 不会自动把不满足格式/能力要求的素材当 fallback

适合：

- 本地开发
- 新测试准备
- 需要逐步积累 fixture library 的项目

### `pinned-only`

推荐 CI / 离线回归使用。

行为：

- 只允许使用已经锁定、hash 验证通过的本地素材
- 缺素材时直接阻塞
- 不联网偷偷替换
- 不自动下载另一个“差不多”的素材

适合：

- CI
- 可复现回归
- 发布前验证
- 多机器统一测试

---

## 4. 最常用：按 Skill 自动准备素材

例如测试材质：

```bash
python3 skills/assets/open-asset-fixture/scripts/prepare_assets.py \
  --skill materials
```

例如同时准备动画、音效、VFX：

```bash
python3 skills/assets/open-asset-fixture/scripts/prepare_assets.py \
  --skill animation-blend audio-feel juice-vfx
```

输出会告诉你：

- 当前 Skill 是否已有素材需求模板
- 需要哪类素材
- 必须满足哪些 capability
- 接受哪些格式
- 是否存在已验证本地素材
- 匹配到哪些远程候选
- License / Edition / Source
- 下一步是获取、导入还是执行测试

---

## 5. 为全部 Skill 生成素材准备清单

```bash
python3 skills/assets/open-asset-fixture/scripts/prepare_assets.py \
  --all-skills skills/catalog.json \
  --output asset-plan.json
```

这个命令适合做全仓库扫描。

注意：

- 没有素材需求定义的 Skill 会保留在结果里
- 不会因为没有 profile 就自动算通过
- 纯逻辑 Skill 可以明确标记为不需要素材

常见状态包括：

| 状态 | 含义 |
|---|---|
| `ready-for-import` | 本地素材满足静态准备条件，但尚未代表引擎导入通过 |
| `needs-acquisition` | 找到候选，但素材文件还没有真正取得/锁定 |
| `needs-requirements` | 当前测试还没有明确素材类型/格式/能力需求 |
| `blocked` | 必要素材、许可证证据或完整性条件缺失 |

---

## 6. 自定义一次素材匹配请求

如果某个测试没有预设 profile，可以直接使用 matcher。

参考模板：

```text
skills/assets/open-asset-fixture/assets/request.example.json
```

执行：

```bash
python3 skills/assets/open-asset-fixture/scripts/asset_fixture.py match \
  --request skills/assets/open-asset-fixture/assets/request.example.json
```

请求里通常包含：

- `kind`：sprite / model / animation / sfx / music / vfx / texture / hdri 等
- `formats`：png / ogg / glb / fbx / obj 等
- `requires`：rigged / animation-clips / pbr-maps / particle-texture 等能力
- `query`：用于相关性排序的软关键词
- License 策略

其中：

- `formats` 和 `requires` 是硬条件
- `query` 只是软排序条件

不要为了命中候选而偷偷放宽 `requires`。

---

## 7. 获取素材后生成 fixture lock

取得素材后，不建议直接把某个本地路径写死进测试。

先建立 pin request，参考：

```text
skills/assets/open-asset-fixture/assets/pin.request.example.json
```

然后执行：

```bash
python3 skills/assets/open-asset-fixture/scripts/fixture_lock.py \
  --root /absolute/fixture-dir \
  pin \
  --request /absolute/pin.json \
  --output /absolute/fixture.lock.json
```

fixture lock 用于记录：

- 文件路径
- SHA/hash
- license evidence
- source
- 格式
- capability
- 版本/edition
- attribution 信息

之后 CI 可以只使用锁定素材。

---

## 8. CI / 离线模式示例

```bash
python3 skills/assets/open-asset-fixture/scripts/prepare_assets.py \
  --skill juice-vfx \
  --root /absolute/fixtures \
  --locks /absolute/fixture.lock.json \
  --pinned-only
```

如果文件被修改、丢失、License evidence 缺失或 capability 不匹配，应直接失败/阻塞。

这能避免：

```text
开发机用 A 素材
CI 临时下载了 B 素材
另一台电脑又生成了 C 素材
最终三个环境结果不可比较
```

---

## 9. 推荐的使用方式

### 场景 A：2D 平台游戏

你可以直接说：

```text
为 platform-jump 和 pixel-animation 准备测试素材，优先使用现有开放素材，不要生成新的素材。
```

理想结果：

1. 找本地已锁定 Sprite/Tile
2. 没有时匹配 Kenney / OpenGameArt 等已登记候选
3. 返回许可证和来源
4. 素材导入后再运行真正的平台跳跃/动画测试

### 场景 B：3D 角色动画

```text
给 animation-blend 和 character-rig 准备一个带骨骼、带多个动画 clip 的角色测试素材。
```

这里必须要求：

- rigged
- animation clips
- 对应可导入格式

静态模型不能作为成功 fallback。

### 场景 C：材质 / 地形

```text
给 materials 和 terrain-surface 准备 PBR 测试素材。
```

重点检查：

- BaseColor
- Normal
- Roughness
- Displacement（测试需要时）
- 纹理尺度
- 通道语义

### 场景 D：音效

```text
给 audio-feel 准备 UI、碰撞和命中反馈音效测试素材。
```

找到 OGG/WAV 候选后，还需要目标音频系统实际解码和播放验证。

### 场景 E：VFX

```text
给 juice-vfx 准备 hit spark、smoke、impact 粒子测试素材。
```

要区分：

- 粒子纹理
- Sprite sequence
- Native effect data

它们不是一回事。

---

## 10. 在 ChatGPT / Codex 中怎么调用

安装/上传插件后，可以直接用自然语言触发：

```text
帮我为当前游戏项目准备测试素材，优先使用开放授权的现成素材。
```

或者更具体：

```text
使用 Open Game Assets 给当前 Three.js 项目准备 3D 环境、PBR 材质和碰撞测试素材。
```

```text
使用 open-asset-fixture 为 animation-blend 找一个真正带骨骼和多个动画 clip 的免费测试模型。
```

```text
只使用已经 pinned 的 fixture 做这次测试，不允许临时下载或生成素材。
```

Skill 会根据需求选择 `library-first` 或 `pinned-only` 工作方式。

---

## 11. 构建 portable plugin

源码位置：

```text
skills/assets/open-asset-fixture/
```

发行时不要手工复制 Skill。

构建目录：

```bash
python tools/build_open_game_assets_plugin.py \
  --output dist/open-game-assets
```

构建 ZIP：

```bash
python tools/build_open_game_assets_plugin.py \
  --zip dist/open-game-assets.zip
```

ZIP 根目录结构应为：

```text
plugin.json
skills/
  open-asset-fixture/
    SKILL.md
    assets/
    reference/
    scripts/
```

---

## 12. License 使用原则

默认策略：

```text
Verified local fixture
    ↓
CC0
    ↓
CC-BY（明确接受 attribution 后）
    ↓
其他 License → 人工审核
    ↓
付费/未知/受限 → 不自动使用
```

注意：

- CC0 不代表没有商标、肖像等其他权利风险
- 软件代码许可证不等于素材许可证
- API / 网站服务条款与素材 License 是两套东西
- 免费版和 Pro / Source / Extra 版不能混为一谈

---

## 13. 它不会做什么

Open Game Assets 当前不会自动：

- 绕过登录、付费墙或下载限制
- 把预览图当原始素材
- 批量抓完整素材站
- 自动调用生成模型补齐缺口
- 把未知 License 当免费
- 把 hash 正确当成引擎导入成功
- 把下载成功当成游戏测试通过
- 执行下载素材中的脚本
- 把第三方 Demo 的 gameplay 实现当测试 oracle

---

## 14. TheLegendOfTrump 的特殊边界

`TheLegendOfTrump` 仍然只是单独授权的 **asset-sample-only** fixture。

可以用于：

- 模型样本
- 纹理样本
- 音频样本
- 图片/素材格式测试

不能用于：

- 证明游戏逻辑实现正确
- 作为 Skill 设计规范
- 自动重新标记为 CC0
- 作为可公开再分发素材包

---

## 15. 推荐团队工作流

建议长期流程：

```text
测试需求
   ↓
Open Game Assets 匹配
   ↓
人工/授权工具获取文件
   ↓
安全检查 + License 检查
   ↓
fixture lock
   ↓
提交 fixture metadata
   ↓
pinned-only CI
   ↓
目标 Skill / Engine 执行
   ↓
Gameplay Validation 判断证据能证明什么
```

这样素材准备、引擎测试和最终验证三层不会混在一起。

---

## 16. 相关文件

```text
skills/assets/open-asset-fixture/SKILL.md
skills/assets/open-asset-fixture/assets/catalog.json
skills/assets/open-asset-fixture/reference/sources.md
skills/assets/open-asset-fixture/reference/usage.md
skills/assets/open-asset-fixture/scripts/prepare_assets.py
skills/assets/open-asset-fixture/scripts/asset_fixture.py
skills/assets/open-asset-fixture/scripts/fixture_lock.py
plugins/open-game-assets/plugin.json
plugins/open-game-assets/README.md
tools/build_open_game_assets_plugin.py
```

Marketplace / 官方公开目录提交属于独立发行流程，参见：

```text
docs/MARKETPLACE_SUBMISSION.md
```
