#!/usr/bin/env python3
"""
managed-blocks.py - Propaga settings de la DB a bloques delimitados en archivos.

Patron (fase 3 de kanam-os, ADR-054):

    memory.db (tabla settings)  ->  este generador  ->  bloques en archivos

Los bloques se delimitan con marcadores HTML (no se renderizan en markdown):

    <!-- BEGIN MANAGED:model-triple -->
    ...contenido generado...
    <!-- END MANAGED:model-triple -->

Reglas de seguridad:
- Solo se reescribe el contenido ENTRE marcadores. Todo lo de afuera queda intacto.
- Si falta un marcador, NO se inserta nada: se reporta y se muestra el snippet
  exacto que habria que colocar a mano. Los archivos de identidad no se tocan solos.
- --dry-run muestra el diff sin escribir.
- Idempotente: aplicar dos veces no cambia nada la segunda vez.

Uso:
    managed-blocks.py list                  settings en la DB
    managed-blocks.py seed                  inserta los defaults faltantes
    managed-blocks.py set <key> <value>     cambia un setting
    managed-blocks.py check                 reporta drift, sin escribir
    managed-blocks.py apply [--dry-run]     regenera los bloques
"""

import argparse
import difflib
import re
import sqlite3
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
DB_PATH = WORKSPACE / "memory" / "memory.db"

BEGIN = "<!-- BEGIN MANAGED:{key} -->"
END = "<!-- END MANAGED:{key} -->"

# Valores vigentes al 2026-09-30 (ADR-076). Semilla, no verdad: la DB manda.
DEFAULTS = {
    "model_primary": "deepseek-v4.1-flash:cloud",
    "model_auxiliary": "gemma4:cloud",
    "model_alternative": "glm-5.3-flash:cloud",
    "thinking_default": "high",
    # Motor del pipeline A/B. Distinto del primario: el router lo usa para los
    # agentes de codigo (scripts/model-router.sh, ruta 'default').
    "model_pipeline": "deepseek-v4.1-flash:cloud",
    # Pipeline A/B asimetrico (ADR-077/ADR-088): A ejecuta, B revisa. El CORE
    # spawnea DOS agentes con estos modelos; scripts/check-pipeline-enforcement.py
    # lo verifica contra el codigo real.
    "model_pipeline_a": "gpt-oss:120b-cloud",
    "model_pipeline_b": "deepseek-v4.1-flash:cloud",
    # Distribucion por agente (2026-10-05, ADR-087). Vive en un setting para que
    # el bloque de AGENTS.md la conserve administrada en vez de un resumen generico.
    "model_by_agent": (
        "main/defaults deepseek-v4.1-flash:cloud (fallback glm-5.3-flash) · "
        "dev glm-5.3-flash:cloud (fallback deepseek) · ops glm-5.3-flash:cloud "
        "(fallback deepseek) · auditor nemotron-3-super:cloud (fallback deepseek) · "
        "critic gpt-oss:120b-cloud · planner minimax-m3:cloud · "
        "mind deepseek-v4.1-flash:cloud · studio gemma4:cloud (fallback glm4:9b local)"
    ),
}

# Que bloque vive en que archivo, con que plantilla.
# Agregar una entrada aca es todo lo que hace falta para sumar un bloque nuevo.
REGISTRY = [
    {
        "file": "AGENTS.md",
        "key": "model-triple",
        "template": (
            "- **Distribución por agente (ADR-087):** {model_by_agent}."
        ),
    },
    {
        # El resumen operativo que reciben TODOS los subagentes: es el bloque
        # mas critico, porque ellos no ven docs/SETUP.md ni MEMORY.md.
        "file": "AGENTS.md",
        "key": "model-operativo",
        "template": (
            "- **Modelo por agente:** {model_by_agent}. Por tarea: primario "
            "`{model_primary}`; pipeline A/B: A `{model_pipeline_a}` / B `{model_pipeline_b}`."
        ),
    },
    {
        # Regla del pipeline A/B (ADR-077/ADR-088). En su PROPIO bloque para que
        # el CORE -que lee AGENTS.md siempre, y cuyos subagentes solo reciben
        # AGENTS.md- la tenga a la vista al delegar. La causa de la violacion
        # 2026-10-05 fue operativa: spawnear un solo agente con el default de rol
        # en vez de A y B con los modelos del pacto. Una regla sin enforcement se
        # viola sola (ADR-083); el gate es scripts/check-pipeline-enforcement.py.
        "file": "AGENTS.md",
        "key": "pipeline-ab",
        "template": (
            "- **Pipeline A/B (ADR-077/ADR-088):** al delegar, el CORE spawnea DOS agentes "
            "distintos, nunca uno: **A escribe** con `{model_pipeline_a}` y **B revisa/corrige** "
            "con `{model_pipeline_b}`. Los prompts los redacta el CORE (no el rol). El CORE "
            "verifica el repo, pero su verificacion **NO reemplaza** al revisor B. Fuente de "
            "verdad del modelo: `./scripts/model-router.sh model pipeline_ab`; gate: "
            "`scripts/check-pipeline-enforcement.py`."
        ),
    },
    {
        "file": "docs/SETUP.md",
        "key": "model-triple",
        "template": (
            "- **Modelo de trabajo:** primario `{model_primary}`, "
            "auxiliar `{model_auxiliary}`, alternativo `{model_alternative}`. "
            "Thinking default: **{thinking_default}**."
        ),
    },
    {
        "file": "docs/SETUP.md",
        "key": "model-pipeline-ab",
        "template": (
            "- **Pipeline A/B:** A escribe con `{model_pipeline_a}`; B revisa/corrige con "
            "`{model_pipeline_b}` (ADR-077/ADR-088). Ruta del router: "
            "`scripts/model-router.sh model pipeline_ab`."
        ),
    },
]


