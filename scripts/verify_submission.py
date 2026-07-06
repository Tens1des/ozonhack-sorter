#!/usr/bin/env python3
"""Проверка полноты комплекта сдачи и работоспособности."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
  "README.md",
  "requirements.txt",
  "Dockerfile",
  "Makefile",
  "docs/concept.md",
  "docs/calculations.md",
  "docs/report.md",
  "docs/algorithms.md",
  "docs/specifications.md",
  "docs/deployment.md",
  "docs/checklist.md",
  "docs/video_script.md",
  "docs/slides.html",
  "docs/presentation.md",
  "simulation/run.py",
  "simulation/model.py",
  "simulation/scenarios.py",
  "control/wms_mock.py",
  "control/wms_server.py",
  "control/routing_logic.py",
  "control/balancer.py",
  "control/sorter_controller.py",
  "cad/layout_top_view.svg",
  "cad/process_flow.svg",
  "cad/kinematic_scheme.svg",
  "cad/kty_station.svg",
  "cad/models/kty_box.stl",
  "cad/models/kty_box.obj",
  "cad/models/module_footprint.stl",
  "docs/demo.mp4",
  "docs/report.html",
  "docs/presentation.pdf",
  "cad/layout.pdf",
  "dist/ozonhack_s3_bundle.zip",
  "docs/STATUS.md",
  "scripts/package_s3.sh",
  "pyproject.toml",
  "scripts/run_all.sh",
]

OPTIONAL_BUT_RECOMMENDED = [
  "simulation/results/scenario_summary.csv",
  "simulation/results/engineering_calculations.json",
]


def check_files() -> list[str]:
  errors = []
  for rel in REQUIRED_FILES:
    if not (ROOT / rel).exists():
      errors.append(f"Отсутствует: {rel}")
  return errors


def check_tests() -> tuple[bool, str]:
    env = {**os.environ, "PYTHONPATH": str(ROOT)}
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env=env,
    )
    return result.returncode == 0, result.stdout + result.stderr


def main() -> int:
  print("=== OzonHack: проверка комплекта сдачи ===\n")
  errors = check_files()
  if errors:
    print("Файлы:")
    for e in errors:
      print(f"  ✗ {e}")
  else:
    print(f"Файлы: ✓ все {len(REQUIRED_FILES)} обязательных на месте")

  missing_opt = [p for p in OPTIONAL_BUT_RECOMMENDED if not (ROOT / p).exists()]
  if missing_opt:
    print("\nРекомендуемые (не критично):")
    for p in missing_opt:
      print(f"  ○ {p}")

  ok, out = check_tests()
  print(f"\nТесты: {'✓' if ok else '✗'}")
  if not ok:
    print(out)
  else:
    print(out.strip())

  manual = [
    "Видео MP4 на S3 (или docs/demo.mp4 локально)",
    "Ссылки S3 в README.md",
    "Состав команды в README.md",
  ]
  print("\nВручную перед сдачей:")
  for m in manual:
    print(f"  ○ {m}")

  return 1 if errors or not ok else 0


if __name__ == "__main__":
  raise SystemExit(main())
