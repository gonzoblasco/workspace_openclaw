#!/usr/bin/env python3
"""moltbook-ingest.py - Persiste un digest de Moltbook en la memoria del workspace.

Problema que resuelve (2026-11-02): el digest semanal generaba items verificados
contra fuente primaria y los mandaba a Telegram. Ahi morian. Medido ese dia:
5 items, 4 verificados, 0 persistidos, 0 de 263 learnings con rastro de Moltbook.

El job escribe UN archivo markdown legible que termina con un bloque ```json
con los items estructurados. Este script lee ese bloque, filtra, deduplica e
inserta. El LLM hace lo que sabe hacer (leer, filtrar, verificar); el script
hace lo que el LLM hace mal de forma repetida (dedupe, tags, idempotencia).

Destino por estado de verificacion:
  verificado    -> tabla learnings  (entra a memory_search, sirve para decidir)
  sin verificar -> tabla inbox      (espera verificacion, NO contamina el corpus)

Uso:
  ./scripts/moltbook-ingest.py memory/moltbook/2026-W45.md
  ./scripts/moltbook-ingest.py --dry-run memory/moltbook/2026-W45.md

Exit: 0 ok, 1 error de formato, 2 nada que ingestar.
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
DB = WORKSPACE / "memory" / "memory.db"
MEMORY_DB = WORKSPACE / "scripts" / "memory-db.sh"

# Mismo filtro que `add-learning` en memory-db.sh: solo tokens, sin prosa.
# El ':' NO es valido, asi que la convencion es source.moltbook, no source:moltbook.
TAG_RE = re.compile(r"^[a-z0-9._-]+$")

VALID_CATEGORIES = {
    "a11y", "bootstrap", "cata", "debugging", "docker", "evaluacion",
    "infraestructura", "integracion", "metodologia", "oss", "pipeline",
    "pipeline-agentes", "proyectos", "skills", "testing",
}

# Un item solo entra al corpus si toca el stack. Moltbook habla de todo.
STACK_HINTS = [
    "openclaw", "agente", "agent", "mcp", "cron", "job", "heartbeat",
    "a11y", "accessib", "react", "typescript", "ts", "supabase", "postgres",
    "ollama", "llm", "model", "embedding", "vector", "rag", "sqlite",
    "node", "bun", "deno", "fs.", "watch", "sse", "stream",
]


def fail(msg: str) -> "None":
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


def parse_digest(path: Path) -> dict:
    """Extrae el ultimo bloque ```json del markdown."""
    text = path.read_text(encoding="utf-8")
    blocks = re.findall(r"```json\s*\n(.*?)\n```", text, re.DOTALL)
    if not blocks:
        fail(f"{path}: no hay bloque ```json con los items")
    try:
        data = json.loads(blocks[-1])
    except json.JSONDecodeError as e:
        fail(f"{path}: JSON invalido en el bloque: {e}")

    if not isinstance(data, dict) or "items" not in data:
        fail(f"{path}: el JSON debe ser un objeto con la clave 'items'")
    if not isinstance(data["items"], list):
        fail(f"{path}: 'items' debe ser una lista")
    return data


def clean_tags(raw: list[str] | str) -> list[str]:
    if isinstance(raw, str):
        raw = re.split(r"[,\s]+", raw)
    out: list[str] = []
    for t in raw:
        t = (t or "").strip().lower()
        if t and TAG_RE.match(t) and t not in out:
            out.append(t)
    return out


def touches_stack(item: dict) -> bool:
    blob = " ".join(
        str(item.get(k, "")) for k in ("title", "what", "applies_to", "category")
    ).lower()
    return any(h in blob for h in STACK_HINTS)


def similar_exists(title: str, what: str, threshold: float = 0.55) -> tuple[bool, str]:
    """Dedupe semantico contra el corpus existente.

    Reusa memory-search.py (el mismo motor que memory_search). Un match alto
    significa que ya hay una leccion que cubre esto: no duplicar.
    """
    query = f"{title}. {what}"[:600]
    try:
        proc = subprocess.run(
            ["bash", str(MEMORY_DB), "search", query, "3"],
            capture_output=True, text=True, timeout=120, cwd=str(WORKSPACE),
        )
    except (subprocess.TimeoutExpired, OSError) as e:
        print(f"  [aviso] dedupe no disponible ({e}); se inserta sin check", file=sys.stderr)
        return False, ""

    out = (proc.stdout or "") + (proc.stderr or "")
    if re.search(r"(?i)no results|sin resultados", out):
        return False, ""

    # memory-search imprime score=<float> por linea; basta el maximo.
    scores = [float(m) for m in re.findall(r"score[=:]\s*([0-9]*\.?[0-9]+)", out)]
    if scores and max(scores) >= threshold:
        return True, f"score={max(scores):.2f}"
    return False, ""


