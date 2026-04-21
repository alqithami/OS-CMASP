# Berth-1-Conflict Report: `outputs/berth1/wide_example`

## Summary by condition

| condition | n | mean_regret | safety_violations | waiting_cost | intervention_cost | false_certifications |
|---|---|---|---|---|---|---|
| provenance_preserving | 4 | 0 | 0 | 0 | 2 | 0 |
| provenance_erased | 4 | 0.25 | 0 | 1 | 3 | 0 |
| random_label_placebo | 4 | 0.5 | 2 | 0 | 0 | 2 |
| labels_without_gating | 4 | 0.5 | 2 | 0 | 0 | 0 |
| oracle_visible_state | 4 | 0 | 0 | 0 | 0 | 0 |
| benign_agreement | 4 | 0 | 0 | 0 | 0 | 0 |

## Paired deltas vs provenance_preserving

| condition | metric | mean_delta_vs_provenance_preserving | ci95_low | ci95_high |
|---|---|---|---|---|
| benign_agreement | regret | 0 | 0 | 0 |
| benign_agreement | safety_violation | 0 | 0 | 0 |
| benign_agreement | waiting_cost | 0 | 0 | 0 |
| benign_agreement | intervention_cost | -0.5 | -0.5 | -0.5 |
| benign_agreement | false_certification | 0 | 0 | 0 |
| labels_without_gating | regret | 0.5 | 0.5 | 0.5 |
| labels_without_gating | safety_violation | 0.5 | 0.5 | 0.5 |
| labels_without_gating | waiting_cost | 0 | 0 | 0 |
| labels_without_gating | intervention_cost | -0.5 | -0.5 | -0.5 |
| labels_without_gating | false_certification | 0 | 0 | 0 |
| oracle_visible_state | regret | 0 | 0 | 0 |
| oracle_visible_state | safety_violation | 0 | 0 | 0 |
| oracle_visible_state | waiting_cost | 0 | 0 | 0 |
| oracle_visible_state | intervention_cost | -0.5 | -0.5 | -0.5 |
| oracle_visible_state | false_certification | 0 | 0 | 0 |
| provenance_erased | regret | 0.25 | -0.24 | 0.74 |
| provenance_erased | safety_violation | 0 | 0 | 0 |
| provenance_erased | waiting_cost | 0.25 | -0.24 | 0.74 |
| provenance_erased | intervention_cost | 0.25 | -0.24 | 0.74 |
| provenance_erased | false_certification | 0 | 0 | 0 |
| random_label_placebo | regret | 0.5 | 0.5 | 0.5 |
| random_label_placebo | safety_violation | 0.5 | 0.5 | 0.5 |
| random_label_placebo | waiting_cost | 0 | 0 | 0 |
| random_label_placebo | intervention_cost | -0.5 | -0.5 | -0.5 |
| random_label_placebo | false_certification | 0.5 | 0.5 | 0.5 |

## Diagnostics

| check | value |
|---|---:|
| benign_low_overhead | True |
| erased_safe_but_burdensome | True |
| erasure_regret_separates | False |
| leakage_guard_passes | True |
| oracle_closes_gap | True |
| preserving_low_regret | True |
| ungated_exposes_safety_need | True |

## Files to share

- `outputs/berth1/wide_example_summary.csv`
- `outputs/berth1/wide_example_paired.csv`
- `outputs/berth1/wide_example_diagnostics.json`
- `outputs/berth1/wide_example.manifest.json`
- `outputs/berth1/wide_example.preflight_manifest.json`
- `outputs/berth1/wide_example_report.md`
