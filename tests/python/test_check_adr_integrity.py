"""Tests for scripts/check-adr-integrity.py (corpus de ADRs vs su indice).

El checker existe porque ADR-063 existia y estaba commiteado, pero no tenia fila
en docs/adr/README.md, y nada lo detectaba: check-refs.py valida que las rutas
citadas existan, no que todo ADR este indexado. Se encontro leyendo.

Propiedades criticas: detectar cada una de las cuatro clases de defecto.
Un chequeo que solo se corre contra un corpus limpio NO esta probado: puede
estar reportando OK sin mirar nada. Por eso cada test SIEMBRA el defecto que
el checker debe cazar, en un corpus falso en tmp_path.

Nota de diseño: los tests usan un corpus temporal porque la version anterior
del chequeo se probaba modificando el README real y restaurandolo con git
checkout. Si el test fallaba a mitad, dejaba el indice del workspace roto.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CHECKER = ROOT / "scripts" / "check-adr-integrity.py"


def load():
    spec = importlib.util.spec_from_file_location("check_adr_integrity", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_vault(tmp_path, files, rows, index_name="README.md"):
    """Corpus falso: `files` son nombres de archivo, `rows` filas del indice.

    Una fila puede ser None para OMITIR el numero del indice (ese es el defecto
    que el checker tiene que cazar). El contenido de cada archivo se pasa aparte
    via `bodies`.
    """
    adr = tmp_path / "adr"
    adr.mkdir(exist_ok=True)
    for name in files:
        (adr / name).write_text(f"# {name}\n", encoding="utf-8")
    lines = ["# ADRs", "", "| # | Titulo | Origen |", "|---|---|---|"]
    for num, title, target in rows:
        if target is None:
            continue
        lines.append(f"| ADR-{num:03d} | [{title}]({target}) | workspace |")
    (adr / index_name).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return adr


# --- 1. EN DISCO SIN INDICE (el caso ADR-063, el bug que motivo el script) ---

def test_detects_file_missing_from_index(tmp_path):
    adr = build_vault(
        tmp_path,
        files=["ADR-001-uno.md", "ADR-002-dos.md"],
        rows=[(1, "Uno", "./ADR-001-uno.md")],  # falta la 002
    )
    mod = load()
    errors = mod.find_defects(adr)
    assert any("EN DISCO SIN INDICE" in e and "ADR-002" in e for e in errors), errors


def test_clean_vault_has_no_defects(tmp_path):
    """El contrapeso: si TODO esta indexado, no debe reportar nada."""
    adr = build_vault(
        tmp_path,
        files=["ADR-001-uno.md", "ADR-002-dos.md"],
        rows=[(1, "Uno", "./ADR-001-uno.md"), (2, "Dos", "./ADR-002-dos.md")],
    )
    mod = load()
    assert mod.find_defects(adr) == []


# --- 2. LINK ROTO EN EL INDICE ---

def test_detects_index_row_pointing_nowhere(tmp_path):
    adr = build_vault(
        tmp_path,
        files=["ADR-001-uno.md"],
        rows=[(1, "Uno", "./ADR-001-uno.md"), (2, "Dos", "./ADR-002-no-existe.md")],
    )
    mod = load()
    errors = mod.find_defects(adr)
    assert any("LINK ROTO EN EL INDICE" in e and "ADR-002" in e for e in errors), errors


# --- 3. NUMERO DUPLICADO (dos decisiones con una direccion) ---

def test_detects_duplicate_number(tmp_path):
    adr = build_vault(
        tmp_path,
        files=["ADR-048-ui.md", "ADR-048-stack.md"],
        rows=[(48, "UI", "./ADR-048-ui.md"), (48, "Stack", "./ADR-048-stack.md")],
    )
    mod = load()
    errors = mod.find_defects(adr)
    assert any("NUMERO DUPLICADO ADR-048" in e for e in errors), errors
    # El mensaje debe nombrar AMBOS archivos: con uno solo no se puede arreglar.
    dup = next(e for e in errors if "DUPLICADO" in e)
    assert "ADR-048-ui.md" in dup and "ADR-048-stack.md" in dup


# --- 4. REF CRUZADA ROTA ---

def test_detects_broken_cross_reference(tmp_path):
    adr = build_vault(
        tmp_path,
        files=["ADR-001-uno.md"],
        rows=[(1, "Uno", "./ADR-001-uno.md")],
    )
    # El ADR-001 cita un ADR-999 que no existe.
    (adr / "ADR-001-uno.md").write_text(
        "# ADR-001\n\nRelacionado: ADR-999 (no existe)\n", encoding="utf-8"
    )
    mod = load()
    errors = mod.find_defects(adr)
    assert any("REF CRUZADA ROTA" in e and "ADR-999" in e for e in errors), errors


def test_self_reference_is_not_broken(tmp_path):
    """Un ADR que se cita a si mismo no es una ref rota."""
    adr = build_vault(
        tmp_path,
        files=["ADR-001-uno.md"],
        rows=[(1, "Uno", "./ADR-001-uno.md")],
    )
    (adr / "ADR-001-uno.md").write_text("# ADR-001\n", encoding="utf-8")
    mod = load()
    assert mod.find_defects(adr) == []


# --- el comportamiento end-to-end del script ---

def test_passes_on_real_corpus():
    """El corpus real del workspace debe estar reconciliado."""
    r = subprocess.run(
        [sys.executable, str(CHECKER)], cwd=ROOT, capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr


def test_exit_code_is_1_when_defects_found(tmp_path):
    """El checker debe FALLAR (exit 1) cuando hay un defecto, no solo avisar.

    Se corre el script REAL contra un corpus falso con un defecto sembrado: la
    unica forma de probar que el exit code distingue un corpus roto de uno sano.
    """
    adr = build_vault(
        tmp_path,
        files=["ADR-001-uno.md", "ADR-002-dos.md"],
        rows=[(1, "Uno", "./ADR-001-uno.md")],  # falta la 002
    )
    r = subprocess.run(
        [sys.executable, str(CHECKER), str(adr)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 1, f"esperaba exit 1, dio {r.returncode}: {r.stdout}"
    assert "EN DISCO SIN INDICE" in r.stdout
    assert "ADR-002" in r.stdout


def test_exit_code_is_0_on_clean_corpus(tmp_path):
    """El contrapeso: contra un corpus sano el script NO debe fallar.

    Sin este caso, un checker que siempre devuelve 1 pasaria el test de arriba.
    Los dos juntos prueban que el exit code discrimina.
    """
    adr = build_vault(
        tmp_path,
        files=["ADR-001-uno.md"],
        rows=[(1, "Uno", "./ADR-001-uno.md")],
    )
    r = subprocess.run(
        [sys.executable, str(CHECKER), str(adr)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, f"esperaba exit 0, dio {r.returncode}: {r.stdout}"
