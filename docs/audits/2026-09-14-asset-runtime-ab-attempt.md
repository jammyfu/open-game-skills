# asset-runtime A/B：首次真实执行记录

## 结论

实验代码已提交 main 并实际启动 GitHub Actions，但独立模型采样尚未发生。不能报告有/无 Skill 的成功率或提升幅度。

代码提交：`804a53ec3099bad8f94d8a5ec52c1c12cb3d6fdf`。
固定基线：`3cf5e4a024e1b338db3ef3ce5cb92699ecdee08e`。

## 真实远端执行

- 工作流：Skill A-B experiment，run `34776887240`，attempt `1`。
- 生成 job `103776522358`：16 项实验工具测试通过；生成步骤退出码 2。
- 报告状态：`blocked`。
- 原因：`OPENAI_API_KEY is not configured`。该工作流收到的环境变量为空；未读取或暴露任何密钥值。
- 实际模型请求：`provider_calls: 0`。
- 12 个计划样本全部 `not-run`，两个条件各 6 个；没有 response.json 或生成候选。
- evaluate job `103776543975` 被跳过：不是模型生成失败或引擎判定失败。
- 两组成功率、配对差值、统计检验均无观测值；不能写成 0% 成功率。
- 记录开始时间：`2026-09-13T19:10:49.093470+00:00`。

原始 artifact：`skill-ab-collection-34776887240-1`，ID `10324121603`，16 个文件。
ZIP SHA-256：`cc10f7e573b4b895fdb2a5c87c10e1b89d276347e27bd1dad62d9bf49070dd7e`。
下载后重新计算了 ZIP 哈希、检查了 collection.json 和全部样本状态，确认没有独立模型响应。没有拿参考实现或合成测试数据替代。

运行记录：https://github.com/jammyfu/open-game-skills/actions/runs/34776887240

## 已固定的实验

单任务 `asset-runtime`；固定快照 `gpt-4.1-mini-2025-04-14`；6 组配对、12 次独立请求。每组顺序随机，请求之间不共享对话。

相同任务、接口、模型、temperature=0.5、4096 输出 token 上限和 JSON schema。只有处理组额外获得完整 asset-runtime/SKILL.md；两组都不给参考实现、测试答案或本次聊天内容。只生成 asset-pool.mjs，simulation.mjs、素材、引擎、判定器固定。

没有 API 自动重试、人工修改、样本替换或挑选最佳结果。所有计划行保留。完整计划及输入哈希见 `tests/behavior/experiments/asset-runtime-ab-v1/plan.json`。

预留估算 $0.105055；配置的 $0.50 是估算检查阈值，不是账户账单硬上限。固定请求上限是 12 次、每次 4096 输出 token。本次没有发出模型请求。

## 不等于 A/B 结果的已执行验证

- 本地全库 Python：365 通过；Node：6 通过；189 Skill 静态错误：0。
- 实验工具单元测试：16 通过，使用明确标注的合成响应，不算真实模型样本。
- 本地参考 Three.js/Chromium：21 项检查与 5 个错误对照通过，仅证明参考运行环境可用。
- 首次无 Xvfb 的参考执行未能创建 WebGL，保留失败；相同代码通过 xvfb-run 执行成功，没有修改判定规则。
- 提交 804a53e 的远端 Skill quality run `34776887201`：success。
- 同提交 Behavior runtime run `34776887196`：success。
- A/B 工作流红灯来自凭据缺失，与上述代码和参考引擎验证分开记录。

## 解除阻塞

在本仓库 Settings → Secrets and variables → Actions → Secrets → New repository secret 中保存名为 `OPENAI_API_KEY` 的有效 OpenAI API 凭据。不要写入源码、日志或聊天。组织级同名 Secret 必须允许本仓库访问。

随后打开 Actions → Skill A-B experiment → Run workflow，选择 main，并勾选 `confirm_bounded_api_calls`。生成与执行使用不同 job，只有生成步骤接收 API key。不要改变已固定的题目、Skill 或判定器来追求更好的结果。

每次执行以 run ID 和 attempt ID 共同区分，原始阻塞记录不能被覆盖。后续重跑是单独授权的新一批最多 12 次请求，不应与旧批次混成一个结果。

官方说明：
- https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets
- https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow

没有修改 Secret、计费设置或 Marketplace。即使后续 12 个样本完成，单任务六对样本也只支持探索性结论，不代表全库 Skill 的普遍效果。本次审计文档提交不修改实验计划，不会再次触发付费采样。
