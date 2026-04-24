# OS-CMASP Promotion Protocol: Berth-1 to Maritime Digital Twin (v34)

This protocol answers the operational question: after the minimal benchmark works, what exactly must be done to port OS-CMASP into a larger maritime digital twin?

The short answer is: do **not** change the solver first. Promote the same process semantics through increasingly realistic replay banks while keeping the ablation interface frozen.

## Current status

The locked synthetic run validates the executable scaffold and the active-regime logic. It does **not** count as maritime-twin evidence. The next step is to run the same frozen ablation on a replay bank exported from the maritime twin or converted deterministically from a one-row-per-step twin export.

## Promotion gates

| Gate | Name | Input | Command | Pass condition | Evidence status |
|---|---|---|---|---|---|
| G0 | Software sanity | Locked synthetic bank | `make local-sanity` | all active-regime diagnostics pass | software only |
| G1 | Twin-export inspect | raw one-row-per-step CSV | `scripts/inspect_berth1_wide_export.sh raw.csv report.json` | `convertible_without_manual_rename=true` | interface only |
| G2 | Berth-1 twin replay | raw wide CSV or long claim CSV | `scripts/run_maritime_twin_gate.sh raw.csv outputs/berth1/twin_gate_v1` | promotion report says `overall_gate_pass=true` | first paper-relevant evidence |
| G3 | Multi-scenario twin slice | declared twin replay over multiple traffic/weather/disruption blocks | same script, multiple block keys | positive paired burden and zero-violation preservation under block reports | pilot twin evidence |
| G4 | Full twin campaign | full simulator campaign | batch gate runs + metric lift | semantic separation plus calibrated emissions/fairness translations | main empirical study |

## Required lock before G2

Before the first paper-relevant replay, lock the following in a PR:

1. visible context map `chi_B1(x)`;
2. proposition-family map `fam`;
3. dominance table `D` by proposition family;
4. freshness windows and timestamp tie rules;
5. six ablation conditions;
6. metric hierarchy;
7. twin-export schema;
8. go/no-go thresholds.

## What counts as success

The desired Berth-1 twin-replay pattern is:

- `provenance_preserving`: low regret and zero/near-zero safety violations;
- `provenance_erased`: paired regret or safety-service burden under the same replay bank;
- `random_label_placebo`: does not close the provenance gap;
- `labels_without_gating`: reveals safety/certification risk;
- `oracle_visible_state`: closes the gap;
- `benign_agreement`: low overhead.

## What to do if G2 fails

Do not add controller depth. Instead:

1. inspect whether the replay contains active contradiction regimes;
2. verify that visible context does not leak the hidden safety state;
3. check whether dominance/freshness rules are appropriate for the proposition family;
4. split the replay into scenario blocks and identify where OS-CMASP semantics are active;
5. revise the declared active regime before running a new locked replay.

## Full twin porting map

The full twin should expose or derive claim records from the following subsystems:

| Twin subsystem | Proposition family | Example claims | Typical observers/sources |
|---|---|---|---|
| Berth readiness | readiness | `ready`, `not ready` | harbor master, terminal ops, strategic plan |
| Crane operations | crane | `craneOK`, `not craneOK` | maintenance system, terminal ops, plan |
| Vessel ETA | eta | `etaOnTime`, `not etaOnTime` | AIS feed, carrier schedule, pilot station |
| Weather/safety | weather | `weatherSafe`, `not weatherSafe` | port safety, approved weather feed, dispatcher |
| Customs/clearance | clearance | `cleared`, `not cleared` | customs system, terminal docs, human override |
| Yard readiness | yard | `yardReady`, `not yardReady` | yard ops, truck gate system, terminal ops |

Berth-1 is the minimum active-regime instantiation. Full twin integration repeats the same logic over more proposition families and more assets.
