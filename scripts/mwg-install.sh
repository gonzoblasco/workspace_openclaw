#!/bin/bash
# Instala el bundle de modern-web-guidance en vendor/mwg/<version>/ (gitignored).
#
# Por que vendor y no npx en cada llamada: el bundle trae 209 guides + vectores
# cuantizados y la busqueda es 100% OFFLINE (el binario no tiene un solo fetch).
# Con el bundle local, search/retrieve tardan milisegundos y no dependen de red.
#
# Uso:  ./scripts/mwg-install.sh [version]
# Reinstalar: borrar vendor/mwg y volver a correr.

set -euo pipefail

VERSION="${1:-1.0.1}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$ROOT/vendor/mwg/$VERSION"

if [ -d "$DEST/skills/modern-web-guidance/gen" ]; then
  echo "OK: ya instalado en ${DEST#${ROOT}/}"
  exit 0
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Descargando modern-web-guidance@${VERSION}..."
URL="https://registry.npmjs.org/modern-web-guidance/-/modern-web-guidance-${VERSION}.tgz"
curl -fsSL -o "$TMP/pkg.tgz" "$URL"

# Sin verificacion no hay instalacion: el tarball viene de la red.
EXPECTED=$(curl -fsSL "https://registry.npmjs.org/modern-web-guidance/${VERSION}" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['dist']['integrity'])")
ACTUAL="sha512-$(openssl dgst -sha512 -binary "$TMP/pkg.tgz" | openssl base64 -A)"
if [ "$EXPECTED" != "$ACTUAL" ]; then
  echo "FALLA: integridad no coincide." >&2
  echo "  esperado: $EXPECTED" >&2
  echo "  obtenido: $ACTUAL" >&2
  exit 1
fi
echo "Integridad OK (sha512 contra el registry)."

mkdir -p "$DEST"
tar xzf "$TMP/pkg.tgz" -C "$DEST" --strip-components=1

if [ ! -f "$DEST/skills/modern-web-guidance/modern-web.mjs" ]; then
  echo "FALLA: el tarball no tiene la estructura esperada." >&2
  exit 1
fi

echo "Instalado en ${DEST#${ROOT}/}"
echo "Probar: DISABLE_TELEMETRY=1 node ${DEST#${ROOT}/}/skills/modern-web-guidance/modern-web.mjs search \"light dismiss dialog\""
