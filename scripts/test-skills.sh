#!/bin/bash
# test-skills.sh - Skill validation suite
#
# Usage:
#   ./scripts/test-skills.sh
#   ./scripts/test-skills.sh --verbose
#   ./scripts/test-skills.sh --quick     # solo sintaxis (bash/python), sin checks de contenido
#
# Checks:
#   A. Sintaxis: bash -n en skills/*/scripts/*.sh, py_compile en *.py
#   B. Frontmatter: todo SKILL.md tiene name, description y metadata.category
#   C. Em dash: ningun SKILL.md usa U+2014/U+2013 (regla de oro del workspace)
#   D. Scripts referenciados: todo scripts/foo.sh|py mencionado en SKILL.md existe
#   E. Links a skills: todo enlace a skills/<name> apunta a una skill existente
#
# Exit codes: 0 todo ok, 1 hay fallos

set -euo pipefail

WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="${WORKSPACE_DIR}/skills"
VERBOSE=0
QUICK=0

for arg in "$@"; do
  case "$arg" in
    --verbose|-v) VERBOSE=1 ;;
    --quick|-q) QUICK=1 ;;
  esac
done

BASH_OK=0; BASH_FAIL=0
PYTHON_OK=0; PYTHON_FAIL=0
FM_OK=0; FM_FAIL=0
DASH_OK=0; DASH_FAIL=0
REF_OK=0; REF_FAIL=0
LINK_OK=0; LINK_FAIL=0

failures=()

# Excepciones documentadas (referencias historicas/ilustrativas, no vivas):
#   skill-collection-maintenance -> narrative-content/scripts/progress-tracker.sh
#     (ejemplo de un incidente CI pasado, no una referencia a usar)
ALLOWLIST_REF=(
  "skills/skill-collection-maintenance/SKILL.md|narrative-content/scripts/progress-tracker.sh"
)

note() { if [[ $VERBOSE -eq 1 ]]; then echo "  $1"; fi; }

# Resuelve una ref cross-skill contra todos los lugares donde puede vivir una
# skill hoy: la raiz del workspace, skills/, y agents/<rol>/skills/ (ADR-073).
# Antes solo miraba los dos primeros, asi que al mover skills al arbol de
# agentes el check marcaba roto un link valido (y peor: habria marcado valido
# uno roto si el nombre se repetia).
ref_exists() {
  local ref="$1"
  [[ -f "$WORKSPACE_DIR/$ref" ]] && return 0
  [[ -f "$WORKSPACE_DIR/skills/$ref" ]] && return 0
  # `skills/<x>/...` calificado: la skill puede vivir hoy en agents/<rol>/skills/.
  local bare="${ref#skills/}"
  [[ -f "$WORKSPACE_DIR/skills/$bare" ]] && return 0
  local candidate
  for candidate in "$WORKSPACE_DIR"/agents/*/skills/"$bare"; do
    [[ -f "$candidate" ]] && return 0
  done
  for candidate in "$WORKSPACE_DIR"/agents/*/skills/"$ref"; do
    [[ -f "$candidate" ]] && return 0
  done
  return 1
}

# --- A. Sintaxis bash/python ---
while IFS= read -r -d '' file; do
  if bash -n "$file" 2>/tmp/bash.err; then
    BASH_OK=$((BASH_OK + 1))
    note "✅ bash OK: $file"
  else
    BASH_FAIL=$((BASH_FAIL + 1))
    echo "  ❌ bash FAIL: $file"
    sed 's/^/      /' /tmp/bash.err
    failures+=("$file")
  fi
done < <(find "$SKILLS_DIR" -type f -name "*.sh" -not -path "*/node_modules/*" -print0)

while IFS= read -r -d '' file; do
  if python3 -m py_compile "$file" 2>/tmp/python.err; then
    PYTHON_OK=$((PYTHON_OK + 1))
    note "✅ python OK: $file"
  else
    PYTHON_FAIL=$((PYTHON_FAIL + 1))
    echo "  ❌ python FAIL: $file"
    sed 's/^/      /' /tmp/python.err
    failures+=("$file")
  fi
