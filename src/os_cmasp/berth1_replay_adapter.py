"""Replay CSV utilities for Berth-1-Conflict.

This module removes the need to hand-edit the long replay CSV template.
It supports four practical modes:

1. locked-synthetic: generate a fully runnable replay CSV from the locked
   synthetic Berth-1 bank. This is a pipeline check, not maritime evidence.
2. validate: validate an existing long replay CSV and optionally normalize it.
3. inspect-wide: inspect a one-row-per-step CSV and report whether it can be
   converted without hand-editing.
4. from-wide: convert a simple one-row-per-step CSV into the canonical long
   replay format using deterministic claim-generation rules.

The from-wide mode is intended for quick twin-export integration when the twin
can export one row per episode step with latent truth columns but does not yet
emit per-observer claim rows. It accepts a small set of common column aliases so
that users do not need to rename columns manually in the common case.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Tuple

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

# Canonical one-row-per-step export columns and common aliases. Canonical names
# always win if present. Alias matching is case-insensitive.
WIDE_ALIASES: Dict[str, Tuple[str, ...]] = {
    "seed": ("seed", "episode", "episode_id", "run", "run_id", "trial", "trial_id", "replicate"),
    "t": ("t", "step", "time_step", "time", "tick", "period", "epoch"),
    "ready": ("ready", "berth_ready", "is_ready", "ready_to_berth", "berth_is_ready", "admission_ready"),
    "scenario": ("scenario", "scenario_family", "event_family", "conflict_type", "disruption_scenario"),
    "crane_ok": ("crane_ok", "craneOK", "crane_available", "crane_operational", "crane_ready"),
    "eta_on_time": ("eta_on_time", "etaOnTime", "eta_ok", "eta_within_window", "arrival_on_time", "vessel_on_time"),
    "weather_safe": ("weather_safe", "weatherSafe", "weather_ok", "safe_weather", "weather_clear"),
    "queue_state": ("queue_state", "queue", "queue_bin", "congestion_state"),
    "weather_regime": ("weather_regime", "weather", "metocean_regime"),
    "disruption_family": ("disruption_family", "disruption", "event_type", "incident_family"),
    "vessel_class": ("vessel_class", "ship_class", "vessel_type"),
    "operating_mode": ("operating_mode", "mode", "ops_mode"),
    "time_bucket": ("time_bucket", "shift", "period_of_day"),
    "berth_slot": ("berth_slot", "berth", "slot", "berth_id"),
    "eta_bin": ("eta_bin", "eta_bucket", "arrival_window"),
    # Optional observer-specific columns. These are copied by semantic name.
    "harbor_master_ready": ("harbor_master_ready", "hm_ready"),
    "terminal_ops_ready": ("terminal_ops_ready", "terminal_ready"),
    "strategic_plan_ready": ("strategic_plan_ready", "plan_ready", "planned_ready"),
    "crane_maintenance_crane_ok": ("crane_maintenance_crane_ok", "maintenance_crane_ok"),
    "terminal_ops_crane_ok": ("terminal_ops_crane_ok", "terminal_crane_ok"),
    "strategic_plan_crane_ok": ("strategic_plan_crane_ok", "plan_crane_ok"),
    "ais_feed_eta_on_time": ("ais_feed_eta_on_time", "ais_eta_on_time"),
    "carrier_schedule_eta_on_time": ("carrier_schedule_eta_on_time", "carrier_eta_on_time"),
    "port_safety_weather_safe": ("port_safety_weather_safe", "safety_weather_safe"),
    "approved_weather_feed_weather_safe": ("approved_weather_feed_weather_safe", "approved_weather_safe"),
    "human_dispatcher_weather_safe": ("human_dispatcher_weather_safe", "dispatcher_weather_safe"),
    "timestamp": ("timestamp", "claim_timestamp", "sim_time"),
    "provenance": ("provenance", "source_file", "source"),
}

REQUIRED_WIDE = ("seed", "t", "ready", "scenario")
OPTIONAL_WIDE = tuple(k for k in WIDE_ALIASES if k not in REQUIRED_WIDE)


def _bool(v: object, default: bool = True) -> bool:
    if v is None or str(v).strip() == "":
        return default
    return str(v).strip().lower() in TRUE_SET


def _get(row: Mapping[str, str], key: str, default: str) -> str:
    val = row.get(key, default)
    return default if val is None or str(val).strip() == "" else str(val).strip()


def write_json(path: str | Path, payload: Dict[str, object]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def _field_lookup(fieldnames: Iterable[str]) -> Dict[str, str]:
    """Return lowercase/stripped field name -> original field name."""
    return {str(name).strip().lower(): str(name) for name in fieldnames}


def infer_wide_mapping(fieldnames: Iterable[str]) -> Dict[str, Optional[str]]:
    """Infer a canonical-column mapping from a wide CSV header."""
    lookup = _field_lookup(fieldnames)
    mapping: Dict[str, Optional[str]] = {}
    for canonical, aliases in WIDE_ALIASES.items():
        found: Optional[str] = None
        for alias in aliases:
            key = alias.strip().lower()
            if key in lookup:
                found = lookup[key]
                break
        mapping[canonical] = found
    return mapping


def normalize_wide_row(row: Mapping[str, str], mapping: Mapping[str, Optional[str]]) -> Dict[str, str]:
    """Map user/twin column names onto canonical Berth-1 wide columns."""
    out: Dict[str, str] = {}
    for canonical, src in mapping.items():
        if src and src in row:
            out[canonical] = row[src]
    # Preserve canonical names that may not be part of the alias table in future.
    for key, value in row.items():
        out.setdefault(key, value)
    return out


def inspect_wide(input_csv: str) -> Dict[str, object]:
    """Inspect a wide export and report whether it is directly convertible."""
    with open(input_csv, newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("wide CSV has no header")
        mapping = infer_wide_mapping(reader.fieldnames)
        rows = list(reader)
    missing = [col for col in REQUIRED_WIDE if mapping.get(col) is None]
    recognized_required = {col: mapping[col] for col in REQUIRED_WIDE if mapping.get(col) is not None}
    recognized_optional = {col: mapping[col] for col in OPTIONAL_WIDE if mapping.get(col) is not None}
    unknown_columns = [c for c in (reader.fieldnames or []) if c not in set(x for x in mapping.values() if x)]
    return {
        "mode": "inspect-wide",
        "input": input_csv,
        "rows": len(rows),
        "convertible_without_manual_rename": len(missing) == 0,
        "required_wide_columns": list(REQUIRED_WIDE),
        "missing_required_canonical_columns": missing,
        "recognized_required_columns": recognized_required,
        "recognized_optional_columns": recognized_optional,
        "unknown_columns": unknown_columns,
        "next_command_if_convertible": (
            f"scripts/build_berth1_replay_from_wide.sh {input_csv} data/replay/twin_replay_claims.csv"
            if len(missing) == 0 else None
        ),
    }


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
        mapping = infer_wide_mapping(reader.fieldnames)
        missing = [col for col in REQUIRED_WIDE if mapping.get(col) is None]
        if missing:
            raise ValueError(
                "wide CSV missing required canonical columns after alias inference: "
                f"{missing}. Run scripts/inspect_berth1_wide_export.sh {input_csv} first."
            )
        for raw_row in reader:
            row = normalize_wide_row(raw_row, mapping)
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
    parser.add_argument("--mode", choices=["locked-synthetic", "validate", "inspect-wide", "from-wide"], required=True)
    parser.add_argument("--input", help="input CSV for validate/inspect-wide/from-wide modes")
    parser.add_argument("--out", help="output replay CSV path, or normalized output for validate mode")
    parser.add_argument("--report", help="optional JSON report path")
    parser.add_argument("--scenario", default="mixed")
    parser.add_argument("--horizon", type=int, default=80)
    parser.add_argument("--seeds", type=int, default=4)
    parser.add_argument("--p-all-clear", type=float, default=0.5)
    args = parser.parse_args()

    if args.mode == "locked-synthetic":
        if not args.out:
            raise SystemExit("--out is required for locked-synthetic mode")
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
    elif args.mode == "inspect-wide":
        if not args.input:
            raise SystemExit("--input is required for inspect-wide mode")
        payload = inspect_wide(args.input)
    elif args.mode == "from-wide":
        if not args.input:
            raise SystemExit("--input is required for from-wide mode")
        if not args.out:
            raise SystemExit("--out is required for from-wide mode")
        payload = convert_wide(args.input, args.out)
    else:  # pragma: no cover
        raise AssertionError(args.mode)

    if args.report:
        write_json(args.report, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
