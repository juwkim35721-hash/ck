#!/usr/bin/env python3
"""네트워크 없이 구조·원본 보존·로컬 문서 링크·셸 문법을 검사한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    errors = []
    preserved = json.loads((ROOT / "harness/preserved-files.json").read_text(encoding="utf-8"))
    actual = {str(p.relative_to(ROOT)) for name in ("snippets", "templates")
              for p in (ROOT / name).rglob("*") if p.is_file() and "__pycache__" not in p.parts}
    if actual != set(preserved):
        errors.append(f"보존 폴더 파일 목록 변경: 추가={sorted(actual-set(preserved))}, 누락={sorted(set(preserved)-actual)}")
    for relative, expected in preserved.items():
        path = ROOT / relative
        if not path.is_file() or path.is_symlink() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            errors.append(f"원본 변경/누락: {relative}")
    stages = json.loads((ROOT / "harness/stages.json").read_text(encoding="utf-8"))
    if len({s["id"] for s in stages}) != len(stages) or len({s["skill"] for s in stages}) != len(stages):
        errors.append("중복 단계 ID 또는 스킬명")
    expected_skills = {s["skill"] for s in stages}
    actual_skills = {p.name for p in (ROOT / "skill").iterdir() if p.is_dir()}
    if expected_skills != actual_skills:
        errors.append("단일 skill/ 폴더와 단계 목록의 스킬이 일치하지 않습니다")
    for obsolete in ("init.sh", "skills", "custom-skills"):
        if (ROOT / obsolete).exists():
            errors.append(f"통합 전 구조가 남아 있습니다: {obsolete}")
    for stage in stages:
        prompt = ROOT / "prompts" / (stage["id"] + ".md")
        skill = ROOT / "skill" / stage["skill"] / "SKILL.md"
        for path in (prompt, skill):
            if not path.is_file():
                errors.append(f"단계 파일 누락: {path.relative_to(ROOT)}")
            elif "[TODO" in path.read_text(encoding="utf-8"):
                errors.append(f"초기화 자리표시자 미완성: {path.relative_to(ROOT)}")
        if prompt.is_file() and prompt.read_text(encoding="utf-8").count("```text") < 2:
            errors.append(f"기본/심화 프롬프트 부족: {prompt.relative_to(ROOT)}")
    files = [ROOT / "README.md", ROOT / "playbooks/MASTER_GUIDE.md", ROOT / "prompts/README.md"]
    files.extend(sorted((ROOT / "prompts").glob("*.md")))
    files.extend(sorted((ROOT / "skill").glob("*/SKILL.md")))
    files.append(ROOT / "harness/AGENTS.md")
    for path in dict.fromkeys(files):
        if not path.is_file():
            errors.append(f"문서 누락: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        if not text or not text.endswith("\n") or text.count("```") % 2:
            errors.append(f"빈 문서/끝 개행/코드 블록 오류: {path.relative_to(ROOT)}")
        prose = re.sub(r"^```.*?^```\s*$", "", text, flags=re.M | re.S)
        for destination in re.findall(r"\[[^\]]+\]\(([^)]+)\)", prose):
            if "://" in destination or destination.startswith(("#", "mailto:")):
                continue
            destination = destination.split("#", 1)[0].replace("%20", " ")
            target = (path.parent / destination).resolve()
            if not target.is_relative_to(ROOT) or not target.exists():
                errors.append(f"로컬 링크 오류: {path.relative_to(ROOT)} -> {destination}")
        for block in re.findall(r"^```bash\n(.*?)^```", text, re.M | re.S):
            result = subprocess.run(["bash", "-n"], input=block, text=True, capture_output=True)
            if result.returncode:
                errors.append(f"문서 Bash 문법: {path.relative_to(ROOT)}: {result.stderr.strip()}")
    for path in (ROOT / "scripts/help.sh",):
        result = subprocess.run(["bash", "-n", str(path)], capture_output=True, text=True)
        if result.returncode:
            errors.append(f"셸 문법: {path.relative_to(ROOT)}: {result.stderr.strip()}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"검사 통과: 원본 {len(preserved)}개 보존, 단계 {len(stages)}개, 프롬프트·신규 스킬 대응, 문서 링크·셸 문법")
    print("스킬 YAML의 공식 검증과 설치 통합 테스트는 별도 수행합니다.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError) as error:
        print(f"저장소 검사 실패: {error}", file=sys.stderr)
        raise SystemExit(1)
