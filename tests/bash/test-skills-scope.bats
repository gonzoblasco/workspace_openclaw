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
    echo "name: x"
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
  # Cada asercion termina en `|| return 1`. En Bats una asercion intermedia que
  # falla NO falla el test: solo cuenta el exit status del ULTIMO comando. Con
  # `[[ ... ]]` sueltos, un test puede salir "ok" habiendo verificado nada.
  # Se detecto el 2026-11-04: este test pasaba en local y fallaba en CI por el
  # ultimo assert, mientras el del contador (roto desde que el em dash dejo de
  # bloquear) nunca se evaluo. Un test que pasa por un assert ciego miente.
  [ "$status" -eq 0 ] || return 1
  # El formato vigente es "N ok, M aviso(s)": el em dash informa, no bloquea
  # (regla del owner 2026-11-04: tipografia no es correccion).
  # El archivo es untracked: queda fuera del scope, asi que el contador de
  # avisos debe seguir en 0. El invariante que se prueba aca es el SCOPE.
  [[ "$output" == *"Em dash:     0 ok, 0 aviso(s)"* ]] || return 1
  [[ "$output" != *"untracked-bad"* ]] || return 1
}

@test "test-skills: staged SKILL.md with em dash warns but does not block" {
  # Owner rule 2026-11-04: tipografia no es correccion. El gate informa y el
  # commit sigue; bloquear por un guion largo detiene trabajo legitimo.
  skill "skills/bad/SKILL.md" emdash
  git -C "$WS" add skills/bad/SKILL.md
  run "$WS/scripts/test-skills.sh"
  [ "$status" -eq 0 ] || return 1
  [[ "$output" == *"no bloquea"* ]] || return 1
  [[ "$output" == *"skills/bad/SKILL.md"* ]] || return 1
  [[ "$output" != *"em dash FAIL"* ]] || return 1
}

@test "test-skills: --all prunes node_modules" {
  # Lo que este test prueba es el PRUNING, y la prueba es por AUSENCIA: si
  # node_modules no se pruneara, el scan reportaria su SKILL.md con em dash y la
  # ruta apareceria en el output. Ese es el assert que vale.
  #
  # Antes habia ademas un assert sobre el contador ("Em dash: 1 ok, 0 ..."). Se
  # saco (2026-11-04): acoplaba el test de PRUNING al formato del reporte de
  # EM DASH. Si manana cambia ese resumen, este test fallaba por un motivo que no
  # tiene nada que ver con lo que dice probar. El contrato del em dash lo cubre
  # el test de arriba, que si es suyo.
  skill "skills/ok/SKILL.md"
  skill "skills/dep/node_modules/third-party/SKILL.md" emdash
  run "$WS/scripts/test-skills.sh" --all
  [ "$status" -eq 0 ]
  [[ "$output" != *"node_modules"* ]]
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
