#!/usr/bin/env python3
"""Summarize Berth-1-Conflict outputs into a shareable Markdown report.

Usage:
  python scripts/summarize_berth1_results.py outputs/twin_replay_v1

Reads:
  <prefix>_summary.csv
  <prefix>_paired.csv
  <prefix>_diagnostics.json
  <prefix>.manifest.json or manifest path recorded separately if present

Writes:
  <prefix>_report.md
  optional <prefix>_regret_bar.png if matplotlib is installed
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Dict, List

PRIMARY_ORDER = [
    "provenance_preserving",
    "provenance_erased",
    "random_label_placebo",
    "labels_without_gating",
    "oracle_visible_state",
    "benign_agreement",
]

SUMMARY_FIELDS = [
    "condition",
    "n",
    "mean_regret",
    "safety_violations",
    "waiting_cost",
    "idling_proxy",
    "intervention_cost",
    "false_certifications",
    "certification_rate",
    "gate_rate",
    "mean_contradiction_count",
]

PAIRED_METRICS = ["regret", "safety_violation", "waiting_cost", "intervention_cost", "false_certification"]


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def fmt(x: str) -> str:
    try:
        v = float(x)
    except Exception:
        return str(x)
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return f"{v:.4g}"


def table(headers: List[str], rows: List[List[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(row) + " |")
    return "\n".join(out)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: summarize_berth1_results.py <out-prefix>")
    prefix = Path(sys.argv[1])
    summary_path = Path(str(prefix) + "_summary.csv")
    paired_path = Path(str(prefix) + "_paired.csv")
    diagnostics_path = Path(str(prefix) + "_diagnostics.json")
    missing = [str(p) for p in [summary_path, paired_path, diagnostics_path] if not p.exists()]
    if missing:
        raise SystemExit("Missing expected output files: " + ", ".join(missing))

    summary = read_csv(summary_path)
    paired = read_csv(paired_path)
    diagnostics = json.loads(diagnostics_path.read_text())

    by_cond = {r["condition"]: r for r in summary}
    ordered_summary = [by_cond[c] for c in PRIMARY_ORDER if c in by_cond] + [r for r in summary if r["condition"] not in PRIMARY_ORDER]
    summary_rows = [[fmt(r.get(h, "")) for h in SUMMARY_FIELDS] for r in ordered_summary]

    paired_rows = []
    for cond in PRIMARY_ORDER:
        if cond == "provenance_preserving":
            continue
        for metric in PAIRED_METRICS:
            matches = [r for r in paired if r.get("condition") == cond and r.get("metric") == metric]
            if matches:
                r = matches[0]
                paired_rows.append([
                    cond,
                    metric,
                    fmt(r.get("mean_delta_vs_provenance_preserving", "")),
                    fmt(r.get("ci95_low", "")),
                    fmt(r.get("ci95_high", "")),
                    fmt(r.get("seeds", "")),
                ])

    checks = diagnostics.get("diagnostics", {}).get("checks", {})
    check_rows = [[k, str(v)] for k, v in checks.items()]

    report = []
    report.append("# Berth-1-Conflict results report")
    report.append("")
    report.append(f"Prefix: `{prefix}`")
    report.append("")
    report.append("## Summary by condition")
    report.append(table(SUMMARY_FIELDS, summary_rows))
    report.append("")
    report.append("## Paired deltas versus provenance-preserving")
    report.append(table(["condition", "metric", "mean delta", "CI95 low", "CI95 high", "seeds"], paired_rows))
    report.append("")
    report.append("## Go/no-go diagnostics")
    report.append(table(["check", "value"], check_rows))
    report.append("")
    report.append("## Interpretation rule")
    report.append("The first paper-critical comparison is provenance_preserving vs provenance_erased under the same episode bank and frozen solver. A positive paired regret delta with zero or lower safety violations for provenance_erased supports the process-semantics separation. labels_without_gating should expose why certificates/admissibility matter; oracle_visible_state should close the gap; benign_agreement should have low overhead.")
    report_path = Path(str(prefix) + "_report.md")
    report_path.write_text("\n".join(report) + "\n")

    try:
        import matplotlib.pyplot as plt  # type: ignore
        conds = [r["condition"] for r in ordered_summary]
        regrets = [float(r.get("mean_regret", 0.0)) for r in ordered_summary]
        fig = plt.figure(figsize=(9, 4.5))
        ax = fig.add_subplot(111)
        ax.bar(range(len(conds)), regrets)
        ax.set_xticks(range(len(conds)))
        ax.set_xticklabels(conds, rotation=35, ha="right")
        ax.set_ylabel("Mean regret")
        ax.set_title("Berth-1-Conflict mean regret by condition")
        fig.tight_layout()
        fig.savefig(str(prefix) + "_regret_bar.png", dpi=200)
        plt.close(fig)
    except Exception:
        pass

    print(f"wrote {report_path}")

if __name__ == "__main__":
    main()
