#!/usr/bin/env bash
set -euo pipefail
PREFIX=${1:-outputs/berth1/synthetic_smoke}
mkdir -p "$(dirname "$PREFIX")"
${PYTHON:-python} -m os_cmasp.berth1_conflict --mode preflight --scenario mixed --horizon 80 --seeds 4 --manifest "${PREFIX}.preflight_manifest.json" --out-prefix "$PREFIX"
${PYTHON:-python} -m os_cmasp.berth1_conflict --mode run --scenario mixed --horizon 80 --seeds 4 --allow-synthetic-results --manifest "${PREFIX}.manifest.json" --out-prefix "$PREFIX"
${PYTHON:-python} scripts/summarize_berth1_results.py "$PREFIX"
