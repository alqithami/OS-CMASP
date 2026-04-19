# Experiment protocol

## Objective

Test whether provenance-preserving OS-CMASP semantics separate from provenance-erased semantics under a frozen solver.

## Non-negotiable controls

- Same latent episode bank across all conditions.
- Same solver across all conditions.
- Same reward, budget, and metric definitions across all conditions.
- Randomized placebo labels must use separate per-step RNG streams so they do not perturb latent episode generation.
- Report paired deltas before aggregate summaries.

## Conditions

1. `provenance_preserving`
2. `provenance_erased`
3. `random_label_placebo`
4. `labels_without_gating`
5. `oracle_visible_state`
6. `benign_agreement`

## Primary metrics

- zero-violation regret;
- critical-action violation rate;
- paired service regret;
- intervention count.

## Secondary diagnostics

- idling-emission proxy;
- service disparity;
- min-max, Gini, APD;
- contradiction burden;
- contradiction half-life.

## First replay command

```bash
scripts/run_replay.sh path/to/twin_replay_claims.csv outputs/twin_replay_v1
```

## Report format

Every result note should include:

- replay SHA-256 hash;
- manifest path;
- condition set;
- paired-delta table;
- go/no-go interpretation;
- deviations from `docs/PRE_RUN_LOCK.md`, if any.
