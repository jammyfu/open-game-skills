# open-game-skills

<p align="center">
  <img src="docs/logo-banner.svg" alt="open-game-skills" width="640"/>
</p>

<p align="center">
  <a href="README.md">English</a> · <b>简体中文</b> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="README.ja.md">日本語</a> · <a href="README.ko.md">한국어</a>
</p>

<p align="center">
  <strong>做游戏用的通用 Agent Skill。</strong><br/>
  系统优先。工作室和引擎是可叠加的列，不是拿来抄的模板。先问列，再写代码。
</p>

给 OpenClaw、Claude Code、Codex、Cursor 用的开源 Skill 集群。
默认文档是 [English README](README.md)。

## 这是什么

- **学科** 决定信息、难度、装备、耐久、战斗、镜头、竞速、Boss 怎么跑
- **引擎 adapter** 只绑定六个原语
- **工作室 / 品类** 只负责选列，不再写一套规则

这不是引擎 API 手册。

## 动手前先问

|系统|问什么|
|---|---|
|地图|信息怎么挣？谁能插销？|
|难度|先改空间、资源，还是数值？|
|装备|换件 / 升级树 / 词缀 / 融合 / 永久 — 按槽位？|
|耐久|碎了换 / 磨刀 / 回点修 / 不坏？|
|战斗|短缓冲 / 长取消 / 承诺白名单 / 土狼平台|
|竞速| drift-kart / boost-rail / grip-weight / combat-arena |
|平台|手机 / 掌机座充 / 客厅 / 掌机 PC / 桌面 |

用户说「通用」：不要世界跟角色等级走，不要满地图任务箭，不要同一把剑又碎又能强化到终局，不要暗改极速。

## 安装

```bash
git clone https://github.com/jammyfu/open-game-skills.git
ln -sfn "$(pwd)/skills" ~/.openclaw/workspace/skills/open-game-skills
```

对 agent 说：「world-map 区域揭雾 + 玩家插销」「武器 A、防具 B、耐久碎换」「racing-feel 选 boost-rail，追赶 none」「platform-targets 手持与座充同一套模拟」。

## 许可

MIT。游戏名归原作者。Skill 写公开设计原则和可选列，不是资产或私有源码。

by jammyfu / PaintingCoder
