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
from typing import List, Optional

from lockutil import file_lock

WORKSPACE = Path(__file__).resolve().parent.parent
HOME = Path.home()

# Nombre de backup aceptado en handoff-history: YYYY-MM-DD-HHMM[-N]-HANDOFF.md.
BACKUP_NAME_RE = re.compile(
    r"^(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{4})(?:-(?P<seq>[0-9]+))?-HANDOFF\.md$"
)

# Linea de fecha del HANDOFF. Anclada al inicio de linea para no tomar una fecha
# incrustada en prosa, en un ejemplo o en un bloque de codigo.
FECHA_RE = re.compile(
    r"^\*\*Fecha:\*\*[ \t]*([0-9]{4}-[0-9]{2}-[0-9]{2})[ \t]+([0-9]{2}:[0-9]{2})(?![0-9])",
    re.MULTILINE,
)

# Binario de papelera del sistema. Se puede overridear con
# HANDOFF_HISTORY_TRASH_BIN (cadena vacia = no intentar el binario y usar el
# fallback local). Es lo que usan los tests para no mandar archivos reales a
# ~/.Trash.
TRASH_BIN = "/usr/bin/trash"

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

# Contenedores donde puede vivir un proyecto, en orden de busqueda. `projects/`
# NO es el unico: un fork, un clon y un proyecto del banco de trabajo tienen su
# propio `.knowledge/` y su HANDOFF tiene que caer ahi, no en un arbol fantasma
# bajo `projects/` (bug corregido 2026-11-03).
#
# `oss/` (2026-11-03) agrupa las contribuciones a repos ajenos:
# `oss/<owner>-<repo>/.knowledge/`. No es codigo ni un repo nuestro: es el
# registro del hilo (que se dijo, quien tiene la pelota). Vive aparte de
# `forks/` porque el fork es codigo desechable y este registro lo sobrevive.
PROJECT_CONTAINERS = ("projects", "_workbench", "forks", "clones", "oss")

