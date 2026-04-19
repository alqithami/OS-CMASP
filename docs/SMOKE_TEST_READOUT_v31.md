# Synthetic smoke-test readout from the uploaded run

The uploaded synthetic smoke run should be interpreted as a software sanity check, not maritime evidence.

Observed scaffold pattern:

- `provenance_preserving`: mean regret 0.0, safety violations 0.
- `provenance_erased`: mean regret 0.434375, safety violations 0, waiting cost 139.0.
- `labels_without_gating`: mean regret 0.565625, safety violations 181.
- `random_label_placebo`: mean regret 0.3625, safety violations 59, false certifications 59.
- `oracle_visible_state`: mean regret 0.0, safety violations 0.
- `benign_agreement`: mean regret 0.0, safety violations 0.

Interpretation: the scaffold behaves as intended in the locked synthetic active regime. Provenance erasure is safe but burdensome; ungated labels expose safety risk; the oracle closes the gap; benign agreement adds negligible overhead. The next check is not to hand-edit replay rows but to generate replay rows using the v31 adapter.
