# Complete GitHub repository pipeline

This document gives the operational pipeline for turning the OS-CMASP package into a controlled GitHub repository.

## 1. Repository identity

Recommended repository name:

```text
os-cmasp
```

Recommended short description:

```text
Observer-Situation Constrained Multi-Agent Simulation Processes for control under fragmented truth.
```

The repository should be presented as a reproducibility package for a process-class manuscript, not as a larger CH-MARL stack.

## 2. Local initialization

```bash
git init
git checkout -b main
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
make test
make preflight
git add .
git commit -m "Initial OS-CMASP manuscript and pre-run scaffold"
```

## 3. Create the remote repository

With GitHub CLI:

```bash
gh repo create <org-or-user>/os-cmasp \
  --private \
  --source=. \
  --remote=origin \
  --push
```

Recommended initial visibility is private until authorship, licensing, replay-data policy, and pre-run lock are approved.

## 4. Branching model

Use a minimal branch model:

- `main`: protected, release-ready manuscript/scaffold state.
- `paper/*`: manuscript revisions.
- `scaffold/*`: benchmark or code changes.
- `replay/*`: replay-schema or manifest changes. Do not commit raw private replay exports.

## 5. Branch protection

Protect `main` with:

- pull request required before merge;
- at least one approving review;
- required checks: `CI / python-contract`, `Paper / build-paper`;
- disallow force pushes;
- require conversation resolution;
- require branches to be up to date before merge.

## 6. GitHub Actions

The repository includes three workflows.

### `ci.yml`

Runs Python compilation, unit tests, and scaffold preflight. It uploads the CI preflight manifest as an artifact.

### `paper.yml`

Builds the LaTeX manuscript from `manuscript/main.tex` and uploads the resulting PDF artifact.

### `release.yml`

On a version tag such as `v0.1.0`, builds the manuscript, creates a repository bundle, and opens a GitHub Release with the PDF and package zip.

## 7. Pre-run lock workflow

Before any local or twin-backed benchmark result is added:

1. Update `docs/PRE_RUN_LOCK.md`.
2. Confirm `configs/run_manifest_template.json` matches the locked condition set.
3. Confirm `data/templates/berth1_replay_template.csv` is the schema expected from the twin export.
4. Run:

```bash
make test
make preflight
```

5. Commit only the lock and manifest changes.
6. Run replay locally or in a controlled private branch.
7. Commit only approved summaries, plots, and manifests. Do not commit raw private replay data.

## 8. Experiment outputs

Output directory convention:

```text
outputs/<YYYYMMDD>_<experiment_slug>/
```

Commit only:

- manifest JSON;
- summary CSV;
- paired-delta CSV;
- final figures;
- a short interpretation note.

Keep out of Git:

- raw twin replay exports;
- full row-level replay traces if they contain operationally sensitive information;
- local caches;
- ad hoc synthetic outputs.

## 9. Release pipeline

Before tagging:

```bash
make test
make preflight
make paper
scripts/package_release.sh v0.1.0
git status
```

Then:

```bash
git tag -a v0.1.0 -m "OS-CMASP pre-run manuscript and scaffold"
git push origin main --tags
```

The release workflow builds the manuscript and publishes release artifacts.

## 10. Governance checklist before public release

- Replace `CITATION.cff` placeholders.
- Decide code and manuscript licenses.
- Confirm whether CH-MARL/IBM project names can be used publicly.
- Remove or anonymize any operationally sensitive replay examples.
- Confirm all arXiv/preprint references are appropriate for the target venue.
- Decide whether the reference PDF should remain committed or be release-only.

## 11. Suggested issue labels

- `theory`
- `formal-model`
- `benchmark`
- `replay-schema`
- `paper-edit`
- `ci`
- `needs-decision`
- `do-not-run-yet`

## 12. Minimal go/no-go gate

Do not scale to full maritime twin replay until `Berth-1-Conflict` shows a clean paired separation under the frozen solver between:

- `provenance_preserving`
- `provenance_erased`
- `random_label_placebo`
- `labels_without_gating`
- `oracle_visible_state`
- `benign_agreement`
