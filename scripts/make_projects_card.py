#!/usr/bin/env python3
"""
Generates an animated Featured Projects SVG (860x260):
- 2x2 grid of modern terminal cards matching the profile theme
- Starts writing at ~8.5s right after the Languages & Tools animation finishes
- Projects slide up with title, tech stack badge, and description, then hold
"""
import html
import os

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "projects-card.svg")

W = 860
H = 260
PAD = 12
GAP = 14

BG = "#0d1117"
BG2 = "#111722"
TILE = "#161b22"
FRAME = "#30363d"
MUTED = "#8b949e"
TEXT = "#c9d1d9"
CYAN = "#58a6ff"
GREEN = "#39d353"
GOLD = "#f2cc60"
PURPLE = "#bc8cff"

PROJECTS = [
    {
        "icon": "📦",
        "title": "Ecommerce-big-Data-Analysis",
        "tag": "PYTHON • BIG DATA",
        "tag_color": CYAN,
        "desc": "Data pipeline & consumer transaction analytics evaluating sales patterns and high-volume data."
    },
    {
        "icon": "🤝",
        "title": "NGO-Data-Analysis",
        "tag": "EDA • METRICS",
        "tag_color": GREEN,
        "desc": "Exploratory data analysis & socioeconomic indicators modeled for non-profit operational decisions."
    },
    {
        "icon": "📊",
        "title": "Titanic-Excel-Analysis",
        "tag": "EXCEL • ML • PYTHON",
        "tag_color": GOLD,
        "desc": "Structured exploratory data analysis, statistical modeling, and survival classification insights."
    },
    {
        "icon": "📫",
        "title": "Connect With Me",
        "tag": "NETWORKING • OPEN TO WORK",
        "tag_color": PURPLE,
        "desc": "Always open to data analyst collaborations, predictive modeling projects, and opportunities."
    }
]

def render_projects_card():
    # Languages & Tools runs from 6.8s to ~8.4s.
    # Projects card starts right after at 8.5s!
    BASE_START = 8.5
    STAGGER = 0.22

    css = """
.tile {
  opacity: 0;
  animation: tileSlide 0.55s cubic-bezier(0.22, 1, 0.36, 1) both;
}
@keyframes tileSlide {
  0% {
    opacity: 0;
    transform: translateY(16px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
@media (prefers-reduced-motion: reduce) {
  .tile { opacity: 1 !important; transform: none !important; animation: none !important; }
}
"""

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">',
        f'<style>{css}</style>',
        '<defs>',
        f'<linearGradient id="tile_bg" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{TILE}"/>',
        '</linearGradient>',
        '</defs>',
    ]

    tile_w = (W - PAD * 2 - GAP) / 2
    tile_h = (H - PAD * 2 - GAP) / 2

    for idx, p in enumerate(PROJECTS):
        col = idx % 2
        row = idx // 2
        x = PAD + col * (tile_w + GAP)
        y = PAD + row * (tile_h + GAP)
        delay = BASE_START + (idx * STAGGER)

        title = html.escape(p["title"])
        tag = html.escape(p["tag"])
        desc = html.escape(p["desc"])
        tag_col = p["tag_color"]
        icon = p["icon"]

        svg.append(f'<g class="tile" style="animation-delay: {delay:.2f}s">')
        # Tile Container
        svg.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{tile_w:.1f}" height="{tile_h:.1f}" rx="10" fill="url(#tile_bg)" stroke="{FRAME}" stroke-width="1"/>')
        
        # Header line inside tile
        svg.append(f'<text x="{x + 18:.1f}" y="{y + 28:.1f}" font-size="14" font-weight="700">')
        svg.append(f'<tspan fill="{TEXT}">{icon} {title}</tspan>')
        svg.append('</text>')

        # Badge tag
        svg.append(f'<rect x="{x + 18:.1f}" y="{y + 38:.1f}" width="{len(tag) * 6.5 + 14:.1f}" height="18" rx="4" fill="{tag_col}" fill-opacity="0.12" stroke="{tag_col}" stroke-opacity="0.4" stroke-width="1"/>')
        svg.append(f'<text x="{x + 25:.1f}" y="{y + 51:.1f}" fill="{tag_col}" font-size="9" font-weight="700">{tag}</text>')

        # Description text
        svg.append(f'<text x="{x + 18:.1f}" y="{y + 76:.1f}" fill="{MUTED}" font-size="11" width="{tile_w - 36}">{desc}</text>')
        svg.append('</g>')

    svg.append('</svg>')
    return "".join(svg)

if __name__ == "__main__":
    content = render_projects_card()
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote {OUT_PATH} ({len(content)} bytes)")
