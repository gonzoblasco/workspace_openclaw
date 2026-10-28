"""Tests for scripts/check-adr-supersede.py (grafo de supersede del corpus de ADRs).

El checker existe porque el corpus acumulo "datos pisados": un ADR que declara
superseder a otro, con el superseded todavia diciendo "Aceptado" en su cabecera
(casos testigo: ADR-075 y ADR-006, cuya nota de supersede vivia en un sidecar
`.appendix` que nadie lee).

Propiedades criticas:
  - detectar el superseded sin marca en su ESTADO (no alcanza un bloque en el cuerpo);
  - la DIRECCION: la marca se le exige al reemplazado, no al que reemplaza (un grafo
    invertido flaguearia al equivocado);
  - el supersede PARCIAL (una seccion) no exige marca;
  - detectar sidecars invisibles (un archivo no-.md en docs/adr/).

Cada test SIEMBRA el defecto en un corpus falso en tmp_path: un chequeo que solo
corre contra el corpus real limpio no esta probado (puede reportar OK sin mirar).
"""
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CHECKER = ROOT / "scripts" / "check-adr-supersede.py"


def load():
    spec = importlib.util.spec_from_file_location("check_adr_supersede", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_adr(adr_dir, num, body, archived=None):
    """Siembra un ADR en el vault falso.

    `archived=None` deriva el sufijo del cuerpo, para que los tests que no
    hablan del nombre no tengan que declararlo. Un test que SIEMBRA el defecto
    del nombre pasa `archived` explicito.
    """
    if archived is None:
        m = re.search(r"^\*\*(?:Estado|Status):\*\*\s*(.+)$", body, re.M)
        accepted = bool(m) and bool(re.match(r"^\s*(aceptado|accepted)\b", m.group(1), re.I))
        archived = not accepted
    stem = f"ADR-{num:03d}-test-{num}"
    if archived:
        stem += "-archived"
    p = adr_dir / f"{stem}.md"
    p.write_text(body, encoding="utf-8")
    return p


def build_vault(tmp_path):
    adr = tmp_path / "adr"
    adr.mkdir(exist_ok=True)
    return adr


# --- el caso limpio: no inventa violaciones ---

def test_clean_corpus_has_no_violations(tmp_path):
    mod = load()
    adr = build_vault(tmp_path)
    write_adr(adr, 1, "**Estado:** Aceptado\n")
    write_adr(adr, 2, "**Estado:** Aceptado\n**Supersede:** ADR-003\n")
    write_adr(adr, 3, "**Estado:** Superseded por ADR-002\n")
    assert mod.find_violations(adr) == []


# --- la causa raiz: superseded sin marca en su estado ---

def test_detects_superseded_without_status_mark(tmp_path):
    """ADR-002 supersede a ADR-001, pero ADR-001 sigue 'Aceptado'."""
    mod = load()
    adr = build_vault(tmp_path)
    write_adr(adr, 1, "**Estado:** Aceptado\n")
    write_adr(adr, 2, "**Estado:** Aceptado\n**Supersede:** ADR-001\n")
    v = mod.find_violations(adr)
    assert any("el estado de ADR-001" in x for x in v), v


def test_body_marker_does_not_excuse_a_lying_header(tmp_path):
    """Un bloque `> SUPERSEDED` enterrado NO alcanza: la cabecera sigue mintiendo.

    Es el caso de ADR-075: el cuerpo decia SUPERSEDED pero el estado decia
    'Aceptado'. El estado es lo primero que se lee; es el contrato. Aca el
    superseder (002) lo declara en su header, asi que la relacion se conoce y la
    marca se le exige a 001.
    """
    mod = load()
    adr = build_vault(tmp_path)
    write_adr(adr, 1, "**Estado:** Aceptado\n\n## Notas\n> SUPERSEDED por ADR-002\n")
    write_adr(adr, 2, "**Estado:** Aceptado\n**Supersede:** ADR-001\n")
    v = mod.find_violations(adr)
    assert any("el estado de ADR-001" in x for x in v), v


# --- DIRECCION: la marca se le exige al reemplazado, no al que reemplaza ---

def test_direction_flags_the_superseded_not_the_superseder(tmp_path):
    """`**Supersede:** ADR-001` en 002 => 002 reemplaza a 001.

    La marca falta en 001 (el reemplazado). Si el grafo se invirtiera, el flagged
    seria 002. La asercion sobre 'el estado de ADR-001' fija la direccion.
    """
    mod = load()
    adr = build_vault(tmp_path)
    write_adr(adr, 1, "**Status:** Accepted\n")
    write_adr(adr, 2, "**Estado:** Aceptado\n**Supersede:** ADR-001\n")
    v = mod.find_violations(adr)
    assert len(v) == 1, v
    assert "el estado de ADR-001" in v[0], v


# --- parcialidad: un supersede parcial no exige marca ---

def test_partial_supersede_does_not_require_mark(tmp_path):
    """ADR-053 supersede una SECCION de ADR-040; ADR-040 sigue gobernando lo demas.

    Si el guard exigiera marca aca, flagguearia ADR-040 (que en el corpus real esta
    'Accepted' a proposito: solo su tabla de thinking quedo superseded).
    """
    mod = load()
    adr = build_vault(tmp_path)
    write_adr(adr, 40, "**Status:** Accepted\n")
    write_adr(adr, 53, "**Estado:** Aceptado\n**Supersede:** la seccion de thinking de ADR-040\n")
    assert mod.find_violations(adr) == []


# --- segunda regla: sidecars invisibles ---

def test_detects_sidecar(tmp_path):
    """Un archivo no-.md en docs/adr/ es invisible para todo lector y guard."""
    mod = load()
    adr = build_vault(tmp_path)
    write_adr(adr, 1, "**Estado:** Aceptado\n")
    (adr / "ADR-001-test-1.md.appendix").write_text("nota escondida\n", encoding="utf-8")
    v = mod.find_violations(adr)
    assert any("sidecar" in x for x in v), v


# --- el campo generico `Relacionado` que declara un reemplazo TOTAL ---
# Verificado 2026-10-12: dos supersedes totales vivian SOLO en `Relacionado` y el
# guard los ignoraba (ADR-098 -> ADR-075 y ADR-091 -> ADR-068).

def test_relacionado_declares_total_replacement(tmp_path):
    """`**Relacionado:** ADR-001 (superseded)` es una relacion total: exige marca.

    Es el caso ADR-098/ADR-091: el reemplazo se declara en el campo generico con la
    señal en el parentesis, y el reemplazado (001) sigue 'Aceptado'.
    """
    mod = load()
    adr = build_vault(tmp_path)
    write_adr(adr, 1, "**Estado:** Aceptado\n")
    write_adr(adr, 2, "**Estado:** Aceptado\n**Relacionado:** ADR-001 (superseded), ADR-003\n")
    v = mod.find_violations(adr)
    assert any("el estado de ADR-001" in x for x in v), v


def test_relacionado_partial_does_not_require_mark(tmp_path):
    """Un `Relacionado` con señal de PARCIALIDAD no exige marca en el target.

    Es el caso ADR-056 -> ADR-084 ("reemplaza la lista de directorios historicos"):
    reemplaza una practica, no la decision entera.
    """
    mod = load()
    adr = build_vault(tmp_path)
    write_adr(adr, 1, "**Estado:** Aceptado\n")
    write_adr(
        adr, 2,
        "**Estado:** Aceptado\n**Relacionado:** ADR-001 (reemplaza la lista de directorios historicos)\n",
    )
    assert mod.find_violations(adr) == []


def test_relacionado_without_signal_is_ignored(tmp_path):
    """Un `Relacionado` sin señal de reemplazo es navegacion, no supersede."""
    mod = load()
    adr = build_vault(tmp_path)
    write_adr(adr, 1, "**Estado:** Aceptado\n")
    write_adr(adr, 2, "**Estado:** Aceptado\n**Relacionado:** ADR-001 (motor del pipeline)\n")
    assert mod.find_violations(adr) == []


def test_relacionado_generic_context_without_parens_ignored(tmp_path):
    """La señal tiene que estar en el CONTEXTO del citado, no en cualquier parte.

    Un `Relacionado` con la palabra "superseded" en otro item no convierte a todos
    los citados en superseded.
    """
    mod = load()
    adr = build_vault(tmp_path)
    write_adr(adr, 1, "**Estado:** Aceptado\n")
    write_adr(
        adr, 2,
        "**Estado:** Aceptado\n**Relacionado:** ADR-001 (motor del pipeline), ADR-003 (superseded)\n",
    )
    # ADR-003 no existe en el vault -> lo saltea integrity; ADR-001 no debe flaguearse.
    v = mod.find_violations(adr)
    assert not any("el estado de ADR-001" in x for x in v), v


# --- end-to-end: el script real sobre el corpus real ---

# --- tercera regla: el sufijo `-archived` acompana al estado ---

def test_detects_archived_status_without_suffix(tmp_path):
    """Un ADR superseded que conserva el nombre viejo se lee como vigente en un `ls`."""
    mod = load()
    adr = build_vault(tmp_path)
    write_adr(adr, 1, "**Estado:** Superseded por ADR-002\n", archived=False)
    write_adr(adr, 2, "**Estado:** Aceptado\n")
    v = mod.find_violations(adr)
    assert any("no lleva el sufijo" in x and "ADR-001" in x for x in v), v


def test_detects_suffix_on_an_accepted_adr(tmp_path):
    """La mentira inversa: con sufijo pero Aceptado. Quien lo ve por nombre lo saltea."""
    mod = load()
    adr = build_vault(tmp_path)
    write_adr(adr, 1, "**Estado:** Aceptado\n", archived=True)
    v = mod.find_violations(adr)
    assert any("lleva el sufijo" in x and "ADR-001" in x for x in v), v


def test_archived_suffix_satisfies_the_rule(tmp_path):
    """El contrapeso: estado no-Aceptado CON sufijo no reporta nada."""
    mod = load()
    adr = build_vault(tmp_path)
    write_adr(adr, 1, "**Estado:** Superseded por ADR-002\n", archived=True)
    write_adr(adr, 2, "**Estado:** Aceptado\n")
    assert mod.find_violations(adr) == []


def test_partial_supersede_keeps_its_name(tmp_path):
    """Un `Aceptado` con un apartado superseded sigue gobernando: sin sufijo."""
    mod = load()
    adr = build_vault(tmp_path)
    write_adr(adr, 40, "**Status:** Accepted\n", archived=False)
    write_adr(adr, 53, "**Estado:** Aceptado\n**Supersede:** la seccion de thinking de ADR-040\n")
    assert mod.find_violations(adr) == []


def test_archived_suffix_tolerated_by_integrity():
    """El sufijo no rompe el matcheo del nombre: los guards deben seguir viendo el ADR."""
    spec = importlib.util.spec_from_file_location(
        "check_adr_integrity", ROOT / "scripts" / "check-adr-integrity.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.FILE_RE.match("ADR-102-minimax-m31-flash-motor-core-archived.md")


def test_passes_on_real_corpus():
    r = subprocess.run(
        [sys.executable, str(CHECKER)], cwd=ROOT, capture_output=True, text=True
    )
    assert r.returncode == 0, r.stdout + r.stderr


def test_can_fail(tmp_path):
    """El check PUEDE fallar: se le da el corpus sucio y se exige exit 1."""
    adr = tmp_path / "adr"
    adr.mkdir()
    (adr / "ADR-001-a.md").write_text("**Estado:** Aceptado\n", encoding="utf-8")
    (adr / "ADR-002-b.md").write_text(
        "**Estado:** Aceptado\n**Supersede:** ADR-001\n", encoding="utf-8"
    )
    script_copy = tmp_path / "check-adr-supersede.py"
    script_copy.write_text(CHECKER.read_text(encoding="utf-8"), encoding="utf-8")
    r = subprocess.run(
        [sys.executable, str(script_copy), str(adr)], cwd=ROOT, capture_output=True, text=True
    )
    assert r.returncode == 1, r.stdout + r.stderr
    assert "ADR-001" in r.stdout
