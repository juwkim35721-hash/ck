# 단계별 전략 프롬프트

문제를 푸는 과정을 10개 단계 폴더로 나누고, 각 단계에서 쓸 프롬프트를 모았습니다. 모든 프롬프트는 같은 이름의 스킬(`$sk-...`)을 호출하며, 결과를 `sk/work/` 작업 노트의 정해진 섹션에 남깁니다. 전체 운영 흐름은 [MASTER_GUIDE](../playbooks/MASTER_GUIDE.md)를 보세요.

## 쓰는 법

터미널 2(과제 루트)에서 꺼내 Codex 입력창에 붙여 넣습니다. `<...>` 자리는 실제 값으로 바꿉니다.

```bash
python3 sk/scripts/help.py            # 전체 목록
python3 sk/scripts/help.py 1.3 -p     # 1.3의 기본 프롬프트만 출력
python3 sk/scripts/help.py 1.3 -b     # 심화·변형 블록 목록
python3 sk/scripts/help.py flow       # 권장 순서
```

각 파일은 `언제 쓰나 → 준비할 입력 → 전략 → 기본 프롬프트 → 심화 프롬프트 → 변형 → 결과물 확인 → 다음 단계 → 주의` 순서로 되어 있습니다.

## 권장 순서

```text
0 착수      0.1 → 0.2 → 0.3
1 발굴·DM   1.0 (권장: 스캔 → 질문 → 답변 붙여넣기 → 후속 질문을 라운드로 반복)
            또는 1.1 → 1.2 → 1.3 → (내가 DM 전송, 답변 붙여넣기) → 1.4 → 1.5
2 명세      2.1 → 2.2 → 2.3 → 2.4        ← READY 전에는 구현하지 않음
3 계획      3.1 → 3.2   (3.3은 결정이 생길 때마다)
4·5 구현    슬라이스마다 4.0 (권장: 착수 점검 → RED → GREEN → 방어 → 검증을 한 바퀴로)
            또는 4.1 → 4.2 → 4.3 → 5.1 / 5.2  (+ 5.3 데이터 · 5.4 API · 5.5 UI)
6 막힐 때    6.1 debug · 6.2 unstuck · 6.3 rollback · 6.4 resume · 6.5 timebox
7 리뷰      7.1 → 7.2
마무리      9.1 → 9.4 → 8.1 → 9.2 → 8.2 → 9.3   (6문항 대비는 제출 전 AI 허용 시간에만)
```

## `0-start` — 착수 — 환경·과제 유형·코드 지도

설치 확인, 실행·테스트 기준선, 과제 유형 판별, 기존 코드 구조 파악. 과제 파일은 읽기만 한다.

| ID | 프롬프트 | 스킬 | 작업 노트 | 사용 자료 |
| :--- | :--- | :--- | :--- | :--- |
| 0.1 | [환경·규칙·기준선 확인](0-start/0.1-context.md) | `$sk-context` | `BRIEF.md` | — |
| 0.2 | [과제 유형 판별·공략 경로 선택](0-start/0.2-triage.md) | `$sk-triage` | `BRIEF.md` | — |
| 0.3 | [기존 코드 지도 작성](0-start/0.3-code-map.md) | `$sk-code-map` | `BRIEF.md` | — |

## `1-discover` — 요구사항 발굴·담당자 DM

문서·코드·테스트·데이터에서 요구사항과 제약을 뽑고, 모호성을 찾아 담당자 DM으로 확정한다. 이 단계가 구현 품질을 결정한다.

| ID | 프롬프트 | 스킬 | 작업 노트 | 사용 자료 |
| :--- | :--- | :--- | :--- | :--- |
| 1.0 | [질의 루프 — 전체 스캔·DM·후속 질문 반복](1-discover/1.0-clarify-loop.md) | `$sk-clarify-loop` | `DISCOVERY.md`, `DM_LOG.md` | `sk/templates/DM_QUESTION_TEMPLATES.txt`, `sk/snippets/data_audit.py` |
| 1.1 | [요구사항·제약·제출물 추출](1-discover/1.1-requirements.md) | `$sk-requirements` | `DISCOVERY.md` | — |
| 1.2 | [모호성·충돌·누락 탐지](1-discover/1.2-ambiguity.md) | `$sk-ambiguity` | `DISCOVERY.md` | `sk/snippets/data_audit.py` |
| 1.3 | [담당자 DM 질문 설계 (DM 템플릿 사용)](1-discover/1.3-dm-questions.md) | `$sk-dm-questions` | `DM_LOG.md` | `sk/templates/DM_QUESTION_TEMPLATES.txt` |
| 1.4 | [담당자 답변 기록·해석·후속 질문](1-discover/1.4-dm-answers.md) | `$sk-dm-log` | `DM_LOG.md` | — |
| 1.5 | [이해 재진술·최종 확인 메시지](1-discover/1.5-dm-confirm.md) | `$sk-dm-confirm` | `DM_LOG.md`, `SPEC.md` | — |

