# open-game-skills

<p align="center">
  <img src="docs/1d3c92f2-8d52-412d-96e0-7b0e67be4f4f.png" alt="open-game-skills" width="640"/>
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="README.ja.md">日本語</a> · <b>한국어</b>
</p>

<p align="center">
  <strong>게임 제작용 범용 Agent Skill.</strong><br/>
  평소히 말하면 dispatcher가 skill과 열을 고른다.
</p>

기본 문서는 [English README](README.md).

## 먼저 말하기

[`skills/SKILL.md`](skills/SKILL.md) → [`dispatcher`](skills/dispatcher/SKILL.md). 출력은 `USE / ENGINE / ASK`. 최대 3 discipline + 1 engine.

| 말 | 불러야 할 것 |
|---|---|
| 스트리트 파이터식 3D | `fighting-design` / grounded-footsies · `action-feel` / short-special |
| 퀘스트 화살표 없는 오픈월드 | `world-map` · `camera-anti-clip` |
| 점프가 떠다 | `platform-jump` · `jump-leniency` |
| 초심자가 깨는가 | `gameplay-validation` / real-input |
| 히트스턴이 너무 길다 | `hitstun-recover` · `enemy-kit-balance` |
| 컷씬 뒤에 조이스틱을 돌려줄 것 | `cutscene-handoff` |

## 철칙

1. 히트스톱 ≠ 히트스턴. 이점 = stun − recover.
2. 플레이어 i-frame이나 스턴을 후려 적을 밸런스하지 말 것.
3. 텔레포트/잠금 해제/디버그는 자연 클리어가 아니다.
4. 결제와 외형은 캔슬 창이나 허트박스를 바꾸지 않는다.
5. 완성 스테이지나 프레임 테이블을 규칙에 넣지 말 것.

목록은 [English README](README.md).

```bash
git clone https://github.com/jammyfu/open-game-skills.git
ln -sfn "$(pwd)/skills" ~/.openclaw/workspace/skills/open-game-skills
```

MIT. by jammyfu / PaintingCoder
