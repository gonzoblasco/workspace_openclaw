#!/usr/bin/env bats
# Tests for scripts/changelog-rotate.py (CHANGELOG active-window rotation, ADR-092).
# El runner real del pre-commit es bats; el script se prueba contra un root temporal.

SCRIPT="$BATS_TEST_DIRNAME/../../scripts/changelog-rotate.py"

setup() {
  ROOT=$(mktemp -d)
  mkdir -p "$ROOT/docs/archive"
  export ROOT
}

teardown() {
  rm -rf "$ROOT"
}

seed() {
  cat > "$ROOT/docs/CHANGELOG.md" <<'EOF'
# CHANGELOG.md

head

---

## [2026-10-06] - new

body new

## [2026-08-01] - old

body old
EOF
}

@test "changelog-rotate: --check reports drift (exit 1)" {
  seed
  run python3 "$SCRIPT" --check --today 2026-10-06 --root "$ROOT"
  [ "$status" -eq 1 ]
  [[ "$output" == *"DESFASADO"* ]]
}

@test "changelog-rotate: rotation keeps window, archives the rest" {
  seed
  run python3 "$SCRIPT" --today 2026-10-06 --root "$ROOT"
  [ "$status" -eq 0 ]
  grep -q "body new" "$ROOT/docs/CHANGELOG.md"
  ! grep -q "body old" "$ROOT/docs/CHANGELOG.md"
  grep -q "body old" "$ROOT/docs/archive/CHANGELOG-archive.md"
}

@test "changelog-rotate: idempotent (second run is a no-op)" {
  seed
  python3 "$SCRIPT" --today 2026-10-06 --root "$ROOT"
  run python3 "$SCRIPT" --today 2026-10-06 --root "$ROOT"
  [ "$status" -eq 0 ]
  [[ "$output" == *"ya en ventana"* ]]
}

@test "changelog-rotate: --check clean after rotation (exit 0)" {
  seed
  python3 "$SCRIPT" --today 2026-10-06 --root "$ROOT"
  run python3 "$SCRIPT" --check --today 2026-10-06 --root "$ROOT"
  [ "$status" -eq 0 ]
  [[ "$output" == *"OK"* ]]
}

@test "changelog-rotate: --dry-run does not write" {
  seed
  before=$(cat "$ROOT/docs/CHANGELOG.md")
  run python3 "$SCRIPT" --dry-run --today 2026-10-06 --root "$ROOT"
  [ "$status" -eq 0 ]
  [ "$before" = "$(cat "$ROOT/docs/CHANGELOG.md")" ]
  [ ! -f "$ROOT/docs/archive/CHANGELOG-archive.md" ]
}

@test "changelog-rotate: bad date is a usage error (exit 2)" {
  seed
  run python3 "$SCRIPT" --today not-a-date --root "$ROOT"
  [ "$status" -eq 2 ]
}
