#!/usr/bin/env bash
set -euo pipefail
if [ $# -lt 2 ]; then
  echo "usage: $0 replay.csv output_prefix" >&2
  exit 2
fi
REPLAY=$1
PREFIX=$2
if [ ! -f "$REPLAY" ]; then
  echo "Missing replay CSV: $REPLAY" >&2
  echo "This command requires an actual CSV file, not a placeholder." >&2
  echo "For a no-manual pipeline check, run:" >&2
  echo "  scripts/run_berth1_locked_replay_demo.sh outputs/berth1/locked_replay_demo" >&2
  echo "For twin export conversion from a wide CSV, run:" >&2
  echo "  scripts/build_berth1_replay_from_wide.sh raw_twin_export.csv data/replay/twin_replay_claims.csv" >&2
  exit 1
fi
mkdir -p "$(dirname "$PREFIX")"
${PYTHON:-python} -m os_cmasp.berth1_conflict --mode preflight --replay-csv "$REPLAY" --manifest "${PREFIX}.preflight_manifest.json" --out-prefix "$PREFIX"
${PYTHON:-python} -m os_cmasp.berth1_conflict --mode run --replay-csv "$REPLAY" --manifest "${PREFIX}.manifest.json" --out-prefix "$PREFIX"
${PYTHON:-python} scripts/summarize_berth1_results.py "$PREFIX"
