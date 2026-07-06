"""HTTP-имитатор WMS для демонстрации и проверки экспертами."""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from control.wms_mock import WmsMock

WMS = WmsMock(400, seed=42)


class WmsHandler(BaseHTTPRequestHandler):
    def _send_json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path in ("/", "/health"):
            self._send_json(200, {"status": "ok", "service": "wms-mock"})
            return
        if self.path.startswith("/route/"):
            barcode = self.path.split("/route/", 1)[1]
            if not barcode:
                self._send_json(400, {"error": "barcode required"})
                return
            decision = WMS.resolve(barcode)
            self._send_json(
                200,
                {
                    "barcode": decision.barcode,
                    "destination": decision.destination,
                    "route_hint": decision.route_hint,
                },
            )
            return
        self._send_json(404, {"error": "not found"})

    def log_message(self, format: str, *args) -> None:
        return


def main() -> None:
    parser = argparse.ArgumentParser(description="WMS mock HTTP server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    server = HTTPServer((args.host, args.port), WmsHandler)
    print(f"WMS mock: http://{args.host}:{args.port}/route/<barcode>")
    server.serve_forever()


if __name__ == "__main__":
    main()
