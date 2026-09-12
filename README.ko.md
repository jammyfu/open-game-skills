# open-game-skills

<p align="center">
  <img src="docs/1d3c92f2-8d52-412d-96e0-7b0e67be4f4f.png" alt="open-game-skills" width="640"/>
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a> · <a href="README.ja.md">日本語</a> · <b>한국어</b>
</p>

<p align="center">
  <strong>게임 제작용 범용 Agent Skill.</strong><br/>
  평소처럼 말하면 dispatcher가 skill과 열을 고른다.
</p>

기본 문서는 [English README](README.md).

## 먼저 말하기

[`skills/SKILL.md`](skills/SKILL.md) → [`dispatcher`](skills/dispatcher/SKILL.md).

```text
USE:
- <skill> / <모드>
ENGINE: none | unknown | custom | threejs | pixijs | phaser | cocos | godot | unity | unreal
ASK: <필요한 질문 하나 또는 빈칸>
DEFER: <후속 단계 또는 빈칸>
```

단계마다 전문 skill 최대 3개(에셋/2D 포함)와 필요한 engine 1개를 읽습니다. 나머지는 DEFER에 기록하고 다음 단계에서 처리합니다. `none`은 설계 작업이라 engine이 필요 없다는 뜻이고, `unknown`은 미확정, `custom`은 실제 사용자 정의 런타임을 뜻합니다. 추측으로 custom을 선택하지 않습니다.

역할과 검증 범위는 [공통 실행 규칙](skills/CONTRACT.md)을 참고하세요. [자동 생성된 전체 목록](skills/catalog.json)에는 모든 skill이 있습니다. 예시 표에는 주요 항목만 표시합니다.

| 말 | 불러야 할 것 |
|---|---|
| 스트리트 파이터식 3D | `fighting-design` / grounded-footsies · `action-feel` / short-special |
| 퀘스트 화살표 없는 오픈월드 | `world-map` · `camera-anti-clip` |
| 점프가 붕 뜬다 | `platform-jump` · `jump-leniency` |
| 처음 하는 사람도 클리어할 수 있는가 | `gameplay-validation` / real-input |
| 히트스턴이 너무 길다 | `hitstun-recover` · `enemy-kit-balance` |
| 컷씬 후 조작을 돌려줄 것 | `cutscene-handoff` |

## 엔진 어댑터

[custom](skills/engines/custom/SKILL.md) · [threejs](skills/engines/threejs/SKILL.md) · [pixijs](skills/engines/pixijs/SKILL.md) · [phaser](skills/engines/phaser/SKILL.md) · [cocos](skills/engines/cocos/SKILL.md) · [godot](skills/engines/godot/SKILL.md) · [unity](skills/engines/unity/SKILL.md) · [unreal](skills/engines/unreal/SKILL.md)

## 철칙

1. 히트스톱 ≠ 히트스턴. 유리 프레임 = 상대의 첫 행동 가능 tick − 자신의 첫 행동 가능 tick.
2. 플레이어 i-frame이나 스턴을 후려 적을 밸런스하지 말 것.
3. 텔레포트/잠금 해제/디버그는 자연 클리어가 아니다.
4. 결제와 외형은 캔슬 창이나 허트박스를 바꾸지 않는다.
5. 완성 스테이지나 프레임 테이블을 규칙에 넣지 말 것.

목록은 [English README](README.md).

## 설치

```bash
git clone https://github.com/jammyfu/open-game-skills.git
cd open-game-skills
python3 tools/install.py --target "$HOME/.openclaw/workspace/skills"
python3 tools/install.py --target "$HOME/.claude/skills"
```

위 경로는 예시입니다. 실제 Agent skills 디렉터리를 지정하세요. 기존 파일이나 다른 링크를 덮어쓰지 않습니다. `--dry-run`으로 확인하고, 필요하면 `--copy`를 사용하세요. 복사본 업데이트는 수동입니다. Python 3.10+가 필요합니다. Windows에서는 `python`과 명시적인 경로를 사용하세요. 각 Agent의 자동 검색은 별도 검증이 필요합니다.

## 기존 설치 업데이트

저장소 디렉터리에서 실행하세요. 먼저 커밋하지 않은 변경 사항을 커밋하거나 별도로 보관하세요. 브랜치가 갈라졌다면 차이를 조정하고 강제로 초기화하지 마세요.

```bash
git switch main
git pull --ff-only origin main
```

심볼릭 링크 설치는 업데이트된 소스를 바로 참조합니다. `--copy`로 설치했다면 기존 설치 디렉터리를 명시적으로 백업하거나 옮긴 뒤 다시 복사하세요. 설치 프로그램은 덮어쓰지 않습니다. 이 작업은 게임을 업데이트하거나 Agent 설정을 변경하지 않습니다.

## 개발 검사

가상 환경에서 Python 3.10+를 사용하고 저장소 루트에서 실행하세요. Windows에서는 예시의 `python3`를 `python`으로 바꾸세요.

```bash
python3 -m pip install -r requirements-dev.txt
python3 -m unittest discover -s tests -v
python3 tools/skill_quality.py --check-catalog
```

skill을 추가, 삭제하거나 이름을 바꾼 뒤 목록을 다시 생성하고 테스트를 다시 실행하세요.

```bash
python3 tools/skill_quality.py --write-catalog --check-catalog
```

이 검사는 메타데이터, 로컬 참조, 목록 일관성, 설치 프로그램 동작, 다국어 README의 공통 정보를 확인합니다. LLM 라우팅 정확도, engine 호환성, 사람이 실제로 플레이할 수 있는지, 번역 품질을 보장하지 않습니다. 범위는 [기여 안내](CONTRIBUTING.md)를 참고하세요. 나머지 skill의 상세 검토는 아직 완료되지 않았습니다.

MIT. by jammyfu / PaintingCoder
