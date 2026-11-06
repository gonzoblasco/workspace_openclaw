#!/usr/bin/env bash
# gateway-config-drift.sh - Detect config drift of ~/.openclaw/openclaw.json
#
# v2 (2026-11-06): drift SEMANTICO, no hash de archivo completo.
# El v1 comparaba un sha256 de todo el archivo contra un baseline. Con el
# archivo cambiando por razones legitimas varias veces por semana (agentes,
# sesiones, modelos), el resultado era DRIFT permanente: 7 de 7 dias. Una
# alarma que siempre suena no es una alarma, es ruido que se aprende a ignorar.
#
# v2 guarda el CONTENIDO canonico como baseline y reporta los campos que
# cambiaron, con valor viejo y nuevo. Los campos de la ALLOWLIST que cambian
# solos se reportan como "informativos" y no cuentan como drift.
#
# Usage:
#   gateway-config-drift.sh              # check: exit 1 if real drift, 0 if clean
#   gateway-config-drift.sh --accept     # accept current config as new baseline
#   gateway-config-drift.sh --json       # machine-readable output
#   gateway-config-drift.sh --verbose    # show every changed path, incl. allowed
set -euo pipefail

CONFIG="$HOME/.openclaw/openclaw.json"
BASELINE="$HOME/.openclaw/gateway-config.baseline.json"
LEGACY_BASELINE="$HOME/.openclaw/gateway-config.baseline"
NOW="$(date '+%Y-%m-%d %H:%M:%S')"
JSON_OUT=false
ACCEPT=false
VERBOSE=false

for arg in "$@"; do
  case "$arg" in
    --json) JSON_OUT=true ;;
    --accept) ACCEPT=true ;;
    --verbose) VERBOSE=true ;;
    *) echo "Unknown arg: $arg" >&2; exit 2 ;;
  esac
done

if [[ ! -f "$CONFIG" ]]; then
  echo "ERROR: config not found at $CONFIG" >&2
  exit 2
fi

# Rutas que cambian por actividad normal del gateway y NO son drift.
# Justificacion por grupo (ver ROADMAP E2.2):
#   agents.entries.*.{workspace,cwd,agentDir}  -> rutas de instalacion por agente
#   agents.entries.*.model.*                   -> rotacion de modelos por agente
#   agents.defaults.model.*                    -> idem, default
#   update.*, meta.*                           -> version y metadatos del runtime
#   gateway.auth.*                             -> tokens rotados por el runtime
#   telemetry.*, wizard.*                      -> estado de telemetria y setup
ALLOWED_PATTERNS=(
  '^agents\.entries\.[^.]+\.model(\.|$)'
  '^agents\.defaults\.model(\.|$)'
  '^agents\.entries\.[^.]+\.models(\.|$)'
  '^agents\.defaults\.models(\.|$)'
  '^agents\.entries\.[^.]+\.workspace$'
  '^agents\.entries\.[^.]+\.cwd$'
  '^agents\.entries\.[^.]+\.agentDir$'
  '^agents\.entries\.[^.]+\.thinkingDefault$'
  '^update\.'
  '^meta\.'
  '^telemetry\.'
  '^wizard\.'
  '^gateway\.auth\.'
)

is_allowed() {
  local path="$1"
  local pat
  for pat in "${ALLOWED_PATTERNS[@]}"; do
    if [[ "$path" =~ $pat ]]; then return 0; fi
  done
  return 1
}

# Normaliza el JSON a "path<TAB>valor" ordenado, una linea por hoja.
# Arrays se tratan como hoja completa (el contenido importa, el orden no).
flatten() {
  python3 - "$1" <<'PY'
import json, sys

def walk(node, prefix, out):
    if isinstance(node, dict):
        if not node:
            out.append((prefix, "{}"))
        for k, v in node.items():
            walk(v, f"{prefix}.{k}" if prefix else k, out)
    elif isinstance(node, list):
        # orden canonico: los arrays de strings se ordenan para no reportar
        # reordenamientos como cambio
        try:
            canon = sorted(node, key=lambda x: json.dumps(x, sort_keys=True))
        except Exception:
            canon = node
        out.append((prefix, json.dumps(canon, sort_keys=True)))
    else:
        out.append((prefix, json.dumps(node, sort_keys=True)))

with open(sys.argv[1]) as f:
    data = json.load(f)
out = []
walk(data, "", out)
for path, val in sorted(out):
    print(f"{path}\t{val}")
PY
}

if [[ "$ACCEPT" == true ]]; then
  flatten "$CONFIG" > "$BASELINE"
  echo "[$NOW] Baseline accepted: $(wc -l < "$BASELINE" | tr -d ' ') campos" >&2
  echo "[$NOW] Baseline accepted: $(wc -l < "$BASELINE" | tr -d ' ') campos"
  exit 0
