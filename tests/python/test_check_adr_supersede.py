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


def write_adr(adr_dir, num, body):
    p = adr_dir / f"ADR-{num:03d}-test-{num}.md"
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


# --- end-to-end: el script real sobre el corpus real ---

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
