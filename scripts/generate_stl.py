#!/usr/bin/env python3
"""Генерация упрощённых STL-моделей (без внешних зависимостей)."""

from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "cad" / "models"


def write_box_stl(path: Path, name: str, sx: float, sy: float, sz: float) -> None:
    """Прямоугольный параллелепипед в ASCII STL."""
    hx, hy, hz = sx / 2, sy / 2, sz / 2
    verts = [
        (-hx, -hy, -hz), (hx, -hy, -hz), (hx, hy, -hz), (-hx, hy, -hz),
        (-hx, -hy, hz), (hx, -hy, hz), (hx, hy, hz), (-hx, hy, hz),
    ]
    faces = [
        (0, 1, 2), (0, 2, 3), (4, 6, 5), (4, 7, 6), (0, 4, 5), (0, 5, 1),
        (2, 6, 7), (2, 7, 3), (0, 3, 7), (0, 7, 4), (1, 5, 6), (1, 6, 2),
    ]
    lines = [f"solid {name}"]
    for f in faces:
        v0, v1, v2 = (verts[i] for i in f)
        lines.append("  facet normal 0 0 0")
        lines.append("    outer loop")
        for v in (v0, v1, v2):
            lines.append(f"      vertex {v[0]} {v[1]} {v[2]}")
        lines.append("    endloop")
        lines.append("  endfacet")
    lines.append(f"endsolid {name}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_box_obj(path: Path, name: str, sx: float, sy: float, sz: float) -> None:
    hx, hy, hz = sx / 2, sy / 2, sz / 2
    verts = [
        (-hx, -hy, -hz), (hx, -hy, -hz), (hx, hy, -hz), (-hx, hy, -hz),
        (-hx, -hy, hz), (hx, -hy, hz), (hx, hy, hz), (-hx, hy, hz),
    ]
    faces = [
        (1, 2, 3, 4), (5, 8, 7, 6), (1, 5, 6, 2), (3, 7, 8, 4),
        (1, 4, 8, 5), (2, 6, 7, 3),
    ]
    lines = [f"# {name}", f"o {name}"]
    for v in verts:
        lines.append(f"v {v[0]} {v[1]} {v[2]}")
    for f in faces:
        lines.append("f " + " ".join(str(i) for i in f))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    write_box_stl(OUT / "kty_box.stl", "kty_box", 0.6, 0.4, 0.3)
    write_box_stl(OUT / "module_footprint.stl", "module_footprint", 58.0, 26.0, 0.15)
    write_box_stl(OUT / "carriage.stl", "carriage", 0.8, 0.6, 0.25)
    write_box_obj(OUT / "kty_box.obj", "kty_box", 0.6, 0.4, 0.3)
    write_box_obj(OUT / "module_footprint.obj", "module_footprint", 58.0, 26.0, 0.15)
    print(f"Saved STL/OBJ models to {OUT}")


if __name__ == "__main__":
    main()
