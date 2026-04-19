#!/usr/bin/env bash
set -euo pipefail
cd manuscript
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
