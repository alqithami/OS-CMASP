#!/usr/bin/env bash
set -euo pipefail
OUTDIR=${1:-outputs/berth1/promotion_demo}
scripts/run_maritime_twin_gate.sh data/examples/berth1_wide_example.csv "$OUTDIR"
