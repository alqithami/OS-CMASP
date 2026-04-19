#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 1 ]]; then
  echo "usage: $0 path/to/twin_replay_claims.csv [out_prefix]" >&2
  exit 2
fi
REPLAY_CSV="$1"
OUT_PREFIX="${2:-outputs/twin_replay_v1}"
mkdir -p "$(dirname "$OUT_PREFIX")"
python -m os_cmasp.berth1_conflict \
  --mode run \
  --replay-csv "$REPLAY_CSV" \
  --out-prefix "$OUT_PREFIX" \
  --manifest "${OUT_PREFIX}.manifest.json"
