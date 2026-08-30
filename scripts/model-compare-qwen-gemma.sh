#!/bin/bash
# model-compare-qwen-gemma.sh — Comparativa rápida de rendimiento entre Qwen3.5 y Gemma 4
# Uso: ./model-compare-qwen-gemma.sh <prompt>
# Output: Benchmark de tokens generados, tiempo y calidad para ambos modelos.

set -euo pipefail

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 '<prompt>'" >&2
  exit 1
fi

PROMPT="$1"

echo "--- COMPARATIVA DE MODELOS: QWEN3.5 vs GEMMA4 ---"
echo "Prompt de prueba:"
echo "$PROMPT"
echo ""

# Variables para medir el rendimiento
QWEN_RESPONSE=""
GEMMA_RESPONSE=""
QWEN_TIME=0
GEMMA_TIME=0

# Ejecutar Qwen3.5 (local, reinstalado)
echo "🔍 Ejecutando Qwen3.5:9b-mlx..."
start=$(date +%s%N)
qwen35_response=$(ollama run qwen3.5:9b-mlx "$PROMPT" 2>&1 || true)
end=$(date +%s%N)
QWEN_TIME=$(( (end - start) / 1000000000 ))

echo ""
echo "⏱️ Tiempo Qwen3.5: ${QWEN_TIME}ms"
echo "📝 Respuesta Qwen3.5:"
echo "$qwen35_response" | head -c 500 # Mostrar solo los primeros 500 caracteres

# Ejecutar Gemma4:e4b-mlx (local)
echo ""
echo "🔍 Ejecutando Gemma4:e4b-mlx..."
start=$(date +%s%N)
gemma4_response=$(ollama run gemma4:e4b-mlx "$PROMPT" 2>&1 || true)
end=$(date +%s%N)
GEMMA_TIME=$(( (end - start) / 1000000000 ))

echo ""
echo "⏱️ Tiempo Gemma4:e4b-mlx: ${GEMMA_TIME}ms"
echo "📝 Respuesta Gemma4:"
echo "$gemma4_response" | head -c 500 # Mostrar solo los primeros 500 caracteres

# Resultado final
echo ""
echo "--- RESUMEN ---"
if [ $QWEN_TIME -lt $GEMMA_TIME ]; then
  echo "🏆 Ganador de velocidad: Qwen3.5 (${QWEN_TIME}ms vs ${GEMMA_TIME}ms)"
else
  echo "🏆 Ganador de velocidad: Gemma4:e4b-mlx (${GEMMA_TIME}ms vs ${QWEN_TIME}ms)"
fi

# Contar tokens aproximados (heuristic simple basándose en la longitud de la respuesta)
QWEN_TOKENS=$(( ($#PROMPT$'#'$qwen35_response$'#') / 4 )) # Heuristica simplificada
GEMMA_TOKENS=$(( ($#PROMPT$'#'$gemma4_response$'#') / 4 ))

echo "🔢 Respuestas aproximadas (tokens): Qwen3.5 ~${QWEN_TOKENS}, Gemma4:e4b-mlx ~${GEMMA_TOKENS}"
echo ""
