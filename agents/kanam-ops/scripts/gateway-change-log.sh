#!/usr/bin/env bash
# gateway-change-log.sh - Registro de cambios de config, legible por maquina.
#
# E2.4 del roadmap de Kanam OPS. El problema que resuelve: la evidencia de un
# cambio de config vivia en prosa dentro del daily, asi que la unica forma de
# reconstruir "cuando se cambio el modelo X y con que backup" era leer un .md
# de 400 lineas a ojo.
#
# Cada cambio deja una linea JSON en ~/.openclaw/gateway-changes.jsonl.
# Append-only y sin secretos: solo rutas, valores y nombres de backup.
#
# Usage:
#   gateway-change-log.sh record --field <dot.path> [--reason <texto>] \
#       [--before <valor>] [--after <valor>] [--backup <archivo>] [--evidence <texto>]
#   gateway-change-log.sh list [--limit N] [--json]
#   gateway-change-log.sh get <n>          # el n-esimo mas reciente (1 = ultimo)
#   gateway-change-log.sh verify           # chequea integridad de las lineas
#
# Si --before/--after se omiten, el script NO los inventa: los marca como
# "no medidos". Un registro que adivina el valor viejo es peor que uno vacio.
set -euo pipefail

LOG="${GATEWAY_CHANGES_LOG:-$HOME/.openclaw/gateway-changes.jsonl}"
NOW="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"

die() { echo "ERROR: $*" >&2; exit 2; }

cmd="${1:-}"; shift || true

case "$cmd" in
  record)
    FIELD=""; REASON=""; BEFORE=""; AFTER=""; BACKUP=""; EVIDENCE=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --field)    FIELD="${2:-}";    shift 2 ;;
        --reason)   REASON="${2:-}";   shift 2 ;;
        --before)   BEFORE="${2:-}";   shift 2 ;;
        --after)    AFTER="${2:-}";    shift 2 ;;
        --backup)   BACKUP="${2:-}";   shift 2 ;;
        --evidence) EVIDENCE="${2:-}"; shift 2 ;;
        *) die "arg desconocido: $1" ;;
      esac
    done
    [[ -n "$FIELD" ]] || die "falta --field (la ruta dot del campo cambiado)"

    # Si no se pasan valores, se leen del config actual (solo el "after").
    if [[ -z "$AFTER" ]]; then
      AFTER="$(openclaw config get "$FIELD" 2>/dev/null | tr '\n' ' ' | sed 's/  */ /g; s/ $//' || true)"
      [[ -z "$AFTER" ]] && AFTER="no medido"
    fi
    [[ -z "$BEFORE" ]] && BEFORE="no medido"
    [[ -z "$REASON" ]] && REASON="sin motivo registrado"

    python3 - "$LOG" "$NOW" "$FIELD" "$REASON" "$BEFORE" "$AFTER" "$BACKUP" "$EVIDENCE" <<'PY'
import json, os, sys

log, ts, field, reason, before, after, backup, evidence = sys.argv[1:9]

entry = {
    "ts": ts,
    "field": field,
    "before": before,
    "after": after,
    "reason": reason,
    "backup": backup or "ninguno",
    "evidence": evidence or "no registrada",
    "host": os.uname().nodename,
}

# Guard de secretos: nunca guardar un valor que parezca credencial.
SUSPECT = ("token", "secret", "password", "apikey", "api_key", "bearer")
blob = json.dumps(entry).lower()
if any(k in blob for k in SUSPECT) and "ref" not in blob:
    entry["redacted"] = True
    entry["after"] = "[REDACTADO: posible credencial]"
    entry["before"] = "[REDACTADO]" if entry["before"] not in ("no medido", "") else "no medido"

os.makedirs(os.path.dirname(log) or ".", exist_ok=True)
with open(log, "a") as f:
    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
print(json.dumps(entry, indent=1, ensure_ascii=False))
PY
    ;;

  list)
    LIMIT=20
    JSON_OUT=false
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --limit) LIMIT="${2:-20}"; shift 2 ;;
        --json) JSON_OUT=true; shift ;;
        *) die "arg desconocido: $1" ;;
      esac
    done
    [[ -f "$LOG" ]] || { echo "Sin cambios registrados ($LOG no existe)."; exit 0; }
    TOTAL="$(grep -c . "$LOG" 2>/dev/null || echo 0)"
    if $JSON_OUT; then
      tail -n "$LIMIT" "$LOG"
    else
      echo "Ultimos $LIMIT cambios registrados ($TOTAL en total):"
      echo
      tail -n "$LIMIT" "$LOG" | python3 -c '
import json, sys
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        d = json.loads(line)
    except Exception:
        continue
    print(f"{d.get(chr(116)+chr(115))}  {d.get(chr(102)+chr(105)+chr(101)+chr(108)+chr(100))}")
    print(f"   {d.get(chr(98)+chr(101)+chr(102)+chr(111)+chr(114)+chr(101))} -> {d.get(chr(97)+chr(102)+chr(116)+chr(101)+chr(114))}")
    print(f"   motivo: {d.get(chr(114)+chr(101)+chr(97)+chr(115)+chr(111)+chr(110))}")
    print(f"   backup: {d.get(chr(98)+chr(97)+chr(99)+chr(107)+chr(117)+chr(112))}")
    print(f"   evidencia: {d.get(chr(101)+chr(118)+chr(105)+chr(100)+chr(101)+chr(110)+chr(99)+chr(101))}")
    print()
'
    fi
    ;;

  get)
    N="${1:-1}"
    [[ -f "$LOG" ]] || die "no hay log en $LOG"
    tail -n "$N" "$LOG" | head -1 | python3 -m json.tool
    ;;

  verify)
    [[ -f "$LOG" ]] || { echo "Sin log: nada que verificar."; exit 0; }
    python3 - "$LOG" <<'PY'
import json, sys
bad = 0
total = 0
required = {"ts", "field", "before", "after", "reason", "backup", "evidence"}
with open(sys.argv[1]) as f:
    for n, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        total += 1
        try:
            d = json.loads(line)
        except Exception as e:
            print(f"linea {n}: JSON invalido ({e})")
            bad += 1
            continue
        missing = required - set(d)
        if missing:
            print(f"linea {n}: faltan campos {sorted(missing)}")
            bad += 1
if bad:
    print(f"FALLA: {bad} de {total} lineas con problemas")
    sys.exit(1)
print(f"OK: {total} entradas, todas con los campos requeridos")
PY
    ;;

  *)
    echo "Usage: $0 {record|list|get|verify} [opciones]" >&2
    exit 2
    ;;
esac
