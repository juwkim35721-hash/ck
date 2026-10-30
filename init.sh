#!/usr/bin/env bash
# ==============================================================================
# SK Hynix AI Hackathon 2026 - Cofa-Probe Master Anti-Panic Arsenal (init.sh)
#
# ⚠️ [10/29 FINAL EMAIL COMPLIANCE RULES]:
# 1. Keep this GitHub repository PUBLIC until the 2nd Round results are announced.
# 2. Recommended Models ONLY: 6.1 Sol, 5.6 Terra, 6.0 Luna (NEVER use Astra!).
# 3. NEVER update Codex CLI version (ignore any update prompts!).
# 4. Wired mouse & wired keyboard ONLY (NO Bluetooth mouse or keyboard!).
#
# [Exam Terminal One-Liner]:
#   git clone https://github.com/juwkim35721/sk /tmp/sk && bash /tmp/sk/init.sh
# ==============================================================================
set -e

# Safety guard: if the user ran `git clone https://github.com/juwkim35721/sk && bash sk/init.sh`
# inside ~/workspace, move ~/workspace/sk to /tmp/sk so ~/workspace stays 100% clean for submission!
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ "$SCRIPT_DIR" == *"/workspace/sk"* ]] && [[ ! -d "/tmp/sk" ]]; then
  cp -r "$SCRIPT_DIR" /tmp/sk
  rm -rf "$SCRIPT_DIR"
  echo "🧹 [Auto-Clean] Moved cloned 'sk' folder from ~/workspace/sk to /tmp/sk to keep submission workspace clean!"
fi

echo "🚀 [1/5] Initializing Official Codex Skill, Template & Snippet Directories..."
mkdir -p ~/.codex/skills ~/.agents/skills /tmp/ext-skills /tmp/cofa-kit/templates /tmp/cofa-kit/snippets /usr/local/bin 2>/dev/null || true

# ------------------------------------------------------------------------------
# LAYER 1: HARNESS (~/.codex/AGENTS.md)
# ------------------------------------------------------------------------------
echo "📦 [2/5] Installing Layer 1: Global Engineering Harness (~/.codex/AGENTS.md)..."
cat << 'EOF' > ~/.codex/AGENTS.md
# Global Engineering & Verification Harness (Cofa-Probe Master Guidelines)

You are collaborating in a 180-minute real-world engineering assessment evaluated on Intent Management, Technical Verification, and Cognitive Clarity. Follow these 6 rules strictly on every turn:

## 1. Ground & Grill First (Requirements Analysis - Do Not Edit Code Yet)
- Before modifying any code, scan `README.md`, existing source files, and sample data.
- Explicitly output:
  1) **필수 제출 파일 및 스펙**: Exact filenames, paths, and required report/document names.
  2) **기술 및 인터페이스 제약 조건**: Existing API endpoints/schemas to preserve, port numbers, and `0.0.0.0` host binding.
  3) **업무 담당자(실무자 에이전트) DM 질문 3가지**: 2-3 sharp Korean questions about ambiguous business rules, outlier/null handling, or priority conflicts.
  4) **단계별 실행 및 검증 계획**: 3 verifiable milestones (MVP -> Edge Cases & Tests -> Submission Docs).

## 2. Architecture & Design Before Coding (Caller-First & Trade-offs)
- Before implementing a module, state the chosen architecture/data structure, 1 alternative you rejected, and the trade-off reason in 2 lines.
- Keep diffs minimal and modular. Never break existing working endpoints or required file structures.

## 3. Systematic Edge-Case Inference & Boundary Guarding (Implementation)
- Guard all system boundaries against the 7 standard failure modes:
  1) Missing values (`Null`, `None`, `NaN`, empty string `""`, empty list/JSON `{}`).
  2) Extreme/corrupted values (negative sensor values like `-999`, `0`, `Infinity`, out-of-range numbers).
  3) Malformed types or schemas (string instead of number, missing required keys).
  4) Timestamp/timezone/sorting anomalies (unsorted logs, invalid dates, tie-breaking rules).
  5) Duplicate records or idempotency issues (duplicate IDs or repeated webhook/API calls).
  6) Auth/permission/state violations (unauthorized access or invalid state transitions).
  7) Web server binding: ALWAYS bind web servers to `0.0.0.0` (never `localhost` or `127.0.0.1` alone) so the Cofa Browser preview connects.

