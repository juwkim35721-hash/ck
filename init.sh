#!/usr/bin/env bash
# SK 준비 도구: 로컬 파일 설치만 수행한다. 네트워크 요청·Codex 업데이트·폴더 이동 없음.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if ! command -v python3 >/dev/null 2>&1; then
  printf '오류: Python 3가 필요합니다. 시험 환경의 허용 범위를 먼저 확인하세요.\n' >&2
  exit 1
fi
if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)'; then
  printf '오류: Python 3.10 이상이 필요합니다. 허용 없이 환경을 업데이트하지 마세요.\n' >&2
  exit 1
fi
exec python3 "$SCRIPT_DIR/scripts/install.py" "$@"
