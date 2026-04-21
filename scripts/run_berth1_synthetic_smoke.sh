#!/usr/bin/env bash
set -euo pipefail
PREFIX=${1:-outputs/berth1/synthetic_smoke}
mkdir -p "$(dirname "$PREFIX")"
${PYTHON:-python} -m os_cmasp.berth1_conflict --mode preflight --horizon "${HORIZON:-80}" --seeds "${SEEDS:-4}" --scenario "${SCENARIO:-mixed}" --manifest "${PREFIX}.preflight_manifest.json" --out-prefix "$PREFIX"
${PYTHON:-python} -m os_cmasp.berth1_conflict --mode run --allow-synthetic-results --horizon "${HORIZON:-80}" --seeds "${SEEDS:-4}" --scenario "${SCENARIO:-mixed}" --manifest "${PREFIX}.manifest.json" --out-prefix "$PREFIX"
${PYTHON:-python} scripts/summarize_berth1_results.py "$PREFIX"
