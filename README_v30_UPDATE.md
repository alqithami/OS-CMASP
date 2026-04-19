# OS-CMASP v30 update package

This package revises the main paper Sections 4--12 and hardens the Berth-1 experiment pipeline.

## Apply as a GitHub branch

```bash
git checkout -b paper/v30-main-core-and-run-pipeline
cp /path/to/os_cmasp_repo_update_v30/manuscript/main.tex manuscript/main.tex
cp /path/to/os_cmasp_repo_update_v30/manuscript/refs.bib manuscript/refs.bib
cp /path/to/os_cmasp_repo_update_v30/os_cmasp_expanded_academic_v30.pdf artifacts/reference/os_cmasp_expanded_academic_v30.pdf
cp /path/to/os_cmasp_repo_update_v30/src/os_cmasp/berth1_conflict.py src/os_cmasp/berth1_conflict.py
cp /path/to/os_cmasp_repo_update_v30/scripts/*.sh scripts/
cp /path/to/os_cmasp_repo_update_v30/scripts/summarize_berth1_results.py scripts/
cp /path/to/os_cmasp_repo_update_v30/docs/EXPERIMENT_PIPELINE_v30.md docs/
cp /path/to/os_cmasp_repo_update_v30/docs/PAPER_REVISION_NOTES_v30.md docs/

git add manuscript/main.tex manuscript/refs.bib artifacts/reference/os_cmasp_expanded_academic_v30.pdf \
  src/os_cmasp/berth1_conflict.py scripts docs/EXPERIMENT_PIPELINE_v30.md docs/PAPER_REVISION_NOTES_v30.md

git commit -m "Strengthen main-paper core and harden Berth-1 run pipeline"
git push -u origin paper/v30-main-core-and-run-pipeline
```

## Safe run sequence

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
make test
make preflight
```

Optional pipeline smoke test:

```bash
scripts/run_berth1_synthetic_smoke.sh outputs/berth1/synthetic_smoke
scripts/package_results.sh outputs/berth1/synthetic_smoke outputs/berth1/synthetic_smoke_results.zip
```

Real replay, after an actual CSV exists:

```bash
scripts/write_berth1_replay_template.sh data/replay/berth1_replay_template.csv
# replace template rows with real exported replay rows
REPLAY=data/replay/twin_replay_claims.csv
test -f "$REPLAY" || { echo "Missing replay CSV: $REPLAY"; exit 1; }
scripts/run_berth1_replay.sh "$REPLAY" outputs/berth1/twin_v1
scripts/package_results.sh outputs/berth1/twin_v1 outputs/berth1/twin_v1_results.zip
```
