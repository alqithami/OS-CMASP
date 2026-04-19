#!/usr/bin/env bash
set -euo pipefail
PYTHON_BIN="${PYTHON_BIN:-python}"


OUT_CSV="${1:-data/replay/berth1_replay_template.csv}"
mkdir -p "$(dirname "$OUT_CSV")"
$PYTHON_BIN -m os_cmasp.berth1_conflict --write-template "$OUT_CSV"
echo "Replay template written to $OUT_CSV"
