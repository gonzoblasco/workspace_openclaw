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
# Regex to capture markdown level‑2 headings (## Title) – used for parsing HANDOFF sections.
SEC_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)

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
#
# `services/` (2026-11-03) es un repo de terceros que CORRE como servicio
# interno: no se le manda PR, se lo opera. Su `.knowledge/` es nuestro y va
# trackeado en nuestro fork. Distinto de `forks/`, que existe para contribuir.
PROJECT_CONTAINERS = ("projects", "_workbench", "forks", "clones", "oss", "services")

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

# ---------------------------------------------------------------------------
# Workspace HANDOFF merge helpers (general HANDOFF).
# ---------------------------------------------------------------------------

def _parse_sections(text: str) -> dict:
    """Parse markdown sections keyed by lower‑cased title.

    Returns a mapping ``title -> body`` where ``title`` is the original title
    (preserving case) and ``body`` is the raw text following the heading up to
    the next ``##`` or end of file.
    """
    secs = {}
    matches = list(SEC_RE.finditer(text))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        title = m.group(1).strip()
        secs[title] = text[start:end]
    return secs

def _extract_que_hizo_entries(body: str, fallback_head: str = "") -> list:
    """Extract entries from the ``Que se hizo`` section.

    Each entry is a tuple ``(header_line, entry_body)`` where ``header_line``
    starts with ``###``. If the section does not contain explicit ``###``
    headings, treat the whole body as a single entry with an empty header.
    """
    lines = body.splitlines()
    entries = []
    cur_head = None
    cur_body = []
    for line in lines:
        if line.startswith("### "):
            if cur_head is not None:
                entries.append((cur_head, "\n".join(cur_body).strip()))
            cur_head = line.strip()
            cur_body = []
        else:
            cur_body.append(line)
    if cur_head is not None:
        entries.append((cur_head, "\n".join(cur_body).strip()))
    # If no ``###`` headings were found, treat the whole body as one entry.
    if not entries:
        entries.append((fallback_head, body.strip()))
    return entries

def _merge_que_hizo(new_body: str, old_body: str, old_head: str = "") -> str:
    # New entry first (timestamped). Normalise the new summary text.
    now_header = f"### {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    new_entry_body = norm_dashes(new_body.strip())
    # Parse old entries which may already be timestamped.
    old_entries = _extract_que_hizo_entries(old_body, old_head)
    # Combine, keeping the new entry first.
    combined = [(now_header, new_entry_body)] + old_entries
    # Deduplicate by normalised body text (ignore header).
    seen = set()
    uniq = []
    for head, body in combined:
        body = body.strip()
        if not body:
            continue
        norm_body = norm_dashes(body).lower()
        if norm_body in seen:
            continue
        seen.add(norm_body)
        uniq.append((head, body))
    # Keep at most 5 entries.
    uniq = uniq[:5]
    # Render back.
    parts = []
    for head, body in uniq:
        parts.append(head if head else "### (sin fecha)")
        if body:
            parts.append(body)
        parts.append("")  # blank line between entries
    return "\n".join(parts).strip()

def _merge_append_section(new_body: str, old_body: str, inherited_title: str) -> str:
    """Preserva el bloque anterior verbatim debajo de un subtitulo.

    Re-renderizar item por item aplana los grupos hechos a mano (HEREDADOS,
    bloques legales, sublistas con 0-bis) y los convierte en una sola vineta
    gigante. Conservar el cuerpo anterior tal como estaba mantiene la lectura
    y garantiza que no se pierde nada.
    """
    new = new_body.strip()
    old = old_body.strip()
    if not old:
        return new
    if not new:
        return old
    new_key = norm_dashes(new).lower()
    old_key = norm_dashes(old).lower()
    if new_key == old_key or new_key in old_key:
        return old
    return f"{new}\n\n{inherited_title}\n\n{old}"

def _extract_code_lines(section_body: str) -> list:
    m = re.search(r"```\n(.*?)\n```", section_body, re.DOTALL)
    if not m:
        return []
    return [ln.strip() for ln in m.group(1).splitlines() if ln.strip()]

def _merge_archivos_section(new_body: str, old_body: str) -> str:
    new_lines = _extract_code_lines(new_body)
    old_lines = _extract_code_lines(old_body)
    combined = new_lines + old_lines
    seen = set()
    uniq = []
    for ln in combined:
        key = norm_dashes(ln).lower()
        if key not in seen:
            seen.add(key)
            uniq.append(ln)
    block = "\n".join(uniq)
    return f"```\n{block}\n```"

