#!/usr/bin/env bash
set -euo pipefail
if [ $# -lt 1 ]; then
  echo "usage: $0 replay.csv [output_prefix]" >&2
  echo "For a no-manual demo, run: scripts/run_berth1_locked_replay_demo.sh outputs/berth1/locked_replay_demo" >&2
  exit 2
fi
REPLAY_CSV="$1"
OUT_PREFIX="${2:-outputs/berth1/twin_replay_v1}"
scripts/run_berth1_replay.sh "$REPLAY_CSV" "$OUT_PREFIX"
