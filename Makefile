.PHONY: test preflight synthetic-smoke paper clean

test:
	python -m compileall src scripts

preflight:
	scripts/run_berth1_preflight.sh artifacts/preflight

synthetic-smoke:
	scripts/run_berth1_synthetic_smoke.sh outputs/berth1/synthetic_smoke

paper:
	cd manuscript && latexmk -pdf -interaction=nonstopmode main.tex

clean:
	rm -rf outputs/berth1 artifacts/preflight manuscript/*.aux manuscript/*.bbl manuscript/*.bcf manuscript/*.blg manuscript/*.log manuscript/*.out manuscript/*.run.xml manuscript/*.toc manuscript/*.fls manuscript/*.fdb_latexmk
