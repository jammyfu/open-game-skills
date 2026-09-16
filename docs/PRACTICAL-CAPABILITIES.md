# 实用生产能力补充 / Practical production capabilities

## 为什么这样补

以 `8051a36b44e38d641db2bd6fc15314468bc86234` 的 189 个 Skill 为基线。当前目录已有动作、输入、战斗、相机、随机生成、存档、联网、资源和评测等职责；本次重点不是重复命名，而是把素材、可玩场景、角色动作、性能和回归证据衔接起来。

比较过三种路径：继续扩充玩法目录、为每个问题新建 Skill、增强现有 owner 并仅补真正缺失的 owner。本次采用第三种：新增 `scene-assembly`，加强七个已有专业 Skill，再补两个可直接调用的标准库工具。已有三专业 Skill 加一引擎的阶段上限不变。独立 LLM A/B 工具已在基线中，不重复实现，也不把其 blocked 记录改成通过。

## 能力与责任

| 能力 | 所属 Skill | 新增交付 |
|---|---|---|
| 素材拼成场景 | scene-assembly（新增） | 组件角色、连接点、摆放记录、出生点/门洞保护区、静态布局预检 |
| 素材适配后再复用 | open-asset-fixture + model-pipeline | 尺度、接触平面、插槽、解码依赖与能力不匹配的明确交接 |
| 动作库跨角色迁移 | character-rig + animation-graph | 语义骨骼映射、静止姿态修正、唯一根位移应用路径、支撑面相对脚滑指标 |
| 保留形象的多档减模 | model-pipeline | 轮廓/关节/插槽保真、实际三角形计数、LOD切换滞回、风格变体与LOD分开 |
| 图形丢失后的资源恢复 | asset-runtime | 内容/CPU描述与GPU代次分离、过期上传防护、有限重试、无重复结算 |
| 回放故障定位 | gameplay-harness | 比较条件门槛、首个偏差tick和字段、原始证据保留、失败案例回归流程 |
| 灰盒换美术不破坏玩法 | level-blockout | 受保护空间和稳定碰撞/门禁身份移交给场景装配 |

这不包含新的自动减模器、自动重定向算法、完整GPU恢复实现或万能场景生成器；相关新增内容是可复用的执行协议、检查方法和评测输入，实际适配仍需在目标项目执行。

## 工具一：场景预检

```sh
python skills/disciplines/scene-assembly/scripts/scene_preflight.py skills/disciplines/scene-assembly/assets/layout.example.json
```

素材准备可先运行 `python skills/assets/open-asset-fixture/scripts/prepare_assets.py --skill scene-assembly`。默认只筛选静态环境候选，不保证是完整且尺寸兼容的组件包；缺少本地锁时，`--pinned-only` 明确阻塞。该目录版本只新增选择配置，没有重新核验已有素材来源。

输入为米制、Y向上的世界空间 AABB 布局。检查房间重叠、物体越界、出生点净空、门洞宽高、门槛高差、门洞是否位于共用边界、门口阻塞、目标房间图可达性。矩形房间/平地/双向居中门洞是明确限制。

例：角色半径0.35m、净空0.1m，所需门宽为0.9m；门宽0.7m时应失败并使该连接不进入可达图。这些数字仅来自合成示例，不是通用游戏标准。

**不是物理引擎或导航网格。** 房间图连通不代表房间内部没有阻断，也不证明跳跃、锁钥谜题或相机可用。模型测量数据需由实际导入器提供；静态工具不读取GLB/OBJ、不获取素材、不生成画面。

## 工具二：回放差异定位

```sh
python skills/disciplines/gameplay-harness/scripts/trace_compare.py baseline.trace.json candidate.trace.json --output /new/comparison.json
```

完整格式见 [回放协议](../skills/disciplines/gameplay-harness/reference/regression-diagnosis.md)。需由当前引擎适配器导出标准化 trace v1，不可把任意旧报告直接传入。比较前要求适配器、oracle、逻辑时钟、输入哈希、初始状态哈希、RNG身份相同；构建SHA可以不同。

比较完整导出的稳定状态与有序事件，返回第一个不一致tick及JSON-pointer字段。记录顺序变更不误判为字典内容改变；事件顺序改变、缺字段、截断、布尔值混成数值都会被区分。默认不判断问题属于游戏还是测试器，也不自动改golden。

两个CLI的退出码：0=当前工具范围通过，1=有效输入未通过检查，2=条件不兼容/输入错误/环境阻塞。输出有输入和工具哈希，拒绝覆盖已有文件；父目录需可信。离线比较不验证哈希声明对应的模型调用是否真实。

## 一次实际任务如何组合

“用现有地牢素材搭一个室内对战场景”按阶段执行，而不是一次加载所有专业Skill：

| 阶段 | 最多三个专业 owner | 阶段产物 |
|---|---|---|
| 素材准备 | open-asset-fixture、model-pipeline、character-rig（有角色时） | 固定来源和字节、适配记录、动作兼容记录 |
| 场景落地 | level-blockout、scene-assembly、asset-runtime | 场景与保护区、资源所有权、预检结果 |
| 行为验证 | gameplay-harness、gameplay-validation、game-qa | 目标引擎运行、回放、首个偏差、明确证据范围 |

每阶段只添加已经确定且必要的引擎适配器；现有引擎不因示例变更。没有角色需求时不加载character-rig；纯状态或布局工具测试不下载美术。

## 验证与状态

本轮先写 `tests/test_practical_capability_tools.py`，观察到两个工具缺失导致测试失败，再实现工具并执行。新增Skill的三类案例和七个既有Skill扩展案例是**已编写/契约审查**，不是独立LLM或引擎执行结果。

复现：

```sh
python -m unittest discover -s tests -p test_practical_capability_tools.py -v
python -m unittest discover -s tests -v
node --test tests/behavior/behavior.test.mjs
python tools/skill_quality.py --check-catalog
python tools/engineering_quality.py
```

`skills/catalog.json` 与逐Skill案例覆盖一起维护，README五种语言入口同步。六项engineering registry的原始范围/模式不扩展；新owner通过通用目录和案例系统注册。目录变成190项不意味着190项都经过行为评测。

以前的实测证据继续绑定以前的源码；修改过的Skill不能沿用旧哈希宣布新能力已通过。本次未运行新的浏览器/引擎、独立模型A/B或真人试玩。证据包应分别保存本轮工具执行日志和既有引擎实测，不合并冒充同一轮。

## 后续最值得做什么

优先让真实Three.js/Godot项目导出布局测量和trace v1，运行“素材→装配→穿门→战斗→重试”最小闭环。随后对根位移/脚接触、LOD轮廓误差、真实设备丢失恢复各补独立可执行样例。暂缓增加更多风格预设、重复玩法owner或额外模型A/B框架。

## 历史实验兼容修复

更新asset-runtime主文档时，旧A/B v1的源哈希保护正确报错。本次没有重新计算旧pin或改写旧结果，而是保留原始Skill字节快照，并使该实验只读取原始哈希对应的文本。生成元数据记录实际source_locations；快照缺失且当前文本已变化、快照被篡改或为符号链接、其它输入漂移仍会阻塞。旧A/B条件差异断言改为检查归档的原始文本，不接受新增指导混入旧实验。

这修复了“Skill继续演进”和“旧实验保持可复现”之间的冲突，不会把旧版本的结论继承给新版本。详见[历史输入说明](../tests/behavior/experiments/asset-runtime-ab-v1/SNAPSHOT.md)。
