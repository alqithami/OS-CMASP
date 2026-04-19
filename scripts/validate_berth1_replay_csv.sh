#!/usr/bin/env bash
set -euo pipefail
if [ $# -lt 1 ]; then
  echo "usage: $0 path/to/replay.csv [normalized_out.csv]" >&2
  exit 2
fi
IN=$1
OUT=${2:-${IN%.csv}.normalized.csv}
if [ ! -f "$IN" ]; then
  echo "Missing replay CSV: $IN" >&2
  echo "To generate a locked synthetic replay for pipeline checks, run:" >&2
  echo "  scripts/write_berth1_locked_synthetic_replay.sh data/replay/berth1_locked_synthetic_replay.csv" >&2
  exit 1
fi
${PYTHON:-python} -m os_cmasp.berth1_replay_adapter --mode validate --input "$IN" --out "$OUT" --report "${OUT%.csv}.validation_report.json"
