#!/usr/bin/env python3
"""
check-linkedin-pipeline.py - El gate de la cadena OSS -> LinkedIn.

POR QUE EXISTE (2026-10-22). La skill `linkedin-merge-post` (workshop de MIND) exige en su
paso 6 "clear both publish gates": el escaneo de guiones largos y un "anti-ai pass" de
`skills/anti-ai`. **Ese gate no existe**: la skill `anti-ai` fue eliminada el 2026-09-22 en la
reestructuracion (16 stubs vacios) y para entonces ya era un placeholder que decía "the detailed
implementation has been merged into other skills". O sea: la referencia es muerta y el paso 6 es
inejecutable tal como esta escrito. La cadena de posts, que es una de las tres acciones del
ROADMAP 2.2, no tiene gate.

Este script restituye el gate. **No inventa las reglas: las recupera del historial.** La version
original de `skills/anti-ai` (commit c0182f17, recuperada con `git show`) define 6 categorias de
deteccion y un flujo de 5 pasos. Este script convierte las categorias verificables en chequeos
automaticos, y deja lo que no se puede verificar en elAutomated como advertencia.

Que verifica:

  MODO POST (--post <archivo>), el gate de publicacion de UN post:
  1. GUIONES: em dash / en dash prohibidos (misma regla que `check_em_dash.py`, reusada).
  2. ESTRUCTURA: el header tiene los campos que el post canonico declara.
  3. IDIOMA: el post esta en ingles (el contenido publicable va en ingles; el reporte a Gonzo,
     en espanol - regla de AGENTS.md).
  4. LONGITUD: el post cae en la ventana que el canonico declara (250-350 palabras).
  5. PATRONES: las 6 categorias del `anti-ai` original, como ADVERTENCIA con conteo.

  MODO AUDIT (por defecto), el gate de CIERRE de la cadena:
  6. DRAFTS VENCIDOS: un post en `draft` que lleva mas de N dias esperando.
  7. MERGES ELEGIBLES SIN POST: un PR mergeado propio (la DB `contributions` es la fuente) que no
     tiene post. Esto es lo que el ROADMAP 2.2 mide como "1 post por merge dentro de la semana".

FALLA (exit 1) en lo que es innegociable: guiones largos, estructura rota, idioma incorrecto, y
los dos fallos de cierre (draft vencido, merge sin post). AVISA sin fallar en los patrones de
lenguaje: "realm" en un post real puede ser la palabra correcta, y un gate que llama plaga a un
post canonico no es un gate.

Uso:
  python3 scripts/check-linkedin-pipeline.py --post docs/linkedin/astryx-5419.md
  python3 scripts/check-linkedin-pipeline.py --post <archivo> --stale-days 14
  python3 scripts/check-linkedin-pipeline.py            # audita toda la cadena
  python3 scripts/check-linkedin-pipeline.py --audit-only

Salida: exit 0 si todo pasa, 1 si encuentra algo que hay que arreglar.
"""
import argparse
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "docs" / "linkedin"
DB = ROOT / "memory" / "memory.db"

# La ventana de longitud que declara el post canonico (astryx-5419.md, "Notas para futuros posts").
MIN_WORDS = 250
MAX_WORDS = 350

# Dias sin publicar antes de que un draft se considere vencido. El backlog medido el 2026-10-22
# tenia drafts de 21 dias: ese es el numero que hay que bajar, no el que hay que(extender).
DEFAULT_STALE_DAYS = 14

# Campos del header. La skill (paso 5) declara "Nicho / Project / PR + merge date / Date /
# Status / Idioma", pero los 10 posts existentes no coinciden: 4 usan espanol ("Nicho",
# "Proyecto"), 3 usan ingles ("Niche", "Project") y 4 no declaran Status. Un gate que reprima
# al post canonico esta roto, asi que:
#   - INNEGOCIABLES: el Status (sin el no hay flip a publicado ni se sabe si es borrador) y el
#     nicho (sin el no se sabe a que pilar de branding pertenece).
#   - El proyecto NO es innegociable: se deduce del link del PR, que si es obligatorio.
# Se aceptan las dos grafias de cada campo.
REQUIRED_HEADER_PATTERNS = {
    "Status": r"\*\*Status",
    "Nicho": r"\*\*(Nicho|Niche)",
}

# --- Las 6 categorias del `anti-ai` original (commit c0182f17) ---------------------------
# Se verifican como ADVERTENCIA: son señales de estilo, no hechos. Un post canonico puede
# contener una de estas palabras con razón.
PATTERN_CATEGORIES = [
    (
        "1. Muletillas de transicion",
        r"\b(however,|furthermore,|additionally,|in conclusion|on the other hand|"
        r"it'?s important to note|worth mentioning|it'?s worth noting|needless to say)\b",
    ),
    (
        "2. Estructuras predecibles",
        r"\b(in today'?s (world|fast-paced|modern)|in the era of|in an increasingly|"
        r"now more than ever|it'?s no secret that)\b",
    ),
    (
        "3. Adverbios y relleno",
        r"\b(effectively,|certainly,|undoubtedly,|arguably,|remarkably,|notably,)\b",
    ),
    (
        "4. Falsas precisiones",
        r"\b(approximately|around [0-9]|almost [0-9]|roughly [0-9])\b",
    ),
    (
        "5. Cierre generico",
        r"\b(in summary|to conclude|to sum up|i hope this helps|feel free to (reach out|contact|ask)|"
        r"don'?t hesitate to (reach out|contact|ask)|let me know if)\b",
    ),
]

