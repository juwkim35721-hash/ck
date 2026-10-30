# SK하이닉스 해커톤 대비 — 전략 프롬프트 & 문제 해결 하네스

[juwkim35721/sk](https://github.com/juwkim35721/sk)는 과제를 **정확히 정의하고, 작은 단위로 구현하고, 실제 증거로 검증하는 과정**을 돕는 공개 준비 도구입니다. 완성된 과제 정답이나 대회 공식 안내를 제공하지 않습니다. 공식 규정과 AI 사용 허용 범위를 확인한 뒤 사용하세요.

**기존 `skills/`, `snippets/`, `templates/`의 11개 파일은 그대로 보존했습니다.** 더 세분화된 신규 스킬 18개는 `custom-skills/`에 분리했고, 사람에게 바로 쓸모 있는 기본·심화 프롬프트 36개는 `prompts/`의 단계별 Markdown 18개에 담았습니다.

## 빠른 시작

Python **3.10 이상**, Bash가 필요합니다. 클론할 때만 Git·네트워크가 필요하며, 새 `init.sh`는 저장소의 로컬 파일만 설치합니다. Codex나 외부 스킬 저장소를 다운로드·업데이트하지 않습니다.

일반 터미널에서 홈 디렉토리 아래 **`sk`**에 클론합니다.

```bash
cd ~ && git clone https://github.com/juwkim35721/sk sk
```

실제 과제 폴더가 `~/workspace`인 경우 다음을 실행합니다. 다른 경로이면 `--workspace` 값을 바꾸세요. 폴더는 이미 존재해야 합니다.

```bash
bash ~/sk/init.sh --workspace "$HOME/workspace"
```

그다음 **실제 과제 루트에서** Codex를 실행합니다. `~/sk`는 준비 도구 저장소이므로 과제 작업 위치로 사용하지 않습니다.

```bash
cd ~/workspace && codex
```

제공 버전이 지원하면 Codex에서 `/status`, `/skills`, `/model`을 확인합니다. 모델 선택과 버전 변경은 공식 안내를 따르며, 없는 명령을 쓰기 위해 Codex를 업데이트하지 않습니다.

설치 전 계획만 확인하려면 `--dry-run`, 설치 기록을 검사만 하려면 `--check`를 사용합니다.

```bash
bash ~/sk/init.sh --workspace "$HOME/workspace" --dry-run
bash ~/sk/init.sh --check
```

`--workspace`를 생략하면 스킬·키트만 설치하고 프로젝트 `AGENTS.md`는 설치하지 않습니다. 개인 연습 환경의 기존 설정도 설치 전에 확인하세요.

## 지금 필요한 프롬프트 고르기

전체 순서와 상황별 선택은 [프롬프트 목록](prompts/README.md), 실전 운영·시간 배분·복구는 [MASTER_GUIDE](playbooks/MASTER_GUIDE.md)에서 확인합니다.

```bash
bash /tmp/cofa-kit/help.sh list
bash /tmp/cofa-kit/help.sh 01
bash /tmp/cofa-kit/help.sh debug
bash /tmp/cofa-kit/help.sh --search 경계
```

설치 전에도 `bash ~/sk/scripts/help.sh list`로 볼 수 있습니다. Markdown 안의 **기본 또는 심화 프롬프트 코드 블록만** Codex에 전달하고, `[과제 루트]`, `[남은 시간: 분]` 등은 실제 값으로 바꿉니다. `$sk-define` 같은 호출이 지원되지 않으면 호출 부분을 빼고 자연어 지시로 사용하세요.

기본 흐름은 다음과 같습니다. 매번 12단계를 모두 실행할 필요는 없습니다.

> 환경·기준선 → 문제 정의 → 정책 확인 → 입출력 계약 → 위험 기반 계획 → 최소 설계 → 수직 슬라이스 구현 → 예외 방어 → 독립 검증 → 반증 리뷰 → 제출 준비 → 설명·회고

오류 반복에는 `$sk-debug`, 맥락 손실에는 `$sk-resume`, 시간 부족에는 `$sk-timebox`를 선택합니다. 데이터·API·UI 과제에는 각각 `$sk-data-validation`, `$sk-api-contract`, `$sk-ui-smoke`를 추가합니다.

## 저장소 구성

```text
sk/
├── README.md
├── init.sh                         # 로컬 설치 진입점
├── harness/
│   ├── AGENTS.md                   # 새 프로젝트 하네스
│   ├── stages.json                 # 단계·프롬프트·스킬 대응 목록
│   └── preserved-files.json        # 기존 11개 파일의 보존 해시
├── prompts/                        # 단계별 Markdown 18개 + 사용 안내
├── custom-skills/                  # 새 맞춤형 스킬 18개
├── skills/                         # 기존 cofa-* 스킬 6개, 원본 보존
├── snippets/                       # 기존 진단 코드 2개, 원본 보존
├── templates/                      # 기존 양식 3개, 원본 보존
├── playbooks/
│   └── MASTER_GUIDE.md              # 처음부터 다시 작성한 실전 운영 가이드
├── scripts/                        # 설치·도움말·구조 검사
└── tests/                          # 설치·백업·도움말 통합 테스트
```

신규 `sk-*`와 기존 `cofa-*` 스킬은 이름이 달라 공존합니다. 기본 설치는 양쪽 스킬을 모두 `~/.agents/skills`와 `~/.codex/skills`에 복사합니다. 기존 스킬의 고정 경로·광범위한 설명은 보존되어 있으므로 **새 흐름에는 `sk-*`를 우선 사용**하세요.

## 설치가 바꾸는 것과 바꾸지 않는 것

키트 기본 위치는 `/tmp/cofa-kit`입니다. 다른 위치가 필요하면 설치와 도움말 실행에 같은 `COFA_KIT_DIR`를 사용하거나 설치 시 `--kit`을 전달합니다.

```bash
export COFA_KIT_DIR="$HOME/.local/share/sk-kit"
bash ~/sk/init.sh --workspace "$HOME/workspace"
bash "$COFA_KIT_DIR/help.sh" list
```

설치는 저장소의 실제 파일을 복사합니다. `--workspace`를 지정하면 해당 폴더의 `AGENTS.md`에 새 하네스를 추가합니다. **기존 지시문은 그대로 유지하고 `SK-KIT:BEGIN/END`로 표시된 관리 구역만 추가·갱신**하며, 변경 전 전체 파일을 키트의 `backups/`에 보관합니다. 표시가 손상되거나 중복되면 자동 수정을 거절합니다. 동일 이름의 스킬·키트 파일도 바뀌는 경우 백업합니다. 무관한 스킬은 삭제하지 않습니다.

**전역 `~/.codex/AGENTS.md`는 변경하지 않습니다.** 작업 폴더·클론 폴더를 이동하거나 삭제하지 않고, 외부 저장소를 추가로 가져오지 않으며, Codex 설치·모델·시스템 설정을 변경하지 않습니다. 이전 버전에서 설치한 전역 하네스가 이미 있다면 자동 제거되지 않으므로 충돌 여부를 확인하세요. 설치에 실패한 경우 일부 파일이 이미 복사되었을 수 있으니 첫 오류와 백업을 확인합니다.

`installation.json`은 설치 파일의 해시와 백업 위치를 기록하며, `workspace.txt`에는 지정한 과제 루트가 저장됩니다. `/tmp`는 임시 공간이므로 시스템이 지우면 재설치해야 합니다. 백업을 장기 보관하려면 홈 아래 키트를 선택하세요.

## 검사

개발·개인 연습 환경에서 다음을 실행합니다.

```bash
cd ~/sk && python3 scripts/check_repo.py
cd ~/sk && python3 -m unittest discover -s tests -v
```

구조 검사에는 기존 파일 보존, 단계·스킬 대응, 문서 링크와 셸 문법 확인이 포함됩니다. 통합 테스트는 임시 HOME·과제 폴더·키트에서 설치를 실행하므로 실제 사용자 설정을 건드리지 않습니다. 이 검사는 준비 도구 자체에 대한 검사이며 **해커톤 과제의 정답·채점·Codex 인식까지 보장하지 않습니다.**

## 사용 경계

출시 단계는 기본적으로 **해커톤 제출·릴리스 준비**입니다. 프롬프트나 설치 스크립트가 외부 push·배포·제출 버튼을 자동 실행하지 않습니다. 실제 외부 동작은 별도 권한과 과제 규정을 따릅니다.

원본 `data_audit.py`는 CSV·JSON·JSONL 파일 하나를 받는 보조 감사이고, 원본 `smoke_test.py`는 GET 응답을 출력하는 보조 검사입니다. 지원 형식·중복 판정·종료 코드의 한계는 MASTER_GUIDE에 정리했습니다. 스니펫의 출력만으로 정확성을 단정하지 마세요.

공개 저장소에 비공개 과제·데이터·자격증명·개인 링크를 올리지 않습니다. 후속 평가에서 AI·자료 참조·복사·붙여넣기가 금지되면 해당 단계의 프롬프트·스킬 사용을 중단하고 직접 답합니다. 공식 메일이 제공되지 않았으므로 특정 모델·시험 시각·출제 문항·점수 보장을 주장하지 않습니다.
