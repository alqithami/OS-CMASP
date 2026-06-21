# Maritime twin promotion runbook v36

## Goal

Move from the minimal Berth-1 benchmark to a maritime digital twin without changing the solver or adding controller layers.

## Gate sequence

1. G0: run local software sanity checks.
2. G1: inspect a raw twin export.
3. G2: run Berth-1 replay from a declared twin export.
4. G3: run pilot twin slices across operational blocks.
5. G4: run the full twin campaign.

## Rule

Scale by replacing the replay source under the frozen ablation protocol, not by changing the controller stack.
