# 단계별 전략 프롬프트

문제 해결을 12개 기본 단계와 6개 보조 상황으로 나누었습니다. 각 Markdown에는 사용 시점·필요 입력·전략·기본 프롬프트·심화/반증 프롬프트·완료 기준을 담았습니다. 단계 이름을 기계적으로 모두 실행하기보다 현재 병목에 필요한 파일을 선택하세요.

설치·시간 배분·백업 복구는 [MASTER_GUIDE](../playbooks/MASTER_GUIDE.md), 전체 구조는 [저장소 README](../README.md)를 참고하세요. 모든 스킬은 [skill/](../skill)에 통합되어 있으며 기존 `cofa-*`의 역할은 대응하는 `sk-*`로 병합했습니다. `snippets/`, `templates/`는 원본을 보존합니다.

## 사용 방법

일반 터미널에서 문서를 열고, 코드 블록 안의 프롬프트만 Codex 입력창에 전달합니다. `[과제 루트]`, `[남은 시간: 분]`, `[요구사항/답변]` 등은 실제 값으로 바꾸고, 없는 정보는 미확인으로 남깁니다. `$sk-*` 호출이 지원되지 않으면 호출 부분만 빼고 사용하세요.

```bash
bash /tmp/cofa-kit/help.sh list
bash /tmp/cofa-kit/help.sh 01
bash /tmp/cofa-kit/help.sh debug
bash /tmp/cofa-kit/help.sh --search 경계
```

기본 키트가 아니라면 `COFA_KIT_DIR` 또는 실제 키트 경로를 사용합니다. 설치 전에는 `bash ~/sk/scripts/help.sh 01`로 볼 수 있습니다. 공식 규정상 AI 사용이 허용된 단계에서만 쓰고, 후속 AI 금지 평가에서는 프롬프트·스킬·자료 사용을 중단합니다.

## 기본 12단계

00~05는 먼저 문제·정책·계약·계획을 확인하는 흐름입니다. 06~08은 작은 기능별로 반복하고, 09 리뷰에서 발견한 문제는 06~08로 되돌립니다. 10은 제출 준비이고, 11은 허용되는 설명·인수인계·회고입니다.

| 단계 | 프롬프트 | 대응 스킬 | 핵심 산출물 |
| :--- | :--- | :--- | :--- |
| 00 | [환경·규칙·기준선 확인](00-context.md) | [`$sk-context`](../skill/sk-context/SKILL.md) | 환경·제약 요약, 실제 실행 명령과 결과, 수정 금지 범위, 다음 확인 항목 |
| 01 | [문제 정의·완료 기준](01-define.md) | [`$sk-define`](../skill/sk-define/SKILL.md) | 요구사항 목록, 수용 기준, 필수 제출 파일, 미확인 가정과 비목표 |
| 02 | [정책·모호성 확인](02-clarify.md) | [`$sk-clarify`](../skill/sk-clarify/SKILL.md) | 영향도 높은 질문 최대 3개, 정책 결정 기록, 미응답 시 가정·되돌릴 지점 |
| 03 | [입출력·데이터 계약 분석](03-data-contract.md) | [`$sk-data-contract`](../skill/sk-data-contract/SKILL.md) | 입출력 계약, 데이터 특성·검사 한계, 정책 확인 후보, 계약별 테스트 입력 |
| 04 | [우선순위·위험 기반 실행 계획](04-plan.md) | [`$sk-plan`](../skill/sk-plan/SKILL.md) | 우선순위 백로그, 시간 예산, 의존성, 단계별 완료 기준, 축소·중단 조건 |
| 05 | [대안 비교·최소 설계](05-design.md) | [`$sk-design`](../skill/sk-design/SKILL.md) | 대안 비교, 선택 근거, 수정 파일·인터페이스, 최소 구현 순서와 위험 |
| 06 | [수직 슬라이스 구현](06-implement.md) | [`$sk-implement`](../skill/sk-implement/SKILL.md) | 구현한 요구사항 ID, 변경 파일·함수, 실행 증거, 남은 작업과 한계 |
| 07 | [예외·경계·불변식 방어](07-harden.md) | [`$sk-harden`](../skill/sk-harden/SKILL.md) | 재현 입력·기대 동작·수정·회귀 테스트 연결, 해당 없음 이유, 잔여 위험 |
| 08 | [요구사항 추적·독립 검증](08-verify.md) | [`$sk-verify`](../skill/sk-verify/SKILL.md) | 요구사항-테스트 대응, 정확한 명령·통과/실패, 독립 기대값, 미검증 항목 |
| 09 | [반증 중심 코드 리뷰](09-review.md) | [`$sk-review`](../skill/sk-review/SKILL.md) | 심각도별 근거 있는 발견 사항, 파일·라인·재현, 회귀 영향, 발견 없음과 검토 한계 |
| 10 | [제출·릴리스 준비](10-deliver.md) | [`$sk-deliver`](../skill/sk-deliver/SKILL.md) | 제출 파일 점검, 재현 명령, 실제 검증 결과, 남은 문제, 제출 전 최종 체크 |
| 11 | [설명·인수인계·회고](11-retrospect.md) | [`$sk-retrospect`](../skill/sk-retrospect/SKILL.md) | 설계/동작/검증 3문장 설명, 사실 기반 개선점, 인수인계와 연습 질문 |

