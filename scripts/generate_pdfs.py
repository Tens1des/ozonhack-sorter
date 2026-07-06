#!/usr/bin/env python3
"""Генерация PDF: компоновка и презентация."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAYOUT_PDF = ROOT / "cad" / "layout.pdf"
PRESENTATION_PDF = ROOT / "docs" / "presentation.pdf"
CSV = ROOT / "simulation" / "results" / "scenario_summary.csv"


def generate_layout_pdf() -> None:
    fig, ax = plt.subplots(figsize=(11.69, 8.27))
    ax.set_xlim(0, 500)
    ax.set_ylim(0, 320)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("OzonHack — компоновка 4 кросс-белт модулей (вид сверху)", fontsize=14)

    modules = [(80, 60, "M1"), (280, 60, "M2"), (80, 200, "M3"), (280, 200, "M4")]
    for cx, cy, label in modules:
        e = plt.Circle((cx, cy), 35, fill=False, color="#005BFF", linewidth=2)
        ax.add_patch(e)
        ax.text(cx, cy, f"{label}\n100 ячеек", ha="center", va="center", fontsize=11, color="#005BFF")

    ax.add_patch(plt.Rectangle((200, 45), 100, 30, fill=True, facecolor="#005BFF", alpha=0.2, edgecolor="#005BFF"))
    ax.text(250, 60, "IN", ha="center", va="center", color="#005BFF")
    ax.text(250, 20, "~9 737 м² | 400 направлений | 100 000 т/ч", ha="center", fontsize=10, color="#666")

    LAYOUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(LAYOUT_PDF, format="pdf", bbox_inches="tight")
    plt.close(fig)


def generate_presentation_pdf() -> None:
    df = pd.read_csv(CSV) if CSV.exists() else None

    slides = [
        ("OzonHack — Трек 2", "Модульный кросс-белт сортировщик\n100 000 т/ч | 400 направлений"),
        ("Решение", "4 модуля × 100 ячеек\nСканер → WMS → Индукция → КТЯ"),
        ("Показатели", "Площадь: 9 737 м²\nМощность: 460 кВт\nТочность: 99,45%"),
    ]

    with PdfPages(PRESENTATION_PDF) as pdf:
        for title, body in slides:
            fig, ax = plt.subplots(figsize=(11.69, 8.27))
            ax.axis("off")
            ax.text(0.5, 0.65, title, ha="center", va="center", fontsize=24, color="#005BFF", transform=ax.transAxes)
            ax.text(0.5, 0.42, body, ha="center", va="center", fontsize=16, transform=ax.transAxes)
            pdf.savefig(fig)
            plt.close(fig)

        if df is not None:
            fig, axes = plt.subplots(1, 2, figsize=(11.69, 8.27))
            axes[0].bar(df["scenario"], df["throughput_per_hour"] / 1000, color="#005BFF")
            axes[0].axhline(100, color="red", linestyle="--")
            axes[0].set_title("Пропускная способность, тыс/ч")
            axes[1].bar(df["scenario"], df["correct_rate"] * 100, color="#00A86B")
            axes[1].set_title("Точность, %")
            for ax in axes:
                ax.tick_params(axis="x", rotation=15)
            fig.suptitle("Симуляция SimPy", fontsize=16)
            pdf.savefig(fig)
            plt.close(fig)

        fig, ax = plt.subplots(figsize=(11.69, 8.27))
        ax.axis("off")
        ax.text(0.5, 0.5, "Запуск: ./scripts/run_all.sh\nREADME.md", ha="center", fontsize=18, transform=ax.transAxes)
        pdf.savefig(fig)
        plt.close(fig)

    print(f"Saved: {PRESENTATION_PDF}")


def main() -> None:
    generate_layout_pdf()
    print(f"Saved: {LAYOUT_PDF}")
    generate_presentation_pdf()


if __name__ == "__main__":
    main()
