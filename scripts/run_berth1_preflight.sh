#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-artifacts/preflight}"
mkdir -p "$OUT_DIR"

PYTHON_BIN="${PYTHON_BIN:-python}"
$PYTHON_BIN -m os_cmasp.berth1_conflict \
  --mode preflight \
  --scenario mixed \
  --horizon 320 \
  --seeds 8 \
  --manifest "$OUT_DIR/berth1_preflight_manifest.json"
