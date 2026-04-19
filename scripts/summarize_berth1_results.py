#!/usr/bin/env python3
"""Create a small shareable Markdown report from Berth-1 output files."""
from __future__ import annotations
import csv, json, sys
from pathlib import Path

if len(sys.argv) != 2:
    raise SystemExit("Usage: scripts/summarize_berth1_results.py OUT_PREFIX")

prefix = Path(sys.argv[1])
summary_path = Path(str(prefix) + "_summary.csv")
paired_path = Path(str(prefix) + "_paired.csv")
diag_path = Path(str(prefix) + "_diagnostics.json")
report_path = Path(str(prefix) + "_report.md")
for p in (summary_path, paired_path, diag_path):
    if not p.exists():
        raise SystemExit(f"Missing required file: {p}")

def read_csv(path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))
summary = read_csv(summary_path)
paired = read_csv(paired_path)
with diag_path.open() as f:
    diagnostics = json.load(f)

lines = []
lines.append(f"# Berth-1-Conflict Report: `{prefix}`")
lines.append("")
lines.append("## Summary by condition")
lines.append("")
lines.append("| condition | n | mean_regret | safety_violations | waiting_cost | intervention_cost | false_certifications |")
lines.append("|---|---:|---:|---:|---:|---:|---:|")
for r in summary:
    lines.append("| {condition} | {n} | {mean_regret} | {safety_violations} | {waiting_cost} | {intervention_cost} | {false_certifications} |".format(**r))
lines.append("")
lines.append("## Paired deltas vs provenance_preserving")
lines.append("")
lines.append("| condition | metric | mean_delta | ci95_low | ci95_high |")
lines.append("|---|---|---:|---:|---:|")
for r in paired:
    lines.append("| {condition} | {metric} | {mean_delta_vs_provenance_preserving} | {ci95_low} | {ci95_high} |".format(**r))
lines.append("")
lines.append("## Diagnostics")
lines.append("")
checks = diagnostics.get("diagnostics", diagnostics).get("checks", {})
if checks:
    lines.append("| check | value |")
    lines.append("|---|---:|")
    for k, v in checks.items():
        lines.append(f"| {k} | {v} |")
else:
    lines.append("Diagnostics JSON did not contain a `checks` field.")
lines.append("")
lines.append("## Files to share")
lines.append("")
for p in (summary_path, paired_path, diag_path, Path(str(prefix)+".manifest.json"), Path(str(prefix)+".preflight_manifest.json"), report_path):
    lines.append(f"- `{p}`")
report_path.write_text("\n".join(lines) + "\n")
print(f"wrote {report_path}")
