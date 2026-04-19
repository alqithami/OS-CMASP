#!/usr/bin/env bash
set -euo pipefail
OUT=${1:-data/replay/berth1_replay_template.csv}
mkdir -p "$(dirname "$OUT")"
${PYTHON:-python} -m os_cmasp.berth1_conflict --write-template "$OUT"
echo "Replay template written to $OUT"
echo "This template is documentation only; do not paste its header into the shell."
