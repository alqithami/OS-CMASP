# Repository update status v35

This file records the repository-side update made through the GitHub connector.

## Branch

`pipeline/v34-maritime-twin-promotion`

## Purpose

The repository already contained the v34 staged promotion path from `Berth-1-Conflict` to maritime-digital-twin replay. This update adds a reviewer/operator-facing runbook that turns the promotion path into concrete gates, commands, pass criteria, failure interpretation, and no-manual replay rules.

## Files changed

- `docs/MARITIME_TWIN_PROMOTION_RUNBOOK_v35.md`
- `README.md`
- `docs/REPO_UPDATE_STATUS_v35.md`

## Why this matters

The manuscript and repository now separate three things that were easy to conflate:

1. software sanity evidence;
2. first paper-relevant Berth-1 twin replay evidence;
3. later full maritime-digital-twin campaign evidence.

The update preserves the central OS-CMASP constraint: scale by replacing the replay source under a frozen ablation, not by adding controller layers.

## Next operator action

After the PR is merged, run:

```bash
make test
make preflight
make local-sanity
make promotion-demo
```

Then move to a real twin wide export and run:

```bash
scripts/run_maritime_twin_gate.sh \
  data/raw/my_twin_export.csv \
  outputs/berth1/twin_gate_v1
```
