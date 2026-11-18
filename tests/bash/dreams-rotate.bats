#!/usr/bin/env bats
# Tests for scripts/dreams-rotate.py (Dream Diary monthly rotation).

SCRIPT="$BATS_TEST_DIRNAME/../../scripts/dreams-rotate.py"

setup() {
  ROOT=$(mktemp -d)
  mkdir -p "$ROOT/memory/archive/dreaming"
  export ROOT
  cat > "$ROOT/DREAMS.md" <<'EOF'
# Dream Diary

<!-- openclaw:dreaming:diary:start -->
---

*September 9, 2026 at 5:34 AM GMT-3*

old dream A

---

*October 5, 2026 at 4:00 AM GMT-3*

new dream B

<!-- openclaw:dreaming:diary:end -->

## Deep Sleep
<!-- openclaw:dreaming:deep:start -->
- x
<!-- openclaw:dreaming:deep:end -->
EOF
}

teardown() {
  rm -rf "$ROOT"
}

@test "dreams-rotate: --check reports drift (exit 1)" {
  run python3 "$SCRIPT" --check --today 2026-10-06 --root "$ROOT"
  [ "$status" -eq 1 ]
  [[ "$output" == *"DESFASADO"* ]]
}

@test "dreams-rotate: rotation keeps current month, archives old" {
  run python3 "$SCRIPT" --today 2026-10-06 --root "$ROOT"
  [ "$status" -eq 0 ]
  grep -q "new dream B" "$ROOT/DREAMS.md"
  ! grep -q "old dream A" "$ROOT/DREAMS.md"
  grep -q "old dream A" "$ROOT/memory/archive/dreaming/DREAMS-2026-09.md"
}

@test "dreams-rotate: plugin markers stay intact" {
  python3 "$SCRIPT" --today 2026-10-06 --root "$ROOT"
  grep -q "openclaw:dreaming:diary:start" "$ROOT/DREAMS.md"
  grep -q "openclaw:dreaming:diary:end" "$ROOT/DREAMS.md"
  grep -q "openclaw:dreaming:deep:start" "$ROOT/DREAMS.md"
}

@test "dreams-rotate: idempotent (second run is a no-op)" {
  python3 "$SCRIPT" --today 2026-10-06 --root "$ROOT"
  run python3 "$SCRIPT" --today 2026-10-06 --root "$ROOT"
  [ "$status" -eq 0 ]
  [[ "$output" == *"ya en el mes en curso"* ]]
}

@test "dreams-rotate: --check clean after rotation (exit 0)" {
  python3 "$SCRIPT" --today 2026-10-06 --root "$ROOT"
  run python3 "$SCRIPT" --check --today 2026-10-06 --root "$ROOT"
  [ "$status" -eq 0 ]
  [[ "$output" == *"OK"* ]]
}

@test "dreams-rotate: --dry-run does not write" {
  before=$(cat "$ROOT/DREAMS.md")
  run python3 "$SCRIPT" --dry-run --today 2026-10-06 --root "$ROOT"
  [ "$status" -eq 0 ]
  [ "$before" = "$(cat "$ROOT/DREAMS.md")" ]
  [ ! -f "$ROOT/memory/archive/dreaming/DREAMS-2026-09.md" ]
}

@test "dreams-rotate: bad date is a usage error (exit 2)" {
  run python3 "$SCRIPT" --today not-a-date --root "$ROOT"
  [ "$status" -eq 2 ]
}

# --- multi-instancia (raiz + agents/*/DREAMS.md) -----------------------------

make_agent_diary() {
  local agent="$1" month="$2" label="$3"
  mkdir -p "$ROOT/agents/$agent"
  cat > "$ROOT/agents/$agent/DREAMS.md" <<EOF
# Dream Diary - $agent

<!-- openclaw:dreaming:diary:start -->
---

*$month 3, 2026 at 4:00 AM GMT-3*

$label

<!-- openclaw:dreaming:diary:end -->
EOF
}

@test "dreams-rotate: --check flags stale agent diaries, not only root" {
  python3 "$SCRIPT" --today 2026-10-06 --root "$ROOT"   # root queda limpio
  make_agent_diary kanam-dev September "septiembre viejo"
  run python3 "$SCRIPT" --check --today 2026-10-06 --root "$ROOT"
  [ "$status" -eq 1 ]
  [[ "$output" == *"kanam-dev=1"* ]]
}

