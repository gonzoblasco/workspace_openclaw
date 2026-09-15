#!/usr/bin/env bats
# Tests for scripts/pipeline-queue.sh (Fase 0: durable execution queue).
# Each test runs against a temp state file: PIPELINE_STATE_FILE is exported,
# so the real pipeline-state.json is never touched.

SCRIPT="$BATS_TEST_DIRNAME/../../scripts/pipeline-queue.sh"
TRACK="$BATS_TEST_DIRNAME/../../scripts/pipeline-track.sh"

setup() {
  TMP_DIR=$(mktemp -d)
  export TMP_DIR
  export PIPELINE_STATE_FILE="$TMP_DIR/state.json"
  # Deterministic retry cap for tests.
  export PIPELINE_MAX_ATTEMPTS=3
  : > "$PIPELINE_STATE_FILE"
}

teardown() {
  rm -rf "$TMP_DIR"
}

# --- enqueue ---

@test "enqueue: creates plan with attempts=0 and parity owners" {
  run bash "$SCRIPT" enqueue "test-phase" U1 U2 U3
  [ "$status" -eq 0 ]

  run jq -r '.fase' "$PIPELINE_STATE_FILE"
  [ "$output" = "test-phase" ]

  run jq -r '[.units[] | select(.name=="U1") | .owner] | .[0]' "$PIPELINE_STATE_FILE"
  [ "$output" = "A" ]
  run jq -r '[.units[] | select(.name=="U2") | .owner] | .[0]' "$PIPELINE_STATE_FILE"
  [ "$output" = "B" ]
  run jq -r '[.units[] | select(.name=="U3") | .owner] | .[0]' "$PIPELINE_STATE_FILE"
  [ "$output" = "A" ]

  run jq -c '[.units[] | .state] | unique | .[0]' "$PIPELINE_STATE_FILE"
  [ "$output" = '"queued"' ]
  run jq -c '[.units[] | .attempts] | unique | .[0]' "$PIPELINE_STATE_FILE"
  [ "$output" = '0' ]
}

@test "enqueue: with --score sets complexity" {
  run bash "$SCRIPT" enqueue "test-phase" --score 14 U1
  [ "$status" -eq 0 ]
  run jq -r '.complexity' "$PIPELINE_STATE_FILE"
  [ "$output" = "14" ]
}

# --- next ---

@test "next: returns first queued in declaration order" {
  bash "$SCRIPT" enqueue "test-phase" U1 U2 U3
  run bash "$SCRIPT" next
  [ "$status" -eq 0 ]
  [ "$output" = "U1" ]
}

@test "next: empty queue prints empty line" {
  bash "$SCRIPT" enqueue "test-phase" U1
  bash "$SCRIPT" claim U1 999999
  run bash "$SCRIPT" next
  [ "$status" -eq 0 ]
  [ "$output" = "" ]
}

# --- claim ---

@test "claim: sets running, increments attempts and records pid" {
  bash "$SCRIPT" enqueue "test-phase" U1
  run bash "$SCRIPT" claim U1 12345
  [ "$status" -eq 0 ]

  run jq -r '.units[0] | .state' "$PIPELINE_STATE_FILE"
  [ "$output" = "running" ]
  run jq -r '.units[0] | .attempts' "$PIPELINE_STATE_FILE"
  [ "$output" = "1" ]
  run jq -r '.units[0] | .pid' "$PIPELINE_STATE_FILE"
  [ "$output" = "12345" ]
}

@test "claim: second claim on already-running unit is idempotent (no dup, no attempts++)" {
  bash "$SCRIPT" enqueue "test-phase" U1
  # The idempotency rule only applies to a LIVE pid (spec rule 6):
  # a dead pid on a running unit is treated as a re-claim.
  sleep 60 &
  LIVE_PID=$!
  bash "$SCRIPT" claim U1 "$LIVE_PID"

  run bash "$SCRIPT" claim U1 "$LIVE_PID"
  [ "$status" -eq 0 ]
  run jq -r '.units[0] | .attempts' "$PIPELINE_STATE_FILE"
  [ "$output" = "1" ]
  run jq -c '[.units[]] | length' "$PIPELINE_STATE_FILE"
  [ "$output" = "1" ]
  kill "$LIVE_PID" 2>/dev/null || true
}

