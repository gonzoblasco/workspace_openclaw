#!/usr/bin/env bash
# dispatch-validation.sh - Validate that the Core does not execute a skill belonging to another agent.
# Usage: dispatch-validation.sh <skill-name> <target-agent>
#   <skill-name>   Name of the skill (directory name as in agents/<agent>/skills/).
#   <target-agent> Agent that should handle the skill (e.g., "kanam-dev", "kanam-ops", "kanam-mind", "kanam-studio" or "core").
# The Core ("core") may execute its own internal skills (listed under the Core section of SKILLS-INDEX.md).
# If the target-agent is not "core" and the skill exists under that agent's workspace, the script exits with code 1 and prints a warning.
# Otherwise it exits with code 0 (allowed).

set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: $0 <skill-name> <target-agent>"
  exit 2
fi

SKILL="$1"
TARGET_AGENT="$2"

# Determine workspace root (parent of this script's directory)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# If the target is core, allow any skill (core internal skills are not under agents directory).
if [[ "$TARGET_AGENT" == "core" ]]; then
  exit 0
fi

# Path to the skill under the target agent
SKILL_PATH="$WORKSPACE_ROOT/agents/$TARGET_AGENT/skills/$SKILL"

if [[ -d "$SKILL_PATH" ]]; then
  echo "Dispatch validation error: Core attempted to execute skill '$SKILL' which belongs to agent '$TARGET_AGENT'."
  echo "Please delegate this task to the appropriate agent instead of running it directly from the Core."
  exit 1
fi

# No conflict detected – allow execution
exit 0
