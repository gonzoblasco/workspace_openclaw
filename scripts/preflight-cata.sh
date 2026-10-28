#!/usr/bin/env bash
# PREFLIGHT de la cata: se asegura que los dos harnesses que viven en Docker
# esten ARRIBA antes de medir.
#
# POR QUE: el 2026-10-28 Docker se reinicio y se llevo por delante los
# containers "opencode" y "openhands-canvas". El runner no los levanta: los
# USA. Sin ellos, el control falla con "No such container: opencode" y
# "Connection refused", y la corrida completa se pierde (27 celdas de cloud
# perdidas por un detail de infra).
#
# Un control fallido por infra NO es un 0 del modelo: es una ausencia. Este
# preflight evita que la ausencia se produzca.
#
# NO hace falta para "claude": ese harness corre en el host.
set -uo pipefail

WORKSPACE="/Users/gonzoblasco/.openclaw/workspace"
TOOLBOX="$WORKSPACE/scripts/ai-toolbox.py"

# Modelos que se van a medir. Se usan para verificar que opencode los
# RESUELVE (no solo que el container este de pie): en su primer arranque el
# catalogo de providers tarda en cargarse y responde "Model unavailable:
# ollama/<modelo>" aunque el container este sano.
MODELS=("$@")

need() {   # need <id> <container> <url> <codigos_aceptados...>
  local id="$1" cont="$2" url="$3"; shift 3
  local codes="$*"

  if docker ps --format '{{.Names}}' | grep -qx "$cont"; then
    echo "  $id: container '$cont' ya esta arriba"
    return 0
  fi

  echo "  $id: levantando '$cont'..."
  if ! timeout 300 "$TOOLBOX" up "$id" >/tmp/cata-preflight-$id.log 2>&1; then
    echo "  $id: FALLO al levantar (ver /tmp/cata-preflight-$id.log)"
    return 1
  fi

  # El compose puede chocar por un container homonimo parado: se resuelve
  # levantando el que quedo (el error "already in use" deja el container
  # viejo en pie, que es justo lo que queremos).
  for _ in $(seq 1 30); do
    if docker ps --format '{{.Names}}' | grep -qx "$cont"; then
      code=$(curl -s -m 5 -o /dev/null -w '%{http_code}' "$url" 2>/dev/null || echo 000)
      for ok in $codes; do
        [ "$code" = "$ok" ] && { echo "  $id: arriba (HTTP $code)"; return 0; }
      done
    fi
    sleep 2
  done
  echo "  $id: no respondio en el tiempo esperado"
  return 1
}

echo "== preflight: harnesses en Docker =="
rc=0

# opencode: puerto 4096, health en /health
need opencode opencode http://localhost:4096/health 200 || rc=1

# openhands: puerto 8000, la raiz redirige (308)
need openhands openhands-canvas http://localhost:8000/ 200 301 302 307 308 || rc=1

# Los modelos tienen que EXISTIR en el catalogo de opencode. El container
# puede estar sano y aun asi no resolver un modelo: el catalogo de providers
# se carga despues del arranque. Con el catalogo incompleto, el control
# falla por infra y se pierden 9 celdas por modelo sin que se note.
if [ "${#MODELS[@]}" -gt 0 ] && docker ps --format '{{.Names}}' | grep -qx opencode; then
  for m in "${MODELS[@]}"; do
    slug="ollama/$m"
    ok=0
    for _ in $(seq 1 15); do
      if docker exec opencode sh -c "opencode models 2>/dev/null" 2>/dev/null | grep -qxF "$slug"; then
        ok=1
        break
      fi
      sleep 2
    done
    if [ "$ok" -eq 1 ]; then
      echo "  opencode: resuelve $slug"
    else
      echo "  opencode: NO resuelve $slug (modelo ausente del catalogo)"
      rc=1
    fi
  done
fi

if [ "$rc" -ne 0 ]; then
  echo "== PREFLIGHT FALLIDO: la cata NO debe arrancar (serian celdas perdidas) =="
  exit 1
fi
echo "== preflight OK =="
exit 0
