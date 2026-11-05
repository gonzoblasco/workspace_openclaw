#!/bin/bash
# model-review.sh - Evaluacion reproducible de un modelo LLM: mide, evalua, escribe.
#
# Hermano de cuento.sh, no copia: mismo patron de etapas con modelos distintos.
#
#   Etapa A (MIDE)      el modelo evaluado corre la bateria. Llama a llm.sh.
#   Etapa B (EVALUA)    un modelo DISTINTO puntua las salidas crudas contra una
#                       fuente de verdad versionada. Un modelo no puede juzgarse
#                       a si mismo: es la razon de ser de esta etapa.
#   Etapa C (REDACTA)   opcional, dos salidas: informe interno y articulo.
#
# Por que B es obligatorio (2026-11-05): Nova-Coder respondio la prueba trampa
# con estructura impecable y el contenido invertido, y nada en su propia salida
# lo delataba. Lo vio un lector que sabia del tema. B es ese lector.
#
# Por que las salidas van CRUDAS a B: pasarle una tabla de metricas oculta el
# contenido. El hallazgo del caso Raft salio de leer la respuesta entera, no del
# conteo de caracteres. Cuesta tokens y vale.
#
# Uso:
#   model-review.sh --model <modelo> [--bateria codigo] [--num-ctx N]
#                   [--salida interna|publica|ambas] [--out DIR] [--dry-run]
#                   [--evaluador TAREA] [--redactor TAREA] [--no-num-predict]
#
# Ejemplo:
#   model-review.sh --model gemma4:12b-mlx --num-ctx 32768 --output docs/articulos/gemma4
#
# Salida por stdout: el informe y/o el articulo.
# Mediciones y JSON de veredicto: en $OUT/metricas.json y $OUT/veredicto.json
# Exit: 0 ok, 2 uso invalido, 4 fallo una etapa.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LLM="$SCRIPT_DIR/llm.sh"
OLLAMA_BASE="${OLLAMA_BASE:-http://127.0.0.1:11434}"
TPL="$SCRIPT_DIR/review-templates"

MODEL=""; BATERIA="codigo"; NUM_CTX=""; SALIDA="ambas"; OUT=""
DRY=0; EVALUADOR="evaluacion"; REDACTOR="redaccion-voz"; NO_NP=""

usage() { sed -n '2,30p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 2; }

while [ $# -gt 0 ]; do
  case "$1" in
    --model)       MODEL="$2"; shift 2 ;;
    --bateria)     BATERIA="$2"; shift 2 ;;
    --num-ctx)     NUM_CTX="$2"; shift 2 ;;
    --out)         OUT="$2"; shift 2 ;;
    --salida)      SALIDA="$2"; shift 2 ;;
    --evaluador)   EVALUADOR="$2"; shift 2 ;;
    --redactor)    REDACTOR="$2"; shift 2 ;;
    --no-num-predict) NO_NP="1"; shift ;;
    --dry-run)     DRY=1; shift ;;
    -h|--help)     usage ;;
    *) echo "model-review.sh: flag desconocida: $1" >&2; exit 2 ;;
  esac
done

[ -n "$MODEL" ] || { echo "model-review.sh: falta --model" >&2; exit 2; }
case "$SALIDA" in interna|publica|ambas) ;; *) echo "model-review.sh: --salida invalida: $SALIDA" >&2; exit 2 ;; esac

BAT_FILE="$TPL/bateria-$BATERIA.md"
VERDAD="$TPL/verdad-consenso.md"
VERDAD2="$TPL/verdad-registro-diagnostico.md"
[ -r "$BAT_FILE" ] || { echo "model-review.sh: no existe la bateria: $BAT_FILE" >&2; exit 4; }

OUT="${OUT:-/tmp/model-review-$BATERIA}"
mkdir -p "$OUT"
FECHA=$(date +%Y-%m-%d)

CTX_ARG=(); [ -n "$NUM_CTX" ] && CTX_ARG=(--num-ctx "$NUM_CTX")
NP_ARG=();  [ -n "$NO_NP" ]   && NP_ARG=(--no-num-predict)

# ---------------------------------------------------------------------------
# Etapa A: partir la bateria en pruebas y correr cada una
# ---------------------------------------------------------------------------
# El parser lee el template y separa por "### id". Se hace en python porque el
# template tiene bloques de codigo con almohadillas que no son titulos.
python3 - "$BAT_FILE" "$OUT" <<'PY' || exit 4
import json, sys, re
path, out = sys.argv[1], sys.argv[2]
text = open(path).read()
parts = re.split(r'^### (\w+)\s*$', text, flags=re.M)
pruebas = []
for i in range(1, len(parts), 2):
    pruebas.append({"id": parts[i], "prompt": parts[i+1].strip()})
json.dump(pruebas, open(f"{out}/pruebas.json", "w"), ensure_ascii=False, indent=1)
print(f"model-review.sh: {len(pruebas)} pruebas en la bateria", file=sys.stderr)
PY

N=$(jq 'length' "$OUT/pruebas.json")

# El contexto DECLARADO por el modelo no es el que le pasamos: es el que trae su
# metadata. Sin esto, una corrida a 32768 hace creer que el modelo declara 32768,
# y la brecha declarado-vs-real -el hallazgo central de una resena- desaparece.
CTX_DECLARADO=$(curl -s "$OLLAMA_BASE/api/show" -d "{\"model\":\"$MODEL\"}" \
  | jq -r '.model_info | to_entries | map(select(.key|endswith(".context_length"))) | .[0].value // "desconocido"' 2>/dev/null)
