#!/bin/bash
# preflight.sh — Verifica prerequisitos para deploy
# Output: JSON con { vercelToken, ghAuth, projectLinked, status }

VERCEL_TOKEN="${VERCEL_TOKEN:-}"

RESULTS="["

# Check 1: VERCEL_TOKEN
if [ -n "$VERCEL_TOKEN" ]; then
  RESULTS+="{\"check\":\"VERCEL_TOKEN\",\"status\":\"ok\"}"
else
  RESULTS+="{\"check\":\"VERCEL_TOKEN\",\"status\":\"fail\",\"error\":\"VERCEL_TOKEN not set\"}"
fi

# Check 2: gh auth
if gh auth status 2>&1 | grep -q "Logged in"; then
  RESULTS+=",{\"check\":\"gh auth\",\"status\":\"ok\"}"
else
  RESULTS+=",{\"check\":\"gh auth\",\"status\":\"fail\",\"error\":\"Not logged in to GitHub CLI\"}"
fi

# Check 3: vercel.json or .vercel
if [ -f "vercel.json" ] || [ -d ".vercel" ]; then
  RESULTS+=",{\"check\":\"vercel project\",\"status\":\"ok\"}"
else
  RESULTS+=",{\"check\":\"vercel project\",\"status\":\"fail\",\"error\":\"No vercel.json or .vercel found\"}"
fi

RESULTS+="]"

# Overall status
OVERALL="ok"
if echo "$RESULTS" | grep -q "fail"; then
  OVERALL="fail"
fi

cat <<EOF
{
  "status": "$OVERALL",
  "checks": $RESULTS
}
EOF
