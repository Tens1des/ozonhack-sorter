#!/usr/bin/env python3
"""Запуск симуляции модульного кросс-белт сортировщика."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from simulation.plots import plot_queue_timeline, plot_scenario_summary
from simulation.scenarios import SCENARIOS, run_all_scenarios

RESULTS_DIR = Path(__file__).resolve().parent / "results"


def main() -> None:
    parser = argparse.ArgumentParser(description="OzonHack sorter simulation")
    parser.add_argument(
        "--scenario",
        choices=[*SCENARIOS.keys(), "all"],
        default="all",
        help="Сценарий для запуска",
    )
    parser.add_argument("--duration", type=int, default=3600, help="Длительность, сек")
    parser.add_argument("--seed", type=int, default=42, help="Seed RNG")
    args = parser.parse_args()

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    if args.scenario == "all":
        df, results = run_all_scenarios(duration_s=args.duration, seed=args.seed)
        csv_path = RESULTS_DIR / "scenario_summary.csv"
        df.to_csv(csv_path, index=False)
        plot_scenario_summary(df)

        details = {}
        for name, result in results.items():
            plot_queue_timeline(result)
            details[name] = result.summary()

        json_path = RESULTS_DIR / "scenario_details.json"
        json_path.write_text(json.dumps(details, indent=2, ensure_ascii=False), encoding="utf-8")

        print("=== OzonHack Simulation Results ===")
        print(df.to_string(index=False))
        print(f"\nSaved: {csv_path}")
        print(f"Saved: {RESULTS_DIR / 'scenario_summary.png'}")
        return

    runner = SCENARIOS[args.scenario]
    result = runner(duration_s=args.duration, seed=args.seed)
    summary = result.summary()
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    plot_queue_timeline(result)


if __name__ == "__main__":
    main()