@test "dreams-rotate: rotates each agent diary into its own archive dir" {
  make_agent_diary kanam-dev September "septiembre viejo"
  run python3 "$SCRIPT" --today 2026-10-06 --root "$ROOT"
  [ "$status" -eq 0 ]
  # el activo del agente EXISTE y conserva sus marcadores (un `! grep` solo
  # pasa igual si el archivo fue borrado: por eso el [ -f ] y los marcadores)
  [ -f "$ROOT/agents/kanam-dev/DREAMS.md" ]
  grep -q "openclaw:dreaming:diary:start" "$ROOT/agents/kanam-dev/DREAMS.md"
  grep -q "openclaw:dreaming:diary:end" "$ROOT/agents/kanam-dev/DREAMS.md"
  # el activo del agente queda solo con el mes en curso
  ! grep -q "septiembre viejo" "$ROOT/agents/kanam-dev/DREAMS.md"
  grep -q "septiembre viejo" \
    "$ROOT/memory/archive/dreaming/agents/kanam-dev/DREAMS-2026-09.md"
  # el archivo del root no se mezcla con el del agente
  [ ! -f "$ROOT/memory/archive/dreaming/DREAMS-2026-09.md" ] || \
    ! grep -q "septiembre viejo" "$ROOT/memory/archive/dreaming/DREAMS-2026-09.md"
}

@test "dreams-rotate: a failed archive leaves the active diary intact (exit 2)" {
  make_agent_diary kanam-dev September "septiembre viejo"
  # `agents` como archivo regular: mkdir del dir de archivo del agente falla
  printf 'not a dir\n' > "$ROOT/memory/archive/dreaming/agents"
  run python3 "$SCRIPT" --today 2026-10-06 --root "$ROOT"
  [ "$status" -eq 2 ]
  # la entrada vieja NO se perdio: sigue en el activo del agente
  grep -q "septiembre viejo" "$ROOT/agents/kanam-dev/DREAMS.md"
  [[ "$output" == *"Error"* ]]
}

@test "dreams-rotate: a block already archived is not duplicated" {
  make_agent_diary kanam-dev September "septiembre viejo"
  # simula una corrida que archivo bien y murio antes de reescribir el activo
  mkdir -p "$ROOT/memory/archive/dreaming/agents/kanam-dev"
  cat > "$ROOT/memory/archive/dreaming/agents/kanam-dev/DREAMS-2026-09.md" <<'EOF'
# DREAMS (archivo) - 2026-09

> Rotado desde `DREAMS.md` por `scripts/dreams-rotate.py`.

---

*September 3, 2026 at 4:00 AM GMT-3*

septiembre viejo
EOF
  run python3 "$SCRIPT" --today 2026-10-06 --root "$ROOT"
  [ "$status" -eq 0 ]
  [ "$(grep -c 'septiembre viejo' \
      "$ROOT/memory/archive/dreaming/agents/kanam-dev/DREAMS-2026-09.md")" -eq 1 ]
}

@test "dreams-rotate: --check clean across all instances after rotating" {
  make_agent_diary kanam-dev September "septiembre viejo"
  make_agent_diary kanam-mind October "octubre viejo"
  python3 "$SCRIPT" --today 2026-11-18 --root "$ROOT"
  run python3 "$SCRIPT" --check --today 2026-11-18 --root "$ROOT"
  [ "$status" -eq 0 ]
  [[ "$output" == *"OK"* ]]
}

@test "dreams-rotate: a diary without markers is skipped, not destroyed" {
  mkdir -p "$ROOT/agents/sin-marcadores"
  printf '# sin marcadores\n\n*September 9, 2026 at 5:34 AM GMT-3*\n\nviejo\n' \
    > "$ROOT/agents/sin-marcadores/DREAMS.md"
  run python3 "$SCRIPT" --today 2026-10-06 --root "$ROOT"
  [ "$status" -eq 0 ]
  grep -q "viejo" "$ROOT/agents/sin-marcadores/DREAMS.md"
}
