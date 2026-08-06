#!/bin/bash
# inspect.sh — Busca patrones sospechosos en archivos de código
# Uso: ./inspect.sh <file-path>
# Output: JSON con patrones encontrados

FILE_PATH="$1"

if [ -z "$FILE_PATH" ]; then
  echo '{"status":"error","error":"FILE_PATH required"}'
  exit 1
fi

if [ ! -f "$FILE_PATH" ]; then
  echo "{\"status\":\"error\",\"error\":\"File not found: $FILE_PATH\"}"
  exit 1
fi

EXT="${FILE_PATH##*.}"

# Patrones según extensión
case "$EXT" in
  ts|tsx|js|jsx)
    PATTERNS=(
      "TODO|FIXME|HACK|XXX"
      "console\.(log|error|warn)"
      "any"
      "as any"
      "// @ts-ignore"
      "// @ts-expect-error"
      "catch\s*(\w+\s*)?{?\s*$"
      "Promise\.all\b"
      "setTimeout|setInterval"
      "useEffect\s*\([^)]*\)"
      "!==\s*undefined|null"
      "===\s*undefined|null"
      "\.\.\.\w+"
      "function\s+\w+\s*\([^)]*\)\s*{"
    )
    ;;
  py)
    PATTERNS=(
      "TODO|FIXME|HACK|XXX"
      "print\("
      "except\s*:"
      "except\s+Exception\s*:"
      "try:"
      "\.\.\.\s*$"
      "pass\s*$"
    )
    ;;
  go)
    PATTERNS=(
      "TODO|FIXME|HACK|XXX"
      "fmt\.Print"
      "log\.Fatal"
      "panic\("
      "defer\s+"
      "interface\{\}"
      "_ = "
    )
    ;;
  rs)
    PATTERNS=(
      "TODO|FIXME|HACK|XXX"
      "unwrap\(\)"
      "expect\(\)"
      "println!"
      "panic!"
      "todo!"
      "unreachable!"
    )
    ;;
  *)
    PATTERNS=(
      "TODO|FIXME|HACK|XXX"
    )
    ;;
esac

RESULTS="["
FIRST=true

for PATTERN in "${PATTERNS[@]}"; do
  while IFS=: read -r LINE_NUM LINE_CONTENT; do
    if [ -n "$LINE_NUM" ]; then
      # Escape para JSON
      ESCAPED=$(echo "$LINE_CONTENT" | sed 's/"/\\"/g' | sed 's/\\/\\\\/g')
      if [ "$FIRST" = true ]; then
        FIRST=false
      else
        RESULTS+=","
      fi
      RESULTS+="{\"line\":$LINE_NUM,\"pattern\":\"$PATTERN\",\"content\":\"$ESCAPED\"}"
    fi
  done < <(grep -nE "$PATTERN" "$FILE_PATH" 2>/dev/null | head -20)
done

RESULTS+="]"

cat <<EOF
{
  "status": "done",
  "file": "$FILE_PATH",
  "patterns": $RESULTS
}
EOF
