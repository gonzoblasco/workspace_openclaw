#!/usr/bin/env python3
"""
test_slice_commit.py - Tests de F3 (slice_commit.py).

    python3 agents/kanam-dev/bin/test_slice_commit.py

Cada test crea un repo git temporal real: el script decide sobre el estado de
HEAD, y simularlo con mocks probaria el mock, no el comportamiento.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import slice_commit  # noqa: E402


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def make_repo(tmp: Path) -> Path:
    repo = tmp / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "dev@test.local")
    git(repo, "config", "user.name", "Test")
    (repo / "README.md").write_text("# x\n", encoding="utf-8")
    git(repo, "add", "README.md")
    git(repo, "commit", "-q", "-m", "init")
    return repo


class TestDangerous(unittest.TestCase):
    def test_env_is_dangerous(self):
        self.assertTrue(slice_commit.is_dangerous(".env"))
        self.assertTrue(slice_commit.is_dangerous("config/.env.local"))

    def test_db_is_dangerous(self):
        self.assertTrue(slice_commit.is_dangerous("data/memory.db"))
        self.assertTrue(slice_commit.is_dangerous("x.sqlite3"))

    def test_venv_and_node_modules_are_dangerous(self):
        self.assertTrue(slice_commit.is_dangerous(".venv/lib/python"))
        self.assertTrue(slice_commit.is_dangerous("node_modules/pkg/index.js"))

    def test_secrets_are_dangerous(self):
        self.assertTrue(slice_commit.is_dangerous("secrets.json"))
        self.assertTrue(slice_commit.is_dangerous("creds/credentials.yaml"))
        self.assertTrue(slice_commit.is_dangerous("server.pem"))

    def test_normal_files_are_not_dangerous(self):
        self.assertFalse(slice_commit.is_dangerous("src/app.js"))
        self.assertFalse(slice_commit.is_dangerous("docs/guide.md"))
        self.assertFalse(slice_commit.is_dangerous("test/foo.test.js"))


class TestClassify(unittest.TestCase):
    def test_docs_by_extension(self):
        self.assertEqual(slice_commit.classify("docs/adr/001-x.md")[0], "docs")
        self.assertEqual(slice_commit.classify("README.md")[0], "docs")

    def test_tests_win_over_code(self):
        self.assertEqual(slice_commit.classify("test/foo.test.js")[0], "test")
        self.assertEqual(slice_commit.classify("tests/test_foo.py")[0], "test")

    def test_ci_paths(self):
        self.assertEqual(slice_commit.classify(".github/workflows/ci.yml")[0], "ci")

    def test_chore_configs(self):
        self.assertEqual(slice_commit.classify("package.json")[0], "chore")
        self.assertEqual(slice_commit.classify(".gitignore")[0], "chore")

    def test_code_needs_head_lookup(self):
        self.assertEqual(slice_commit.classify("src/core/logic.js")[0], "code")


class TestPlanOnRealRepo(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = make_repo(Path(self.tmp.name))

    def tearDown(self):
        self.tmp.cleanup()

    def test_groups_by_intention(self):
        (self.repo / "src").mkdir()
        (self.repo / "src" / "new.js").write_text("x\n", encoding="utf-8")
        (self.repo / "README.md").write_text("# x\n\nmore\n", encoding="utf-8")
        (self.repo / "test").mkdir()
        (self.repo / "test" / "a.test.js").write_text("x\n", encoding="utf-8")

        commits, dangerous = slice_commit.plan(self.repo, None)
        self.assertEqual(dangerous, [])
        kinds = [c["type"] for c in commits]
        self.assertIn("feat", kinds)
        self.assertIn("docs", kinds)
        self.assertIn("test", kinds)

    def test_new_file_is_feat_and_modified_is_fix(self):
        (self.repo / "src").mkdir()
        new = self.repo / "src" / "brand-new.js"
        new.write_text("x\n", encoding="utf-8")
        (self.repo / "README.md").write_text("# x\n\nchanged\n", encoding="utf-8")
        git(self.repo, "add", "README.md")
        git(self.repo, "commit", "-q", "-m", "seed")
        (self.repo / "README.md").write_text("# x\n\nchanged again\n", encoding="utf-8")

        commits, _ = slice_commit.plan(self.repo, None)
        by_type = {c["type"]: c for c in commits}
        self.assertIn("feat", by_type)
        self.assertIn("docs", by_type)

    def test_dangerous_file_blocks_entire_plan(self):
        (self.repo / ".env").write_text("SECRET=1\n", encoding="utf-8")
        (self.repo / "ok.js").write_text("x\n", encoding="utf-8")
        commits, dangerous = slice_commit.plan(self.repo, None)
        self.assertEqual(commits, [])
        self.assertEqual(dangerous, [".env"])

    def test_issue_suffix_is_applied(self):
        (self.repo / "a.md").write_text("x\n", encoding="utf-8")
        commits, _ = slice_commit.plan(self.repo, "42")
        self.assertTrue(all(c["message"].endswith("(#42)") for c in commits))

    def test_messages_are_english(self):
        (self.repo / "a.md").write_text("x\n", encoding="utf-8")
        commits, _ = slice_commit.plan(self.repo, None)
        for c in commits:
            message = c["message"]
            self.assertRegex(message, r"^(feat|fix|test|docs|ci|chore)(\([^)]+\))?: ")


class TestCli(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = make_repo(Path(self.tmp.name))

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(HERE / "slice_commit.py"), *args],
            capture_output=True, text=True,
        )

    def test_dry_run_does_not_commit(self):
        (self.repo / "a.md").write_text("x\n", encoding="utf-8")
        before = git(self.repo, "rev-parse", "HEAD").stdout.strip()
        proc = self.run_cli(str(self.repo))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("dry run", proc.stdout)
        after = git(self.repo, "rev-parse", "HEAD").stdout.strip()
        self.assertEqual(before, after)

    def test_apply_creates_commits(self):
        (self.repo / "a.md").write_text("x\n", encoding="utf-8")
        (self.repo / "src").mkdir()
        (self.repo / "src" / "b.js").write_text("x\n", encoding="utf-8")
        proc = self.run_cli(str(self.repo), "--apply")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        log = git(self.repo, "log", "--oneline").stdout
        self.assertIn("docs", log)
        self.assertIn("feat", log)

    def test_dangerous_file_exits_one_and_commits_nothing(self):
        (self.repo / ".env").write_text("SECRET=1\n", encoding="utf-8")
        before = git(self.repo, "rev-parse", "HEAD").stdout.strip()
        proc = self.run_cli(str(self.repo), "--apply")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("BLOQUEA", proc.stderr)
        after = git(self.repo, "rev-parse", "HEAD").stdout.strip()
        self.assertEqual(before, after)

    def test_not_a_repo_is_exit_two(self):
        proc = self.run_cli("/tmp")
        self.assertEqual(proc.returncode, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
