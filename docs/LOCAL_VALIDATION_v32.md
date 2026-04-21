# v32 Local Validation Notes

This package was checked as a complete repository package. The important correction versus v31 is that the root now contains `pyproject.toml` and `Makefile`, so `python -m pip install -e .` must be run from this directory, not from a partial update bundle.

Validation performed in the build environment:

```bash
PYTHONPATH=src python -S -m unittest discover -s tests -v
PYTHONPATH=src PYTHON='python -S' scripts/run_berth1_locked_replay_demo.sh outputs/berth1/locked_replay_demo
PYTHONPATH=src PYTHON='python -S' make wide-example
```

The unit tests passed. The locked replay demo produced the expected active-regime scaffold pattern. The included wide-example converter also ran end-to-end, but its toy four-step dataset is intentionally too small to satisfy all separation criteria. It is a converter smoke test, not evidence.

On a normal local virtual environment, use the standard commands without `PYTHONPATH` or `python -S`:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
make test
make preflight
scripts/run_berth1_locked_replay_demo.sh outputs/berth1/locked_replay_demo
```
