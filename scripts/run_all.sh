#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH=.

python scripts/calculations.py
python scripts/generate_layout.py
python scripts/generate_diagrams.py
python scripts/generate_kty_diagram.py
python scripts/generate_stl.py
python scripts/generate_pdfs.py
python scripts/generate_report_html.py
python simulation/run.py --scenario all --duration 600
python scripts/generate_demo_video.py
chmod +x scripts/package_s3.sh 2>/dev/null || true
./scripts/package_s3.sh 2>/dev/null || bash scripts/package_s3.sh
python scripts/verify_submission.py

echo ""
echo "Done. Results in simulation/results/ and docs/demo.mp4"
