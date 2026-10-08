"""Stamp a source note at the bottom right of a figure.

- Matplotlib figures (fig.ipynb) go through ``save_with_source``.
- Static images with no generating code are kept untouched in ``raw/`` and stamped
  by running this file as a script (``python source_note.py``).
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

NOTE_STYLE = dict(fontsize=9, style="italic", color="#555555")
GAP_IN = 0.08  # vertical gap between the lowest artist and the note (inches)


def save_with_note(fig, path, text, dpi=300):
    """Save ``fig`` to ``path`` with ``text`` right-aligned below everything else drawn."""
    fig.canvas.draw()
    bbox = fig.get_tightbbox(fig.canvas.get_renderer())  # inches, includes legends/labels
    note = fig.text(bbox.x1 / fig.get_figwidth(), (bbox.y0 - GAP_IN) / fig.get_figheight(),
                    text, ha="right", va="top", **NOTE_STYLE)
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    note.remove()
    print(f"Figure saved to: {path}")


def save_with_source(fig, path, source, dpi=300):
    """Save ``fig`` to ``path`` with a "Source: ..." note."""
    save_with_note(fig, path, f"Source: {source}", dpi)


# ── Static images ────────────────────────────────────────────────────────────
STATIC_SOURCES = {
    "map_textile": "BPS, authors' calculation.",
    "footwear_supply_chain": "DEN.",
    "footwear_production_process": "DEN (2025), based on site visits and interviews with footwear manufacturers.",
    "map_footwear": "APRISINDO (2025); DEN analysis.",
    "machinery_modernization": "DEN, ITMF, Gherzi.",
    "workforce_projection": "Ministry of Manpower.",
    "investment_pipeline": "DEN.",
    "licensing_time": "DEN.",
}


def _italic_font(px):
    for name in ("DejaVuSans-Oblique.ttf", "ariali.ttf"):
        try:
            return ImageFont.truetype(name, px)
        except OSError:
            pass
    from matplotlib import font_manager
    return ImageFont.truetype(font_manager.findfont("DejaVu Sans:italic"), px)


def stamp_image(src, out, text):
    """Append a white strip under ``src`` with ``text`` right-aligned, and save to ``out``."""
    img = Image.open(src).convert("RGB")
    w, h = img.size
    font = _italic_font(max(12, round(w * 0.013)))
    left, top, right, bottom = font.getbbox(text)
    pad = round(font.size * 0.6)
    canvas = Image.new("RGB", (w, h + (bottom - top) + 2 * pad), "white")
    canvas.paste(img, (0, 0))
    ImageDraw.Draw(canvas).text((w - pad - right, h + pad - top), text, font=font, fill="#555555")
    canvas.save(out, dpi=img.info.get("dpi", (300, 300)))


if __name__ == "__main__":
    here = Path(__file__).parent
    for name, source in STATIC_SOURCES.items():
        stamp_image(here / "raw" / f"{name}.png", here / f"{name}.png", f"Source: {source}")
        print(f"Stamped {name}.png")
