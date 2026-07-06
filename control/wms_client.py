"""HTTP-клиент для WMS-имитатора."""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from control.wms_mock import RoutingDecision, WmsMock
from simulation.config import CONFIG


class WmsClient:
  def __init__(
    self,
    base_url: str = "http://localhost:8080",
    fallback: bool = True,
    seed: int = 42,
  ) -> None:
    self.base_url = base_url.rstrip("/")
    self.fallback = fallback
    self._local = WmsMock(
      CONFIG.num_destinations,
      seed=seed,
      chutes_per_module=CONFIG.chutes_per_module,
    )

  def _parse_decision(self, data: dict, barcode: str) -> RoutingDecision:
    destination = int(data["destination"])
    if not (1 <= destination <= CONFIG.num_destinations):
      raise ValueError(f"destination out of range: {destination}")
    return RoutingDecision(
      barcode=data.get("barcode", barcode),
      destination=destination,
      route_hint=data["route_hint"],
    )

  def resolve(self, barcode: str) -> RoutingDecision:
    url = f"{self.base_url}/route/{barcode}"
    try:
      with urllib.request.urlopen(url, timeout=0.5) as resp:
        data = json.loads(resp.read().decode("utf-8"))
      return self._parse_decision(data, barcode)
    except (urllib.error.URLError, TimeoutError, KeyError, ValueError):
      if self.fallback:
        return self._local.resolve(barcode)
      raise
