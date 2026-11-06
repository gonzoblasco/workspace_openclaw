#!/bin/bash
# llm.sh - Una llamada a un modelo con la tarea declarada, no adivinada.
#
# El problema que resuelve: el modelo correcto depende de la tarea, y una skill
# hereda UN modelo para todas sus tareas. Aca la tarea es un parametro, y con la
# tarea vienen el modelo, el nivel de thinking, el presupuesto de tokens y la
# temperatura. Los valores salen de catas con fecha (ver llm-tasks.json).
#
# Y resuelve el error que costo dos veredictos falsos el 2026-11-05: descartar un
# modelo por su salida cuando el problema era el parametro de invocacion. Sin
# 'think' explicito, cada modelo hereda su default (deepseek piensa; glm no
# escribe). Aca nunca se hereda: siempre va explicito.
#
# Uso:
#   llm.sh <tarea> [--template ARCHIVO] [--prompt TEXTO] [--var k=v]... [--json]
#            [--num-ctx N] [--no-num-predict] [--model M] [--think LVL]
#   llm.sh --list                      # tareas disponibles y por que ese modelo
#   llm.sh <tarea> --show              # config resuelta, sin llamar al modelo
#
# Overrides para MEDIR, no para producir (2026-11-05):
#   --num-ctx N        fija el contexto de la corrida. Sin este flag y sin
#                      num_ctx en el registro, no se manda: Ollama usa el
#                      default del modelo (que en un GGUF puede ser 163840 y
#                      swap thrashing: 469s para un saludo).
#   --no-num-predict   no manda num_predict: el modelo decide cuando cortar.
#                      Necesario para medir calidad sin el techo artificial.
#   --model M          pisa el modelo de la tarea (evaluar un modelo que no
#                      tiene tarea propia todavia).
#   --think LVL        pisa el nivel de thinking de la tarea.
#   Con --json, la salida suma ctx, num_predict y done_reason utiles para medir.
#
# Ejemplos:
#   llm.sh narrativa --template templates/cuento.md --var tema="estacion minera"
#   llm.sh clasificacion --prompt "clasifica: arreglar el css del boton"
#   llm.sh codigo --prompt "explica este error: EADDRINUSE" --json
#   llm.sh codigo --prompt "di OK" --num-ctx 32768 --model gemma4:12b-mlx
#
# Salida por defecto: el texto del modelo, limpio.
# Con --json: {text, model, think, task, tokens_in, tokens_out, secs, done}.
#
# Exit: 0 ok, 2 uso invalido, 3 la tarea no existe, 4 la llamada fallo.

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASKS_FILE="${LLM_TASKS_FILE:-$SCRIPT_DIR/llm-tasks.json}"
OLLAMA_BASE="${OLLAMA_BASE:-http://127.0.0.1:11434}"
# Tope por defecto 600s: un modelo sano no tarda mas. Configurable por si una
# corrida legitima necesita mas.
LLM_MAX_TIME="${LLM_MAX_TIME:-600}"

# Tope duro adicional: si el modelo produce CERO tokens en este tiempo, no esta
# razonando, esta trabado. Se corta antes que el tope general.
LLM_STALL_TIME="${LLM_STALL_TIME:-180}"

die() { echo "llm.sh: $*" >&2; exit "$1"; shift; }

if [ ! -r "$TASKS_FILE" ]; then
  echo "llm.sh: no encuentro el registro de tareas: $TASKS_FILE" >&2
  exit 4
fi

# ---------- --list ----------
if [ "${1:-}" = "--list" ]; then
  jq -r '.tasks | to_entries[] |
    "\(.key)\n  \(.value.model)  think=\(.value.think)  tokens=\(.value.num_predict)  temp=\(.value.temperature)\n  \(.value.why)\n"' "$TASKS_FILE"
  exit 0
fi

