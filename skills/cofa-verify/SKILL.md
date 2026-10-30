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
