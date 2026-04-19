# Pre-run lock checklist

Before running local or twin-backed experiments, freeze the following items.

1. Visible-context map
- Freeze chi_B1(x), including which operational facts are visible to the controller and which are only represented through claim provenance.

2. Claim language and consistency
- Freeze the formula language L_Phi used for Berth-1-Conflict.
- Freeze the consistency predicate Cons for the benchmark.
- Decide whether the first run is literal-only or SAT/SMT-backed.

3. Proposition-family dominance scheme
- Freeze fam(phi).
- Freeze the dominance relation D by proposition family.
- Freeze rank defaults, freshness windows, and tie-breaking rules.

4. Ablation conditions
- provenance_preserving
- provenance_erased
- random_label_placebo
- labels_without_gating
- oracle_visible_state
- benign_agreement

5. Solver identity
- Keep the solver fixed across all ablations.
- Do not change training budget, feature dimensions, hidden sizes, reward weights, or gating logic across semantics conditions unless explicitly listed as an ablation.

6. Metrics
Primary:
- zero-violation regret
- critical-action violation rate
- paired service regret
- intervention count

Secondary:
- idling-emission burden
- service disparity
- min-max, Gini, APD
- contradiction half-life

7. Replay protocol
- Freeze replay CSV schema.
- Freeze seed pairing and scenario-key block definition.
- Report paired deltas before aggregate metrics.

Go/no-go rule:
- If provenance-preserving semantics do not separate from provenance-erased semantics under a frozen solver on Berth-1-Conflict, do not scale to the full maritime twin. First identify whether the scenario distribution is provenance-active.
