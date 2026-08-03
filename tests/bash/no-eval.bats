#!/usr/bin/env bats
# Ensure no script uses eval "$cmd" anti-pattern

@test "no eval \"\$cmd\" in any bash skill script" {
  run bash -c 'grep -rn '"'"'eval "\$cmd"'"'"' "$HOME/.openclaw/workspace/skills"/*/scripts/*.sh 2>/dev/null || true'
  [ -z "$output" ]
}