if [ $# -lt 1 ] || [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  sed -n '2,30p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
  exit 2
fi

TASK="$1"; shift

# ---------- la tarea tiene que existir ----------
if ! jq -e --arg t "$TASK" '.tasks[$t]' "$TASKS_FILE" >/dev/null 2>&1; then
  {
    echo "llm.sh: la tarea '$TASK' no existe en $TASKS_FILE"
    echo "Tareas disponibles:"
    jq -r '.tasks | keys[] | "  - \(.)"' "$TASKS_FILE"
  } >&2
  exit 3
fi

MODEL=$(jq -r --arg t "$TASK" '.tasks[$t].model' "$TASKS_FILE")
THINK=$(jq -r --arg t "$TASK" '.tasks[$t].think' "$TASKS_FILE")
NUM_PREDICT=$(jq -r --arg t "$TASK" '.tasks[$t].num_predict | if . == null then "" else . end' "$TASKS_FILE")
TEMP=$(jq -r --arg t "$TASK" '.tasks[$t].temperature' "$TASKS_FILE")
# num_ctx es opcional: sin valor en el registro no se manda y Ollama usa su
# default. Eso mantiene el comportamiento anterior intacto.
NUM_CTX=$(jq -r --arg t "$TASK" '.tasks[$t].num_ctx // ""' "$TASKS_FILE")
NO_NUM_PREDICT=0

# ---------- flags ----------
TEMPLATE=""; PROMPT=""; SHOW=0; JSON_OUT=0
VARS=()

while [ $# -gt 0 ]; do
  case "$1" in
    --template) [ -n "${2:-}" ] || die 2 "--template necesita un archivo"; TEMPLATE="$2"; shift 2 ;;
    --prompt)   [ -n "${2:-}" ] || die 2 "--prompt necesita texto";      PROMPT="$2";   shift 2 ;;
    --var)      [ -n "${2:-}" ] || die 2 "--var necesita k=v";           VARS+=("$2");  shift 2 ;;
    --json)     JSON_OUT=1; shift ;;
    --show)     SHOW=1; shift ;;
    --num-ctx)  [ -n "${2:-}" ] || die 2 "--num-ctx necesita un numero"; NUM_CTX="$2"; shift 2 ;;
    --no-num-predict) NO_NUM_PREDICT=1; shift ;;
    --model)    [ -n "${2:-}" ] || die 2 "--model necesita un nombre"; MODEL="$2"; shift 2 ;;
    --think)    [ -n "${2:-}" ] || die 2 "--think necesita un nivel"; THINK="$2"; shift 2 ;;
    *) die 2 "flag desconocida: $1 (ver --help)" ;;
  esac
done

# --no-num-predict gana sobre lo que diga el registro.
[ "$NO_NUM_PREDICT" = "1" ] && NUM_PREDICT=""

# Un num_ctx que no es entero positivo es un error de uso, no un default silencioso.
if [ -n "$NUM_CTX" ]; then
  case "$NUM_CTX" in
    ''|*[!0-9]*) die 2 "--num-ctx espera un entero positivo, recibi: $NUM_CTX" ;;
  esac
fi

if [ "$SHOW" = "1" ]; then
  echo "tarea=$TASK"
  echo "model=$MODEL"
  echo "think=$THINK"
  echo "num_predict=${NUM_PREDICT:-<modelo>}"
  echo "num_ctx=${NUM_CTX:-<default del modelo>}"
  echo "temperature=$TEMP"
  exit 0
fi

# ---------- el prompt: un template o texto directo, nunca los dos ----------
[ -z "$TEMPLATE" ] && [ -z "$PROMPT" ] && die 2 "falta --template o --prompt"
[ -n "$TEMPLATE" ] && [ -n "$PROMPT" ]   && die 2 "--template y --prompt son excluyentes"

if [ -n "$TEMPLATE" ]; then
  [ -r "$TEMPLATE" ] || die 4 "no puedo leer el template: $TEMPLATE"
  TEXT=$(cat "$TEMPLATE")
else
  TEXT="$PROMPT"
fi