def merge_workspace_handoff(new_text: str, old_text: str) -> str:
    """Merge a new HANDOFF (general workspace) with the existing one.

    The merge follows the rules described in the task specification.
    """
    # Split header (everything before first "##")
    header_end = new_text.find("\n##")
    if header_end == -1:
        # Unexpected format – fallback to new content.
        return new_text
    header = new_text[:header_end].rstrip()
    new_secs = _parse_sections(new_text)
    old_secs = _parse_sections(old_text)
    # La entrada anterior puede no tener subtitulo: usar la Fecha del HANDOFF
    # viejo como timestamp en vez de un "(sin fecha)" que no dice nada.
    fecha_m = re.search(r"\*\*Fecha:\*\*\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2})", old_text)
    old_entry_head = f"### {fecha_m.group(1)}" if fecha_m else ""

    merged_secs = {}
    # Known sections with special merge handling.
    for title, new_body in new_secs.items():
        low = title.lower()
        old_body = old_secs.get(title, "")
        if low == "que se hizo en esta sesion":
            merged_body = _merge_que_hizo(new_body, old_body, old_entry_head)
        elif low == "proximos pasos":
            merged_body = _merge_append_section(
                new_body, old_body, "### Pendientes heredados (sin cambios)"
            )
        elif low == "estado actual":
            merged_body = _merge_append_section(
                new_body, old_body, "### Estado previo (heredado)"
            )
        elif low == "decisiones y contexto que no debe perderse":
            merged_body = _merge_append_section(
                new_body, old_body, "### Heredadas (sin cambios)"
            )
        elif low == "cerrados en esta sesion":
            merged_body = _merge_append_section(
                new_body, old_body, "### Cerrados previamente"
            )
        elif low == "archivos tocados":
            merged_body = _merge_archivos_section(new_body, old_body)
        else:
            # New section wins.
            merged_body = new_body
        merged_secs[title] = merged_body

    # Preserve any old‑only sections that were not in the new content.
    for title, old_body in old_secs.items():
        if title not in merged_secs:
            merged_secs[title] = old_body

    # Re‑assemble the document.
    parts = [header]
    for title, body in merged_secs.items():
        parts.append(f"## {title}\n")
        if body:
            parts.append(body.strip())
        parts.append("")
    return "\n".join(parts).strip() + "\n"


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
    if getattr(args, "course", None):
        repo_cwd = WORKSPACE
    else:
        repo_cwd = resolve_handoff_path(args.project, None).parent.parent
    repo = args.repo or git_output(
        "remote", "get-url", "origin", cwd=repo_cwd
    )
    repo = re.sub(r"^git@[^:]+:", "https://github.com/", repo or "")
    repo = re.sub(r"\.git$", "", repo or "")

    parts = []
    display_name = f"Curso {args.course}" if getattr(args, "course", None) else args.project
    parts.append(f"# HANDOFF - {display_name}")
    parts.append("")
    parts.append(f"**Fecha:** {now} GMT-3")
    # For course handoff, show the slug as the proyecto identifier.
    proj_label = args.project if getattr(args, "course", None) is None else args.course
    parts.append(f"**Proyecto:** {proj_label}")
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

    # Los items declarados con --closed tienen que QUEDAR ESCRITOS. Antes solo
    # se pasaban al validador de merge: el gate dejaba de frenar, pero la lista
    # de cerrados no llegaba al archivo, asi que el cierre siguiente volvia a
    # verlos como pendientes perdidos y frenaba otra vez. Un dato que se usa
    # para autorizar una escritura y no se guarda es una validacion sin memoria.
    closed = [norm_dashes(c.strip()) for c in getattr(args, "closed", []) if c and c.strip()]
    if closed:
        parts.append("## Cerrados en esta sesion")
        parts.append("")
        for item in closed:
            parts.append(f"- {item}")
        parts.append("")

    files = files_changed(args.files)
    if getattr(args, "course", None) and not args.files:
        # Un curso no hereda los archivos sucios de otras sesiones del workspace.
        prefix = f"studies/{args.course}/"
        files = "\n".join(ln for ln in files.splitlines() if ln.startswith(prefix))
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


