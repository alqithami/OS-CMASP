#!/usr/bin/env bash
set -euo pipefail
if [ $# -lt 2 ]; then
  echo "usage: $0 input_wide_or_long.csv output_dir [--long-form]" >&2
  echo "" >&2
  echo "Wide mode expects one row per simulator step and converts it to canonical claim replay." >&2
  echo "Long-form mode expects a canonical one-row-per-claim replay CSV and validates it directly." >&2
  exit 2
fi
IN=$1
OUTDIR=$2
MODE=${3:-wide}
PY=${PYTHON:-python}
if [ ! -f "$IN" ]; then
  echo "Missing input CSV: $IN" >&2
  exit 1
fi
mkdir -p "$OUTDIR" data/replay
PREFIX="$OUTDIR/twin_gate"
INSPECT="$OUTDIR/twin_gate.inspect_report.json"
REPLAY="$OUTDIR/twin_gate_claims.csv"

if [ "$MODE" = "--long-form" ] || [ "$MODE" = "long-form" ]; then
  echo "[1/5] validate long-form replay"
  $PY -m os_cmasp.berth1_replay_adapter --mode validate --input "$IN" --out "$REPLAY" --report "$OUTDIR/twin_gate.adapter_report.json"
else
  echo "[1/5] inspect wide export"
  scripts/inspect_berth1_wide_export.sh "$IN" "$INSPECT"
  $PY - <<PY2
import json, sys
p = "$INSPECT"
with open(p) as f:
    report = json.load(f)
if not report.get("convertible_without_manual_rename"):
    print(json.dumps(report, indent=2, sort_keys=True))
    raise SystemExit("Wide export is not convertible. Share this inspect report and the CSV header; do not edit replay rows manually.")
PY2
  echo "[2/5] convert wide export to canonical replay"
  scripts/build_berth1_replay_from_wide.sh "$IN" "$REPLAY"
fi

echo "[3/5] run frozen Berth-1 ablation"
scripts/run_berth1_replay.sh "$REPLAY" "$PREFIX"

echo "[4/5] package outputs"
scripts/package_results.sh "$PREFIX" "$OUTDIR/twin_gate_results.zip"

echo "[5/5] write promotion report"
if [ -f "$INSPECT" ]; then
  $PY scripts/write_promotion_gate_report.py "$PREFIX" --inspect-report "$INSPECT" --out "$OUTDIR/twin_gate_promotion_report.md" --json-out "$OUTDIR/twin_gate_promotion_gate.json"
else
  $PY scripts/write_promotion_gate_report.py "$PREFIX" --out "$OUTDIR/twin_gate_promotion_report.md" --json-out "$OUTDIR/twin_gate_promotion_gate.json"
fi

echo "done: $OUTDIR"
echo "share: $OUTDIR/twin_gate_results.zip and $OUTDIR/twin_gate_promotion_report.md"
