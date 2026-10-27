#!/usr/bin/env bash
# ==============================================================================
# SK Hynix AI Hackathon 2026 - Cofa-Probe One-Command Bootstrap Harness
#
# [1] In Exam Terminal (Cofa-Probe):
#     git clone https://github.com/<YOUR_ID>/ck /tmp/k && bash /tmp/k/init.sh
#
# [2] Local Dry-Run & Verification Test (Before Exam):
#     bash init.sh --verify
# ==============================================================================
set -e

echo "🚀 [1/4] Initializing Official Codex Skill & Config Directories..."
mkdir -p ~/.codex/skills ~/.agents/skills /tmp/ext-skills

echo "📦 [2/4] Writing Global Engineering Discipline (~/.codex/AGENTS.md)..."
cat << 'EOF' > ~/.codex/AGENTS.md
# Global Engineering & Verification Rules (Cofa-Probe Harness)

You are collaborating in a time-boxed (180-min) real-world engineering assessment evaluated on Intent Management, Technical Verification, and Architectural Clarity. Follow these rules strictly on every turn:

## 1. Ground & Grill First (Phase 1 - Do Not Edit Code Yet)
- When asked to analyze or start a task, FIRST scan `README.md` and the repository layout without modifying files.
- Explicitly list:
  1) Required deliverables and exact file paths/names.
  2) Technical constraints (ports, schemas, `0.0.0.0` host binding for web servers, forbidden modifications).
  3) 2-3 high-impact policy or edge-case questions the user should ask the Stakeholder Agent (`업무 담당자`) via DM.
  4) A 3-step verifiable implementation plan.

## 2. Boundary Discipline & Minimal Diff (Phase 2 - Implementation)
- Preserve all existing API contracts, function signatures, and required file structures.
- Validate all external inputs, missing values (Null/Empty/NaN), boundary conditions, and permission rules at system boundaries.
- Whenever starting a web server or preview service, ALWAYS bind the host to `0.0.0.0` (never `localhost` or `127.0.0.1` alone) so the Cofa Browser tool can connect.
- Avoid unnecessary token-burning loops or creating separate git worktrees; do all work cleanly in the current `~/workspace` directory.

## 3. Systematic Debugging & Verification Before Completion (Phase 3 - Testing)
- Never declare a feature or bugfix complete without running actual verification commands.
- Always write and execute automated tests covering both:
  1) Happy Path (standard valid inputs and expected outputs).
  2) Edge & Failure Cases (empty inputs, outliers, malformed types, unauthorized access).
- For data analysis or aggregation tasks, cross-check summary metrics against raw dataset row counts and sums.

## 4. Show Your Work & Post-Q&A Briefing (Phase 4 - Cognitive Clarity)
- After completing each major milestone, provide a concise 3-line summary:
  - **Why (Design Choice)**: Why this approach/structure was chosen over alternatives (trade-offs).
  - **How (Mechanism)**: Exact file/function names and data flow.
  - **Limitations (Failure Mode)**: Which extreme edge cases or scale conditions could cause issues and how to mitigate them.
EOF

echo '🛠️ [3/4] Installing Custom High-Score Skills ($cofa-start, $cofa-verify, $cofa-brief)...'

# Skill 1: cofa-start (Phase 1 Explorer & Stakeholder Question Generator)
mkdir -p ~/.agents/skills/cofa-start
cat << 'EOF' > ~/.agents/skills/cofa-start/SKILL.md
---
name: cofa-start
description: Phase 1 task analyzer. Use when starting a task to scan README.md and repo structure, identify constraints, and draft questions for the stakeholder DM agent before writing code.
---
# Cofa-Start: Phase 1 Grounding & Grill Workflow

Do NOT modify any source files yet. Perform the following read-only grounding steps:
1. Read `README.md` and inspect the directory tree of the current workspace.
2. Output a structured Phase 1 Brief in Korean with four sections:
   - **필수 제출 파일 목록**: Exact filenames, paths, and formats required for submission.
   - **기술 및 인터페이스 제약 조건**: Existing APIs to preserve, port numbers, `0.0.0.0` binding requirements, and data schemas.
   - **업무 담당자(실무자 에이전트) DM 질문 3가지**: 2 to 3 sharp, concise questions in Korean regarding ambiguous business rules, edge-case priorities, or conflict resolution that I can copy-paste into the DM with `업무 담당자`.
   - **단계별 구현 및 검증 계획**: 3 verifiable milestones (MVP -> Edge Cases & Tests -> Submission Docs).
EOF

