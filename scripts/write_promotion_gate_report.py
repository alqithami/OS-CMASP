#!/usr/bin/env python3
"""Write a promotion-gate report for Berth-1 replay results.

This script turns the raw output bundle from the frozen Berth-1 ablation into a
human-readable decision report. It deliberately separates:

- software sanity evidence: synthetic/locked generated replays;
- replay-interface evidence: converted example rows or schema checks;
- paper-relevant evidence: declared maritime-twin replay with a non-null replay
  CSV recorded in the manifest.

It does not alter results. It only reads summary, paired-delta, diagnostics, and
manifest files produced by the existing pipeline.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Dict, Iterable, Optional


def _read_json(path: Path) -> Dict[str, Any]:
    with path.open() as f:
        return json.load(f)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def _float(row: dict[str, str], key: str, default: float = 0.0) -> float:
    try:
        return float(row.get(key, default))
    except (TypeError, ValueError):
        return default


def _int(row: dict[str, str], key: str, default: int = 0) -> int:
    try:
        return int(float(row.get(key, default)))
    except (TypeError, ValueError):
        return default


def _by_condition(rows: Iterable[dict[str, str]]) -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        cond = row.get("condition")
        if cond:
            out[cond] = row
    return out


def _paired_lookup(rows: Iterable[dict[str, str]], condition: str, metric: str) -> Optional[dict[str, str]]:
    for row in rows:
        if row.get("condition") == condition and row.get("metric") == metric:
            return row
    return None


def classify_evidence(manifest: Dict[str, Any], inspect_report: Optional[Dict[str, Any]]) -> str:
    replay_csv = manifest.get("replay_csv")
    if replay_csv:
        if inspect_report and inspect_report.get("input") and "example" in str(inspect_report.get("input", "")).lower():
            return "pipeline/example replay - not paper evidence"
        return "declared replay run - candidate paper evidence if the CSV is a real twin export"
    scenario = manifest.get("scenario")
    if scenario:
        return "locked synthetic/software sanity - not maritime evidence"
    return "unknown evidence class"


def promotion_decision(summary_rows: list[dict[str, str]], paired_rows: list[dict[str, str]], diagnostics: Dict[str, Any]) -> Dict[str, Any]:
    s = _by_condition(summary_rows)
    erased_regret = _paired_lookup(paired_rows, "provenance_erased", "regret")
    random_regret = _paired_lookup(paired_rows, "random_label_placebo", "regret")
    labels_safety = _paired_lookup(paired_rows, "labels_without_gating", "safety_violation")

    preserving = s.get("provenance_preserving", {})
    oracle = s.get("oracle_visible_state", {})
    benign = s.get("benign_agreement", {})

    criteria = {
        "diagnostics_all_pass": bool(diagnostics.get("diagnostics", diagnostics).get("all_checks_pass", False)),
        "preserving_zero_violation": _int(preserving, "safety_violations", 999) == 0,
        "preserving_low_regret": _float(preserving, "mean_regret", 999.0) <= 1e-9,
        "erasure_regret_ci_positive": bool(erased_regret) and _float(erased_regret or {}, "ci95_low", -999.0) > 0.0,
        "random_placebo_not_oracle": bool(random_regret) and _float(random_regret or {}, "mean_delta_vs_provenance_preserving", 0.0) > 0.0,
        "ungated_safety_need_visible": bool(labels_safety) and _float(labels_safety or {}, "mean_delta_vs_provenance_preserving", 0.0) > 0.0,
        "oracle_closes_gap": _float(oracle, "mean_regret", 999.0) <= 1e-9 and _int(oracle, "safety_violations", 999) == 0,
        "benign_low_overhead": _float(benign, "mean_regret", 999.0) <= 1e-9 and _int(benign, "safety_violations", 999) == 0,
    }
    return {"criteria": criteria, "gate_pass": all(criteria.values())}


def write_markdown(
    out: Path,
    prefix: Path,
    evidence_class: str,
    manifest: Dict[str, Any],
    diagnostics: Dict[str, Any],
    summary_rows: list[dict[str, str]],
    paired_rows: list[dict[str, str]],
    inspect_report: Optional[Dict[str, Any]],
    decision: Dict[str, Any],
) -> None:
    diag = diagnostics.get("diagnostics", diagnostics)
    lines: list[str] = []
    lines.append(f"# OS-CMASP Promotion Gate Report: `{prefix}`")
    lines.append("")
    lines.append(f"**Evidence class:** {evidence_class}")
    lines.append("")
    lines.append("## Gate decision")
    lines.append("")
    lines.append("| Criterion | Pass |")
    lines.append("|---|---:|")
    for key, value in decision["criteria"].items():
        lines.append(f"| `{key}` | {str(value)} |")
    lines.append(f"| **overall_gate_pass** | **{decision['gate_pass']}** |")
    lines.append("")

    if inspect_report is not None:
        lines.append("## Wide-export inspection")
        lines.append("")
        lines.append("| Field | Value |")
        lines.append("|---|---|")
        for key in ["input", "rows", "convertible_without_manual_rename", "missing_required_canonical_columns"]:
            lines.append(f"| `{key}` | `{inspect_report.get(key)}` |")
        lines.append("")

    lines.append("## Manifest")
    lines.append("")
    bank_report = manifest.get("bank_report", {}) if isinstance(manifest.get("bank_report"), dict) else {}
    lines.append("| Field | Value |")
    lines.append("|---|---|")
    for key in ["mode", "scenario", "solver_version", "dominance_table_version", "replay_csv", "replay_sha256"]:
        lines.append(f"| `{key}` | `{manifest.get(key)}` |")
    # For replay runs, the command-line horizon/seeds are defaults; the bank report is authoritative.
    lines.append(f"| `bank_steps` | `{bank_report.get('steps', manifest.get('horizon'))}` |")
    lines.append(f"| `bank_seeds` | `{bank_report.get('seeds', manifest.get('seeds'))}` |")
    lines.append(f"| `bank_scenarios` | `{bank_report.get('scenarios')}` |")
    lines.append("")

    lines.append("## Diagnostics")
    lines.append("")
    lines.append(f"Interpretation: `{diag.get('interpretation')}`")
    lines.append("")
    lines.append("| Check | Value |")
    lines.append("|---|---:|")
    for key, value in sorted(diag.get("checks", {}).items()):
        lines.append(f"| `{key}` | {value} |")
    lines.append("")

    lines.append("## Summary by condition")
    lines.append("")
    fields = ["condition", "n", "mean_regret", "safety_violations", "waiting_cost", "intervention_cost", "false_certifications"]
    lines.append("| " + " | ".join(fields) + " |")
    lines.append("|" + "|".join(["---"] + ["---:"] * (len(fields) - 1)) + "|")
    for row in summary_rows:
        lines.append("| " + " | ".join(str(row.get(f, "")) for f in fields) + " |")
    lines.append("")

    lines.append("## Promotion interpretation")
    lines.append("")
    if "not maritime evidence" in evidence_class or "software sanity" in evidence_class:
        lines.append("This run validates the executable pathway and active-regime scaffold. It should not be reported as maritime-twin evidence.")
    elif decision["gate_pass"]:
        lines.append("This run satisfies the Berth-1 promotion criteria. The next step is a larger twin slice with the same frozen condition set and manifest discipline.")
    else:
        lines.append("This run does not satisfy all promotion criteria. Do not scale up by changing the solver; inspect the failed criterion and either narrow the active regime or revise the declared dominance/claim mapping before running a new locked replay.")
    lines.append("")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Write promotion-gate report from Berth-1 replay outputs")
    parser.add_argument("prefix", help="output prefix used by run_berth1_replay.sh, e.g. outputs/berth1/twin_v1")
    parser.add_argument("--inspect-report", help="optional wide-export inspection JSON")
    parser.add_argument("--out", help="output markdown path; defaults to <prefix>_promotion_report.md")
    parser.add_argument("--json-out", help="optional machine-readable gate summary JSON")
    args = parser.parse_args()

    prefix = Path(args.prefix)
    summary_path = Path(f"{prefix}_summary.csv")
    paired_path = Path(f"{prefix}_paired.csv")
    diagnostics_path = Path(f"{prefix}_diagnostics.json")
    manifest_path = Path(f"{prefix}.manifest.json")

    missing = [p for p in [summary_path, paired_path, diagnostics_path, manifest_path] if not p.exists()]
    if missing:
        raise SystemExit("Missing required output files for promotion report:\n" + "\n".join(str(p) for p in missing))

    summary_rows = _read_csv(summary_path)
    paired_rows = _read_csv(paired_path)
    diagnostics = _read_json(diagnostics_path)
    manifest = _read_json(manifest_path)
    inspect_report = _read_json(Path(args.inspect_report)) if args.inspect_report else None
    evidence_class = classify_evidence(manifest, inspect_report)
    decision = promotion_decision(summary_rows, paired_rows, diagnostics)

    out = Path(args.out) if args.out else Path(f"{prefix}_promotion_report.md")
    write_markdown(out, prefix, evidence_class, manifest, diagnostics, summary_rows, paired_rows, inspect_report, decision)
    payload = {"prefix": str(prefix), "evidence_class": evidence_class, **decision}
    if args.json_out:
        Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_out).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"report": str(out), **payload}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
