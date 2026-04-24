# v34 Update: Promotion Path to Maritime Digital Twin

This update answers: what must happen after the minimal benchmark works?

## Main idea

Promote OS-CMASP by changing the replay source, not the solver:

1. G0: software sanity on locked synthetic replay.
2. G1: inspect a raw twin wide export.
3. G2: run Berth-1 on a declared twin replay.
4. G3: run a pilot twin slice by block key.
5. G4: run full twin campaign and metric lifts.

## Apply to repo

```bash
git checkout -b pipeline/v34-maritime-twin-promotion
UPDATE=/path/to/os_cmasp_repo_v34_full

cp "$UPDATE/manuscript/main.tex" manuscript/main.tex
cp "$UPDATE/manuscript/refs.bib" manuscript/refs.bib
cp "$UPDATE/artifacts/reference/os_cmasp_expanded_academic_v34.pdf" artifacts/reference/

cp "$UPDATE/src/os_cmasp/berth1_conflict.py" src/os_cmasp/berth1_conflict.py
cp "$UPDATE/src/os_cmasp/berth1_replay_adapter.py" src/os_cmasp/berth1_replay_adapter.py
cp "$UPDATE/scripts/"*.sh scripts/
cp "$UPDATE/scripts/summarize_berth1_results.py" scripts/
cp "$UPDATE/scripts/write_promotion_gate_report.py" scripts/
chmod +x scripts/*.sh scripts/*.py

cp "$UPDATE/docs/MARITIME_TWIN_PROMOTION_PROTOCOL_v34.md" docs/
cp "$UPDATE/docs/COMPLETION_PLAN_v34.md" docs/
cp "$UPDATE/docs/PAPER_UPDATE_NOTES_v34.md" docs/
mkdir -p data/contracts
cp "$UPDATE/data/contracts/berth1_twin_export_contract_v34.json" data/contracts/
cp "$UPDATE/Makefile" Makefile
cp "$UPDATE/pyproject.toml" pyproject.toml
cp "$UPDATE/README.md" README.md

git add .
git commit -m "Add maritime twin promotion protocol and gate pipeline"
git push -u origin pipeline/v34-maritime-twin-promotion
```

## Commands to run

```bash
python -m pip install -e .
make test
make preflight
make local-sanity
make promotion-demo
```

For real twin data:

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
