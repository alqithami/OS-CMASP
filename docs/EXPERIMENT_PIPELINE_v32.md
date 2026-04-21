# v32 Experiment Pipeline

This version fixes the v31 packaging problem by making the distribution root an installable Python project. The previous `os_cmasp_repo_update_v31_clean` folder was a partial update bundle and therefore had no `pyproject.toml`; v32 is a full repository package.

## 1. Install from the v32 repository root

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

If `pip install -e .` says no `pyproject.toml` was found, you are not in the v32 repository root. Run:

```bash
pwd
ls pyproject.toml Makefile src/os_cmasp/berth1_conflict.py
```

All three paths must exist.

## 2. Contract checks

```bash
make test
make preflight
```

## 3. Replay-path check without manual CSV editing

```bash
scripts/run_berth1_locked_replay_demo.sh outputs/berth1/locked_replay_demo
```

This writes `data/replay/berth1_locked_synthetic_replay.csv`, runs the replay pipeline, and packages outputs. It is not maritime evidence.

## 4. Example wide-export conversion

```bash
make wide-example
```

This uses `data/examples/berth1_wide_example.csv` to test the converter.

## 5. Actual twin run

Export a wide CSV from the twin with at least:

```text
seed,t,ready,scenario
```

Recommended columns:

```text
crane_ok,eta_on_time,weather_safe,
queue_state,weather_regime,disruption_family,vessel_class,
operating_mode,time_bucket,berth_slot,eta_bin
```

Run:

```bash
scripts/build_berth1_replay_from_wide.sh data/raw/my_twin_export.csv data/replay/twin_replay_claims.csv
scripts/run_berth1_replay.sh data/replay/twin_replay_claims.csv outputs/berth1/twin_v1
scripts/package_results.sh outputs/berth1/twin_v1 outputs/berth1/twin_v1_results.zip
```

Share back:

```text
outputs/berth1/twin_v1_results.zip
outputs/berth1/twin_v1_report.md
```

## 6. What not to run

Do not run placeholder paths such as:

```bash
scripts/run_berth1_replay.sh path/to/twin_replay_claims.csv outputs/berth1/twin_v1
```

The script now rejects missing files before Python execution, but the placeholder still has no data behind it.
