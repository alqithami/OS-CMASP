# Maritime twin promotion runbook v35

This runbook converts the phrase "only after the minimal benchmark works" into an operational promotion sequence.

## Current status

The repository already contains the Berth-1-Conflict scaffold, no-manual replay adapters, and a staged promotion path from minimal benchmark to maritime-digital-twin replay. The latest verified software sanity run should be treated as **software validation only**, not maritime evidence.

The locked synthetic sanity pattern to preserve is:

- `provenance_preserving`: low/zero regret, zero safety violations;
- `provenance_erased`: safe but service-burdensome;
- `random_label_placebo`: should not close the gap and may expose false certification;
- `labels_without_gating`: should expose why admissibility/certification is needed;
- `oracle_visible_state`: should close the gap;
- `benign_agreement`: should have low overhead.

## Gate sequence

### G0: local software sanity

Purpose: verify installation, preflight, fixed condition set, and packaging.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .

make test
make preflight
make local-sanity
```

Expected output: a complete local sanity bundle under `outputs/berth1/`.

Evidence status: software validation only.

### G1: raw twin export inspection

Purpose: check whether a one-row-per-step twin export can be converted without hand editing.

The minimum wide-export columns are:

```text
seed,t,ready,scenario
```

Recommended columns are:

```text
crane_ok,eta_on_time,weather_safe,
queue_state,weather_regime,disruption_family,vessel_class,
operating_mode,time_bucket,berth_slot,eta_bin
```

Run:

```bash
scripts/inspect_berth1_wide_export.sh \
  data/raw/my_twin_export.csv \
  data/raw/my_twin_export.inspect_report.json
```

If the report says `convertible_without_manual_rename: false`, do not hand-edit replay rows. Extend the alias table or modify the exporter.

Evidence status: interface validation only.

### G2: Berth-1 twin replay

Purpose: replace synthetic claim generation with declared twin replay while preserving the frozen solver and the six frozen ablation conditions.

Run the one-command gate:

```bash
scripts/run_maritime_twin_gate.sh \
  data/raw/my_twin_export.csv \
  outputs/berth1/twin_gate_v1
```

For canonical long-form one-row-per-claim replay:

```bash
scripts/run_maritime_twin_gate.sh \
  data/raw/my_claim_replay.csv \
  outputs/berth1/twin_gate_v1 \
  --long-form
```

Share these files for review:

```text
outputs/berth1/twin_gate_v1/twin_gate_results.zip
outputs/berth1/twin_gate_v1/twin_gate_promotion_report.md
outputs/berth1/twin_gate_v1/twin_gate_promotion_gate.json
```

Pass criterion:

- provenance-preserving separates from provenance-erased and random-label placebo;
- provenance-preserving remains zero-violation or near-zero-violation;
- oracle visible-state closes the relevant gap;
- benign agreement has low overhead;
- the diagnostics do not indicate visible-context leakage.

Evidence status: first paper-relevant empirical evidence.

### G3: pilot twin slices

Purpose: test whether the G2 effect is stable across declared operational blocks.

Recommended blocks:

- authority conflict;
- freshness conflict;
- context conflict;
- human override;
- crane disruption;
- ETA conflict;
- weather disruption.

Each block should be run with the same frozen condition set and reported with paired deltas.

Evidence status: pilot twin evidence.

### G4: full twin campaign

Purpose: scale from Berth-1 twin replay to the larger maritime digital twin.

Only start this after G2 and at least one G3 block pass. The full campaign adds calibrated operational metrics:

- emissions/idling proxy;
- service disparity;
- intervention spend;
- contradiction half-life;
- false-certification rate.

Evidence status: main empirical study.

## Non-negotiable controls

- Do not change solver identity across conditions.
- Do not change the six-condition ablation set after observing results.
- Do not hand-edit canonical replay rows.
- Do not treat synthetic replay as maritime evidence.
- Do not add controller depth to rescue a failed G2 run.
- Do not scale to full twin before the minimal twin replay separates under the frozen solver.

## Interpretation of failures

A failed G2 run does not automatically falsify OS-CMASP. It narrows the active regime. Check, in order:

1. Did the replay contain actual observer--situation conflict?
2. Did visible context accidentally leak hidden readiness/safety?
3. Did the dominance order fail to match the operational authority structure?
4. Did freshness windows erase the intended conflict?
5. Did the replay contain mostly benign agreement?

Only after these checks should the benchmark or formal model be revised.