## 4. Evidence Before Completion (Automated Verification & Testing)
- Never declare a task complete without running automated tests and real CLI/HTTP checks.
- Always write and execute tests covering:
  1) **Happy Path**: Standard valid inputs produce exact expected outputs.
  2) **Edge & Failure Cases**: At least 3 boundary/invalid inputs handled gracefully without crashing.
  3) **Data Integrity Cross-Check**: Aggregated counts/sums match raw source data.
- Do all work directly in `~/workspace` (do NOT create separate git worktrees).

## 5. Cognitive Clarity & Post-Q&A Readiness (Every Turn Summary)
- At the end of every major implementation or bugfix turn, print a 3-line Korean summary box:
  - **설계 선택 이유 (Why)**: Why this approach was chosen over alternatives.
  - **핵심 동작 원리 (How)**: Exact file name, function name, and data flow.
  - **한계점 및 보완책 (Limitations)**: Extreme scale/edge conditions where this could fail and how to improve it.

## 6. Strict Platform Safety
- Never run `codex update` or upgrade the Codex CLI binary.
- Never run `git push` to external repositories.
EOF

# ------------------------------------------------------------------------------
# LAYER 2: 6 SITUATIONAL SKILLS (~/.agents/skills/* & ~/.codex/skills/*)
# ------------------------------------------------------------------------------
echo '🛠️ [3/5] Installing Layer 2: 6 Situational Skills ($cofa-start, $cofa-design, $cofa-eda, $cofa-edge, $cofa-verify, $cofa-brief)...'

# Skill 1: $cofa-start (Phase 1 Requirements Analysis & Stakeholder DM Questions)
mkdir -p ~/.agents/skills/cofa-start
cat << 'EOF' > ~/.agents/skills/cofa-start/SKILL.md
---
name: cofa-start
description: Step 1 Requirements Analyzer. Scans README.md, codebase, and data samples without editing files. Outputs required deliverables, constraints, 3 Stakeholder DM questions, and a 3-step plan.
---
# Cofa-Start: Requirements Analysis & Stakeholder Grill Workflow

Do NOT modify any source files yet. Perform these read-only grounding steps:
1. Read `README.md` and inspect the file tree and data samples in `~/workspace`.
2. Classify the problem into one or more scenarios:
   - **Type A**: Data/Log Anomaly Detection & Aggregation Pipeline
   - **Type B**: Backend API Feature / Complex Business Rule Implementation
   - **Type C**: Full-Stack Web Service & Interactive Dashboard (`0.0.0.0` Browser Preview)
   - **Type D**: Bugfix / Legacy Refactoring & Performance Optimization
3. Output a structured Korean report with 4 exact sections:
   - **1) 필수 제출 파일 및 합격 조건 (Deliverables & Done Criteria)**: Exact filenames, paths, API routes, and required documents.
   - **2) 기술 및 인터페이스 제약 조건 (Hard Constraints)**: Existing APIs/schemas to preserve, port numbers, `0.0.0.0` binding.
   - **3) 업무 담당자(실무자 에이전트) DM 질문 3가지**: 3 sharp, copy-pasteable Korean questions regarding ambiguous business rules, null/outlier handling, or tie-breaking priorities.
   - **4) 단계별 구현 및 검증 계획 (3-Step Execution Plan)**: Step 1 (Core MVP), Step 2 (Edge Cases & Boundary Guards), Step 3 (Automated Tests & Submission Docs).
EOF

# Skill 2: $cofa-design (Step 2 Architecture, Interface & Trade-off Designer)
mkdir -p ~/.agents/skills/cofa-design
cat << 'EOF' > ~/.agents/skills/cofa-design/SKILL.md
---
name: cofa-design
description: Step 2 Architecture & Design planner. Defines module interfaces, data flow, and explicit design trade-offs (Why B over A) before writing implementation code.
---
# Cofa-Design: Architecture & Trade-Off Blueprint Workflow

