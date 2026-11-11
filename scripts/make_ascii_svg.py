#!/usr/bin/env python3
"""
Convert an avatar photo into an animated ASCII SVG portrait.
Dual-theme adaptive:
- Dark Mode: Dark background, light ink characters. Dark background = space, face/highlights = characters.
- Light Mode: Light background, dark ink characters. Inverted density mapping so face and features
  are drawn with ink while the light background remains clean white space.
"""
from PIL import Image, ImageEnhance, ImageOps
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "avatar-ascii.svg")

COLS = int(os.environ.get("COLS", 140))
ART_W_TARGET = 800
CELL_W = ART_W_TARGET / COLS
CELL_H = CELL_W * 15 / 8
ROWS = round(COLS * 8 / 15)
RAMP = " .`:-=+*cs#%@"

PAD = 20
TITLEBAR_H = 34
CANVAS_W = 840
CANVAS_H = 880

BASE_START = 0.65
TOTAL_TYPE_DUR = 0.65
ROW_DUR = 0.05
STAGGER = TOTAL_TYPE_DUR / ROWS

im = Image.open(SRC).convert("L")
im = ImageOps.autocontrast(im, cutoff=2)
im = ImageEnhance.Contrast(im).enhance(1.4)
im = im.resize((COLS, ROWS), Image.Resampling.LANCZOS)
px = im.load()

# Dark theme: higher brightness = denser character
dark_rows = []
# Light theme: inverted brightness so darker facial features/hair get dense ink, light/transparent bg stays empty space
light_rows = []

for y in range(ROWS):
    d_chars = []
    l_chars = []
    for x in range(COLS):
        val = px[x, y]
        # Dark mode index
        d_idx = int(val / 256 * len(RAMP))
        d_idx = max(0, min(len(RAMP) - 1, d_idx))
        d_chars.append(RAMP[d_idx])

        # Light mode index (inverted)
        l_idx = int((255 - val) / 256 * len(RAMP))
        l_idx = max(0, min(len(RAMP) - 1, l_idx))
        l_chars.append(RAMP[l_idx])

    dark_rows.append("".join(d_chars))
    light_rows.append("".join(l_chars))

css = f"""
:root {{
  --bg-top: #111722;
  --bg-bot: #0d1117;
  --frame: #30363d;
  --sep: #30363d;
  --title: #7d8590;
  --ink: #c9d1d9;
  --cursor: #58a6ff;
}}
@media (prefers-color-scheme: light) {{
  :root {{
    --bg-top: #ffffff;
    --bg-bot: #f6f8fa;
    --frame: #d0d7de;
    --sep: #d8dee4;
    --title: #656d76;
    --ink: #1f2328;
    --cursor: #0969da;
  }}
  .row-dark {{ display: none !important; }}
  .row-light {{ display: inline !important; }}
}}
@media (prefers-color-scheme: dark) {{
  .row-light {{ display: none !important; }}
  .row-dark {{ display: inline !important; }}
}}
/* Default fallback when prefers-color-scheme is not supported */
.row-light {{ display: none; }}

.card-frame {{ stroke: var(--frame); stroke-width: 1.2px; }}
.sep-line {{ stroke: var(--sep); }}
.txt-title {{ fill: var(--title); }}
.txt-ink {{ fill: var(--ink); }}
.cursor-bar {{ fill: var(--cursor); }}
""".strip()

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{CANVAS_W}" height="{CANVAS_H}" '
    f'viewBox="0 0 {CANVAS_W} {CANVAS_H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    f'<style>{css}</style>',
    '<defs>',
    f'<linearGradient id="bg_ascii" x1="0" y1="0" x2="0" y2="1">',
    f'<stop offset="0" stop-color="var(--bg-top)"/><stop offset="1" stop-color="var(--bg-bot)"/>',
    f'</linearGradient></defs>',
    f'<rect width="{CANVAS_W}" height="{CANVAS_H}" rx="12" fill="url(#bg_ascii)"/>',
    f'<rect class="card-frame" x="0.6" y="0.6" width="{CANVAS_W-1.2:.1f}" height="{CANVAS_H-1.2:.1f}" rx="12" fill="none"/>',
    f'<line class="sep-line" x1="0" y1="{TITLEBAR_H}" x2="{CANVAS_W}" y2="{TITLEBAR_H}"/>',
]

for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(f'<text class="txt-title" x="{CANVAS_W/2}" y="{TITLEBAR_H/2 + 4}" font-size="12" text-anchor="middle">ASCII Portrait</text>')

for y in range(ROWS):
    clip_id = f"r{y}"
    row_y = TITLEBAR_H + PAD + y * CELL_H
    t_start = BASE_START + y * STAGGER
    t_end = t_start + ROW_DUR

    parts.append(f'<clipPath id="{clip_id}">')
    parts.append(f'<rect x="{PAD}" y="{row_y:.1f}" height="{CELL_H:.1f}" width="0">')
    parts.append(f'<animate attributeName="width" from="0" to="{ART_W_TARGET:.1f}" begin="{t_start:.3f}s" dur="{ROW_DUR:.2f}s" fill="freeze"/>')
    parts.append('</rect></clipPath>')

    d_esc = html.escape(dark_rows[y])
    l_esc = html.escape(light_rows[y])

    parts.append(f'<g clip-path="url(#{clip_id})">')
    # Dark mode text node
    parts.append(
        f'<text class="txt-ink row-dark" xml:space="preserve" x="{PAD}" y="{row_y + CELL_H * 0.74:.1f}" '
        f'font-size="{CELL_H * 0.9:.1f}" textLength="{ART_W_TARGET:.1f}" lengthAdjust="spacing">{d_esc}</text>'
    )
    # Light mode text node (inverted density)
    parts.append(
        f'<text class="txt-ink row-light" xml:space="preserve" x="{PAD}" y="{row_y + CELL_H * 0.74:.1f}" '
        f'font-size="{CELL_H * 0.9:.1f}" textLength="{ART_W_TARGET:.1f}" lengthAdjust="spacing">{l_esc}</text>'
    )
    parts.append('</g>')

    parts.append(
        f'<rect class="cursor-bar" y="{row_y + 1:.1f}" width="{CELL_W:.1f}" height="{CELL_H - 1:.1f}" opacity="0">'
        f'<animate attributeName="x" from="{PAD}" to="{PAD + ART_W_TARGET:.1f}" begin="{t_start:.3f}s" dur="{ROW_DUR:.2f}s" fill="freeze"/>'
        f'<set attributeName="opacity" to="0.85" begin="{t_start:.3f}s"/>'
        f'<set attributeName="opacity" to="0" begin="{t_end:.3f}s"/>'
        f'</rect>'
    )

parts.append('</svg>')
svg = "".join(parts)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"wrote {OUT} ({len(svg)} bytes)")