# Proyectos cuyo slug difiere del nombre de la carpeta en <workspace>/projects.
PROJECT_DIR_OVERRIDES = {
    # El proyecto ACTIVO de OnWheels vive en projects/onwheels (creado 2026-10-21,
    # greenfield). El repo projects/kanam-onwheels quedo DORMIDO (ver
    # docs/ecosystem/CONSOLIDACION-PRODUCTO-DEALER.md, decision D4): se conserva
    # como referencia de lectura y su HANDOFF ya no se actualiza.
    # Antes este mapeo Mandaba "onwheels" al repo dormido, y el HANDOFF de la
    # sesion caia en el proyecto equivocado.
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


def _container_dirs(name: str) -> List[Path]:
    """Carpetas reales de proyecto que se llaman `name` en cualquier contenedor.

    Primero busca coincidencia **exacta**: hay directorios que terminaban en
    espacio (`"OSS "`) y el slug recortado no los encontraba, asi que el cierre
    escribia en una ruta inexistente. Solo si no hay ninguna exacta se compara
    contra el nombre recortado, para que un slug prolijo (`OSS`) siga llegando a
    una carpeta sucia sin que eso oculte el caso exacto.
    """
    entries_by_container = []
    for container in PROJECT_CONTAINERS:
        root = WORKSPACE / container
        try:
            entries = [e for e in root.iterdir() if e.is_dir()]
        except OSError:
            continue
        entries_by_container.append(entries)

    exact = [e for entries in entries_by_container for e in entries if e.name == name]
    if exact:
        return exact
    normalized = name.strip()
    return [
        e for entries in entries_by_container for e in entries if e.name.strip() == normalized
    ]


def _reject_traversal(path: Path, what: str) -> None:
    """Rechaza un destino que se salga del arbol del workspace.

    Un slug con separadores (`"OSS / astryx (meta/astryx #3335)"`) hacia que
    `WORKSPACE / "projects" / slug` se convirtiera en un arbol anidado que
    `mkdir(parents=True)` creaba sin avisar: el 2026-10-29 quedo
    `projects/OSS / astryx (meta/astryx #3335)/.knowledge/` en vez del
    `.knowledge/` del proyecto. Un `..` hacia lo mismo, pero hacia afuera.
    """
    resolved = path.expanduser().resolve()
    try:
        resolved.relative_to(WORKSPACE.resolve())
    except ValueError:
        raise ValueError(
            f"{what} apunta fuera del workspace ({resolved}). Pasar un destino "
            "dentro del arbol del workspace."
        ) from None


def resolve_handoff_path(project: str, override: Optional[str]) -> Path:
    """Resuelve el `.knowledge/` del sujeto, este donde este.

    Orden: override -> alias de workspace -> carpeta real del proyecto en
    `projects/`, `_workbench/`, `forks/` o `clones/`. Si el slug coincide con mas
    de una carpeta se falla con error explicito: adivinar es como se termina
    escribiendo el HANDOFF de un proyecto en el `.knowledge/` de otro. Si no
    existe ninguna carpeta, se cae al comportamiento historico (`projects/<slug>`)
    para no romper llamadas con slugs que todavia no tienen carpeta.
    """
    if override:
        dest = Path(override).expanduser()
        _reject_traversal(dest, "el destino de --handoff-dir")
        return dest / "HANDOFF.md"
    raw = project.strip()
    key = raw.lower()
    if key in WORKSPACE_ALIASES:
        return WORKSPACE / ".knowledge" / "HANDOFF.md"
    slug = PROJECT_DIR_OVERRIDES.get(key, project.strip())
    if "/" in slug or "\\" in slug or slug in (".", ".."):
        raise ValueError(
            f"El slug '{project}' no es un nombre de carpeta: contiene separadores "
            "de ruta o '..'. Usar el slug real del proyecto (sin barras) o pasar "
            "--handoff-dir con la carpeta ya existente."
        )

    matches = _container_dirs(slug)
    if len(matches) > 1:
        rels = ", ".join(str(p.relative_to(WORKSPACE)) for p in matches)
        raise ValueError(
            f"El slug '{slug}' existe en mas de un contenedor ({rels}). "
            "Pasar el destino real con --handoff-dir para desambiguar."
        )
    if len(matches) == 1:
        return matches[0] / ".knowledge" / "HANDOFF.md"

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


def _fecha_from_handoff(target: Path) -> Optional[datetime]:
    """Devuelve la fecha de la linea ``**Fecha:**`` del HANDOFF, o None."""
    try:
        content = target.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    m = FECHA_RE.search(content)
    if not m:
        return None
    try:
        return datetime.strptime(f"{m.group(1)} {m.group(2)}", "%Y-%m-%d %H:%M")
    except ValueError:
        return None


def _backup_sort_key(path: Path):
    """Clave de orden de un backup: (fecha del nombre, sufijo de colision).

    El nombre puede ser ``YYYY-MM-DD-HHMM-HANDOFF.md`` o llevar sufijo
    ``-2``, ``-3``: el regex extrae la fecha base en ambos casos y el sufijo
    desempata para que el mas nuevo de una misma fecha quede primero.
    """
    m = BACKUP_NAME_RE.match(path.name)
    if not m:
        return (datetime.min, 0)
    try:
        dt = datetime.strptime(m.group("date"), "%Y-%m-%d-%H%M")
    except ValueError:
        return (datetime.min, 0)
    seq = int(m.group("seq") or 1)
    return (dt, seq)


def _trash_bin() -> Optional[str]:
    """Binario de papelera a usar, o None si hay que caer al fallback local.

    ``HANDOFF_HISTORY_TRASH_BIN`` permite forzar el comportamiento: si esta
    definida y vacia, nunca se invoca el binario del sistema (los tests lo usan
    para no mandar archivos reales a ``~/.Trash``).
    """
    override = os.getenv("HANDOFF_HISTORY_TRASH_BIN")
    if override is not None:
        override = override.strip()
        return override or None
    if os.path.isfile(TRASH_BIN) and os.access(TRASH_BIN, os.X_OK):
        return TRASH_BIN
    return None


def _discard_backup(path: Path, hist: Path) -> None:
    """Saca un backup del historial de forma recuperable. Nunca borra.

    Primero intenta el binario de papelera del sistema; si no esta disponible
    (o falla), lo mueve a ``handoff-history/.trash/``. En ambos casos el archivo
    queda recuperable: no se usa ``rm`` ni ``unlink`` en ningun camino.
    """
    bin_path = _trash_bin()
    if bin_path:
        try:
            res = subprocess.run(
                [bin_path, str(path)], capture_output=True, text=True, check=False
            )
            if res.returncode == 0 and not path.exists():
                return
        except Exception:
            pass
    trash_dir = hist / ".trash"
    trash_dir.mkdir(parents=True, exist_ok=True)
    dest = trash_dir / path.name
    suffix = 2
    while dest.exists():
        dest = trash_dir / f"{path.stem}-{suffix}{path.suffix}"
        suffix += 1
    path.rename(dest)


def backup_previous(target: Path, ts: str) -> Optional[Path]:
    """A. Guarda el HANDOFF anterior antes de pisarlo.

    El segundo cierre del dia no pierde al primero: queda archivado en
    ``.knowledge/handoff-history/YYYY-MM-DD-HHMM-HANDOFF.md``. Se mantiene el
    historial fuera del arbol de primer nivel para no ensuciar ``.knowledge/``.

    Reglas:
    - El nombre del archivo archivado se deriva de la fecha del HANDOFF que se
      copia (la linea ``**Fecha:** YYYY-MM-DD HH:MM``, al inicio de linea), no
      del timestamp ``ts`` del cierre que lo reemplaza.
    - Si esa linea falta o no parsea, se usa el ``mtime`` del archivo; si
      tampoco se puede obtener, el ``ts`` recibido; como ultimo recurso, ahora.
    - Si el destino ya existe (misma fecha y minuto), se agrega un sufijo
      incremental ``-2``, ``-3``... sin sobrescribir nada.
    - Retencion: se conservan los ultimos ``N`` backups, con ``N`` tomado de
      ``HANDOFF_HISTORY_KEEP`` (default 10; un valor no entero cae al default y
      un valor negativo se trata como 0). El backup recien creado nunca se poda.
      Los descartados van al binario ``/usr/bin/trash`` si esta disponible; si
      no, a ``handoff-history/.trash/``. Nunca se borran de forma irreversible.
    """
    if not target.exists():
        return None

    # ---------------------------------------------------------------------
    # Determinar la fecha a usar para el nombre del backup.
    # ---------------------------------------------------------------------
    date_dt = _fecha_from_handoff(target)
    if date_dt is None:
        try:
            date_dt = datetime.fromtimestamp(target.stat().st_mtime)
        except OSError:
            date_dt = None
    if date_dt is None:
        try:
            date_dt = datetime.strptime(ts, "%Y-%m-%d %H:%M")
        except ValueError:
            date_dt = datetime.now()

    # ---------------------------------------------------------------------
    # Construir nombre del archivo de backup.
    # ---------------------------------------------------------------------
    hist = target.parent / "handoff-history"
    hist.mkdir(parents=True, exist_ok=True)

    stem = date_dt.strftime("%Y-%m-%d-%H%M")
    dest = hist / f"{stem}-HANDOFF.md"
    suffix = 2
    while dest.exists():
        dest = hist / f"{stem}-{suffix}-HANDOFF.md"
        suffix += 1

    shutil.copy2(target, dest)

    # ---------------------------------------------------------------------
    # Politica de retencion: mantener solo N backups, contando el recien creado.
    # ---------------------------------------------------------------------
    keep_str = os.getenv("HANDOFF_HISTORY_KEEP", "10")
    try:
        keep = int(keep_str)
    except (TypeError, ValueError):
        keep = 10
    if keep < 0:
        keep = 0

    all_backups = [
        p for p in hist.iterdir() if p.is_file() and BACKUP_NAME_RE.match(p.name)
    ]
    to_remove: List[Path] = []
    if len(all_backups) > keep:
        ordered = sorted(all_backups, key=_backup_sort_key, reverse=True)
        survivors = ordered[:keep]
        if dest not in survivors:
            # El backup recien creado sobrevive a su propia poda.
            survivors = survivors[: max(keep - 1, 0)] + [dest]
        to_remove = [p for p in ordered if p not in survivors]

    for old in to_remove:
        _discard_backup(old, hist)

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
