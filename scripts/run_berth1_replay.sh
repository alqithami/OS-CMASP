#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 2 ]]; then
  echo "Usage: scripts/run_berth1_replay.sh <replay_csv> <out_prefix>" >&2
  exit 2
fi
REPLAY_CSV="$1"
OUT_PREFIX="$2"
mkdir -p "$(dirname "$OUT_PREFIX")"
python -m os_cmasp.berth1_conflict \
  --mode preflight \
  --replay-csv "$REPLAY_CSV" \
  --manifest "${OUT_PREFIX}.preflight_manifest.json"
python -m os_cmasp.berth1_conflict \
  --mode run \
  --replay-csv "$REPLAY_CSV" \
  --out-prefix "$OUT_PREFIX" \
  --manifest "${OUT_PREFIX}.manifest.json"
python scripts/summarize_berth1_results.py "$OUT_PREFIX"