# Palabras que delatan texto generado. Advertencia, no fallo: aparecen en prosa legitima.
SLOP_WORDS = [
    "delve", "tapestry", "landscape", "testament", "pivotal", "seamless", "leverage",
    "harness", "unlock", "game-chang", "navigate the", "robust solution", "elevate",
]

EM_DASH = "\u2014"
EN_DASH = "\u2013"

# Guiones y espacios "invisibles": no los ve el lector pero se copian. El gate de guiones largo
# (`check_em_dash.py`) solo mira U+2014 y U+2013, asi que estos pasaban. Medido el 2026-10-22 en
# los 2 posts que escribio MIND: 10 y 9 guiones no separables (U+2011) + 8 espacios angostos
# (U+202F). Los 10 posts canonicos tienen CERO de estos. Son el mismo defecto que el em dash:
# un texto que se ve bien y no lo esta.
INVISIBLE_GLYPHS = {
    "\u2011": "guion no separable (U+2011)",
    "\u202f": "espacio angosto (U+202F)",
    "\u00a0": "espacio duro (U+00A0)",
}


def _post_body(text: str) -> str:
    """El contenido publicable: lo que va despues del header, sin las notas para Gonzo.

    El post canonico tiene tres bloques (header / post / notas). Solo el del medio se publica.
    """
    # Recorta desde "## Notas" si existe: esas notas son para Gonzo, no para LinkedIn.
    text = re.split(r"^##\s+(Notas|Notes|Notas para Gonzo)", text, maxsplit=1, flags=re.M)[0]
    # Si hay un bloque "## Post" o "## Draft", tomalo desde ahi.
    m = re.search(r"^##\s+(Post|Draft|Post \(.*?\))", text, flags=re.M)
    if m:
        text = text[m.end():]
    return text


def _header(text: str) -> str:
    """El bloque de header: hasta el primer H2."""
    parts = re.split(r"^##\s+", text, maxsplit=1, flags=re.M)
    return parts[0]


def check_post(path: Path, stale_days: int) -> tuple[list[str], list[str]]:
    """Valida un post. Devuelve (problemas, advertencias).

    Acepta `-` como path: en ese caso lee el texto de stdin. Lo necesita el pre-commit,
    que valida el contenido STAGED (lo que se commitea), no el del disco.
    """
    problems: list[str] = []
    warnings: list[str] = []

    if str(path) == "-":
        text = sys.stdin.read()
    else:
        if not path.exists():
            return [f"No existe: {path}"], []
        text = path.read_text(encoding="utf-8")

    header = _header(text)
    body = _post_body(text)

    # 1. Guiones largos. Innegociable (regla de Gonzo).
    em = text.count(EM_DASH)
    en = text.count(EN_DASH)
    if em or en:
        problems.append(
            f"Guiones largos: {em} em dash (U+2014) y {en} en dash (U+2013). "
            f"Usar guion comun (-) SIEMPRE."
        )

    # 1b. Guiones y espacios invisibles. Innegociables por la misma razon que el em dash.
    invisible = {name: text.count(ch) for ch, name in INVISIBLE_GLYPHS.items() if text.count(ch)}
    if invisible:
        detalle = ", ".join(f"{n} {name}" for name, n in invisible.items())
        problems.append(
            f"Caracteres invisibles: {detalle}. Se ven bien pero no lo estan: usar guion comun (-) "
            f"y espacio normal."
        )

    # 2. Estructura del header.
    for field, pattern in REQUIRED_HEADER_PATTERNS.items():
        if not re.search(pattern, header):
            problems.append(f"El header no declara el campo '{field}'.")

    # 2b. El PR tiene que estar citado: sin el link no hay trazabilidad del merge.
    if not re.search(r"pull/\d+", body):
        problems.append(
            "El cuerpo no cita el PR (falta un link '.../pull/<n>'). Sin el, el post no es "
            "trazable al merge que lo origina."
        )

    # 3. Idioma: el cuerpo publicable va en ingles.
    spanish_markers = len(re.findall(r"\b(el|la|los|las|de|que|para|con|una|por)\b", body.lower()))
    english_words = len(re.findall(r"\b[a-zA-Z]+\b", body))
    if english_words and spanish_markers / max(english_words, 1) > 0.12:
        problems.append(
            f"El cuerpo parece estar en espanol ({spanish_markers} marcadores / {english_words} "
            f"palabras). El post publicable va en ingles; el reporte a Gonzo, en espanol."
        )

    # 4. Longitud.
    words = len(re.findall(r"\b[a-zA-Z][a-zA-Z'-]*\b", body))
    if words and not (MIN_WORDS <= words <= MAX_WORDS):
        warnings.append(
            f"Longitud: {words} palabras, fuera de la ventana que declara el canonico "
            f"({MIN_WORDS}-{MAX_WORDS})."
        )

    # 5. Patrones del anti-ai original. Advertencia, no fallo.
    for label, pattern in PATTERN_CATEGORIES:
        hits = re.findall(pattern, body, flags=re.I)
        if hits:
            uniq = sorted({h.strip(",.").lower() for h in hits})
            warnings.append(f"{label}: {len(hits)} instancia(s) -> {', '.join(uniq[:5])}")

    slop_hits = [w for w in SLOP_WORDS if w in body.lower()]
    if slop_hits:
        warnings.append(f"Palabras de texto generado: {', '.join(slop_hits[:6])}")

    # 6. Estado declarado.
    if re.search(r"\*\*Status:\*\*\s*(draft|BORRADOR)", header, flags=re.I):
        warnings.append("El post sigue en draft: necesita OK de Gonzo y flip del Status a publicado.")

    return problems, warnings


