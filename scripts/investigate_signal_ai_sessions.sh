#!/bin/bash
# Investigation script for Signal AI sessions in crypto-ai project
# This script helps understand the structure before cleanup

set -euo pipefail

PROJECT_DIR="projects/-Users-morriz-Workspace-InstruktAI-crypto-ai"
SEARCH_PATTERN="system: You are Signal AI"
RESULTS_FILE="/tmp/signal_ai_investigation_$(date +%Y%m%d_%H%M%S).txt"

echo "Signal AI Session Investigation" > "$RESULTS_FILE"
echo "================================" >> "$RESULTS_FILE"
echo "Date: $(date)" >> "$RESULTS_FILE"
echo "" >> "$RESULTS_FILE"

# Count files containing the pattern
echo "Counting files with pattern..." >&2
FILE_COUNT=$(grep -l "$SEARCH_PATTERN" "$PROJECT_DIR"/*.jsonl 2>/dev/null | wc -l | tr -d ' ')
echo "Files containing 'system: You are Signal AI': $FILE_COUNT" >> "$RESULTS_FILE"

# Get total file count in directory
TOTAL_FILES=$(ls "$PROJECT_DIR"/*.jsonl 2>/dev/null | wc -l | tr -d ' ')
echo "Total .jsonl files in directory: $TOTAL_FILES" >> "$RESULTS_FILE"
echo "" >> "$RESULTS_FILE"

# Calculate sizes
echo "Calculating sizes..." >&2
TOTAL_SIZE=$(du -sh "$PROJECT_DIR" | awk '{print $1}')
echo "Total directory size: $TOTAL_SIZE" >> "$RESULTS_FILE"

# Sample a few files to understand structure
echo "" >> "$RESULTS_FILE"
echo "Sample file analysis:" >> "$RESULTS_FILE"
echo "--------------------" >> "$RESULTS_FILE"

SAMPLE_FILE=$(grep -l "$SEARCH_PATTERN" "$PROJECT_DIR"/*.jsonl 2>/dev/null | head -1)
if [ -n "$SAMPLE_FILE" ]; then
    echo "Sample file: $(basename "$SAMPLE_FILE")" >> "$RESULTS_FILE"
    echo "First occurrence of pattern:" >> "$RESULTS_FILE"
    grep "$SEARCH_PATTERN" "$SAMPLE_FILE" | head -1 | jq -r '.message.content' 2>/dev/null | head -5 >> "$RESULTS_FILE" || echo "(unable to parse)" >> "$RESULTS_FILE"
fi

echo "" >> "$RESULTS_FILE"
echo "Files to be deleted:" >> "$RESULTS_FILE"
echo "--------------------" >> "$RESULTS_FILE"
grep -l "$SEARCH_PATTERN" "$PROJECT_DIR"/*.jsonl 2>/dev/null | while read -r file; do
    SIZE=$(du -h "$file" | awk '{print $1}')
    echo "  - $(basename "$file") ($SIZE)" >> "$RESULTS_FILE"
done

echo "" >> "$RESULTS_FILE"
echo "Investigation complete!" >> "$RESULTS_FILE"
echo "Results saved to: $RESULTS_FILE" >> "$RESULTS_FILE"

cat "$RESULTS_FILE"
echo ""
echo "Full results saved to: $RESULTS_FILE"
