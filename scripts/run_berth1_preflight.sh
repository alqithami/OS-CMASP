#!/usr/bin/env bash
set -euo pipefail
mkdir -p artifacts/preflight
python -m os_cmasp.berth1_conflict \
  --mode preflight \
  --scenario mixed \
  --horizon 40 \
  --seeds 8 \
  --manifest artifacts/preflight/berth1_preflight_manifest.json
