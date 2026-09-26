#!/usr/bin/env bash
# frontmatter_validator.sh – ensure every SKILL.md file has a valid front‑matter block.
# If a file is missing front‑matter, a minimal block is prepended:
#   ---
#   title: <slug>
#   description: TODO: add description
#   ---
# Usage: ./scripts/frontmatter_validator.sh [paths...]
# If no paths are supplied, it scans the workspace for all `SKILL.md` files.
#
# Deteccion (corregido 2026-09-26): un SKILL.md puede empezar con un comentario
# de proyecto (`<!-- project: ... -->`) y el front-matter venir despues. Antes
# el chequeo era `head -1 | grep '^---'`, asi que esos archivos se veian "sin
# front-matter" y el script les prependia un bloque encima del que ya tenian,
# dejando dos bloques apilados y un `title: SKILL` inutil. Ahora busca el bloque
# en las primeras lineas.

set -euo pipefail

# Helper to generate a slug from the filename (basename without extension)
# Para `skills/<x>/SKILL.md` el slug es `<x>`, no `SKILL`: usar el basename daba
# `title: SKILL` en los 11 archivos a los que se les insertaba el bloque.
slug_from_path() {
  local path="$1"
  local base="$(basename "$(dirname "$path")")"
  # Remove the .md extension
  echo "${base%.md}"
}

# Gather target files
if [[ $# -gt 0 ]]; then
  TARGETS=($@)
else
  # Use a POSIX‑compatible loop to collect SKILL.md files
  TARGETS=()
  while IFS= read -r f; do
    TARGETS+=("$f")
  done < <(git ls-files "**/SKILL.md" 2>/dev/null || true)
fi

if [[ ${#TARGETS[@]} -eq 0 ]]; then
  echo "No SKILL.md files found."
  exit 0
fi

for file in "${TARGETS[@]}"; do
  if [[ ! -f $file ]]; then continue; fi
  # Check if the file already has a front‑matter block (--- ... ---) cerca del
  # inicio: en la linea 1, o despues de un comentario de proyecto.
  if head -5 "$file" | grep -q '^---$'; then
    # Assume it has front‑matter; no action needed.
    continue
  fi
  # Insert minimal front‑matter at the top of the file.
  slug=$(slug_from_path "$file")
  echo "Adding front‑matter to $file"
  tmp=$(mktemp)
  {
    echo "---"
    echo "title: $slug"
    echo "description: TODO: add description"
    echo "---"
    cat "$file"
  } > "$tmp"
  mv "$tmp" "$file"
done

echo "Front‑matter validation completed."
