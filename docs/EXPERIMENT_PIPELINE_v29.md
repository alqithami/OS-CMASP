# Berth-1-Conflict experiment pipeline v29

This protocol is designed to produce the first paper-critical result without changing the solver. The only thing that changes across conditions is claim-state semantics.

## 0. Repository setup

```bash
git clone https://github.com/alqithami/OS-CMASP.git
cd OS-CMASP
git checkout -b experiment/berth1-prelock-v29

python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
make test
```

## 1. Apply and review the pre-run lock

Before any results are produced, review and commit the following locked objects:

- `chi_B1(x)`: visible context excludes `ready`, `crane_ok`, `eta_on_time`, and `weather_safe`.
- Dominance table `D`: observer priority by proposition family.
- Freshness windows and tie rules.
- Six ablation conditions:
  - `provenance_preserving`
  - `provenance_erased`
  - `random_label_placebo`
  - `labels_without_gating`
  - `oracle_visible_state`
  - `benign_agreement`
- Replay CSV schema.
- Metric hierarchy and go/no-go criteria.

Commit the lock before any run:

```bash
git add docs/PRE_RUN_LOCK.md configs/berth1_locked_v29.json data/templates/berth1_replay_template.csv
git commit -m "Lock Berth-1-Conflict pre-run protocol"
```

## 2. Run contract preflight only

```bash
make preflight
```

Expected output:

- `artifacts/preflight/berth1_preflight_manifest.json`

Preflight checks:

- no visible-context leakage;
- scenario coverage;
- condition set frozen;
- dominance-table version recorded;
- solver version recorded.

## 3. Export maritime replay to CSV

Export a small replay extract from the maritime twin into the schema in:

```text
data/templates/berth1_replay_template.csv
```

Minimum required columns:

```text
seed,t,ready,scenario,prop,value,observer,situation
```

Recommended full columns:

```text
seed,t,ready,crane_ok,eta_on_time,weather_safe,scenario,
queue_state,weather_regime,disruption_family,vessel_class,operating_mode,
time_bucket,berth_slot,eta_bin,prop,value,observer,situation,
credibility,timestamp,provenance
```

Each `(seed,t)` pair should have multiple claim rows. The latent booleans (`ready`, `crane_ok`, `eta_on_time`, `weather_safe`) are evaluation labels and must not be included in `chi_B1(x)`.

Suggested first replay size:

- 20-50 seeds;
- 20-100 steps per seed;
- at least four scenario families: authority conflict, freshness conflict, context conflict, human override;
- one benign agreement block.

## 4. Run the fixed-solver ablation

```bash
scripts/run_berth1_replay.sh path/to/twin_replay_claims.csv outputs/berth1/twin_v1
```

This runs preflight first, then the fixed-solver ablation, then writes a Markdown report.

Expected outputs:

```text
outputs/berth1/twin_v1.csv
outputs/berth1/twin_v1_summary.csv
outputs/berth1/twin_v1_paired.csv
outputs/berth1/twin_v1_diagnostics.json
outputs/berth1/twin_v1.manifest.json
outputs/berth1/twin_v1.preflight_manifest.json
outputs/berth1/twin_v1_report.md
outputs/berth1/twin_v1_regret_bar.png    # optional, if matplotlib is installed
```

## 5. Package results for sharing

```bash
scripts/package_results.sh outputs/berth1/twin_v1 outputs/berth1/twin_v1_results.zip
```

Share the zip plus the replay CSV only if allowed. If the replay cannot be shared, share only:

- manifest JSONs;
- summary CSV;
- paired-delta CSV;
- diagnostics JSON;
- generated Markdown report;
- replay hash from the manifest.

## 6. Primary interpretation

The first paper-critical table is `*_paired.csv`.

The key contrast is:

```text
provenance_erased - provenance_preserving
```

The process-semantics claim is supported if:

1. `provenance_preserving` has low regret and zero or near-zero safety violations;
2. `provenance_erased` has higher paired regret under the same replay bank;
3. `labels_without_gating` exposes safety failures or false certifications;
4. `oracle_visible_state` closes the gap;
5. `benign_agreement` has low overhead.

If the paired delta is absent, do not change the solver. First inspect whether the replay actually contains a provenance-active regime: same visible context, conflicting claims, and different admissibility under dominance.

## 7. Paper figure recommendation

The first figure should not be a learning curve. It should be a process-semantics ablation figure:

- x-axis: condition;
- y-axis: mean regret or cumulative zero-violation regret;
- paired confidence intervals over seeds;
- annotate safety violations separately.

The first table should include:

- mean regret;
- safety violations;
- waiting cost;
- intervention cost;
- false certifications;
- paired delta vs provenance-preserving.
