#!/usr/bin/env bash
set -euo pipefail

# Source: Quaternius RPG Character Pack — https://quaternius.com/packs/rpgcharacters.html
# License: CC0 1.0. Downloads one character only; the pack is not redistributed.
# Run from anywhere: resolves the project root from this script.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${SCRIPT_DIR}"

URL="https://drive.google.com/uc?export=download&id=1oALqyqy7yVQnLh-Vs19kKg3eZgJqIgoc"
DEST_DIR="assets/quaternius/rpg-characters"
FILE="${DEST_DIR}/Warrior.gltf"

mkdir -p "${DEST_DIR}"

if [[ -f "${FILE}" ]]; then
  echo "Warrior.gltf already exists. Skipping download."
else
  echo "Downloading Warrior.gltf..."
  curl -L --fail --silent --show-error -o "${FILE}" "${URL}"
fi

if [[ "$(head -c 1 "${FILE}")" != "{" ]]; then
  echo "Verification failed: file does not start with '{'"
  exit 1
fi

SIZE="$(stat -f%z "${FILE}" 2>/dev/null || stat -c%s "${FILE}")"
if (( SIZE < 1048576 )); then
  echo "Verification failed: file size (${SIZE} bytes) is less than 1 MB"
  exit 1
fi

echo "Asset fetched and verified successfully (${SIZE} bytes)."

# Additional assets for Day 3: House and Tree.

# House asset
HOUSE_URL="https://drive.google.com/uc?export=download&id=1ITHANc2S6cJxNRx0O0wDfEmYC4nXBBVg"
HOUSE_DEST_DIR="assets/quaternius/rts"
HOUSE_FILE="${HOUSE_DEST_DIR}/Houses_FirstAge_1_Level1.gltf"
mkdir -p "${HOUSE_DEST_DIR}"
if [[ -f "${HOUSE_FILE}" ]]; then
  echo "House.gltf already exists. Skipping download."
else
  echo "Downloading House.gltf..."
  curl -L --fail --silent --show-error -o "${HOUSE_FILE}" "${HOUSE_URL}"
fi
if [[ "$(head -c 1 \"${HOUSE_FILE}\")" != "{" ]]; then
  echo "Verification failed: House file does not start with '{'"
  exit 1
fi
HOUSE_SIZE="$(stat -f%z \"${HOUSE_FILE}\" 2>/dev/null || stat -c%s \"${HOUSE_FILE}\")"
if (( HOUSE_SIZE < 1024 )); then
  echo "Verification failed: House file size (${HOUSE_SIZE} bytes) is unexpectedly small"
  exit 1
fi

# Tree asset
TREE_URL="https://drive.google.com/uc?export=download&id=1SxfLA9jE6fza2y9vedlEornDJX-622QJ"
TREE_DEST_DIR="assets/quaternius/rts"
TREE_FILE="${TREE_DEST_DIR}/Resource_Tree1.gltf"
mkdir -p "${TREE_DEST_DIR}"
if [[ -f "${TREE_FILE}" ]]; then
  echo "Tree.gltf already exists. Skipping download."
else
  echo "Downloading Tree.gltf..."
  curl -L --fail --silent --show-error -o "${TREE_FILE}" "${TREE_URL}"
fi
if [[ "$(head -c 1 \"${TREE_FILE}\")" != "{" ]]; then
  echo "Verification failed: Tree file does not start with '{'"
  exit 1
fi
TREE_SIZE="$(stat -f%z \"${TREE_FILE}\" 2>/dev/null || stat -c%s \"${TREE_FILE}\")"
if (( TREE_SIZE < 1024 )); then
  echo "Verification failed: Tree file size (${TREE_SIZE} bytes) is unexpectedly small"
  exit 1
fi

echo "All additional assets fetched and verified successfully."
