"""Tests para scripts/session-handoff.py (A+C: historial + indice de sesiones).

Contexto (2026-10-13): el HANDOFF es last-writer-wins por diseno (es "estado
actual"). Dos cierres sobre el MISMO proyecto perdian el primero. Se agregan:

  - A. backup del HANDOFF previo en `.knowledge/handoff-history/` antes de pisarlo;
  - C. indice append-only `.knowledge/SESSIONS.md` con una linea por cierre.

Lo que se prueba es el CONTRATO observable en disco, siempre sobre un tmp_path
(nunca el workspace real):

  - primer cierre: crea HANDOFF y SESSIONS.md, sin historial;
  - segundo cierre: HANDOFF = el nuevo, historial = el anterior, indice con 2 filas;
  - el indice es append puro: las filas previas nunca se pierden;
  - un HANDOFF ausente no genera backup (no hay nada que preservar).
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS = ROOT / "scripts"
# session-handoff.py hace `from lockutil import file_lock`; lockutil vive en
# scripts/, asi que hay que poner ese directorio en sys.path antes de cargarlo.
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location(
    "session_handoff", SCRIPTS / "session-handoff.py"
)
session_handoff = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(session_handoff)


def _close(handoff_dir, summary, ts):
    """Ejecuta el cierre en `handoff_dir` con un timestamp fijo (determinista)."""
    target = Path(handoff_dir) / "HANDOFF.md"
    with session_handoff.file_lock(target):
        existed = target.exists()
        backup = session_handoff.backup_previous(target, ts) if existed else None
        index = session_handoff.append_session_index(target, "workspace", ts, summary)
        tmp = target.with_suffix(".md.tmp")
        tmp.write_text(session_handoff.build_handoff(_Args(summary)), encoding="utf-8")
        import os

        os.replace(tmp, target)
    return backup, index


class _Args:
    """Minimo de args que build_handoff consume."""

    def __init__(self, summary):
        self.date = "2026-10-13"
        self.branch = "main"
        self.repo = "https://github.com/gonzoblasco/workspace_openclaw"
        self.summary = summary
        self.status = ""
        self.next_steps = ""
        self.decisions = ""
        self.files = ""
        self.project = "workspace"

    def __getattr__(self, name):  # pragma: no cover - solo por robustez
        return ""


def test_first_close_creates_handoff_and_index_without_history(tmp_path):
    k = tmp_path / ".knowledge"
    k.mkdir()
    backup, _ = _close(k, "Primera sesion", "2026-10-13 10:00")

    assert backup is None, "sin HANDOFF previo no debe haber backup"
    assert (k / "HANDOFF.md").exists()
    assert (k / "SESSIONS.md").exists()
    assert not (k / "handoff-history").exists()


def test_second_close_preserves_first_in_history_and_index(tmp_path):
    k = tmp_path / ".knowledge"
    k.mkdir()
    _close(k, "Primera sesion", "2026-10-13 10:00")
    backup, _ = _close(k, "Segunda sesion", "2026-10-13 11:00")

    # A: el HANDOFF anterior quedo archivado, no perdido.
    assert backup is not None and backup.exists()
    assert "Primera sesion" in backup.read_text(encoding="utf-8")
    # HANDOFF actual = el nuevo (last-writer-wins se mantiene).
    assert "Segunda sesion" in (k / "HANDOFF.md").read_text(encoding="utf-8")
    # C: el indice acumula las dos sesiones, sin pisar la primera.
    index = (k / "SESSIONS.md").read_text(encoding="utf-8")
    assert "Primera sesion" in index
    assert "Segunda sesion" in index
    assert index.count("- **") == 2


def test_index_is_append_only(tmp_path):
    k = tmp_path / ".knowledge"
    k.mkdir()
    for i in range(5):
        _close(k, f"Sesion {i}", f"2026-10-13 1{i}:00")
    index = (k / "SESSIONS.md").read_text(encoding="utf-8")
    # Ninguna fila previa se pierde: append puro.
    for i in range(5):
        assert f"Sesion {i}" in index
    assert index.count("- **") == 5


# ---------------------------------------------------------------------------
# Resolucion del destino (2026-11-03): el sujeto no siempre vive en projects/.
# Antes de este fix, un slug de `forks/` o `_workbench/` resolvia a
# `projects/<slug>/.knowledge/`, el script creaba ese arbol inexistente y el
# HANDOFF real quedaba sin actualizar, sin ningun error visible.
# ---------------------------------------------------------------------------
def _fake_workspace(tmp_path, monkeypatch, layout):
    """Arma un workspace descartable con la estructura dada y apunta el modulo.

    `layout` es un dict {contenedor: [nombres de carpeta]}.
    """
    for container, names in layout.items():
        root = tmp_path / container
        root.mkdir(parents=True, exist_ok=True)
        for name in names:
            (root / name).mkdir()
    monkeypatch.setattr(session_handoff, "WORKSPACE", tmp_path)
    return tmp_path


def test_resolve_encuentra_proyecto_en_projects(tmp_path, monkeypatch):
    _fake_workspace(tmp_path, monkeypatch, {"projects": ["alfa", "beta"]})
    path = session_handoff.resolve_handoff_path("alfa", None)

    assert path == tmp_path / "projects" / "alfa" / ".knowledge" / "HANDOFF.md"


def test_resolve_encuentra_fork_fuera_de_projects(tmp_path, monkeypatch):
    _fake_workspace(tmp_path, monkeypatch, {"projects": [], "forks": ["vane"]})
    path = session_handoff.resolve_handoff_path("vane", None)

    assert path == tmp_path / "forks" / "vane" / ".knowledge" / "HANDOFF.md"
    # El bug: no debe inventar projects/vane.
    assert not (tmp_path / "projects" / "vane").exists()


def test_resolve_encuentra_workbench_fuera_de_projects(tmp_path, monkeypatch):
    _fake_workspace(tmp_path, monkeypatch, {"_workbench": ["onwheels"]})
    path = session_handoff.resolve_handoff_path("onwheels", None)

    assert path == tmp_path / "_workbench" / "onwheels" / ".knowledge" / "HANDOFF.md"


def test_resolve_encuentra_clon_fuera_de_projects(tmp_path, monkeypatch):
    _fake_workspace(tmp_path, monkeypatch, {"clones": ["externo"]})
    path = session_handoff.resolve_handoff_path("externo", None)

    assert path == tmp_path / "clones" / "externo" / ".knowledge" / "HANDOFF.md"


def test_resolve_encuentra_contribucion_oss(tmp_path, monkeypatch):
    """Las contribuciones a repos ajenos viven en oss/<owner>-<repo>/."""
    _fake_workspace(tmp_path, monkeypatch, {"oss": ["facebook-astryx"]})
    path = session_handoff.resolve_handoff_path("facebook-astryx", None)

    assert path == tmp_path / "oss" / "facebook-astryx" / ".knowledge" / "HANDOFF.md"


def test_resolve_prefiere_projects_sobre_otros_contenedores(tmp_path, monkeypatch):
    """Si el mismo slug vive en projects/ y en forks/, manda projects/."""
    _fake_workspace(tmp_path, monkeypatch, {"projects": ["gemelo"], "forks": ["gemelo"]})

    try:
        session_handoff.resolve_handoff_path("gemelo", None)
    except ValueError as exc:
        assert "mas de un contenedor" in str(exc)
    else:  # pragma: no cover - el contrato es fallar, no elegir
        raise AssertionError("un slug ambiguo debe fallar en vez de adivinar")


def test_resolve_carpeta_con_espacio_final(tmp_path, monkeypatch):
    """Un directorio que termina en espacio ('OSS ') tiene que resolverse."""
    ws = _fake_workspace(tmp_path, monkeypatch, {"projects": ["OSS ", "otro"]})
    path = session_handoff.resolve_handoff_path("OSS ", None)

    assert path == ws / "projects" / "OSS " / ".knowledge" / "HANDOFF.md"


def test_resolve_sin_carpeta_cae_al_comportamiento_historico(tmp_path, monkeypatch):
    """Un slug sin carpeta todavia sigue apuntando a projects/<slug>."""
    _fake_workspace(tmp_path, monkeypatch, {"projects": []})
    path = session_handoff.resolve_handoff_path("todavia-no-existe", None)

    assert path == tmp_path / "projects" / "todavia-no-existe" / ".knowledge" / "HANDOFF.md"


def test_resolve_override_gana_sobre_la_busqueda(tmp_path, monkeypatch):
    _fake_workspace(tmp_path, monkeypatch, {"forks": ["vane"]})
    custom = tmp_path / "elegido"
    path = session_handoff.resolve_handoff_path("vane", str(custom))

    assert path == custom / "HANDOFF.md"


def test_resolve_alias_de_workspace_sigue_yendo_al_global(tmp_path, monkeypatch):
    _fake_workspace(tmp_path, monkeypatch, {"projects": ["workspace"]})
    path = session_handoff.resolve_handoff_path("workspace", None)

    assert path == tmp_path / ".knowledge" / "HANDOFF.md"


# ---------------------------------------------------------------------------
# Guarda de traversal (2026-11-03): un slug con barras creaba un arbol anidado.
# El 2026-10-29 quedo `projects/OSS / astryx (meta/astryx #3335)/.knowledge/`
# porque el cierre recibio el titulo de la sesion como si fuera un slug.
# ---------------------------------------------------------------------------
def test_resolve_rechaza_slug_con_barras(tmp_path, monkeypatch):
    _fake_workspace(tmp_path, monkeypatch, {"projects": []})

    try:
        session_handoff.resolve_handoff_path("OSS / astryx (meta/astryx #3335)", None)
    except ValueError as exc:
        assert "separadores" in str(exc)
    else:  # pragma: no cover - el contrato es fallar
        raise AssertionError("un slug con barras debe rechazarse, no crear el arbol")


def test_resolve_rechaza_dot_dot(tmp_path, monkeypatch):
    _fake_workspace(tmp_path, monkeypatch, {"projects": []})

    for bad in ("../fuera", "..", "."):
        try:
            session_handoff.resolve_handoff_path(bad, None)
        except ValueError:
            continue
        raise AssertionError(f"el slug {bad!r} debe rechazarse")


def test_resolve_rechaza_override_fuera_del_workspace(tmp_path, monkeypatch):
    _fake_workspace(tmp_path, monkeypatch, {"projects": []})
    fuera = tmp_path.parent / "afuera"

    try:
        session_handoff.resolve_handoff_path("alfa", str(fuera))
    except ValueError as exc:
        assert "fuera del workspace" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("--handoff-dir fuera del workspace debe rechazarse")


def test_resolve_slug_astryx_ahora_es_carpeta_real(tmp_path, monkeypatch):
    """El proyecto rescatado el 2026-11-03 vive en projects/astryx."""
    ws = _fake_workspace(tmp_path, monkeypatch, {"projects": ["astryx"]})
    path = session_handoff.resolve_handoff_path("astryx", None)

    assert path == ws / "projects" / "astryx" / ".knowledge" / "HANDOFF.md"
