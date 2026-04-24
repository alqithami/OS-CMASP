# Completion Plan (v34)

## Milestone 1 - Merge pipeline and paper bridge

Apply v34 to the GitHub repo and run:

```bash
python -m pip install -e .
make test
make preflight
make local-sanity
make promotion-demo
```

Expected: no errors. `promotion-demo` is a pipeline exercise using the tiny example file; it is not expected to be paper evidence.

## Milestone 2 - Export a real twin wide CSV

Produce a one-row-per-step export with at least:

```text
seed,t,ready,scenario
```

Recommended additional columns:

```text
crane_ok,eta_on_time,weather_safe,
queue_state,weather_regime,disruption_family,vessel_class,
operating_mode,time_bucket,berth_slot,eta_bin
```

No manual replay editing is needed.

## Milestone 3 - Run the first paper-relevant gate

```bash
scripts/run_maritime_twin_gate.sh \
  data/raw/my_twin_export.csv \
  outputs/berth1/twin_gate_v1
```

Share back:

```text
outputs/berth1/twin_gate_v1/twin_gate_results.zip
outputs/berth1/twin_gate_v1/twin_gate_promotion_report.md
outputs/berth1/twin_gate_v1/twin_gate_promotion_gate.json
```

## Milestone 4 - Decide whether to scale

Scale to a larger twin slice only if the promotion report passes. If it fails, do not tune the solver; inspect the failing gate criterion.

## Milestone 5 - Larger twin slice

Run the same gate on scenario-blocked exports:

```bash
scripts/run_maritime_twin_gate.sh data/raw/twin_weather_blocks.csv outputs/berth1/twin_weather_blocks
scripts/run_maritime_twin_gate.sh data/raw/twin_crane_blocks.csv outputs/berth1/twin_crane_blocks
scripts/run_maritime_twin_gate.sh data/raw/twin_eta_blocks.csv outputs/berth1/twin_eta_blocks
```

Then aggregate by block key and report paired deltas.
