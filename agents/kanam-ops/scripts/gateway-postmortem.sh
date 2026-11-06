#!/usr/bin/env bash
# Post-mortem automatico de incidentes del gateway (E3.4).
#
# Lee los reportes de estabilidad que el runtime deja en ~/.openclaw/logs/stability/
# y arma un timeline, agrupa por causa raiz y propone hipotesis. READ-ONLY.
#
# Uso:
#   postmortem.sh                 # todos los incidentes
#   postmortem.sh --since 7d      # solo los ultimos 7 dias
#   postmortem.sh --json          # salida legible por maquina
#
# Exit codes:
#   0 = informe armado (haya o no incidentes)
#   2 = no se pudo leer el directorio de estabilidad
set -uo pipefail

ROOT="${OPENCLAW_STABILITY_DIR:-$HOME/.openclaw/logs/stability}"
SINCE=""
JSON_OUT=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --since) SINCE="$2"; shift 2 ;;
    --json) JSON_OUT=true; shift ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

if [[ ! -d "$ROOT" ]]; then
  echo "No existe el directorio de estabilidad: $ROOT" >&2
  exit 2
fi

python3 - "$ROOT" "$SINCE" "$JSON_OUT" <<'PY'
import json, sys, os, re
from datetime import datetime, timedelta, timezone
from collections import defaultdict

root, since, json_out = sys.argv[1], sys.argv[2], sys.argv[3] == "true"

def parse_since(s):
    if not s:
        return None
    m = re.fullmatch(r"(\d+)([dhm])", s)
    if not m:
        return None
    n, unit = int(m.group(1)), m.group(2)
    key = {"d": "days", "h": "hours", "m": "minutes"}[unit]
    return datetime.now(timezone.utc) - timedelta(**{key: n})

cutoff = parse_since(since)

incidents = []
unreadable = []

for name in sorted(os.listdir(root)):
    if not name.endswith(".json"):
        continue
    path = os.path.join(root, name)
    try:
        with open(path) as fh:
            data = json.load(fh)
    except Exception as e:
        unreadable.append((name, str(e)))
        continue

    ts_raw = data.get("generatedAt")
    try:
        ts = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
    except Exception:
        unreadable.append((name, "generatedAt invalido: %r" % ts_raw))
        continue

    if cutoff and ts < cutoff:
        continue

    err = data.get("error") or {}
    proc = data.get("process") or {}
    incidents.append({
        "file": name,
        "ts": ts,
        "ts_raw": ts_raw,
        "reason": data.get("reason") or "?",
        "message": err.get("message") or "",
        "code": err.get("code"),
        "pid": proc.get("pid"),
        "node": proc.get("node"),
        "uptimeMs": proc.get("uptimeMs"),
        "events": len((data.get("snapshot") or {}).get("events") or []),
    })

incidents.sort(key=lambda x: x["ts"])

# Agrupa por causa raiz: el mensaje de error es la senal mas directa.
by_cause = defaultdict(list)
for i in incidents:
    cause = i["message"] or "(sin mensaje)"
    by_cause[cause].append(i)

# Rafagas: incidentes de la misma causa separados por menos de 5 minutos.
def bursts(items, gap_s=300):
    out, cur = [], []
    for it in items:
        if cur and (it["ts"] - cur[-1]["ts"]).total_seconds() > gap_s:
            out.append(cur); cur = []
        cur.append(it)
    if cur:
        out.append(cur)
    return out

summary = {
    "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "dir": root,
    "since": since or "todo",
    "total": len(incidents),
    "unreadable": len(unreadable),
    "by_reason": {r: sum(1 for i in incidents if i["reason"] == r)
                  for r in sorted({i["reason"] for i in incidents})},
    "by_cause": {c: len(v) for c, v in sorted(by_cause.items(), key=lambda kv: -len(kv[1]))},
}

if json_out:
    summary["incidents"] = [
        {k: (v if k != "ts" else v.isoformat()) for k, v in i.items()}
        for i in incidents
    ]
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    sys.exit(0)

print("POST-MORTEM de estabilidad del gateway")
print("Generado: %s" % summary["generatedAt"])
print("Fuente:   %s" % root)
print("Ventana:  %s" % summary["since"])
print("")

if not incidents:
    print("Sin incidentes en la ventana. Nada que analizar.")
    if unreadable:
        print("")
        print("PERO hay %d archivo(s) ilegible(s):" % len(unreadable))
        for n, e in unreadable:
            print("  - %s: %s" % (n, e))
    sys.exit(0)

print("TOTAL: %d incidente(s)" % len(incidents))
if unreadable:
    print("Ademas %d archivo(s) ilegible(s) - se listan al final." % len(unreadable))
print("")

print("POR TIPO")
for r, n in summary["by_reason"].items():
    print("  %-32s %d" % (r, n))
print("")

print("POR CAUSA RAIZ")
for c, n in sorted(summary["by_cause"].items(), key=lambda kv: -kv[1]):
    print("  %3dx  %s" % (n, c[:100]))
print("")

print("TIMELINE")
for cause, items in sorted(by_cause.items(), key=lambda kv: kv[1][0]["ts"]):
    for b in bursts(items):
        first, last = b[0], b[-1]
        if len(b) == 1:
            when = first["ts_raw"]
        else:
            span = (last["ts"] - first["ts"]).total_seconds()
            when = "%s .. %s (%ds, %d veces)" % (
                first["ts_raw"], last["ts"].strftime("%H:%M:%SZ"), span, len(b))
        print("  %s" % when)
        print("    causa: %s" % (cause[:110]))
        print("    tipo:  %s | pid %s | node %s" % (
            first["reason"], first["pid"], first["node"]))
        if first["uptimeMs"] is not None:
            print("    vivio: %.1fs antes de caer" % (first["uptimeMs"] / 1000))
    print("")

print("HIPOTESIS")
seen_hypotheses = set()
for cause, items in sorted(by_cause.items(), key=lambda kv: -len(kv[1])):
    low = cause.lower()
    if "tailscale" in low:
        if "tailscale" in seen_hypotheses:
            continue
        seen_hypotheses.add("tailscale")
        print("  - '%s' (%dx): el gateway no arranca si Tailscale esta detenido" % (cause[:60], len(items)))
        print("    porque lo usa para reclamar la ruta. No es un bug de OpenClaw:")
        print("    es una dependencia no declarada. Si Tailscale es opcional para")
        print("    este host, conviene revisar la config de ruta; si no, el arranque")
        print("    depende de que Tailscale este siempre arriba.")
    elif "shutdown did not complete" in low or "shutdown_timeout" in items[0]["reason"]:
        if "shutdown" in seen_hypotheses:
            print("      (y %dx mas con la misma causa de apagado)" % len(items))
            continue
        seen_hypotheses.add("shutdown")
        print("  - Apagado que no completa: el proceso no cierra a tiempo.")
        print("    Suele ser trabajo en vuelo (requests, streams, timers) que no")
        print("    respeta el deadline. No impide arrancar, pero deja estado sucio.")
    elif "stopped" in low:
        print("  - '%s' (%dx): dependencia externa caida al arrancar." % (cause[:60], len(items)))
    else:
        print("  - '%s' (%dx): sin patron conocido, revisar a mano." % (cause[:60], len(items)))

print("")
print("Este informe es una lectura automatica de los reportes. No reemplaza")
print("la revision humana de un incidente con impacto en produccion.")

if unreadable:
    print("")
    print("ARCHIVOS ILEGIBLES (%d)" % len(unreadable))
    for n, e in unreadable:
        print("  - %s: %s" % (n, e))
PY