## `2-spec` — 구현 전 명세 정리·동결

흩어진 요구사항·제약·DM 답변·가정을 SPEC.md 한 곳에 정리하고, 수용 테스트 표를 만든 뒤 구현 착수 여부를 판정한다.

| ID | 프롬프트 | 스킬 | 작업 노트 | 사용 자료 |
| :--- | :--- | :--- | :--- | :--- |
| 2.1 | [명세 통합 (SPEC.md)](2-spec/2.1-spec.md) | `$sk-spec` | `SPEC.md` | — |
| 2.2 | [입출력·데이터 계약 (data_audit.py 사용)](2-spec/2.2-io-contract.md) | `$sk-data-contract` | `SPEC.md` | `sk/snippets/data_audit.py` |
| 2.3 | [수용 기준·테스트 케이스 표](2-spec/2.3-acceptance.md) | `$sk-acceptance` | `SPEC.md` | — |
| 2.4 | [구현 착수 게이트·명세 동결](2-spec/2.4-spec-gate.md) | `$sk-spec-gate` | `SPEC.md` | — |

## `3-plan` — 계획·설계

명세를 작은 수직 슬라이스와 시간 예산으로 나누고, 최소 설계와 결정 근거를 기록한다.

| ID | 프롬프트 | 스킬 | 작업 노트 | 사용 자료 |
| :--- | :--- | :--- | :--- | :--- |
| 3.1 | [슬라이스·시간 예산 계획](3-plan/3.1-plan.md) | `$sk-plan` | `PLAN.md` | — |
| 3.2 | [최소 설계·대안 비교](3-plan/3.2-design.md) | `$sk-design` | `DECISIONS.md` | — |
| 3.3 | [설계 결정·AI 교정 즉시 기록](3-plan/3.3-decision-log.md) | `$sk-decision-log` | `DECISIONS.md` | — |

## `4-build` — 구현

수용 테스트를 먼저 세우고, 슬라이스 하나씩 최소 변경으로 구현한 뒤 관련 엣지 케이스를 방어한다. 4.0 구현 루프는 이 과정과 5단계 검증을 슬라이스 단위 한 바퀴로 묶는다.

| ID | 프롬프트 | 스킬 | 작업 노트 | 사용 자료 |
| :--- | :--- | :--- | :--- | :--- |
| 4.0 | [구현 루프 — 슬라이스 하나를 RED→GREEN→방어→검증까지](4-build/4.0-build-loop.md) | `$sk-build-loop` | `PLAN.md`, `EVIDENCE.md`, `SPEC.md` | `sk/snippets/data_audit.py`, `sk/snippets/smoke_test.py` |
| 4.1 | [실패하는 수용 테스트 먼저 작성](4-build/4.1-test-first.md) | `$sk-test-first` | `SPEC.md`, `EVIDENCE.md` | — |
| 4.2 | [슬라이스 하나 최소 변경 구현](4-build/4.2-implement.md) | `$sk-implement` | `PLAN.md`, `SPEC.md`, `DECISIONS.md` | — |
| 4.3 | [관련 엣지 케이스 방어](4-build/4.3-harden.md) | `$sk-harden` | `SPEC.md`, `EVIDENCE.md` | — |

## `5-verify` — 검증·증거

요구사항별로 독립 근거가 있는 검증을 실행하고 재현 가능한 증거를 남긴다.

| ID | 프롬프트 | 스킬 | 작업 노트 | 사용 자료 |
| :--- | :--- | :--- | :--- | :--- |
| 5.1 | [요구사항 추적 검증](5-verify/5.1-verify.md) | `$sk-verify` | `SPEC.md`, `EVIDENCE.md` | — |
| 5.2 | [실행 증거 기록](5-verify/5.2-evidence.md) | `$sk-evidence` | `EVIDENCE.md` | — |
| 5.3 | [데이터 정합성 독립 검산 (data_audit.py 사용)](5-verify/5.3-data-validation.md) | `$sk-data-validation` | `EVIDENCE.md` | `sk/snippets/data_audit.py` |
| 5.4 | [API 계약 검증 (smoke_test.py 사용)](5-verify/5.4-api-contract.md) | `$sk-api-contract` | `EVIDENCE.md` | `sk/snippets/smoke_test.py` |
| 5.5 | [UI 핵심 흐름 확인 (smoke_test.py 사용)](5-verify/5.5-ui-smoke.md) | `$sk-ui-smoke` | `EVIDENCE.md` | `sk/snippets/smoke_test.py` |

