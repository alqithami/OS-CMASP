# Repository architecture

## Manuscript

`manuscript/main.tex` and `manuscript/refs.bib` contain the academic draft.

## Scaffold

`src/os_cmasp/berth1_conflict.py` contains the contract-first benchmark scaffold.

## Data templates

`data/templates/berth1_replay_template.csv` defines the claim-level twin replay schema.

## Configs

`configs/run_manifest_template.json` is the manifest schema for preflight and replay-backed runs.

## Tests

`tests/` checks the leakage guard, replay template, paired-bank contract, and ablation-row structure.

## Outputs

`outputs/`, `results/`, and raw replay exports are intentionally ignored by Git.
