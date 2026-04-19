#!/usr/bin/env bash
set -euo pipefail
if [ $# -lt 2 ]; then
  echo "usage: $0 input_wide.csv output_replay.csv" >&2
  echo "wide required columns: seed,t,ready,scenario" >&2
  echo "wide optional truth/context columns: crane_ok,eta_on_time,weather_safe,queue_state,weather_regime,disruption_family,vessel_class,operating_mode,time_bucket,berth_slot,eta_bin" >&2
  echo "wide optional observer columns: harbor_master_ready,strategic_plan_ready,crane_maintenance_crane_ok,ais_feed_eta_on_time,port_safety_weather_safe,human_dispatcher_weather_safe" >&2
  exit 2
fi
IN=$1
OUT=$2
if [ ! -f "$IN" ]; then
  echo "Missing input wide CSV: $IN" >&2
  exit 1
fi
mkdir -p "$(dirname "$OUT")"
${PYTHON:-python} -m os_cmasp.berth1_replay_adapter --mode from-wide --input "$IN" --out "$OUT" --report "${OUT%.csv}.adapter_report.json"
