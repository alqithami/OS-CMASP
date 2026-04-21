#!/usr/bin/env bash
set -euo pipefail
if [ $# -lt 1 ]; then
  echo "usage: $0 input_wide.csv [report.json]" >&2
  echo "inspects whether a one-row-per-step twin export can be converted without manual CSV editing" >&2
  exit 2
fi
IN=$1
REPORT=${2:-${IN%.csv}.inspect_report.json}
if [ ! -f "$IN" ]; then
  echo "Missing input wide CSV: $IN" >&2
  exit 1
fi
mkdir -p "$(dirname "$REPORT")"
${PYTHON:-python} -m os_cmasp.berth1_replay_adapter --mode inspect-wide --input "$IN" --report "$REPORT"
echo "wrote inspect report: $REPORT"
