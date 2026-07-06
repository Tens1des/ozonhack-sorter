"""Тесты балансировщика."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from control.balancer import InputBalancer


def test_balancer_picks_least_loaded():
    b = InputBalancer(num_modules=4)
    b.modules[1].active_items = 50
    b.modules[2].active_items = 10
    b.modules[3].active_items = 30
    b.modules[4].active_items = 25
    assert b.select_module() == 2


def test_balancer_skips_failed():
    b = InputBalancer(num_modules=4)
    b.set_failed(1)
    b.set_failed(3)
    selected = b.select_module()
    assert selected in (2, 4)
