"""Тесты контроллера и клиента WMS."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
  sys.path.insert(0, str(ROOT))

from control.sorter_controller import SorterController
from control.wms_client import WmsClient
from simulation.items import generate_item
import random


def test_wms_client_fallback():
  client = WmsClient("http://127.0.0.1:1", fallback=True)
  d = client.resolve("OZ999")
  assert 1 <= d.destination <= 400


def test_sorter_controller():
  ctrl = SorterController()
  cmd = ctrl.process_barcode("OZ111222333")
  assert cmd is not None
  assert 1 <= cmd.destination <= 400
  module = ctrl.balancer.modules[cmd.module_id]
  assert module.induction_queue == 1
  ctrl.complete_item(cmd.destination)
  assert module.induction_queue == 0
  assert module.active_items == 0


def test_routing_invalid_destination():
  from control.routing_logic import RoutingLogic

  routing = RoutingLogic(400, chute_buffer_capacity=12, jam_threshold_queue=8)
  dest = routing.select_destination(999)
  assert dest is not None
  assert 1 <= dest <= 400


def test_item_dimensions_in_limits():
  rng = random.Random(0)
  for _ in range(100):
    item = generate_item(rng)
    assert item.fits_limits()
