#!/bin/bash
# test-skills.sh - Skill validation suite
#
# Usage:
#   ./scripts/test-skills.sh            # scope: SOLO los archivos staged (git diff --cached)
#   ./scripts/test-skills.sh --all      # scope: todo el arbol de skills en disco
#   ./scripts/test-skills.sh --verbose
#   ./scripts/test-skills.sh --quick    # solo sintaxis (bash/python), sin checks de contenido
#
# Checks:
#   A. Sintaxis: bash -n en skills/*/scripts/*.sh, py_compile en *.py
#   B. Frontmatter: todo SKILL.md tiene name, description y metadata.category
#   C. Em dash: aviso. Se prefiere guion comun, pero U+2014/U+2013 NO bloquea
#      (owner rule 2026-11-04: bloquear un commit por tipografia frena trabajo)
#      y el resumen lo cuenta como 'avisos', no como failed.
#   D. Scripts referenciados: todo scripts/foo.sh|py mencionado en SKILL.md existe
#   E. Links a skills: todo enlace a skills/<name> apunta a una skill existente
#
# Scope (2026-10-07): por defecto el suite revisa SOLO los archivos staged del
# commit en curso (`git diff --cached --name-only -z --diff-filter=ACMR`), no
# todo el disco. Motivo: el pre-commit lo invoca en cada commit, y al escanear
# el disco entero bloqueaba commits AJENOS por defectos que no tocaban:
#   - los SKILL.md de playwright-core bajo node_modules/ (3 por copia instalada),
#   - los arboles de skills de agentes todavia no trackeados (staged vacio).
# El sintoma era commits sin relacion forzados a --no-verify. Un check que
# bloquea por lo que no se commitea no es una guarda, es ruido.
# `--all` reproduce el barrido completo (lo que corre el CI, donde no hay
# staging). La segunda barrera en la superficie publica sigue siendo el CI.
#
# node_modules/ se poda del walk (`-prune`) en TODOS los checks, incluido el de
# em dash: antes B/C/D/E no podaban y C fallaba contra el codigo de terceros.
#
# Exit codes: 0 todo ok, 1 hay fallos

set -euo pipefail

WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="${WORKSPACE_DIR}/skills"

# El ciclo de skills vive en DOS arboles (ADR-073): `skills/` (workspace) y
# `agents/<rol>/skills/` (por rol). Este script solo escaneaba el primero, asi
# que las 42 skills de agente no tenian NINGUN check: ni sintaxis, ni
# frontmatter, ni guion, ni scripts referenciados, ni links. Es la misma clase
# de falso verde que el de SKILLS-INDEX (auditoria Nivel 2, 2026-09-29): un
# check que reporta "36 ok" mientras la mitad del arbol no se mira.
AGENT_SKILL_DIRS=()
while IFS= read -r d; do
  [[ -n "$d" ]] && AGENT_SKILL_DIRS+=("$d")
done < <(find "${WORKSPACE_DIR}/agents" -maxdepth 2 -type d -name skills -print 2>/dev/null || true)

if [[ ${#AGENT_SKILL_DIRS[@]} -gt 0 ]]; then
  SKILL_ROOTS=("$SKILLS_DIR" "${AGENT_SKILL_DIRS[@]}")
else
  SKILL_ROOTS=("$SKILLS_DIR")
fi
VERBOSE=0
QUICK=0
SCOPE_ALL=0

for arg in "$@"; do
  case "$arg" in
    --verbose|-v) VERBOSE=1 ;;
    --quick|-q) QUICK=1 ;;
    --all|-a) SCOPE_ALL=1 ;;
  esac
done

# --- SCOPING ---
# Por defecto, solo los archivos staged que caen dentro de un SKILL_ROOT.
# --all barre todo el disco (CI / auditoria manual).
#
# Guarda anti-verde-falso: en CI no hay staging, asi que el scope por defecto
# veria 0 archivos y saldria en verde sin mirar nada. Si el entorno es CI
# (`CI` seteado) y no se pidio --all, se aborta en vez de reportar un verde
# hueco. Un gate que se puede convertir en no-op por omision es la misma clase
# de falso verde que este workspace ya registro (Etapa 2: artefactos que
# existen y nadie invoca).
if [[ $SCOPE_ALL -eq 0 && -n "${CI:-}" ]]; then
  echo "ABORT: CI debe invocar test-skills.sh --all (sin --all el scope staged seria 0 archivos)." >&2
  exit 1
