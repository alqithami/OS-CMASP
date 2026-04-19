# v30 paper revision notes

This revision responds to the concern that Sections 4--12 of the main paper were too generic and did not preserve enough technical detail from the longer appendix.

## Strengthened sections

- Section 4 now gives a more operational berth-readiness example, an explicit two-aggregate example, and a table positioning the example against POMDP/POSG belief states, common-information MARL, shielding, truth maintenance, and provenance/fusion.
- Section 5 now states explicit modeling commitments: visible-context, dominance, solver isolation, and evidence status.
- Section 6 now expands OS-CPOSG/OS-CMASP semantics, emphasizing claim state, epistemic actions, dominant certificates, and no-cherry-picking admissibility.
- Section 7 now adds a stronger discussion of containment, shielding, certificate soundness, and a gate-safety-by-construction proposition.
- Section 8 now details Berth-1-Conflict latent state, scenario families, ablations, expected result pattern, and metrics.
- Section 9 now separates preflight, semantic separation, maritime replay, and metric lift; it explicitly warns against placeholder replay paths.
- Section 10 now distinguishes executable modes: preflight, synthetic smoke, replay run, and packaging.
- Sections 11--12 now state the active-regime limitations and the correct empirical next step.

## Code / pipeline fixes

- The replay runner now refuses missing replay CSVs before launching a run.
- The placeholder path `path/to/twin_replay_claims.csv` is explicitly detected.
- Packaging refuses to create a zero-file zip.
- Synthetic smoke tests are explicit and labeled non-evidentiary.
- A Markdown report is generated from summary, paired-delta, and diagnostics outputs.
