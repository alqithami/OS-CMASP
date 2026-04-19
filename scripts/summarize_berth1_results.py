#!/usr/bin/env python3
from __future__ import annotations
import csv
import json
import sys
from pathlib import Path


def read_csv(path: Path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: summarize_berth1_results.py output_prefix")
    prefix = Path(sys.argv[1])
    summary_path = Path(str(prefix) + "_summary.csv")
    paired_path = Path(str(prefix) + "_paired.csv")
    diag_path = Path(str(prefix) + "_diagnostics.json")
    out_path = Path(str(prefix) + "_report.md")
    summary = read_csv(summary_path)
    paired = read_csv(paired_path)
    diagnostics = json.loads(diag_path.read_text()).get("diagnostics", {})

    lines = [f"# Berth-1-Conflict Report: `{prefix}`", "", "## Summary by condition", ""]
    cols = ["condition", "n", "mean_regret", "safety_violations", "waiting_cost", "intervention_cost", "false_certifications"]
    lines.append("| " + " | ".join(cols) + " |")
    lines.append("|" + "---|" * len(cols))
    for row in summary:
        lines.append("| " + " | ".join(str(row.get(c, "")) for c in cols) + " |")
    lines += ["", "## Paired deltas vs provenance_preserving", ""]
    pcols = ["condition", "metric", "mean_delta_vs_provenance_preserving", "ci95_low", "ci95_high"]
    lines.append("| " + " | ".join(pcols) + " |")
    lines.append("|" + "---|" * len(pcols))
    for row in paired:
        lines.append("| " + " | ".join(str(row.get(c, "")) for c in pcols) + " |")
    lines += ["", "## Diagnostics", ""]
    lines.append("| check | value |")
    lines.append("|---|---:|")
    for k, v in diagnostics.get("checks", {}).items():
        lines.append(f"| {k} | {v} |")
    lines += ["", "## Files to share", ""]
    for suffix in ["_summary.csv", "_paired.csv", "_diagnostics.json", ".manifest.json", ".preflight_manifest.json", "_report.md"]:
        lines.append(f"- `{prefix}{suffix}`")
    out_path.write_text("\n".join(lines) + "\n")
    print(f"wrote {out_path}")

if __name__ == "__main__":
    main()
