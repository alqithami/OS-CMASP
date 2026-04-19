#!/usr/bin/env bash
set -euo pipefail
OUT=${1:-data/replay/berth1_locked_synthetic_replay.csv}
HORIZON=${HORIZON:-80}
SEEDS=${SEEDS:-4}
SCENARIO=${SCENARIO:-mixed}
mkdir -p "$(dirname "$OUT")"
${PYTHON:-python} -m os_cmasp.berth1_replay_adapter \
  --mode locked-synthetic \
  --out "$OUT" \
  --horizon "$HORIZON" \
  --seeds "$SEEDS" \
  --scenario "$SCENARIO" \
  --report "${OUT%.csv}.adapter_report.json"
echo "locked synthetic replay written to: $OUT"
echo "adapter report written to: ${OUT%.csv}.adapter_report.json"
