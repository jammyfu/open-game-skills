# open-game-skills

<p align="center">
  <img src="docs/logo-banner.svg" alt="open-game-skills" width="640"/>
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh.md">中文</a> · <a href="README.ja.md">日本語</a> · <b>한국어</b>
</p>

<p align="center">
  <strong>게임을 만들기 위한 범용 Agent Skill.</strong><br/>
  시스템이 먼저다. 스튜디와 엔진은 쌍는 열이지, 베끼는 템플릿이 아니다. 열을 고른 뒤 코드를 쓱니다.
</p>

OpenClaw / Claude Code / Codex / Cursor용 오픈 소스 Skill 모음입니다.
기본 문서는 [English README](README.md)입니다.

## 이것이 무엇인가

- **학과**가 정보·난이도·장비·내구·전투·카메라·레이스·Boss 규칙을 정합니다
- **엔진 어댑터**는 6개 원어만 바인딩합니다
- **스튜디 이름**은 열을 고를 뿐입니다

## 코드 전에 물을 것

| 시스템 | 질문 |
|---|---|
| 지도 | 정보는 어떻게 버나가? 누가 핀을 박나? |
| 난이도 | 공간, 자원, 숫자 중 무엇을 먼저? |
| 장비 | 교체 / 강화 트리 / 접두사 / 운합 / 영구 |
| 내구 | 부서고 교체 / 갈기 / 수리 / 안 부서짐 |
| 전투 | 짧은 버퍼 / 긴 캔슬 / 승인 화이트리스트 / 코요테 |
| 레이스 | drift-kart / boost-rail / grip-weight / combat-arena |
| 플랫폼 | 폰 / 핸드헬드-독 / 거실 / 핸드헬드 PC / 데스크톱 |

“범용”이라고 하면: 세계를 플레이어 레벨에 맞추지 말 것, 지도 전체에 퀘스트 화살표를 뽑지 말 것, 같은 칼에 “부서짐”과 “엔딩까지 강화”를 써지 말 것.

## 설치

```bash
git clone https://github.com/jammyfu/open-game-skills.git
ln -sfn "$(pwd)/skills" ~/.openclaw/workspace/skills/open-game-skills
```

## 라이선스

MIT. 작품명은 권리자에게 있습니다. Skill은 공개된 설계 원칙과 선택 가능한 열을 설명할 뿐입니다.

by jammyfu / PaintingCoder
