# OS-CMASP: Observer-Situation Constrained Multi-Agent Simulation Processes

This repository packages the manuscript, executable Berth-1-Conflict scaffold, and pre-run protocol for the OS-CMASP project.

The repository identity is **process semantics for control under fragmented truth**. The implementation witness keeps the solver fixed and changes only the claim-state semantics across ablations. This is deliberately not a controller-stack repository.

## Repository status

- Manuscript: expanded academic draft in `manuscript/`.
- Reference PDF: `artifacts/reference/os_cmasp_expanded_academic_v26.pdf`.
- Executable scaffold: `src/os_cmasp/berth1_conflict.py`.
- Replay template: `data/templates/berth1_replay_template.csv`.
- Pre-run lock: `docs/PRE_RUN_LOCK.md`.
- No benchmark evidence is committed. Preflight is the default.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
make test
make preflight
```

The default scaffold mode is preflight. It validates the replay/schema/ablation contract and writes no result CSVs.

## Build the manuscript

```bash
make paper
```

This runs `latexmk` inside `manuscript/`. Install a LaTeX distribution with `latexmk` and `biber` first.

## Pre-run discipline

Before any replay-backed experiment:

1. Freeze the visible-context map `chi_B1(x)`.
2. Freeze the proposition-family dominance table `D`.
3. Freeze freshness windows and tie rules.
4. Freeze the six ablation conditions.
5. Freeze the replay CSV schema.
6. Run only preflight.
7. Run the paired fixed-solver ablation on a small replay extract.
8. Report paired deltas before aggregate plots.

See `docs/PRE_RUN_LOCK.md` and `docs/GITHUB_REPOSITORY_PIPELINE.md`.

## Running replay after lock

```bash
python -m os_cmasp.berth1_conflict \
  --mode run \
  --replay-csv path/to/twin_replay_claims.csv \
  --out-prefix outputs/twin_replay_v1 \
  --manifest outputs/twin_replay_v1.manifest.json
```

Generated outputs are ignored by Git. Commit only manifests, summary tables, and figures after the pre-run lock has been reviewed.

## Citation and licensing

`CITATION.cff` contains placeholders. Replace authorship, DOI, repository URL, and release date before public release. Licensing is intentionally left as an owner decision; see `docs/LICENSING_DECISION.md`.
