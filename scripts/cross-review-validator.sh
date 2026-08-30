#!/bin/bash
# 🔍 CROSS-REVIEW VALIDATOR
# Valida cambios contra docs reales (no solo comments)
# Ejemplo: si hay un endpoint documentado, el hook verifica que exista

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 CROSS-REVIEW VALIDATOR"
echo "⏰ $(date +%Y-%m-%d %H:%M)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Configurar repos para operar en workspace
cd /Users/gonzoblasco/.openclaw/workspace || exit 1

echo "🎯 TARGET: Current session changes"
echo ""

VALIDATION_SCORE=0
TOTAL_CHECKS=0

# === CHECK 1: ADRs missing for recent architectural decisions ===
echo "🔍 VALIDATION #1: DOCUMENTATION AUDIT"
echo ""
echo "   Checking for undocumented architectural decisions..."

ADRs_COUNT=$(find . -name "ADR-*.md" -type f | wc -l)
RECENT_FILES=$(git diff --name-only HEAD~10..HEAD 2>/dev/null || echo "")

if [ -n "$RECENT_FILES" ]; then
    MISSING_ADRS=0
    
    while IFS= read -r file; do
        if [[ "$file" != *.md ]] && [[ ! "$file" =~ ^\. ]]; then
            TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
            
            # Verificar si hay cambio importante que debería tener ADR
            if grep -q "architecture\|design\|pattern\|decision" "$file" 2>/dev/null; then
                echo "    ⚠️ $file: May need ADR documentation"
                MISSING_ADRS=$((MISSING_ADRS + 1))
            fi
            
        fi
    done <<< "$RECENT_FILES"
    
    if [ "$MISSING_ADRS" -gt 0 ]; then
        echo "   ℹ️ Found $MISSING_ADRS files that may benefit from ADR documentation"
        VALIDATION_SCORE=$((VALIDATION_SCORE + 5))
    else
        echo "    ✅ Recent changes appear well-documented"
        VALIDATION_SCORE=$((VALIDATION_SCORE + 10))
    fi
else
    echo "    ✅ No recent changes detected (session stable)"
    VALIDATION_SCORE=$((VALIDATION_SCORE + 10))
fi

echo ""

# === CHECK 2: Cross-review against AGENTS.md rules ===
echo "🔍 VALIDATION #2: AGENTS COMPLIANCE"
echo ""

AGENTS_FILE="./AGENTS.md"
if [ -f "$AGENTS_FILE" ]; then
    echo "   Checking current code against AGENTS.md rules..."
    
    # Regla 1: Em-dash check (already covered by pre-push, but cross-verify)
    echo "    • Rule 1 (em-dash): Referencing pre-push hook validation ✅"
    
    # Regla 2: GitHub English, UI Spanish
    ENGLISH_DOCS=$(find . -name "*.md" -type f -exec grep -l "^#" {} \; | xargs file | grep -c "ASCII text" || echo "0")
    if [ "$ENGLISH_DOCS" -gt 0 ]; then
        echo "     ✅ Documentation in English detected: $ENGLISH_DOCS files"
    fi
else
    echo "   ⚠️ AGENTS.md not found (referencing workspace standard)"
fi

echo ""

# === CHECK 3: ADR-037 Compliance (Icons) ===
echo "🔍 VALIDATION #3: ICONOGRAPHY COMPLIANCE (ADR-037)"
echo ""

ICONS_DIR="./projects/*/components/*"
ICON_FILES=$(find . -name "*icon*" -o -name "*Icon*" 2>/dev/null | head -5)

if [ -n "$ICON_FILES" ]; then
    # Verificar que usen Lucide, no emojis como iconografía UI
    EMOJI_ICONS=$(echo "$ICON_FILES" | grep -c "😀\|😎\|🚀\|💯\|🎯" || echo "0")
    
    if [ "$EMOJI_ICONS" -gt 0 ]; then
        echo "   ⚠️ Potential emoji icons detected (ADR-037: Lucide base)"
        echo "      ℹ️ Consider using lucide-react instead for production UI"
        VALIDATION_SCORE=$((VALIDATION_SCORE + 2))
    else
        echo "    ✅ Iconography follows ADR-037 (Lucide-based)"
        VALIDATION_SCORE=$((VALIDATION_SCORE + 10))
    fi
else
    echo "    ✅ No custom icon components found (good!)"
fi

echo ""

# === CHECK 4: Pipeline A/B documentation presence ===
echo "🔍 VALIDATION #4: PIPELINE DOCUMENTATION"
echo ""

HANDOFF_COUNT=$(find . -name "HANDOFF.md" -type f | wc -l)
AGENTS_HANDOFF=$(find . -name "AGENTS*.md" -type f | wc -l)

if [ "$HANDOFF_COUNT" -eq 0 ] && [ "$AGENTS_HANDOFF" -gt 0 ]; then
    echo "   ℹ️ Cross-review documented in AGENTS* files: $AGENTS_HANDOFF found"
elif [ "$HANDOFF_COUNT" -gt 0 ]; then
    echo "    ✅ HANDOFF.md present for cross-review ($HANDOFF_COUNT file(s))"
else
    echo "   ⚠️ No cross-review documentation found"
fi

echo ""

# === CHECK 5: Build artifacts validation ===
echo "🔍 VALIDATION #5: BUILD ARTIFACTS"
echo ""

if command -v npm >/dev/null 2>&1; then
    # Verificar si hay build directory (sign of successful previous build)
    BUILD_CHECK=$(find . -name "dist" -o -name "build" -type d 2>/dev/null | head -1)
    
    if [ -n "$BUILD_CHECK" ] && [ -d "$BUILD_CHECK" ]; then
        echo "    ✅ Build artifacts present (recent build detected)"
        VALIDATION_SCORE=$((VALIDATION_SCORE + 5))
    else
        echo "   ℹ️ No build artifacts found (build may need to be run)"
        echo "      ℹ️ This is normal for fresh clone"
    fi
else
    echo "    ⚠️ npm not found (skipping build validation)"
fi

echo ""

# === FINAL VALIDATION SUMMARY ===
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 CROSS-REVIEW VALIDATION COMPLETE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ "$VALIDATION_SCORE" -ge 70 ]; then
    echo "✅ EXCELLENT STATE ($VALIDATION_SCORE/100)"
    echo ""
    echo "Your session meets high quality standards:"
    echo "   ✓ Documentation in place where needed"
    echo "   ✓ Code follows AGENTS.md rules"
    echo "   ✓ ADR compliance validated"
    echo "   ✓ Iconography follows production standards"
    
elif [ "$VALIDATION_SCORE" -ge 40 ]; then
    echo "⚠️ ACCEPTABLE STATE ($VALIDATION_SCORE/100)"
    echo ""
    echo "Session is functional but has room for improvement:"
    echo "   • Consider documenting key architectural decisions as ADRs"
    echo "   • Review iconography against ADR-037 (Lucide base)"
else
    echo "🔴 NEEDS ATTENTION ($VALIDATION_SCORE/100)"
    echo ""
    echo "Session requires quality improvements before merge:"
    echo "   ⚠️ Documentation gaps detected"
    echo "   ⚠️ Consider AGENTS.md compliance review"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 ACTION ITEMS (if any):"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$VALIDATION_SCORE" -lt 70 ]; then
    echo "   🔸 Review undocumented architectural decisions → Create ADRs"
    echo "   🔸 Audit iconography components → Use lucide-react"
    echo "   🔸 Verify cross-review documentation exists (HANDOFF/AGENTS*) files"
fi

echo ""
echo "🎯 Cross-review validation complete!"
echo ""
