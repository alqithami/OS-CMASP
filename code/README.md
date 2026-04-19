# Code entry points

The maintained CLI lives in `src/os_cmasp/berth1_conflict.py` and can be invoked after installation as:

```bash
python -m os_cmasp.berth1_conflict --mode preflight --manifest preflight_manifest.json
```

The file `code/berth1_conflict.py` is a thin compatibility wrapper for earlier drafts. Keep new implementation work in `src/os_cmasp/`.
