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
