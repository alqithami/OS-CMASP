# OS-CMASP

Observer-Situation Constrained Multi-Agent Simulation Process (OS-CMASP): manuscript, Berth-1-Conflict fixed-solver scaffold, no-manual replay adapters, and a staged promotion path to maritime-digital-twin replay.

This package is a **complete installable repository**. In practical terms, this means the repository root contains `pyproject.toml`, a `src/` Python package layout, command-line entry points, a `Makefile`, scripts, tests, manuscript sources, local validation utilities, and the promotion-gate pipeline.

## What "installable" means

From the repository root, this command installs the local package in editable mode:

```bash
python -m pip install -e .
```

Editable mode means changes to files under `src/os_cmasp/` are reflected immediately without reinstalling. The configured command-line entry points are:

```bash
berth1-conflict
berth1-replay-adapter
```

The same functionality is also available with module execution:

```bash
python -m os_cmasp.berth1_conflict --help
python -m os_cmasp.berth1_replay_adapter --help
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .

make test
make preflight
```

## Local software sanity

This validates the executable scaffold. It is not maritime-twin evidence.

```bash
make local-sanity
```

## Promotion demo

This runs the end-to-end promotion gate on the tiny example wide export. It verifies the gate pipeline, not the paper claim.

```bash
make promotion-demo
```

## First paper-relevant twin run

Export a one-row-per-step CSV from the maritime twin. Minimum columns:

```text
seed,t,ready,scenario
```

Recommended columns:

```text
crane_ok,eta_on_time,weather_safe,
queue_state,weather_regime,disruption_family,vessel_class,
operating_mode,time_bucket,berth_slot,eta_bin
```

Then run the no-manual promotion gate:

```bash
scripts/run_maritime_twin_gate.sh \
  data/raw/my_twin_export.csv \
  outputs/berth1/twin_gate_v1
```

For a canonical one-row-per-claim replay CSV instead of a wide export:

```bash
scripts/run_maritime_twin_gate.sh \
  data/raw/my_claim_replay.csv \
  outputs/berth1/twin_gate_v1 \
  --long-form
```

Share these outputs:

```text
outputs/berth1/twin_gate_v1/twin_gate_results.zip
outputs/berth1/twin_gate_v1/twin_gate_promotion_report.md
outputs/berth1/twin_gate_v1/twin_gate_promotion_gate.json
```

## Promotion protocol

See:

- `docs/MARITIME_TWIN_PROMOTION_RUNBOOK_v36.md` — current operational gate-by-gate runbook.
- `docs/MARITIME_TWIN_PROMOTION_RUNBOOK_v35.md` — prior detailed runbook retained for traceability.
- `docs/MARITIME_TWIN_PROMOTION_PROTOCOL_v34.md`
- `docs/COMPLETION_PLAN_v34.md`
- `docs/TWIN_EXPORT_GUIDE_v33.md`

The promotion gates are:

1. G0 software sanity;
2. G1 twin-export inspection;
3. G2 Berth-1 twin replay;
4. G3 pilot twin slice;
5. G4 full twin campaign.

Do not scale to the full maritime twin by adding controller layers. Scale by preserving the frozen ablation and replacing the replay source.
