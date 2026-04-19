PYTHON ?= python
OUT ?= outputs
MANIFEST ?= $(OUT)/preflight_manifest.json

.PHONY: setup test preflight replay-template paper clean package

setup:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -e .[dev]

test:
	$(PYTHON) -m compileall src tests
	$(PYTHON) -m unittest discover -s tests -v

preflight:
	mkdir -p $(OUT)
	$(PYTHON) -m os_cmasp.berth1_conflict --mode preflight --manifest $(MANIFEST)

replay-template:
	$(PYTHON) -m os_cmasp.berth1_conflict --write-template data/templates/berth1_replay_template.csv

paper:
	cd manuscript && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

clean:
	rm -rf build dist *.egg-info .pytest_cache .ruff_cache outputs
	cd manuscript && latexmk -C || true

package:
	mkdir -p dist
	git archive --format=zip --output=dist/os-cmasp-repo-snapshot.zip HEAD
