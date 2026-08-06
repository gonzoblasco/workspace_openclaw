#!/bin/bash
# health.sh — Health checks post-deploy
# Uso: ./health.sh <url>
# Output: JSON con resultados

URL="$1"

if [ -z "$URL" ]; then
  echo '{"status":"error","error":"URL required"}'
  exit 1
fi

RESULTS="["

# HTTP 200
HTTP_CODE=$(curl -o /dev/null -s -w "%{http_code}" "$URL" 2>&1)
if [ "$HTTP_CODE" = "200" ]; then
  RESULTS+="{\"check\":\"http200\",\"status\":\"pass\",\"code\":$HTTP_CODE}"
else
  RESULTS+="{\"check\":\"http200\",\"status\":\"fail\",\"code\":$HTTP_CODE}"
fi

# Response time
RESPONSE_TIME=$(curl -o /dev/null -s -w "%{time_total}" "$URL" 2>&1)
if [ "$(echo "$RESPONSE_TIME < 2" | bc -l 2>/dev/null)" = "1" ]; then
  RESULTS+=",{\"check\":\"responseTime\",\"status\":\"pass\",\"seconds\":$RESPONSE_TIME}"
else
  RESULTS+=",{\"check\":\"responseTime\",\"status\":\"warn\",\"seconds\":$RESPONSE_TIME}"
fi

# API health (if /api/health exists)
API_CODE=$(curl -o /dev/null -s -w "%{http_code}" "$URL/api/health" 2>&1)
if [ "$API_CODE" = "200" ]; then
  RESULTS+=",{\"check\":\"apiHealth\",\"status\":\"pass\",\"code\":$API_CODE}"
elif [ "$API_CODE" = "000" ]; then
  # No API endpoint, skip
  :
else
  RESULTS+=",{\"check\":\"apiHealth\",\"status\":\"warn\",\"code\":$API_CODE}"
fi

RESULTS+="]"

OVERALL="pass"
if echo "$RESULTS" | grep -q "\"status\":\"fail\""; then
  OVERALL="fail"
fi

cat <<EOF
{
  "status": "$OVERALL",
  "url": "$URL",
  "checks": $RESULTS
}
EOF
