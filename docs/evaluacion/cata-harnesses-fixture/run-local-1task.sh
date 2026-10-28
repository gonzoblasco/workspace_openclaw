#!/usr/bin/env bash
# Driver de la FASE LOCAL de la cata de harnesses.
#
# QUE ES: la version VISIONADA de playground/cata-harnesses-2026-10-27/run-local-1task.sh.
# El playground esta en .gitignore (las corridas y los entregables son
# efimeros), pero este driver tiene las TRAMPAS que costaron perder celdas,
# asi que vive en el repo.
#
# QUE MIDE: 4 modelos locales (GGUF en CPU) x 3 harnesses x 1 TAREA (T1) = 12 celdas.
# Por que 1 tarea y no 3 (decision de Gonzo, 2026-10-28): los locales tardan
# 10-20 min por celda. Con 3 tareas serian 36 celdas y 6-8 horas. La pregunta
# que responden los locales es "el harness aguanta un modelo lento?", y para
# eso UNA tarea por modelo alcanza.
#
# ORDEN: de menor a mayor RAM, para que el mas chico valide el camino completo
# antes de gastar tiempo con el mas grande.
#
# RAM (medido 2026-10-28): con Docker abierto (VM 3,8 GB) y el embedding
# descargado (4,4 GB) quedan 3,71 GB libres. Los runners de los cloud NO
# consumen RAM local; los locales si, y se descargan con keep_alive:0 al
# terminar cada celda.
#
# TRAMPAS QUE ESTE DRIVER EVITA (las tres son de medicion, no de infraestructura):
#
#  1. results.json NO se sobrescribe: se MERGEa por (tarea, harness). Este
#     driver corre UN harness por invocacion (CATA_HARNESS), cada una en su
#     propio proceso. Antes, cada invocacion escribia results.json desde cero
#     con solo sus filas, y la celda de openhands (la ultima) borraba las de
#     claude y opencode. Medido: nova-2b quedo con 1 de 3 filas, y las dos
#     perdidas si se habian ejecutado (203 s y 100 s).
#
#  2. El sello LOCAL-DONE significa "este modelo ya esta medido" y el driver lo
#     usa para saltarlo. Se verifica ANTES de ponerlo: si el modelo no tiene
#     sus 3 filas de T1, NO se sella, para que la proxima pasada lo remedie.
#     Un modelo con 3 filas esta completo, tenga o no entregable: la ausencia
#     de entregable es un 0 legitimo, no un dato faltante.
#
#  3. El "ya medido" al arrancar cuenta FILAS de results.json, no artefactos.
#     Los artefactos son acumulativos y sobreviven a una corrida perdida;
#     las filas son lo que la suite y el informe necesitan.
#
#  4. LOCK: el driver se toma un lock con flock. Sin el, un watchdog que
#     relanza el driver cada 5 minutos puede arrancar una SEGUNDA tanda en
#     paralelo si la primera esta entre modelos (la ventana sin runner.py).
#     Las dos tandas miden las mismas celdas al mismo tiempo y se pisan los
#     results.json y los artefactos.
#
# NO OLVIDAR: NO cerrar Docker durante la fase local (opencode y OpenHands son
# containers). Al terminar, cerrar Docker Desktop para devolver los 7,7 GB
# de memoria wired.
set -uo pipefail

CATA_DIR="${CATA_DIR:-/Users/gonzoblasco/.openclaw/workspace/playground/cata-harnesses-2026-10-27}"
OUT="${CATA_OUT:-/tmp/cata-harnesses}"

cd "$CATA_DIR" || { echo "no existe la cata en $CATA_DIR"; exit 1; }

LOCALES=(
  "hf.co/ModernoTech/nova-2b:latest"
  "ornith-1.5:9b"
  "gemma4:12b-mlx"
  "qwen3.5:9b-mlx"
)
TAREAS="T1"

slug() { echo "$1" | tr ':/' '__'; }

# Trampa 4: LOCK. Un watchdog que relanza el driver cada 5 minutos puede
# arrancar una segunda tanda en paralelo si la primera esta entre modelos (la
# ventana sin runner.py). Con el lock, la segunda tanda espera en vez de medir
# las mismas celdas al mismo tiempo.
#
# OJO: macOS no trae flock. Se usa mkdir, que es atomico en POSIX: el que lo
# crea gana, el otro espera. Si el lock es viejo (el driver murio sin
# limpiarlo), se libera por edad.
LOCK="$OUT/.local-driver.lock"
LOCK_MAX_AGE=21600   # 6 h: un driver que dura mas se considera vivo
esperar_lock() {
  local i
  for i in $(seq 1 120); do
    if mkdir "$LOCK" 2>/dev/null; then
      echo $$ > "$LOCK/pid" 2>/dev/null
      return 0
    fi
    # Lock viejo: el driver que lo tomo murio sin limpiarlo.
    if [ -d "$LOCK" ]; then
      local edad=$(( $(date +%s) - $(stat -f %m "$LOCK" 2>/dev/null || echo 0) ))
      if [ "$edad" -gt "$LOCK_MAX_AGE" ]; then
        rm -rf "$LOCK"
        continue
      fi
    fi
    sleep 5
  done
  return 1
}
esperar_lock || { echo "no se pudo tomar el lock del driver local"; exit 1; }
# Liberar el lock al salir, para que el proximo watchdog no espere 6 h.
trap 'rm -rf "$LOCK"' EXIT

