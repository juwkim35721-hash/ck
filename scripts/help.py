#!/usr/bin/env python3
"""SK 프롬프트·템플릿·작업 노트 도우미 (어디서 실행해도 동작, 읽기 전용).

    python3 sk/scripts/help.py               단계별 전체 목록
    python3 sk/scripts/help.py 1             1단계 폴더의 프롬프트 목록
    python3 sk/scripts/help.py 1.3           프롬프트 파일 전체 (ID 또는 이름: dm-questions)
    python3 sk/scripts/help.py 1.3 -p        기본 프롬프트만 출력 (복사용)
    python3 sk/scripts/help.py 1.3 -p 2      두 번째 프롬프트 블록 출력
    python3 sk/scripts/help.py 1.3 -b        프롬프트 블록 제목 목록
    python3 sk/scripts/help.py -s 동점        제목·본문 검색
    python3 sk/scripts/help.py dm|report|qa  템플릿 원문 (DM 질문 / 보고서 / 6문항 카드)
    python3 sk/scripts/help.py work          작업 노트(sk/work) 현황
    python3 sk/scripts/help.py flow          권장 진행 순서 요약
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "prompts"
TEMPLATES = {
    "dm": "templates/DM_QUESTION_TEMPLATES.txt",
    "report": "templates/SUBMISSION_DOC_TEMPLATE.md",
    "qa": "templates/POST_QA_6_TEMPLATE.md",
}
NOTES = ["BRIEF", "DISCOVERY", "DM_LOG", "SPEC", "PLAN", "DECISIONS", "EVIDENCE", "REVIEW",
         "UNDERSTANDING", "QA_CARD", "REPORT_DRAFT"]
FLOW = """권장 진행 순서 (상세: sk/playbooks/MASTER_GUIDE.md)
  0 착수      0.1 context → 0.2 triage → 0.3 code-map
  1 발굴·DM   1.1 requirements → 1.2 ambiguity → 1.3 dm-questions → (DM 전송·답변) → 1.4 dm-answers → 1.5 dm-confirm
  2 명세      2.1 spec → 2.2 io-contract → 2.3 acceptance → 2.4 spec-gate   ← READY 전에는 구현하지 않음
  3 계획      3.1 plan → 3.2 design   (3.3 decision-log는 수시로)
  4 구현 루프  슬라이스마다 4.1 test-first → 4.2 implement → 4.3 harden → 5.1 verify / 5.2 evidence
  5 검증 특화  5.3 data-validation · 5.4 api-contract · 5.5 ui-smoke
  6 막힐 때    6.1 debug · 6.2 unstuck · 6.3 rollback · 6.4 resume · 6.5 timebox
  7 리뷰      7.1 review → 7.2 compliance
  마무리      9.1 understand → 9.4 retrospect → 8.1 report → 9.2 qa-card → 8.2 deliver → 9.3 qa-drill
              (보고서 3·5절 근거를 먼저 만들고, 6문항 대비는 제출 전 AI 허용 시간에만)"""
BLOCK = re.compile(r"^```text\n(.*?)^```", re.S | re.M)


def prompt_files() -> list[dict]:
    items = []
    for path in sorted(PROMPTS.glob("*/*.md")):
        text = path.read_text(encoding="utf-8")
        head = re.match(r"#\s+(\d+\.\d+)\s+(.+)", text)
        if not head:
            continue
        skill = re.search(r"^>\s*스킬:.*?\$(sk-[a-z0-9-]+)", text, re.M)
        items.append({
            "id": head.group(1),
            "title": head.group(2).strip(),
            "slug": path.stem.split("-", 1)[1] if "-" in path.stem else path.stem,
            "phase": path.parent.name,
            "skill": skill.group(1) if skill else "-",
            "path": path,
            "text": text,
        })
    return sorted(items, key=lambda i: tuple(int(x) for x in i["id"].split(".")))


def blocks(text: str) -> list[tuple[str, str]]:
    found = []
    for match in BLOCK.finditer(text):
        heading = re.findall(r"^##\s+(.+)$", text[:match.start()], re.M)
        found.append((heading[-1].strip() if heading else "프롬프트", match.group(1).rstrip("\n")))
    return found


def show_list(items: list[dict], phase: str | None = None) -> None:
    current = None
    for item in items:
        if phase is not None and not item["phase"].startswith(phase + "-"):
            continue
        if item["phase"] != current:
            current = item["phase"]
            print(f"\n[{current}]")
        print(f"  {item['id']:<5} {item['slug']:<16} ${item['skill']:<20} {item['title']}")
    print("\n보기: help.py <ID> · 복사용: help.py <ID> -p · 검색: help.py -s <단어> · 순서: help.py flow")


def find(items: list[dict], key: str) -> dict | None:
    for item in items:
        short = item["skill"][3:] if item["skill"].startswith("sk-") else item["skill"]
        if key in (item["id"], item["slug"], item["skill"], short):
            return item
    return None


def notes_status() -> None:
    work = ROOT / "work"
    print(f"작업 노트 폴더: {work}")
    for name in NOTES:
        path = work / f"{name}.md"
        if path.is_file():
            lines = path.read_text(encoding="utf-8").count("\n")
            print(f"  [있음] {name}.md ({lines}줄)")
        else:
            print(f"  [없음] {name}.md")


def main() -> int:
    parser = argparse.ArgumentParser(description="SK 프롬프트 도우미 (읽기 전용)")
    parser.add_argument("key", nargs="?", help="ID(1.3), 이름(dm-questions), 단계 번호(1), dm/report/qa, work, flow")
    parser.add_argument("-p", "--prompt", nargs="?", const=1, type=int, help="N번째 프롬프트 블록만 출력 (기본 1)")
    parser.add_argument("-b", "--blocks", action="store_true", help="프롬프트 블록 제목 목록")
    parser.add_argument("-s", "--search", help="제목·본문 검색어")
    args = parser.parse_args()
    items = prompt_files()

    if args.search:
        word = args.search.lower()
        hits = [i for i in items if word in i["text"].lower()]
        for item in hits:
            count = item["text"].lower().count(word)
            print(f"  {item['id']:<5} {item['title']}  ({count}회)  {item['path'].relative_to(ROOT.parent)}")
        print(f"{len(hits)}개 파일")
        return 0 if hits else 1
    if not args.key:
        show_list(items)
        return 0
    if args.key == "flow":
        print(FLOW)
        return 0
    if args.key == "work":
        notes_status()
        return 0
    if args.key in TEMPLATES:
        print(f"# {TEMPLATES[args.key]}\n")
        print((ROOT / TEMPLATES[args.key]).read_text(encoding="utf-8"))
        return 0
    if args.key.isdigit():
        show_list(items, args.key)
        return 0
    item = find(items, args.key)
    if not item:
        print(f"찾을 수 없습니다: {args.key}. 목록: python3 sk/scripts/help.py", file=sys.stderr)
        return 1
    found = blocks(item["text"])
    if args.blocks:
        for number, (heading, _) in enumerate(found, 1):
            print(f"  -p {number}  {heading}")
        return 0
    if args.prompt is not None:
        if not 1 <= args.prompt <= len(found):
            print(f"{item['id']}의 프롬프트 블록은 {len(found)}개입니다.", file=sys.stderr)
            return 1
        print(found[args.prompt - 1][1])
        return 0
    print(f"파일: {item['path'].relative_to(ROOT.parent)}\n")
    print(item["text"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
