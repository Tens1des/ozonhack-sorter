#!/usr/bin/env python3
"""Инженерные расчёты производительности, площади и энергопотребления."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from simulation.config import CONFIG


@dataclass
class PerformanceCalc:
    target_items_per_hour: int
    target_items_per_second: float
    modules: int
    per_module_items_per_hour: float
    per_module_items_per_second: float
    induction_lanes_per_module: int
    induction_capacity_per_module_pps: float
    total_induction_capacity_pps: float
    design_margin: float


@dataclass
class AreaCalc:
    modules: int
    module_loop_length_m: float
    module_loop_width_m: float
    module_area_m2: float
    total_sorter_area_m2: float
    aux_area_m2: float
    total_area_m2: float
    limit_m2: float
    area_utilization: float


@dataclass
class EnergyCalc:
    sorter_power_kw: float
    aux_power_kw: float
    total_power_kw: float
    energy_per_item_wh: float
    energy_per_100k_items_kwh: float


def calc_performance() -> PerformanceCalc:
    target_pps = CONFIG.target_throughput_per_hour / 3600
    per_module_hour = CONFIG.target_throughput_per_hour / CONFIG.num_modules
    per_module_pps = per_module_hour / 3600
    lane_capacity = CONFIG.induction_lanes_per_module / CONFIG.induction_time_s
    total_lane_capacity = lane_capacity * CONFIG.num_modules
    margin = total_lane_capacity / target_pps
    return PerformanceCalc(
        target_items_per_hour=CONFIG.target_throughput_per_hour,
        target_items_per_second=round(target_pps, 2),
        modules=CONFIG.num_modules,
        per_module_items_per_hour=round(per_module_hour, 1),
        per_module_items_per_second=round(per_module_pps, 2),
        induction_lanes_per_module=CONFIG.induction_lanes_per_module,
        induction_capacity_per_module_pps=round(lane_capacity, 2),
        total_induction_capacity_pps=round(total_lane_capacity, 2),
        design_margin=round(margin, 2),
    )


def calc_area() -> AreaCalc:
    # Овальный контур кросс-белт модуля на 100 ячеек
    length_m = 58.0
    width_m = 26.0
    loop_length = 2 * (length_m - width_m) + 3.14159 * width_m
    module_area = length_m * width_m * 1.15  # проходы обслуживания
    sorter_area = module_area * CONFIG.num_modules
    aux_area = 2800.0  # индукция, КТЯ-станции, серверная, буферы
    total = sorter_area + aux_area
    return AreaCalc(
        modules=CONFIG.num_modules,
        module_loop_length_m=round(loop_length, 1),
        module_loop_width_m=width_m,
        module_area_m2=round(module_area, 1),
        total_sorter_area_m2=round(sorter_area, 1),
        aux_area_m2=aux_area,
        total_area_m2=round(total, 1),
        limit_m2=CONFIG.max_area_m2,
        area_utilization=round(total / CONFIG.max_area_m2, 3),
    )


def calc_energy(throughput_per_hour: int | None = None) -> EnergyCalc:
    throughput = throughput_per_hour or CONFIG.target_throughput_per_hour
    sorter_kw = CONFIG.power_per_module_kw * CONFIG.num_modules
    total_kw = sorter_kw + CONFIG.power_aux_kw
    wh_per_item = (total_kw * 1000) / max(throughput, 1)
    return EnergyCalc(
        sorter_power_kw=sorter_kw,
        aux_power_kw=CONFIG.power_aux_kw,
        total_power_kw=total_kw,
        energy_per_item_wh=round(wh_per_item, 2),
        energy_per_100k_items_kwh=round(wh_per_item * 100, 1),
    )


def main() -> None:
    output = {
        "performance": asdict(calc_performance()),
        "area": asdict(calc_area()),
        "energy": asdict(calc_energy()),
    }
    out_dir = Path(__file__).resolve().parent.parent / "simulation" / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "engineering_calculations.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    main()