# Sustitucion de {{var}}. Se hace en python para no pelear con sed y con los
# caracteres especiales del texto del usuario.
if [ ${#VARS[@]} -gt 0 ]; then
  TEXT=$(printf '%s' "$TEXT" | python3 -c '
import sys, re
text = sys.stdin.read()
for pair in sys.argv[1:]:
    if pair == "--":
        continue
    if "=" not in pair:
        sys.exit("llm.sh: --var espera k=v, recibi: " + pair)
    k, v = pair.split("=", 1)
    text = re.sub(r"\{\{\s*" + re.escape(k) + r"\s*\}\}", v.replace("\\", "\\\\"), text)
sys.stdout.write(text)
' -- "${VARS[@]}") || exit 4
fi

# Las variables sin sustituir son un error, no un prompt roto en silencio.
LEFTOVER=$(printf '%s' "$TEXT" | grep -o '{{[a-zA-Z0-9_]*}}' | sort -u | tr '\n' ' ')
if [ -n "$LEFTOVER" ]; then
  die 2 "quedaron variables sin valor en el template: $LEFTOVER"
fi

# ---------- la llamada ----------
# 'think' viaja SIEMPRE explicito, con el tipo correcto (false o "low"/"medium"/"high").
# Un script sin 'think' hereda el default del modelo: eso fue el bug medido el 2026-11-05.
PAYLOAD=$(python3 - "$MODEL" "$THINK" "$NUM_PREDICT" "$TEMP" "$TEXT" "$NUM_CTX" <<'PY'
import json, sys
model, think, npred, temp, text, nctx = sys.argv[1:7]

def parse_think(v):
    if v in ("false", "False", "off", "0"): return False
    if v in ("true", "True", "on", "1"): return True
    if v in ("low", "medium", "high"): return v
    raise SystemExit("llm.sh: think invalido en el registro: " + v)

opts = {"temperature": float(temp)}
# num_predict vacio = el modelo corta cuando quiere (medicion de calidad).
if npred not in ("", "null"):
    opts["num_predict"] = int(npred)
# num_ctx vacio = no se manda: Ollama usa el default del modelo (compatibilidad).
if nctx not in ("", "null"):
    opts["num_ctx"] = int(nctx)

print(json.dumps({
    "model": model,
    "think": parse_think(think),
    "stream": False,
    "messages": [{"role": "user", "content": text}],
    "options": opts,
}))
PY
) || exit 4

# --max-time corta la TRANSFERENCIA, no garantiza que el modelo dejo de generar:
# el proceso puede seguir colgado. Se limita ademas con un tope externo, y se
# distingue el timeout de la respuesta vacia. Medido 2026-11-05: un modelo en
# Q2_K quedo generando sin devolver nada y el script no lo detecto.
# Deteccion de estancamiento: se lanza curl con streaming y se corta si no llega
# ningun token en LLM_STALL_TIME. Un modelo sano empieza a emitir en segundos;
# 600s sin un solo token es un loop degenerado, no razonamiento. Medido
# 2026-11-05: Qwen2.5-Coder-3B y Nova-Core se colgaron asi en la prueba de consenso.
CURL_EXIT=0
RESP=""

# La llamada va en un proceso python aparte, en archivo temporal: hay que leer el
# stream token a token para distinguir "tarda" de "se trabo". Un modelo sano
# emite el primer token en segundos.
_CHAT_PY=$(mktemp -t llmchat)
cat > "$_CHAT_PY" <<'PYEOF'
import json, sys, time, urllib.request

base, payload_s, max_time, stall_time = sys.argv[1:5]
max_time, stall_time = float(max_time), float(stall_time)
payload = json.loads(payload_s)
payload["stream"] = True
data = json.dumps(payload).encode()

req = urllib.request.Request(base + "/api/chat", data=data,
                             headers={"Content-Type": "application/json"})
t0 = time.time()
content, thinking = [], []
done = False
last_token = t0
eval_count = prompt_eval_count = 0
load_ns = eval_ns = 0
try:
    with urllib.request.urlopen(req, timeout=max_time) as r:
        for raw in r:
            if time.time() - t0 > max_time:
                print("llm.sh: TIMEOUT global", file=sys.stderr)
                sys.exit(28)
            line = raw.decode("utf-8", "replace").strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = obj.get("message") or {}
            if msg.get("content"):
                content.append(msg["content"])
                last_token = time.time()
            if msg.get("thinking"):
                thinking.append(msg["thinking"])
                last_token = time.time()
            if obj.get("error"):
                print(json.dumps({"error": obj["error"]}))
                sys.exit(0)
            if obj.get("done"):
                done = True
                eval_count = obj.get("eval_count", len(content))
                prompt_eval_count = obj.get("prompt_eval_count", 0)
                load_ns = obj.get("load_duration", 0)
                eval_ns = obj.get("eval_duration", 0)
                break
            if time.time() - last_token > stall_time:
                print("llm.sh: ESTANCADO: %.0fs sin emitir un token"
                      % (time.time() - last_token), file=sys.stderr)
                sys.exit(29)
except Exception as e:
    print("llm.sh: error de red: %s" % e, file=sys.stderr)
    sys.exit(4)

print(json.dumps({
    "message": {"content": "".join(content), "thinking": "".join(thinking)},
    "done": done,
    "eval_count": eval_count,
    "prompt_eval_count": prompt_eval_count,
    "load_duration": load_ns,
    "eval_duration": eval_ns,
    "total_duration": int((time.time() - t0) * 1e9),
}, ensure_ascii=False))
PYEOF

RESP=$(python3 "$_CHAT_PY" "$OLLAMA_BASE" "$PAYLOAD" "$LLM_MAX_TIME" "$LLM_STALL_TIME") || CURL_EXIT=$?
rm -f "$_CHAT_PY"

if [ "$CURL_EXIT" -eq 29 ]; then
  echo "llm.sh: ESTANCADO en la tarea $TASK (modelo $MODEL)." >&2
  echo "llm.sh: el modelo dejo de emitir tokens; no es lentitud, es traba." >&2
  exit 5
elif [ "$CURL_EXIT" -eq 28 ]; then
  echo "llm.sh: TIMEOUT tras ${LLM_MAX_TIME}s (modelo $MODEL, tarea $TASK)." >&2
  echo "llm.sh: el modelo no termino de generar. Revisar num_predict/num_ctx." >&2
  exit 5
elif [ "$CURL_EXIT" -ne 0 ]; then
  echo "llm.sh: curl fallo con exit $CURL_EXIT (modelo $MODEL)" >&2
  exit 4
fi

if [ -z "$RESP" ]; then
  echo "llm.sh: la API devolvio vacio (modelo $MODEL)" >&2
  exit 4
fi

# Un error de la API se reporta como error, no como texto vacio.
if printf '%s' "$RESP" | python3 -c 'import json,sys; d=json.load(sys.stdin); sys.exit(0 if d.get("error") else 1)' 2>/dev/null; then
  echo "llm.sh: la API rechazo la llamada:" >&2
  printf '%s\n' "$RESP" | jq -r '.error' >&2 2>/dev/null || printf '%s\n' "$RESP" >&2
  exit 4
fi

# ---------- la salida ----------
if [ "$JSON_OUT" = "1" ]; then
  printf '%s' "$RESP" | jq --arg task "$TASK" --arg model "$MODEL" --arg think "$THINK" \
       --arg nctx "${NUM_CTX:-}" --arg npred "${NUM_PREDICT:-}" '
    {
      text: (.message.content // ""),
      task: $task,
      model: $model,
      think: $think,
      ctx: (if $nctx == "" then null else ($nctx | tonumber) end),
      num_predict: (if $npred == "" then null else ($npred | tonumber) end),
      tokens_in: (.prompt_eval_count // 0),
      tokens_out: (.eval_count // 0),
      load_secs: (((.load_duration // 0) / 1000000000) * 100 | round / 100),
      secs: (((.total_duration // 0) / 1000000000) * 100 | round / 100),
      done: (.done_reason // ""),
      thinking_chars: ((.message.thinking // "") | length)
    }'
else
  printf '%s' "$RESP" | jq -r '.message.content // ""'
fi

# Un modelo que gasta el presupuesto pensando y no escribe es un fallo, no una
# respuesta vacia. Paso medido el 2026-11-05 con deepseek y nemotron.
CONTENT_LEN=$(printf '%s' "$RESP" | jq -r '.message.content // "" | length')
THINK_LEN=$(printf '%s' "$RESP" | jq -r '.message.thinking // "" | length')
if [ "$CONTENT_LEN" -eq 0 ] && [ "$THINK_LEN" -gt 0 ]; then
  echo "llm.sh: AVISO: $MODEL gasto ${THINK_LEN} chars pensando y no escribio nada." >&2
  echo "llm.sh: revisa think/num_predict de la tarea '$TASK' (ver --show)." >&2
  exit 4
fi

exit 0
