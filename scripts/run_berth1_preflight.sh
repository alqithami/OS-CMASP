#!/usr/bin/env bash
set -euo pipefail
OUTDIR=${1:-artifacts/preflight}
mkdir -p "$OUTDIR"
${PYTHON:-python} -m os_cmasp.berth1_conflict \
  --mode preflight \
  --horizon "${HORIZON:-320}" \
  --seeds "${SEEDS:-8}" \
  --scenario "${SCENARIO:-mixed}" \
  --manifest "$OUTDIR/berth1_preflight_manifest.json"
