"""Дискретно-событийная модель модульного кросс-белт сортировщика."""

from __future__ import annotations

import random
from dataclasses import dataclass, field

import simpy

from control.balancer import InputBalancer
from control.routing_logic import NodeState, RoutingLogic
from control.wms_mock import WmsMock
from simulation.config import CONFIG, SystemConfig
from simulation.items import generate_item, kty_slots_for_item


@dataclass
class ItemStats:
    generated: int = 0
    sorted_correctly: int = 0
    misrouted: int = 0
    lost: int = 0
    damaged: int = 0
    rejected_no_route: int = 0


@dataclass
class KtyStats:
    swaps: int = 0
    full_events: int = 0
    compaction_events: int = 0


@dataclass
class SimulationMetrics:
    item_stats: ItemStats = field(default_factory=ItemStats)
    kty_stats: KtyStats = field(default_factory=KtyStats)
    wait_times: list[float] = field(default_factory=list)
    cycle_times: list[float] = field(default_factory=list)
    queue_samples: list[tuple[float, int]] = field(default_factory=list)
    throughput_samples: list[tuple[float, int]] = field(default_factory=list)
    jam_events: int = 0


class CrossBeltSorterSimulation:
    def __init__(
        self,
        config: SystemConfig = CONFIG,
        seed: int = 42,
        arrival_rate_per_hour: int | None = None,
        failed_chutes: set[int] | None = None,
        degraded_modules: set[int] | None = None,
    ) -> None:
        self.config = config
        self.seed = seed
        self.rng = random.Random(seed)
        self.env = simpy.Environment()
        self.wms = WmsMock(
            config.num_destinations,
            seed=seed,
            chutes_per_module=config.chutes_per_module,
        )
        self.routing = RoutingLogic(
            num_destinations=config.num_destinations,
            chute_buffer_capacity=config.chute_buffer_capacity,
            jam_threshold_queue=config.jam_threshold_queue,
            chutes_per_module=config.chutes_per_module,
        )
        self.balancer = InputBalancer(num_modules=config.num_modules)
        self.metrics = SimulationMetrics()
        self.arrival_rate_per_hour = arrival_rate_per_hour or config.target_throughput_per_hour
        self.failed_chutes = failed_chutes or set()
        self.degraded_modules = degraded_modules or set()

        for chute_id in self.failed_chutes:
            self.routing.set_chute_state(chute_id, NodeState.FAILED)

        for module_id in self.degraded_modules:
            self.balancer.set_degraded(module_id)

        self.induction_resources = [
            simpy.Resource(self.env, capacity=config.induction_lanes_per_module)
            for _ in range(config.num_modules)
        ]
        self.kty_swap_resources = [
            simpy.Resource(self.env, capacity=1) for _ in range(config.num_destinations)
        ]
        self.kty_fill: dict[int, float] = {i: 0.0 for i in range(1, config.num_destinations + 1)}
        self.kty_capacity: dict[int, int] = {}
        for chute_id in range(1, config.num_destinations + 1):
            cap = max(
                8,
                int(
                    self.rng.gauss(
                        config.kty_capacity_items_mean,
                        config.kty_capacity_items_std,
                    )
                ),
            )
            self.kty_capacity[chute_id] = cap

        self._processed_in_window = 0
        self._window_start = 0.0
        self._prev_congested: set[int] = set()

    def _sync_kty_fill(self, chute_id: int) -> None:
        ratio = self.kty_fill[chute_id] / self.kty_capacity[chute_id]
        self.routing.update_kty_fill(chute_id, ratio)

    def _module_index(self, destination: int) -> int:
        return (destination - 1) // self.config.chutes_per_module

    def _loop_transit_time(self, module_idx: int) -> float:
        base = max(1.0, self.rng.gauss(self.config.loop_transit_mean_s, self.config.loop_transit_std_s))
        if (module_idx + 1) in self.degraded_modules:
            return base * 1.35
        return base

    def _kty_swap_time(self) -> float:
        if self.config.use_auto_kty_swap:
            return self.config.kty_swap_time_auto_s
        return self.config.kty_swap_time_manual_s

    def kty_manager(self, chute_id: int) -> simpy.events.Process:
        def process() -> simpy.events.Generator:
            while True:
                fill_ratio = self.kty_fill[chute_id] / self.kty_capacity[chute_id]
                self.routing.update_kty_fill(chute_id, fill_ratio)

                if fill_ratio >= 0.88 and self.rng.random() < 0.15:
                    yield self.env.timeout(0.4)
                    self.kty_fill[chute_id] *= self.config.kty_compaction_ratio
                    self._sync_kty_fill(chute_id)
                    self.metrics.kty_stats.compaction_events += 1
                    continue

                if self.kty_fill[chute_id] >= self.kty_capacity[chute_id]:
                    self.metrics.kty_stats.full_events += 1
                    with self.kty_swap_resources[chute_id - 1].request() as swap_req:
                        yield swap_req
                        yield self.env.timeout(self._kty_swap_time())
                        self.kty_fill[chute_id] = 0.0
                        self.metrics.kty_stats.swaps += 1
                        self.routing.update_kty_fill(chute_id, 0.0)
                yield self.env.timeout(1.0)

        return self.env.process(process())

    def item_process(self, barcode: str, arrival_time: float, item_dims=None) -> simpy.events.Process:
        def process() -> simpy.events.Generator:
            start = self.env.now
            self.metrics.item_stats.generated += 1

            yield self.env.timeout(self.config.scan_time_s)
            decision = self.wms.resolve(barcode)
            yield self.env.timeout(self.config.wms_lookup_time_s)

            preferred = decision.destination
            destination = self.routing.select_destination(preferred)

            if destination is None:
                self.metrics.item_stats.rejected_no_route += 1
                self.metrics.item_stats.lost += 1
                return

            module_idx = self._module_index(destination)
            module_id = module_idx + 1
            self.routing.on_item_routed(destination)
            self.balancer.on_induction_start(module_id)

            with self.induction_resources[module_idx].request() as induction_req:
                yield induction_req
                yield self.env.timeout(self.config.induction_time_s)

            self.balancer.on_induction_end(module_id)

            yield self.env.timeout(self._loop_transit_time(module_idx))
            yield self.env.timeout(self.config.discharge_time_s)

            if self.rng.random() < 0.0008:
                self.metrics.item_stats.damaged += 1
                self.routing.on_item_discharged(destination)
                self.balancer.on_item_complete(module_id)
                return

            misrouted = destination != preferred
            if misrouted:
                self.metrics.item_stats.misrouted += 1
            else:
                self.metrics.item_stats.sorted_correctly += 1

            dims = item_dims or generate_item(self.rng)
            slots = kty_slots_for_item(dims, self.kty_capacity[destination])
            self.kty_fill[destination] += slots
            self._sync_kty_fill(destination)
            self.routing.on_item_discharged(destination)
            self.balancer.on_item_complete(module_id)

            cycle_time = self.env.now - start
            wait_time = start - arrival_time
            self.metrics.cycle_times.append(cycle_time)
            self.metrics.wait_times.append(wait_time)

            self._processed_in_window += 1
            if self.env.now - self._window_start >= 60:
                self.metrics.throughput_samples.append((self.env.now, self._processed_in_window))
                self._processed_in_window = 0
                self._window_start = self.env.now

        return self.env.process(process())

    def item_generator(self) -> simpy.events.Process:
        def process() -> simpy.events.Generator:
            rate_per_sec = self.arrival_rate_per_hour / 3600.0
            while True:
                inter_arrival = self.rng.expovariate(rate_per_sec)
                yield self.env.timeout(inter_arrival)
                arrival_time = self.env.now
                barcode = self.wms.generate_barcode()
                item_dims = generate_item(self.rng)
                self.item_process(barcode, arrival_time, item_dims)

        return self.env.process(process())

    def monitor(self, interval_s: float = 30.0) -> simpy.events.Process:
        def process() -> simpy.events.Generator:
            while True:
                congested = set(self.routing.congested_chutes())
                total_queue = sum(c.queue_depth for c in self.routing.chutes.values())
                self.metrics.queue_samples.append((self.env.now, total_queue))
                new_jams = congested - self._prev_congested
                self.metrics.jam_events += len(new_jams)
                self._prev_congested = congested
                yield self.env.timeout(interval_s)

        return self.env.process(process())

    def run(self, duration_s: float) -> SimulationMetrics:
        for chute_id in range(1, self.config.num_destinations + 1):
            self.kty_manager(chute_id)

        self.item_generator()
        self.monitor()
        self.env.run(until=duration_s)

        if self._processed_in_window > 0:
            self.metrics.throughput_samples.append((self.env.now, self._processed_in_window))

        return self.metrics
