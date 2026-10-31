# SK하이닉스 AI 해커톤 Cofa-Probe 실전 시간표 & 실행 체크리스트

> **기준 문서**: [`juwkim35721/sk` MASTER_GUIDE.md](https://github.com/juwkim35721/sk/blob/main/playbooks/MASTER_GUIDE.md) · [3_사전_체험_및_응시환경_상세_가이드.pdf](https://drive.google.com/file/d/1km2fH7RFPTp33K9gHaKquhyGZBK3ALgb/view?usp=drivesdk) · [1_시험_필수확인사항_브리프.pdf](https://drive.google.com/file/d/1qLv_xlCKo1CEEU43QtIIf0kbBfnG1hOD/view?usp=drivesdk) · [2_Proctor_설치_및_촬영가이드.pdf](https://drive.google.com/file/d/1dpA2GJAtWp9n073OiutjUZ-kr5iGFmiA/view?usp=drivesdk)

## 1. 한눈에 보는 전체 타임플로우 (10:00 ~ 14:00)

| 시간 구간 | 소요 시간 | 단계 | 핵심 실행 명령 (터미널 2 조회 → 터미널 1 Codex 입력) | 완료 기준 및 산출물 |
| :--- | :--- | :--- | :--- | :--- |
| **09:40 ~ 10:00** | 20분 | **접속·감독 대기** | 개인 링크 접속 → 규정 동의 → 웹캠·전체화면 공유·Cofa Proctor 연결 | 3개 감독 장치 연결 완료 대기 |
| **10:00 ~ 10:02** | 2분 | **녹화 직후 본인확인** | **'과제 시작'** 클릭 → 휴대폰 거치 → Proctor 카메라에 신분증·안경 제시 | 손·키보드·얼굴·모니터 구도 고정 |
| **10:02 ~ 10:05** | 3분 | **레포 클론·초기 기동** | `git clone https://github.com/juwkim35721/sk sk && python3 sk/scripts/install.py && codex` | `/model` (Sol 6.1), `/skills` 확인 |
| **10:05 ~ 10:12** | 7분 | **0. 착수·코드 파악** | `help.py 0.1 -p` → `0.2 -p` → `0.3 -p` | `sk/work/BRIEF.md` 생성 |
| **10:12 ~ 10:22** | 10분 | **1. 발굴·첫 DM 발송** | `help.py 1.0 -p` (라운드 0 스캔 및 질문 생성) | 우측 메신저 담당자에게 첫 DM(M01) 전송 |
| **10:22 ~ 10:40** | 18분 | **1~2. 답변 반영·명세 동결** | `help.py 1.0 -p 2` (답변 반영) → `1.0 -p 4` (마감) → `2.1 -p` → `2.3 -p` → `2.4 -p` | `sk/work/SPEC.md` 상태 `READY` |
| **10:40 ~ 10:50** | 10분 | **3. 구현 계획·설계** | `help.py 3.1 -p` → `3.2 -p` | `sk/work/PLAN.md`, `DECISIONS.md` |
| **10:50 ~ 12:00** | 70분 | **4~5. 슬라이스 구현·검증** | Codex에 `$sk-build-loop` (또는 `help.py 4.0 -p`) / 검증 `4.0 -p 3`, `5.3~5.5 -p` | P0 슬라이스 전체 PASS (`EVIDENCE.md`) |
| **12:00 ~ 12:15** | 15분 | **7. 리뷰·규정 감사** | `help.py 7.1 -p` → `7.2 -p` | `sk/work/REVIEW.md` (결함 수정 완료) |
| **12:15 ~ 12:35** | 20분 | **8~9. 보고서·6문항 카드** | `help.py 9.1 -p` → `9.4 -p` → `8.1 -p` → `9.2 -p` | `UNDERSTANDING.md`, `QA_CARD.md`, 보고서 |
| **12:35 ~ 12:45** | 10분 | **8.2 최종 납품 점검** | `help.py 8.2 -p` (필요 시 숙지 후 `install.py --uninstall`) | 필수 제출 파일 저장(`저장됨`)·GO 판정 |
| **12:45 ~ 12:50** | 5분 | **암기 리허설·과제 제출** | `help.py 9.3 -p` → 상단 **'제출하고 문제풀기'** → **'제출물 확정하고 문제풀기'** | 제출물 고정 완료 (이후 AI·복붙 금지) |
| **12:50 ~ 13:30** | 약 35분 | **후속 서술형 6문항** | 질문 준비 대기(최대 10분) → **'문제 풀기'** 클릭 → 6문항 직접 타이핑(문항당 5분) | **'답안 제출하고 마치기'** 및 제출 ID 확인 |

## 2. 시간대별 상세 행동 지침 및 명령어

### [10:00 ~ 10:02] 과제 시작 직후 감독 절차 (터미널 조작 전 필수)
- [ ] **'과제 시작'** 버튼을 누르면 그 순간부터 녹화가 자동 시작됩니다.
- [ ] **휴대폰 세로 거치**: 의자에 앉아 한쪽 팔을 옆으로 펼쳐 손끝이 닿는 위치에 거치하고 충전선을 연결합니다. 전면 카메라에 **손·키보드, 얼굴, 모니터 화면**이 모두 들어오는지 확인합니다.
- [ ] **실물 신분증 제시 (Proctor 휴대폰 카메라)**:
  - 주민등록증: 주민번호 뒤 7자리와 주소를 가리고 **사진·이름·생년월일(앞 6자리)**이 보이게 얼굴 옆에 나란히 들어 보여줍니다.
  - 운전면허증: 주민번호 뒤 7자리, 면허번호, 주소, 암호일련번호를 가립니다.
  - 여권: 여권번호 전체, 하단 MRZ 두 줄(주민번호 기재 시 뒤 7자리 포함)을 가립니다.
- [ ] **안경 확인 (착용자만)**: 안경을 벗어 Proctor 카메라에 앞면·렌즈 → 양쪽 안경다리 바깥쪽·안쪽을 차례로 천천히 보여준 뒤 다시 착용합니다.

### [10:02 ~ 10:05] 레포 클론 및 Codex 초기 기동
모든 작업은 반드시 **과제 루트 디렉터리(시험이 제공한 기본 폴더)**에서 실행합니다.

1. **터미널 1 (Codex 전용 탭)**에서 아래 명령을 차례로 실행합니다:
   ```bash
   pwd && ls -la
   git clone https://github.com/juwkim35721/sk sk
   python3 sk/scripts/install.py
   codex
   ```
   - 폴더 신뢰(Folder Trust) 확인 시 **Yes** 선택
   - Codex 업데이트 안내가 뜨면 반드시 **No / Skip** 선택
2. **터미널 1의 Codex 입력창**에서 상태를 점검합니다:
   ```text
   /status
   /model
   /skills
   ```
   - `/model`에서 **6.1 Sol** (1순위) 또는 **5.6 Terra / 6.0 Luna** 선택 (**Astra 사용 절대 금지**)
   - `/skills`에서 `sk-*` 스킬 37개 로드 확인
3. **터미널 2 (프롬프트 조회·테스트·서버 실행용 보조 탭)**를 `+` 버튼으로 새로 열고 실행합니다:
   ```bash
   python3 sk/scripts/help.py flow
   ```
   - 터미널 복사: 텍스트 선택 후 `Ctrl+C` (Mac `Cmd+C`)
   - 터미널 붙여넣기: `Ctrl+Shift+V` (Mac `Cmd+V`)

### [10:05 ~ 10:12] 0단계: 착수 (환경·유형·코드 지도 파악)
터미널 2에서 아래 명령을 하나씩 쳐서 나온 프롬프트를 터미널 1(Codex)에 붙여넣습니다.

```bash
python3 sk/scripts/help.py 0.1 -p
python3 sk/scripts/help.py 0.2 -p
python3 sk/scripts/help.py 0.3 -p
```
- [ ] CSV/JSON/JSONL 데이터 파일이 있는 과제라면 터미널 2에서 즉시 구조를 감사합니다:
  ```bash
  python3 sk/snippets/data_audit.py <데이터파일_경로>
  ```
- [ ] `sk/work/BRIEF.md`에 실행·테스트 명령, 과제 유형(A~D), 코드 지도가 정리되었는지 확인합니다.

### [10:12 ~ 10:22] 1단계: 요구사항 발굴 & 첫 담당자 DM 발송
```bash
python3 sk/scripts/help.py 1.0 -p
```
- [ ] Codex가 스캔 커버리지와 함께 요구사항(`R#`), 제약(`C#`), 모호성(`G#`) 및 **복붙용 DM 질문 초안(`M01`)**을 생성합니다.
- [ ] 우측 메신저에서 **업무 담당자(시나리오 에이전트)**를 선택해 질문을 붙여넣고 전송(`Enter`, 줄바꿈은 `Shift+Enter`)합니다.
- [ ] 10:22 이전에 첫 DM 발송을 완료합니다.

### [10:22 ~ 10:40] 1~2단계: DM 답변 반영 및 명세(`SPEC.md`) 동결
1. **담당자 답변이 도착하면** 터미널 2에서 블록 2 프롬프트를 꺼내 답변과 함께 Codex에 넣습니다:
   ```bash
   python3 sk/scripts/help.py 1.0 -p 2
   ```
2. **질의를 마감할 때** 블록 4 프롬프트로 남은 모호성을 합리적 가정으로 전환합니다:
   ```bash
   python3 sk/scripts/help.py 1.0 -p 4
   ```
3. **구현 전 명세 및 수용 기준을 동결**합니다:
   ```bash
   python3 sk/scripts/help.py 2.1 -p
   python3 sk/scripts/help.py 2.3 -p
   python3 sk/scripts/help.py 2.4 -p
   ```
- [ ] `sk/work/SPEC.md` 상태가 `READY` 또는 `READY-WITH-ASSUMPTIONS`인지 확인합니다.

### [10:40 ~ 10:50] 3단계: 슬라이스 계획 및 설계 결정 기록
```bash
python3 sk/scripts/help.py 3.1 -p
python3 sk/scripts/help.py 3.2 -p
```
- [ ] 구현 단위가 검증 가능한 작은 슬라이스(`S1`, `S2`, `S3`...)로 쪼개져 `sk/work/PLAN.md`에 기록되었는지 확인합니다.
- [ ] 핵심 아키텍처·트레이드오프 결정이 `sk/work/DECISIONS.md`에 남았는지 확인합니다.

### [10:50 ~ 12:00] 4~5단계: 슬라이스 구현 루프 & 실행 증거 확보
1. **구현 루프 시작** (Codex 입력창에 직접 호출하거나 프롬프트 복붙):
   ```text
   $sk-build-loop
   ```
   *(또는 터미널 2에서 `python3 sk/scripts/help.py 4.0 -p` 조회)*
2. **슬라이스별 진행**: `S1 진행`, `S2 진행` 순서로 **테스트 작성(RED) → 구현(GREEN) → 방어적 예외 처리 → 검증 및 증거(`E#`) 기록**을 반복합니다.
3. **코드 변경 없이 검증만 확인할 때**:
   ```bash
   python3 sk/scripts/help.py 4.0 -p 3
   ```
4. **과제 성격별 추가 검증**:
   ```bash
   python3 sk/scripts/help.py 5.3 -p   # 데이터 입출력·정합성 검증
   python3 sk/scripts/help.py 5.4 -p   # API 계약 검증
   python3 sk/scripts/help.py 5.5 -p   # UI 스모크 테스트
   ```
   - HTTP/웹 서버 과제일 경우: 서버를 반드시 `0.0.0.0`에 바인딩해 실행하고(해당 터미널 탭 유지), 터미널 2에서 `python3 sk/snippets/smoke_test.py http://127.0.0.1:<PORT>/health`로 확인한 뒤 좌측 **Browser** 도구에서 포트와 경로를 입력해 직접 화면·버튼 동작을 점검합니다.
   - 만약 구현 중 막히거나 루프에 빠지면 `python3 sk/scripts/help.py 6.2 -p` (`unstuck`) 또는 `6.5 -p` (`timebox`)로 즉시 범위를 조정합니다.

### [12:00 ~ 12:15] 7단계: 코드 리뷰 및 규정 준수 감사
```bash
python3 sk/scripts/help.py 7.1 -p
python3 sk/scripts/help.py 7.2 -p
```
- [ ] `sk/work/REVIEW.md`를 통해 차단(Blocker)·높음(High) 등급 결함과 요구사항 누락을 모두 해결합니다.
- [ ] 에디터에 열린 파일들과 Codex가 수정한 파일 사이에 저장 충돌이 있다면 **'외부 변경 불러오기'**로 최신본을 맞추고 모두 `저장됨` 상태인지 확인합니다.

### [12:15 ~ 12:35] 8~9단계: 제출 보고서 및 후속 6문항 암기 카드 작성
```bash
python3 sk/scripts/help.py 9.1 -p   # 내 구현 이해 지도 (UNDERSTANDING.md)
python3 sk/scripts/help.py 9.4 -p   # 회고 및 한계·개선안 정리
python3 sk/scripts/help.py 8.1 -p   # 과제 제출용 보고서 작성
python3 sk/scripts/help.py 9.2 -p   # 후속 서술형 6문항 암기 카드 (QA_CARD.md)
```
- [ ] `sk/work/UNDERSTANDING.md`와 `sk/work/QA_CARD.md`가 생성되었는지 확인하고, 핵심 설계 이유·검증 명령·엣지 케이스·남은 한계를 눈에 익힙니다.

### [12:35 ~ 12:45] 8.2단계: 최종 납품 점검 (Deliver Gate)
```bash
python3 sk/scripts/help.py 8.2 -p
```
- [ ] 과제 안내에서 요구한 **공식 제출 파일명·경로·형식**이 정확히 존재하는지, 에디터 탭 우측이 모두 **`저장됨`**인지 확인합니다.
- [ ] `QA_CARD.md`와 `UNDERSTANDING.md` 내용을 충분히 숙지한 뒤, 제출 작업 공간을 순수 과제 파일만 남기려면 아래 명령으로 키트 설치 흔적을 정리합니다:
  ```bash
  python3 sk/scripts/install.py --uninstall
  rm -rf sk
  ```
  *(주의: 삭제 전 반드시 6문항 핵심 답변 포인트를 머릿속에 숙지하세요!)*

### [12:45 ~ 12:50] 암기 리허설 및 과제 제출 확정
- [ ] 상단 **`제출하고 문제풀기`** 클릭 → 미리보기 확인 → **`제출물 확정하고 문제풀기`** 클릭.
- [ ] **주의**: 제출물 확정 순간부터 파일 수정이 불가하며, 이어지는 후속 서술형에서는 **AI(Codex 포함) 사용 및 복사·붙여넣기가 전면 금지**됩니다.

### [12:50 ~ 13:30] 후속 서술형 6문항 직접 작성 및 최종 종료
1. **질문 생성 대기 (최대 10분)**: 제출물과 작업 기록을 바탕으로 문항이 생성될 때까지 기다립니다(이 대기 시간은 문항당 5분 타이머에 포함되지 않음).
2. **`문제 풀기` 클릭**: 준비 완료 화면에서 버튼을 누르면 1번 문항 5분 타이머가 시작됩니다.
3. **문항별 답변 (총 6문항, 문항당 5분)**:
   - 복사·붙여넣기 불가, AI 사용 불가, 이전 문항으로 돌아가기 불가.
   - 직전 답안을 제출하는 즉시 다음 문항 5분 타이머가 시작됩니다.
   - 질문의 전제와 내 실제 구현이 다르면 차이를 명확히 밝히고, **내가 선택한 구조·이유·검증 결과·남은 한계**를 내 언어로 직접 입력합니다.
4. **최종 완료 확인**: 마지막 문항에서 **`답안 제출하고 마치기`**를 누른 뒤, 녹화 업로드와 처리가 끝날 때까지 기다려 **`"과제가 잘 제출됐어요."`** 문구와 **제출 ID·시각·파일 수·크기**를 확인하고 브라우저를 닫습니다.
