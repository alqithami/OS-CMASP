# Berth-1-Conflict Report: `outputs/berth1/synthetic_smoke`

## Summary by condition

| condition | n | mean_regret | safety_violations | waiting_cost | intervention_cost | false_certifications |
|---|---:|---:|---:|---:|---:|---:|
| provenance_preserving | 320 | 0.0 | 0 | 0.0 | 181.0 | 0 |
| provenance_erased | 320 | 0.434375 | 0 | 139.0 | 320.0 | 0 |
| random_label_placebo | 320 | 0.3625 | 59 | 57.0 | 179.0 | 59 |
| labels_without_gating | 320 | 0.565625 | 181 | 0.0 | 0.0 | 0 |
| oracle_visible_state | 320 | 0.0 | 0 | 0.0 | 0.0 | 0 |
| benign_agreement | 320 | 0.0 | 0 | 0.0 | 0.0 | 0 |

## Paired deltas vs provenance_preserving

| condition | metric | mean_delta | ci95_low | ci95_high |
|---|---|---:|---:|---:|
| benign_agreement | regret | 0.0 | 0.0 | 0.0 |
| benign_agreement | safety_violation | 0.0 | 0.0 | 0.0 |
| benign_agreement | waiting_cost | 0.0 | 0.0 | 0.0 |
| benign_agreement | intervention_cost | -0.565625 | -0.6251142759943618 | -0.5061357240056383 |
| benign_agreement | false_certification | 0.0 | 0.0 | 0.0 |
| labels_without_gating | regret | 0.565625 | 0.5061357240056383 | 0.6251142759943618 |
| labels_without_gating | safety_violation | 0.565625 | 0.5061357240056383 | 0.6251142759943618 |
| labels_without_gating | waiting_cost | 0.0 | 0.0 | 0.0 |
| labels_without_gating | intervention_cost | -0.565625 | -0.6251142759943618 | -0.5061357240056383 |
| labels_without_gating | false_certification | 0.0 | 0.0 | 0.0 |
| oracle_visible_state | regret | 0.0 | 0.0 | 0.0 |
| oracle_visible_state | safety_violation | 0.0 | 0.0 | 0.0 |
| oracle_visible_state | waiting_cost | 0.0 | 0.0 | 0.0 |
| oracle_visible_state | intervention_cost | -0.565625 | -0.6251142759943618 | -0.5061357240056383 |
| oracle_visible_state | false_certification | 0.0 | 0.0 | 0.0 |
| provenance_erased | regret | 0.434375 | 0.37488572400563835 | 0.49386427599436167 |
| provenance_erased | safety_violation | 0.0 | 0.0 | 0.0 |
| provenance_erased | waiting_cost | 0.434375 | 0.37488572400563835 | 0.49386427599436167 |
| provenance_erased | intervention_cost | 0.434375 | 0.37488572400563835 | 0.49386427599436167 |
| provenance_erased | false_certification | 0.0 | 0.0 | 0.0 |
| random_label_placebo | regret | 0.3625 | 0.3166646970120192 | 0.40833530298798076 |
| random_label_placebo | safety_violation | 0.184375 | 0.12659186556615332 | 0.2421581344338467 |
| random_label_placebo | waiting_cost | 0.178125 | 0.14439113039787263 | 0.21185886960212738 |
| random_label_placebo | intervention_cost | -0.0062500000000000056 | -0.08903196764191265 | 0.07653196764191264 |
| random_label_placebo | false_certification | 0.184375 | 0.12659186556615332 | 0.2421581344338467 |

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

- `outputs/berth1/synthetic_smoke_summary.csv`
- `outputs/berth1/synthetic_smoke_paired.csv`
- `outputs/berth1/synthetic_smoke_diagnostics.json`
- `outputs/berth1/synthetic_smoke.manifest.json`
- `outputs/berth1/synthetic_smoke.preflight_manifest.json`
- `outputs/berth1/synthetic_smoke_report.md`