# Skill 2: cofa-verify (Phase 3 Automated Happy + Edge Case Verifier)
mkdir -p ~/.agents/skills/cofa-verify
cat << 'EOF' > ~/.agents/skills/cofa-verify/SKILL.md
---
name: cofa-verify
description: Phase 3 verification workflow. Use to run happy-path and edge-case tests, check data integrity and git status/diff, and prove the artifact works before completion.
---
# Cofa-Verify: Evidence-Based Verification Workflow

1. Write and run automated tests covering:
   - **Happy Path**: Standard inputs produce exact expected outputs.
   - **Edge & Failure Cases**: Null/empty values, boundary numbers, malformed requests, or invalid states are handled gracefully without crashing.
   - **Data Integrity Check**: Verify output counts/totals match raw source data.
2. If any test fails, trace the root cause, apply a minimal fix, and re-run until 100% green.
3. Run `git status` and `git diff --stat` to verify that no untracked temporary clutter or accidental deletions exist in the workspace.
4. Report the exact test command run and the verification evidence in Korean.
EOF

# Skill 3: cofa-brief (Phase 4 Submission Doc & 6-Question Post-Q&A Cheat Sheet)
mkdir -p ~/.agents/skills/cofa-brief
cat << 'EOF' > ~/.agents/skills/cofa-brief/SKILL.md
---
name: cofa-brief
description: Phase 4 wrap-up workflow. Use before submission to generate required planning/collaboration docs and print a Korean cheat-sheet for the 6 post-submission written questions.
---
# Cofa-Brief: Submission Documentation & Post-Q&A Prep

1. Check `README.md` for any required planning/collaboration/architecture documents and write/update them thoroughly in Korean.
2. Print a **Post-Q&A 6-Question Memorization Card** in the terminal (in Korean, 3 sentences per item) so the user can review it before clicking submit:
   - **Q1 (아키텍처·설계 선택 이유 - Why)**: Why this structure/algorithm was chosen over alternative A, and its trade-offs.
   - **Q2 (핵심 코드·함수 동작 원리 - How)**: Exact file names, function names, and step-by-step pipeline flow.
   - **Q3 (예외 처리 및 경계값 방어 - Edge Cases)**: Which edge cases (null, outlier, auth, schema) were guarded and where.
   - **Q4 (검증 과정 및 AI 오류 수정 - Verification)**: What initial AI mistakes or bugs were caught and how tests proved the fix.
   - **Q5 (업무 맥락 및 제약 반영 - Business Fit)**: How `README.md` and stakeholder DM requirements were prioritized.
   - **Q6 (현재 구현의 한계점과 개선안 - Limitations)**: Under what extreme condition (scale, concurrency, unseen pattern) this implementation could fail, and how to improve it next.
EOF

echo "🌐 [4/4] Fetching Curated Open-Source Skills (mattpocock, superpowers, pstack)..."
if git clone --depth 1 https://github.com/mattpocock/skills.git /tmp/ext-skills/mp 2>/dev/null; then
  cp -r /tmp/ext-skills/mp/skills/engineering/diagnosing-bugs ~/.agents/skills/ 2>/dev/null || true
  cp -r /tmp/ext-skills/mp/skills/engineering/tdd ~/.agents/skills/ 2>/dev/null || true
  cp -r /tmp/ext-skills/mp/skills/productivity/grill-me ~/.agents/skills/ 2>/dev/null || true
  cp -r /tmp/ext-skills/mp/skills/productivity/handoff ~/.agents/skills/ 2>/dev/null || true
  echo "  ✔ Loaded mattpocock/skills (diagnosing-bugs, tdd, grill-me, handoff)"
fi

if git clone --depth 1 https://github.com/obra/superpowers.git /tmp/ext-skills/sp 2>/dev/null; then
  cp -r /tmp/ext-skills/sp/skills/systematic-debugging ~/.agents/skills/ 2>/dev/null || true
  cp -r /tmp/ext-skills/sp/skills/verification-before-completion ~/.agents/skills/ 2>/dev/null || true
  echo "  ✔ Loaded obra/superpowers (systematic-debugging, verification-before-completion)"
fi

if git clone --depth 1 https://github.com/cursor/plugins.git /tmp/ext-skills/cp 2>/dev/null; then
  cp -r /tmp/ext-skills/cp/pstack/skills/how ~/.agents/skills/ 2>/dev/null || true
  cp -r /tmp/ext-skills/cp/pstack/skills/teach ~/.agents/skills/ 2>/dev/null || true
  cp -r /tmp/ext-skills/cp/pstack/skills/show-me-your-work ~/.agents/skills/ 2>/dev/null || true
  echo "  ✔ Loaded cursor/plugins pstack (how, teach, show-me-your-work)"