def _load_merge_checker():
    """Carga check-handoff-merge.py (el nombre tiene guiones, no es importable)."""
    import importlib.util
    path = Path(__file__).resolve().parent / "check-handoff-merge.py"
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location("handoff_merge_check", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def validate_merge_before_write(new_text: str, target: Path,
                                closed: List[str]) -> Optional[str]:
    """Devuelve un mensaje de error si el HANDOFF nuevo PISA pendientes heredados.

    POR QUE EXISTE (2026-11-04). El gate vivia FUERA, en session-end.sh, y corria
    DESPUES del os.replace: avisaba con el archivo ya mal escrito. Gonzo lo dijo
    exacto: "esto es lo que queriamos evitar". Un gate que avisa despues de
    destruir no previene, mitiga. Este corre ANTES: si hay perdidas no declaradas,
    el archivo no se toca y el cierre falla.
    """
    checker = _load_merge_checker()
    if checker is None:
        return None  # fail-open explicito: sin checker no bloqueamos

    prev = target if target.exists() else checker.pick_prev(target)
    if prev is None or not prev.exists():
        return None  # primer HANDOFF

    res = checker.analyze(new_text, prev.read_text(), closed)
    if res["ok"]:
        return None

    lines = [f"HANDOFF NO ESCRITO: el contenido nuevo pierde {len(res['missing'])} "
             f"item(s) heredados de {prev.name}."]
    for m in res["missing"]:
        lines.append(f"  [{m['seccion']}] cov={m['cobertura']}  {m['item'][:110]}")
    lines.append("")
    lines.append("Fusiona el item en --next-steps/--decisions, declaralo en la seccion")
    lines.append('CERRADOS del HANDOFF, o pasa --closed "<texto>" una vez por item.')
    lines.append("Para forzar la escritura igual: --force-merge (queda registrado).")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="Genera/actualiza el HANDOFF del proyecto en curso")
    # Mutually exclusive project or course. Exactly one is required.
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--project", help="workspace|workspace_openclaw|main, o el slug del proyecto")
    group.add_argument("--course", help="Slug del curso (sin separadores de ruta)")
    p.add_argument("--summary", required=True, help="Que se hizo en la sesion (multilinea)")
    p.add_argument("--status", default="", help="Estado actual del proyecto (opcional)")
    p.add_argument("--next-steps", dest="next_steps", default="", help="Proximos pasos (multilinea)")
    p.add_argument("--decisions", default="", help="Decisiones/contexto a no perder (multilinea)")
    p.add_argument("--files", default="", help="Archivos tocados (si se omite, se toma de git)")
    p.add_argument("--branch", default="unknown")
    p.add_argument("--repo", default="")
    p.add_argument("--date", default="")
    p.add_argument("--handoff-dir", dest="handoff_dir", default="", help="Override del directorio destino")
    p.add_argument("--closed", action="append", default=[],
                   help="Item heredado que se declara CERRADO (repetible)")
    p.add_argument("--force-merge", dest="force_merge", action="store_true",
                   help="Escribe aunque se pierdan heredados (queda como decision explicita)")
    args = p.parse_args()

    # Determine handoff destination based on mode (project vs course)
    if getattr(args, "course", None):
        # Validate slug – no path separators or parent refs
        slug = args.course.strip()
        if "/" in slug or "\\" in slug or slug in (".", ".."):
            print(f"Error: slug de curso '{slug}' contiene separadores de ruta o '..'", file=sys.stderr)
            sys.exit(2)
        # Ensure the studies/<slug>/ directory exists
        course_dir = WORKSPACE / "studies" / slug
        if not course_dir.is_dir():
            print(f"Error: el directorio de estudio '{course_dir}' no existe", file=sys.stderr)
            sys.exit(2)
        target = course_dir / "HANDOFF.md"
    else:
        target = resolve_handoff_path(args.project, args.handoff_dir or None)
    content = build_handoff(args)

    target.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    # B6 (2026-10-12): varias sesiones cierran sobre el MISMO repo; el HANDOFF es
    # last-writer-wins. El lock serializa el ciclo para que dos cierres simultaneos
    # no se intercalen. A+C (2026-10-13): el mismo lock cubre el backup del HANDOFF
    # previo (A) y el append al indice de sesiones (C), asi el orden
    # backup -> index -> replace es consistente entre cierres concurrentes.
    # Determine if we are merging the general workspace HANDOFF (project alias).
    is_workspace_merge = (
        not getattr(args, "course", None)
        and args.project
        and args.project.lower() in WORKSPACE_ALIASES
    )

    with file_lock(target):
        # For workspace merges we skip the gate (the new content is a merge of
        # the old one, so no pending loss is possible). For project handoffs we
        # keep the original validation behavior.
        if not is_workspace_merge:
            problem = validate_merge_before_write(content, target, args.closed)
            if problem and not args.force_merge:
                print(problem, file=sys.stderr)
                return 3
            if problem and args.force_merge:
                print("AVISO: --force-merge activo; se escriben con perdidas declaradas:",
                      file=sys.stderr)
                print(problem, file=sys.stderr)

        # Prepare content: if workspace merge, combine with existing file.
        final_content = content
        if is_workspace_merge:
            # Load previous file if exists, then merge according to rules.
            prev_text = target.read_text(encoding="utf-8") if target.exists() else ""
            try:
                final_content = merge_workspace_handoff(content, prev_text)
            except Exception as exc:
                # On any parsing error fallback to the plain new content and warn.
                print(f"WARN: merge_workspace_handoff falló ({exc}); se sobrescribe sin merge.",
                      file=sys.stderr)
                final_content = content

        existed = target.exists()
        backup = backup_previous(target, ts) if existed else None
        # Use a label that includes the study prefix when applicable.
        label_for_index = args.project if args.project else f"studies/{args.course}"
        index = append_session_index(target, label_for_index, ts, args.summary)
        tmp = target.with_suffix(".md.tmp")
        tmp.write_text(final_content, encoding="utf-8")
        os.replace(tmp, target)

    action = "actualizado" if existed else "creado"
    print(f"HANDOFF {action}: {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
