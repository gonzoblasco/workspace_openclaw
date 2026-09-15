#!/bin/bash
# 🔍 HIDEAK - Heartbeat & Incident Detection Automation & Kickstart
# Automatiza el ritual de inicio de sesión con check proactivo de PRs pendientes
# Ahorra ~15 min por session

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 HIDEAK - Startup Check Automated"
echo "⏰ $(date +%Y-%m-%d %H:%M)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# === CHECK 1: PRs pendientes (GitHub API) ===
echo "📋 CHECKING FOR PENDING PRs..."
echo ""

GITHUB_TOKEN="${GITHUB_TOKEN:-}"
USER="${GITHUB_USER:-gonzoblasco}"

if [ -n "$GITHUB_TOKEN" ]; then
    PRS=$(gh api /repos/gonzoblasco/workspace_openclaw/pulls?state=open \
        -H "Authorization: token $GITHUB_TOKEN" 2>/dev/null | jq -c '.[] | {number, title, user, base}"' || echo "[]")
else
    # Fallback si no hay token: check git remote status
    PRS="⚠️ GitHub API token no proporcionado (Opcional para este check)"
fi

echo "📊 Pending PRs:"
if [ "$PRS" == "[]" ] || [ -z "$PRS" ]; then
    echo "   ✅ Ningún PR pendiente detectado"
else
    echo "$PRS" | while read -r pr; do
        TITLE=$(echo "$pr" | jq -r '.title')
        NUM=$(echo "$pr" | jq -r '.number')
        USER=$(echo "$pr" | jq -r '.user.login')
        echo "   🔢 PR #$NUM: $TITLE (@$USER)"
    done
fi

echo ""

# === CHECK 2: Status report reciente ===
echo "📊 CHECKING FOR LATEST STATUS REPORT..."
LATEST_STATUS=$(find /Users/gonzoblasco/.openclaw/workspace/projects -maxdepth 1 -name "STATUS_REPORT_*.md" -type f | sort | tail -1)

if [ -n "$LATEST_STATUS" ] && [ -f "$LATEST_STATUS" ]; then
    STATUS_DATE=$(basename "$LATEST_STATUS")
    STATUS_CONTENT=$(head -20 "$LATEST_STATUS")
    echo "   📄 Último status: $STATUS_DATE"
    echo "   ────────────────────────────────────────────────"
    echo "$STATUS_CONTENT"
else
    echo "   ⚠️ No se encontraron reports de status recientes"
fi

echo ""

# === CHECK 3: System health check ===
echo "🔍 SYSTEM HEALTH CHECK..."
echo ""

# Workspace git health
GIT_STATUS=$(git -C /Users/gonzoblasco/.openclaw/workspace status --porcelain)
UNSTAGED=$(echo "$GIT_STATUS" | grep -c '^?' || echo "0")
UNCOMMITTED=$(echo "$GIT_STATUS" | grep -c '^ ' || echo "0")

echo "   • Workspace status:"
if [ "$UNSTAGED" -eq 0 ] && [ "$UNCOMMITTED" -eq 0 ]; then
    echo "      ✅ Clean workspace (nothing uncommitted)"
else
    echo "      ⚠️ $UNSTAGED unstaged / $UNCOMMITTED staged changes detected"
fi

echo ""

# === CHECK 4: Recent activity pattern ===
echo "📊 RECENT ACTIVITY PATTERN (last 7 days)..."
RECENT_COMMITS=$(git -C /Users/gonzoblasco/.openclaw/workspace log --since="7 days ago" --pretty=format:"%h %s [%ad]" --date='short' | head -10)

if [ -n "$RECENT_COMMITS" ]; then
    echo "   Recent commits:"
    echo "$RECENT_COMMITS"
else
    echo "   • No actividad en los últimos 7 días (esperando nuevos trabajos)"
fi

echo ""

# === SUMMARY & SUGGESTIONS ===
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 HIDEAK SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ "$UNSTAGED" -eq 0 ] && [ "$UNCOMMITTED" -eq 0 ]; then
    echo "✅ Workspace limpio y listo para trabajar"
else
    echo "⚠️ Hay cambios pendientes de commit en el workspace"
fi

echo ""
echo "🎯 SUGERENCIAS:"
echo ""
echo "   1. Review pending PRs antes de empezar sesión nueva"
echo "   2. Verificar status report actualizado"
echo "   3. Confirmar que workspace está limpio (si hay changes, commitarlos)"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ HIDEAK CHECK COMPLETE - System ready!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
