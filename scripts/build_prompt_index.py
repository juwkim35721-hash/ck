#!/usr/bin/env python3
"""harness/stages.json으로 prompts/README.md를 재생성한다."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
stages = json.loads((ROOT / "harness/stages.json").read_text(encoding="utf-8"))
lines = [
    "# 단계별 전략 프롬프트", "",
    "문제 해결을 12개 기본 단계와 6개 보조 상황으로 나누었습니다. 각 Markdown에는 사용 시점·필요 입력·전략·기본 프롬프트·심화/반증 프롬프트·완료 기준을 담았습니다. 단계 이름을 기계적으로 모두 실행하기보다 현재 병목에 필요한 파일을 선택하세요.", "",
    "설치·시간 배분·백업 복구는 [MASTER_GUIDE](../playbooks/MASTER_GUIDE.md), 전체 구조는 [저장소 README](../README.md)를 참고하세요. 새 스킬은 [custom-skills/](../custom-skills)에 분리되어 있고 기존 `skills/`, `snippets/`, `templates/`는 보존되어 있습니다.", "",
    "## 사용 방법", "",
    "일반 터미널에서 문서를 열고, 코드 블록 안의 프롬프트만 Codex 입력창에 전달합니다. `[과제 루트]`, `[남은 시간: 분]`, `[요구사항/답변]` 등은 실제 값으로 바꾸고, 없는 정보는 미확인으로 남깁니다. `$sk-*` 호출이 지원되지 않으면 호출 부분만 빼고 사용하세요.", "",
    "```bash", "bash /tmp/cofa-kit/help.sh list", "bash /tmp/cofa-kit/help.sh 01", "bash /tmp/cofa-kit/help.sh debug", "bash /tmp/cofa-kit/help.sh --search 경계", "```", "",
    "기본 키트가 아니라면 `COFA_KIT_DIR` 또는 실제 키트 경로를 사용합니다. 설치 전에는 `bash ~/sk/scripts/help.sh 01`로 볼 수 있습니다. 공식 규정상 AI 사용이 허용된 단계에서만 쓰고, 후속 AI 금지 평가에서는 프롬프트·스킬·자료 사용을 중단합니다.", "",
    "## 기본 12단계", "",
    "00~05는 먼저 문제·정책·계약·계획을 확인하는 흐름입니다. 06~08은 작은 기능별로 반복하고, 09 리뷰에서 발견한 문제는 06~08로 되돌립니다. 10은 제출 준비이고, 11은 허용되는 설명·인수인계·회고입니다.", "",
    "| 단계 | 프롬프트 | 대응 스킬 | 핵심 산출물 |", "| :--- | :--- | :--- | :--- |"
]
for s in stages:
    if s["kind"] == "core":
        lines.append(f"| {s['id'].split('-',1)[0]} | [{s['title']}]({s['id']}.md) | [`${s['skill']}`](../custom-skills/{s['skill']}/SKILL.md) | {s['output']} |")
lines += ["", "## 보조 상황 6종", "", "오류·맥락·시간 문제 또는 해당 과제 유형이 있을 때만 추가합니다. 없는 API·UI·ML 기능을 새로 만들기 위한 목록이 아닙니다.", "", "| 상황 | 프롬프트 | 대응 스킬 | 핵심 산출물 |", "| :--- | :--- | :--- | :--- |"]
for s in stages:
    if s["kind"] == "support":
        lines.append(f"| {s['id'].split('-',1)[0]} | [{s['title']}]({s['id']}.md) | [`${s['skill']}`](../custom-skills/{s['skill']}/SKILL.md) | {s['output']} |")
lines += ["", "## 프롬프트를 연결하는 공통 계약", "",
    "요구사항은 `R1`, `R2` 같은 ID로 구분하고 수용 기준·구현·테스트를 연결합니다. 다음 단계에는 실제 확인한 정책, 변경 파일·함수, 정확한 실행 명령·결과, 남은 위험만 전달합니다. 새 보고서 파일은 과제가 요구하거나 사용자가 요청한 경우 지정 경로에만 저장합니다.", "",
    "읽기 전용 분석·계획·리뷰와 수정·테스트 실행을 구분합니다. 원본 데이터와 관련 없는 변경을 보존하고, 스펙 밖 기본값·임의 중복 제거·실패 테스트 삭제로 문제를 숨기지 않습니다. 장황한 사고과정 대신 간결한 판단 근거와 검증 증거를 요청합니다.", "",
    "`출시`는 기본적으로 해커톤 제출·릴리스 준비입니다. 외부 push·배포·실제 제출 버튼 조작·민감정보 전송은 자동 수행하지 않으며 별도 권한과 공식 규정을 따릅니다.", "",
    "이 인덱스는 `harness/stages.json`을 기준으로 `python3 scripts/build_prompt_index.py`에서 재생성할 수 있습니다.", ""]
(ROOT / "prompts/README.md").write_text("\n".join(lines), encoding="utf-8")
print(f"프롬프트 인덱스 생성: {len(stages)}개 단계")
