"""Конфигурация модульного кросс-белт сортировщика OzonHack."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SystemConfig:
    # Целевые параметры задачи
    target_throughput_per_hour: int = 100_000
    num_destinations: int = 400
    max_area_m2: float = 20_000

    # Архитектура: 4 параллельных модуля по 100 направлений
    num_modules: int = 4
    chutes_per_module: int = 100
    induction_lanes_per_module: int = 4

    # Времена операций (секунды)
    scan_time_s: float = 0.05
    wms_lookup_time_s: float = 0.015
    induction_time_s: float = 0.12
    discharge_time_s: float = 0.18
    loop_transit_mean_s: float = 11.0
    loop_transit_std_s: float = 3.0

    # КТЯ
    kty_capacity_items_mean: int = 28
    kty_capacity_items_std: int = 5
    kty_compaction_ratio: float = 0.92
    kty_swap_time_manual_s: float = 45.0
    kty_swap_time_auto_s: float = 14.0
    use_auto_kty_swap: bool = True

    # Буферы ячеек
    chute_buffer_capacity: int = 12
    jam_threshold_queue: int = 8

    # Энергия (оценочные)
    power_per_module_kw: float = 85.0
    power_aux_kw: float = 120.0


CONFIG = SystemConfig()
