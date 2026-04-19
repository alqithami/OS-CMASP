# Manuscript

Source files:

- `main.tex`
- `refs.bib`

Build locally with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

or from the repository root:

```bash
make paper
```

The current reference PDF from the working draft is stored in `artifacts/reference/`. In normal GitHub operation, future PDFs should be produced by the `Paper` workflow and attached to releases.
