#!/usr/bin/env bash
set -euo pipefail
if [ $# -lt 2 ]; then
  echo "usage: $0 output_prefix output_zip" >&2
  exit 2
fi
PREFIX=$1
ZIP=$2
FILES=(
  "${PREFIX}.csv"
  "${PREFIX}_summary.csv"
  "${PREFIX}_paired.csv"
  "${PREFIX}_diagnostics.json"
  "${PREFIX}.manifest.json"
  "${PREFIX}.preflight_manifest.json"
  "${PREFIX}_report.md"
)
MISSING=()
for f in "${FILES[@]}"; do
  if [ ! -f "$f" ]; then
    MISSING+=("$f")
  fi
done
if [ ${#MISSING[@]} -gt 0 ]; then
  echo "Refusing to create results zip because required outputs are missing:" >&2
  printf '  %s\n' "${MISSING[@]}" >&2
  exit 1
fi
mkdir -p "$(dirname "$ZIP")"
rm -f "$ZIP"
zip -q "$ZIP" "${FILES[@]}"
echo "wrote $ZIP with ${#FILES[@]} files"
