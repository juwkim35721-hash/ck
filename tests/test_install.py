"""설치 테스트는 실제 HOME·전역 설정·과제 파일에 접근하지 않는다."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="sk-kit-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.home = self.base / "home with spaces"
        self.workspace = self.base / "task with spaces"
        self.kit = self.base / "kit with spaces"
        self.home.mkdir()
        self.workspace.mkdir()
        self.env = dict(os.environ, HOME=str(self.home))
        self.env.pop("COFA_KIT_DIR", None)
        self.global_agents = self.home / ".codex/AGENTS.md"
        self.global_agents.parent.mkdir()
        self.global_agents.write_text("global original\n")
        (self.workspace / "README.md").write_text("private task\n")

    def install(self, *args, expected=0):
        result = subprocess.run(["bash", str(ROOT / "init.sh"), "--kit", str(self.kit), *args],
                                env=self.env, cwd=self.base, text=True, capture_output=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def helper(self, *args, expected=0):
        result = subprocess.run(["bash", str(self.kit / "help.sh"), *args], env=self.env,
                                cwd=self.base, text=True, capture_output=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def test_install_copies_sources_and_keeps_global_and_task_data(self):
        self.install("--workspace", str(self.workspace))
        self.assertEqual(self.global_agents.read_text(), "global original\n")
        self.assertEqual((self.workspace / "README.md").read_text(), "private task\n")
        self.assertIn((ROOT / "harness/AGENTS.md").read_bytes(), (self.workspace / "AGENTS.md").read_bytes())
        self.assertEqual((self.kit / "workspace.txt").read_text().strip(), str(self.workspace))
        manifest = json.loads((self.kit / "installation.json").read_text())
        self.assertEqual(manifest["skill_count"], 24)
        for target in (".agents", ".codex"):
            for skill_root in ("skills", "custom-skills"):
                for skill in (ROOT / skill_root).iterdir():
                    if skill.is_dir():
                        self.assertEqual((self.home / target / "skills" / skill.name / "SKILL.md").read_bytes(),
                                         (skill / "SKILL.md").read_bytes())
        self.install("--check")

    def test_backup_and_repeat_install_preserve_unrelated_skill(self):
        old = self.workspace / "AGENTS.md"
        old.write_text("existing project instructions\n")
        unrelated = self.home / ".agents/skills/unrelated/SKILL.md"
        unrelated.parent.mkdir(parents=True)
        unrelated.write_text("unrelated skill\n")
        self.install("--workspace", str(self.workspace))
        manifest = json.loads((self.kit / "installation.json").read_text())
        backup = next(b for b in manifest["backups"] if b["original"] == str(old))
        self.assertEqual(Path(backup["backup"]).read_text(), "existing project instructions\n")
        self.assertTrue(old.read_text().startswith("existing project instructions\n"))
        self.install("--workspace", str(self.workspace))
        self.assertEqual(unrelated.read_text(), "unrelated skill\n")
        self.assertEqual(Path(backup["backup"]).read_text(), "existing project instructions\n")
        self.assertEqual(self.global_agents.read_text(), "global original\n")
        self.install("--check")

    def test_managed_project_section_keeps_user_additions_on_reinstall(self):
        self.install("--workspace", str(self.workspace))
        path = self.workspace / "AGENTS.md"
        path.write_text("custom leading rule\n" + path.read_text() + "custom trailing rule\n")
        self.install("--workspace", str(self.workspace))
        text = path.read_text()
        self.assertTrue(text.startswith("custom leading rule\n"))
        self.assertTrue(text.endswith("custom trailing rule\n"))
        self.assertEqual(text.count("<!-- SK-KIT:BEGIN -->"), 1)
        self.assertEqual(text.count("<!-- SK-KIT:END -->"), 1)
        self.install("--check")

    def test_broken_managed_marker_rejected_before_installation(self):
        path = self.workspace / "AGENTS.md"
        path.write_text("original\n<!-- SK-KIT:BEGIN -->\n")
        self.install("--workspace", str(self.workspace), expected=1)
        self.assertFalse(self.kit.exists())
        self.assertEqual(path.read_text(), "original\n<!-- SK-KIT:BEGIN -->\n")

    def test_dry_run_has_no_writes(self):
        before = sorted(str(p.relative_to(self.base)) for p in self.base.rglob("*"))
        self.install("--workspace", str(self.workspace), "--dry-run")
        after = sorted(str(p.relative_to(self.base)) for p in self.base.rglob("*"))
        self.assertEqual(before, after)
        self.assertFalse(self.kit.exists())
        self.assertFalse((self.workspace / "AGENTS.md").exists())

    def test_missing_workspace_rejected_without_creating_folder(self):
        missing = self.base / "missing"
        self.install("--workspace", str(missing), expected=1)
        self.assertFalse(missing.exists())
        self.assertFalse(self.kit.exists())

    def test_no_workspace_installs_only_skills_and_kit(self):
        self.install()
        self.assertFalse((self.workspace / "AGENTS.md").exists())
        self.assertEqual((self.kit / "workspace.txt").read_text().strip(), "")
        self.assertIn("과제 루트 미지정", self.helper("workspace").stdout)
        self.install("--check")

    def test_hash_check_detects_changed_installed_file(self):
        self.install("--workspace", str(self.workspace))
        (self.workspace / "AGENTS.md").write_text("intentional change\n")
        self.assertIn("다르거나 누락", self.install("--check", expected=1).stderr)

    def test_helper_lists_and_resolves_every_stage(self):
        self.install()
        stages = json.loads((ROOT / "harness/stages.json").read_text())
        listing = self.helper("list").stdout
        for stage in stages:
            self.assertIn(stage["skill"], listing)
            output = self.helper(stage["id"]).stdout
            self.assertEqual(output, (ROOT / "prompts" / (stage["id"] + ".md")).read_text())
        self.assertIn("sk-debug", self.helper("debug").stdout)
        self.assertIn("sk-define", self.helper("01").stdout)
        self.assertIn("sk-api-contract", self.helper("--search", "API").stdout)
        self.helper("not-a-stage", expected=2)
        for alias in ("guide", "dm", "doc", "qa"):
            self.assertTrue(self.helper(alias).stdout.strip())

    def test_symlink_destination_is_rejected_without_writes(self):
        outside = self.base / "outside"
        outside.mkdir()
        self.kit.symlink_to(outside, target_is_directory=True)
        self.install(expected=1)
        self.assertEqual(list(outside.iterdir()), [])

    def test_workspace_kit_overlap_is_rejected(self):
        self.kit = self.workspace / "kit"
        self.install("--workspace", str(self.workspace), expected=1)
        self.assertFalse(self.kit.exists())

    def test_custom_kit_environment_is_supported(self):
        self.env["COFA_KIT_DIR"] = str(self.kit)
        result = subprocess.run(["bash", str(ROOT / "init.sh"), "--workspace", str(self.workspace)],
                                env=self.env, cwd=self.base, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("sk-context", self.helper("list").stdout)


if __name__ == "__main__":
    unittest.main()
