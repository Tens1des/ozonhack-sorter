#!/usr/bin/env python3
"""Генерация 2D-схемы компоновки (вид сверху)."""

from pathlib import Path

OUTPUT = Path(__file__).resolve().parent.parent / "cad" / "layout_top_view.svg"

MODULES = [
    (80, 60, "M1"),
    (280, 60, "M2"),
    (80, 200, "M3"),
    (280, 200, "M4"),
]


def oval(cx: float, cy: float, rx: float, ry: float) -> str:
    return (
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" '
        f'fill="#E8F0FE" stroke="#005BFF" stroke-width="2"/>'
    )


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="500" height="320" viewBox="0 0 500 320">',
        '<rect width="500" height="320" fill="#FAFAFA"/>',
        '<text x="250" y="24" text-anchor="middle" font-size="16" font-family="sans-serif" fill="#333">'
        "OzonHack — компоновка 4 кросс-белт модулей (вид сверху)</text>",
        '<rect x="30" y="40" width="440" height="260" fill="none" stroke="#CCC" stroke-dasharray="4"/>',
        '<text x="40" y="55" font-size="11" fill="#666">Входной распределитель</text>',
        '<rect x="200" y="45" width="100" height="30" fill="#005BFF" opacity="0.2" stroke="#005BFF"/>',
        '<text x="250" y="64" text-anchor="middle" font-size="10" fill="#005BFF">IN</text>',
    ]

    for cx, cy, label in MODULES:
        parts.append(oval(cx, cy, 70, 35))
        parts.append(
            f'<text x="{cx}" y="{cy + 4}" text-anchor="middle" font-size="14" '
            f'font-family="sans-serif" fill="#005BFF" font-weight="bold">{label}</text>'
        )
        parts.append(
            f'<text x="{cx}" y="{cy + 20}" text-anchor="middle" font-size="9" fill="#666">100 ячеек</text>'
        )

    parts.extend(
        [
            '<text x="250" y="305" text-anchor="middle" font-size="10" fill="#888">'
            "~9 737 м² | 400 направлений | 100 000 т/ч</text>",
            "</svg>",
        ]
    )

    OUTPUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()
