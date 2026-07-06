"""Построение графиков по результатам симуляции."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

RESULTS_DIR = Path(__file__).resolve().parent / "results"


def ensure_results_dir() -> Path:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    return RESULTS_DIR


def plot_scenario_summary(df: pd.DataFrame, output_path: Path | None = None) -> Path:
    ensure_results_dir()
    output_path = output_path or RESULTS_DIR / "scenario_summary.png"

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    fig.suptitle("OzonHack Cross-Belt Sorter — сводка сценариев", fontsize=14)

    axes[0, 0].bar(df["scenario"], df["throughput_per_hour"], color="#005BFF")
    axes[0, 0].axhline(100_000, color="red", linestyle="--", label="Цель 100k/ч")
    axes[0, 0].set_title("Пропускная способность")
    axes[0, 0].set_ylabel("тов/ч")
    axes[0, 0].tick_params(axis="x", rotation=20)
    axes[0, 0].legend()

    axes[0, 1].bar(df["scenario"], df["correct_rate"] * 100, color="#00A86B")
    axes[0, 1].set_title("Доля корректной сортировки")
    axes[0, 1].set_ylabel("%")
    axes[0, 1].tick_params(axis="x", rotation=20)

    axes[1, 0].bar(df["scenario"], df["misroute_rate"] * 100, color="#F5A623")
    axes[1, 0].set_title("Доля перенаправлений (overflow)")
    axes[1, 0].set_ylabel("%")
    axes[1, 0].tick_params(axis="x", rotation=20)

    axes[1, 1].bar(df["scenario"], df["avg_cycle_s"], color="#7B61FF", label="avg")
    axes[1, 1].bar(df["scenario"], df["p95_cycle_s"], color="#B8A9FF", alpha=0.6, label="p95")
    axes[1, 1].set_title("Время цикла обработки")
    axes[1, 1].set_ylabel("сек")
    axes[1, 1].tick_params(axis="x", rotation=20)
    axes[1, 1].legend()

    plt.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    return output_path


def plot_queue_timeline(result, output_path: Path | None = None) -> Path | None:
    samples = result.metrics.queue_samples
    if not samples:
        return None

    ensure_results_dir()
    output_path = output_path or RESULTS_DIR / f"queue_{result.name}.png"

    times, queues = zip(*samples)
    plt.figure(figsize=(10, 4))
    plt.plot(times, queues, color="#005BFF")
    plt.title(f"Суммарная очередь — сценарий {result.name}")
    plt.xlabel("Время, с")
    plt.ylabel("Очередь")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    return output_path
