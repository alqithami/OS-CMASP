# Paper Update Notes v33

v33 does not promote the synthetic run to empirical evidence. It records the run as software validation and strengthens the reproducibility path.

Changes:

1. Added a local-run readout documenting the successful locked replay demo.
2. Added a twin-export guide that removes manual replay-row editing.
3. Added wide-export inspection and common alias inference in the replay adapter.
4. Added `make local-sanity` to run preflight, locked replay demo, and wide-example conversion in one command.
5. Added tests for alias-based wide conversion.

Manuscript stance:

- The paper remains a theory-and-protocol manuscript until real twin replay is available.
- Locked synthetic replay is only a software sanity check.
- Wide-example conversion is only a converter path check.
- First paper-relevant evidence is the fixed-solver paired ablation on a real twin replay bank.
