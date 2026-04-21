# v32 Packaging Fix

The v31 update bundle was a partial copy intended to be applied into the repository. It omitted root-level project files such as `pyproject.toml`, `Makefile`, and tests. Installing directly from that partial folder produced:

```text
does not appear to be a Python project: neither 'setup.py' nor 'pyproject.toml' found
```

v32 fixes this by shipping a complete installable repository package with:

- `pyproject.toml`
- `Makefile`
- `src/os_cmasp/berth1_conflict.py`
- `src/os_cmasp/berth1_replay_adapter.py`
- complete scripts for preflight, replay demo, wide conversion, replay run, packaging, and reporting
- unit tests for the scaffold and replay adapter
- manuscript sources and reference PDF

Recommended command:

```bash
unzip os_cmasp_repo_v32_full.zip
cd os_cmasp_repo_v32_full
python -m pip install -e .
make test
make preflight
scripts/run_berth1_locked_replay_demo.sh outputs/berth1/locked_replay_demo
```
