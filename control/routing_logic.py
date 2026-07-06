"""Логика маршрутизации и антизатор для сортировщика."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class NodeState(str, Enum):
    ACTIVE = "active"
    DEGRADED = "degraded"
    FAILED = "failed"


@dataclass
class ChuteState:
    chute_id: int
    state: NodeState = NodeState.ACTIVE
    queue_depth: int = 0
    kty_fill_ratio: float = 0.0


@dataclass
class RoutingLogic:
    num_destinations: int
    chute_buffer_capacity: int
    jam_threshold_queue: int
    chutes_per_module: int = 100
    chutes: dict[int, ChuteState] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.chutes:
            self.chutes = {
                i: ChuteState(chute_id=i) for i in range(1, self.num_destinations + 1)
            }

    def module_for_destination(self, destination: int) -> int:
        return (destination - 1) // self.chutes_per_module + 1

    def is_valid_destination(self, destination: int) -> bool:
        return 1 <= destination <= self.num_destinations

    def can_accept(self, destination: int) -> bool:
        if not self.is_valid_destination(destination):
            return False
        chute = self.chutes[destination]
        if chute.state == NodeState.FAILED:
            return False
        if chute.queue_depth >= self.chute_buffer_capacity:
            return False
        if chute.kty_fill_ratio >= 0.98:
            return False
        return True

    def select_destination(self, preferred: int) -> int | None:
        if self.is_valid_destination(preferred) and self.can_accept(preferred):
            return preferred

        if self.is_valid_destination(preferred):
            module = self.module_for_destination(preferred)
            module_range = range(
                (module - 1) * self.chutes_per_module + 1,
                module * self.chutes_per_module + 1,
            )

            candidates = [
                chute_id
                for chute_id in module_range
                if self.can_accept(chute_id)
                and self.chutes[chute_id].queue_depth < self.jam_threshold_queue
            ]
            if candidates:
                return min(candidates, key=lambda c: self.chutes[c].queue_depth)

        overflow = [
            chute_id
            for chute_id in range(1, self.num_destinations + 1)
            if self.can_accept(chute_id)
        ]
        if not overflow:
            return None
        return min(overflow, key=lambda c: self.chutes[c].queue_depth)

    def on_item_routed(self, destination: int) -> None:
        self.chutes[destination].queue_depth += 1

    def on_item_discharged(self, destination: int) -> None:
        chute = self.chutes[destination]
        chute.queue_depth = max(0, chute.queue_depth - 1)

    def update_kty_fill(self, destination: int, fill_ratio: float) -> None:
        self.chutes[destination].kty_fill_ratio = min(1.0, max(0.0, fill_ratio))

    def set_chute_state(self, destination: int, state: NodeState) -> None:
        self.chutes[destination].state = state

    def congested_chutes(self) -> list[int]:
        return [
            chute_id
            for chute_id, chute in self.chutes.items()
            if chute.queue_depth >= self.jam_threshold_queue
            or chute.kty_fill_ratio >= 0.95
        ]
