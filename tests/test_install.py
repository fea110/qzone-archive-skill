"""Offline installer checks. No QQ access or user profile changes."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "install.py"


class InstallTests(unittest.TestCase):
    def test_install_to_explicit_skills_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "profile with spaces" / "skills"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--skills-dir", str(target)],
                text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            installed = target / "qzone-archive" / "SKILL.md"
            self.assertEqual(installed.read_bytes(), (ROOT / "qzone-archive" / "SKILL.md").read_bytes())

    def test_dry_run_does_not_create_target(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "missing" / "skills"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--skills-dir", str(target), "--dry-run"],
                text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(str(target / "qzone-archive"), result.stdout)
            self.assertFalse(target.exists())

    def test_default_destination_respects_hermes_home(self):
        with tempfile.TemporaryDirectory() as temp:
            profile = Path(temp) / "hermes-profile"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--dry-run"],
                env=dict(os.environ, HERMES_HOME=str(profile)),
                text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(str(profile / "skills" / "qzone-archive"), result.stdout)
            self.assertFalse(profile.exists())

    def test_existing_skill_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            skills = Path(temp) / "skills"
            existing = skills / "qzone-archive"
            existing.mkdir(parents=True)
            original = existing / "SKILL.md"
            original.write_text("my private improvements", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--skills-dir", str(skills)],
                text=True, capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(original.read_text(encoding="utf-8"), "my private improvements")
            self.assertEqual(list(existing.iterdir()), [original])

    def test_explicit_directory_overrides_hermes_home(self):
        with tempfile.TemporaryDirectory() as temp:
            explicit = Path(temp) / "chosen" / "skills"
            other = Path(temp) / "other-profile"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--skills-dir", str(explicit), "--dry-run"],
                env=dict(os.environ, HERMES_HOME=str(other)),
                text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(str(explicit / "qzone-archive"), result.stdout)
            self.assertNotIn(str(other), result.stdout)
            self.assertFalse(explicit.exists())
            self.assertFalse(other.exists())


if __name__ == "__main__":
    unittest.main()
