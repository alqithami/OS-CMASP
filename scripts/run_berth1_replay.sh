#!/usr/bin/env bash
set -euo pipefail
PYTHON_BIN="${PYTHON_BIN:-python}"


if [[ $# -lt 2 ]]; then
  cat >&2 <<'USAGE'
Usage: scripts/run_berth1_replay.sh ACTUAL_REPLAY_CSV OUT_PREFIX

Example:
  scripts/run_berth1_replay.sh data/replay/twin_replay_claims.csv outputs/berth1/twin_v1

Do not pass the documentation placeholder path/to/twin_replay_claims.csv.
Create a template first with:
  scripts/write_berth1_replay_template.sh data/replay/berth1_replay_template.csv
USAGE
  exit 2
fi

REPLAY_CSV="$1"
OUT_PREFIX="$2"

if [[ "$REPLAY_CSV" == path/to/* || "$REPLAY_CSV" == *twin_replay_claims.csv && ! -f "$REPLAY_CSV" ]]; then
  echo "ERROR: Replay CSV does not exist: $REPLAY_CSV" >&2
  echo "Replace the placeholder with an actual CSV path. For a pipeline check, run:" >&2
  echo "  scripts/run_berth1_synthetic_smoke.sh outputs/berth1/synthetic_smoke" >&2
  exit 2
fi

if [[ ! -f "$REPLAY_CSV" ]]; then
  echo "ERROR: Replay CSV does not exist: $REPLAY_CSV" >&2
  echo "Create/check the file, or generate a schema template with:" >&2
  echo "  scripts/write_berth1_replay_template.sh data/replay/berth1_replay_template.csv" >&2
  exit 2
fi

mkdir -p "$(dirname "$OUT_PREFIX")"

$PYTHON_BIN -m os_cmasp.berth1_conflict \
  --mode preflight \
  --replay-csv "$REPLAY_CSV" \
  --manifest "$OUT_PREFIX.preflight_manifest.json"

$PYTHON_BIN -m os_cmasp.berth1_conflict \
  --mode run \
  --replay-csv "$REPLAY_CSV" \
  --out-prefix "$OUT_PREFIX" \
  --manifest "$OUT_PREFIX.manifest.json"

$PYTHON_BIN scripts/summarize_berth1_results.py "$OUT_PREFIX"
