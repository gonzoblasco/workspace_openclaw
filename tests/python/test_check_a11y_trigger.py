"""Tests for scripts/check-a11y-trigger.py - el disparador de validacion manual.

Por que existen: el gate existe porque la skill `a11y-at-validation` define un
boundary (cuando el cambio afecta lo que el screen reader ANUNCIA, la validacion
manual es obligatoria) que vivia solo en la skill, sin respaldo mecanico. El
precedente del workspace es explicito: una regla que dice tener respaldo sin
tenerlo da confianza falsa (el `scripts/pr-thread-brief.sh` que nunca existio,
el guard de contraste que nunca encontraba un par).

Los tests que importan prueban que el gate PUEDE bloquear, que NO bloquea de mas
(un `aria-label` estatico es codigo valido), y que el override es consciente.
"""
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
GATE = ROOT / "scripts" / "check-a11y-trigger.py"


def load():
    spec = importlib.util.spec_from_file_location("check_a11y_trigger", GATE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --- parsing del diff: solo lineas agregadas cuentan ---

DIFF = """diff --git a/x/Widget.tsx b/x/Widget.tsx
index 111..222 100644
--- a/x/Widget.tsx
+++ b/x/Widget.tsx
@@ -1,3 +1,4 @@
 unchanged line
-removed old line
+<div aria-posinset={1} />
 trailing context
"""


def test_parses_added_lines_with_new_numbers():
    mod = load()
    added = mod.added_lines_from_diff(DIFF)
    assert len(added) == 1
    path, no, text = added[0]
    assert path == "x/Widget.tsx"
    assert "aria-posinset" in text
    assert no == 2  # contexto(1) + agregada(2)


def test_removed_lines_are_not_reported():
    """Una linea que se va no es un cambio de esta tarea."""
    mod = load()
    added = mod.added_lines_from_diff(DIFF)
    assert all("removed old line" not in t for _, _, t in added)


# --- clasificacion: bloqueante vs aviso ---

def test_posinset_blocks():
    mod = load()
    blocking, warnings = mod.classify([("a.tsx", 1, '<div aria-posinset={2} />')])
    assert len(blocking) == 1
    assert not warnings


def test_setsize_blocks():
    mod = load()
    blocking, _ = mod.classify([("a.tsx", 1, '<div aria-setsize={5} />')])
    assert len(blocking) == 1


def test_activedescendant_blocks():
    mod = load()
    blocking, _ = mod.classify([("a.tsx", 1, 'aria-activedescendant={id}')])
    assert len(blocking) == 1


def test_live_region_blocks():
    mod = load()
    blocking, _ = mod.classify([("a.tsx", 1, '<div aria-live="polite" />')])
    assert len(blocking) == 1


def test_widget_role_blocks():
    mod = load()
    blocking, _ = mod.classify([("a.tsx", 1, '<div role="listbox" />')])
    assert len(blocking) == 1


def test_static_aria_label_only_warns():
    """No bloquear de mas: un label estatico es codigo valido."""
    mod = load()
    blocking, warnings = mod.classify([("a.tsx", 1, '<button aria-label="Close" />')])
    assert not blocking
    assert len(warnings) == 1


def test_no_duplicate_when_line_matches_both_levels():
    """Una linea que matchea bloqueo no aparece tambien como aviso."""
    mod = load()
    blocking, warnings = mod.classify([("a.tsx", 1, '<div role="listbox" aria-label="x" />')])
    assert len(blocking) == 1
    assert not warnings


# --- end-to-end: sin nada staged no hay nada que disparar ---

def test_clean_tree_passes():
    """Sin cambios de UI que disparar, el gate pasa.

    Hermetico a proposito: se corre con un rango vacio (HEAD..HEAD) en vez del
    staging ambiente. El modo staged leia lo que hubiera en el indice, asi que
    cualquier cosa staged rompia este test - una barrera que dependia del estado
    ambiente del que la corria (encontrado 2026-10-07, con las skills de auditor
    staged).
    """
    r = subprocess.run(
        [sys.executable, str(GATE), "--range", "HEAD..HEAD"],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr


def test_override_recognizes_trigger():
    """A11Y_VALIDATED=1 debe reconocer el disparo, no desactivar el gate."""
    env = dict(os.environ, A11Y_VALIDATED="1")
    r = subprocess.run(
        [sys.executable, str(GATE)], cwd=ROOT, capture_output=True, text=True, env=env
    )
    assert r.returncode == 0, r.stdout + r.stderr


# --- modo --range: la barrera de CI, donde no hay diff staged ---

def test_parse_range_reads_both_forms():
    mod = load()
    assert mod.parse_range(["--range", "origin/main..HEAD"]) == "origin/main..HEAD"
    assert mod.parse_range(["--range=main..HEAD"]) == "main..HEAD"
    assert mod.parse_range(["a.tsx"]) is None


def test_range_without_value_is_usage_error():
    """`--range` sin valor no puede caer al modo staged en silencio."""
    r = subprocess.run(
        [sys.executable, str(GATE), "--range"], cwd=ROOT, capture_output=True, text=True
    )
    assert r.returncode == 2
    assert "--range" in r.stdout


def test_unresolvable_range_fails_loudly():
    """Un rango roto en CI no debe pasar en silencio: seria una barrera apagada."""
    r = subprocess.run(
        [sys.executable, str(GATE), "--range", "no-existe-xyz..HEAD"],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert r.returncode == 1
    assert "no pude resolver" in r.stdout


# --- filtro por superficie: solo lo que RENDERIZA puede cambiar un anuncio ---
#
# El gate encontro sus dos falsos positivos solo: al commitear su propio test y
# su propio script, se bloqueo a si mismo. Los patrones de ARIA viven como
# literales en ambos. Sin este filtro el gate seria inusable: dispararia sobre
# cualquier archivo que mencione ARIA, incluido el mismo.

def test_ui_extensions_are_scanned():
    mod = load()
    for p in ("src/Widget.tsx", "src/a.jsx", "a.ts", "b.html", "c.vue", "d.svelte"):
        assert not mod.is_skipped_path(p), p


def test_non_ui_files_are_skipped():
    """Un doc, un script o un JSON no renderizan: no pueden cambiar un anuncio."""
    mod = load()
    for p in ("docs/x.md", "scripts/check-a11y-trigger.py", "data.json", "notes.txt"):
        assert mod.is_skipped_path(p), p


def test_tests_are_skipped():
    """Los tests no se embarcan y contienen los patrones como data de prueba."""
    mod = load()
    assert mod.is_skipped_path("tests/python/test_check_a11y_trigger.py")


def test_nested_role_tests_are_skipped():
    """Regresion 2026-10-07: `tests/` a cualquier profundidad, no solo la raiz.

    Los arboles de rol viven en agents/<rol>/skills/<skill>/tests/. El filtro
    por prefijo no los alcanzaba y el gate bloqueaba sobre fixtures HTML que no
    se embarcan.
    """
    mod = load()
    for p in (
        "agents/kanam-auditor/skills/accessibility-oracle/tests/fixtures/accessible.html",
        "agents/kanam-critic/tests/evidence-hunter/sandbox/page.html",
        "skills/foo/tests/a.tsx",
    ):
        assert mod.is_skipped_path(p), p


def test_non_test_html_is_still_scanned():
    """El arreglo no debe volver ciego al gate: una app real sigue disparando."""
    mod = load()
    for p in (
        "src/app/page.tsx",
        "agents/kanam-auditor/skills/accessibility-oracle/src/oracle.js",
    ):
        assert not mod.is_skipped_path(p), p


def test_gate_does_not_block_its_own_source():
    """Regresion del falso positivo: el script no se bloquea a si mismo."""
    r = subprocess.run(
        [sys.executable, str(GATE), "scripts/check-a11y-trigger.py"],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
