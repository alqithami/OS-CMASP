#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: scripts/package_results.sh OUT_PREFIX ZIP_PATH" >&2
  exit 2
fi

OUT_PREFIX="$1"
ZIP_PATH="$2"
REQUIRED=(
  "$OUT_PREFIX.csv"
  "$OUT_PREFIX"_summary.csv
  "$OUT_PREFIX"_paired.csv
  "$OUT_PREFIX"_diagnostics.json
  "$OUT_PREFIX.manifest.json"
  "$OUT_PREFIX.preflight_manifest.json"
  "$OUT_PREFIX"_report.md
)

MISSING=()
for f in "${REQUIRED[@]}"; do
  [[ -f "$f" ]] || MISSING+=("$f")
done
if (( ${#MISSING[@]} > 0 )); then
  echo "ERROR: refusing to create an empty/incomplete results zip. Missing:" >&2
  printf '  %s\n' "${MISSING[@]}" >&2
  exit 2
fi

mkdir -p "$(dirname "$ZIP_PATH")"
rm -f "$ZIP_PATH"
zip -q "$ZIP_PATH" "${REQUIRED[@]}"
echo "wrote $ZIP_PATH with ${#REQUIRED[@]} files"
