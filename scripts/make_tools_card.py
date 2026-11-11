#!/usr/bin/env python3
"""
Generates an animated Languages & Tools SVG:
Dual-theme adaptive: adapts card styling and typography to Light and Dark modes.
"""
import base64
import html
import os
import urllib.request

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "tools-card.svg")

W = 860
H = 136
TITLEBAR_H = 34
PAD = 24

TOOLS = [
    ("Python", "https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg"),
    ("R", "https://raw.githubusercontent.com/devicons/devicon/master/icons/r/r-original.svg"),
    ("MySQL", "https://raw.githubusercontent.com/devicons/devicon/master/icons/mysql/mysql-original.svg"),
    ("Pandas", "https://raw.githubusercontent.com/devicons/devicon/master/icons/pandas/pandas-original.svg"),
    ("NumPy", "https://raw.githubusercontent.com/devicons/devicon/master/icons/numpy/numpy-original.svg"),
    ("Scikit-Learn", "https://raw.githubusercontent.com/devicons/devicon/master/icons/scikitlearn/scikitlearn-original.svg"),
    ("Power BI", "https://raw.githubusercontent.com/microsoft/PowerBI-Icons/main/SVG/Power-BI.svg"),
    ("Git", "https://raw.githubusercontent.com/devicons/devicon/master/icons/git/git-original.svg"),
    ("VS Code", "https://raw.githubusercontent.com/devicons/devicon/master/icons/vscode/vscode-original.svg"),
]

def fetch_b64(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = urllib.request.urlopen(req).read()
    return "data:image/svg+xml;base64," + base64.b64encode(data).decode("utf-8")

def render_tools_card():
    BASE_START = 1.80
    STAGGER = 0.04

    css = """
:root {
  --bg-top: #111722;
  --bg-bot: #0d1117;
  --frame: #30363d;
  --sep: #30363d;
  --muted: #8b949e;
  --text: #c9d1d9;
}
@media (prefers-color-scheme: light) {
  :root {
    --bg-top: #ffffff;
    --bg-bot: #f6f8fa;
    --frame: #d0d7de;
    --sep: #d8dee4;
    --muted: #656d76;
    --text: #1f2328;
  }
}
.card-frame { stroke: var(--frame); stroke-width: 1.2px; }
.sep-line { stroke: var(--sep); }
.txt-muted { fill: var(--muted); }
.txt-tool { fill: var(--text); }

.card {
  opacity: 0;
  animation: cardIn 0.35s ease-out both;
}
@keyframes cardIn {
  0% { opacity: 0; transform: translateY(10px); }
  100% { opacity: 1; transform: translateY(0); }
}
.tool-item {
  opacity: 0;
  animation: popIn 0.18s cubic-bezier(0.22, 1, 0.36, 1) both;
}
@keyframes popIn {
  0% {
    opacity: 0;
    transform: translateY(10px) scale(0.9);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}
@media (prefers-reduced-motion: reduce) {
  .card, .tool-item { opacity: 1 !important; transform: none !important; animation: none !important; }
}
"""

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">',
        f'<style>{css}</style>',
        '<defs>',
        f'<linearGradient id="bg_tools" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0" stop-color="var(--bg-top)"/><stop offset="1" stop-color="var(--bg-bot)"/>',
        '</linearGradient>',
        '</defs>',
        f'<g class="card" style="animation-delay: {BASE_START:.2f}s">',
        f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg_tools)"/>',
        f'<rect class="card-frame" x="0.6" y="0.6" width="{W-1.2:.1f}" height="{H-1.2:.1f}" rx="12" fill="none"/>',
        f'<line class="sep-line" x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}"/>',
    ]

    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        svg.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

    svg.append(f'<text class="txt-muted" x="{W/2}" y="{TITLEBAR_H/2 + 4}" font-size="12" text-anchor="middle">Stack &amp; Technologies</text>')
    svg.append('</g>')

    n_tools = len(TOOLS)
    usable_w = W - PAD * 2
    slot_w = usable_w / n_tools
    icon_size = 40
    icon_y = TITLEBAR_H + 18
    text_y = icon_y + icon_size + 18

    for idx, (name, url) in enumerate(TOOLS):
        b64 = fetch_b64(url)
        center_x = PAD + idx * slot_w + slot_w / 2
        img_x = center_x - icon_size / 2
        delay = BASE_START + (idx * STAGGER)

        svg.append(f'<g class="tool-item" style="animation-delay: {delay:.2f}s">')
        svg.append(
            f'<image href="{b64}" x="{img_x:.1f}" y="{icon_y}" width="{icon_size}" height="{icon_size}"/>'
        )
        svg.append(
            f'<text class="txt-tool" x="{center_x:.1f}" y="{text_y}" font-size="12" font-weight="600" text-anchor="middle">{html.escape(name)}</text>'
        )
        svg.append('</g>')

    svg.append('</svg>')
    return "".join(svg)


if __name__ == "__main__":
    content = render_tools_card()
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote {OUT_PATH} ({len(content)} bytes)")
