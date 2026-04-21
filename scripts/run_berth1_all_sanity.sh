#!/usr/bin/env bash
set -euo pipefail
ROOT=${1:-outputs/berth1}
mkdir -p "$ROOT" data/replay artifacts/preflight

echo "[1/4] preflight"
scripts/run_berth1_preflight.sh artifacts/preflight

echo "[2/4] locked replay demo"
scripts/run_berth1_locked_replay_demo.sh "$ROOT/locked_replay_demo"

echo "[3/4] wide example conversion + replay run"
scripts/inspect_berth1_wide_export.sh data/examples/berth1_wide_example.csv data/replay/berth1_wide_example.inspect_report.json
scripts/build_berth1_replay_from_wide.sh data/examples/berth1_wide_example.csv data/replay/berth1_wide_example_replay.csv
scripts/run_berth1_replay.sh data/replay/berth1_wide_example_replay.csv "$ROOT/wide_example"
scripts/package_results.sh "$ROOT/wide_example" "$ROOT/wide_example_results.zip"

echo "[4/4] local validation bundle"
zip -q -r "$ROOT/local_validation_bundle.zip" \
  artifacts/preflight \
  data/replay/berth1_wide_example.inspect_report.json \
  data/replay/berth1_wide_example_replay.csv \
  data/replay/berth1_locked_synthetic_replay.csv \
  "$ROOT/locked_replay_demo_results.zip" \
  "$ROOT/locked_replay_demo_report.md" \
  "$ROOT/wide_example_results.zip" \
  "$ROOT/wide_example_report.md"

echo "done: $ROOT/local_validation_bundle.zip"
