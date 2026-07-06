"""Базовые тесты WMS и маршрутизации."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from control.routing_logic import NodeState, RoutingLogic
from control.wms_mock import WmsMock


def test_wms_stable_destination():
    wms = WmsMock(400, seed=1)
    a = wms.resolve("OZ111")
    b = wms.resolve("OZ111")
    assert a.destination == b.destination
    assert 1 <= a.destination <= 400


def test_routing_overflow():
    routing = RoutingLogic(400, chute_buffer_capacity=2, jam_threshold_queue=1)
    routing.chutes[42].queue_depth = 2
    dest = routing.select_destination(42)
    assert dest != 42
    assert dest is not None


def test_failed_chute():
    routing = RoutingLogic(400, chute_buffer_capacity=12, jam_threshold_queue=8)
    routing.set_chute_state(10, NodeState.FAILED)
    assert routing.can_accept(10) is False
    dest = routing.select_destination(10)
    assert dest != 10
