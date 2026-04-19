#!/usr/bin/env bash
set -euo pipefail
PREFIX=${1:-outputs/berth1/locked_replay_demo}
REPLAY=${2:-data/replay/berth1_locked_synthetic_replay.csv}
mkdir -p "$(dirname "$REPLAY")" "$(dirname "$PREFIX")"
HORIZON=${HORIZON:-80} SEEDS=${SEEDS:-4} SCENARIO=${SCENARIO:-mixed} \
  scripts/write_berth1_locked_synthetic_replay.sh "$REPLAY"
scripts/run_berth1_replay.sh "$REPLAY" "$PREFIX"
scripts/package_results.sh "$PREFIX" "${PREFIX}_results.zip"
echo "done: ${PREFIX}_results.zip"
