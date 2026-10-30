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
