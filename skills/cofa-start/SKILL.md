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
