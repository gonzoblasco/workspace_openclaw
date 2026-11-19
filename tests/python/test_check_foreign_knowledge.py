"""Tests para scripts/check-foreign-knowledge.py (guarda de .knowledge ajeno).

Contexto (2026-11-03, pedido de Gonzo): *"nunca subir el .knowledge a los repos
OSS... El tema es no ensuciar lo ajeno."*

El riesgo medido: un fork con 9 archivos `.knowledge/` trackeados y un remote
`upstream` al repo del tercero. No estaban en upstream (0 archivos), pero nada
impedia que un `git push upstream` los subiera - y el diff del PR los muestra
igual aunque el push vaya a nuestro fork.

Lo que se prueba, siempre sobre repos descartables en tmp_path:
  - un repo de terceros con `.knowledge/` trackeado y remote ajeno = riesgo;
  - el hook se instala y es ejecutable;
  - el hook RECHAZA el push de una rama que contiene `.knowledge/` a un remote
    ajeno, y PERMITE el mismo push a un remote de gonzoblasco;
  - un repo sin `.knowledge/` trackeado no requiere hook (no hay nada que filtrar).
"""
import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

SPEC = importlib.util.spec_from_file_location(
    "check_foreign_knowledge", SCRIPTS / "check-foreign-knowledge.py"
)
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


def _git(cwd, *args):
    return subprocess.run(
        ["git", *args], cwd=str(cwd), capture_output=True, text=True, check=False
    )


def _repo(path: Path, with_knowledge: bool = True, remotes=()):
    """Crea un repo con commit inicial y los remotes pedidos."""
    path.mkdir(parents=True, exist_ok=True)
    _git(path, "init", "-q")
    _git(path, "config", "user.email", "t@t")
    _git(path, "config", "user.name", "t")
    (path / "code.txt").write_text("x", encoding="utf-8")
    if with_knowledge:
        k = path / ".knowledge"
        k.mkdir()
        (k / "HANDOFF.md").write_text("memoria local", encoding="utf-8")
    _git(path, "add", "-A")
    _git(path, "commit", "-qm", "init")
    for name, url in remotes:
        _git(path, "remote", "add", name, url)
    return path


