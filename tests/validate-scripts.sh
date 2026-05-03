#!/usr/bin/env bash
# tests/validate-scripts.sh
set -euo pipefail
SCRIPTS_DIR="$(cd "$(dirname "$0")/../scripts" && pwd)"
PASS=0; FAIL=0
for f in "$SCRIPTS_DIR"/*.py; do
  if python3 -m py_compile "$f" 2>/dev/null; then
    echo "  v $(basename "$f")"; PASS=$((PASS+1))
  else
    echo "  x $(basename "$f") -- syntax error"; FAIL=$((FAIL+1))
  fi
done
echo; echo "Scripts: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
