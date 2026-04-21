# v31 update package

This package fixes the replay pipeline and revises the paper text accordingly.

Apply the changed files to the repository, then run:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .

make test
make preflight
scripts/run_berth1_locked_replay_demo.sh outputs/berth1/locked_replay_demo
```

The command above requires no manual CSV editing and should produce:

```text
outputs/berth1/locked_replay_demo_results.zip
```

For a wide twin export, run:

```bash
scripts/build_berth1_replay_from_wide.sh data/raw/my_twin_export.csv data/replay/twin_replay_claims.csv
scripts/run_berth1_replay.sh data/replay/twin_replay_claims.csv outputs/berth1/twin_v1
scripts/package_results.sh outputs/berth1/twin_v1 outputs/berth1/twin_v1_results.zip
```
