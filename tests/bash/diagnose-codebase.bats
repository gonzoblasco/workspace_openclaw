#!/usr/bin/env bats
# Tests for skills/vibe-code-cleanup/scripts/diagnose-codebase.sh

SCRIPT="$BATS_TEST_DIRNAME/../../skills/vibe-code-cleanup/scripts/diagnose-codebase.sh"

setup() {
  TMP_DIR=$(mktemp -d)
  export TMP_DIR
}

teardown() {
  rm -rf "$TMP_DIR"
}

@test "diagnose-codebase: detects issues in sample code" {
  mkdir -p "$TMP_DIR/src"
  printf 'let x: any = 1;\nconsole.log(x);\n// TODO: fix\nconst API_KEY = "***";\n' > "$TMP_DIR/src/app.ts"

  cd "$TMP_DIR"
  run bash "$SCRIPT" --dir src
  [ "$status" -eq 0 ]

  REPORT=$(ls *.md | head -1)
  [ -f "$REPORT" ]
  run cat "$REPORT"
  [[ "$output" == *"TypeScript files:** 1"* ]]
  [[ "$output" == *"Total lines:** 4"* ]]
}

@test "diagnose-codebase: finds potential secrets case-insensitively" {
  mkdir -p "$TMP_DIR/src"
  printf 'const API_KEY = "***";\n' > "$TMP_DIR/src/app.ts"

  cd "$TMP_DIR"
  bash "$SCRIPT" --dir src >/dev/null 2>&1
  REPORT=$(ls *.md | head -1)
  run cat "$REPORT"
  [[ "$output" == *"Potential secrets"* ]]
}

@test "diagnose-codebase: no eval remains" {
  run grep -n 'eval "\$cmd"' "$SCRIPT"
  [ "$status" -ne 0 ]
}
