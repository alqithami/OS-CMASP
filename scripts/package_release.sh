#!/usr/bin/env bash
set -euo pipefail
VERSION="${1:-local}"
mkdir -p dist
ZIP="dist/os-cmasp-${VERSION}.zip"
rm -f "$ZIP"
zip -r "$ZIP" README.md CITATION.cff pyproject.toml Makefile manuscript src tests data configs docs scripts .github .gitignore .gitattributes artifacts/reference -x '*/__pycache__/*' '*.pyc'
echo "wrote $ZIP"
