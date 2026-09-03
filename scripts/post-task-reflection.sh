#!/usr/bin/env bash
# post-task-reflection.sh - Reflexion post-tarea automatica
#
# Nueva etapa del ciclo de vida (2026-09-03): despues de tareas complejas,
# estructura la reflexion, detecta duplicados en la DB, cruza con skills
# existentes via skill-router, y opcionalmente genera una propuesta de skill
# nueva si el patron no esta cubierto.
#
# Complementa (no reemplaza) la self-reflection de session-lifecycle:
#   - session-lifecycle: learnings globales al cerrar sesion (LEARNINGS.md)
#   - este script: reflexion inmediata post-tarea + deteccion de skills
#
# Uso:
#   ./scripts/post-task-reflection.sh --type debug --summary "..." [opciones]
#
# Opciones:
#   --type <tipo>        debug|feature|review|config|research|oss|docs|other
#   --summary "<texto>"   que paso en la tarea (obligatorio)
#   --lesson "<texto>"    leccion aprendida (opcional; si falta, el agente la completa)
#   --category <cat>      categoria de learning (default: auto por tipo)
#   --check-dups          buscar learnings similares en la DB (semantico)
#   --propose-skill       generar propuesta de skill si el patron no esta cubierto
#   --save                persistir el learning en la DB (tabla learnings)
#   --verbose             output detallado
#
# Exit codes: 0 ok, 1 error de uso, 2 fallo interno

set -euo pipefail

WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$WORKSPACE_DIR"

TYPE=""
SUMMARY=""
LESSON=""
CATEGORY=""
CHECK_DUPS=0
PROPOSE_SKILL=0
SAVE=0
VERBOSE=0

usage() {
  sed -n '2,30p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
  exit 1
}

# --- Parse args ---
while [[ $# -gt 0 ]]; do
  case "$1" in
    --type) TYPE="$2"; shift 2 ;;
    --summary) SUMMARY="$2"; shift 2 ;;
    --lesson) LESSON="$2"; shift 2 ;;
    --category) CATEGORY="$2"; shift 2 ;;
    --check-dups) CHECK_DUPS=1; shift ;;
    --propose-skill) PROPOSE_SKILL=1; shift ;;
    --save) SAVE=1; shift ;;
    --verbose) VERBOSE=1; shift ;;
    -h|--help) usage ;;
    *) echo "Unknown option: $1" >&2; usage ;;
  esac
done

if [[ -z "$TYPE" || -z "$SUMMARY" ]]; then
  echo "Error: --type y --summary son obligatorios" >&2
  usage
fi

# --- Mapeo tipo -> categoria default ---
case "$TYPE" in
  debug) DEFAULT_CAT="infraestructura" ;;
  feature) DEFAULT_CAT="proyectos" ;;
  review) DEFAULT_CAT="pipeline-agentes" ;;
  config) DEFAULT_CAT="infraestructura" ;;
  research) DEFAULT_CAT="metodologia" ;;
  oss) DEFAULT_CAT="oss" ;;
  docs) DEFAULT_CAT="metodologia" ;;
  a11y) DEFAULT_CAT="a11y" ;;
  *) DEFAULT_CAT="metodologia" ;;
esac
CATEGORY="${CATEGORY:-$DEFAULT_CAT}"

echo "=============================================="
echo "  Reflexion post-tarea"
echo "=============================================="
echo "  Tipo:      $TYPE"
echo "  Categoria: $CATEGORY"
echo "  Resumen:   $SUMMARY"
[[ -n "$LESSON" ]] && echo "  Leccion:   $LESSON"
echo ""

# --- 1. Skills existentes que cubren el patron ---
echo "--- 1. Skills existentes que cubren el patron ---"
SKILL_HITS=""
if [[ -x "scripts/skill-router.py" ]]; then
  SKILL_HITS=$(python3 scripts/skill-router.py --top 3 "$SUMMARY" 2>/dev/null || true)
  if [[ -n "$SKILL_HITS" ]]; then
    echo "$SKILL_HITS"
  else
    echo "  (skill-router no devolvio resultados)"
  fi
else
  echo "  (skill-router.py no encontrado - skip)"
fi
echo ""

# --- 2. Duplicados en la DB (semantico) ---
if [[ $CHECK_DUPS -eq 1 ]]; then
  echo "--- 2. Learnings similares ya registrados ---"
  if [[ -x "scripts/memory-db.sh" ]]; then
    DUPS=$(./scripts/memory-db.sh search "$SUMMARY" 3 2>/dev/null || true)
    if [[ -n "$DUPS" && "$DUPS" != *"no results"* && "$DUPS" != *"No results"* ]]; then
      echo "$DUPS"
      echo ""
      echo "  ⚠️  Si alguno de estos ya cubre la leccion, no duplicar:"
      echo "      actualizar Recurrence-Count o el learning existente."
    else
      echo "  Sin duplicados semanticos cercanos."
    fi
  else
    echo "  (memory-db.sh no encontrado - skip)"
  fi
  echo ""
