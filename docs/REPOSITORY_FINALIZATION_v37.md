# Repository finalization v37

This document records the current repository state before moving from software validation to the maritime-twin promotion run.

## Installability

The repository is installable because it contains:

- `pyproject.toml` with a setuptools build backend;
- a `src/` package layout;
- package discovery under `src`;
- command-line entry points for `berth1-conflict` and `berth1-replay-adapter`;
- a `Makefile` with test, preflight, local-sanity, and promotion-demo targets.

Validation command:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
make test
make preflight
make local-sanity
make promotion-demo
```

## Current promotion path

The current path to paper-relevant evidence is:

1. G0: local software sanity;
2. G1: raw twin export inspection;
3. G2: Berth-1 twin replay under the frozen six-condition ablation;
4. G3: pilot twin slices over operational blocks;
5. G4: full maritime digital-twin campaign.

## Repository status

The repository is ready for the next operational step: a G2 run using a real maritime-twin export.

The repository is not claiming that the locked synthetic replay is maritime evidence. Synthetic replay remains a software sanity artifact only.

## Remaining non-blocking item

No open-source license has been selected yet. This does not block private validation or controlled public visibility, but it should be resolved before any public release, archival deposit, or external reuse request.
