#!/usr/bin/env python3
"""Генерация печатного HTML-отчёта из markdown."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / "docs" / "report.md"
OUT = ROOT / "docs" / "report.html"

STYLE = """
body { font-family: Georgia, serif; max-width: 800px; margin: 40px auto; padding: 0 20px; line-height: 1.6; color: #222; }
h1 { color: #005BFF; border-bottom: 2px solid #005BFF; padding-bottom: 8px; }
h2 { color: #333; margin-top: 2em; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; }
th, td { border: 1px solid #ccc; padding: 8px 12px; text-align: left; }
th { background: #f0f4ff; }
code { background: #f5f5f5; padding: 2px 6px; border-radius: 3px; }
@media print { body { margin: 0; } }
"""


def md_to_html(text: str) -> str:
    lines = text.splitlines()
    html: list[str] = []
    in_table = False

    for line in lines:
        if line.startswith("# "):
            html.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            html.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("---"):
            html.append("<hr>")
        elif line.startswith("|") and "|" in line[1:]:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if all(set(c) <= set("- ") for c in cells):
                continue
            tag = "th" if not in_table else "td"
            row = "".join(f"<{tag}>{c}</{tag}>" for c in cells)
            if not in_table:
                html.append("<table>")
                in_table = True
            html.append(f"<tr>{row}</tr>")
        else:
            if in_table:
                html.append("</table>")
                in_table = False
            if line.strip().startswith("- "):
                html.append(f"<li>{line.strip()[2:]}</li>")
            elif line.strip():
                html.append(f"<p>{line}</p>")
    if in_table:
        html.append("</table>")
    return "\n".join(html)


def main() -> None:
    body = md_to_html(MD.read_text(encoding="utf-8"))
    doc = f"""<!DOCTYPE html>
<html lang="ru"><head><meta charset="UTF-8"><title>OzonHack — Отчёт</title>
<style>{STYLE}</style></head><body>{body}
<p style="margin-top:3em;color:#888;font-size:0.9em">OzonHack Трек 2 — сгенерировано автоматически</p>
</body></html>"""
    OUT.write_text(doc, encoding="utf-8")
    print(f"Saved: {OUT}")


if __name__ == "__main__":
    main()