fi
#
# Se usa NUL como separador (`-z` / `read -d ''`) para tolerar paths con
# espacios; ademas se filtra por prefijo contra cada SKILL_ROOT real, asi que
# un cambio en scripts/ (que dispara el hook) no mete archivos fuera del arbol
# de skills en el scope.
in_scope() {
  local abs="$1" r
  for r in "${SKILL_ROOTS[@]}"; do
    [[ "$abs" == "$r/"* ]] && return 0
  done
  return 1
}

CANDIDATES=()
if [[ $SCOPE_ALL -eq 1 ]]; then
  while IFS= read -r -d '' f; do
    CANDIDATES+=("$f")
  done < <(find "${SKILL_ROOTS[@]}" -type d -name node_modules -prune -o -type f -print0 2>/dev/null || true)
else
  while IFS= read -r -d '' f; do
    abs="${WORKSPACE_DIR}/${f}"
    [[ -f "$abs" ]] || continue
    in_scope "$abs" || continue
    CANDIDATES+=("$abs")
  done < <(git -C "$WORKSPACE_DIR" diff --cached --name-only -z --diff-filter=ACMR 2>/dev/null || true)
fi

if [[ $SCOPE_ALL -eq 1 ]]; then
  echo "Scope: all skill tree on disk"
else
  echo "Scope: staged only (${#CANDIDATES[@]} file(s) under skill roots)"
fi

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

# Excepciones de links a skills (seccion E). Mismo criterio que ALLOWLIST_REF:
# la referencia es un ejemplo ilustrativo, no una promesa sobre este arbol.
#   spec-driven-development es la skill-PLANTILLA del formato de spec: su tabla
#   "Related Documents" muestra rutas de un proyecto DESTINO (REQ-001,
#   tests/registration.test.ts, una API y mockups que el proyecto describira),
#   no archivos de este workspace. Exigir que existan convertiria la plantilla
#   en una promesa falsa. Los otros links de la seccion si son vivos.
ALLOWLIST_LINK=(
  "agents/kanam-dev/skills/spec-driven-development/SKILL.md|../docs/adr/adr-001-state-management.md"
  "agents/kanam-dev/skills/spec-driven-development/SKILL.md|../../api/docs/openapi.json"
  "agents/kanam-dev/skills/spec-driven-development/SKILL.md|../design/mockups/"
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

is_skill_md() { [[ "$(basename "$1")" == "SKILL.md" ]]; }

# --- A. Sintaxis bash/python ---
# Los candidatos ya vienen podados de node_modules (find -prune) y scoped
# (staged o --all); solo se filtra por extension.
for file in "${CANDIDATES[@]+"${CANDIDATES[@]}"}"; do
  case "$file" in
    *.sh)
      if bash -n "$file" 2>/tmp/bash.err; then
        BASH_OK=$((BASH_OK + 1))
        note "✅ bash OK: $file"
      else
        BASH_FAIL=$((BASH_FAIL + 1))
        echo "  ❌ bash FAIL: $file"
        sed 's/^/      /' /tmp/bash.err
        failures+=("$file")
      fi
      ;;
    *.py)
      if python3 -m py_compile "$file" 2>/tmp/python.err; then
        PYTHON_OK=$((PYTHON_OK + 1))
        note "✅ python OK: $file"
      else
        PYTHON_FAIL=$((PYTHON_FAIL + 1))
        echo "  ❌ python FAIL: $file"
        sed 's/^/      /' /tmp/python.err
        failures+=("$file")
      fi
      ;;
  esac
done

rm -f /tmp/bash.err /tmp/python.err

