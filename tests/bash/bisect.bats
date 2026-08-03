#!/usr/bin/env bats
# Tests for skills/debug-agent/scripts/bisect.sh

SCRIPT="$BATS_TEST_DIRNAME/../../skills/debug-agent/scripts/bisect.sh"

setup() {
  TMP_DIR=$(mktemp -d)
  export TMP_DIR
  cd "$TMP_DIR"
  git init -q
  git config user.email "test@example.com"
  git config user.name "Test User"
  for i in 1 2 3; do
    echo "v$i" > version.txt
    git add -A
    git commit -m "commit $i" -q
    git tag "v$i"
  done
}

teardown() {
  rm -rf "$TMP_DIR"
}

@test "bisect: finds first bad commit" {
  GOOD=$(git -C "$TMP_DIR" rev-parse v1)
  run bash "$SCRIPT" "$TMP_DIR" "$GOOD" 'grep -q v2 version.txt'
  [ "$status" -eq 0 ]
  [[ "$output" == *'"status": "found"'* ]]
  [[ "$output" == *'"message": "commit 3"'* ]]
}

@test "bisect: no executable grep -oP remains" {
  # Allow comments mentioning grep -oP, but no actual command
  run bash -c 'grep -nE "^[^#]*grep -oP" "$1"' bash "$SCRIPT"
  [ -z "$output" ]
}
