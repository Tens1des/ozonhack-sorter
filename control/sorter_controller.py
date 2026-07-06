"""Высокоуровневый контроллер сортировщика."""

from __future__ import annotations

from dataclasses import dataclass

from control.balancer import InputBalancer
from control.routing_logic import RoutingLogic
from control.wms_client import WmsClient
from control.wms_mock import RoutingDecision
from simulation.config import CONFIG


@dataclass
class SortCommand:
  barcode: str
  destination: int
  module_id: int
  route_hint: str
  overflow: bool = False


class SorterController:
  def __init__(self, wms_url: str | None = None) -> None:
    self.wms = WmsClient(wms_url) if wms_url else WmsClient(fallback=True)
    self.routing = RoutingLogic(
      num_destinations=CONFIG.num_destinations,
      chute_buffer_capacity=CONFIG.chute_buffer_capacity,
      jam_threshold_queue=CONFIG.jam_threshold_queue,
      chutes_per_module=CONFIG.chutes_per_module,
    )
    self.balancer = InputBalancer(num_modules=CONFIG.num_modules)

  def process_barcode(self, barcode: str) -> SortCommand | None:
    decision: RoutingDecision = self.wms.resolve(barcode)
    destination = self.routing.select_destination(decision.destination)
    if destination is None:
      return None
    module_id = self.routing.module_for_destination(destination)
    self.routing.on_item_routed(destination)
    self.balancer.on_induction_start(module_id)
    return SortCommand(
      barcode=barcode,
      destination=destination,
      module_id=module_id,
      route_hint=decision.route_hint,
      overflow=destination != decision.destination,
    )

  def induction_complete(self, module_id: int) -> None:
    """Товар прошёл индукцию и вышел на контур модуля."""
    self.balancer.on_induction_end(module_id)

  def complete_item(self, destination: int) -> None:
    module_id = self.routing.module_for_destination(destination)
    self.balancer.on_induction_end(module_id)
    self.routing.on_item_discharged(destination)
    self.balancer.on_item_complete(module_id)
