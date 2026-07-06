"""Сценарии симуляции и агрегация метрик."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from simulation.config import CONFIG
from simulation.model import CrossBeltSorterSimulation, SimulationMetrics


@dataclass
class ScenarioResult:
    name: str
    duration_s: float
    metrics: SimulationMetrics

    def summary(self) -> dict:
        stats = self.metrics.item_stats
        generated = max(stats.generated, 1)
        hours = self.duration_s / 3600.0
        processed = stats.sorted_correctly + stats.misrouted
        throughput = processed / hours if hours > 0 else 0.0

        cycle = self.metrics.cycle_times
        avg_cycle = sum(cycle) / len(cycle) if cycle else 0.0
        p95_cycle = sorted(cycle)[int(len(cycle) * 0.95)] if cycle else 0.0

        return {
            "scenario": self.name,
            "duration_s": self.duration_s,
            "generated": stats.generated,
            "processed": processed,
            "throughput_per_hour": round(throughput, 1),
            "target_per_hour": CONFIG.target_throughput_per_hour,
            "throughput_ratio": round(throughput / CONFIG.target_throughput_per_hour, 3),
            "correct_rate": round(stats.sorted_correctly / generated, 4),
            "misroute_rate": round(stats.misrouted / generated, 4),
            "lost_rate": round(stats.lost / generated, 6),
            "damage_rate": round(stats.damaged / generated, 6),
            "rejected_rate": round(stats.rejected_no_route / generated, 6),
            "avg_cycle_s": round(avg_cycle, 2),
            "p95_cycle_s": round(p95_cycle, 2),
            "kty_swaps": self.metrics.kty_stats.swaps,
            "kty_full_events": self.metrics.kty_stats.full_events,
            "jam_events": self.metrics.jam_events,
        }


def run_baseline(duration_s: float = 3600, seed: int = 42) -> ScenarioResult:
    sim = CrossBeltSorterSimulation(seed=seed)
    metrics = sim.run(duration_s)
    return ScenarioResult("baseline", duration_s, metrics)


def run_overload(duration_s: float = 3600, seed: int = 42) -> ScenarioResult:
    sim = CrossBeltSorterSimulation(
        seed=seed,
        arrival_rate_per_hour=int(CONFIG.target_throughput_per_hour * 1.25),
    )
    metrics = sim.run(duration_s)
    return ScenarioResult("overload_125pct", duration_s, metrics)


def run_chute_failure(duration_s: float = 3600, seed: int = 42) -> ScenarioResult:
    failed = {7, 42, 155, 299}
    sim = CrossBeltSorterSimulation(seed=seed, failed_chutes=failed)
    metrics = sim.run(duration_s)
    return ScenarioResult("chute_failure", duration_s, metrics)


def run_module_degraded(duration_s: float = 3600, seed: int = 42) -> ScenarioResult:
    sim = CrossBeltSorterSimulation(seed=seed, degraded_modules={2})
    metrics = sim.run(duration_s)
    return ScenarioResult("module_degraded", duration_s, metrics)


def run_hotspot_jam(duration_s: float = 3600, seed: int = 7) -> ScenarioResult:
    """Имитация перекоса потока: повышенная нагрузка на модуль 1."""
    from control.wms_mock import RoutingDecision

    sim = CrossBeltSorterSimulation(seed=seed)
    original_resolve = sim.wms.resolve

    def biased_resolve(barcode: str) -> RoutingDecision:
        decision = original_resolve(barcode)
        if sim.rng.random() < 0.55:
            destination = sim.rng.randint(1, CONFIG.chutes_per_module)
            return RoutingDecision(
                barcode=barcode,
                destination=destination,
                route_hint=f"M1-C{destination:03d}",
            )
        return decision

    sim.wms.resolve = biased_resolve  # type: ignore[method-assign]
    metrics = sim.run(duration_s)
    return ScenarioResult("hotspot_jam", duration_s, metrics)


SCENARIOS = {
    "baseline": run_baseline,
    "overload": run_overload,
    "chute_failure": run_chute_failure,
    "module_degraded": run_module_degraded,
    "hotspot_jam": run_hotspot_jam,
}


def run_all_scenarios(
    duration_s: float = 3600, seed: int = 42
) -> tuple[pd.DataFrame, dict[str, ScenarioResult]]:
    results: dict[str, ScenarioResult] = {}
    rows = []
    for name, runner in SCENARIOS.items():
        result = runner(duration_s=duration_s, seed=seed)
        results[name] = result
        rows.append(result.summary())
    return pd.DataFrame(rows), results