[ -z "$CTX_DECLARADO" ] && CTX_DECLARADO="desconocido"
echo "$CTX_DECLARADO" > "$OUT/ctx-declarado.txt"
echo "model-review.sh: contexto declarado por el modelo: $CTX_DECLARADO" >&2

if [ "$DRY" = "1" ]; then
  echo "model=$MODEL bateria=$BATERIA pruebas=$N ctx=${NUM_CTX:-<default>} evaluador=$EVALUADOR redactor=$REDACTOR"
  jq -r '.[] | "  - \(.id)"' "$OUT/pruebas.json"
  exit 0
fi

: > "$OUT/mediciones.jsonl"
: > "$OUT/salidas.txt"

i=0
while [ "$i" -lt "$N" ]; do
  ID=$(jq -r ".[$i].id" "$OUT/pruebas.json")
  jq -r ".[$i].prompt" "$OUT/pruebas.json" > "$OUT/prompt-$ID.txt"

  echo "model-review.sh: mide $ID ($((i+1))/$N)" >&2
  if ! "$LLM" codigo --template "$OUT/prompt-$ID.txt" --model "$MODEL" \
        --json "${CTX_ARG[@]}" "${NP_ARG[@]}" > "$OUT/resp-$ID.json" 2>"$OUT/err-$ID.txt"; then
    # Un modelo que no contesta no aborta la cata: se registra como NON DELIVERY
    # y la etapa B lo puntua como NO_ENTREGA.
    echo "model-review.sh: $ID no entrego ($(head -1 "$OUT/err-$ID.txt"))" >&2
    jq -n --arg id "$ID" '{id:$id, no_entrega:true, text:"", secs:null}' > "$OUT/resp-$ID.json"
  fi

  jq --arg id "$ID" '. + {id:$id}' "$OUT/resp-$ID.json" >> "$OUT/mediciones.jsonl"

  {
    echo ""
    echo "### $ID"
    jq -r '.text // ""' "$OUT/resp-$ID.json"
  } >> "$OUT/salidas.txt"
  i=$((i+1))
done

# ---------------------------------------------------------------------------
# Etapa B: el evaluador puntua las salidas CRUDAS contra la fuente de verdad
# ---------------------------------------------------------------------------
echo "model-review.sh: evalua con $EVALUADOR" >&2
"$LLM" "$EVALUADOR" --template "$TPL/evaluacion.md" \
  --var "modelo=$MODEL" --var "fecha=$FECHA" \
  --var "ctx_declarado=$(cat "$OUT/ctx-declarado.txt")" \
  --var "verdad_consenso=$(cat "$VERDAD")" \
  --var "verdad_registro=$(cat "$VERDAD2")" \
  --var "salidas=$(cat "$OUT/salidas.txt")" \
  > "$OUT/veredicto.md" 2>"$OUT/err-evaluador.txt" || {
    echo "model-review.sh: fallo el evaluador (ver $OUT/err-evaluador.txt)" >&2; exit 4; }

# ---------------------------------------------------------------------------
# Etapa C: redaccion
# ---------------------------------------------------------------------------
MED="modelo: $MODEL
contexto_declarado_por_el_modelo: $(cat "$OUT/ctx-declarado.txt")
contexto_de_la_corrida: ${NUM_CTX:-<default>}
$(cat "$OUT/mediciones.jsonl")"
VER=$(cat "$OUT/veredicto.md")
SAL=$(cat "$OUT/salidas.txt")
[ ${#MED} -gt 20000 ] && MED="${MED:0:20000}... [truncado]"
[ ${#SAL} -gt 20000 ] && SAL="${SAL:0:20000}... [truncado]"

if [ "$SALIDA" = "interna" ] || [ "$SALIDA" = "ambas" ]; then
  echo "model-review.sh: redacta informe interno" >&2
  "$LLM" "$REDACTOR" --template "$TPL/informe-interno.md" \
    --var "modelo=$MODEL" --var "fecha=$FECHA" \
    --var "mediciones=$MED" --var "veredicto=$VER" \
    > "$OUT/informe-interno.md" 2>"$OUT/err-interno.txt" \
    || { echo "model-review.sh: fallo la redaccion interna" >&2; exit 4; }
  echo "" ; cat "$OUT/informe-interno.md"
fi

if [ "$SALIDA" = "publica" ] || [ "$SALIDA" = "ambas" ]; then
  echo "model-review.sh: redacta articulo" >&2
  "$LLM" "$REDACTOR" --template "$TPL/articulo.md" \
    --var "modelo=$MODEL" \
    --var "mediciones=$MED" --var "veredicto=$VER" --var "salidas=$SAL" \
    > "$OUT/articulo.md" 2>"$OUT/err-articulo.txt" \
    || { echo "model-review.sh: fallo la redaccion publica" >&2; exit 4; }
  echo "" ; cat "$OUT/articulo.md"
fi

echo "" >&2
echo "model-review.sh: artefactos en $OUT" >&2
echo "  mediciones.jsonl  veredicto.md  informe-interno.md  articulo.md" >&2
exit 0
