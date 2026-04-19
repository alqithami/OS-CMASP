# Next step after v29

1. Open a manuscript-only PR with v29 `manuscript/main.tex` and `manuscript/refs.bib`.
2. Open a separate protocol PR with `docs/EXPERIMENT_PIPELINE_v29.md`, `configs/berth1_locked_v29.json`, and the scripts.
3. Review the pre-run lock before any local result generation.
4. Export a small maritime replay extract in the template schema.
5. Run `scripts/run_berth1_replay.sh` and share the result package.

Do not scale to the full maritime twin until the fixed-solver one-berth replay separates provenance-preserving from provenance-erased semantics.