# --- Checks de contenido (se pueden saltar con --quick) ---
if [[ $QUICK -eq 0 ]]; then

  # --- B. Frontmatter ---
  for skmd in "${CANDIDATES[@]+"${CANDIDATES[@]}"}"; do
    is_skill_md "$skmd" || continue
    if head -1 "$skmd" | grep -q '^---$'; then
      FM_OK=$((FM_OK + 1))
    else
      FM_FAIL=$((FM_FAIL + 1))
      echo "  ❌ frontmatter FAIL (sin bloque ---): $skmd"
      failures+=("$skmd")
    fi
  done

  # --- C. Em dash (U+2014/U+2013) ---
  # Usa python3 (portable): grep -P no existe en BSD grep de macOS, lo que
  # daba falsos OK locales y fallos en CI Linux. Python detecta en ambos.
  # El scope (staged por defecto) + el prune de node_modules es lo que evita
  # que los guiones del codigo de playwright tumben un commit ajeno.
  for skmd in "${CANDIDATES[@]+"${CANDIDATES[@]}"}"; do
    is_skill_md "$skmd" || continue
    if python3 -c 'import sys; c=open(sys.argv[1],encoding="utf-8").read(); sys.exit(1 if ("\u2013" in c or "\u2014" in c) else 0)' "$skmd" 2>/dev/null; then
      DASH_OK=$((DASH_OK + 1))
    else
      DASH_FAIL=$((DASH_FAIL + 1))
      # AVISO, no veto (owner rule 2026-11-04): el guion largo es estilo, no
      # correccion. Bloquear un commit entero por tipografia detiene trabajo
      # legitimo; el gate informa y el commit sigue.
      echo "  ⚠️  em dash (guion largo, no bloquea): $skmd"
    fi
  done

  # --- D. Scripts referenciados existen ---
  # Resuelve tres patrones:
  #   - relativos: ./scripts/foo.sh (con ./ explicito) o scripts/foo.sh tras pipe/espacio
  #   - cross-skill con prefijo: skills/<otra>/scripts/foo.sh
  #   - cross-skill sin prefijo: <otra-skill>/scripts/foo.sh
  # Excluye bloques de codigo (```) - ahi los scripts son ejemplos ilustrativos.
  for skmd in "${CANDIDATES[@]+"${CANDIDATES[@]}"}"; do
    is_skill_md "$skmd" || continue
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
  done

  # --- E. Links markdown relativos a skills existen ---
  # Resuelve el link relativo contra el directorio real del SKILL.md, que es
  # como lo resuelve markdown. Antes solo matcheaba `](../<skill>)` de un solo
  # nivel: al mover skills a agents/<rol>/skills/ los links validos pasaron a
  # ser `](../../agents/...)` y el check dejaba de verlos (verde sobre links
  # rotos). Resolver el path de verdad cubre ambas formas sin enumerarlas.
  # No matchea texto plano (paths en bloques de codigo, menciones sueltas).
  for skmd in "${CANDIDATES[@]+"${CANDIDATES[@]}"}"; do
    is_skill_md "$skmd" || continue
    skill_dir="$(dirname "$skmd")"
    while read -r ref; do
      [[ -z "$ref" ]] && continue
      case "$ref" in
        *'<'*|*'>'*|*'#'*) continue ;;  # placeholder o ancla, no una ruta
      esac
      if [[ -e "$skill_dir/$ref" ]]; then
        LINK_OK=$((LINK_OK + 1))
      else
        # check allowlist antes de fallar (mismo criterio que ALLOWLIST_REF)
        allowed=0
        for entry in "${ALLOWLIST_LINK[@]}"; do
          entry_file="${entry%%|*}"
          entry_ref="${entry##*|}"
          if [[ "$skmd" == "$WORKSPACE_DIR/$entry_file" && "$ref" == "$entry_ref" ]]; then
            allowed=1
            break
          fi
        done
        if [[ $allowed -eq 1 ]]; then
          LINK_OK=$((LINK_OK + 1))
        else
          LINK_FAIL=$((LINK_FAIL + 1))
          echo "  ❌ skill link FAIL: $skmd -> $ref"
          failures+=("$skmd -> $ref")
        fi
      fi
    done < <(grep -oE '\]\(\.\./[^) ]+' "$skmd" 2>/dev/null | sed -E 's/^\]\(//' | sort -u || true)
  done

fi

# --- Resumen ---
echo ""
echo "Skill validation complete"
echo "  Bash:      $BASH_OK passed, $BASH_FAIL failed"
echo "  Python:    $PYTHON_OK passed, $PYTHON_FAIL failed"
if [[ $QUICK -eq 0 ]]; then
  echo "  Frontmatter: $FM_OK ok, $FM_FAIL failed"
  echo "  Em dash:     $DASH_OK ok, $DASH_FAIL aviso(s)"
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
