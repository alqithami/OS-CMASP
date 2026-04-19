#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 2 ]]; then
  echo "Usage: scripts/package_results.sh <out_prefix> <zip_path>" >&2
  exit 2
fi
PFX="$1"
ZIP="$2"
python - <<PY
from pathlib import Path
import zipfile
pfx=Path('$PFX')
zip_path=Path('$ZIP')
files=[]
for suffix in ['.csv','_summary.csv','_paired.csv','_diagnostics.json','.manifest.json','.preflight_manifest.json','_report.md','_regret_bar.png']:
    p=Path(str(pfx)+suffix)
    if p.exists(): files.append(p)
zip_path.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for f in files: z.write(f, f.name)
print(f'wrote {zip_path} with {len(files)} files')
PY
