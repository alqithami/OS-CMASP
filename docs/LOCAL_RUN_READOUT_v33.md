# Local Run Readout v33

## Status

The uploaded local run validates the software path, not the maritime-twin claim. It is still useful because it confirms that the frozen Berth-1 ablation interface, preflight checks, replay writer, replay runner, diagnostics, and result packaging all execute end-to-end.

## Locked synthetic replay adapter

The adapter wrote `data/replay/berth1_locked_synthetic_replay.csv` in `locked-synthetic` mode. The bank report covered six frozen conditions, dominance table `maritime-dominance-v22`, solver `berth1-fixed-solver-v22`, four seeds, 320 steps, and the four active-regime scenario families. The leakage guard passed: hidden precondition truth differs while the controller-visible context remains equal for the ready/not-ready pair.

This remains a software sanity artifact and is not maritime-twin evidence.

## Locked replay demo result pattern

The locked demo passed all active-regime checks:

- provenance-preserving: mean regret 0, safety violations 0;
- provenance-erased: mean regret 0.434375, safety violations 0;
- labels-without-gating: mean regret 0.565625, safety violations 181;
- random-label placebo: mean regret 0.3625, safety violations 59, false certifications 59;
- oracle-visible-state: mean regret 0, safety violations 0;
- benign-agreement: mean regret 0, safety violations 0.

Interpretation: the scaffold behaves as intended. Provenance erasure is safe but burdensome, ungated labels expose safety risk, random labels do not solve the problem, oracle closes the gap, and benign agreement has low overhead.

## Wide-example converter

The example wide export converted successfully and exercised the from-wide path. Because the example has only four decision steps, it is not expected to give stable confidence intervals. Its role is path validation only.

## Next evidence step

The next paper-relevant step is a real twin export in wide one-row-per-step form. Do not hand-edit the long replay schema. Export a wide CSV, inspect it, convert it, then run the fixed-solver ablation:

```bash
scripts/inspect_berth1_wide_export.sh data/raw/my_twin_export.csv data/raw/my_twin_export.inspect_report.json
scripts/build_berth1_replay_from_wide.sh data/raw/my_twin_export.csv data/replay/twin_replay_claims.csv
scripts/run_berth1_replay.sh data/replay/twin_replay_claims.csv outputs/berth1/twin_v1
scripts/package_results.sh outputs/berth1/twin_v1 outputs/berth1/twin_v1_results.zip
```

Share back the zip and report:

```text
outputs/berth1/twin_v1_results.zip
outputs/berth1/twin_v1_report.md
```