## `6-debug` — 디버깅·복구·시간 관리

실패를 가설로 좁혀 고치고, AI가 헛돌거나 맥락을 잃거나 시간이 부족할 때 안전하게 복구한다.

| ID | 프롬프트 | 스킬 | 작업 노트 | 사용 자료 |
| :--- | :--- | :--- | :--- | :--- |
| 6.1 | [가설 기반 디버깅](6-debug/6.1-debug.md) | `$sk-debug` | `EVIDENCE.md`, `DECISIONS.md` | — |
| 6.2 | [AI 반복 루프 탈출](6-debug/6.2-unstuck.md) | `$sk-unstuck` | `PLAN.md` | — |
| 6.3 | [내 변경만 안전하게 되돌리기](6-debug/6.3-rollback.md) | `$sk-rollback` | `PLAN.md`, `EVIDENCE.md` | — |
| 6.4 | [맥락 복구·작업 재개](6-debug/6.4-resume.md) | `$sk-resume` | `PLAN.md` | — |
| 6.5 | [시간 부족 시 범위 축소](6-debug/6.5-timebox.md) | `$sk-timebox` | `PLAN.md` | — |

## `7-review` — 리뷰·준수 감사

변경을 반증하려는 시각으로 검토하고, 명세·DM 답변·제약이 실제 코드와 증거에 모두 반영됐는지 감사한다.

| ID | 프롬프트 | 스킬 | 작업 노트 | 사용 자료 |
| :--- | :--- | :--- | :--- | :--- |
| 7.1 | [반증 중심 코드 리뷰](7-review/7.1-review.md) | `$sk-review` | `REVIEW.md` | — |
| 7.2 | [명세·DM 반영 준수 감사](7-review/7.2-compliance.md) | `$sk-compliance` | `REVIEW.md` | — |

## `8-submit` — 문서화·제출

증거에 근거한 보고서를 템플릿으로 작성하고, 제출 전 최종 점검과 도구 정리 판단을 한다.

| ID | 프롬프트 | 스킬 | 작업 노트 | 사용 자료 |
| :--- | :--- | :--- | :--- | :--- |
| 8.1 | [보고서 작성 (SUBMISSION 템플릿 사용)](8-submit/8.1-report.md) | `$sk-report` | `SPEC.md`, `DM_LOG.md`, `DECISIONS.md`, `EVIDENCE.md`, `UNDERSTANDING.md` | `sk/templates/SUBMISSION_DOC_TEMPLATE.md` |
| 8.2 | [제출 전 최종 점검·도구 정리](8-submit/8.2-deliver.md) | `$sk-deliver` | `EVIDENCE.md` | — |

## `9-qa` — 후속 서술형 6문항 대비

내가 구현한 것을 실제 코드·결정·증거로 이해하고 Q1~Q6(설계 의도, 동작 원리, 예외 방어, 검증·AI 교정, 업무 맥락, 한계·개선)에 내 말로 답할 수 있게 준비한다. AI 사용이 허용된 단계에서만 사용한다.

| ID | 프롬프트 | 스킬 | 작업 노트 | 사용 자료 |
| :--- | :--- | :--- | :--- | :--- |
| 9.1 | [내 구현 이해 지도](9-qa/9.1-understand.md) | `$sk-understand` | `UNDERSTANDING.md` | — |
| 9.2 | [6문항 암기 카드 (POST_QA 템플릿 사용)](9-qa/9.2-qa-card.md) | `$sk-qa-card` | `QA_CARD.md` | `sk/templates/POST_QA_6_TEMPLATE.md` |
| 9.3 | [설명 연습·꼬리질문 대비](9-qa/9.3-qa-drill.md) | `$sk-qa-drill` | `QA_CARD.md` | — |
| 9.4 | [한계·개선안 정리](9-qa/9.4-retrospect.md) | `$sk-retrospect` | `UNDERSTANDING.md` | — |
