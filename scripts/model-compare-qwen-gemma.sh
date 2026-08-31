#!/bin/bash
# model-compare-qwen-gemma.sh — Comparativa de rendimiento entre Qwen3.5 y Gemma 4
# Uso: ./model-compare-qwen-gemma.sh "<prompt>"
# Output: Benchmark de tiempo de generacion y longitud de respuesta para ambos modelos.
#
# Nota: usa `ollama run` con salida capturada. El tiempo mide la generacion completa
# (no solo la llamada), y los tokens se estiman por caracteres de la respuesta.

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

# --- Funcion: medir generacion de un modelo ---
# Devuelve: tiempo en segundos (stderr) y la respuesta (stdout)
run_model() {
  local model="$1"
  local start end elapsed
  start=$(date +%s)
  local out
  out=$(ollama run "$model" "$PROMPT" 2>/dev/null || true)
  end=$(date +%s)
  elapsed=$(( end - start ))
  echo "$out"
  echo "ELAPSED:$elapsed" >&2
}

echo "🔍 Ejecutando Qwen3.5:9b-mlx..."
QWEN_OUT=$(run_model "qwen3.5:9b-mlx" 2>/tmp/qwen_time.txt)
QWEN_TIME=$(grep -o 'ELAPSED:[0-9]*' /tmp/qwen_time.txt | cut -d: -f2)
QWEN_TIME=${QWEN_TIME:-0}

echo ""
echo "⏱️ Tiempo Qwen3.5: ${QWEN_TIME}s"
echo "📝 Respuesta Qwen3.5 (primeros 300 chars):"
echo "$QWEN_OUT" | head -c 300
echo ""

echo ""
echo "🔍 Ejecutando Gemma4:e4b-mlx..."
GEMMA_OUT=$(run_model "gemma4:e4b-mlx" 2>/tmp/gemma_time.txt)
GEMMA_TIME=$(grep -o 'ELAPSED:[0-9]*' /tmp/gemma_time.txt | cut -d: -f2)
GEMMA_TIME=${GEMMA_TIME:-0}

echo ""
echo "⏱️ Tiempo Gemma4:e4b-mlx: ${GEMMA_TIME}s"
echo "📝 Respuesta Gemma4 (primeros 300 chars):"
echo "$GEMMA_OUT" | head -c 300
echo ""

# --- Resumen ---
echo ""
echo "--- RESUMEN ---"
if [ "$QWEN_TIME" -lt "$GEMMA_TIME" ]; then
  echo "🏆 Ganador de velocidad: Qwen3.5 (${QWEN_TIME}s vs ${GEMMA_TIME}s)"
else
  echo "🏆 Ganador de velocidad: Gemma4:e4b-mlx (${GEMMA_TIME}s vs ${QWEN_TIME}s)"
fi

# Longitud de respuesta (caracteres) como proxy de tokens
QWEN_CHARS=${#QWEN_OUT}
GEMMA_CHARS=${#GEMMA_OUT}
echo "📏 Longitud de respuesta: Qwen3.5=${QWEN_CHARS} chars, Gemma4=${GEMMA_CHARS} chars"
echo ""
