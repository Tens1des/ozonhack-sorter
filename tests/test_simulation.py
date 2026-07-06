"""Тесты симуляции."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from simulation.model import CrossBeltSorterSimulation
from simulation.scenarios import run_baseline, run_chute_failure


def test_baseline_runs():
    result = run_baseline(duration_s=30, seed=1)
    summary = result.summary()
    assert summary["generated"] > 0
    assert summary["throughput_per_hour"] > 0


def test_chute_failure_runs():
    result = run_chute_failure(duration_s=30, seed=2)
    assert result.metrics.item_stats.generated > 0


def test_simulation_metrics_structure():
    sim = CrossBeltSorterSimulation(seed=3)
    metrics = sim.run(20)
    assert metrics.item_stats.generated >= 0
    assert len(sim.routing.chutes) == 400
