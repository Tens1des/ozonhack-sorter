"""Модель товара с габаритами и весом по ТЗ."""

from __future__ import annotations

import random
from dataclasses import dataclass


@dataclass(frozen=True)
class ItemDimensions:
    length_mm: float
    width_mm: float
    height_mm: float
    weight_g: float
    is_flat: bool

    @property
    def volume_mm3(self) -> float:
        return self.length_mm * self.width_mm * self.height_mm

    def fits_limits(self) -> bool:
        dims = sorted([self.length_mm, self.width_mm, self.height_mm])
        lo = sorted([15.0, 35.0, 10.0])
        hi = sorted([400.0, 320.0, 280.0])
        return (
            lo[0] <= dims[0] <= hi[0]
            and lo[1] <= dims[1] <= hi[1]
            and lo[2] <= dims[2] <= hi[2]
            and 10 <= self.weight_g <= 5000
        )


def generate_item(rng: random.Random) -> ItemDimensions:
    """Генерация товара в допустимых пределах ТЗ."""
    for _ in range(50):
        if rng.random() < 0.12:
            item = ItemDimensions(
                length_mm=rng.uniform(120, 400),
                width_mm=rng.uniform(80, 320),
                height_mm=rng.uniform(10, 25),
                weight_g=rng.uniform(10, 800),
                is_flat=True,
            )
        else:
            item = ItemDimensions(
                length_mm=rng.uniform(15, 400),
                width_mm=rng.uniform(35, 320),
                height_mm=rng.uniform(10, 280),
                weight_g=rng.uniform(10, 5000),
                is_flat=False,
            )
        if item.fits_limits():
            return item
    return ItemDimensions(100.0, 50.0, 30.0, 200.0, False)


def kty_slots_for_item(item: ItemDimensions, base_capacity: int) -> float:
    """Доля ёмкости КТЯ, занимаемая товаром (калибровано под ~99% точности)."""
    ref_volume = 200.0 * 100.0 * 60.0
    ratio = item.volume_mm3 / ref_volume
    return max(0.35, min(1.0, ratio**0.55))