@test "claim: unknown unit fails with exit 2" {
  run bash "$SCRIPT" claim NOPE 12345
  [ "$status" -eq 2 ]
}

# --- release ---

@test "release: requeues unit while attempts below max" {
  bash "$SCRIPT" enqueue "test-phase" U1
  bash "$SCRIPT" claim U1 12345

  run bash "$SCRIPT" release U1 "flaky run"
  [ "$status" -eq 0 ]
  run jq -r '.units[0] | .state' "$PIPELINE_STATE_FILE"
  [ "$output" = "queued" ]
  run jq -r '.units[0] | .pid' "$PIPELINE_STATE_FILE"
  [ "$output" = "null" ]
  run jq -r '.units[0] | .lastError' "$PIPELINE_STATE_FILE"
  [ "$output" = "flaky run" ]
}

@test "release: exhausted attempts moves unit to failed" {
  bash "$SCRIPT" enqueue "test-phase" U1
  bash "$SCRIPT" claim U1 10001
  bash "$SCRIPT" release U1 "err1"
  bash "$SCRIPT" claim U1 10002
  bash "$SCRIPT" release U1 "err2"
  bash "$SCRIPT" claim U1 10003

  run bash "$SCRIPT" release U1 "err3"
  [ "$status" -eq 0 ]
  run jq -r '.units[0] | .state' "$PIPELINE_STATE_FILE"
  [ "$output" = "failed" ]
  run jq -r '.units[0] | .attempts' "$PIPELINE_STATE_FILE"
  [ "$output" = "3" ]
  run jq -r '.units[0] | .pid' "$PIPELINE_STATE_FILE"
  [ "$output" = "null" ]
}

@test "release: unknown unit fails with exit 2" {
  run bash "$SCRIPT" release NOPE
  [ "$status" -eq 2 ]
}

# --- failed does not block the queue ---

@test "next: skips failed units and returns next queued" {
  bash "$SCRIPT" enqueue "test-phase" U1 U2 U3
  bash "$SCRIPT" claim U1 10001
  bash "$SCRIPT" release U1 "err1"
  bash "$SCRIPT" claim U1 10002
  bash "$SCRIPT" release U1 "err2"
  bash "$SCRIPT" claim U1 10003
  bash "$SCRIPT" release U1 "err3"

  run jq -r '.units[0] | .state' "$PIPELINE_STATE_FILE"
  [ "$output" = "failed" ]

  run bash "$SCRIPT" next
  [ "$status" -eq 0 ]
  [ "$output" = "U2" ]
}

# --- orphan detection ---

@test "orphans: running unit with dead pid is listed" {
  bash "$SCRIPT" enqueue "test-phase" U1 U2
  # U1 gets a dead pid (orphan); U2 gets a live pid (not an orphan).
  sleep 60 &
  LIVE_PID=$!
  bash "$SCRIPT" claim U1 999999
  bash "$SCRIPT" claim U2 "$LIVE_PID"

  run bash "$SCRIPT" orphans
  [ "$status" -eq 0 ]
  [ "$output" = "U1" ]
  kill "$LIVE_PID" 2>/dev/null || true
}

@test "orphans: running unit without pid is not considered orphan (old plan compat)" {
  # Old plans miss attempts/pid: build one by hand via pipeline-track + jq.
  bash "$TRACK" init "legacy" L1
  run bash "$SCRIPT" orphans
  [ "$status" -eq 0 ]
  [ "$output" = "" ]
}

@test "tick: requeues orphan and prints next unit" {
  bash "$SCRIPT" enqueue "test-phase" U1 U2
  bash "$SCRIPT" claim U1 999999

  run bash "$SCRIPT" tick
  [ "$status" -eq 0 ]
  run jq -r '.units[0] | .state' "$PIPELINE_STATE_FILE"
  [ "$output" = "queued" ]
  run jq -r '.units[0] | .pid' "$PIPELINE_STATE_FILE"
  [ "$output" = "null" ]
  # Next in declaration order after requeue.
  run jq -r '[.units[] | select(.state == "queued") | .name] | .[0]' "$PIPELINE_STATE_FILE"
  [ "$output" = "U1" ]
}

