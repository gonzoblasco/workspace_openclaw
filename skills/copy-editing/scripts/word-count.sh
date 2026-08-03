#!/usr/bin/env bash
# word-count.sh — Word, character, sentence, and readability stats for a text file
# Usage: ./word-count.sh <file>

set -euo pipefail

FILE="${1:-}"

if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
  echo "Usage: word-count.sh <file>"
  exit 1
fi

TEXT=$(cat "$FILE")

# Word count
WORDS=$(echo "$TEXT" | wc -w | tr -d ' ')

# Character count (no spaces)
CHARS=$(echo "$TEXT" | tr -d '[:space:]' | wc -c | tr -d ' ')

# Character count (with spaces)
CHARS_SPACES=$(echo "$TEXT" | wc -c | tr -d ' ')

# Sentence count (rough: split on .!?)
SENTENCES=$(echo "$TEXT" | tr '\n' ' ' | grep -oE '[^.!?]+[.!?]' | wc -l | tr -d ' ')

# Paragraph count
PARAGRAPHS=$(grep -cE '^[[:space:]]*$' "$FILE" || true)
PARAGRAPHS=$((PARAGRAPHS + 1))

# Average words per sentence
if [ "$SENTENCES" -gt 0 ]; then
  AVG_WORDS=$(echo "scale=1; $WORDS / $SENTENCES" | bc)
else
  AVG_WORDS="N/A"
fi

# Reading time (avg 200 wpm)
READ_TIME=$(echo "scale=1; $WORDS / 200" | bc)

echo "📊 Text Stats: $FILE"
echo "===================="
echo "Words:        $WORDS"
echo "Characters:   $CHARS (no spaces) / $CHARS_SPACES (with spaces)"
echo "Sentences:    $SENTENCES"
echo "Paragraphs:   $PARAGRAPHS"
echo "Words/sentence: $AVG_WORDS"
echo "Reading time: ~${READ_TIME} min"
echo ""
echo "💡 Ideal: 14-20 words/sentence, 3-5 sentences/paragraph"