Before writing or modifying implementation code, establish a clear engineering design in Korean:
1. **데이터 및 상태 흐름 (Data & State Flow)**: Input -> Validation Guard -> Core Domain Logic -> Output Schema.
2. **모듈 및 함수 인터페이스 (Interfaces)**: Exact files and function signatures to create or modify, ensuring zero breaking changes to existing callers.
3. **핵심 설계 판단과 트레이드오프 (Why & Trade-offs)**:
   - Compare **대안 A (Alternative)** vs. **채택안 B (Chosen Design)** across complexity, reliability, and maintainability.
   - State clearly why B is superior under the 180-minute constraint (this directly feeds the submission document and Post-Q&A Q1).
4. Proceed to implement Step 1 (Core MVP) cleanly after presenting this design.
EOF

# Skill 3: $cofa-eda (Data & Log Anomaly Auditor)
mkdir -p ~/.agents/skills/cofa-eda
cat << 'EOF' > ~/.agents/skills/cofa-eda/SKILL.md
---
name: cofa-eda
description: Data and log auditing skill. Runs /tmp/cofa-kit/snippets/data_audit.py against CSV/JSON/JSONL/SQLite/log files to uncover missing values, negative outliers, duplicates, and schema traps.
---
# Cofa-EDA: Rapid Data & Anomaly Audit Workflow

1. Run `python3 /tmp/cofa-kit/snippets/data_audit.py` on all dataset files in `~/workspace` (and inspect sample lines).
2. Summarize findings in Korean:
   - Exact row/column counts, data types, and timestamp ranges.
   - Missing value (`Null`/`NaN`/empty) counts per field.
   - Corrupted or extreme outliers (e.g., `-999`, negative numbers, spikes, malformed dates, duplicate IDs).
   - Concrete preprocessing and filtering rules to apply in code (and any edge case to confirm with `업무 담당자`).
EOF

# Skill 4: $cofa-edge (Edge-Case Inference & Defensive Coding Hardener)
mkdir -p ~/.agents/skills/cofa-edge
cat << 'EOF' > ~/.agents/skills/cofa-edge/SKILL.md
---
name: cofa-edge
description: Edge-case inference and defensive hardening skill. Audits current implementation against 7 classic failure modes (nulls, outliers, boundary values, duplicates, sorting ties, malformed requests, 0.0.0.0 binding) and patches vulnerabilities.
---
# Cofa-Edge: Systematic Edge-Case Inference & Guard Hardening

Audit the current codebase and requirements against these 7 edge-case categories, list every vulnerability found, and add defensive guards:
1. **결측치 및 빈 입력 (Null/Empty)**: `None`, `NaN`, `""`, `[]`, `{}` passed to functions or API endpoints.
2. **경계값 및 극단적 이상치 (Boundary & Outliers)**: `0`, negative numbers (`-1`, `-999`), division by zero, max/min threshold boundaries (`>` vs `>=`).
3. **데이터 타입 및 스키마 불일치 (Malformed Schema)**: Numeric strings (`"123"`), corrupted JSON lines, missing required fields.
4. **중복 데이터 및 멱등성 (Duplicates & Idempotency)**: Duplicate primary keys/timestamps or repeated requests producing double counts.
5. **정렬 및 동점자 처리 (Sorting & Tie-Breaking)**: Deterministic ordering when values or timestamps are identical.
6. **권한 및 상태 전이 오류 (Auth & State Violations)**: Invalid state transitions or unauthorized requests returning proper 4xx codes instead of 500 crashes.
7. **웹 서버 호스트 및 CORS (`0.0.0.0` Binding)**: Ensure web servers bind to `0.0.0.0` and handle UI preview requests cleanly.
EOF

