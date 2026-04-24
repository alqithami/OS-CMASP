# Paper Update Notes v34

v34 adds the missing bridge between the minimal benchmark and the larger maritime digital twin.

## Added to the paper

- A stage-gated promotion protocol from Berth-1 to full twin deployment.
- A clear definition of what has already been achieved: software sanity, not maritime evidence.
- A no-manual data path for real twin evidence.
- A table of promotion gates G0-G4.
- A concrete porting map from twin subsystems to proposition families and observer sources.
- A warning that failed promotion should narrow the active regime rather than motivate a deeper controller stack.

## Added to the repo

- `scripts/run_maritime_twin_gate.sh`
- `scripts/write_promotion_gate_report.py`
- `scripts/run_promotion_demo.sh`
- `docs/MARITIME_TWIN_PROMOTION_PROTOCOL_v34.md`
- `docs/COMPLETION_PLAN_v34.md`

The new gate script inspects, converts, runs, packages, and writes a promotion report from a twin wide CSV without manual replay construction.
