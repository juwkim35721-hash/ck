# sk — SK하이닉스 해커톤 Codex 키트

담당자 DM으로 요구사항·제약을 먼저 확정하고, 명세를 한 번에 정리한 뒤 구현·검증·보고서·후속 6문항 대비까지 진행하도록 돕는 **Codex 스킬 37개 + 단계별 전략 프롬프트 37개** 모음입니다. 운영 방법 전체는 [MASTER_GUIDE](playbooks/MASTER_GUIDE.md)에 있습니다. 공식 대회 공지와 과제 문서가 항상 우선합니다.

## 빠른 시작 — 모두 과제 루트에서

```bash
git clone https://github.com/juwkim35721/sk sk
python3 sk/scripts/install.py
codex
```

과제 루트는 시험이 준 실제 과제 폴더입니다. 설치 프로그램은 `sk`의 부모 폴더를 과제 루트로 보고, 과제 루트 `AGENTS.md`에 관리 구역을 추가하고, 스킬을 `.agents/skills/`에 복사하고, 작업 노트 폴더 `sk/work/`를 만듭니다. 기존 파일은 덮어쓰기 전에 `sk/.install/backups/`에 백업합니다. 프롬프트는 다른 터미널에서 `python3 sk/scripts/help.py`로 꺼내 봅니다.

## 구성

| 경로 | 내용 |
| :--- | :--- |
| [`playbooks/MASTER_GUIDE.md`](playbooks/MASTER_GUIDE.md) | 설치 약속, 시간 흐름, DM·명세 동결 전략, 막힐 때 대응, 제출·6문항 대비 |
| [`prompts/`](prompts/README.md) | 단계별 폴더 10개(`0-start` … `9-qa`)의 전략 프롬프트 |
| `skill/sk-*/SKILL.md` | 프롬프트와 1:1로 대응하는 스킬 원본 (설치 시 `.agents/skills/`로 복사) |
| `harness/AGENTS.md` | 과제 루트 `AGENTS.md` 관리 구역에 들어가는 공통 규칙 |
| `templates/` | 담당자 DM 질문 양식, 보고서 양식, 6문항 암기 카드 양식 |
| `snippets/` | `data_audit.py`(CSV·JSON·JSONL 감사), `smoke_test.py`(HTTP 도달성 확인) |
| `scripts/install.py` | 설치·점검(`--check`)·계획(`--dry-run`)·제거(`--uninstall`) |
| `scripts/help.py` | 프롬프트·템플릿·작업 노트 조회 |

## 단계

| 폴더 | 단계 | 프롬프트 |
| :--- | :--- | :--- |
| `0-start` | 착수 | 0.1 context · 0.2 triage · 0.3 code-map |
| `1-discover` | 요구사항 발굴·담당자 DM | **1.0 clarify-loop**(스캔·질문·후속 질문 반복) · 1.1 requirements · 1.2 ambiguity · 1.3 dm-questions · 1.4 dm-answers · 1.5 dm-confirm |
| `2-spec` | 구현 전 명세 정리·동결 | 2.1 spec · 2.2 io-contract · 2.3 acceptance · 2.4 spec-gate |
| `3-plan` | 계획·설계 | 3.1 plan · 3.2 design · 3.3 decision-log |
| `4-build` | 구현 | **4.0 build-loop**(슬라이스 하나를 착수 점검→RED→GREEN→방어→검증까지 한 번에) · 4.1 test-first · 4.2 implement · 4.3 harden |
| `5-verify` | 검증·증거 | 5.1 verify · 5.2 evidence · 5.3 data-validation · 5.4 api-contract · 5.5 ui-smoke |
| `6-debug` | 디버깅·복구·시간 관리 | 6.1 debug · 6.2 unstuck · 6.3 rollback · 6.4 resume · 6.5 timebox |
| `7-review` | 리뷰·준수 감사 | 7.1 review · 7.2 compliance |
| `8-submit` | 문서화·제출 | 8.1 report · 8.2 deliver |
| `9-qa` | 후속 서술형 6문항 대비 | 9.1 understand · 9.2 qa-card · 9.3 qa-drill · 9.4 retrospect |

## 지키는 것

Codex는 담당자에게 DM을 보내지 않고 복붙용 메시지만 만듭니다. 외부 push·배포·제출, `git reset --hard`·`clean`·`stash`, 원본 데이터·기존 테스트 삭제, Codex 업데이트는 하지 않습니다. 6문항 대비 자료는 AI 사용이 허용된 시간에만 만들고, AI 금지 단계가 시작되면 사용을 멈춥니다. 작업 노트(`sk/work/`)와 설치 기록(`sk/.install/`)은 이 저장소에 올라가지 않습니다.