# Skill 5: $cofa-verify (Automated Testing & Git Cleanliness Verifier)
mkdir -p ~/.agents/skills/cofa-verify
cat << 'EOF' > ~/.agents/skills/cofa-verify/SKILL.md
---
name: cofa-verify
description: Step 4 Verification workflow. Writes and executes automated unit/integration tests for Happy Path + Edge Cases, cross-checks data totals, and verifies git status/diff cleanliness.
---
# Cofa-Verify: Evidence-Based Verification & Test Suite Workflow

1. Write and execute automated tests (`pytest`, `unittest`, `node --test`, or `/tmp/cofa-kit/snippets/smoke_test.py`) covering:
   - **Happy Path**: Standard inputs produce exact expected outputs and schemas.
   - **Edge & Failure Cases**: Every edge case guarded in `$cofa-edge` (nulls, outliers, malformed inputs, boundary conditions) is tested with assertions.
   - **Data Integrity Check**: Output row counts and sums match raw source data.
2. If any test fails, use systematic root-cause debugging (reproduce -> hypothesize -> minimal fix -> re-test) until 100% green.
3. Run `git status` and `git diff --stat` to verify that no untracked temporary clutter or accidental deletions exist in `~/workspace`.
4. Report the exact test commands executed and pass/fail counts in Korean.
EOF

# Skill 6: $cofa-brief (Submission Document Generator & Post-Q&A 6-Question Cheat Sheet)
mkdir -p ~/.agents/skills/cofa-brief
cat << 'EOF' > ~/.agents/skills/cofa-brief/SKILL.md
---
name: cofa-brief
description: Final wrap-up workflow (run 20 mins before submission). Generates required submission documents using SUBMISSION_DOC_TEMPLATE.md and prints the 6-question Post-Q&A memorization card in the terminal.
---
# Cofa-Brief: Submission Documentation & Post-Q&A 6-Question Prep

1. Check `README.md` for required planning, architecture, or collaboration documents. Using `/tmp/cofa-kit/templates/SUBMISSION_DOC_TEMPLATE.md`, write a thorough, well-structured Korean document in `~/workspace` with the exact required filename.
2. Print a **Post-Q&A 6-Question Memorization Card** in the terminal (in Korean, 3 concise sentences per question) based on the actual code and tests you built, following `/tmp/cofa-kit/templates/POST_QA_6_TEMPLATE.md`:
   - **Q1 (아키텍처·설계 선택 이유 - Why)**
   - **Q2 (핵심 코드·함수 동작 원리 - How)**
   - **Q3 (예외 처리 및 경계값 방어 - Edge Cases)**
   - **Q4 (검증 과정 및 AI 오류 수정 - Verification)**
   - **Q5 (업무 맥락 및 실무자 요구사항 반영 - Business Fit)**
   - **Q6 (현재 구현의 한계점과 개선안 - Limitations)**
EOF

# Fetch curated open-source skills if network permits
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

# ------------------------------------------------------------------------------
# LAYER 3: TEMPLATES (/tmp/cofa-kit/templates/*)
# ------------------------------------------------------------------------------
echo "📄 [4/5] Installing Layer 3: Reusable Document & DM Templates (/tmp/cofa-kit/templates/)..."

cat << 'EOF' > /tmp/cofa-kit/templates/SUBMISSION_DOC_TEMPLATE.md
# 과제 수행 계획 및 기술 의사결정·검증 보고서

## 1. 문제 정의 및 요구사항 분석 (Requirements & Constraints)
- **핵심 해결 목표**: [과제가 해결하고자 하는 핵심 비즈니스/기술 문제 요약]
- **필수 제약 및 인터페이스 준수 기준**: [기존 API 스펙 유지, 출력 스키마, `0.0.0.0` 바인딩, 응답 정합성 기준]
- **실무자(업무 담당자) DM 확인 및 반영 사항**:
  - 문의 1: [모호했던 예외/정책 질문] → 반영 결과: [확인된 기준으로 로직 구현]

