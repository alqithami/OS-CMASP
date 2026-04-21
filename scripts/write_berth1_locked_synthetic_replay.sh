#!/usr/bin/env bash
set -euo pipefail
OUT=${1:-data/replay/berth1_locked_synthetic_replay.csv}
mkdir -p "$(dirname "$OUT")"
${PYTHON:-python} -m os_cmasp.berth1_replay_adapter \
  --mode locked-synthetic \
  --out "$OUT" \
  --report "${OUT%.csv}.adapter_report.json" \
  --scenario "${SCENARIO:-mixed}" \
  --horizon "${HORIZON:-80}" \
  --seeds "${SEEDS:-4}" \
  --p-all-clear "${P_ALL_CLEAR:-0.5}"
echo "wrote locked synthetic replay: $OUT"
