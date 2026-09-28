#!/usr/bin/env bats
# Tests for scripts/verify-delegation.sh
#
# This suite lives under tests/bash/ on purpose: the pre-commit hook runs
# `npx bats tests/bash` whenever skills/ or scripts/ change, so wiring the gate
# here is what makes it enforced instead of an orphan script.
#
# The contract under test: 0 = pass, 1 = criteria failed, 3 = could not run.
# Zero matching artifacts is never a pass.

SCRIPT="$BATS_TEST_DIRNAME/../../scripts/verify-delegation.sh"

setup() {
  TMP_DIR=$(mktemp -d)
  export TMP_DIR
  cd "$TMP_DIR" || return 1
}

teardown() {
  rm -rf "$TMP_DIR"
}

@test "verify-delegation: exact count matches, exit 0" {
  touch a1.txt a2.txt a3.txt
  run bash "$SCRIPT" '*.txt' 3
  [ "$status" -eq 0 ]
  [[ "$output" == *"RESULT: pass"* ]]
}

@test "verify-delegation: count mismatch, exit 1" {
  touch a1.txt a2.txt a3.txt
  run bash "$SCRIPT" '*.txt' 2
  [ "$status" -eq 1 ]
  [[ "$output" == *"count mismatch"* ]]
}

@test "verify-delegation: zero artifacts is exit 3, never 0" {
  run bash "$SCRIPT" '*.txt' 0
  [ "$status" -eq 3 ]
  [[ "$output" == *"cannot run"* ]]
}

@test "verify-delegation: path-shaped pattern rejected, exit 3" {
  mkdir -p sub && touch sub/a.txt
  run bash "$SCRIPT" 'sub/*.txt' 1
  [ "$status" -eq 3 ]
  [[ "$output" == *"basename glob"* ]]
}

@test "verify-delegation: universal pattern rejected, exit 3" {
  touch a.txt
  run bash "$SCRIPT" '*' 1
  [ "$status" -eq 3 ]
  [[ "$output" == *"verifies nothing"* ]]
}

@test "verify-delegation: extra command failure gives exit 1" {
  touch b.txt
  run bash "$SCRIPT" 'b.txt' 1 false
  [ "$status" -eq 1 ]
  [[ "$output" == *"extra command failed"* ]]
}

@test "verify-delegation: extra command success gives exit 0" {
  touch b.txt
  run bash "$SCRIPT" 'b.txt' 1 true
  [ "$status" -eq 0 ]
}

@test "verify-delegation: filename with spaces counted correctly" {
  touch 'ar chivo.txt'
  run bash "$SCRIPT" 'ar chivo.txt' 1
  [ "$status" -eq 0 ]
}
