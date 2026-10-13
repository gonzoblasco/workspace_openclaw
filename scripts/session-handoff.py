#!/usr/bin/env python3
"""
session-handoff.py - Genera/actualiza el HANDOFF.md del proyecto en curso
(o del workspace) al cerrar una sesion.

Pedido de Gonzo (2026-10-06): cada cierre de sesion debe dejar, ademas del
informe en `memory/YYYY-MM-DD.md`, un HANDOFF.md en el `.knowledge/` del
proyecto del que se trato la sesion, para continuar del modo correcto sin
re-descubrir contexto.

Destino:
  - workspace / sistema -> <workspace>/.knowledge/HANDOFF.md
  - proyecto           -> <workspace>/projects/<slug>/.knowledge/HANDOFF.md  (ADR-098)

Uso:
  scripts/session-handoff.py --project workspace --summary "..." \
      [--status "..."] [--next-steps "1. ...\n2. ..."] [--decisions "..."] \
      [--branch main] [--repo <url>] [--date YYYY-MM-DD]

El HANDOFF es un documento "de estado actual": cada cierre lo regenera con lo
de la ultima sesion (el historial completo vive en memory/ y en git).
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from lockutil import file_lock

WORKSPACE = Path(__file__).resolve().parent.parent
HOME = Path.home()

# Aliases que apuntan al HANDOFF del workspace (el sistema mismo).
WORKSPACE_ALIASES = {
    "workspace",
    "workspace_openclaw",
    "workspace-openclaw",
    "main",
    "core",
    "kanam-core",
    "sistema",
    "system",
}

# Proyectos cuyo slug difiere del nombre de la carpeta en <workspace>/projects.
PROJECT_DIR_OVERRIDES = {
    "onwheels": "kanam-onwheels",
    "kanam-onwheels": "kanam-onwheels",
}


def norm_dashes(text: str) -> str:
    """Normaliza cualquier guion largo a guion comun (regla del workspace)."""
    for ch in "\u2010\u2011\u2012\u2013\u2014\u2015\u2212":
        text = text.replace(ch, "-")
    return text


def git_output(*args: str, cwd: Optional[Path] = None) -> str:
    try:
        out = subprocess.run(
            ["git", *args],
            cwd=str(cwd or WORKSPACE),
            capture_output=True,
            text=True,
            check=False,
        )
        return out.stdout.strip()
    except Exception:
        return ""


def resolve_handoff_path(project: str, override: Optional[str]) -> Path:
    if override:
        return Path(override).expanduser() / "HANDOFF.md"
    key = project.strip().lower()
    if key in WORKSPACE_ALIASES:
        return WORKSPACE / ".knowledge" / "HANDOFF.md"
    slug = PROJECT_DIR_OVERRIDES.get(key, project.strip())
    return WORKSPACE / "projects" / slug / ".knowledge" / "HANDOFF.md"


def session_line(summary: str, limit: int = 160) -> str:
    """Primera linea no vacia del summary, recortada, como asunto de la sesion."""
    for ln in summary.split("\n"):
        ln = ln.strip()
        if ln:
            ln = norm_dashes(ln)
            if len(ln) > limit:
                ln = ln[: limit - 1].rstrip() + "\u2026"
            return ln
    return "(sin resumen)"


def append_session_index(target: Path, project: str, ts: str, summary: str) -> Optional[Path]:
    """C. Indice append-only de sesiones junto al HANDOFF (`SESSIONS.md`).

    El HANDOFF es last-writer-wins por diseno (es "estado actual"); el indice
    preserva la historia de cierres por proyecto sin depender de esa ultima
    escritura. Append puro: nunca pisa filas previas. Corre DENTRO del lock del
    HANDOFF para que el orden append <-> replace sea consistente entre cierres.
    """
    index = target.parent / "SESSIONS.md"
    if not index.exists():
        header = (
            f"# SESSIONS - {project}\n\n"
            "> Indice append-only de cierres de sesion. El HANDOFF.md es solo el "
            "estado actual; esta lista es la historia (no se pisa).\n\n"
        )
        with index.open("w", encoding="utf-8") as fh:
            fh.write(header)
    line = f"- **{ts}** - {session_line(summary)}\n"
    with index.open("a", encoding="utf-8") as fh:
        fh.write(line)
    return index


def backup_previous(target: Path, ts: str) -> Optional[Path]:
    """A. Guarda el HANDOFF anterior antes de pisarlo.

    El segundo cierre del dia no pierde al primero: queda archivado en
    `.knowledge/handoff-history/YYYY-MM-DD-HHMM-HANDOFF.md`. Se mantiene el
    historial fuera del arbol de primer nivel para no ensuciar `.knowledge/`.
    """
    if not target.exists():
        return None
    hist = target.parent / "handoff-history"
    hist.mkdir(parents=True, exist_ok=True)
    dest = hist / f"{ts.replace(':', '').replace(' ', '-')}-HANDOFF.md"
    shutil.copy2(target, dest)
    return dest


def bullet_block(text: str, numbered: bool = False) -> str:
    """Convierte un texto multilinea en lista (numerada o con guiones)."""
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    if not lines:
        return ""
    out = []
    for i, ln in enumerate(lines, 1):
        # Si ya viene como item de lista, se respeta.
        if re.match(r"^(\d+[.)]|[-*])\s+", ln):
            out.append(ln)
        else:
            prefix = f"{i}. " if numbered else "- "
            out.append(prefix + ln)
    return "\n".join(out)


def files_changed(explicit: str) -> str:
    if explicit:
        return explicit.strip()
    staged = git_output("diff", "--name-only", "--cached")
    worktree = git_output("diff", "--name-only")
    names = sorted({*staged.splitlines(), *worktree.splitlines()})
    return "\n".join(n for n in names if n)


def build_handoff(args) -> str:
    date = args.date or datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    branch = args.branch if args.branch and args.branch != "unknown" else git_output("branch", "--show-current") or "unknown"
    repo = args.repo or git_output(
        "remote", "get-url", "origin", cwd=resolve_handoff_path(args.project, None).parent.parent
    )
    repo = re.sub(r"^git@[^:]+:", "https://github.com/", repo or "")
    repo = re.sub(r"\.git$", "", repo or "")

    parts = []
    parts.append(f"# HANDOFF - {args.project}")
    parts.append("")
    parts.append(f"**Fecha:** {now} GMT-3")
    parts.append(f"**Proyecto:** {args.project}")
    parts.append(f"**Branch:** {branch}")
    if repo:
        parts.append(f"**Repo:** {repo}")
    parts.append("**Autor:** Kanam (CORE)")
    parts.append("")
    parts.append(
        f"> HANDOFF generado en el cierre de sesion ({date}). Es el punto de entrada "
        "para continuar este proyecto. El informe detallado de la sesion vive en "
        f"`memory/{date}.md`."
    )
    parts.append("")
    parts.append("---")
    parts.append("")
    parts.append("## Que se hizo en esta sesion")
    parts.append("")
    parts.append(norm_dashes(args.summary.strip()))
    parts.append("")

    if args.status:
        parts.append("## Estado actual")
        parts.append("")
        parts.append(norm_dashes(args.status.strip()))
        parts.append("")

    if args.next_steps:
        parts.append("## Proximos pasos")
        parts.append("")
        parts.append(bullet_block(norm_dashes(args.next_steps), numbered=True))
        parts.append("")

    if args.decisions:
        parts.append("## Decisiones y contexto que no debe perderse")
        parts.append("")
        parts.append(bullet_block(norm_dashes(args.decisions)))
        parts.append("")

    files = files_changed(args.files)
    if files:
        parts.append("## Archivos tocados")
        parts.append("")
        parts.append("```")
        parts.append(norm_dashes(files))
        parts.append("```")
        parts.append("")

    parts.append("## Como continuar")
    parts.append("")
    parts.append("1. Leer este HANDOFF (estado actual + proximos pasos).")
    parts.append(f"2. Leer `memory/{date}.md` para el informe completo de la sesion.")
    parts.append("3. Verificar el estado real antes de actuar (git, tests, la DB).")
    parts.append("")
    parts.append("---")
    parts.append("")
    parts.append(
        "*Generado por `scripts/session-handoff.py` (session-lifecycle). "
        "Se regenera en cada cierre de sesion.*"
    )
    parts.append("")

    return "\n".join(parts)


def main():
    p = argparse.ArgumentParser(description="Genera/actualiza el HANDOFF del proyecto en curso")
    p.add_argument("--project", required=True, help="workspace|workspace_openclaw|main, o el slug del proyecto")
    p.add_argument("--summary", required=True, help="Que se hizo en la sesion (multilinea)")
    p.add_argument("--status", default="", help="Estado actual del proyecto (opcional)")
    p.add_argument("--next-steps", dest="next_steps", default="", help="Proximos pasos (multilinea)")
    p.add_argument("--decisions", default="", help="Decisiones/contexto a no perder (multilinea)")
    p.add_argument("--files", default="", help="Archivos tocados (si se omite, se toma de git)")
    p.add_argument("--branch", default="unknown")
    p.add_argument("--repo", default="")
    p.add_argument("--date", default="")
    p.add_argument("--handoff-dir", dest="handoff_dir", default="", help="Override del directorio destino")
    args = p.parse_args()

    target = resolve_handoff_path(args.project, args.handoff_dir or None)
    content = build_handoff(args)

    target.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    # B6 (2026-10-12): varias sesiones cierran sobre el MISMO repo; el HANDOFF es
    # last-writer-wins. El lock serializa el ciclo para que dos cierres simultaneos
    # no se intercalen. A+C (2026-10-13): el mismo lock cubre el backup del HANDOFF
    # previo (A) y el append al indice de sesiones (C), asi el orden
    # backup -> index -> replace es consistente entre cierres concurrentes.
    with file_lock(target):
        existed = target.exists()
        backup = backup_previous(target, ts) if existed else None
        index = append_session_index(target, args.project, ts, args.summary)
        tmp = target.with_suffix(".md.tmp")
        tmp.write_text(content, encoding="utf-8")
        os.replace(tmp, target)

    action = "actualizado" if existed else "creado"
    print(f"HANDOFF {action}: {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
