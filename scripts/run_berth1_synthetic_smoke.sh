#!/usr/bin/env bash
set -euo pipefail
PYTHON_BIN="${PYTHON_BIN:-python}"

OUT_PREFIX="${1:-outputs/berth1/synthetic_smoke}"
mkdir -p "$(dirname "$OUT_PREFIX")"

$PYTHON_BIN -m os_cmasp.berth1_conflict \
  --mode preflight \
  --scenario mixed \
  --horizon 80 \
  --seeds 4 \
  --manifest "$OUT_PREFIX.preflight_manifest.json"

$PYTHON_BIN -m os_cmasp.berth1_conflict \
  --mode run \
  --allow-synthetic-results \
  --scenario mixed \
  --horizon 80 \
  --seeds 4 \
  --out-prefix "$OUT_PREFIX" \
  --manifest "$OUT_PREFIX.manifest.json"

$PYTHON_BIN scripts/summarize_berth1_results.py "$OUT_PREFIX"