# --- report ---

@test "report: shows telemetry for claimed unit" {
  bash "$SCRIPT" enqueue "test-phase" U1
  bash "$SCRIPT" claim U1 12345

  run bash "$SCRIPT" report
  [ "$status" -eq 0 ]
  echo "$output" | grep -q "U1"
  echo "$output" | grep -q "running"
}

# --- old state without attempts/pid reads without error ---

@test "old plan without attempts/pid: report and status read without error" {
  bash "$TRACK" init "legacy" L1
  run bash "$SCRIPT" report
  [ "$status" -eq 0 ]
  echo "$output" | grep -q "L1"

  run bash "$SCRIPT" status
  [ "$status" -eq 0 ]
  echo "$output" | grep -q "L1"
}

@test "old plan without attempts/pid: is selectable by next" {
  bash "$TRACK" init "legacy" L1 L2
  # Simulate L1 started long ago in the old tool: running, dead process,
  # no pid field (old format). Not an orphan; next still respects states.
  run bash "$SCRIPT" next
  [ "$status" -eq 0 ]
  [ "$output" = "L1" ]
}

# --- regression: corrupt and hostile state ---

@test "corrupt state file: read commands fail loud with exit 2" {
  echo 'this is not json' > "$PIPELINE_STATE_FILE"

  run bash "$SCRIPT" next
  [ "$status" -eq 2 ]
  [[ "$output" == *"corrupt"* || "$output" == *"no es JSON"* ]]

  run bash "$SCRIPT" status
  [ "$status" -eq 2 ]
}

@test "empty state file: treated as empty queue, not an error" {
  : > "$PIPELINE_STATE_FILE"
  run bash "$SCRIPT" next
  [ "$status" -eq 0 ]
  [ "$output" = "" ]
}

@test "corrupt state file: enqueue still works as the recovery path" {
  echo 'garbage' > "$PIPELINE_STATE_FILE"
  run bash "$SCRIPT" enqueue "recovered" U1
  [ "$status" -eq 0 ]
  run jq -r '.units[0].name' "$PIPELINE_STATE_FILE"
  [ "$output" = "U1" ]
}

@test "PIPELINE_MAX_ATTEMPTS non-numeric falls back to 3 instead of leaking an error" {
  bash "$SCRIPT" enqueue "test-phase" U1
  run env PIPELINE_MAX_ATTEMPTS=abc bash "$SCRIPT" claim U1 12345
  [ "$status" -eq 0 ]
  [[ "$output" != *"integer expression expected"* ]]
  run jq -r '.units[0].state' "$PIPELINE_STATE_FILE"
  [ "$output" = "running" ]
}

@test "PIPELINE_MAX_ATTEMPTS zero is rejected and falls back to 3" {
  bash "$SCRIPT" enqueue "test-phase" U1
  run env PIPELINE_MAX_ATTEMPTS=0 bash "$SCRIPT" claim U1 12345
  [ "$status" -eq 0 ]
  run jq -r '.units[0].state' "$PIPELINE_STATE_FILE"
  [ "$output" = "running" ]
}

@test "orphans: pid 0 and pid -1 are dead, not always-alive" {
  # kill -0 0 and kill -0 -1 succeed, so a naive check never requeues them.
  for bad in 0 -1; do
    printf '{"fase":"t","units":[{"name":"U1","state":"running","owner":"A","note":"","startTime":null,"endTime":null,"iterations":0,"regressions":0,"attempts":1,"pid":"%s"}]}' "$bad" > "$PIPELINE_STATE_FILE"
    run bash "$SCRIPT" orphans
    [ "$status" -eq 0 ]
    [ "$output" = "U1" ]
  done
}

@test "orphans: non-numeric pid is treated as dead" {
  printf '{"fase":"t","units":[{"name":"U1","state":"running","owner":"A","note":"","startTime":null,"endTime":null,"iterations":0,"regressions":0,"attempts":1,"pid":"abc"}]}' > "$PIPELINE_STATE_FILE"
  run bash "$SCRIPT" orphans
  [ "$status" -eq 0 ]
  [ "$output" = "U1" ]
}
