#!/bin/bash
# aggregate-sync.sh - RETIRED (2026-10-13, ADR-098)
#
# This script used to sync the private aggregate repo `projects_openclaw`
# (a flat mirror of `projects/`). Under ADR-098 the aggregate layer does not
# exist: `projects/` is a flat container folder, 100% ignored by the workspace
# git, and each `projects/<slug>/` is its own git repo (source of truth, with
# its own `.knowledge/`). There is nothing to aggregate.
#
# Verified 2026-10-13: `projects/` has no `.git` of its own; `git -C projects`
# resolves to the workspace `.git`. `gonzoblasco/projects_openclaw` is archived.
#
# Kept as a stub (not deleted) so any old reference or automation fails loudly
# with the reason instead of a confusing git error. Per ADR-067 §4: archive
# before deleting - the record of a retired mechanism is what stops it recurring.

set -euo pipefail

echo "aggregate-sync.sh RETIRED (2026-10-13, ADR-098)."
echo ""
echo "There is no aggregate repo. \`projects/\` is a flat container folder, ignored"
echo "100% by the workspace git; each \`projects/<slug>/\` is its own git repo"
echo "(source of truth, with its own \`.knowledge/\`)."
echo ""
echo "Work with the project directly:"
echo "  git -C projects/<slug> status"
echo "  git -C projects/<slug> push"
exit 1
