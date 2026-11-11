#!/usr/bin/env python3
"""
Generates an animated Featured Projects SVG:
Dual-theme adaptive: adapts tile backgrounds, tags, and borders to Light and Dark modes.
"""
import html
import os

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "projects-card.svg")

W = 860
H = 260
PAD = 12
GAP = 14

PROJECTS = [
    {
        "icon": "📦",
        "title": "Ecommerce-big-Data-Analysis",
        "tag": "PYTHON • BIG DATA",
        "tag_type": "cyan",
        "desc": "Data pipeline & consumer transaction analytics evaluating sales patterns and high-volume data."
    },
    {
        "icon": "🤝",
        "title": "NGO-Data-Analysis",
        "tag": "EDA • METRICS",
        "tag_type": "green",
        "desc": "Exploratory data analysis & socioeconomic indicators modeled for non-profit operational decisions."
    },
    {
        "icon": "📊",
        "title": "Titanic-Excel-Analysis",
        "tag": "EXCEL • ML • PYTHON",
        "tag_type": "gold",
        "desc": "Structured exploratory data analysis, statistical modeling, and survival classification insights."
    },
    {
        "icon": "📫",
        "title": "Connect With Me",
        "tag": "NETWORKING • OPEN TO WORK",
        "tag_type": "purple",
        "desc": "Always open to data analyst collaborations, predictive modeling projects, and opportunities."
    }
]

def render_projects_card():
    BASE_START = 2.20
    STAGGER = 0.06

    css = """
:root {
  --bg-top: #111722;
  --tile-bg: #161b22;
  --frame: #30363d;
  --muted: #8b949e;
  --text: #e6edf3;
  --cyan: #58a6ff;
  --green: #39d353;
  --gold: #f2cc60;
  --purple: #bc8cff;
}
@media (prefers-color-scheme: light) {
  :root {
    --bg-top: #ffffff;
    --tile-bg: #f6f8fa;
    --frame: #d0d7de;
    --muted: #656d76;
    --text: #1f2328;
    --cyan: #0969da;
    --green: #1a7f37;
    --gold: #9a6700;
    --purple: #8250df;
  }
}
.tile-box { fill: var(--tile-bg); stroke: var(--frame); stroke-width: 1.2px; }
.txt-muted { fill: var(--muted); }
.txt-title { fill: var(--text); }
.tag-cyan { fill: var(--cyan); }
.tag-green { fill: var(--green); }
.tag-gold { fill: var(--gold); }
.tag-purple { fill: var(--purple); }

.tile {
  opacity: 0;
  animation: tileSlide 0.22s cubic-bezier(0.22, 1, 0.36, 1) both;
}
@keyframes tileSlide {
  0% {
    opacity: 0;
    transform: translateY(14px);
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
        tag_cls = f"tag-{p['tag_type']}"
        icon = p["icon"]

        svg.append(f'<g class="tile" style="animation-delay: {delay:.2f}s">')
        svg.append(f'<rect class="tile-box" x="{x:.1f}" y="{y:.1f}" width="{tile_w:.1f}" height="{tile_h:.1f}" rx="10"/>')
        
        svg.append(f'<text x="{x + 18:.1f}" y="{y + 28:.1f}" font-size="14" font-weight="700">')
        svg.append(f'<tspan class="txt-title">{icon} {title}</tspan>')
        svg.append('</text>')

        svg.append(f'<text class="{tag_cls}" x="{x + 18:.1f}" y="{y + 48:.1f}" font-size="10" font-weight="700" letter-spacing="0.5">')
        svg.append(f'{tag}')
        svg.append('</text>')

        svg.append(f'<text class="txt-muted" x="{x + 18:.1f}" y="{y + 74:.1f}" font-size="11.5">')
        if len(desc) > 52:
            parts_desc = desc.split(" ")
            mid = len(parts_desc) // 2
            line1 = " ".join(parts_desc[:mid])
            line2 = " ".join(parts_desc[mid:])
            svg.append(f'<tspan x="{x + 18:.1f}" dy="0">{html.escape(line1)}</tspan>')
            svg.append(f'<tspan x="{x + 18:.1f}" dy="16">{html.escape(line2)}</tspan>')
        else:
            svg.append(f'<tspan>{html.escape(desc)}</tspan>')
        svg.append('</text>')

        svg.append('</g>')

    svg.append('</svg>')
    return "".join(svg)


if __name__ == "__main__":
    content = render_projects_card()
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote {OUT_PATH} ({len(content)} bytes)")
