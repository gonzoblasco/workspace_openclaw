#!/usr/bin/env bash
# Politica de drift y presupuesto de riesgo de OPS (E4.1 + E4.3).
#
# Clasifica cada campo cambiado entre el baseline y el config vivo por
# REVERSIBILIDAD, y decide si OPS puede resolverlo solo o debe escalar.
#
# Uso:
#   risk-policy.sh              # informe legible
#   risk-policy.sh --json       # legible por maquina
#
# Exit codes:
#   0 = todo lo pendiente es riesgo BAJO -> OPS puede auto-aceptar
#   1 = hay riesgo MEDIO o ALTO       -> escalar a Gonzo
#   2 = no se pudo evaluar            -> escalar (nunca asumir sano)
#
# POR QUE ESTE SCRIPT EXISTE Y NO UN FLAG EN drift.sh:
# drift.sh mide. Esta politica decide. Mezclarlas haria que el medidor
# tenga permiso de escribir, que es exactamente como se acepta a ciegas.
set -uo pipefail

CONFIG="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"
BASELINE="${OPENCLAW_BASELINE:-$HOME/.openclaw/gateway-config.baseline.json}"
JSON_OUT=false

for arg in "$@"; do
  case "$arg" in
    --json) JSON_OUT=true ;;
    *) echo "Unknown arg: $arg" >&2; exit 2 ;;
  esac
done

if [[ ! -f "$CONFIG" ]]; then
  echo "ERROR: no existe $CONFIG" >&2
  exit 2
fi
if [[ ! -f "$BASELINE" ]]; then
  echo "ERROR: no existe el baseline $BASELINE. Correr gateway-config-drift.sh primero." >&2
  exit 2
fi

python3 - "$CONFIG" "$BASELINE" "$JSON_OUT" <<'PY'
import json, sys, re

config_path, baseline_path, json_out = (
    sys.argv[1], sys.argv[2], sys.argv[3] == "true"
)

def flatten(node, prefix=""):
    out = {}
    if isinstance(node, dict):
        if not node:
            out[prefix] = "{}"
        for k, v in node.items():
            out.update(flatten(v, f"{prefix}.{k}" if prefix else k))
    elif isinstance(node, list):
        try:
            canon = sorted(node, key=lambda x: json.dumps(x, sort_keys=True))
        except Exception:
            canon = node
        out[prefix] = json.dumps(canon, sort_keys=True)
    else:
        out[prefix] = json.dumps(node, sort_keys=True)
    return out

try:
    with open(config_path) as f:
        new = flatten(json.load(f))
    old = {}
    with open(baseline_path) as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            k, _, v = line.partition("\t")
            old[k] = v
except Exception as e:
    print("ERROR: no se pudo leer config o baseline: %s" % e, file=sys.stderr)
    sys.exit(2)

# ---------------------------------------------------------------------------
# CLASIFICACION POR REVERSIBILIDAD
#
# ALTO: si esto esta mal, el gateway puede no arrancar, se pierde acceso, o se
#       expone o destruye algo. NUNCA se auto-acepta. Ni con allowlist.
# MEDIO: reversible pero con efecto operativo (cambia quien recibe trabajo,
#       que corre, con que frecuencia). Se escala salvo que el cambio sea trivial.
# BAJO: rotacion normal del runtime o preferencia por agente. Auto-aceptable.
#
# REGLA QUE MANDA SOBRE TODAS: **la allowlist nunca gana sobre un patron de
# riesgo alto.** Un campo permitido por drift.sh que tambien sea de riesgo alto
# se clasifica ALTO. El silencio del medidor no es permiso de la politica.
# ---------------------------------------------------------------------------

HIGH = [
    # gateway.auth.token NO va aca: el runtime lo rota solo y es BAJO. Un token
    # nuevo no es "exponer acceso", es rotacion. Lo que si es ALTO es cambiar
    # QUIEN entra (port, bind, host, tls, trustProxy).
    (r'^(gateway\.(port|bind|host|tls|trustProxy)\b)', 'expone o corta el acceso al gateway'),
    (r'^(gateway\.(remote|controlUi|allow)\w*)', 'superficie de acceso remoto'),
    (r'^(hooks\.(enabled|allowedAgentIds|auth)\b)', 'quien puede ejecutar hooks'),
    (r'^(tools\.(approval|allow|deny)\w*)', 'aprobaciones y alcance de herramientas'),
    (r'^(security\.|sandbox\.)', 'limites de seguridad'),
    (r'^(secrets\.|models\.providers\.[\w-]+\.apiKey)', 'credenciales'),
    (r'^(plugins\.entries\.[\w-]+\.enabled)', 'habilita o corta funcionalidad entera'),
    (r'^(channels\.[\w-]+\.(token|enabled|accounts))', 'canal de comunicacion'),
]

