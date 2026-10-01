"""Exporta el Markdown del E1 a PDF y verifica el máximo de 15 páginas."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import markdown
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "entregable1" / "e1_tiendacol.md"
OUTPUT = ROOT / "docs" / "entregable1" / "e1_tiendacol.pdf"

CSS = r"""
@page {
  size: A4;
  margin: 9mm 10mm 11mm;
  @bottom-center {
    content: "TiendaCol · E1 · " counter(page) " / " counter(pages);
    color: #617386;
    font: 7pt Arial, sans-serif;
  }
}
@page:first { @bottom-center { content: none; } }
* { box-sizing: border-box; }
html { font-family: Arial, sans-serif; color: #232f3e; }
body { font-size: 8.1pt; line-height: 1.16; margin: 0; }
h1, h2, h3 { color: #183b56; page-break-after: avoid; }
h1 { font-size: 15pt; margin: 5mm 0 2.2mm; }
h2 { font-size: 11.5pt; margin: 3.5mm 0 1.5mm; }
h3 { font-size: 9.5pt; margin: 2.5mm 0 1mm; }
p { margin: 1.2mm 0; orphans: 2; widows: 2; }
ul, ol { margin: 1.2mm 0 1.2mm 4.5mm; padding-left: 3mm; }
li { margin: .5mm 0; }
table { width: 100%; border-collapse: collapse; margin: 1.5mm 0 2mm; font-size: 6.4pt; line-height: 1.1; page-break-inside: auto; }
thead { display: table-header-group; }
tr { page-break-inside: avoid; }
th, td { border: .25pt solid #9aa9b5; padding: 1.05mm; vertical-align: top; overflow-wrap: anywhere; }
th { background: #eaf0f4; color: #183b56; font-weight: 700; }
code { font-family: Consolas, monospace; font-size: .9em; overflow-wrap: anywhere; }
pre { white-space: pre-wrap; font-size: 6.4pt; line-height: 1.1; padding: 1.5mm; background: #f5f7f8; }
blockquote { margin: 1.5mm 0; padding-left: 3mm; border-left: 1mm solid #8bb12b; color: #445566; }
img { display: block; max-width: 100%; max-height: 176mm; margin: 2mm auto; object-fit: contain; }
a { color: #1565a8; text-decoration: none; }
hr { border: 0; border-top: .4pt solid #b6c2ca; margin: 2mm 0; }
"""


def chrome_path() -> Path | None:
    candidates = (
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate
    executable = shutil.which("chrome") or shutil.which("google-chrome")
    return Path(executable) if executable else None


def main() -> int:
    chrome = chrome_path()
    if chrome is None:
        print("ERROR: no se encontró Google Chrome.", file=sys.stderr)
        return 2

    source = SOURCE.read_text(encoding="utf-8")
    body = markdown.markdown(
        source,
        extensions=["tables", "fenced_code", "sane_lists"],
        output_format="html5",
    )
    document = (
        "<!doctype html><html lang='es'><head><meta charset='utf-8'>"
        f"<base href='{SOURCE.parent.as_uri()}/'>"
        "<title>TiendaCol en tiempo real — Entregable 1</title>"
        f"<style>{CSS}</style></head><body>{body}</body></html>"
    )

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", encoding="utf-8", delete=False
    ) as temporary:
        temporary.write(document)
        html_path = Path(temporary.name)
    try:
        result = subprocess.run(
            [
                str(chrome),
                "--headless",
                "--disable-gpu",
                "--no-pdf-header-footer",
                f"--print-to-pdf={OUTPUT}",
                html_path.as_uri(),
            ],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        if result.returncode != 0 or not OUTPUT.exists():
            print(result.stderr, file=sys.stderr)
            print("ERROR: Chrome no generó el PDF.", file=sys.stderr)
            return 2
    finally:
        html_path.unlink(missing_ok=True)

    reader = PdfReader(str(OUTPUT))
    annex_page = next(
        (
            number
            for number, page in enumerate(reader.pages, start=1)
            if "Anexo A. Supuestos" in (page.extract_text() or "")
        ),
        None,
    )
    if annex_page is None:
        print("ERROR: no se encontró el inicio del Anexo A.", file=sys.stderr)
        return 2

    body_pages = annex_page - 1
    print(f"PDF: {OUTPUT}")
    print(f"Páginas totales: {len(reader.pages)}")
    print(f"Páginas antes del Anexo A: {body_pages}")
    if body_pages > 15:
        print("ERROR: el cuerpo supera el máximo de 15 páginas.", file=sys.stderr)
        return 1
    print("OK: el cuerpo cumple el máximo de 15 páginas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
