#!/usr/bin/env bats
# Tests for the SCOPING of scripts/test-skills.sh (2026-10-07).
#
# Por que existe esta suite. El suite de skills corria `find` sobre TODO el
# disco en cada pre-commit. Eso bloqueaba commits AJENOS por defectos que no
# tocaban: los SKILL.md de playwright-core bajo node_modules/ (3 por copia
# instalada) y los arboles de skills de agentes todavia no trackeados. El
# sintoma era commits sin relacion forzados a --no-verify. La cura tiene dos
# mitades, y cada mitad se prueba aca:
#   1) SCOPE = staged (git diff --cached), no el disco.
#   2) node_modules/ podado del walk.
# Mas una guarda anti-verde-falso: en CI (sin staging) el default veria 0
# archivos y saldria verde sin mirar nada; el script debe abortar.
#
# El script deriva su WORKSPACE_DIR de su propia ubicacion, asi que cada test
# arma un arbol temporal con una COPIA del script real (<WS>/scripts/), su
# propio repo git, y lo invoca ahi. Se prueba el codigo real, no un doble.
#
# El em dash se emite con `$'\xe2\x80\x94'` (bash 3.2 no soporta `\u` en printf).

REAL_SCRIPT="$BATS_TEST_DIRNAME/../../scripts/test-skills.sh"

setup() {
  WS=$(mktemp -d)
  export WS
  # Aislar de CI: en GitHub Actions `CI=true` esta seteado globalmente y haria
  # que los tests 1-4 (scope local) aborten por la guarda anti-verde-hueco.
  unset CI
  mkdir -p "$WS/scripts"
  cp "$REAL_SCRIPT" "$WS/scripts/test-skills.sh"
  chmod +x "$WS/scripts/test-skills.sh"
  git -C "$WS" init -q
}

teardown() {
  rm -rf "$WS"
}

# skill <relpath> [emdash] - escribe un SKILL.md con front-matter; agrega un
# em dash U+2014 si el segundo argumento es "emdash".
skill() {
  local rel="$1" dash="${2:-}"
  mkdir -p "$WS/$(dirname "$rel")"
  {
    echo "---"
    echo "title: x"
    echo "description: d"
    echo "---"
    echo
    echo "body"
  } > "$WS/$rel"
  if [ "$dash" = "emdash" ]; then
    printf 'una raya larga: %s\n' $'\xe2\x80\x94' >> "$WS/$rel"
  fi
}

@test "test-skills: untracked SKILL.md with em dash is out of the default scope" {
  skill "skills/untracked-bad/SKILL.md" emdash
  run "$WS/scripts/test-skills.sh"
  [ "$status" -eq 0 ]
  [[ "$output" == *"Em dash:     0 ok, 0 failed"* ]]
  [[ "$output" != *"untracked-bad"* ]]
}

@test "test-skills: staged SKILL.md with em dash still fails" {
  skill "skills/bad/SKILL.md" emdash
  git -C "$WS" add skills/bad/SKILL.md
  run "$WS/scripts/test-skills.sh"
  [ "$status" -eq 1 ]
  [[ "$output" == *"em dash FAIL"* ]]
  [[ "$output" == *"skills/bad/SKILL.md"* ]]
}

@test "test-skills: --all prunes node_modules" {
  skill "skills/ok/SKILL.md"
  skill "skills/dep/node_modules/third-party/SKILL.md" emdash
  run "$WS/scripts/test-skills.sh" --all
  [ "$status" -eq 0 ]
  [[ "$output" != *"node_modules"* ]]
  [[ "$output" == *"Em dash:     1 ok, 0 failed"* ]]
}

@test "test-skills: staged path outside the skill roots is not scanned" {
  mkdir -p "$WS/scripts"
  printf 'this is not bash (( (\n' > "$WS/scripts/broken.sh"
  git -C "$WS" add scripts/broken.sh
  run "$WS/scripts/test-skills.sh"
  [ "$status" -eq 0 ]
  [[ "$output" == *"0 file(s) under skill roots"* ]]
}

@test "test-skills: CI without --all aborts instead of a hollow green" {
  skill "skills/ok/SKILL.md"
  git -C "$WS" add skills/ok/SKILL.md
  run env CI=true "$WS/scripts/test-skills.sh"
  [ "$status" -eq 1 ]
  [[ "$output" == *"ABORT"* ]]
}
