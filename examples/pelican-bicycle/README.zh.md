# 鹈鹕骑自行车：IK 驱动下的蒙皮权重

<p align="center">
  <img src="docs/preview.gif" alt="分层绘制的鹈鹕骑车，双腿通过双骨 IK 跟随踏板" width="520"/>
</p>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="../../skills/2d/skin-weights/SKILL.md">skin-weights Skill</a> ·
  <a href="../../skills/2d/spine-skeletal/SKILL.md">spine-skeletal 审计</a>
</p>

一只分层绘制的鹈鹕在骑自行车。每条腿是一张加权网格，由羽毛大腿和带鳞小腿组成，通过双骨 IK 跟随旋转曲柄上的踏板。蹼足是一个独立的刚性图层，在踝部像铰链一样转动。脖子是一张双骨网格，其余部件都是刚性层。全部 15 个图层由本目录下的确定性脚本生成，不需要下载素材、付费编辑器或游戏资源。

这个案例跑通了 [skin-weights](../../skills/2d/skin-weights/SKILL.md) 的完整流程，并展示权重出错的两种方式：翻折，以及像橡皮一样弯曲。

## 运行

```sh
python -m pip install -r requirements-dev.txt
python examples/pelican-bicycle/run.py --out /tmp/pelican-review
python examples/pelican-bicycle/make_figures.py --run /tmp/pelican-review   # 可选：重建 docs/ 插图
```

只有两种预期结果都复现时，`run.py` 才以 0 退出。输出目录包含全部报告、两份轨迹，以及供目检用的 GIF 和联系表。

| 步骤 | 脚本 | 产物 |
|---|---|---|
| 绘制图层、骨架与动作 | `make_art.py` | `source/`（15 张 PNG 图层、`rig.json`、`motion.json`） |
| 覆盖透明度、外轮廓优先的网格 | `build_mesh.py` | `mesh.json` |
| 调和权重与刚性对照组 | `solve_weights.py` | `harmonic.weights.json`、`nearest.weights.json` |
| 静态检查 | `lint_weights.py` | `*.lint.json` |
| IK 踩踏轨迹，60 Hz 共 121 帧 | `pose_trace.py` | `*.trace.json`、`*.pose.json` |
| 翻折审计与表面应变 | spine-skeletal 的 `audit_skin.py`、`measure_surface.py` | `*.audit.json`、`*.surface.json` |
| 固定相机复核 | `render_skin.py` | `*.gif`、`*.sheet.png` |

## 结果

| 权重 | 静态检查 | 翻折审计 | 可见翻折像素 | 小腿软段占比（近 / 远） |
|---|---|---|---|---|
| 调和权重，逐骨声明刚性区 | 通过 | 通过 | 0 | 0.05 / 0.10 |
| 最近骨刚性绑定（对照组） | 失败 | 失败 | 近侧 198，远侧 164 | 0（不会弯，只会折） |

整个循环中两只脚踝始终贴在踏板上，误差在 2e-14 世界单位以内。近侧膝关节在 48° 到 114° 之间摆动，近侧腿最小的三角形仍保留 38% 的装配面积。

![同一帧下调和权重与最近骨刚性绑定的对比](docs/compare.png)

## 插图说明

**图层。** 每个部件都是独立图片，按从后到前排列。加权网格标出其影响骨，刚性层只跟随一根骨。踝部圆球画在腿上，脚在它下面转动时不会露出接缝。

![全部 15 个图层](docs/layers.png)

**权重视图。** 与 Spine 的权重视图一样，一种颜色代表一根骨。颜色混合带就是两个刚性区之间的调和过渡。腿上的过渡位于大腿末端，被膝盖羽毛盖住；小腿从膝盖下方开始就是单一颜色。

![近侧腿与脖子的权重](docs/weights.png)

## 这个案例沉淀下来的经验

- **通过审计不等于好看。** 早期版本把脚放在腿的网格里，两端用对称的 30% 过渡带。翻折审计零翻折、顺利通过，但细小腿像橡皮一样弯进脚踝。修法分两步：脚改成画好踝部圆球盖住的刚性图层；膝部过渡用不对称 inset 挪到大腿一侧。`pose_trace.py` 现在会报告每根骨的 `softLengthFraction`，让这个问题可以被量化。
- **接缝在动起来之前就被拦下。** 所有腿骨共用同一个 handle 半径时，小腿和脚的刚性区挨在一起，审计在那个脚踝发现了翻折。现在静态的接缝检查不跑动作就能拒绝这种配置。
- **对照组证明检查有效。** 同一网格换成最近骨刚性绑定后，两个膝盖都会翻折，静态检查和审计都会拒绝。
- **导出经过验证，不是假设。** `export_rigc.py --verify-rigc` 用 rig-c 2.79.0 编译该骨架，并用 rig-c 自己的求值器摆姿。121 帧里每个图层的每个顶点与本求值器的偏差都在 2e-5 世界单位以内。导出时 IK 被烘焙为关键帧。Spine 官方编辑器与解析器的往返验证未执行。

## 范围

这是一个技术性的形变案例，不代表角色设计、解剖结构、玩法时序或目标运行时已经验收。参考求值器不是正式运行时；游戏仍需导出自己的轨迹作为最终证据。所有素材由仓库代码生成，采用仓库的 MIT 许可证。