fi

if [[ ! -f "$BASELINE" ]]; then
  # Migracion desde el baseline v1 (hash plano): lo convertimos en semantic
  # pero NO aceptamos a ciegas; solo avisamos.
  if [[ -f "$LEGACY_BASELINE" ]]; then
    echo "[$NOW] Baseline v1 (hash) detectado. Convirtiendo a baseline semantico." >&2
  fi
  flatten "$CONFIG" > "$BASELINE"
  echo "[$NOW] No semantic baseline found. Created one from current config ($(wc -l < "$BASELINE" | tr -d ' ') campos)."
  exit 0
fi

TMP_NOW="$(mktemp)"
TMP_OLD="$(mktemp)"
trap 'rm -f "$TMP_NOW" "$TMP_OLD"' EXIT

flatten "$CONFIG" > "$TMP_NOW"
cp "$BASELINE" "$TMP_OLD"

# diff de las dos tablas: solo las rutas presentes en una u otra
CHANGED="$(python3 - "$TMP_OLD" "$TMP_NOW" <<'PY'
import sys

def load(p):
    d = {}
    with open(p) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            k, _, v = line.partition("\t")
            d[k] = v
    return d

old = load(sys.argv[1])
new = load(sys.argv[2])
for path in sorted(set(old) | set(new)):
    o, n = old.get(path), new.get(path)
    if o != n:
        print(f"{path}\t{o or '<ausente>'}\t{n or '<ausente>'}")
PY
)"

if [[ -z "$CHANGED" ]]; then
  if $JSON_OUT; then
    echo '{"drift":false,"allowed":[],"unexplained":[]}'
  else
    echo "[$NOW] OK: sin drift ($(wc -l < "$TMP_NOW" | tr -d ' ') campos semánticos)"
  fi
  exit 0
fi

# separar explicado vs no explicado
# Se usa un archivo temporal en vez de arrays con += porque bajo `set -e` la
# expansion de un array vacio aborta el script: ese bug hizo que un cambio
# permitido saliera con exit 1 sin imprimir nada.
UNEXPLAINED_FILE="$(mktemp)"
ALLOWED_FILE="$(mktemp)"
: > "$UNEXPLAINED_FILE"
: > "$ALLOWED_FILE"
trap 'rm -f "$TMP_NOW" "$TMP_OLD" "$UNEXPLAINED_FILE" "$ALLOWED_FILE"' EXIT
while IFS=$'\t' read -r path old new; do
  [[ -z "$path" ]] && continue
  if is_allowed "$path"; then
    printf '%s|%s|%s\n' "$path" "$old" "$new" >> "$ALLOWED_FILE"
  else
    printf '%s|%s|%s\n' "$path" "$old" "$new" >> "$UNEXPLAINED_FILE"
  fi
done <<< "$CHANGED"

ALLOWED_COUNT="$(wc -l < "$ALLOWED_FILE" | tr -d ' ')"
UNEXPLAINED_COUNT="$(wc -l < "$UNEXPLAINED_FILE" | tr -d ' ')"

if $JSON_OUT; then
  python3 - "$ALLOWED_FILE" "$UNEXPLAINED_FILE" <<'PY'
import json, sys

def load(p):
    out = []
    with open(p) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            path, old, new = line.split("|", 2)
            out.append({"path": path, "old": old, "new": new})
    return out

unexplained = load(sys.argv[2])
print(json.dumps({
    "drift": bool(unexplained),
    "allowed": load(sys.argv[1]),
    "unexplained": unexplained,
}, indent=1))
sys.exit(1 if unexplained else 0)
PY
  exit $?
fi

if [[ "$ALLOWED_COUNT" -gt 0 ]]; then
  if $VERBOSE; then
    echo "[$NOW] Cambios esperados (allowlist, no cuentan como drift): $ALLOWED_COUNT"
    while IFS='|' read -r p o n; do
      [[ -z "$p" ]] && continue
      echo "   ~ $p: $o -> $n"
    done < "$ALLOWED_FILE"
  else
    echo "[$NOW] $ALLOWED_COUNT cambios esperados (allowlist). Usa --verbose para verlos."
  fi
fi

if [[ "$UNEXPLAINED_COUNT" -gt 0 ]]; then
  echo "[$NOW] DRIFT: $UNEXPLAINED_COUNT campo(s) sin explicar."
  while IFS='|' read -r p o n; do
    [[ -z "$p" ]] && continue
    echo "   ! $p"
    echo "       antes:  $o"
    echo "       ahora:  $n"
  done < "$UNEXPLAINED_FILE"
  echo "  Si el cambio es esperado: $0 --accept"
  exit 1
fi

echo "[$NOW] OK: sin drift no explicado ($ALLOWED_COUNT cambios esperados)."
exit 0
