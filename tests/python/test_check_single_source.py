"""Tests for scripts/check-single-source.py (un dato, un dueno).

El checker existe porque el 2026-10-20 Gonzo dijo: "necesitamos definir una unica
fuente de la verdad y no tantos md que pueden chocarse y lo hacen a diario". El
diagnostico real no era la cantidad de markdown: era que ningun archivo tenia
dueno de un dato, y los gates existentes verificaban rutas, no afirmaciones.

Propiedades criticas:
  1. Caza una regla repetida en dos archivos normativos.
  2. NO caza un rotulo corto, un encabezado ni una linea de codigo.
  3. Caza un tag de modelo escrito a mano fuera del bloque managed.
  4. NO caza el tag dentro de un bloque managed (esa es la copia legitima).
  5. NO caza la historia congelada (dailies, ADRs, CHANGELOG).

Un chequeo que solo corre contra un arbol limpio NO esta probado. Cada test
SIEMBRA el defecto en arboles falsos en tmp_path, y el ultimo exige que el check
DISTINGA el caso limpio del sucio.
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CHECKER = ROOT / "scripts" / "check-single-source.py"

REGLA = (
    "- **Regla de prueba:** toda ruta citada en un documento del workspace debe "
    "existir de verdad antes de que alguien confie en ella, sin excepciones."
)


def load():
    spec = importlib.util.spec_from_file_location("check_single_source", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def seed(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


# --- repeticion literal ---

def test_duplicate_rule_across_files_is_caught(tmp_path):
    mod = load()
    seed(tmp_path, "AGENTS.md", REGLA + "\n")
    seed(tmp_path, "MEMORY.md", REGLA + "\n")
    dups = mod.find_duplicates(tmp_path)
    files = {d[0] for d in dups} | {d[2] for d in dups}
    assert files == {"AGENTS.md", "MEMORY.md"}


def test_single_copy_is_clean(tmp_path):
    mod = load()
    seed(tmp_path, "AGENTS.md", REGLA + "\n")
    seed(tmp_path, "MEMORY.md", "- Otra cosa distinta, sin relacion con lo anterior.\n")
    assert mod.find_duplicates(tmp_path) == []


def test_short_label_is_not_a_rule(tmp_path):
    mod = load()
    seed(tmp_path, "AGENTS.md", "- **Modelos:** ver ADR-090.\n")
    seed(tmp_path, "MEMORY.md", "- **Modelos:** ver ADR-090.\n")
    assert mod.find_duplicates(tmp_path) == []


def test_headings_are_not_duplicates(tmp_path):
    # Un titulo es el NOMBRE de la regla, no la regla: repetirlo es como repetir
    # un nombre de archivo. Si esto fallara, cualquier doc que enlace a otro
    # quedaria bloqueado.
    mod = load()
    heading = "## Pausa obligatoria: agentes iteran, revision final, push y borrador"
    seed(tmp_path, "AGENTS.md", heading + "\n")
    seed(tmp_path, "docs/AGENTS-DETALLE.md", heading + "\n")
    assert mod.find_duplicates(tmp_path) == []


def test_paragraph_in_one_file_only_is_not_compared(tmp_path):
    # El gate compara ENTRE archivos, nunca una linea consigo misma.
    mod = load()
    seed(tmp_path, "AGENTS.md", REGLA + "\n")
    assert mod.find_duplicates(tmp_path) == []


# --- tags de modelo ---

def test_manual_model_outside_managed_is_caught(tmp_path):
    mod = load()
    seed(tmp_path, "AGENTS.md", "- Motor: `deepseek-v4.1-flash:cloud` para todo.\n")
    stray = mod.find_stray_models(tmp_path)
    assert len(stray) == 1
    assert stray[0][0] == "AGENTS.md"


def test_model_inside_managed_block_is_allowed(tmp_path):
    mod = load()
    seed(
        tmp_path,
        "AGENTS.md",
        "<!-- BEGIN MANAGED:model-operativo -->\n"
        "- Motor: `deepseek-v4.1-flash:cloud`.\n"
        "<!-- END MANAGED:model-operativo -->\n",
    )
    assert mod.find_stray_models(tmp_path) == []


def test_model_catalog_owner_is_free(tmp_path):
    # SETUP.md declara el catalogo de modelos instalados: es su dato, no una
    # copia de la asignacion por rol.
    mod = load()
    seed(tmp_path, "docs/SETUP.md", "- Local: `gemma4:e4b-mlx`, `qwen3-embedding:0.6b`.\n")
    assert mod.find_stray_models(tmp_path) == []


def test_history_mark_exempts_a_benchmark_line(tmp_path):
    mod = load()
    seed(
        tmp_path,
        "MEMORY.md",
        "- Benchmark 2026-08-30: `gemma4:e4b-mlx` 23s vs el anterior 154s. "
        + mod.HISTORY_MARK
        + "\n",
    )
    assert mod.find_stray_models(tmp_path) == []


def test_historic_dirs_are_not_scanned(tmp_path):
    mod = load()
    seed(tmp_path, "memory/2026-08-30.md", "- Motor: `deepseek-v4-flash:cloud`.\n")
    seed(tmp_path, "docs/adr/ADR-046.md", "- Motor: `deepseek-v4-flash:cloud`.\n")
    assert mod.find_stray_models(tmp_path) == []


# --- el gate distingue limpio de sucio ---

def test_exit_code_distinguishes_clean_from_dirty(tmp_path):
    mod = load()
    seed(tmp_path, "AGENTS.md", "- Unico: nada que repetir en otro archivo del arbol.\n")
    assert mod.main([str(tmp_path)]) == 0

    seed(tmp_path, "MEMORY.md", REGLA + "\n")
    seed(tmp_path, "AGENTS.md", REGLA + "\n")
    assert mod.main([str(tmp_path)]) == 1
