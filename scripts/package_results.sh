#!/usr/bin/env bash
set -euo pipefail
if [ $# -lt 2 ]; then
  echo "usage: $0 output_prefix result_zip" >&2
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
missing=0
for f in "${FILES[@]}"; do
  if [ ! -f "$f" ]; then
    echo "Missing expected result file: $f" >&2
    missing=1
  fi
done
if [ "$missing" -ne 0 ]; then
  echo "Refusing to create a partial or empty result zip." >&2
  exit 1
fi
mkdir -p "$(dirname "$ZIP")"
rm -f "$ZIP"
${PYTHON:-python} - "$ZIP" "${FILES[@]}" <<'PY'
import sys
from zipfile import ZipFile, ZIP_DEFLATED
zip_path = sys.argv[1]
files = sys.argv[2:]
with ZipFile(zip_path, 'w', ZIP_DEFLATED) as z:
    for f in files:
        z.write(f)
print(f"wrote {zip_path} with {len(files)} files")
PY