def _bare(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    _git(path.parent, "init", "-q", "--bare", str(path))
    return path


def _workspace(tmp_path, monkeypatch, layout, with_knowledge: bool = True):
    for container, names in layout.items():
        root = tmp_path / container
        root.mkdir(parents=True, exist_ok=True)
        for name in names:
            _repo(root / name, with_knowledge=with_knowledge)
    monkeypatch.setattr(guard, "WORKSPACE", tmp_path)
    return tmp_path


def test_detecta_riesgo_cuando_hay_knowledge_y_remote_ajeno(tmp_path, monkeypatch):
    # Nombre fuera de EXEMPT: `vane` se deja tal cual por decision de Gonzo.
    ws = _workspace(tmp_path, monkeypatch, {"forks": ["tanstack-router"]})
    repo = ws / "forks" / "tanstack-router"
    _git(repo, "remote", "add", "upstream", "https://github.com/ItzCrazyKns/Vane")
    _git(repo, "remote", "add", "origin", "https://github.com/gonzoblasco/tanstack-router.git")

    results = guard.scan()

    assert len(results) == 1
    r = results[0]
    assert r["at_risk"] is True
    assert "upstream" in r["third_party_remotes"]
    assert "origin" not in r["third_party_remotes"]
    assert r["hook"] is False


def test_instala_el_hook_y_lo_deja_ejecutable(tmp_path, monkeypatch):
    ws = _workspace(tmp_path, monkeypatch, {"clones": ["ajeno"]})
    hook = guard.install_hook(ws / "clones" / "ajeno")

    assert hook.exists()
    assert os.access(hook, os.X_OK)
    assert guard.HOOK_MARKER in hook.read_text(encoding="utf-8")


def test_sin_knowledge_trackeado_no_hay_riesgo(tmp_path, monkeypatch):
    ws = _workspace(tmp_path, monkeypatch, {"forks": ["limpio"]}, with_knowledge=False)
    _git(ws / "forks" / "limpio", "remote", "add", "upstream", "https://github.com/x/y")

    r = guard.scan()[0]

    assert r["tracked_knowledge"] == []
    assert r["at_risk"] is False


def _run_hook(repo: Path, remote_name: str, remote_url: str, refs: str = ""):
    """Ejecuta el pre-push instalado, como lo haria git.

    git le pasa dos argumentos (nombre y URL del remote) y las refs por stdin.
    Invocarlo directo prueba el contrato sin depender de la red ni de
    `insteadOf` (que en un push real reescribe la URL antes del hook).
    """
    hook = repo / ".git" / "hooks" / "pre-push"
    if not refs:
        head = _git(repo, "rev-parse", "HEAD").stdout.strip()
        refs = f"refs/heads/main {head} refs/heads/main {guard.ZERO_SHA}\n"
    return subprocess.run(
        ["sh", str(hook), remote_name, remote_url],
        cwd=str(repo),
        input=refs,
        capture_output=True,
        text=True,
        check=False,
    )


def test_hook_rechaza_push_a_remote_ajeno(tmp_path):
    """El contrato real: el pre-push falla si la rama trae .knowledge."""
    repo = _repo(tmp_path / "vane")
    guard.install_hook(repo)

    res = _run_hook(repo, "upstream", "https://github.com/ItzCrazyKns/Vane.git")

    assert res.returncode != 0, "el push a un repo ajeno debe rechazarse"
    assert "rechazado" in res.stderr.lower()


def test_hook_rechaza_forma_ssh_de_un_remote_ajeno(tmp_path):
    repo = _repo(tmp_path / "vane")
    guard.install_hook(repo)

    res = _run_hook(repo, "upstream", "git@github.com:ItzCrazyKns/Vane.git")

    assert res.returncode != 0
    assert "rechazado" in res.stderr.lower()


def test_hook_permite_push_a_remote_propio(tmp_path):
    repo = _repo(tmp_path / "vane")
    guard.install_hook(repo)

    for url in (
        "https://github.com/gonzoblasco/vane.git",
        "git@github.com:gonzoblasco/vane.git",
    ):
        res = _run_hook(repo, "origin", url)
        assert res.returncode == 0, f"{url}: {res.stderr}"


def test_hook_deja_pasar_rama_sin_knowledge_aunque_sea_ajena(tmp_path):
    """No hay nada que filtrar: el hook no bloquea por bloquear."""
    repo = _repo(tmp_path / "limpio", with_knowledge=False)
    guard.install_hook(repo)

    res = _run_hook(repo, "upstream", "https://github.com/ItzCrazyKns/Vane.git")

    assert res.returncode == 0, res.stderr


def test_scan_ignora_projects(tmp_path, monkeypatch):
    """`projects/` son repos nuestros: ahi el .knowledge/ es el proyecto."""
    _workspace(tmp_path, monkeypatch, {"projects": ["propio"]})

    assert guard.scan() == []


# ---------------------------------------------------------------------------
# El riesgo real es el INDICE, no el remote (aclaracion de Gonzo, 2026-11-03).
# Un PR sale del fork: si `.knowledge/` esta commiteado ahi, entra al diff que
# revisa el maintainer aunque el push vaya a nuestro propio fork. El hook del
# pre-push no alcanza; hace falta sacarlo del indice.
# ---------------------------------------------------------------------------
def test_detecta_knowledge_trackeado_aunque_el_remote_sea_nuestro(tmp_path, monkeypatch):
    ws = _workspace(tmp_path, monkeypatch, {"forks": ["mi-fork"]})
    repo = ws / "forks" / "mi-fork"
    _git(repo, "remote", "add", "origin", "https://github.com/gonzoblasco/mi-fork.git")

    r = guard.scan()[0]

    # El remote es nuestro, pero el .knowledge/ esta en el indice: viaja en el PR.
    assert r["third_party_remotes"] == {}
    assert r["tracked_knowledge"] != []
    assert r["at_risk"] is True
    assert any("trackeados" in p for p in guard._problems(guard.scan()))


def test_untrack_saca_del_indice_y_deja_los_archivos(tmp_path):
    repo = _repo(tmp_path / "fork")
    assert guard.tracked_knowledge(repo) != []

    assert guard.untrack_knowledge(repo) is True

    assert guard.tracked_knowledge(repo) == []
    assert (repo / ".knowledge" / "HANDOFF.md").exists(), "el archivo queda en disco"


def test_add_info_exclude_no_toca_ningun_archivo_versionado(tmp_path):
    """`info/exclude` es privado del clon: el repo ajeno no se ensucia."""
    repo = _repo(tmp_path / "fork")
    antes = _git(repo, "ls-files").stdout

    guard.add_info_exclude(repo)

    assert guard.excluded_knowledge(repo) is True
    # Ni .gitignore nuevo ni archivo trackeado de mas.
    assert _git(repo, "ls-files").stdout == antes
    assert not (repo / ".gitignore").exists()


def test_add_info_exclude_es_idempotente(tmp_path):
    repo = _repo(tmp_path / "fork")
    guard.add_info_exclude(repo)
    guard.add_info_exclude(repo)

    lines = (repo / ".git" / "info" / "exclude").read_text(encoding="utf-8")
    assert lines.count(".knowledge/") == 1


def test_servicio_puede_trackear_knowledge_con_la_guarda(tmp_path, monkeypatch):
    """`services/` es otra cosa que `forks/`: `.knowledge/` es deliberado.

    `vane` estaba en `forks/` y necesitaba una exencion. Una exencion es un olor
    a clasificacion equivocada: el problema era la carpeta, no la regla.
    """
    ws = _workspace(tmp_path, monkeypatch, {"services": ["vane"]})
    repo = ws / "services" / "vane"
    _git(repo, "remote", "add", "origin", "https://github.com/gonzoblasco/vane.git")
    _git(repo, "remote", "add", "upstream", "https://github.com/ItzCrazyKns/Vane")

    r = guard.scan()[0]

    assert r["is_service"] is True
    assert r["tracked_knowledge"] != [], "en un servicio se trackea a proposito"
    # Con la guarda puesta, no hay riesgo.
    guard.install_hook(repo)
    r = guard.scan()[0]
    assert r["at_risk"] is False
    assert guard._problems(guard.scan()) == []


def test_servicio_sin_guarda_si_es_riesgo(tmp_path, monkeypatch):
    """Sin hook, un push al upstream subiria el .knowledge."""
    ws = _workspace(tmp_path, monkeypatch, {"services": ["vane"]})
    repo = ws / "services" / "vane"
    _git(repo, "remote", "add", "upstream", "https://github.com/ItzCrazyKns/Vane")

    r = guard.scan()[0]

    assert r["at_risk"] is True
    assert any("pre-push" in p for p in guard._problems(guard.scan()))


def test_install_no_destrackea_el_knowledge_de_un_servicio(tmp_path, monkeypatch):
    """La excepcion al destrackeo: en services/ el .knowledge se queda."""
    ws = _workspace(tmp_path, monkeypatch, {"services": ["vane"]})
    repo = ws / "services" / "vane"

    guard.install_hook(repo)
    monkeypatch.setattr(guard, "WORKSPACE", ws)
    monkeypatch.setattr("sys.argv", ["x", "--install"])
    guard.main()

    assert guard.tracked_knowledge(repo) != [], "el servicio conserva su memoria"


def test_fork_si_se_destrackea(tmp_path, monkeypatch):
    """La contracara: en un fork se saca del indice."""
    ws = _workspace(tmp_path, monkeypatch, {"forks": ["tanstack"]})
    repo = ws / "forks" / "tanstack"

    assert guard.tracked_knowledge(repo) != []
    monkeypatch.setattr(guard, "WORKSPACE", ws)
    monkeypatch.setattr("sys.argv", ["x", "--install"])
    guard.main()

    assert guard.tracked_knowledge(repo) == []
    assert (repo / ".knowledge" / "HANDOFF.md").exists()


def test_ignora_git_dir_heredado_del_hook(tmp_path, monkeypatch):
    """Un pre-commit exporta GIT_DIR; el check NO debe leer el repo equivocado.

    Medido el 2026-11-19: el check daba OK standalone y fallaba dentro del
    commit, porque `git -C <fork>` no pisa GIT_DIR: leia el `.knowledge/` del
    WORKSPACE y lo reportaba como trackeado en el fork.
    """
    # Workspace con su propio .knowledge trackeado (el "repo padre").
    ws = _workspace(tmp_path, monkeypatch, {"projects": ["propio"]})
    parent = _repo(tmp_path / "parent")
    (parent / ".knowledge").mkdir(exist_ok=True)
    (parent / ".knowledge" / "HANDOFF.md").write_text("x", encoding="utf-8")
    _git(parent, "add", "-A")
    _git(parent, "commit", "-qm", "x")

    # Fork limpio: NO tiene .knowledge propio. (El helper lo agrega por defecto;
    # sin `with_knowledge=False` el test verificaba otra cosa.)
    _workspace(tmp_path, monkeypatch, {"forks": ["limpio"]}, with_knowledge=False)

    # Simular el entorno del hook apuntando al repo padre.
    monkeypatch.setenv("GIT_DIR", str(parent / ".git"))
    monkeypatch.setenv("GIT_WORK_TREE", str(parent))

    r = guard.scan()[0]

    assert r["tracked_knowledge"] == [], "leyo el .knowledge del repo padre"
