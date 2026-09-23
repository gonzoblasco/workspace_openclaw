#!/usr/bin/env python3
"""
interpret-entries.py - Propone campos para las unidades de una ficha, con revision.

TERCERA ETAPA del refactor de fichas (2026-09-23):

  1. migrate-entries.py  (hecho)  -> desaplana: 521 unidades de nivel 2
  2. este script         -> PROPONE campos interpretando el material
  3. revision humana     -> se aprueba y recien ahi se escriben

PRINCIPIO: el LLM PROPONE, no escribe. Nada de lo que devuelve va a la DB sin
que se revise. Es la diferencia entre interpretar y fabricar:

  - Determinsta (migrate-entries): el titulo dice "Pendientes" -> es una seccion
    de pendientes. No hay juicio.
  - Interpretativo (aca): el titulo dice "Cap 1 - The Architecture" -> ¿es una
    leccion? ¿un tema de estudio? ¿una nota? Eso lo propone el modelo y lo
    confirma una persona.

Los campos propuestos se guardan en una tabla de PROPUESTAS, no en las columnas
de la ficha. Asi una propuesta erronea no contamina el registro.

QUE PROPONE (y por que esos):

  project   el proyecto al que pertenece la unidad, de la lista real de projects/
  topic     de que trata, en 3-6 palabras
  kind      'trabajo' | 'estudio' | 'reflexion' | 'cierre' | 'otro'
  summary   una linea de que paso

QUE NO PROPONE:

  - Fechas, ids, o cualquier cosa que ya este en una columna. Se verifica.
  - Campos que no se puedan verificar contra algo (ej: "importancia: 7/10" es
    opinion, no dato).

Uso:
    interpret-entries.py --dry-run [--limit N] [--session ID]
    interpret-entries.py --apply --session ID     (requiere propuestas revisadas)
    interpret-entries.py --review [--session ID]  (muestra las propuestas)
"""
import argparse
import json
import os
import re
import sqlite3
import subprocess
import sys
import urllib.request
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
DB = Path(os.environ.get("MEMORY_DB", WS / "memory" / "memory.db"))
OLLAMA = os.environ.get("OLLAMA_BASE", "http://127.0.0.1:11434")
MODEL = os.environ.get("INTERPRET_MODEL", "gemma4:cloud")

SCHEMA = """
CREATE TABLE IF NOT EXISTS proposed_fields (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id    INTEGER NOT NULL,      -- FK a session_entries
    field       TEXT NOT NULL,         -- project | topic | kind | summary
    value       TEXT NOT NULL,
    model       TEXT,                  -- que modelo lo propuso
    status      TEXT NOT NULL DEFAULT 'pending',   -- pending | approved | rejected
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (entry_id, field)
);
CREATE INDEX IF NOT EXISTS idx_proposed_status ON proposed_fields(status);
CREATE INDEX IF NOT EXISTS idx_proposed_entry  ON proposed_fields(entry_id);
"""

VALID_KINDS = {"trabajo", "estudio", "reflexion", "cierre", "otro"}


def real_projects():
    """Los proyectos que existen en disco. El vocabulario se valida contra esto."""
    p = WS / "projects"
    if not p.is_dir():
        return []
    return sorted(d.name for d in p.iterdir() if d.is_dir() and not d.name.startswith("."))


def call_model(prompt, timeout=90):
    """Una llamada a Ollama. Devuelve el texto o None."""
    body = json.dumps(
        {"model": MODEL, "prompt": prompt, "stream": False, "options": {"temperature": 0.1}}
    ).encode()
    req = urllib.request.Request(
        f"{OLLAMA}/api/generate", data=body, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read()).get("response", "")
    except Exception as exc:
        print(f"    modelo no disponible: {exc}", file=sys.stderr)
        return None


def body_of(conn, entry_id):
    r = conn.execute(
        "SELECT session_id, char_start, char_end FROM session_entries WHERE id=?", (entry_id,)
    ).fetchone()
    if not r:
        return None, None
    sid, cs, ce = r
    cb = conn.execute("SELECT content_bare FROM sessions_relacional WHERE id=?", (sid,)).fetchone()
    return (cb[0][cs:ce] if cb else ""), sid


def build_prompt(title, body, projects):
    lista = ", ".join(projects[:24]) if projects else "(sin proyectos)"
    return f"""Analiza esta unidad de una sesion de trabajo y devuelve SOLO un JSON valido.

TITULO: {title}

CONTENIDO:
{body[:1800]}

Proyectos reales del usuario (elegi uno o "ninguno"): {lista}

Devuelve exactamente estas claves:
{{
  "project": "<uno de la lista, o 'ninguno' si no es claro>",
  "topic": "<de que trata, 3-6 palabras>",
  "kind": "<trabajo|estudio|reflexion|cierre|otro>",
  "summary": "<una linea de que paso>"
}}

Reglas:
- Si el proyecto no surge CLARAMENTE del texto, devolve "ninguno". No adivines.
- "topic" describe el contenido, no repite el titulo.
- Responde unicamente el JSON, sin explicaciones."""


