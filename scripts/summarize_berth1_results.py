#!/usr/bin/env python3
"""Write a compact Markdown report for Berth-1-Conflict outputs."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Iterable, List, Dict


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def md_table(rows: List[Dict[str, object]], columns: List[str]) -> str:
    out = []
    out.append("| " + " | ".join(columns) + " |")
    out.append("|" + "|".join(["---" for _ in columns]) + "|")
    for row in rows:
        out.append("| " + " | ".join(str(row.get(c, "")) for c in columns) + " |")
    return "\n".join(out)


def maybe_float(s: str) -> object:
    try:
        f = float(s)
        if abs(f - round(f)) < 1e-12:
            return int(round(f))
        return round(f, 6)
    except Exception:
        return s


def compact(rows: Iterable[Dict[str, str]]) -> List[Dict[str, object]]:
    return [{k: maybe_float(v) for k, v in row.items()} for row in rows]


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: summarize_berth1_results.py output_prefix")
    prefix = Path(sys.argv[1])
    summary_path = Path(f"{prefix}_summary.csv")
    paired_path = Path(f"{prefix}_paired.csv")
    diag_path = Path(f"{prefix}_diagnostics.json")
    manifest_path = Path(f"{prefix}.manifest.json")
    preflight_path = Path(f"{prefix}.preflight_manifest.json")
    required = [summary_path, paired_path, diag_path, manifest_path, preflight_path]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise SystemExit("missing required files for report:\n" + "\n".join(missing))

    summary = compact(read_csv(summary_path))
    paired = compact(read_csv(paired_path))
    diag = json.loads(diag_path.read_text())
    checks = diag.get("diagnostics", {}).get("checks", {})

    summary_cols = ["condition", "n", "mean_regret", "safety_violations", "waiting_cost", "intervention_cost", "false_certifications"]
    paired_cols = ["condition", "metric", "mean_delta_vs_provenance_preserving", "ci95_low", "ci95_high"]
    # Older versions used mean_delta; normalize the display if needed.
    for row in paired:
        if "mean_delta_vs_provenance_preserving" not in row and "mean_delta" in row:
            row["mean_delta_vs_provenance_preserving"] = row["mean_delta"]

    lines = []
    lines.append(f"# Berth-1-Conflict Report: `{prefix}`")
    lines.append("")
    lines.append("## Summary by condition")
    lines.append("")
    lines.append(md_table(summary, summary_cols))
    lines.append("")
    lines.append("## Paired deltas vs provenance_preserving")
    lines.append("")
    lines.append(md_table(paired, paired_cols))
    lines.append("")
    lines.append("## Diagnostics")
    lines.append("")
    lines.append("| check | value |")
    lines.append("|---|---:|")
    for k, v in sorted(checks.items()):
        lines.append(f"| {k} | {v} |")
    lines.append("")
    lines.append("## Files to share")
    lines.append("")
    for p in required + [Path(f"{prefix}_report.md")]:
        lines.append(f"- `{p}`")
    lines.append("")
    report_path = Path(f"{prefix}_report.md")
    report_path.write_text("\n".join(lines))
    print(f"wrote {report_path}")


if __name__ == "__main__":
    main()
