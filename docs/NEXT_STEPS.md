# Recommended next step

Do not add more theory before the first locked ablation.

Next action:
1. Review and freeze PRE_RUN_LOCK.md.
2. Instantiate chi_B1(x) and the dominance table D in the code scaffold.
3. Run only the scaffold preflight first.
4. Export a small maritime replay in the provided replay-template schema.
5. Run the fixed-solver paired ablation on Berth-1-Conflict.
6. Report paired deltas across the six conditions before any aggregate figures.

The first paper-critical figure should be cumulative zero-violation regret across:
- provenance_preserving
- provenance_erased
- random_label_placebo
- labels_without_gating
- oracle_visible_state
- benign_agreement

Move to full maritime-twin replay only after the one-berth separation is clean under the frozen-solver contract.
