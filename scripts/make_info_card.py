#!/usr/bin/env python3
"""
Generates an animated developer info card SVG using CSS keyframe animations.
- Starts writing sequentially after the PFP + stats finish (~5.2s).
- Smooth typewriter / line slide-in effect that settles and freezes.
"""
import html
import os

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "info-card.svg")

W = 860
H = 340
TITLEBAR_H = 34
PAD = 24

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#8b949e"
TEXT = "#e6edf3"
CYAN = "#58a6ff"
GREEN = "#39d353"
ACCENT = "#58a6ff"

lines = [
    ("header", ("Lessly K.J", "Data Analyst & AI Specialist")),
    ("div", "--------------------------------------------------------"),
    ("item", ("Role", "Data Analytics Specialist | AI & Machine Learning")),
    ("item", ("GitHub", "https://github.com/iblamelessly")),
    ("item", ("Focus", "Big Data Analytics, Advanced EDA, Predictive Modeling, AI")),
    ("item", ("Projects", "Ecommerce Big Data, NGO Analytics, Titanic EDA")),
    ("item", ("Languages", "Python, SQL, R, Bash")),
    ("item", ("Tools", "Pandas, NumPy, Scikit-learn, Git, PowerBI / Excel")),
    ("palette", ["#ff5f56", "#ffbd2e", "#27c93f", "#58a6ff", "#bc8cff", "#f0883e", "#39d353", "#c9d1d9"])
]

def render_info_card():
    css = """
.t {
  opacity: 0;
  animation: in 0.40s ease-out both;
}
@keyframes in {
  0% { opacity: 0; transform: translateY(8px); }
  100% { opacity: 1; transform: translateY(0); }
}
@media (prefers-reduced-motion: reduce) {
  .t { opacity: 1 !important; transform: none !important; animation: none !important; }
}
"""

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">',
        f'<style>{css}</style>',
        '<defs>',
        f'<linearGradient id="bg_info" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>',
        '</linearGradient>',
        '</defs>',
        f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg_info)"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
    ]

    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        svg.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

    svg.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" text-anchor="middle">Developer Profile</text>')

    start_y = TITLEBAR_H + 28
    line_h = 24
    curr_y = start_y
    # Starts writing after PFP + Stats finish!
    delay = 5.2

    for item in lines:
        kind = item[0]
        delay_str = f"{delay:.2f}s"

        if kind == "header":
            name = html.escape(item[1][0])
            role = html.escape(item[1][1])
            svg.append(
                f'<g class="t" style="animation-delay:{delay_str}">'
                f'<text x="{PAD}" y="{curr_y}" font-size="14">'
                f'<tspan fill="{GREEN}" font-weight="700">{name}</tspan>'
                f'<tspan fill="{MUTED}"> &#8226; </tspan>'
                f'<tspan fill="{CYAN}" font-weight="600">{role}</tspan>'
                f'<tspan fill="{GREEN}"> _</tspan>'
                f'</text></g>'
            )
        elif kind == "div":
            svg.append(
                f'<g class="t" style="animation-delay:{delay_str}">'
                f'<text x="{PAD}" y="{curr_y}" fill="{MUTED}" font-size="12">{html.escape(item[1])}</text>'
                f'</g>'
            )
        elif kind == "item":
            key = html.escape(item[1][0])
            val = html.escape(item[1][1])
            svg.append(
                f'<g class="t" style="animation-delay:{delay_str}">'
                f'<text x="{PAD}" y="{curr_y}" font-size="13">'
                f'<tspan fill="{CYAN}" font-weight="600">{key:<10}</tspan>'
                f'<tspan fill="{MUTED}">: </tspan>'
                f'<tspan fill="{TEXT}">{val}</tspan>'
                f'</text></g>'
            )
        elif kind == "palette":
            boxes = []
            x_offset = PAD
            for col in item[1]:
                boxes.append(f'<rect x="{x_offset}" y="{curr_y - 12}" width="26" height="13" rx="2" fill="{col}"/>')
                x_offset += 32
            svg.append(
                f'<g class="t" style="animation-delay:{delay_str}">'
                f'{"".join(boxes)}'
                f'</g>'
            )

        curr_y += line_h
        delay += 0.16

    svg.append('</svg>')
    return "".join(svg)

if __name__ == "__main__":
    content = render_info_card()
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote {OUT_PATH} ({len(content)} bytes)")
