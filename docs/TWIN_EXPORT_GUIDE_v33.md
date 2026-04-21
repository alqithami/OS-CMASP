# Twin Export Guide v33

This guide avoids manual replay-row editing.

## Option A: preferred long export

If the twin can export one row per observer claim, use this long schema directly:

```text
seed,t,ready,crane_ok,eta_on_time,weather_safe,scenario,
queue_state,weather_regime,disruption_family,vessel_class,operating_mode,
time_bucket,berth_slot,eta_bin,prop,value,observer,situation,credibility,timestamp,provenance
```

Then validate and run:

```bash
python -m os_cmasp.berth1_replay_adapter \
  --mode validate \
  --input data/raw/twin_long_claims.csv \
  --out data/replay/twin_replay_claims.csv \
  --report data/replay/twin_replay_claims.adapter_report.json

scripts/run_berth1_replay.sh data/replay/twin_replay_claims.csv outputs/berth1/twin_v1
scripts/package_results.sh outputs/berth1/twin_v1 outputs/berth1/twin_v1_results.zip
```

## Option B: simple wide export

If the twin cannot export per-observer claims, export one row per step with at least:

```text
seed,t,ready,scenario
```

Recommended columns:

```text
crane_ok,eta_on_time,weather_safe,
queue_state,weather_regime,disruption_family,vessel_class,
operating_mode,time_bucket,berth_slot,eta_bin
```

Common aliases such as `episode_id`, `step`, `berth_ready`, `scenario_family`, `crane_available`, `arrival_on_time`, and `weather_ok` are recognized automatically.

Inspect first:

```bash
scripts/inspect_berth1_wide_export.sh data/raw/my_twin_export.csv data/raw/my_twin_export.inspect_report.json
```

If `convertible_without_manual_rename` is true, run:

```bash
scripts/build_berth1_replay_from_wide.sh data/raw/my_twin_export.csv data/replay/twin_replay_claims.csv
scripts/run_berth1_replay.sh data/replay/twin_replay_claims.csv outputs/berth1/twin_v1
scripts/package_results.sh outputs/berth1/twin_v1 outputs/berth1/twin_v1_results.zip
```

If the inspect report says a required canonical column is missing, the export itself lacks the needed information. Do not edit replay rows by hand; either add that column to the twin export or share the inspect report and raw CSV header so the alias table can be extended.

## Local sanity before real twin export

Run this from the repository root:

```bash
make test
make preflight
make local-sanity
```

This creates a local validation bundle under `outputs/berth1/local_validation_bundle.zip`.
