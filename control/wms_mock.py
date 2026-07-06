"""Имитация внешней складской системы (WMS)."""

from __future__ import annotations

import hashlib
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class RoutingDecision:
    barcode: str
    destination: int
    route_hint: str


class WmsMock:
    """Возвращает ячейку назначения по штрихкоду."""

    def __init__(self, num_destinations: int = 400, seed: int = 42) -> None:
        if num_destinations < 1:
            raise ValueError("num_destinations must be positive")
        self.num_destinations = num_destinations
        self._rng = random.Random(seed)

    def _stable_destination(self, barcode: str) -> int:
        digest = hashlib.sha256(barcode.encode("utf-8")).hexdigest()
        return int(digest, 16) % self.num_destinations + 1

    def resolve(self, barcode: str) -> RoutingDecision:
        destination = self._stable_destination(barcode)
        module = (destination - 1) // 100 + 1
        chute = (destination - 1) % 100 + 1
        return RoutingDecision(
            barcode=barcode,
            destination=destination,
            route_hint=f"M{module}-C{chute:03d}",
        )

    def generate_barcode(self) -> str:
        return f"OZ{self._rng.randint(10**11, 10**12 - 1)}"
