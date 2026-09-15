#!/usr/bin/env bash
# publish-skills.sh - Publica skills del workspace (privado) al repo publico kanam-skills.
#
# REGLA DE ORO: el workspace es la FUENTE; el repo publico es un ARTEFACTO generado.
# Este script es el unico camino para publicar: mismo input -> mismo resultado, asi el
# repo no puede volver a divergir del workspace sin que el check lo diga.
#
# Uso:
#   ./scripts/publish-skills.sh --check                  # reporta diferencias (NO escribe)
#   ./scripts/publish-skills.sh --check --group1         # solo skills ya en ingles
#   ./scripts/publish-skills.sh --apply --group1         # publica las que ya estan en EN
#   ./scripts/publish-skills.sh --apply                  # publica todo lo que exista en ambos
#   ./scripts/publish-skills.sh --apply --skill <name>   # una sola skill
#   ./scripts/publish-skills.sh --apply --include-new    # ademas publica skills nuevas
#
# Sanitizacion (ver docs/AGENTS-DETALLE.md):
#   SALE:  datos personales (Gonzo/Gonzalo/gonzoblasco/rutas /Users/) y proyectos internos
#          (a11y-fixer, workspace_openclaw, soporteml, kanam-lab, ...).
#   QUEDA: la marca Kanam (nombre del PRODUCTO publicado, no una identidad personal).
#
# Exit: 0 ok | 1 error de uso | 2 problemas de verificacion.

set -uo pipefail

WS="${HOME}/.openclaw/workspace"
SRC="${WS}/skills"
DST="${WS}/projects/kanam-skills/skills"

MODE="check"; ONLY_SKILL=""; GROUP1=0; INCLUDE_NEW=0

while [ $# -gt 0 ]; do
  case "$1" in
    --check) MODE="check" ;;
    --apply) MODE="apply" ;;
    --skill) ONLY_SKILL="${2:-}"; shift ;;
    --group1) GROUP1=1 ;;
    --include-new) INCLUDE_NEW=1 ;;
    -h|--help) sed -n '2,22p' "$0"; exit 0 ;;
    *) echo "Opcion desconocida: $1" >&2; exit 1 ;;
  esac
  shift
done

[ -d "$SRC" ] || { echo "No existe el origen: $SRC" >&2; exit 1; }
[ -d "$DST" ] || { echo "No existe el destino: $DST" >&2
  echo "Clona primero: git clone git@github.com:gonzoblasco/kanam-skills.git projects/kanam-skills" >&2
  exit 1; }

EXCLUDES=(--exclude '.DS_Store' --exclude '__pycache__' --exclude '*.pyc'
          --exclude 'node_modules' --exclude '.venv' --exclude '*.db' --exclude '.knowledge')

INTERNAL_RE='a11y-fixer|a11y-playground|workspace_openclaw|soporteml|kanam-lab|kanam-pulse|kanam-story|kanam-studio|kanam-forge|kanam-insight|kanam-tetris|kanam-solitaires|projects_openclaw'
PERSONAL_RE='\bGonzo\b|\bGonzalo\b|gonzoblasco|/Users/gonzoblasco'

is_english() {  # $1 = skill name -> 0 si el SKILL.md del workspace esta en ingles
  python3 - "$SRC/$1/SKILL.md" <<'PY'
import re, sys
try:
    t = open(sys.argv[1], encoding="utf-8", errors="ignore").read()
except OSError:
    sys.exit(1)
ES = re.compile(r'\b(usalo|usá|cuando|sesión|también|revisión|código|podés|debés|tenés|para|porque|sobre|después|siempre|nunca|debe|puede)\b', re.I)
EN = re.compile(r'\b(use when|when to use|you should|the |and |with |this is|before |after |always |never |must |should )\b', re.I)
s, e = len(ES.findall(t)), len(EN.findall(t))
if s == 0 and e == 0:
    sys.exit(1)
sys.exit(0 if s / (s + e) < 0.35 else 1)
PY
}

# --- Fase 1: set de skills a evaluar ------------------------------------------
targets=()
if [ -n "$ONLY_SKILL" ]; then
  [ -d "$SRC/$ONLY_SKILL" ] || { echo "No existe la skill: $ONLY_SKILL" >&2; exit 1; }
  targets=("$ONLY_SKILL")