# Cuantas FILAS de T1 tiene la medicion de un modelo.
n_filas() {
  python3 - "$1" "$2" <<'PY'
import json, pathlib, sys
p = pathlib.Path(sys.argv[1]) / "results.json"
tarea = sys.argv[2] if len(sys.argv) > 2 else "T1"
try:
    rows = json.loads(p.read_text())
except Exception:
    rows = []
if not isinstance(rows, list):
    rows = []
print(len([r for r in rows if r.get("task_id") == tarea]))
PY
}

# Descarga un modelo del daemon (keep_alive:0) para liberar su RAM.
unload() {
  local m="$1"
  curl -s -m 300 -X POST http://127.0.0.1:11434/api/chat \
    -H 'Content-Type: application/json' \
    -d "{\"model\":\"$m\",\"messages\":[{\"role\":\"user\",\"content\":\"x\"}],\"stream\":false,\"keep_alive\":0}" \
    > /dev/null 2>&1
  sleep 3
}

# Libera el embedding (4,4 GB) que sostiene el gateway.
unload_embedding() {
  curl -s -m 300 -X POST http://127.0.0.1:11434/api/embeddings \
    -H 'Content-Type: application/json' \
    -d '{"model":"qwen3-embedding:0.6b","input":"x","keep_alive":0}' > /dev/null 2>&1
  sleep 3
}

./prepare-corpus.sh > /dev/null 2>&1

cat > /tmp/cata-probe.json <<'JSON'
[{"id":"probe","prompt":"Escribi un archivo llamado informe.md en el directorio actual con una sola linea que diga: PROBE","corpus":[]}]
JSON

for MODEL in "${LOCALES[@]}"; do
  SLUG=$(slug "$MODEL"); OUTD="$OUT/$SLUG"
  mkdir -p "$OUTD"; cp tasks.json "$OUTD/tasks.json"

  SELLO="$OUTD/LOCAL-DONE"

  # Trampa 3: el "ya medido" cuenta FILAS, no artefactos.
  if [ -f "$SELLO" ]; then
    echo "[local] $MODEL ya medido: se saltea"
    continue
  fi
  n_pre=$(n_filas "$OUTD" "$TAREAS")
  if [ "$n_pre" -ge 3 ]; then
    echo "[local] $MODEL ya tiene sus 3 celdas de $TAREAS: se sella y se saltea"
    touch "$SELLO"
    continue
  fi

  echo "================================================================"
  echo "== LOCAL: $MODEL"
  echo "================================================================"

  # 1. Control: el modelo viaja y hace tool calling.
  unload_embedding
  CATA_MODEL="$MODEL" CATA_OUT="$OUTD" CATA_TIMEOUT=600 CATA_TASKS=/tmp/cata-probe.json \
    python3 runner.py > "$OUTD/probe.log" 2>&1
  python3 - "$OUTD/results.json" <<'PY'
import json, sys
try: d = json.load(open(sys.argv[1]))
except Exception as e: print(f"  SIN RESULTADO: {e}"); sys.exit(0)
for r in d: print(f"  control {r['harness']:<10} ok={r['control_ok']} model={r['model_used']}")
PY
  rm -f "$OUTD/results.json"

  # 2. La celda por harness, con la tarea unica.
  for HARNESS in claude opencode openhands; do
    echo "-- $HARNESS --"
    unload_embedding
    CATA_MODEL="$MODEL" CATA_OUT="$OUTD" CATA_HARNESS="$HARNESS" CATA_ONLY="$TAREAS" \
      CATA_TIMEOUT=3600 python3 runner.py 2>&1 | tail -3
    # El modelo local se descarga: 3-9 GB de RAM no pueden quedar cacheados.
    unload "$MODEL"
  done

  # 3. Suite oculta sobre lo que hay (1 tarea x 3 harnesses).
  CATA_MODEL="$MODEL" CATA_OUT="$OUTD" python3 suite.py 2>&1 | tail -6

  # 4. Juez: los dos cloud que no son candidatos (el juez nunca es local: seria
  #    lento y el local ya es el candidato).
  J1="deepseek-v4.1-flash:cloud"; J2="gpt-oss:120b-cloud"
  case "$MODEL" in
    gemma4:12b-mlx)  J1="nemotron-3-super:cloud" ;;
    qwen3.5:9b-mlx) J1="nemotron-3-super:cloud" ;;
  esac
  echo "-- juez: $J1 + $J2 --"
  CATA_MODEL="$MODEL" CATA_OUT="$OUTD" JUDGE_MODEL="$J1" \
    timeout 3600 python3 judge.py --jueces "$J1,$J2" 2>&1 | tail -6

  # 5. Consolidar (los artefactos son acumulativos y son la fuente de verdad).
  python3 consolidate.py 2>&1 | grep -iE "nova|ornith|gemma4:12b|qwen3.5" || true

  # Trampa 2: no se sella un modelo con celdas perdidas.
  n_post=$(n_filas "$OUTD" "$TAREAS")
  if [ "$n_post" -lt 3 ]; then
    echo "   FALTAN CELDAS: $n_post/3. NO se sella: se remedira en la proxima pasada."
    continue
  fi
  touch "$SELLO"
  echo "   sellado ($n_post/3 celdas)"
done

echo "================================================================"
echo "== FASE LOCAL TERMINADA"
echo "== NO OLVIDES: cerrar Docker Desktop (osascript -e 'quit app \"Docker\"')"
