#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

DIST="dist/s3_bundle"
rm -rf dist
mkdir -p "$DIST/cad/models" "$DIST/docs" "$DIST/simulation/results"

# Видео
if [[ -f docs/demo.mp4 ]]; then
  cp docs/demo.mp4 "$DIST/docs/"
else
  echo "WARN: docs/demo.mp4 не найден — запустите make video"
fi

# CAD
cp cad/*.svg "$DIST/cad/" 2>/dev/null || true
cp cad/layout.pdf "$DIST/cad/" 2>/dev/null || true
cp docs/presentation.pdf "$DIST/docs/" 2>/dev/null || true
cp cad/models/*.stl "$DIST/cad/models/" 2>/dev/null || true
cp cad/models/*.obj "$DIST/cad/models/" 2>/dev/null || true

# Результаты симуляции
cp simulation/results/*.png "$DIST/simulation/results/" 2>/dev/null || true
cp simulation/results/*.csv "$DIST/simulation/results/" 2>/dev/null || true
cp simulation/results/*.json "$DIST/simulation/results/" 2>/dev/null || true

# README для эксперта S3
cat > "$DIST/README.txt" <<'EOF'
OzonHack — S3 bundle
- docs/demo.mp4 — видеодемонстрация
- cad/ — схемы и STL
- simulation/results/ — метрики и графики
Полный репозиторий: см. GitHub README.md
EOF

(cd dist && zip -r ozonhack_s3_bundle.zip s3_bundle)
echo "Saved: dist/ozonhack_s3_bundle.zip"
