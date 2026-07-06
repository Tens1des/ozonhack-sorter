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
  ctrl.complete_item(cmd.destination)


def test_item_dimensions_in_limits():
  rng = random.Random(0)
  for _ in range(100):
    item = generate_item(rng)
    assert item.fits_limits()