## 2. 아키텍처 및 핵심 설계 판단 (Architecture & Trade-offs)
| 의사결정 항목 | 채택한 방식 (Chosen) | 비교 대안 (Alternative) | 채택 이유 및 트레이드오프 (Rationale) |
| :--- | :--- | :--- | :--- |
| 데이터/상태 처리 구조 | [예: 입력 경계 검증 + 모듈형 파이프라인] | [예: 단일 함수 일괄 처리] | [결측치/이상치 격리 및 단위 테스트 용이성 확보] |
| 예외 및 경계값 방어 | [예: 입구 Guard Clause + 명시적 에러 분류] | [예: 런타임 예외 무시] | [비정상 데이터 하위 전파 차단 및 디버깅 투명성 확보] |

## 3. 핵심 구현 메커니즘 (Implementation Details)
- **`[주요 파일/모듈 1]` (`[핵심 함수명]`)**: [입력 검증 → 도메인 규칙 적용 → 결과 반환 흐름]
- **`[주요 파일/모듈 2]` (`[핵심 함수명]`)**: [예외 처리, 상태 갱신, API/UI 연동 흐름]

## 4. 엣지 케이스 추론 및 테스트 검증 결과 (Edge Cases & Verification)
- **정상 경로(Happy Path) 검증**: [표준 입력에 대한 기대 출력 및 원본 데이터 행 수·합계 교차 검증 일치 확인]
- **7대 엣지 케이스 방어 및 테스트 결과**:
  1) 결측치(`Null`/`NaN`/빈 값): [에러 중단 없이 안전 처리 확인]
  2) 극단적 이상치(음수/센서 오류값/경계값): [필터링 또는 별도 상태 분류 확인]
  3) 잘못된 스키마/타입 및 중복 레코드: [방어 로직 및 멱등성 확인]
- **AI 협업 및 오류 수정 내역**: [Codex 초기 생성 코드에서 발견한 엣지 케이스 누락/스키마 불일치를 발견하고 수정 지시한 과정]

## 5. 현재 구현의 한계점 및 향후 고도화 방향 (Limitations & Next Steps)
- **잠재적 실패 조건 (Failure Mode)**: [예: 단일 프로세스 인메모리 처리 구조로 인해 대규모 동시 스트림 유입 시 메모리 병목 가능성 / 사전에 정의되지 않은 신규 이상 패턴 유입 시 분류 한계]
- **실무 확장 개선안**: [예: 비동기 큐 및 배치 파이프라인 분리, 동적 임계치 설정 테이블 및 모니터링 알림 도입]
EOF

cat << 'EOF' > /tmp/cofa-kit/templates/DM_QUESTION_TEMPLATES.txt
====================================================================
💬 [우측 메신저 '업무 담당자(실무자 에이전트)' DM 질문 템플릿]
====================================================================
[질문 1: 결측치·이상치 처리 기준 확인]
안녕하세요, 데이터/입력 처리 기준을 명확히 하고자 문의드립니다.
원본 데이터에 결측치(Null/빈 값)나 비정상 극단값(음수 또는 센서 오류값)이 포함된 경우, 해당 레코드를 집계에서 제외해야 하나요, 아니면 별도 오류 상태(ERROR/UNKNOWN)로 분류해 포함해야 하나요?

[질문 2: 비즈니스 규칙 충돌 시 우선순위 확인]
안녕하세요, 요구사항 구현 중 두 조건이 동시에 발생하는 경계 케이스에 대해 문의드립니다.
[조건 A]와 [조건 B]가 동시에 만족될 때 어느 기준을 우선 적용해야 실무 정책에 부합하나요?

[질문 3: 출력 정렬 기준 및 동점 처리 확인]
안녕하세요, 결과물 스키마 및 정렬 기준 관련하여 문의드립니다.
동일 수치(동점) 또는 동일 타임스탬프 발생 시 2차 정렬 우선순위(예: ID 오름차순 등) 기준이 따로 있는지 확인 부탁드립니다.
====================================================================
EOF

cat << 'EOF' > /tmp/cofa-kit/templates/POST_QA_6_TEMPLATE.md
# [후속 서술형 6문항 (문항당 5분 · AI/복붙 금지) 직전 암기 카드]

