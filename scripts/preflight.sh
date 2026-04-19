#!/usr/bin/env bash
set -euo pipefail
mkdir -p outputs
python -m os_cmasp.berth1_conflict --mode preflight --manifest outputs/preflight_manifest.json