def audit_chain(stale_days: int, root: Path = None) -> list[str]:
    """El gate de cierre: drafts vencidos y merges elegibles sin post.

    `root` es inyectable (misma convencion que los otros guards del workspace: las rutas son
    inyectables para que los tests construyan arboles falsos). Por defecto, la raiz del repo.
    """
    problems: list[str] = []
    now = datetime.now(timezone.utc)

    root = Path(root) if root is not None else ROOT
    posts_dir = root / "docs" / "linkedin"
    db_path = root / "memory" / "memory.db"

    if not posts_dir.exists():
        return [f"No existe el directorio de posts: {posts_dir}"]

    posts = sorted(posts_dir.glob("*.md"))
    if not posts:
        return [f"No hay posts en {POSTS_DIR}"]

    # 6. Drafts vencidos.
    for p in posts:
        text = p.read_text(encoding="utf-8")
        header = _header(text)
        if not re.search(r"\*\*Status:\*\*\s*(draft|BORRADOR)", header, flags=re.I):
            continue
        mtime = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc)
        age = (now - mtime).days
        if age >= stale_days:
            problems.append(
                f"Draft vencido: {p.name} lleva {age} dias esperando publicacion "
                f"(umbral: {stale_days} dias)."
            )

    # 7. Merges elegibles sin post.
    if not db_path.exists():
        problems.append(f"No existe la DB de memoria: {db_path}")
        return problems

    try:
        con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        merged = con.execute(
            "select repo, pr from contributions where status='merged' and tipo='pr'"
        ).fetchall()
    except sqlite3.Error as e:
        problems.append(f"No se pudo leer la DB de memoria: {e}")
        return problems

    # El texto de todos los posts, para buscar el numero de PR.
    corpus = "\n".join(p.read_text(encoding="utf-8") for p in posts)

    missing = []
    for repo, pr in merged:
        num = (pr or "").lstrip("#")
        if not num:
            continue
        # El post tiene que citar el PR. Se acepta la forma con o sin #.
        if not re.search(rf"(pull/{num}\b|#{num}\b)", corpus):
            missing.append(f"{repo}#{num}")

    if missing:
        problems.append(
            f"Merges elegibles sin post ({len(missing)}): {', '.join(sorted(missing))}. "
            f"El ROADMAP 2.2 mide '1 post por merge dentro de la semana'."
        )

    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description="Gate de la cadena OSS -> LinkedIn.")
    ap.add_argument("--post", help="Archivo de post a validar (el gate de publicacion).")
    ap.add_argument("--stale-days", type=int, default=DEFAULT_STALE_DAYS,
                    help=f"Dias sin publicar para que un draft cuente como vencido "
                         f"(default {DEFAULT_STALE_DAYS}).")
    ap.add_argument("--audit-only", action="store_true",
                    help="Solo auditar la cadena, sin validar un post puntual.")
    args = ap.parse_args()

    if args.post:
        if args.post == "-":
            path = Path("-")
        else:
            path = Path(args.post)
            if not path.is_absolute():
                path = ROOT / args.post
        problems, warnings = check_post(path, args.stale_days)
        print(f"Gate de post: {path}")
        if problems:
            print("\nFALLA:")
            for p in problems:
                print(f"  - {p}")
        else:
            print("  OK: guiones, estructura, idioma y longitud.")
        if warnings:
            print("\nAVISA (no bloquea):")
            for w in warnings:
                print(f"  - {w}")
        if not args.audit_only:
            return 1 if problems else 0

    if not args.post or args.audit_only:
        problems = audit_chain(args.stale_days, ROOT)
        print(f"Auditoria de la cadena: {POSTS_DIR}")
        if problems:
            print("\nFALLA:")
            for p in problems:
                print(f"  - {p}")
        else:
            print("  OK: ningun draft vencido, ningun merge elegible sin post.")

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
