# OS-CMASP v31 experiment pipeline: no manual CSV editing

This version fixes the previous replay-pipeline problem: you no longer need to hand-edit `berth1_replay_template.csv` or paste CSV headers into the shell. The template remains schema documentation only.

## 0. Install and contract checks

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .

make test
make preflight
```

## 1. No-manual replay-path check

This command generates a fully runnable locked synthetic replay CSV, runs the replay path on it, and packages the outputs.

```bash
scripts/run_berth1_locked_replay_demo.sh outputs/berth1/locked_replay_demo
```

Expected output package:

```text
outputs/berth1/locked_replay_demo_results.zip
```

This is a software sanity artifact, not maritime-twin evidence. It proves that the replay interface works end-to-end without manual CSV editing.

## 2. Optional direct synthetic smoke test

The older smoke-test path is still available:

```bash
scripts/run_berth1_synthetic_smoke.sh outputs/berth1/synthetic_smoke
scripts/package_results.sh outputs/berth1/synthetic_smoke outputs/berth1/synthetic_smoke_results.zip
```

Use this only as a scaffold check.

## 3. Convert a simple wide export into replay CSV

If your maritime/twin code can export one row per episode step, use the wide adapter. The required wide columns are:

```text
seed,t,ready,scenario
```

Recommended truth/context columns are:

```text
crane_ok,eta_on_time,weather_safe,
queue_state,weather_regime,disruption_family,vessel_class,
operating_mode,time_bucket,berth_slot,eta_bin
```

Optional observer-specific columns include:

```text
harbor_master_ready,terminal_ops_ready,strategic_plan_ready,
crane_maintenance_crane_ok,terminal_ops_crane_ok,strategic_plan_crane_ok,
ais_feed_eta_on_time,carrier_schedule_eta_on_time,
port_safety_weather_safe,approved_weather_feed_weather_safe,human_dispatcher_weather_safe
```

Example:

```bash
scripts/build_berth1_replay_from_wide.sh \
  data/examples/berth1_wide_example.csv \
  data/replay/berth1_wide_example_replay.csv

scripts/run_berth1_replay.sh \
  data/replay/berth1_wide_example_replay.csv \
  outputs/berth1/wide_example

scripts/package_results.sh \
  outputs/berth1/wide_example \
  outputs/berth1/wide_example_results.zip
```

For actual twin results, replace only the input wide CSV path:

```bash
scripts/build_berth1_replay_from_wide.sh \
  data/raw/my_twin_export.csv \
  data/replay/twin_replay_claims.csv

scripts/run_berth1_replay.sh \
  data/replay/twin_replay_claims.csv \
  outputs/berth1/twin_v1

scripts/package_results.sh \
  outputs/berth1/twin_v1 \
  outputs/berth1/twin_v1_results.zip
```

## 4. Validate an already-long replay CSV

If you already have one row per claim, validate and normalize it:

```bash
scripts/validate_berth1_replay_csv.sh \
  data/replay/twin_replay_claims.csv \
  data/replay/twin_replay_claims.normalized.csv
```

Then run the normalized replay:

```bash
scripts/run_berth1_replay.sh \
  data/replay/twin_replay_claims.normalized.csv \
  outputs/berth1/twin_v1
```

## 5. What to share back

Share the result zip and report:

```text
outputs/berth1/<run_name>_results.zip
outputs/berth1/<run_name>_report.md
```

The zip contains:

```text
<prefix>.csv
<prefix>_summary.csv
<prefix>_paired.csv
<prefix>_diagnostics.json
<prefix>.manifest.json
<prefix>.preflight_manifest.json
<prefix>_report.md
```

## 6. Interpretation order

Inspect in this order:

1. preflight leakage guard;
2. provenance_erased - provenance_preserving paired regret;
3. labels_without_gating safety violations;
4. random_label_placebo behavior;
5. oracle_visible_state closure;
6. benign_agreement overhead.

A replay run is informative only if the solver, seeds, dominance table, and ablation set remain fixed.