else
  for d in "$DST"/*/; do
    [ -d "$d" ] || continue
    n=$(basename "$d")
    [ -f "$SRC/$n/SKILL.md" ] || continue
    if [ "$GROUP1" = 1 ] && ! is_english "$n"; then continue; fi
    targets+=("$n")
  done
  if [ "$INCLUDE_NEW" = 1 ]; then
    for d in "$SRC"/*/; do
      [ -d "$d" ] || continue
      n=$(basename "$d")
      [ -f "$d/SKILL.md" ] || continue
      [ -d "$DST/$n" ] && continue
      if [ "$GROUP1" = 1 ] && ! is_english "$n"; then continue; fi
      targets+=("$n")
    done
  fi
fi

echo "publish-skills | modo=$MODE | group1=$GROUP1 | skills=${#targets[@]}"
echo

# --- Fase 2: comparar / copiar ------------------------------------------------
same=0; written=0; created=0
for n in "${targets[@]}"; do
  s="$SRC/$n"; t="$DST/$n"

  if [ -d "$t" ] && diff -rq --exclude '.DS_Store' --exclude '__pycache__' --exclude '.knowledge' "$s" "$t" >/dev/null 2>&1; then
    same=$((same+1)); continue
  fi

  if [ "$MODE" = apply ]; then
    if [ ! -d "$t" ]; then created=$((created+1)); else written=$((written+1)); fi
    mkdir -p "$t"
    rsync -a --delete "${EXCLUDES[@]}" "$s"/ "$t"/
  else
    [ -d "$t" ] && written=$((written+1)) || created=$((created+1))
  fi
done

# --- Fase 3: sanitizar (solo apply) -------------------------------------------
# Usa sanitize-skills.py: saca datos personales y proyectos internos, y PRESERVA
# la marca Kanam y la identidad de instalacion del repo (gonzoblasco/kanam-skills).
if [ "$MODE" = apply ]; then
  python3 "$WS/scripts/sanitize-skills.py" "$DST" || true
fi

# --- Fase 4: verificar (siempre) ----------------------------------------------
echo "VERIFICACION"
echo "------------"

p=$(grep -rIlE "$PERSONAL_RE" "$DST" 2>/dev/null | wc -l | tr -d ' ')
echo "  referencias personales: $p"
if [ "$p" -gt 0 ]; then grep -rInE "$PERSONAL_RE" "$DST" 2>/dev/null | head -5; fi

i=$(grep -rIlE "$INTERNAL_RE" "$DST" 2>/dev/null | wc -l | tr -d ' ')
echo "  proyectos internos:     $i"
if [ "$i" -gt 0 ]; then grep -rInE "$INTERNAL_RE" "$DST" 2>/dev/null | head -5; fi

k=$(grep -rI "\bKanam\b" "$DST" 2>/dev/null | wc -l | tr -d ' ')
echo "  marca Kanam (queda):    $k"

dashes=$(python3 - "$DST" <<'PY'
import pathlib, sys
bad = 0
for f in pathlib.Path(sys.argv[1]).rglob("*"):
    if f.is_file() and f.suffix in {".md", ".sh", ".py", ".json", ".yml"}:
        try:
            t = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if "\u2014" in t or "\u2013" in t:
            bad += 1
            print(f"    {f}")
print(f"COUNT={bad}")
PY
)
echo "  em/en dash:             $(printf '%s' "$dashes" | sed -n 's/^COUNT=//p')"
printf '%s' "$dashes" | grep -v '^COUNT=' | sed '/^$/d'

noskill=0
for d in "$DST"/*/; do
  [ -d "$d" ] || continue
  [ -f "$d/SKILL.md" ] || { echo "  SIN SKILL.md: $(basename "$d")"; noskill=$((noskill+1)); }
done
echo "  dirs sin SKILL.md:      $noskill"

problems=0
[ "$p" -gt 0 ] && problems=$((problems+1))
[ "$i" -gt 0 ] && problems=$((problems+1))
[ "$(printf '%s' "$dashes" | sed -n 's/^COUNT=//p')" -gt 0 ] && problems=$((problems+1))
[ "$noskill" -gt 0 ] && problems=$((problems+1))

echo
echo "RESUMEN: iguales=$same  escritas=$written  nuevas=$created  problemas=$problems"
if [ "$MODE" = apply ]; then
  echo "Los cambios quedaron en el working tree del repo publico. Revisar: git -C projects/kanam-skills diff --stat"
else
  echo "Modo check: no se escribio nada."
fi

[ "$problems" -gt 0 ] && exit 2
exit 0
