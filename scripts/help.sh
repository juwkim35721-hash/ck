#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$HERE/help.py" ]]; then
  exec python3 "$HERE/help.py" "$@"
fi
exec python3 "$HERE/scripts/help.py" "$@"