## 보조 상황 6종

오류·맥락·시간 문제 또는 해당 과제 유형이 있을 때만 추가합니다. 없는 API·UI·ML 기능을 새로 만들기 위한 목록이 아닙니다.

| 상황 | 프롬프트 | 대응 스킬 | 핵심 산출물 |
| :--- | :--- | :--- | :--- |
| 90 | [가설 기반 디버깅](90-debug.md) | [`$sk-debug`](../skill/sk-debug/SKILL.md) | 재현 명령, 원인 가설·판별 근거, 최소 수정, 재실행 결과 |
| 91 | [맥락 복구·작업 인수인계](91-resume.md) | [`$sk-resume`](../skill/sk-resume/SKILL.md) | 짧은 상태 캡슐, 사실·주장 구분, 마지막 검증, 다음 작업 하나 |
| 92 | [시간 부족·범위 축소](92-timebox.md) | [`$sk-timebox`](../skill/sk-timebox/SKILL.md) | 남은 시간 예산, P0/P1 작업, 중단 목록, 최소 검증·제출 순서 |
| 93 | [집계·이상탐지 데이터 검증](93-data-validation.md) | [`$sk-data-validation`](../skill/sk-data-validation/SKILL.md) | 포함/제외 규칙, 독립 합계·행 수, 누수·시간 경계 검사, 재현 가능한 검증 결과 |
| 94 | [API 계약·상태 전이 검증](94-api-contract.md) | [`$sk-api-contract`](../skill/sk-api-contract/SKILL.md) | 메서드/경로별 계약 테스트, 본문 assert, 상태 전이·멱등성 결과, 미검증 항목 |
| 95 | [UI 핵심 흐름·접근성 점검](95-ui-smoke.md) | [`$sk-ui-smoke`](../skill/sk-ui-smoke/SKILL.md) | 사용자 흐름별 기대/실제, 화면·API 연동 확인, 접근성·실패 상태, 미검증 목록 |

## 프롬프트를 연결하는 공통 계약

요구사항은 `R1`, `R2` 같은 ID로 구분하고 수용 기준·구현·테스트를 연결합니다. 다음 단계에는 실제 확인한 정책, 변경 파일·함수, 정확한 실행 명령·결과, 남은 위험만 전달합니다. 새 보고서 파일은 과제가 요구하거나 사용자가 요청한 경우 지정 경로에만 저장합니다.

읽기 전용 분석·계획·리뷰와 수정·테스트 실행을 구분합니다. 원본 데이터와 관련 없는 변경을 보존하고, 스펙 밖 기본값·임의 중복 제거·실패 테스트 삭제로 문제를 숨기지 않습니다. 장황한 사고과정 대신 간결한 판단 근거와 검증 증거를 요청합니다.

`출시`는 기본적으로 해커톤 제출·릴리스 준비입니다. 외부 push·배포·실제 제출 버튼 조작·민감정보 전송은 자동 수행하지 않으며 별도 권한과 공식 규정을 따릅니다.

이 인덱스는 `harness/stages.json`을 기준으로 `python3 scripts/build_prompt_index.py`에서 재생성할 수 있습니다.
