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
