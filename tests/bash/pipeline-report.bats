#!/usr/bin/env bats
# Tests for scripts/pipeline-report.sh (Fase "observabilidad 0$"): it must be
# a read-only aggregate - never mutate state, correct totals, and fail loud
# on a missing/corrupt state file.

SCRIPT="$BATS_TEST_DIRNAME/../../scripts/pipeline-report.sh"

setup() {
  TMP_DIR=$(mktemp -d)
  export TMP_DIR
  export PIPELINE_STATE_FILE="$TMP_DIR/state.json"
  cat > "$PIPELINE_STATE_FILE" <<'EOF'
{"fase":"fase de test","complexity":"14","units":[
  {"name":"U1","state":"done","owner":"A","startTime":100,"endTime":150,"iterations":1,"regressions":0,"attempts":2},
  {"name":"U2","state":"done","owner":"B","startTime":150,"endTime":170,"iterations":1,"regressions":1,"attempts":1},
  {"name":"U3","state":"failed","owner":"A","startTime":170,"endTime":175,"iterations":3,"regressions":0,"attempts":3},
  {"name":"U4","state":"queued","owner":"B","startTime":null,"endTime":null,"iterations":0,"regressions":0,"attempts":0}
]}
EOF
}

teardown() {
  rm -rf "$TMP_DIR"
}

@test "report: is read-only, never mutates the state file" {
  cp "$PIPELINE_STATE_FILE" "$TMP_DIR/before.json"
  run bash "$SCRIPT"
  [ "$status" -eq 0 ]
  diff <(cat "$TMP_DIR/before.json") <(cat "$PIPELINE_STATE_FILE") # empty output = identical
}

@test "report: human output shows phase and complexity header" {
  run bash "$SCRIPT"
  [ "$status" -eq 0 ]
  echo "$output" | grep -q "# fase de test"
  echo "$output" | grep -q "T=14"
}

@test "report: totals are aggregated correctly" {
  run bash "$SCRIPT"
  [ "$status" -eq 0 ]
  # 3 measurable units (U1, U2, U3): (50) + (20) + (5) = 75s, avg 25s, max 50s
  echo "$output" | grep -q "Tiempo total: 75s sobre 3 unidades medibles"
  echo "$output" | grep -q "avg: 25s"
  echo "$output" | grep -q "max: 50s"
  # 1 regression (U2) totals across all units
  echo "$output" | grep -q "Regresiones (bugs de B al corregir): 1"
  echo "$output" | grep -q "Reintentos totales: 6"
}

@test "report: --json returns machine-readable aggregate" {
  run bash "$SCRIPT" --json
  [ "$status" -eq 0 ]
  # Capture once: `run` overwrites $output, so later queries must read a saved copy.
  local json="$output"
  run jq -r '.regressions_total' <<< "$json"
  [ "$output" = "1" ]
  run jq -r '.attempts_total' <<< "$json"
  [ "$output" = "6" ]
  run jq -r '.total_seconds' <<< "$json"
  [ "$output" = "75" ]
}

@test "report: missing state file fails loud with exit 2" {
  export PIPELINE_STATE_FILE="$TMP_DIR/nope.json"
  run bash "$SCRIPT"
  [ "$status" -eq 2 ]
}

@test "report: corrupt state file fails loud with exit 2" {
  echo 'not json' > "$TMP_DIR/bad.json"
  export PIPELINE_STATE_FILE="$TMP_DIR/bad.json"
  run bash "$SCRIPT"
  [ "$status" -eq 2 ]
}

@test "report: empty queue (no measurable units) degrades gracefully" {
  echo '{"fase":"x","units":[{"name":"U1","state":"done","owner":"A","startTime":null,"endTime":null,"iterations":0,"regressions":0,"attempts":0}]}' > "$TMP_DIR/nodur.json"
  export PIPELINE_STATE_FILE="$TMP_DIR/nodur.json"
  run bash "$SCRIPT"
  [ "$status" -eq 0 ]
  echo "$output" | grep -q "sin unidades medibles"
}
