# OS-CMASP: Observer-Situation Constrained Multi-Agent Simulation Processes

This repository contains the OS-CMASP manuscript, the Berth-1-Conflict fixed-solver scaffold, and the pre-run experiment protocol.

The repository identity is process semantics for control under fragmented operational truth. The implementation witness keeps the solver fixed and varies only claim-state semantics across ablations.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
make test
make preflight
```

## Build the paper

```bash
make paper
```

The compiled PDF is produced under `manuscript/main.pdf`.

## Run a replay-backed ablation after pre-run lock

```bash
scripts/run_berth1_replay.sh path/to/twin_replay_claims.csv outputs/berth1/twin_v1
scripts/package_results.sh outputs/berth1/twin_v1 outputs/berth1/twin_v1_results.zip
```

See `docs/EXPERIMENT_PIPELINE_v29.md` for the complete protocol.
