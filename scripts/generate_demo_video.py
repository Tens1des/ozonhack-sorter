#!/usr/bin/env python3
"""Генерация демо-видео MP4 для сдачи (matplotlib + ffmpeg)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
  sys.path.insert(0, str(ROOT))

from simulation.scenarios import run_all_scenarios

OUT = ROOT / "docs" / "demo.mp4"
FRAMES = ROOT / "docs" / "_video_frames"
CSV = ROOT / "simulation" / "results" / "scenario_summary.csv"


def ensure_data() -> pd.DataFrame:
  if not CSV.exists():
    df = run_all_scenarios(duration_s=120, seed=42)
    CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CSV, index=False)
    return df
  return pd.read_csv(CSV)


def render_frames(df: pd.DataFrame) -> None:
  FRAMES.mkdir(parents=True, exist_ok=True)
  for old in FRAMES.glob("frame_*.png"):
    old.unlink()

  slides = [
    ("OzonHack — Кросс-белт сортировщик", "100 000 т/ч | 400 направлений | 4 модуля"),
    ("Архитектура", "Вход → Сканер → WMS → Индукция → Сброс → КТЯ"),
    ("Площадь", "9 737 м² (49% от лимита 20 000 м²)"),
    ("Энергия", "460 кВт | 4,6 Вт·ч на товар"),
  ]

  idx = 0
  for title, subtitle in slides:
    fig, ax = plt.subplots(figsize=(12.8, 7.2))
    ax.axis("off")
    ax.text(0.5, 0.62, title, ha="center", va="center", fontsize=28, color="#005BFF", transform=ax.transAxes)
    ax.text(0.5, 0.42, subtitle, ha="center", va="center", fontsize=18, color="#333", transform=ax.transAxes)
    fig.savefig(FRAMES / f"frame_{idx:03d}.png", dpi=100, facecolor="white")
    plt.close(fig)
    idx += 1

  fig, ax = plt.subplots(figsize=(12.8, 7.2))
  ax.bar(df["scenario"], df["throughput_per_hour"] / 1000, color="#005BFF")
  ax.axhline(100, color="red", linestyle="--", label="Цель 100k/ч")
  ax.set_title("Результаты симуляции SimPy", fontsize=18)
  ax.set_ylabel("тыс. товаров/ч")
  ax.legend()
  plt.xticks(rotation=15)
  fig.savefig(FRAMES / f"frame_{idx:03d}.png", dpi=100, facecolor="white", bbox_inches="tight")
  plt.close(fig)
  idx += 1

  fig, ax = plt.subplots(figsize=(12.8, 7.2))
  ax.bar(df["scenario"], df["correct_rate"] * 100, color="#00A86B")
  ax.set_title("Точность сортировки, %", fontsize=18)
  ax.set_ylabel("%")
  plt.xticks(rotation=15)
  fig.savefig(FRAMES / f"frame_{idx:03d}.png", dpi=100, facecolor="white", bbox_inches="tight")
  plt.close(fig)
  idx += 1

  fig, ax = plt.subplots(figsize=(12.8, 7.2))
  ax.axis("off")
  ax.text(0.5, 0.55, "Запуск: ./scripts/run_all.sh", ha="center", fontsize=22, transform=ax.transAxes)
  ax.text(0.5, 0.40, "Репозиторий: README.md", ha="center", fontsize=18, color="#666", transform=ax.transAxes)
  fig.savefig(FRAMES / f"frame_{idx:03d}.png", dpi=100, facecolor="white")
  plt.close(fig)


def encode_video() -> None:
  cmd = [
    "ffmpeg", "-y",
    "-framerate", "1/3",
    "-i", str(FRAMES / "frame_%03d.png"),
    "-vf", "scale=1280:720",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    str(OUT),
  ]
  subprocess.run(cmd, check=True, capture_output=True)


def main() -> None:
  df = ensure_data()
  render_frames(df)
  encode_video()
  print(f"Saved: {OUT}")


if __name__ == "__main__":
  main()