- **Q1. 설계 의도 (Why)**: `[요구사항/제약]`을 안정적으로 충족하기 위해 `[대안 A]` 대신 에러 격리와 유지보수가 명확한 `[현재 구조 B]`를 선택했습니다. 이를 통해 기존 인터페이스 변경 없이 안정성을 확보했습니다.
- **Q2. 동작 원리 (How)**: `[파일명]`의 `[함수명]`에서 입력을 받아 1차로 경계값 검증을 수행하고, 2차로 `[핵심 도메인 로직]`을 거쳐 최종 결과를 반환하도록 파이프라인을 구성했습니다.
- **Q3. 예외 방어 (Edge Cases)**: 빈 입력(`Null`), 범위를 벗어난 이상치, 잘못된 타입 입력을 핵심 예외로 정의하고, 입구 단계에서 방어 로직(`guard clause`)으로 처리해 런타임 크래시를 방지했습니다.
- **Q4. 검증 및 AI 교정 (Verification)**: Codex의 초기 코드에서 `[특정 예외 누락]`을 발견해 수정 지시했으며, 정상 경로와 실패 경로 단위 테스트 및 원본 데이터 대조를 통해 정합성을 검증했습니다.
- **Q5. 업무 맥락 반영 (Business Fit)**: `README.md`와 업무 담당자 DM으로 확인한 `[핵심 정책]`을 최우선 기준으로 삼아 예외 상황에서도 일관된 결과가 나오도록 반영했습니다.
- **Q6. 한계점 및 개선안 (Limitations)**: 제한 시간 내 핵심 동작 보장을 위해 `[단일 프로세스/인메모리]`로 구현하여 대규모 트래픽 유입 시 병목이 발생할 수 있으며, 실무 적용 시 `[비동기 큐/캐싱/스키마 검증기]`로 확장할 수 있습니다.
EOF

# ------------------------------------------------------------------------------
# LAYER 4: CODE SNIPPETS & ANTI-PANIC CLI HELPER (/tmp/cofa-kit/snippets/*)
# ------------------------------------------------------------------------------
echo "🧪 [5/5] Installing Layer 4: Diagnostic Snippets & Anti-Panic Helper (/tmp/cofa-kit/help.sh)..."

cat << 'EOF' > /tmp/cofa-kit/snippets/data_audit.py
#!/usr/bin/env python3
"""
Universal Data Auditor for Cofa-Probe (CSV / JSON / JSONL)
Usage: python3 /tmp/cofa-kit/snippets/data_audit.py <path_to_data_file>
"""
import csv
import json
import math
import os
import sys
from collections import Counter

def audit_rows(rows, label):
    print(f"=== 📊 DATA AUDIT REPORT: {label} ===")
    print(f"Total Rows: {len(rows)}")
    if not rows:
        return
    cols = list(rows[0].keys())
    print(f"Columns ({len(cols)}): {cols}\n")
    for c in cols:
        vals = [r.get(c) for r in rows]
        nulls = sum(1 for v in vals if v is None or str(v).strip() in ("", "null", "None", "NaN", "nan", "N/A"))
        num_vals = []
        for v in vals:
            if v is not None and str(v).strip() not in ("", "null", "None", "NaN", "nan", "N/A"):
                try:
                    fv = float(v)
                    if not math.isnan(fv) and not math.isinf(fv):
                        num_vals.append(fv)
                except ValueError:
                    pass
        if len(num_vals) > len(rows) * 0.5 and num_vals:
            num_vals.sort()
            p50 = num_vals[len(num_vals) // 2]
            negs = sum(1 for x in num_vals if x < 0)
            zeros = sum(1 for x in num_vals if x == 0)
            print(f"  - [{c}] (Numeric): nulls={nulls}, min={num_vals[0]}, median={p50}, max={num_vals[-1]}, negatives={negs}, zeros={zeros}")
        else:
            non_null = [str(v).strip() for v in vals if v is not None and str(v).strip() != ""]
            top = Counter(non_null).most_common(5)
            dups = len(non_null) - len(set(non_null))
            print(f"  - [{c}] (Categorical/Text): nulls={nulls}, unique={len(set(non_null))}, duplicates={dups}, top5={top}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 data_audit.py <file.csv|file.json|file.jsonl>")
        sys.exit(1)
    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"File not found: {path}")
        sys.exit(1)
    if path.endswith(".csv"):
        with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
            reader = csv.DictReader(f)
            audit_rows(list(reader), path)
    elif path.endswith(".jsonl"):
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            rows = [json.loads(line) for line in f if line.strip()]
            audit_rows(rows, path)
    elif path.endswith(".json"):
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            data = json.load(f)
            if isinstance(data, list):
                audit_rows(data, path)
            elif isinstance(data, dict):
                print(f"JSON Dict Keys: {list(data.keys())}")
                for k, v in data.items():
                    if isinstance(v, list) and v and isinstance(v[0], dict):
                        audit_rows(v, f"{path}[{k}]")