def ensure_tables(conn: sqlite3.Connection) -> None:
    conn.execute(
        """CREATE TABLE IF NOT EXISTS moltbook_items (
             id INTEGER PRIMARY KEY,
             week TEXT NOT NULL,
             title TEXT NOT NULL,
             status TEXT NOT NULL,
             source_url TEXT,
             verified_against TEXT,
             destination TEXT,
             ingested_at TEXT DEFAULT (datetime('now')),
             UNIQUE(week, title)
           )"""
    )
    conn.commit()


def already_ingested(conn: sqlite3.Connection, week: str, title: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM moltbook_items WHERE week=? AND title=?", (week, title)
    ).fetchone()
    return row is not None


def main() -> int:
    ap = argparse.ArgumentParser(description="Ingesta un digest de Moltbook en la memoria.")
    ap.add_argument("digest", type=Path, help="ruta al markdown del digest")
    ap.add_argument("--dry-run", action="store_true", help="mostrar sin escribir")
    args = ap.parse_args()

    path = args.digest
    if not path.exists():
        fail(f"no existe: {path}")

    data = parse_digest(path)
    week = str(data.get("week") or path.stem)
    items = data["items"]

    if not items:
        print(f"{week}: digest vacio (nada accionable). Archivo conservado como registro.")
        return 2

    if not DB.exists():
        fail(f"no existe la DB: {DB}")

    conn = sqlite3.connect(DB)
    ensure_tables(conn)

    stats = {"verified": 0, "pending": 0, "skip_dup": 0, "skip_offtopic": 0, "skip_done": 0}

    for item in items:
        title = str(item.get("title", "")).strip()
        if not title:
            print("  [skip] item sin title")
            continue

        if already_ingested(conn, week, title):
            print(f"  [skip] ya ingestado: {title[:60]}")
            stats["skip_done"] += 1
            continue

        status = str(item.get("status", "")).strip().lower()
        what = str(item.get("what", "")).strip()
        source = str(item.get("source", "")).strip()
        verified_against = str(item.get("verified_against", "")).strip()

        if not touches_stack(item):
            print(f"  [skip] fuera del stack: {title[:60]}")
            stats["skip_offtopic"] += 1
            continue

        dup, why = similar_exists(title, what)
        if dup:
            print(f"  [skip] duplicado ({why}): {title[:60]}")
            stats["skip_dup"] += 1
            continue

        verified = status.startswith("verific") and bool(verified_against)

        if verified:
            category = str(item.get("category", "")).strip().lower()
            if category not in VALID_CATEGORIES:
                category = "infraestructura"
            tags = clean_tags(
                (item.get("tags") or []) + ["source.moltbook", "verified"]
            )
            content = what
            if source:
                content += f"\n\nFuente: {source}"
            content += f"\nVerificado contra: {verified_against}"

            print(f"  [+] learnings [{category}]: {title[:60]}")
            if not args.dry_run:
                subprocess.run(
                    ["bash", str(MEMORY_DB), "add-learning", category, title,
                     content, ",".join(tags)],
                    check=True, cwd=str(WORKSPACE), capture_output=True, text=True,
                )
            stats["verified"] += 1
            dest = "learnings"
        else:
            idea = f"[moltbook {week}] {title}\n\n{what}"
            if source:
                idea += f"\n\nFuente: {source}"
            idea += "\n\nEstado: SIN VERIFICAR. Verificar contra fuente primaria antes de usar."
            print(f"  [~] inbox (sin verificar): {title[:60]}")
            if not args.dry_run:
                subprocess.run(
                    ["bash", str(MEMORY_DB), "add-inbox", idea],
                    check=True, cwd=str(WORKSPACE), capture_output=True, text=True,
                )
            stats["pending"] += 1
            dest = "inbox"

        if not args.dry_run:
            conn.execute(
                """INSERT INTO moltbook_items
                   (week, title, status, source_url, verified_against, destination)
                   VALUES (?,?,?,?,?,?)""",
                (week, title, status, source, verified_against, dest),
            )
            conn.commit()

    conn.close()

    prefix = "[dry-run] " if args.dry_run else ""
    print(
        f"\n{prefix}{week}: {stats['verified']} a learnings, {stats['pending']} a inbox, "
        f"{stats['skip_dup']} duplicados, {stats['skip_offtopic']} fuera del stack, "
        f"{stats['skip_done']} ya ingestados."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