fi

cp -r ~/.agents/skills/* ~/.codex/skills/ 2>/dev/null || true
rm -rf /tmp/ext-skills

cat << 'EOF' > /tmp/cofa_prompts.txt
====================================================================
📌 [Cofa-Probe 단계별 원클릭 프롬프트 컨닝페이퍼 (cat /tmp/cofa_prompts.txt)]
====================================================================
💡 팁: Codex 입력창에서 `/skills`를 치거나 `$스킬이름`을 입력하면 스킬이 즉시 호출됩니다!

[0단계: Codex 시작 직후 필수 명령어]
/status
/model           (-> Sol 6.1, Terra 5.6, Luna 6, Sol 6.0 중 선택! Astra 금지!)
/skills          (-> 설치된 스킬 목록 확인)

[1단계: 시작 직후 탐색 ($cofa-start)]
$cofa-start 현재 작업 공간의 README.md와 코드 구조를 분석하고, 필수 제출 파일, 기술 제약(0.0.0.0 바인딩 등), 업무 담당자 DM 질문 3가지, 3단계 구현 계획을 정리해 줘.

[2단계: 제약 기반 구현]
방금 정리한 계획과 업무 담당자 답변을 반영해 1단계 기능부터 구현해 줘. 기존 API/스키마 호환성을 유지하고, 경계값 예외 처리를 추가하며, 웹 서버는 반드시 0.0.0.0에 바인딩해 줘.

[3단계: 정상·예외 테스트 검증 ($cofa-verify)]
$cofa-verify 정상 경로(Happy Path)와 예외/경계값 경로(Edge Case) 테스트를 모두 작성·실행하고, 원본 데이터 정합성과 git diff 상태를 검증해 줘.

[4단계: 제출 문서 생성 & 후속 서술형 6문항 암기 카드 출력 ($cofa-brief)]
$cofa-brief 과제에서 요구한 제출 문서(계획서/협업 기록)를 작성해 저장하고, 내가 후속 서술형 6문항에서 직접 보고 외울 수 있도록 Q1~Q6 핵심 답변 요약을 터미널에 출력해 줘.
====================================================================
EOF

echo ""
echo "✅ Cofa-Probe Harness Installed Successfully!"
echo "👉 Installed Skills in ~/.agents/skills/ :"
ls -1 ~/.agents/skills/ | sed 's/^/   - $/'
echo "👉 Anytime you need prompt templates, run: cat /tmp/cofa_prompts.txt"

# Optional verification & mock workspace generator for local testing
if [[ "${1:-}" == "--verify" ]]; then
  echo ""
  echo "🔍 [VERIFY MODE] Creating Mock Cofa-Probe Workspace at /tmp/mock-workspace..."
  mkdir -p /tmp/mock-workspace/src /tmp/mock-workspace/data
  cat << 'MOCK_EOF' > /tmp/mock-workspace/README.md
# [모의 과제] 반도체 패키징 라인 설비 알람 이상 탐지 및 리포트 서비스

## 1. 과제 개요
설비 센서 로그(`data/sensor_logs.csv`)를 읽어 결함 알람을 분류하고, 웹 대시보드 및 요약 API를 제공하는 서비스를 완성하세요.

## 2. 필수 제출물
- `src/server.py` (또는 기존 서버 파일 수정)
- `SUBMISSION_PLAN.md` (문제 정의, 설계 근거, 테스트 결과, 한계점 기술)

## 3. 제약 조건
- 기존 `/api/health` 엔드포인트 응답 스키마를 유지할 것
- 결측치(NaN/Null) 또는 음수 온도값 유입 시 에러로 중단되지 않고 예외 처리할 것
MOCK_EOF
  cat << 'MOCK_EOF' > /tmp/mock-workspace/data/sensor_logs.csv
timestamp,equip_id,temp_c,vibration_hz,status
2026-10-31T09:00:00Z,EQ-101,85.2,12.1,NORMAL
2026-10-31T09:05:00Z,EQ-102,-999.0,45.8,ERROR
2026-10-31T09:10:00Z,EQ-101,,15.0,WARN
MOCK_EOF
  echo "  ✔ Mock workspace ready at: /tmp/mock-workspace"
  echo "  ✔ To test with local Codex CLI:"
  echo "      cd /tmp/mock-workspace && codex"
  echo "      (Inside Codex, type: /skills  or  \$cofa-start)"
fi