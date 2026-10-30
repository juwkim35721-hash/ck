#!/usr/bin/env python3
"""로컬 SK 준비 도구 설치. 네트워크·Codex 업데이트·작업 폴더 이동 없음."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import shlex
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
COPY_DIRS = ("harness", "skills", "custom-skills", "prompts", "snippets", "templates", "playbooks", "scripts")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_within(path: Path, parent: Path) -> bool:
    return path == parent or parent in path.parents


def reject_symlinks(path: Path) -> None:
    for item in (path, *path.parents):
        if item.is_symlink():
            raise ValueError(f"심볼릭 링크 경로에는 설치하지 않습니다: {item}")


def mkdir(path: Path) -> None:
    reject_symlinks(path)
    path.mkdir(parents=True, exist_ok=True)


def project_harness(existing: bytes, payload: bytes) -> bytes:
    begin = b"<!-- SK-KIT:BEGIN -->"
    end = b"<!-- SK-KIT:END -->"
    block = begin + b"\n" + payload.rstrip(b"\n") + b"\n" + end
    if not existing.count(begin) and not existing.count(end):
        separator = (b"\n" if existing and not existing.endswith(b"\n") else b"") + (b"\n" if existing else b"")
        return existing + separator + block + b"\n"
    if existing.count(begin) != 1 or existing.count(end) != 1 or existing.index(begin) > existing.index(end):
        raise ValueError("기존 AGENTS.md의 SK-KIT 표시가 손상되거나 중복되었습니다. 자동 수정하지 않습니다")
    first = existing.index(begin)
    last = existing.index(end) + len(end)
    return existing[:first] + block + existing[last:]


def source_files() -> list[Path]:
    files = [ROOT / "README.md", ROOT / "init.sh"]
    for directory in COPY_DIRS:
        base = ROOT / directory
        if not base.is_dir():
            raise ValueError(f"필수 폴더가 없습니다: {base}")
        files.extend(sorted(p for p in base.rglob("*") if p.is_file() and "__pycache__" not in p.parts))
    for path in files:
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"일반 원본 파일이 아닙니다: {path}")
    return files


def check_install(kit: Path) -> int:
    manifest_path = kit / "installation.json"
    if not manifest_path.is_file():
        print(f"설치 기록 없음: {manifest_path}", file=sys.stderr)
        return 1
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    failures = []
    for record in manifest["files"]:
        path = Path(record["path"])
        if path.is_symlink() or not path.is_file() or digest(path) != record["sha256"]:
            failures.append(str(path))
    if failures:
        print("설치 당시와 다르거나 누락된 파일:", file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"설치 파일 {len(manifest['files'])}개 무결성 확인")
    print("이 검사는 파일만 확인합니다. Codex의 실제 스킬 인식·과제 테스트는 별도입니다.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", help="이미 존재하는 실제 과제 루트. 생략하면 프로젝트 하네스는 설치하지 않음")
    parser.add_argument("--kit", default=os.environ.get("COFA_KIT_DIR", "/tmp/cofa-kit"), help="설치 키트 위치")
    parser.add_argument("--dry-run", action="store_true", help="설치 계획만 출력하고 파일을 변경하지 않음")
    parser.add_argument("--check", action="store_true", help="기존 설치 파일 검사만 수행. 설치·덮어쓰기 없음")
    args = parser.parse_args()
    raw_kit = Path(args.kit).expanduser().absolute()
    reject_symlinks(raw_kit)
    kit = raw_kit.resolve()
    if args.check:
        if args.dry_run or args.workspace:
            parser.error("--check는 --workspace/--dry-run과 함께 사용하지 않습니다")
        return check_install(kit)

    workspace = None
    if args.workspace:
        raw_workspace = Path(args.workspace).expanduser().absolute()
        reject_symlinks(raw_workspace)
        workspace = raw_workspace.resolve()
        if not workspace.is_dir():
            raise ValueError(f"실제 과제 폴더가 없습니다. 경로를 확인하세요: {workspace}")
        if workspace == ROOT:
            raise ValueError("준비 도구 저장소를 과제 루트로 지정하지 마세요")
    home = Path.home().resolve()
    if kit in (Path("/"), home) or is_within(kit, ROOT) or is_within(ROOT, kit):
        raise ValueError("키트 위치는 홈 자체·저장소 내부·저장소의 상위 폴더일 수 없습니다")
    if workspace and (is_within(kit, workspace) or is_within(workspace, kit)):
        raise ValueError("키트와 실제 과제 폴더는 서로 겹치지 않아야 합니다")

    plans: list[tuple[Path, Path, str]] = []
    for source in source_files():
        relative = source.relative_to(ROOT)
        plans.append((source, kit / relative, "kit/" + relative.as_posix()))
    # 설치 도움말은 키트 루트에서도 실행할 수 있도록 별도 진입점을 둔다.
    plans.append((ROOT / "scripts/help.sh", kit / "help.sh", "kit/help.sh"))
    skill_count = 0
    for folder in ("skills", "custom-skills"):
        for skill in sorted((ROOT / folder).iterdir()):
            if not skill.is_dir() or not (skill / "SKILL.md").is_file():
                continue
            skill_count += 1
            for source in sorted(p for p in skill.rglob("*") if p.is_file()):
                relative = source.relative_to(skill)
                for target in (".agents", ".codex"):
                    destination = home / target / "skills" / skill.name / relative
                    label = f"{target}/skills/{skill.name}/{relative.as_posix()}"
                    plans.append((source, destination, label))
    if workspace:
        plans.append((ROOT / "harness/AGENTS.md", workspace / "AGENTS.md", "workspace/AGENTS.md"))
        if is_within(ROOT, workspace):
            print("주의: 준비 도구가 과제 루트 안에 있습니다. 폴더는 이동·삭제하지 않으며 제출 포함 여부를 직접 확인하세요.", file=sys.stderr)

    for _, destination, _ in plans:
        reject_symlinks(destination)
        if destination.exists() and not destination.is_file():
            raise ValueError(f"파일 설치 위치에 다른 유형이 있습니다: {destination}")
    for metadata_name in ("installation.json", "workspace.txt"):
        destination = kit / metadata_name
        reject_symlinks(destination)
        if destination.exists() and not destination.is_file():
            raise ValueError(f"메타데이터 위치에 다른 유형이 있습니다: {destination}")
    merged_project = None
    if workspace:
        project_path = workspace / "AGENTS.md"
        existing = project_path.read_bytes() if project_path.is_file() else b""
        merged_project = project_harness(existing, (ROOT / "harness/AGENTS.md").read_bytes())
    print(f"원본: {ROOT}\n키트: {kit}\n과제 루트: {workspace or '미지정(프로젝트 하네스 미설치)'}")
    print(f"스킬 {skill_count}개 × 검색 경로 2곳, 계획 파일 {len(plans)}개")
    if args.dry_run:
        for _, destination, _ in plans:
            print(f"계획: {destination}")
        print("dry-run 완료: 파일을 변경하지 않았습니다")
        return 0

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    backup_root = kit / "backups" / stamp
    backups: list[dict[str, str]] = []
    records: list[dict[str, str]] = []
    changed = 0

    def backup(destination: Path, label: str) -> None:
        if destination.is_file():
            backup_path = backup_root / label
            mkdir(backup_path.parent)
            shutil.copy2(destination, backup_path)
            backups.append({"original": str(destination), "backup": str(backup_path)})

    for source, destination, label in plans:
        content = merged_project if label == "workspace/AGENTS.md" else source.read_bytes()
        same = destination.is_file() and destination.read_bytes() == content
        if not same:
            backup(destination, label)
            mkdir(destination.parent)
            if label == "workspace/AGENTS.md":
                destination.write_bytes(content)
            else:
                shutil.copy2(source, destination)
            changed += 1
        records.append({"path": str(destination), "sha256": digest(destination)})
    workspace_file = kit / "workspace.txt"
    workspace_text = (str(workspace) if workspace else "") + "\n"
    if workspace_file.is_file() and workspace_file.read_text(encoding="utf-8") != workspace_text:
        backup(workspace_file, "kit/workspace.txt")
    workspace_file.write_text(workspace_text, encoding="utf-8")
    records.append({"path": str(workspace_file), "sha256": digest(workspace_file)})
    manifest_path = kit / "installation.json"
    backup(manifest_path, "kit/installation.json")
    manifest = {"format_version": 1, "source": str(ROOT), "kit": str(kit),
                "workspace": str(workspace) if workspace else None, "installed_at_utc": stamp,
                "skill_count": skill_count, "files": records, "backups": backups}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"설치 완료: 변경/신규 {changed}개, 기존 파일 백업 {len(backups)}개")
    if backups:
        print(f"백업: {backup_root}\n백업 파일은 삭제하지 않았습니다. 복구 방법은 MASTER_GUIDE를 확인하세요.")
    print(f"도움말: bash {shlex.quote(str(kit / 'help.sh'))} list")
    print("전역 ~/.codex/AGENTS.md는 변경하지 않았습니다. Codex를 실제 과제 루트에서 재시작해 스킬·하네스 적용을 확인하세요.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"설치/검사 실패: {error}", file=sys.stderr)
        raise SystemExit(1)
