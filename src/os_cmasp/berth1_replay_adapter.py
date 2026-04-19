"""Replay CSV utilities for Berth-1-Conflict.

This module removes the need to hand-edit the long replay CSV template.
It supports three practical modes:

1. locked-synthetic: generate a fully runnable replay CSV from the locked
   synthetic Berth-1 bank. This is a pipeline check, not maritime evidence.
2. validate: validate an existing long replay CSV and optionally normalize it.
3. from-wide: convert a simple one-row-per-step CSV into the canonical long
   replay format using deterministic claim-generation rules.

The from-wide mode is intended for quick twin-export integration when the twin
can export one row per episode step with latent truth columns but does not yet
emit per-observer claim rows.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, Iterable, List

from .berth1_conflict import (
    CURRENT_SITUATION,
    PLANNING_SITUATION,
    Claim,
    EpisodeStep,
    LatentState,
    REPLAY_REQUIRED_FIELDS,
    REPLAY_TEMPLATE_FIELDS,
    generate_episode_bank,
    load_replay_bank,
    make_claims,
    validate_bank,
    write_replay_bank,
)

TRUE_SET = {"1", "true", "t", "yes", "y"}


def _bool(v: object, default: bool = True) -> bool:
    if v is None or str(v).strip() == "":
        return default
    return str(v).strip().lower() in TRUE_SET


def _get(row: Dict[str, str], key: str, default: str) -> str:
    val = row.get(key, default)
    return default if val is None or str(val).strip() == "" else str(val).strip()


def write_json(path: str | Path, payload: Dict[str, object]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def normalize_long(input_csv: str, output_csv: str | None = None) -> Dict[str, object]:
    bank = load_replay_bank(input_csv)
    report = validate_bank(bank)
    if output_csv:
        write_replay_bank(output_csv, bank)
    return {"mode": "validate", "input": input_csv, "output": output_csv, "bank_report": report}


def _default_claims_from_wide(row: Dict[str, str], x: LatentState, scenario: str, t: int) -> List[Claim]:
    """Build claims from a wide row.

    If observer-specific columns exist, they are used. Otherwise we fall back to
    the same deterministic claim generator used by the locked synthetic bank,
    with latent truths taken from the wide row.

    Supported optional observer-specific columns include examples such as:
      harbor_master_ready, strategic_plan_ready, crane_maintenance_crane_ok,
      ais_feed_eta_on_time, port_safety_weather_safe, human_dispatcher_weather_safe
    Values are booleans. Missing observer columns are fine.
    """
    claims: List[Claim] = []
    tstamp = int(float(_get(row, "timestamp", str(t))))
    provenance = _get(row, "provenance", "wide-export")

    mapping = [
        ("ready", "harbor_master_ready", "harbor_master", CURRENT_SITUATION),
        ("ready", "terminal_ops_ready", "terminal_ops", CURRENT_SITUATION),
        ("ready", "strategic_plan_ready", "strategic_plan", PLANNING_SITUATION),
        ("craneOK", "crane_maintenance_crane_ok", "crane_maintenance", CURRENT_SITUATION),
        ("craneOK", "terminal_ops_crane_ok", "terminal_ops", CURRENT_SITUATION),
        ("craneOK", "strategic_plan_crane_ok", "strategic_plan", PLANNING_SITUATION),
        ("etaOnTime", "ais_feed_eta_on_time", "ais_feed", CURRENT_SITUATION),
        ("etaOnTime", "carrier_schedule_eta_on_time", "carrier_schedule", PLANNING_SITUATION),
        ("weatherSafe", "port_safety_weather_safe", "port_safety", CURRENT_SITUATION),
        ("weatherSafe", "approved_weather_feed_weather_safe", "approved_weather_feed", CURRENT_SITUATION),
        ("weatherSafe", "human_dispatcher_weather_safe", "human_dispatcher", CURRENT_SITUATION),
    ]
    for prop, col, observer, situation in mapping:
        if col in row and str(row[col]).strip() != "":
            claims.append(Claim(prop, _bool(row[col]), observer, situation, timestamp=tstamp, provenance=f"{provenance}:{col}"))

    if claims:
        return claims
    return make_claims(x, scenario, t)


def convert_wide(input_csv: str, output_csv: str) -> Dict[str, object]:
    rows_out: List[EpisodeStep] = []
    with open(input_csv, newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("wide CSV has no header")
        required = {"seed", "t", "ready", "scenario"}
        missing = required - set(reader.fieldnames)
        if missing:
            raise ValueError(f"wide CSV missing columns: {sorted(missing)}")
        for row in reader:
            seed = int(row["seed"])
            t = int(row["t"])
            scenario = _get(row, "scenario", "authority_conflict")
            x = LatentState(
                ready=_bool(row.get("ready"), default=True),
                crane_ok=_bool(row.get("crane_ok"), default=True),
                eta_on_time=_bool(row.get("eta_on_time"), default=True),
                weather_safe=_bool(row.get("weather_safe"), default=True),
                queue_state=_get(row, "queue_state", "normal"),
                weather_regime=_get(row, "weather_regime", "clear"),
                disruption_family=_get(row, "disruption_family", "none"),
                vessel_class=_get(row, "vessel_class", "feeder"),
                operating_mode=_get(row, "operating_mode", "nominal"),
                time_bucket=_get(row, "time_bucket", "day"),
                berth_slot=_get(row, "berth_slot", "slot-A"),
                eta_bin=_get(row, "eta_bin", "on-window"),
            )
            claims = tuple(_default_claims_from_wide(row, x, scenario, t))
            rows_out.append(EpisodeStep(seed, t, scenario, x, claims))
    report = validate_bank(rows_out)
    write_replay_bank(output_csv, rows_out)
    return {"mode": "from-wide", "input": input_csv, "output": output_csv, "bank_report": report}


def main() -> None:
    parser = argparse.ArgumentParser(description="Build or validate Berth-1 replay CSVs without hand-editing templates")
    parser.add_argument("--mode", choices=["locked-synthetic", "validate", "from-wide"], required=True)
    parser.add_argument("--input", help="input CSV for validate/from-wide modes")
    parser.add_argument("--out", required=True, help="output replay CSV path, or normalized output for validate mode")
    parser.add_argument("--report", help="optional JSON report path")
    parser.add_argument("--scenario", default="mixed")
    parser.add_argument("--horizon", type=int, default=80)
    parser.add_argument("--seeds", type=int, default=4)
    parser.add_argument("--p-all-clear", type=float, default=0.5)
    args = parser.parse_args()

    if args.mode == "locked-synthetic":
        bank = generate_episode_bank(args.scenario, args.horizon, args.seeds, args.p_all_clear)
        report = validate_bank(bank)
        write_replay_bank(args.out, bank)
        payload = {
            "mode": args.mode,
            "output": args.out,
            "warning": "locked synthetic replay is a software sanity artifact, not maritime-twin evidence",
            "bank_report": report,
        }
    elif args.mode == "validate":
        if not args.input:
            raise SystemExit("--input is required for validate mode")
        payload = normalize_long(args.input, args.out)
    elif args.mode == "from-wide":
        if not args.input:
            raise SystemExit("--input is required for from-wide mode")
        payload = convert_wide(args.input, args.out)
    else:  # pragma: no cover
        raise AssertionError(args.mode)

    if args.report:
        write_json(args.report, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
