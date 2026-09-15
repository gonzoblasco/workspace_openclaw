"""Tests for scripts/check-prompts.py (versioned prompts validator)."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CHECKER = ROOT / "scripts" / "check-prompts.py"


def run_checker(tmp_path, files):
    """Write the given {name: content} files under a fake prompts/ dir and
    run the checker against it by monkeypatching its PROMPTS path."""
    for name, content in files.items():
        (tmp_path / name).write_text(content, encoding="utf-8")
    # We drive the checker's logic by importing it and pointing PROMPTS at tmp_path.
    import importlib.util

    spec = importlib.util.spec_from_file_location("check_prompts", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.PROMPTS = tmp_path
    return mod, mod.main()


def valid_prompt(slug, version="1", scope="workspace", tags='["a"]'):
    return (
        "---\n"
        f"id: {slug}\n"
        f"version: {version}\n"
        f"scope: {scope}\n"
        f"tags: {tags}\n"
        "---\n\n# body\n\nsome prompt\n"
    )


def test_valid_prompt_passes(tmp_path):
    mod, rc = run_checker(tmp_path, {"sample.md": valid_prompt("sample")})
    assert rc == 0


def test_id_must_match_filename(tmp_path):
    mod, rc = run_checker(tmp_path, {"sample.md": valid_prompt("other")})
    assert rc == 1


def test_version_must_be_positive_integer(tmp_path):
    mod, rc = run_checker(tmp_path, {"sample.md": valid_prompt("sample", version="0")})
    assert rc == 1
    mod, rc = run_checker(tmp_path, {"sample.md": valid_prompt("sample", version="abc")})
    assert rc == 1


def test_scope_must_be_allowed(tmp_path):
    mod, rc = run_checker(tmp_path, {"sample.md": valid_prompt("sample", scope="nope")})
    assert rc == 1


def test_tags_may_not_be_empty(tmp_path):
    mod, rc = run_checker(tmp_path, {"sample.md": valid_prompt("sample", tags="[]")})
    assert rc == 1


def test_missing_frontmatter_fails(tmp_path):
    mod, rc = run_checker(tmp_path, {"sample.md": "# no frontmatter\n\nbody\n"})
    assert rc == 1


def test_duplicate_ids_fail(tmp_path):
    files = {
        "a.md": valid_prompt("shared"),
        "b.md": valid_prompt("shared"),
    }
    mod, rc = run_checker(tmp_path, files)
    assert rc == 1


def test_empty_prompts_dir_is_ok(tmp_path):
    mod, rc = run_checker(tmp_path, {})
    assert rc == 0


def test_real_prompts_dir_passes():
    """The real prompts/ must always pass the validator."""
    code = subprocess.run([sys.executable, str(CHECKER)], cwd=ROOT, capture_output=True, text=True)
    assert code.returncode == 0, code.stdout + code.stderr
