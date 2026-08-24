#!/bin/bash
# safe-fetch.sh - URL pre-flight security check before opening a URL.
#
# Ported concept from the PreClick plugin (ClawHub), but 100% LOCAL and FREE:
# no URL is sent to any third-party service. Verifies scheme, known-bad
# domains, typosquatting of domains we use, and prompt-injection payloads.
#
# Usage:
#   safe-fetch.sh <url>            -> prints verdict (ALLOW/DENY/CAUTION) + reason
#   safe-fetch.sh --verbose <url>  -> detailed checks
#
# Exit codes: 0 = ALLOW, 1 = DENY, 2 = CAUTION, 3 = usage error.

set -uo pipefail

# --- Config ---
# Trusted domains we frequently use (for typosquatting detection).
TRUSTED_DOMAINS="github.com githubusercontent.com supabase.co supabase.com vercel.app vercel.com netlify.app netlify.com npmjs.com stackoverflow.com developer.mozilla.org docs.openclaw.ai openclaw.ai google.com youtube.com"

# Known typosquat variants of trusted domains (curated; extend as discovered).
TYPO_VARIANTS="githhub.com githuub.com git-hub.com gitgub.com githuh.com supabase.cm supaabase.com vercelapp.com vercel.co netlifyapp.com nmpjs.com stakoverflow.com"

# Known-bad: blocklist of phishing/malware domains (curated, extend over time).
BLOCKLIST=""

VERBOSE=0

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 [--verbose] <url>" >&2
  exit 3
fi

if [ "$1" = "--verbose" ]; then VERBOSE=1; shift; fi
URL="$1"

FAIL_REASONS=()
CAUTION_REASONS=()

# --- 1. Scheme check ---
if [[ ! "$URL" =~ ^https:// ]]; then
  if [[ "$URL" =~ ^http:// ]]; then
    FAIL_REASONS+=("esquema http (no cifrado) - usar https")
  else
    FAIL_REASONS+=("esquema invalido (solo https)")
  fi
fi

# --- 2. Extract host ---
HOST_PORT="${URL#https://}"
HOST_PORT="${HOST_PORT%%/*}"
HOST_PORT="${HOST_PORT%%\?*}"
HOST_PORT="${HOST_PORT%%\#*}"
HOST="${HOST_PORT%%:*}"
HOST_LOWER=$(echo "$HOST" | tr '[:upper:]' '[:lower:]')

# --- 3. Basic host sanity ---
if [ -z "$HOST" ]; then
  FAIL_REASONS+=("host vacio")
fi
if [[ "$HOST" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  CAUTION_REASONS+=("host es IP literal (puede ser dev local o redir)")
fi
if [[ "$HOST_LOWER" =~ ^(localhost|127\.0\.0\.1|0\.0\.0\.0)$ ]]; then
  CAUTION_REASONS+=("host local/privado (solo si es intencional)")
fi

# --- 4. Blocklist ---
for bad in $BLOCKLIST; do
  if [ "$HOST_LOWER" = "$bad" ] || [[ "$HOST_LOWER" == *".$bad" ]]; then
    FAIL_REASONS+=("dominio en blocklist: $bad")
  fi
done

# --- 5. Typosquatting detection ---
# 5a. Direct hit on known typo variant -> DENY
for v in $TYPO_VARIANTS; do
  if [ "$HOST_LOWER" = "$v" ] || [[ "$HOST_LOWER" == *".$v" ]]; then
    FAIL_REASONS+=("posible typosquatting: '$HOST' es una variante conocida de un dominio confiable")
  fi
done

# 5b. Near-similar check: host root vs trusted base, close length + high overlap.
for t in $TRUSTED_DOMAINS; do
  t_lower="$t"   # ya estan en minuscula
  # exact trusted domain -> fine, skip
  if [ "$HOST_LOWER" = "$t_lower" ]; then
    continue
  fi
  # subdomain of trusted (e.g. api.github.com) -> fine
  if [[ "$HOST_LOWER" == *".$t_lower" ]]; then
    continue
  fi
  base="${t_lower%%.*}"   # e.g. github
  host_root="${HOST_LOWER%%.*}"
  # false-positive list for legit OSS domains that look similar
  case "$HOST_LOWER" in
    *githubusercontent.com|*github.io|*githubapp.com) continue;;
  esac
  # if host root matches exactly a trusted base, it's a legit same-registrant TLD
  # (e.g. supabase.co vs supabase.com) - only if that TLD is itself trusted
  if [ "$host_root" = "$base" ]; then
    continue
  fi
  if [ "${#host_root}" -ge 4 ] && [ "${#base}" -ge 4 ]; then
    diff_len=$(( ${#host_root} > ${#base} ? ${#host_root} - ${#base} : ${#base} - ${#host_root} ))
    if [ "$diff_len" -le 1 ]; then
      min_len=$(( ${#host_root} < ${#base} ? ${#host_root} : ${#base} ))
      same=0
      for ((i=0; i<min_len; i++)); do
        if [ "${host_root:i:1}" = "${base:i:1}" ]; then ((same++)); fi
      done
      if [ "$same" -ge $((min_len - 1)) ] && [ "$same" -ge 4 ]; then
        FAIL_REASONS+=("posible typosquatting: '$HOST' se parece a '$t' (near-match)")
        break
      fi
    fi
  fi
done

# --- 6. Prompt-injection payload check (path + query) ---
PATH_QUERY="${URL#*://}"
PATH_QUERY="${PATH_QUERY#*/}"   # strip host, keep /path?query
LOWER_PQ=$(echo "$PATH_QUERY" | tr '[:upper:]' '[:lower:]')
for p in 'ignore previous' 'ignore prior' 'system prompt' 'you are now' 'jailbreak' 'reveal' 'instructions' 'do not follow' 'act as'; do
  if [[ "$LOWER_PQ" == *"$p"* ]]; then
    CAUTION_REASONS+=("path/query contiene patron sospechoso de injection: '$p'")
  fi
done

# --- Output ---
if [ "$VERBOSE" = "1" ]; then
  echo "URL: $URL"
  echo "Host: $HOST"
fi

if [ "${#FAIL_REASONS[@]}" -gt 0 ]; then
  echo "DENY - $URL"
  for r in "${FAIL_REASONS[@]}"; do echo "  - $r"; done
  exit 1
fi

if [ "${#CAUTION_REASONS[@]}" -gt 0 ]; then
  echo "CAUTION - $URL (ALLOW con cuidado)"
  for r in "${CAUTION_REASONS[@]}"; do echo "  - $r"; done
  exit 2
fi

echo "ALLOW - $URL"
exit 0
