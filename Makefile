.PHONY: setup test preflight paper clean

setup:
	python -m pip install --upgrade pip
	python -m pip install -e .[dev]

test:
	python -m compileall src scripts

preflight:
	scripts/run_berth1_preflight.sh

paper:
	cd manuscript && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

clean:
	cd manuscript && latexmk -C || true
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