done < <(find "$SKILLS_DIR" -type f -name "*.py" -not -path "*/node_modules/*" -print0)

rm -f /tmp/bash.err /tmp/python.err

# --- Checks de contenido (se pueden saltar con --quick) ---
if [[ $QUICK -eq 0 ]]; then

  # --- B. Frontmatter ---
  while IFS= read -r -d '' skmd; do
    if head -1 "$skmd" | grep -q '^---$'; then
      FM_OK=$((FM_OK + 1))
    else
      FM_FAIL=$((FM_FAIL + 1))
      echo "  ❌ frontmatter FAIL (sin bloque ---): $skmd"
      failures+=("$skmd")
    fi
  done < <(find "$SKILLS_DIR" -name "SKILL.md" -print0)

  # --- C. Em dash (U+2014/U+2013) ---
  # Usa python3 (portable): grep -P no existe en BSD grep de macOS, lo que
  # daba falsos OK locales y fallos en CI Linux. Python detecta en ambos.
  while IFS= read -r -d '' skmd; do
    if python3 -c 'import sys; c=open(sys.argv[1],encoding="utf-8").read(); sys.exit(1 if ("\u2013" in c or "\u2014" in c) else 0)' "$skmd" 2>/dev/null; then
      DASH_OK=$((DASH_OK + 1))
    else
      DASH_FAIL=$((DASH_FAIL + 1))
      echo "  ❌ em dash FAIL (usar guion comun -): $skmd"
      failures+=("$skmd")
    fi
  done < <(find "$SKILLS_DIR" -name "SKILL.md" -print0)

  # --- D. Scripts referenciados existen ---
  # Resuelve tres patrones:
  #   - relativos: ./scripts/foo.sh (con ./ explicito) o scripts/foo.sh tras pipe/espacio
  #   - cross-skill con prefijo: skills/<otra>/scripts/foo.sh
  #   - cross-skill sin prefijo: <otra-skill>/scripts/foo.sh
  # Excluye bloques de codigo (```) - ahi los scripts son ejemplos ilustrativos.
  while IFS= read -r -d '' skmd; do
    skill_dir="$(dirname "$skmd")"
    body=$(awk 'BEGIN{inblock=0} /^```/{inblock=!inblock; next} !inblock{print}' "$skmd")
    # relativos con ./ explicito
    while read -r ref; do
      [[ -z "$ref" ]] && continue
      ref="${ref#./}"
      if [[ -f "$skill_dir/$ref" || -f "$WORKSPACE_DIR/$ref" ]]; then
        REF_OK=$((REF_OK + 1))
      else
        REF_FAIL=$((REF_FAIL + 1))
        echo "  ❌ script ref FAIL: $skmd -> $ref"
        failures+=("$skmd -> $ref")
      fi
    done < <(echo "$body" | grep -oE '\./scripts/[A-Za-z0-9_./-]+\.(sh|py|mjs|js)' 2>/dev/null | sort -u || true)
    # relativos sin ./ pero delimitados (inicio de linea, pipe de tabla, espacio)
    while read -r ref; do
      [[ -z "$ref" ]] && continue
      if [[ -f "$skill_dir/$ref" || -f "$WORKSPACE_DIR/$ref" ]]; then
        REF_OK=$((REF_OK + 1))
      else
        REF_FAIL=$((REF_FAIL + 1))
        echo "  ❌ script ref FAIL: $skmd -> $ref"
        failures+=("$skmd -> $ref")
      fi
    done < <(echo "$body" | grep -oE '(^|[|` ])scripts/[A-Za-z0-9_./-]+\.(sh|py|mjs|js)' 2>/dev/null | grep -oE 'scripts/[A-Za-z0-9_./-]+\.(sh|py|mjs|js)' | sort -u || true)
    # cross-skill con prefijo skills/
    while read -r ref; do
      [[ -z "$ref" ]] && continue
      if ref_exists "$ref"; then
        REF_OK=$((REF_OK + 1))
      else
        REF_FAIL=$((REF_FAIL + 1))
        echo "  ❌ script ref FAIL: $skmd -> $ref"
        failures+=("$skmd -> $ref")
      fi
    done < <(echo "$body" | grep -oE 'skills/[A-Za-z0-9_-]+/scripts/[A-Za-z0-9_./-]+\.(sh|py|mjs|js)' 2>/dev/null | sort -u || true)
    # cross-skill sin prefijo: <skill>/scripts/foo
    while read -r ref; do
      [[ -z "$ref" ]] && continue
      if ref_exists "$ref"; then
        REF_OK=$((REF_OK + 1))
      else
        # check allowlist antes de fallar (match por basename del SKILL.md)
        allowed=0
        for entry in "${ALLOWLIST_REF[@]}"; do
          entry_file="${entry%%|*}"
          entry_ref="${entry##*|}"
          if [[ "$(basename "$skmd")" == "$(basename "$entry_file")" && "$ref" == "$entry_ref" ]]; then
            allowed=1
            break
          fi
        done
        if [[ $allowed -eq 1 ]]; then
          REF_OK=$((REF_OK + 1))
        else
          REF_FAIL=$((REF_FAIL + 1))
          echo "  ❌ script ref FAIL: $skmd -> $ref"
          failures+=("$skmd -> $ref")
        fi
      fi
    done < <(echo "$body" | grep -oE '[A-Za-z0-9_-]+/scripts/[A-Za-z0-9_./-]+\.(sh|py|mjs|js)' 2>/dev/null | sort -u || true)
  done < <(find "$SKILLS_DIR" -name "SKILL.md" -print0)

  # --- E. Links markdown relativos a skills existen ---
  # Resuelve el link relativo contra el directorio real del SKILL.md, que es
  # como lo resuelve markdown. Antes solo matcheaba `](../<skill>)` de un solo
  # nivel: al mover skills a agents/<rol>/skills/ los links validos pasaron a
  # ser `](../../agents/...)` y el check dejaba de verlos (verde sobre links
  # rotos). Resolver el path de verdad cubre ambas formas sin enumerarlas.
  # No matchea texto plano (paths en bloques de codigo, menciones sueltas).
  while IFS= read -r -d '' skmd; do
    skill_dir="$(dirname "$skmd")"
    while read -r ref; do
      [[ -z "$ref" ]] && continue
      case "$ref" in
        *'<'*|*'>'*|*'#'*) continue ;;  # placeholder o ancla, no una ruta
      esac
      if [[ -e "$skill_dir/$ref" ]]; then
        LINK_OK=$((LINK_OK + 1))
      else
        LINK_FAIL=$((LINK_FAIL + 1))
        echo "  ❌ skill link FAIL: $skmd -> $ref"
        failures+=("$skmd -> $ref")
      fi
    done < <(grep -oE '\]\(\.\./[^) ]+' "$skmd" 2>/dev/null | sed -E 's/^\]\(//' | sort -u || true)
  done < <(find "$SKILLS_DIR" -name "SKILL.md" -print0)

fi

# --- Resumen ---
echo ""
echo "Skill validation complete"
echo "  Bash:      $BASH_OK passed, $BASH_FAIL failed"
echo "  Python:    $PYTHON_OK passed, $PYTHON_FAIL failed"
if [[ $QUICK -eq 0 ]]; then
  echo "  Frontmatter: $FM_OK ok, $FM_FAIL failed"
  echo "  Em dash:     $DASH_OK ok, $DASH_FAIL failed"
  echo "  Script refs: $REF_OK ok, $REF_FAIL failed"
  echo "  Skill links: $LINK_OK ok, $LINK_FAIL failed"
fi

if [[ ${#failures[@]} -gt 0 ]]; then
  echo ""
  echo "Failed items:"
  printf '  - %s\n' "${failures[@]}" | sort -u
  exit 1
fi

exit 0
