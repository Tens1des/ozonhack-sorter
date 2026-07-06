#!/usr/bin/env python3
"""Генерация SVG-диаграмм: поток процессов и кинематика."""

from pathlib import Path

CAD = Path(__file__).resolve().parent.parent / "cad"


def process_flow() -> None:
    svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="720" height="200" viewBox="0 0 720 200">
  <rect width="720" height="200" fill="#FAFAFA"/>
  <text x="360" y="22" text-anchor="middle" font-size="14" font-family="sans-serif" fill="#333">Поток обработки товара</text>
  <g font-family="sans-serif" font-size="11">
    <rect x="10" y="60" width="80" height="40" rx="6" fill="#E8F0FE" stroke="#005BFF"/>
    <text x="50" y="85" text-anchor="middle" fill="#005BFF">Вход</text>
    <rect x="110" y="60" width="80" height="40" rx="6" fill="#E8F0FE" stroke="#005BFF"/>
    <text x="150" y="85" text-anchor="middle" fill="#005BFF">Сканер</text>
    <rect x="210" y="60" width="80" height="40" rx="6" fill="#E8F0FE" stroke="#005BFF"/>
    <text x="250" y="85" text-anchor="middle" fill="#005BFF">WMS</text>
    <rect x="310" y="60" width="80" height="40" rx="6" fill="#E8F0FE" stroke="#005BFF"/>
    <text x="350" y="85" text-anchor="middle" fill="#005BFF">Индукция</text>
    <rect x="410" y="60" width="80" height="40" rx="6" fill="#E8F0FE" stroke="#005BFF"/>
    <text x="450" y="85" text-anchor="middle" fill="#005BFF">Контур</text>
    <rect x="510" y="60" width="80" height="40" rx="6" fill="#E8F0FE" stroke="#005BFF"/>
    <text x="550" y="85" text-anchor="middle" fill="#005BFF">Сброс</text>
    <rect x="610" y="60" width="90" height="40" rx="6" fill="#E6F7EE" stroke="#00A86B"/>
    <text x="655" y="85" text-anchor="middle" fill="#00A86B">КТЯ</text>
  </g>
  <g stroke="#999" stroke-width="1.5" marker-end="url(#arrow)">
    <defs><marker id="arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#999"/></marker></defs>
    <line x1="90" y1="80" x2="110" y2="80"/><line x1="190" y1="80" x2="210" y2="80"/>
    <line x1="290" y1="80" x2="310" y2="80"/><line x1="390" y1="80" x2="410" y2="80"/>
    <line x1="490" y1="80" x2="510" y2="80"/><line x1="590" y1="80" x2="610" y2="80"/>
  </g>
  <text x="655" y="140" text-anchor="middle" font-size="10" fill="#666">уплотнение → смена</text>
</svg>"""
    (CAD / "process_flow.svg").write_text(svg, encoding="utf-8")


def kinematic_scheme() -> None:
    svg = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="500" height="280" viewBox="0 0 500 280">
  <rect width="500" height="280" fill="#FAFAFA"/>
  <text x="250" y="22" text-anchor="middle" font-size="14" font-family="sans-serif">Кинематическая схема модуля</text>
  <ellipse cx="250" cy="150" rx="180" ry="70" fill="none" stroke="#005BFF" stroke-width="2" stroke-dasharray="6"/>
  <text x="250" y="155" text-anchor="middle" font-size="11" fill="#005BFF">Контур 2,5 м/с</text>
  <rect x="60" y="135" width="30" height="20" fill="#7B61FF" stroke="#333"/>
  <text x="75" y="170" text-anchor="middle" font-size="9">Тележка</text>
  <rect x="120" y="130" width="40" height="8" fill="#F5A623"/>
  <text x="140" y="125" text-anchor="middle" font-size="9">Поперечная лента</text>
  <rect x="230" y="55" width="40" height="25" fill="#E8F0FE" stroke="#005BFF"/>
  <text x="250" y="45" text-anchor="middle" font-size="9">Индукция</text>
  <path d="M 350 150 L 420 150 L 420 200 L 380 220" fill="none" stroke="#00A86B" stroke-width="2"/>
  <rect x="400" y="200" width="50" height="35" fill="#E6F7EE" stroke="#00A86B"/>
  <text x="425" y="222" text-anchor="middle" font-size="9">КТЯ</text>
  <text x="250" y="260" text-anchor="middle" font-size="10" fill="#888">Овал 58×26 м | 100 ячеек сброса</text>
</svg>"""
    (CAD / "kinematic_scheme.svg").write_text(svg, encoding="utf-8")


def main() -> None:
    CAD.mkdir(parents=True, exist_ok=True)
    process_flow()
    kinematic_scheme()
    print(f"Saved: {CAD / 'process_flow.svg'}")
    print(f"Saved: {CAD / 'kinematic_scheme.svg'}")


if __name__ == "__main__":
    main()
