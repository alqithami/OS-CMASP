PYTHON ?= python
OUT ?= artifacts/preflight
MANIFEST ?= $(OUT)/berth1_preflight_manifest.json

.PHONY: setup test preflight locked-replay-demo synthetic-smoke wide-example inspect-wide-example local-sanity replay-template paper clean package

setup:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e .[dev]

test:
	$(PYTHON) -m compileall src scripts tests
	$(PYTHON) -m unittest discover -s tests -v

preflight:
	mkdir -p $(OUT)
	scripts/run_berth1_preflight.sh $(OUT)

locked-replay-demo:
	scripts/run_berth1_locked_replay_demo.sh outputs/berth1/locked_replay_demo

synthetic-smoke:
	scripts/run_berth1_synthetic_smoke.sh outputs/berth1/synthetic_smoke

inspect-wide-example:
	scripts/inspect_berth1_wide_export.sh data/examples/berth1_wide_example.csv data/replay/berth1_wide_example.inspect_report.json

wide-example:
	mkdir -p data/replay outputs/berth1
	scripts/inspect_berth1_wide_export.sh data/examples/berth1_wide_example.csv data/replay/berth1_wide_example.inspect_report.json
	scripts/build_berth1_replay_from_wide.sh data/examples/berth1_wide_example.csv data/replay/berth1_wide_example_replay.csv
	scripts/run_berth1_replay.sh data/replay/berth1_wide_example_replay.csv outputs/berth1/wide_example
	scripts/package_results.sh outputs/berth1/wide_example outputs/berth1/wide_example_results.zip

local-sanity:
	scripts/run_berth1_all_sanity.sh outputs/berth1

replay-template:
	scripts/write_berth1_replay_template.sh data/templates/berth1_replay_template.csv

paper:
	cd manuscript && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

clean:
	rm -rf build dist *.egg-info .pytest_cache .ruff_cache outputs data/replay
	cd manuscript && latexmk -C || true

package:
	mkdir -p dist
	git archive --format=zip --output=dist/os-cmasp-repo-snapshot.zip HEAD
