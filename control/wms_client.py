"""HTTP-клиент для WMS-имитатора."""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from control.wms_mock import RoutingDecision, WmsMock


class WmsClient:
  def __init__(self, base_url: str = "http://localhost:8080", fallback: bool = True) -> None:
    self.base_url = base_url.rstrip("/")
    self.fallback = fallback
    self._local = WmsMock(400)

  def resolve(self, barcode: str) -> RoutingDecision:
    url = f"{self.base_url}/route/{barcode}"
    try:
      with urllib.request.urlopen(url, timeout=0.5) as resp:
        data = json.loads(resp.read().decode("utf-8"))
      return RoutingDecision(
        barcode=data["barcode"],
        destination=int(data["destination"]),
        route_hint=data["route_hint"],
      )
    except (urllib.error.URLError, TimeoutError, KeyError, ValueError):
      if self.fallback:
        return self._local.resolve(barcode)
      raise
