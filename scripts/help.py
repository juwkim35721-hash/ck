#!/usr/bin/env python3
"""SK 준비 도구의 단계별 Markdown을 읽기 전용으로 출력한다."""
import argparse
import json
import os
from pathlib import Path
import sys


def main() -> int:
    root = Path(os.environ.get("COFA_KIT_DIR", str(Path(__file__).resolve().parent.parent))).expanduser()
    stages = json.loads((root / "harness/stages.json").read_text(encoding="utf-8"))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic", nargs="?", default="list", help="list, 00, 단계 ID, 스킬명, guide, dm, doc, qa, workspace")
    parser.add_argument("--search", metavar="TEXT", help="제목·스킬명·프롬프트 내용 검색")
    args = parser.parse_args()
    if args.search:
        term = args.search.casefold()
        found = False
        for stage in stages:
            text = (root / "prompts" / (stage["id"] + ".md")).read_text(encoding="utf-8")
            if term in (stage["title"] + stage["skill"] + text).casefold():
                print(f"{stage['id']:22} {stage['title']}  (${stage['skill']})")
                found = True
        if not found:
            print("검색 결과 없음")
        return 0
    if args.topic in ("list", "all"):
        for stage in stages:
            mark = "기본" if stage["kind"] == "core" else "보조"
            print(f"[{mark}] {stage['id']:22} {stage['title']}  (${stage['skill']})")
        print("\n예: bash ~/sk/scripts/help.sh 01")
        print("설치 후: bash /tmp/cofa-kit/help.sh debug 또는 --search 경계")
        print("프롬프트의 [자리표시자]를 실제 입력으로 바꾸고 코드 블록만 Codex에 전달하세요.")
        return 0
    special = {"guide": "playbooks/MASTER_GUIDE.md", "dm": "templates/DM_QUESTION_TEMPLATES.txt",
               "doc": "templates/SUBMISSION_DOC_TEMPLATE.md", "qa": "templates/POST_QA_6_TEMPLATE.md"}
    if args.topic == "workspace":
        marker = root / "workspace.txt"
        text = marker.read_text(encoding="utf-8").strip() if marker.is_file() else ""
        print(text or "과제 루트 미지정. init.sh --workspace <실제 과제 루트>로 하네스를 설치하세요.")
        return 0
    if args.topic in special:
        path = root / special[args.topic]
    else:
        matches = [s for s in stages if args.topic in (s["id"], s["id"].split("-", 1)[0], s["id"].split("-", 1)[1], s["skill"])]
        if len(matches) != 1:
            print(f"알 수 없거나 모호한 단계: {args.topic}. list로 목록을 확인하세요.", file=sys.stderr)
            return 2
        path = root / "prompts" / (matches[0]["id"] + ".md")
    print(path.read_text(encoding="utf-8"), end="")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError) as error:
        print(f"도움말 오류: {error}", file=sys.stderr)
        raise SystemExit(1)