MEDIUM = [
    (r'^(agents\.entries\.[\w-]+\.(agent|workspace|cwd|agentDir))$', 'ruta de trabajo de un agente'),
    (r'^(agents\.entries\.[\w-]+\.(tools|toolsAllow|model\.fallbacks))\b', 'poderes o respaldo de un agente'),
    (r'^(agents\.entries\.[\w-]+\.heartbeat)\b', 'un agente pasa a latir solo, con su propio prompt e intervalo'),
    (r'^(automations\.|jobs\.)', 'que corre y cuando'),
    (r'^(agents\.defaults\.(tools|heartbeat|contextPruning))\b', 'comportamiento por defecto'),
    (r'^(compaction\.|memory\.)', 'retencion y contexto'),
]

LOW = [
    (r'^(agents\.entries\.[\w-]+\.model\.primary)$', 'modelo de un agente, reversible con config set'),
    (r'^(agents\.defaults\.model\.primary)$', 'modelo por defecto, reversible'),
    (r'^(update\.|meta\.|telemetry\.|wizard\.)', 'metadatos y rotacion del runtime'),
    (r'^(gateway\.auth\.token)$', 'token rotado por el propio runtime'),
]

def classify(path):
    for pattern, why in HIGH:
        if re.search(pattern, path):
            return "ALTO", why
    for pattern, why in MEDIUM:
        if re.search(pattern, path):
            return "MEDIO", why
    for pattern, why in LOW:
        if re.search(pattern, path):
            return "BAJO", why
    # Sin patron conocido: no es "bajo por default". Un campo que la politica
    # no entiende es justamente el que hay que mirar.
    return "MEDIO", "campo no clasificado: revisar a mano"

changed = []
for path in sorted(set(old) | set(new)):
    o, n = old.get(path), new.get(path)
    if o == n:
        continue
    level, why = classify(path)
    changed.append({
        "path": path,
        "old": o if o is not None else "<ausente>",
        "new": n if n is not None else "<ausente>",
        "risk": level,
        "why": why,
    })

counts = {"ALTO": 0, "MEDIO": 0, "BAJO": 0}
for c in changed:
    counts[c["risk"]] += 1

verdict = "AUTO_ACEPTAR" if (changed and counts["ALTO"] == 0 and counts["MEDIO"] == 0) else (
    "SIN_DRIFT" if not changed else "ESCALAR"
)

if json_out:
    print(json.dumps({
        "verdict": verdict,
        "counts": counts,
        "changes": changed,
        "rule": "la allowlist nunca gana sobre un patron de riesgo alto",
    }, ensure_ascii=False, indent=2))
    sys.exit(0 if verdict in ("AUTO_ACEPTAR", "SIN_DRIFT") else 1)

print("POLITICA DE RIESGO: drift pendiente clasificado")
print("Config:   %s" % config_path)
print("Baseline: %s" % baseline_path)
print("")

if not changed:
    print("SIN DRIFT. Nada que clasificar.")
    sys.exit(0)

for level in ("ALTO", "MEDIO", "BAJO"):
    items = [c for c in changed if c["risk"] == level]
    if not items:
        continue
    print("%s (%d)" % (level, len(items)))
    for c in items:
        print("  %s" % c["path"])
        print("    %s -> %s" % (c["old"][:60], c["new"][:60]))
        print("    porque: %s" % c["why"])
    print("")

print("VEREDICTO: %s" % verdict)
if verdict == "AUTO_ACEPTAR":
    print("Todo lo pendiente es riesgo BAJO y reversible. OPS puede aceptar el")
    print("baseline solo, dejando registro en el change log.")
elif verdict == "ESCALAR":
    if counts["ALTO"]:
        print("Hay %d campo(s) de riesgo ALTO. NO se auto-acepta, aunque esten en" % counts["ALTO"])
        print("la allowlist del medidor: la allowlist no gana sobre el riesgo.")
    if counts["MEDIO"]:
        unclassified = sum(1 for c in changed if c["why"] == "campo no clasificado: revisar a mano")
        if unclassified:
            print("Hay %d campo(s) de riesgo MEDIO, de los cuales %d sin clasificar."
                  % (counts["MEDIO"], unclassified))
        else:
            print("Hay %d campo(s) de riesgo MEDIO." % counts["MEDIO"])
    print("Requiere OK de Gonzo.")

sys.exit(0 if verdict in ("AUTO_ACEPTAR", "SIN_DRIFT") else 1)
PY
