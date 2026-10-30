#!/usr/bin/env python3
"""SK 해커톤 키트 설치 프로그램.

약속된 사용법 (과제 루트에서 실행):
    git clone https://github.com/juwkim35721/sk sk
    python3 sk/scripts/install.py              # 설치 또는 갱신
    python3 sk/scripts/install.py --dry-run    # 변경 없이 계획만 출력
    python3 sk/scripts/install.py --check      # 설치 상태 점검 (읽기 전용)
    python3 sk/scripts/install.py --uninstall  # 설치한 것만 제거 (작업 노트·백업은 보존)

과제 루트 = sk 폴더의 부모 폴더. 네트워크·패키지 설치·Codex 설정 변경은 하지 않는다.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # <과제 루트>/sk
TASK_ROOT = ROOT.parent
STATE = ROOT / ".install"
MANIFEST = STATE / "manifest.json"
HARNESS = ROOT / "harness" / "AGENTS.md"
SKILL_SOURCE = ROOT / "skill"
SKILL_DIRS = {"agents": ".agents/skills", "codex": ".codex/skills"}
BEGIN = "<!-- SK-KIT:BEGIN (python3 sk/scripts/install.py가 관리하는 구역입니다. 직접 수정하지 마세요.) -->"
BEGIN_PREFIX = "<!-- SK-KIT:BEGIN"
END = "<!-- SK-KIT:END -->"
EXCLUDE_BEGIN = "# SK-KIT:BEGIN (python3 sk/scripts/install.py)"
EXCLUDE_END = "# SK-KIT:END"
AGENTS_LIMIT = 32 * 1024  # Codex 기본 project_doc_max_bytes


class InstallError(Exception):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(TASK_ROOT).as_posix()


def check_location() -> None:
    """약속한 위치(과제 루트/sk)에서 과제 루트를 현재 폴더로 실행했는지 확인한다."""
    if ROOT.name != "sk":
        raise InstallError(f"클론 폴더 이름은 sk여야 합니다: {ROOT}\n"
                           "과제 루트에서 git clone https://github.com/juwkim35721/sk sk 로 받으세요.")
    if Path.cwd().resolve() != TASK_ROOT.resolve():
        raise InstallError("과제 루트에서 실행하세요. 과제 루트는 sk 폴더의 부모 폴더입니다.\n"
                           f"  cd '{TASK_ROOT}' && python3 sk/scripts/install.py")
    if TASK_ROOT.resolve() in {Path.home().resolve(), Path("/")}:
        raise InstallError(f"홈 폴더나 / 를 과제 루트로 쓸 수 없습니다: {TASK_ROOT}\n"
                           "실제 과제 폴더로 이동한 뒤 그 안에서 sk를 클론하세요.")
    if not HARNESS.is_file() or not SKILL_SOURCE.is_dir():
        raise InstallError(f"sk 폴더 구성이 올바르지 않습니다: {ROOT}")


def reject_symlink(path: Path) -> None:
    """과제 루트 안의 쓰기 대상 경로에 심볼릭 링크가 있으면 거절한다 (루트 밖 쓰기 방지)."""
    current = TASK_ROOT
    for part in path.relative_to(TASK_ROOT).parts:
        current = current / part
        if current.is_symlink():
            raise InstallError(f"심볼릭 링크 경로에는 쓰지 않습니다: {current}")


def load_manifest() -> dict:
    if MANIFEST.is_file():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {}


def harness_block() -> str:
    body = HARNESS.read_text(encoding="utf-8").strip("\n")
    return f"{BEGIN}\n{body}\n{END}\n"


def split_managed(text: str) -> tuple[str, str, bool]:
    """AGENTS.md에서 관리 구역 앞/뒤를 분리한다. 표시가 손상됐으면 거절한다."""
    begins = text.count(BEGIN_PREFIX)
    ends = text.count(END)
    if begins == 0 and ends == 0:
        return text, "", False
    if begins != 1 or ends != 1 or text.index(BEGIN_PREFIX) > text.index(END):
        raise InstallError("AGENTS.md의 SK-KIT 관리 구역 표시가 손상되었거나 중복되었습니다. "
                           "직접 확인한 뒤 BEGIN/END 한 쌍만 남기세요. 자동 수정은 하지 않습니다.")
    start = text.index(BEGIN_PREFIX)
    stop = text.index(END) + len(END)
    if text[stop:stop + 1] == "\n":
        stop += 1
    return text[:start], text[stop:], True


def merged_agents(existing: str) -> str:
    before, after, found = split_managed(existing)
    block = harness_block()
    if found:
        return before + block + after
    if not existing.strip():
        return block
    return existing.rstrip("\n") + "\n\n" + block


def removed_agents(existing: str) -> str:
    before, after, found = split_managed(existing)
    if not found:
        return existing
    return (before.rstrip("\n") + "\n" + after.lstrip("\n")) if before.strip() else after.lstrip("\n")


def exclude_lines(skills_dir: str, agents_created: bool) -> list[str]:
    lines = [EXCLUDE_BEGIN, "/sk/", f"/{skills_dir}/sk-*/"]
    if agents_created:
        lines.append("/AGENTS.md")
    return lines + [EXCLUDE_END]


def strip_exclude(text: str) -> str:
    out, inside = [], False
    for line in text.splitlines():
        if line.startswith("# SK-KIT:BEGIN"):
            inside = True
            continue
        if inside and line.strip() == EXCLUDE_END:
            inside = False
            continue
        if not inside:
            out.append(line)
    return "\n".join(out).rstrip("\n") + ("\n" if out else "")


class Writer:
    """dry-run이면 계획만 출력하고, 아니면 백업 후 쓴다."""

    def __init__(self, dry_run: bool):
        self.dry_run = dry_run
        self.stamp = time.strftime("%Y%m%d-%H%M%S")
        self.backups: list[dict] = []
        self.changes: list[str] = []

    def backup(self, path: Path) -> None:
        if not path.is_file():
            return
        target = STATE / "backups" / self.stamp / rel(path)
        self.backups.append({"original": rel(path), "backup": target.relative_to(ROOT).as_posix()})
        if not self.dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)

    def write(self, path: Path, data: bytes, note: str) -> None:
        reject_symlink(path)
        if path.is_file() and path.read_bytes() == data:
            return
        self.changes.append(f"{note}: {rel(path)}")
        if self.dry_run:
            return
        self.backup(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def remove(self, path: Path, note: str) -> None:
        reject_symlink(path)
        self.changes.append(f"{note}: {rel(path)}")
        if self.dry_run:
            return
        self.backup(path)
        path.unlink()


def prune_empty(path: Path, stop: Path, dry_run: bool) -> None:
    """stop 아래에서 비어 있는 상위 폴더만 지운다."""
    current = path
    while not dry_run and current != stop and current.is_dir() and not any(current.iterdir()):
        current.rmdir()
        current = current.parent


def skill_plan(skills_dir: str) -> dict[Path, bytes]:
    plan: dict[Path, bytes] = {}
    for source in sorted(SKILL_SOURCE.rglob("*")):
        if source.is_file() and "__pycache__" not in source.parts:
            if source.is_symlink():
                raise InstallError(f"스킬 원본에 심볼릭 링크가 있습니다: {source}")
            plan[TASK_ROOT / skills_dir / source.relative_to(SKILL_SOURCE)] = source.read_bytes()
    return plan


def install(args: argparse.Namespace) -> int:
    previous = load_manifest()
    skills_dir = SKILL_DIRS[args.skills_dir]
    writer = Writer(args.dry_run)
    agents_path = TASK_ROOT / "AGENTS.md"
    reject_symlink(agents_path)
    agents_created = previous.get("agents_created", not agents_path.exists())

    # 1) 과제 루트 AGENTS.md: 기존 내용은 그대로 두고 관리 구역만 추가·갱신
    existing = agents_path.read_text(encoding="utf-8") if agents_path.is_file() else ""
    merged = merged_agents(existing)
    writer.write(agents_path, merged.encode("utf-8"), "하네스 관리 구역")
    if len(merged.encode("utf-8")) > AGENTS_LIMIT:
        print(f"경고: AGENTS.md가 {AGENTS_LIMIT // 1024}KiB를 넘어 Codex가 뒷부분을 읽지 못할 수 있습니다.")

    # 2) 스킬 복사: <과제 루트>/.agents/skills/sk-*
    plan = skill_plan(skills_dir)
    for path, data in plan.items():
        writer.write(path, data, "스킬")

    # 3) 이전 설치에만 있던 스킬 파일 정리 (내용이 기록과 같을 때만)
    kept: list[str] = []
    for entry in previous.get("files", []):
        path = TASK_ROOT / entry["path"]
        if entry.get("kind") != "skill" or path in plan or not path.is_file():
            continue
        if sha256(path.read_bytes()) == entry["sha256"]:
            writer.remove(path, "이전 스킬 정리")
            prune_empty(path.parent, TASK_ROOT, args.dry_run)
        else:
            kept.append(entry["path"])

    # 4) git 상태에서 도구 파일 숨기기 (.git/info/exclude, 로컬 전용·커밋되지 않음)
    git_dir = TASK_ROOT / ".git"
    git_exclude = git_dir.is_dir()
    if git_exclude:
        exclude = git_dir / "info" / "exclude"
        current = exclude.read_text(encoding="utf-8") if exclude.is_file() else ""
        base = strip_exclude(current)
        updated = (base.rstrip("\n") + "\n" if base.strip() else "") + "\n".join(exclude_lines(skills_dir, agents_created)) + "\n"
        if updated != current:
            writer.changes.append("git 제외 설정: .git/info/exclude")
            if not args.dry_run:
                exclude.parent.mkdir(parents=True, exist_ok=True)
                exclude.write_text(updated, encoding="utf-8")

    print(f"과제 루트: {TASK_ROOT}\n도구 폴더: {ROOT}")
    print(f"스킬 {len({p.relative_to(TASK_ROOT / skills_dir).parts[0] for p in plan})}개 → {skills_dir}/")
    for line in writer.changes:
        print(("계획  " if args.dry_run else "변경  ") + line)
    for item in kept:
        print(f"보존  사용자가 수정한 이전 스킬 파일은 지우지 않았습니다: {item}")
    if not git_exclude and (git_dir.exists()):
        print("참고  .git이 폴더가 아니어서(worktree 등) git 제외 설정을 건너뛰었습니다.")
    if args.dry_run:
        print("dry-run: 파일을 변경하지 않았습니다.")
        return 0

    (ROOT / "work").mkdir(exist_ok=True)
    STATE.mkdir(exist_ok=True)
    files = [{"path": rel(agents_path), "sha256": sha256(agents_path.read_bytes()), "kind": "harness"}]
    files += [{"path": rel(path), "sha256": sha256(data), "kind": "skill"} for path, data in plan.items()]
    manifest = {
        "format": 3,
        "task_root": str(TASK_ROOT),
        "skills_dir": skills_dir,
        "agents_created": agents_created,
        "git_exclude": git_exclude,
        "installed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "files": files,
        "backups": previous.get("backups", []) + writer.backups,
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"설치 완료: 변경 {len(writer.changes)}건, 백업 {len(writer.backups)}건 (sk/.install/backups)")
    print("다음: 과제 루트에서 codex 실행 → /skills 에서 sk-* 확인. 프롬프트 보기: python3 sk/scripts/help.py")
    return 0


def check() -> int:
    manifest = load_manifest()
    if not manifest:
        print("설치 기록이 없습니다. 과제 루트에서 python3 sk/scripts/install.py 를 실행하세요.")
        return 1
    problems = []
    for entry in manifest["files"]:
        path = TASK_ROOT / entry["path"]
        if entry["kind"] == "harness":
            text = path.read_text(encoding="utf-8") if path.is_file() else ""
            if BEGIN_PREFIX not in text or END not in text:
                problems.append(f"AGENTS.md 관리 구역 없음: {entry['path']}")
            elif harness_block() not in text:
                problems.append("AGENTS.md 관리 구역이 sk/harness/AGENTS.md와 다릅니다 (재설치로 갱신)")
        elif not path.is_file():
            problems.append(f"없음: {entry['path']}")
        elif sha256(path.read_bytes()) != entry["sha256"]:
            problems.append(f"설치 후 변경됨: {entry['path']}")
    if skill_plan(manifest["skills_dir"]).keys() != {TASK_ROOT / e["path"] for e in manifest["files"] if e["kind"] == "skill"}:
        problems.append("sk/skill 원본과 설치된 스킬 목록이 다릅니다 (git pull 후 재설치 필요)")
    skills = {Path(e["path"]).parts[2] for e in manifest["files"] if e["kind"] == "skill"}
    print(f"과제 루트: {TASK_ROOT}\n설치 시각: {manifest['installed_at']}\n스킬 {len(skills)}개 → {manifest['skills_dir']}/")
    for problem in problems:
        print(f"문제  {problem}")
    print("점검 결과: 정상" if not problems else f"점검 결과: 문제 {len(problems)}건")
    print("참고: 이 점검은 파일 상태만 봅니다. Codex 인식 여부는 codex 안에서 /skills 로 확인하세요.")
    return 0 if not problems else 1


def uninstall(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    if not manifest:
        print("설치 기록이 없어 제거할 것이 없습니다.")
        return 0
    writer = Writer(args.dry_run)
    kept = []
    for entry in manifest["files"]:
        path = TASK_ROOT / entry["path"]
        if entry["kind"] != "skill" or not path.is_file():
            continue
        if sha256(path.read_bytes()) == entry["sha256"]:
            writer.remove(path, "스킬 제거")
            prune_empty(path.parent, TASK_ROOT, args.dry_run)
        else:
            kept.append(entry["path"])
    agents_path = TASK_ROOT / "AGENTS.md"
    if agents_path.is_file():
        text = agents_path.read_text(encoding="utf-8")
        remaining = removed_agents(text)
        if remaining != text:
            if manifest.get("agents_created") and not remaining.strip():
                writer.remove(agents_path, "하네스 파일 제거(설치 때 새로 만든 파일)")
            else:
                writer.write(agents_path, remaining.encode("utf-8"), "하네스 관리 구역 제거")
    exclude = TASK_ROOT / ".git" / "info" / "exclude"
    if manifest.get("git_exclude") and exclude.is_file():
        text = exclude.read_text(encoding="utf-8")
        if strip_exclude(text) != text:
            writer.changes.append("git 제외 설정 제거: .git/info/exclude")
            if not args.dry_run:
                exclude.write_text(strip_exclude(text), encoding="utf-8")
    for line in writer.changes:
        print(("계획  " if args.dry_run else "제거  ") + line)
    for item in kept:
        print(f"보존  설치 후 수정된 파일이라 지우지 않았습니다: {item}")
    if args.dry_run:
        print("dry-run: 파일을 변경하지 않았습니다.")
        return 0
    manifest["uninstalled_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    manifest["backups"] = manifest.get("backups", []) + writer.backups
    MANIFEST.rename(STATE / f"manifest.uninstalled-{writer.stamp}.json")
    (STATE / f"manifest.uninstalled-{writer.stamp}.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("제거 완료. 작업 노트(sk/work)와 백업(sk/.install)은 남겨 두었습니다.")
    print("sk 폴더 자체를 지울지는 공식 제출 규칙을 확인한 뒤 결정하세요. 필요한 노트는 먼저 과제 루트 밖으로 복사하세요.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="SK 해커톤 키트 설치. 과제 루트에서 python3 sk/scripts/install.py 로 실행합니다.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="설치 상태만 점검 (읽기 전용)")
    mode.add_argument("--uninstall", action="store_true", help="설치한 하네스 구역·스킬·git 제외 설정 제거")
    parser.add_argument("--dry-run", action="store_true", help="변경 없이 계획만 출력 (설치·제거와 함께 사용)")
    parser.add_argument("--skills-dir", choices=sorted(SKILL_DIRS), default="agents",
                        help="스킬 설치 위치. 기본 agents=.agents/skills. 구버전 Codex에서 /skills에 안 보일 때만 codex")
    args = parser.parse_args()
    try:
        check_location()
        if args.check:
            if args.dry_run:
                parser.error("--check는 이미 읽기 전용입니다")
            return check()
        if args.uninstall:
            return uninstall(args)
        return install(args)
    except InstallError as error:
        print(f"중단: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
