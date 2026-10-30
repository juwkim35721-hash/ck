# SK Hynix AI Hackathon 2026 - 2nd Round Cofa-Probe Kit & Harness (`juwkim35721/sk`)

본 저장소(`https://github.com/juwkim35721/sk`)는 SK하이닉스 AI 해커톤 2026 2차 예선(Cofa-Probe)의 **[공개 자료 활용] 규정**을 준수하여 사전 설계된 공개 엔지니어링 하네스(`AGENTS.md`), 단계별 스킬(`skills/`), 제출 문서·DM 템플릿(`templates/`), 진단 코드 스니펫(`snippets/`), 그리고 상황별 대응 지침서(`playbooks/`)입니다.

> **규정 준수 안내**: 본 저장소는 공개(Public) 상태이며 2차 예선 결과 통지 시점까지 공개 상태로 유지됩니다. 결과물을 통째로 대체하는 애플리케이션 코드가 아닌, 요구사항 분석·설계·엣지 케이스 방어·자동화 검증을 돕는 범용 엔지니어링 도구 모음입니다.

## 1. 시험장 터미널 원클릭 설치 명령어 (One-Liner)

```bash
# 추천 1: /tmp/sk 에 클론하여 작업 공간(~/workspace)을 깨끗하게 유지
git clone https://github.com/juwkim35721/sk /tmp/sk && bash /tmp/sk/init.sh

# 추천 2: 그냥 현재 폴더에 클론해도 init.sh가 자동으로 /tmp/sk 로 옮기고 정리해 줌!
git clone https://github.com/juwkim35721/sk && bash sk/init.sh
```

## 2. 디렉토리 구조 (Repository Architecture)

```text
.
├── init.sh                              # 원클릭 통합 설치 스크립트 (~/.codex, ~/.agents, /tmp/cofa-kit 자동 구축)
├── README.md                            # 저장소 개요 및 빠른 실행 안내
├── harness/
│   └── AGENTS.md                        # Codex 전역 엔지니어링 규율 (탐색 우선, 0.0.0.0 바인딩, 7대 엣지케이스 방어)
├── skills/                              # Codex CLI 전용 6대 상황별 스킬 ($스킬명으로 호출)
│   ├── cofa-start/SKILL.md              # Step 1: 요구사항 해체, 문제 유형 분류, 실무자 DM 질문 3개 도출
│   ├── cofa-eda/SKILL.md                # Step 1-B: 데이터셋 결측치·이상치·스키마 전수 감사
│   ├── cofa-design/SKILL.md             # Step 2: 아키텍처 대안 비교(Trade-off) 및 핵심 MVP 설계·구현
│   ├── cofa-edge/SKILL.md               # Step 3: 7대 단골 엣지 케이스 추론 및 방어 코드(Guard Clause) 주입
│   ├── cofa-verify/SKILL.md             # Step 4: 정상+예외 자동화 테스트 실행, 원본 대조, git diff 점검
│   └── cofa-brief/SKILL.md              # Step 5: 제출 문서 생성 및 후속 서술형 6문항(Q1~Q6) 3문장 암기 카드 출력
├── templates/                           # 문서 및 커뮤니케이션 템플릿
│   ├── SUBMISSION_DOC_TEMPLATE.md       # 계획·협업·검증 보고서 표준 양식
│   ├── DM_QUESTION_TEMPLATES.txt        # 우측 메신저 '업무 담당자' 질문 양식 3종
│   └── POST_QA_6_TEMPLATE.md            # 후속 서술형 6문항(문항당 5분, 복붙 불가) 대비 3문장 답변 틀
├── snippets/                            # 범용 데이터·API 진단 유틸리티 코드
│   ├── data_audit.py                    # CSV/JSON/JSONL 결측치·음수 이상치·중복 3초 스캐너
│   └── smoke_test.py                    # 로컬 웹 서버(0.0.0.0) HTTP 상태 및 응답 속도 검증기
└── playbooks/
    └── MASTER_GUIDE.md                  # 코덱스 기초 조작법 및 패닉 방지 상황별 마스터 지침서
```