if __name__ == "__main__":
    main()
EOF
chmod +x /tmp/cofa-kit/snippets/data_audit.py

cat << 'EOF' > /tmp/cofa-kit/snippets/smoke_test.py
#!/usr/bin/env python3
"""
Universal HTTP Endpoint & Edge-Case Smoke Tester for Cofa-Probe
Usage: python3 /tmp/cofa-kit/snippets/smoke_test.py http://127.0.0.1:3000/api/health
"""
import sys
import time
import urllib.request
import urllib.error
import json

def test_endpoint(url, method="GET", payload=None, expect_status=None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Content-Type": "application/json"} if payload is not None else {}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = resp.getcode()
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        status = e.code
        body = e.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  ❌ [{method} {url}] Connection Failed: {e}")
        return False
    dt = (time.time() - t0) * 1000
    ok = (expect_status is None and 200 <= status < 300) or (status == expect_status)
    mark = "✅" if ok else "⚠️"
    print(f"  {mark} [{method} {url}] -> HTTP {status} ({dt:.1f}ms) | Body: {body[:120]}")
    return ok

if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:3000/"
    print(f"=== 🔍 SMOKE TESTING: {base_url} ===")
    test_endpoint(base_url, "GET")
EOF
chmod +x /tmp/cofa-kit/snippets/smoke_test.py

# Master Anti-Panic Cheat Sheet (/tmp/cofa_prompts.txt & /tmp/cofa-kit/help.sh)
cat << 'EOF' > /tmp/cofa_prompts.txt
================================================================================
🚨 [패닉 방지 마스터 치트시트] 언제든 터미널에: bash /tmp/cofa-kit/help.sh
================================================================================
[0단계: 시작 직후 (00~05분) - 절대 잊지 말 것!]
1. 터미널에 `codex` 입력해 실행 (절대 버전 업데이트 금지!)
2. Codex 창에서 즉시 입력:
   /model     --> 반드시 `6.1 Sol`, `5.6 Terra`, `6.0 Luna` 중 선택! (Astra 금지!)
   /status    --> 모델 및 AGENTS.md 로드 확인
   /skills    --> 설치된 스킬($cofa-start 등) 확인

--------------------------------------------------------------------------------
[1단계: 요구사항 분석 & 실무자 DM 질문 뽑기 (05~20분)] -> 복붙 프롬프트:
$cofa-start 현재 작업 공간의 @README.md 와 전체 파일/데이터 구조를 스캔해서 (1) 필수 제출 파일명과 합격 기준, (2) 기술/인터페이스 제약(0.0.0.0 바인딩 등), (3) 우측 DM 업무 담당자에게 물어볼 정책/예외 질문 3가지, (4) 3단계 구현 계획을 정리해 줘. 아직 코드는 수정하지 마.

*(👉 만약 데이터/로그 파일이 있다면 이어서 바로 입력)*:
$cofa-eda /tmp/cofa-kit/snippets/data_audit.py 를 실행해서 모든 데이터 파일의 행 수, 결측치(Null/NaN), 음수/극단값 이상치, 중복 여부를 전수 조사하고 전처리 기준을 알려줘.

--------------------------------------------------------------------------------
[2단계: 설계 & 대안 비교 후 MVP 구현 (20~90분)] -> 복붙 프롬프트:
$cofa-design @README.md 요구사항과 업무 담당자 답변([답변내용])을 반영해서 1단계 핵심 기능(MVP)을 구현해 줘. 구현 전에 왜 다른 대안 대신 이 구조를 택했는지(Trade-off) 2줄로 먼저 밝히고, 기존 API/스키마를 유지하며 웹 서버는 반드시 0.0.0.0에 바인딩해 줘.

--------------------------------------------------------------------------------
[3단계: 7대 엣지 케이스 추론 & 방어 로직 강화 (90~125분)] -> 복붙 프롬프트:
$cofa-edge 지금까지 구현한 코드에서 (1) 결측치/빈 입력(Null/Empty), (2) 음수/극단값/0 나누기, (3) 잘못된 타입/스키마, (4) 중복 입력, (5) 동점자 정렬 순서, (6) 권한/상태 오류, (7) 0.0.0.0 바인딩 등 7대 엣지 케이스 취약점을 모두 찾아 방어 로직(Guard Clause)을 추가해 줘.

--------------------------------------------------------------------------------
[4단계: 정상+예외 자동화 테스트 & Git 검증 (125~150분)] -> 복붙 프롬프트:
$cofa-verify 정상 경로(Happy Path)와 방금 방어한 모든 엣지 케이스(Edge/Failure Case)를 검증하는 자동화 테스트 코드를 작성해 실행해 줘. 집계 수치가 원본 데이터와 일치하는지 교차 검증하고, git status와 git diff로 불필요한 임시 파일이 없는지 확인해 줘.

--------------------------------------------------------------------------------
[5단계: 제출 문서 자동 생성 & 후속 서술형 6문항 암기 (150~165분)] -> 복붙 프롬프트:
$cofa-brief /tmp/cofa-kit/templates/SUBMISSION_DOC_TEMPLATE.md 양식을 참고해 과제에서 요구한 제출 문서를 충실히 작성·저장해 줘. 그리고 내가 제출 직후 AI/복붙 없이 후속 서술형 6문항(문항당 5분)을 직접 타이핑할 수 있도록 Q1(설계이유)~Q6(한계점) 핵심 답변 요약 카드를 터미널에 출력해 줘.
================================================================================
EOF

cat << 'EOF' > /tmp/cofa-kit/help.sh
#!/usr/bin/env bash
case "${1:-all}" in
  dm)   cat /tmp/cofa-kit/templates/DM_QUESTION_TEMPLATES.txt ;;
  doc)  cat /tmp/cofa-kit/templates/SUBMISSION_DOC_TEMPLATE.md ;;
  qa)   cat /tmp/cofa-kit/templates/POST_QA_6_TEMPLATE.md ;;
  *)    cat /tmp/cofa_prompts.txt ;;
esac
EOF
chmod +x /tmp/cofa-kit/help.sh

echo ""
echo "✅ Cofa-Probe Master Anti-Panic Arsenal Installed!"
echo "   - Full Cheat Sheet : cat /tmp/cofa_prompts.txt  (or: bash /tmp/cofa-kit/help.sh)"
echo "   - DM Templates     : bash /tmp/cofa-kit/help.sh dm"
echo "   - Post-Q&A 6 Card  : bash /tmp/cofa-kit/help.sh qa"

if [[ "${1:-}" == "--verify" ]]; then
  echo ""
  echo "🔍 [VERIFY MODE] Testing data_audit.py and help.sh..."
  mkdir -p /tmp/mock-workspace/data
  cat << 'MOCK_EOF' > /tmp/mock-workspace/data/sensor_logs.csv
timestamp,equip_id,temp_c,vibration_hz,status
2026-10-31T09:00:00Z,EQ-101,85.2,12.1,NORMAL
2026-10-31T09:05:00Z,EQ-102,-999.0,45.8,ERROR
2026-10-31T09:10:00Z,EQ-101,,15.0,WARN
MOCK_EOF
  python3 /tmp/cofa-kit/snippets/data_audit.py /tmp/mock-workspace/data/sensor_logs.csv
fi