fi

# --- 3. Propuesta de skill si el patron no esta cubierto ---
if [[ $PROPOSE_SKILL -eq 1 ]]; then
  echo "--- 3. Deteccion de skill nueva ---"
  # Si skill-router devolvio un match fuerte (score >= 0.6) CON hits keyword (L1),
  # el patron ya esta cubierto. Un match solo-embedding puede ser ruido semantico
  # (ej: godot-mcp 0.77 para migracion de agentes) - no cuenta como cobertura.
  COVERED=0
  if [[ -n "$SKILL_HITS" ]]; then
    # Buscar lineas tipo "1. nombre (score=0.77, embed, L1=2)"
    while IFS= read -r line; do
      score=$(echo "$line" | grep -oE "score=[0-9]+\.[0-9]+" | head -1 | cut -d= -f2)
      l1=$(echo "$line" | grep -oE "L1=[0-9]+" | head -1 | cut -d= -f2)
      if [[ -n "$score" && -n "$l1" ]]; then
        if awk -v s="$score" 'BEGIN{exit !(s >= 0.6)}' && [[ "$l1" -ge 1 ]]; then
          COVERED=1
          echo "  Patron ya cubierto por skill existente (score=$score, L1=$l1)."
          echo "  Si la skill no aplica bien, mejorarla directamente."
          break
        fi
      fi
    done < <(echo "$SKILL_HITS" | grep -E "^\([0-9]+\)\." || true)
    if [[ $COVERED -eq 0 ]]; then
      echo "  Sin cobertura solida (los matches son solo-embedding o debiles)."
    fi
  fi

  if [[ $COVERED -eq 0 ]]; then
    # Derivar slug del summary: primeras palabras significativas
    SLUG=$(echo "$SUMMARY" | tr '[:upper:]' '[:lower:]' \
      | sed 's/[^a-z0-9 ]//g' \
      | awk '{for(i=1;i<=NF;i++) if (length($i)>=4 && $i !~ /^(with|this|that|from|have|were|what|when|your|into|about|after|before|during|using|there|their|which|would|could|should|these|those)$/) printf "%s%s", (n++?",":""), $i; if (n>=3) exit}' \
      | tr ',' '-')
    SLUG="${SLUG:-reflexion-$(date +%s)}"
    PROPOSAL_DIR="skills/_proposals/${SLUG}"
    mkdir -p "$PROPOSAL_DIR"

    cat > "$PROPOSAL_DIR/SKILL.md" << PROPOSAL
---
name: "${SLUG}"
metadata:
  category: "Workflow"
  tags:
    - ${TYPE}
    - reflexion
description: "PROPUESTA AUTOMATICA - patron detectado en tarea de tipo ${TYPE}. Revisar y completar antes de aprobar."
user-invocable: false
---

# Workflow: ${SLUG}

> **Estado: PROPUESTA** - generada por post-task-reflection.sh el $(date '+%Y-%m-%d').
> Revisar con skill_workshop antes de activar. Si ya existe una skill que cubre
> esto, descartar esta propuesta y mejorar la existente.

## Origen de la propuesta

- **Tipo de tarea:** ${TYPE}
- **Resumen:** ${SUMMARY}
$( [[ -n "$LESSON" ]] && echo "- **Leccion:** ${LESSON}" )

## Proposito

<!-- Completar: que problema resuelve esta skill -->

## Cuando usarlo

<!-- Completar: en que situaciones -->

## Pasos

<!-- Completar: el procedimiento -->

## Criterios de exito

<!-- Completar: como saber que funciono -->
PROPOSAL
    echo "  ✅ Propuesta generada: $PROPOSAL_DIR/SKILL.md"
    echo "     Revisarla con skill_workshop antes de activar."
  fi
  echo ""
fi

# --- 4. Persistir learning en la DB ---
if [[ $SAVE -eq 1 ]]; then
  echo "--- 4. Persistir learning en la DB ---"
  if [[ -z "$LESSON" ]]; then
    echo "  ⚠️  --save requiere --lesson. No se persistio nada."
  elif [[ -x "scripts/memory-db.sh" ]]; then
    TAGS="${TYPE},reflexion-post-tarea"
    if ./scripts/memory-db.sh add-learning "$CATEGORY" "$SUMMARY" "$LESSON" "$TAGS" >/dev/null 2>&1; then
      echo "  ✅ Learning guardado en memory.db (categoria: $CATEGORY)"
      echo "     Consultar con: ./scripts/memory-db.sh learnings $CATEGORY"
    else
      echo "  ❌ Fallo al guardar el learning" >&2
      exit 2
    fi
  else
    echo "  (memory-db.sh no encontrado - skip)"
  fi
  echo ""
fi

echo "=============================================="
echo "  Reflexion completa. Siguiente paso:"
echo "  - Si hay leccion nueva -> registrarla (--save) o en docs/LEARNINGS.md"
echo "  - Si hay propuesta de skill -> revisarla con skill_workshop"
echo "=============================================="
exit 0
