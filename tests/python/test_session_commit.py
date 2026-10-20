"""Tests para scripts/session-commit.sh (commit con pathspec explicito).

Contexto (2026-10-18): un cierre dejo 13 archivos staged y otra sesion se los
llevo en su commit porque `git commit` sin pathspec commitea el indice ENTERO.
El script commitea solo las rutas nombradas, dejando intacto el resto del
indice.

Lo que se prueba, sobre un repo descartable:
  - commitea la ruta nombrada;
  - NO commitea otra ruta que estaba staged (el caso del 18/10);
  - deja ese otro archivo staged, no lo descarta;
  - rechaza invocaciones sin `--` o sin rutas.

Nota: el script vive en el workspace pero opera sobre el cwd. Se copia al repo
de prueba junto con lockutil.py y with-lock.py porque resuelve `./scripts/…`
relativo al cwd.
"""
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"


def _git(repo, *args, check=True):
    return subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, check=check
    )


def _init_repo(tmp_path):
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    for name in ("session-commit.sh", "with-lock.py", "lockutil.py"):
        shutil.copy(SCRIPTS / name, repo / "scripts" / name)
    (repo / "scripts" / "session-commit.sh").chmod(0o755)

    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    for name in ("a.txt", "b.txt"):
        (repo / name).write_text("base\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-qm", "init")
    return repo


def test_commits_only_named_paths(tmp_path):
    """El caso del 2026-10-18: lo staged por otra sesion sobrevive."""
    repo = _init_repo(tmp_path)

    # "sesion A" stagea a.txt
    (repo / "a.txt").write_text("A-change\n")
    _git(repo, "add", "a.txt")

    # "sesion B" modifica b.txt y commitea solo b.txt
    (repo / "b.txt").write_text("B-change\n")
    r = subprocess.run(
        ["./scripts/session-commit.sh", "-m", "B only", "--", "b.txt"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr

    # a.txt NO viajo en el commit
    assert _git(repo, "show", "HEAD:a.txt").stdout == "base\n"
    # y sigue staged para su propia sesion
    staged = _git(repo, "diff", "--cached", "--name-only").stdout.split()
    assert staged == ["a.txt"]


def test_rejects_missing_paths(tmp_path):
    repo = _init_repo(tmp_path)
    r = subprocess.run(
        ["./scripts/session-commit.sh", "-m", "sin rutas"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 2
    assert "--" in r.stderr or "rutas" in r.stderr


def test_rejects_missing_message(tmp_path):
    repo = _init_repo(tmp_path)
    (repo / "a.txt").write_text("x\n")
    r = subprocess.run(
        ["./scripts/session-commit.sh", "--", "a.txt"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 2