def db():
    if not DB_PATH.exists():
        sys.exit(f"Error: no existe la DB en {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute(
        """CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            description TEXT,
            updated_at TEXT
        )"""
    )
    return conn


def get_settings(conn):
    return {k: v for k, v in conn.execute("SELECT key, value FROM settings")}


def cmd_list(conn, _args):
    rows = list(conn.execute("SELECT key, value, COALESCE(updated_at,'-') FROM settings ORDER BY key"))
    if not rows:
        print("(sin settings. Correr: managed-blocks.py seed)")
        return
    width = max(len(r[0]) for r in rows)
    for key, value, updated in rows:
        print(f"  {key.ljust(width)}  {value}   ({updated})")
    print()
    print("Bloques registrados:")
    for e in REGISTRY:
        print(f"  {e['file']}  ::  {e['key']}")


def cmd_seed(conn, _args):
    added = 0
    for key, value in DEFAULTS.items():
        exists = conn.execute("SELECT 1 FROM settings WHERE key = ?", (key,)).fetchone()
        if not exists:
            # 3 placeholders: key, value, description. updated_at lo pone datetime('now')
            # como literal, no como binding.
            conn.execute(
                "INSERT INTO settings (key, value, description, updated_at) VALUES (?,?,?,NULL)",
                (key, value, "semilla inicial"),
            )
            added += 1
            print(f"  + {key} = {value}")
    conn.commit()
    print(f"{added} setting(s) agregados." if added else "Nada que agregar (ya estaban).")


def cmd_set(conn, args):
    if not args.key or args.value is None:
        sys.exit("Uso: managed-blocks.py set <key> <value>")
    conn.execute(
        """INSERT INTO settings (key, value, description, updated_at)
           VALUES (?,?,?,datetime('now'))
           ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=datetime('now')""",
        (args.key, args.value, "editado a mano"),
    )
    conn.commit()
    print(f"  {args.key} = {args.value}")


def render(entry, settings):
    try:
        return entry["template"].format(**settings)
    except KeyError as e:
        return f"!! falta el setting {e} para el bloque {entry['key']}"


def find_block(text, key):
    """Devuelve (inicio, fin) del contenido entre marcadores, o None si faltan."""
    b = re.escape(BEGIN.format(key=key))
    e = re.escape(END.format(key=key))
    m = re.search(b + r"\n?(.*?)\n?" + e, text, re.DOTALL)
    return m


def snippet(entry, settings):
    """El bloque exacto a pegar a mano cuando faltan los marcadores."""
    return (
        f"{BEGIN.format(key=entry['key'])}\n"
        f"{render(entry, settings)}\n"
        f"{END.format(key=entry['key'])}"
    )


def process(entry, settings, dry_run, quiet=False):
    path = WORKSPACE / entry["file"]
    if not path.exists():
        return f"  ❌ {entry['file']}: no existe"
    text = path.read_text(encoding="utf-8")
    m = find_block(text, entry["key"])
    if not m:
        out = [f"  ⚠️  {entry['file']}: faltan los marcadores '{entry['key']}' (no se toca)"]
        out.append("      Pegar esto una vez en el lugar correcto del archivo, y despues")
        out.append("      el mecanismo lo mantiene solo:")
        out.append("")
        for line in snippet(entry, settings).splitlines():
            out.append(f"      {line}")
        return "\n".join(out)

    old = m.group(1)
    new = render(entry, settings)
    if old == new:
        return f"  ✅ {entry['file']}: al dia" if not quiet else ""

    if dry_run:
        diff = "\n".join(
            difflib.unified_diff(
                old.splitlines(),
                new.splitlines(),
                fromfile=f"{entry['file']} (actual)",
                tofile=f"{entry['file']} (nuevo)",
                lineterm="",
            )
        )
        return f"  ~ {entry['file']}\n{diff}"

    replaced = text[: m.start()] + f"{BEGIN.format(key=entry['key'])}\n{new}\n{END.format(key=entry['key'])}" + text[m.end():]
    path.write_text(replaced, encoding="utf-8")
    return f"  ✅ {entry['file']}: actualizado"


def run_all(conn, dry_run, quiet=False):
    settings = get_settings(conn)
    lines = []
    for entry in REGISTRY:
        r = process(entry, settings, dry_run, quiet)
        if r:
            lines.append(r)
    return lines


def cmd_check(conn, _args):
    print("Estado de los bloques (sin escribir):")
    for line in run_all(conn, True, quiet=True):
        print(line)
    print()
    print("(check no escribe. Para ver el diff completo: apply --dry-run)")


def cmd_apply(conn, args):
    print("Modo: DRY-RUN (no escribe)" if args.dry_run else "Modo: apply (escribe)")
    for line in run_all(conn, args.dry_run):
        print(line)
    if not args.dry_run:
        print()
        print("Recordar regenerar los espejos: ./scripts/memory-db.sh export-* si aplica.")


def main():
    p = argparse.ArgumentParser(description="Propaga settings de la DB a bloques managed en archivos.")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="muestra los settings")
    sub.add_parser("seed", help="inserta los defaults faltantes")
    ps = sub.add_parser("set", help="cambia un setting")
    ps.add_argument("key")
    ps.add_argument("value")
    sub.add_parser("check", help="reporta drift sin escribir")
    pa = sub.add_parser("apply", help="regenera los bloques")
    pa.add_argument("--dry-run", action="store_true", help="muestra el diff sin escribir")

    args = p.parse_args()
    conn = db()
    try:
        {
            "list": cmd_list,
            "seed": cmd_seed,
            "set": cmd_set,
            "check": cmd_check,
            "apply": cmd_apply,
        }[args.cmd](conn, args)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