def parse_json(raw):
    """Extrae el primer objeto JSON del texto. Devuelve dict o None."""
    if not raw:
        return None
    m = re.search(r"\{.*\}", raw, re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except Exception:
        return None
    return d if isinstance(d, dict) else None


def validate(conn, entry_id, props, projects):
    """Descarta lo que no se puede verificar. Devuelve solo lo valido.

    Esto es lo que separa esta etapa de "confiar en el modelo": cada campo
    propuesto pasa por una verificacion antes de guardarse como propuesta.
    """
    ok = {}
    project = (props.get("project") or "").strip()
    if project and project.lower() not in ("ninguno", "none", ""):
        # El vocabulario se valida contra los proyectos reales.
        match = next((p for p in projects if p.lower() == project.lower()), None)
        if match:
            ok["project"] = match
    # Un valor largo se TRUNCA, no se descarta: el modelo se paso de largo pero
    # el contenido sirve. Un valor corto si se descarta (no aporta).
    topic = (props.get("topic") or "").strip()
    if len(topic) >= 3:
        ok["topic"] = topic[:80]
    kind = (props.get("kind") or "").strip().lower()
    if kind in VALID_KINDS:
        ok["kind"] = kind
    summary = (props.get("summary") or "").strip()
    if len(summary) >= 10:
        ok["summary"] = summary[:300]
    return ok


def interpret(conn, limit, session_id, dry_run):
    projects = real_projects()
    where = "WHERE e.kind='tema'"
    params = []
    if session_id:
        where += " AND e.session_id=?"
        params.append(session_id)
    rows = conn.execute(
        f"""SELECT e.id, e.title, e.session_id FROM session_entries e
            {where} ORDER BY e.session_id, e.ordinal LIMIT ?""",
        (*params, limit),
    ).fetchall()

    print(f"  unidades a interpretar: {len(rows)} (de {len(projects)} proyectos reales)")
    hechas = 0
    for eid, title, sid in rows:
        body, _ = body_of(conn, eid)
        if not body:
            continue
        props = parse_json(call_model(build_prompt(title, body, projects)))
        if not props:
            print(f"    [{sid}] {title[:40]!r}: sin respuesta valida, se omite")
            continue
        validos = validate(conn, eid, props, projects)
        if not validos:
            print(f"    [{sid}] {title[:40]!r}: nada verificable, se omite")
            continue
        if not dry_run:
            for field, value in validos.items():
                conn.execute(
                    """INSERT OR REPLACE INTO proposed_fields (entry_id, field, value, model, status)
                       VALUES (?,?,?,?, 'pending')""",
                    (eid, field, value, MODEL),
                )
            conn.commit()
        campos = ", ".join(f"{k}={v[:26]}" for k, v in validos.items())
        print(f"    [{sid}] {title[:34]!r} -> {campos}")
        hechas += 1
    return hechas


def review(conn, session_id):
    where = "WHERE p.status='pending'"
    params = []
    if session_id:
        where += " AND e.session_id=?"
        params.append(session_id)
    rows = conn.execute(
        f"""SELECT e.session_id, e.title, p.field, p.value
            FROM proposed_fields p JOIN session_entries e ON e.id = p.entry_id
            {where} ORDER BY e.session_id, e.ordinal, p.field""",
        params,
    ).fetchall()
    if not rows:
        print("  sin propuestas pendientes")
        return 0
    actual = None
    for sid, title, field, value in rows:
        if sid != actual:
            print(f"\n  === ficha {sid} ===")
            actual = sid
        print(f"    {title[:44]!r}")
        print(f"       {field:8} = {value}")
    print(f"\n  total propuestas pendientes: {len(rows)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true", help="escribe las propuestas aprobadas")
    ap.add_argument("--review", action="store_true", help="muestra las propuestas pendientes")
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--session", type=int, default=None)
    args = ap.parse_args()

    if not DB.exists():
        sys.exit(f"No existe {DB}")

    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        conn.executescript(SCHEMA)
        conn.commit()

        if args.review:
            print("Propuestas pendientes de revision:")
            review(conn, args.session)
            return 0

        if args.apply:
            # Solo se aplican las APROBADAS. Si nadie aprobo nada, no pasa nada.
            n = conn.execute(
                "SELECT count(*) FROM proposed_fields WHERE status='approved'"
            ).fetchone()[0]
            print(f"  propuestas aprobadas: {n}")
            print("  (la aplicacion a las columnas va en la etapa siguiente)")
            return 0

        modo = " (DRY-RUN)" if args.dry_run else ""
        print(f"Interpretando{modo} con {MODEL}...")
        n = interpret(conn, args.limit, args.session, args.dry_run)
        print(f"\n  unidades interpretadas: {n}")
        if not args.dry_run:
            print("  Revisar con: --review")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
