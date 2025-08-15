#!/usr/bin/env bash
set -euo pipefail

REPO="abstract-scroller"
SNAP_ID="v2025-08-15"

# mkdir -p "$REPO"

echo "→ init git"
git init -q


echo "→ .gitignore"
cat > .gitignore <<'EOF'
__pycache__/
.env
.venv
node_modules/
dist/
*.pyc
*.pyo
*.log
.DS_Store
coverage/
/.pytest_cache
EOF


echo "→ README"
cat > README.md <<'EOF'
# Econ Abstracts Viewer (MVP)

Batch publisher → immutable snapshot → dumb, fast reader (tiles + masks).
This repo scaffolds Milestone M1: manifest, tiles, and a simple viewer.

## Quick start



1) Create venv and install deps:
   python -m venv .venv && source .venv/bin/activate
   pip install -e .

2) Build a toy snapshot:
   make snapshot

3) Serve with Brotli headers:
   make serve    # http://localhost:8000/snapshots/v2025-08-15/manifest.json

4) Open frontend:
   open frontend/index.html  (or your OS equivalent)
EOF

echo "→ Makefile"
cat > Makefile <<'EOF'
PY?=python3

.PHONY: snapshot validate serve clean

snapshot:
	$(PY) -m backend.jobs.mvp_snapshot --input data/sample.csv --out data/snapshots/v2025-08-15

validate:
	$(PY) -m backend.publish.manifest --validate data/snapshots/v2025-08-15

serve:
	$(PY) -m backend.devserver --root data

clean:
	rm -rf data/snapshots/v2025-08-15
EOF

echo "→ pyproject.toml"
cat > pyproject.toml <<'EOF'
[project]
name = "econ-abstracts-viewer"
version = "0.0.1"
description = "Snapshot publisher + tile viewer MVP"
requires-python = ">=3.9"
dependencies = [
  "pandas>=2.0,<3.0",
  "numpy>=1.26,<3.0",
  "brotli>=1.1",
  "jsonschema>=4.0",
  "scikit-learn>=1.3"  # for tiny TF-IDF in nodes.py (later)
]

[project.scripts]
# optional CLI entry points later

[build-system]
requires = ["setuptools>=67", "wheel"]
build-backend = "setuptools.build_meta"
EOF
