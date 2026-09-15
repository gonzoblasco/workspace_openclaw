#!/bin/bash
# 🗂️ DAILY AUTO ARCHIVER
# Move memory/YYYY.md -> archive/ cuando pasa 7 días
# No más acumulación de dailies viejas

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 DAILY AUTO ARCHIVER"
echo "⏰ $(date +%Y-%m-%d %H:%M)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Configurar repos para operar en workspace
cd /Users/gonzoblasco/.openclaw/workspace/memory || exit 1

echo "🎯 TARGET: Archive dailies older than 7 days"
echo ""

SEVEN_DAYS_AGO=$(date -d "7 days ago" '+%Y-%m-%d')
CURRENT_DATE=$(date '+%Y-%m-%d')

echo "Reference dates:"
echo "    • Current date:      $CURRENT_DATE"
echo "    • 7 days ago:        $SEVEN_DAYS_AGO"
echo ""

ARCHIVED_COUNT=0
STILL_RECENT=0
SKIPPED_COUNT=0

echo "🔍 SCANNING DAILY FILES..."
echo ""

# Buscar todos los archivos daily
for daily in $(ls memory/YYYY-MM-DD.md 2>/dev/null | sort); do
    if [ -z "$daily" ]; then
        break
    fi
    
    FILE_PATH="memory/$daily"
    
    if [ ! -f "$FILE_PATH" ]; then
        continue
    fi
    
     # Obtener fecha del archivo
    FILE_DATE=$(echo "$daily" | sed 's/memory\///')
    
    # Verificar si está en el rango de 7 días
    if [[ "$FILE_DATE" < "$SEVEN_DAYS_AGO" ]]; then
        echo "📦 ARCHIVING: $daily (older than 7 days)"
        
        # Crear directorio archive si no existe
        mkdir -p memory/archive
        
        # Mover archivo a archive
        mv "$FILE_PATH" "memory/archive/"
        
        ARCHIVED_COUNT=$((ARCHIVED_COUNT + 1))
    else
        echo "✅ SKIP: $daily (still recent)"
        STILL_RECENT=$((STILL_RECENT + 1))
    fi
done

echo ""

# === SUMMARY ===
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 ARCHIVE SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ "$ARCHIVED_COUNT" -gt 0 ]; then
    echo "✅ SUCCESSFULLY ARCHIVED:"
    echo "   $ARCHIVED_COUNT day(s) moved to archive/ directory"
    echo ""
    
     # Commit changes if we archived something
    if git status --porcelain | grep -q "^M"; then
        echo "📝 Git: Archive operation modified workspace"
        echo "   Suggested next step:"
        echo "     git add memory/archive/.* daily*.md\$ 2>/dev/null || true"
        echo "     git commit -m 'chore(memory): archive dailies older than 7 days'"
    fi
else
    echo "✅ ALL DAILIES ARE RECENT!"
    echo "   $STILL_RECENT day(s) kept (within 7-day window)"
fi

echo ""
echo "📊 Current state:"
echo "    • Archived:      $ARCHIVED_COUNT file(s)"
echo "    • Still recent:  $STILL_RECENT file(s)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Daily archive complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
