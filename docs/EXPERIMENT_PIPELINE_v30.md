# OS-CMASP v30 experiment pipeline

This pipeline has three modes. Do not skip directly to replay unless you have an actual replay CSV.

## 0. Setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Use Python 3.10 or newer. Python 3.12 is fine.

## 1. Contract checks only

```bash
make test
make preflight
```

This writes:

```text
artifacts/preflight/berth1_preflight_manifest.json
```

Preflight is not evidence. It only confirms that the scaffold can validate the locked contract.

## 2. Optional synthetic smoke test

Run this only to check that the code path writes outputs correctly. It is not maritime evidence.

```bash
make synthetic-smoke
```

The script first runs a small preflight and then a deliberately small synthetic run (80 horizon steps, 4 seeds). This keeps it fast and avoids confusing a software smoke test with paper evidence.

or explicitly:

```bash
scripts/run_berth1_synthetic_smoke.sh outputs/berth1/synthetic_smoke
scripts/package_results.sh outputs/berth1/synthetic_smoke outputs/berth1/synthetic_smoke_results.zip
```

Share the zip only if the goal is debugging the pipeline.

## 3. Create the replay CSV template

```bash
scripts/write_berth1_replay_template.sh data/replay/berth1_replay_template.csv
```

Replace the template rows with a real export from the maritime twin. The minimum required columns are:

```text
seed,t,ready,scenario,prop,value,observer,situation
```

The recommended full schema is in `data/templates/berth1_replay_template.csv` and should be copied into `data/replay/` for local runs.

## 4. Real replay run

Do not run with `path/to/twin_replay_claims.csv`; that is only a placeholder. First check that the file exists:

```bash
REPLAY=data/replay/twin_replay_claims.csv
test -f "$REPLAY" || { echo "Missing replay CSV: $REPLAY"; exit 1; }
```

Then run:

```bash
scripts/run_berth1_replay.sh "$REPLAY" outputs/berth1/twin_v1
scripts/package_results.sh outputs/berth1/twin_v1 outputs/berth1/twin_v1_results.zip
```

## 5. Files to share back

Share the zip and, if useful, the individual report:

```text
outputs/berth1/twin_v1_results.zip
outputs/berth1/twin_v1_report.md
```

The zip contains:

```text
outputs/berth1/twin_v1.csv
outputs/berth1/twin_v1_summary.csv
outputs/berth1/twin_v1_paired.csv
outputs/berth1/twin_v1_diagnostics.json
outputs/berth1/twin_v1.manifest.json
outputs/berth1/twin_v1.preflight_manifest.json
outputs/berth1/twin_v1_report.md
```

## 6. First diagnostic to inspect

The first paper-critical quantity is the paired delta:

```text
provenance_erased - provenance_preserving
```

The desired pattern is:

- `provenance_preserving`: low regret and zero or near-zero safety violations;
- `provenance_erased`: higher paired regret or a safety-service burden;
- `random_label_placebo`: does not close the gap;
- `labels_without_gating`: reveals safety/certification risk;
- `oracle_visible_state`: closes the gap;
- `benign_agreement`: low overhead.

## 7. What the earlier error meant

The command

```bash
scripts/run_berth1_replay.sh path/to/twin_replay_claims.csv outputs/berth1/twin_v1
```

failed because `path/to/twin_replay_claims.csv` was a placeholder, not a real file. v30 scripts now catch this before Python opens the file and print a direct instruction.
