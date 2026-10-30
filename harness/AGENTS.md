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
