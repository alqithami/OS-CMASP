# Berth-1-Conflict Report: `outputs/berth1/locked_replay_demo`

## Summary by condition

| condition | n | mean_regret | safety_violations | waiting_cost | intervention_cost | false_certifications |
|---|---|---|---|---|---|---|
| provenance_preserving | 320 | 0 | 0 | 0 | 181 | 0 |
| provenance_erased | 320 | 0.434375 | 0 | 139 | 320 | 0 |
| random_label_placebo | 320 | 0.3625 | 59 | 57 | 179 | 59 |
| labels_without_gating | 320 | 0.565625 | 181 | 0 | 0 | 0 |
| oracle_visible_state | 320 | 0 | 0 | 0 | 0 | 0 |
| benign_agreement | 320 | 0 | 0 | 0 | 0 | 0 |

## Paired deltas vs provenance_preserving

| condition | metric | mean_delta_vs_provenance_preserving | ci95_low | ci95_high |
|---|---|---|---|---|
| benign_agreement | regret | 0 | 0 | 0 |
| benign_agreement | safety_violation | 0 | 0 | 0 |
| benign_agreement | waiting_cost | 0 | 0 | 0 |
| benign_agreement | intervention_cost | -0.565625 | -0.625114 | -0.506136 |
| benign_agreement | false_certification | 0 | 0 | 0 |
| labels_without_gating | regret | 0.565625 | 0.506136 | 0.625114 |
| labels_without_gating | safety_violation | 0.565625 | 0.506136 | 0.625114 |
| labels_without_gating | waiting_cost | 0 | 0 | 0 |
| labels_without_gating | intervention_cost | -0.565625 | -0.625114 | -0.506136 |
| labels_without_gating | false_certification | 0 | 0 | 0 |
| oracle_visible_state | regret | 0 | 0 | 0 |
| oracle_visible_state | safety_violation | 0 | 0 | 0 |
| oracle_visible_state | waiting_cost | 0 | 0 | 0 |
| oracle_visible_state | intervention_cost | -0.565625 | -0.625114 | -0.506136 |
| oracle_visible_state | false_certification | 0 | 0 | 0 |
| provenance_erased | regret | 0.434375 | 0.374886 | 0.493864 |
| provenance_erased | safety_violation | 0 | 0 | 0 |
| provenance_erased | waiting_cost | 0.434375 | 0.374886 | 0.493864 |
| provenance_erased | intervention_cost | 0.434375 | 0.374886 | 0.493864 |
| provenance_erased | false_certification | 0 | 0 | 0 |
| random_label_placebo | regret | 0.3625 | 0.316665 | 0.408335 |
| random_label_placebo | safety_violation | 0.184375 | 0.126592 | 0.242158 |
| random_label_placebo | waiting_cost | 0.178125 | 0.144391 | 0.211859 |
| random_label_placebo | intervention_cost | -0.00625 | -0.089032 | 0.076532 |
| random_label_placebo | false_certification | 0.184375 | 0.126592 | 0.242158 |

## Diagnostics

| check | value |
|---|---:|
| benign_low_overhead | True |
| erased_safe_but_burdensome | True |
| erasure_regret_separates | True |
| leakage_guard_passes | True |
| oracle_closes_gap | True |
| preserving_low_regret | True |
| ungated_exposes_safety_need | True |

## Files to share

- `outputs/berth1/locked_replay_demo_summary.csv`
- `outputs/berth1/locked_replay_demo_paired.csv`
- `outputs/berth1/locked_replay_demo_diagnostics.json`
- `outputs/berth1/locked_replay_demo.manifest.json`
- `outputs/berth1/locked_replay_demo.preflight_manifest.json`
- `outputs/berth1/locked_replay_demo_report.md`
