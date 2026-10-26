#!/usr/bin/env python3
"""
Generates an animated Languages & Tools SVG (860x130):
- Dark terminal card container (860px wide) with window header dots
- Sequential typewriter entry after the About Me card finishes (~6.8s)
- Embedded high-res Devicon SVGs with name tags, subtle glow on entry, and clean hold
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

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#8b949e"
TEXT = "#c9d1d9"
CYAN = "#58a6ff"
GREEN = "#39d353"

# Tools list: (Display Name, Icon URL)
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
    # Sequence starts at 6.8s (right after About Me completes)
    BASE_START = 6.8
    STAGGER = 0.16

    css = """
.card {
  opacity: 0;
  animation: cardIn 0.45s ease-out both;
}
@keyframes cardIn {
  0% { opacity: 0; transform: translateY(12px); }
  100% { opacity: 1; transform: translateY(0); }
}
.tool-item {
  opacity: 0;
  animation: popIn 0.50s cubic-bezier(0.22, 1, 0.36, 1) both;
}
@keyframes popIn {
  0% {
    opacity: 0;
    transform: translateY(14px) scale(0.85);
    filter: brightness(1);
  }
  50% {
    opacity: 1;
    transform: translateY(-2px) scale(1.05);
    filter: brightness(1.6) drop-shadow(0 0 6px rgba(88, 166, 255, 0.7));
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
    filter: brightness(1) drop-shadow(0 0 0 transparent);
  }
}
@media (prefers-reduced-motion: reduce) {
  .card, .tool-item { opacity: 1 !important; transform: none !important; animation: none !important; filter: none !important; }
}
"""

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace">',
        f'<style>{css}</style>',
        '<defs>',
        f'<linearGradient id="bg_tools" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>',
        '</linearGradient>',
        '</defs>',
        # Background window
        f'<g class="card" style="animation-delay: {BASE_START:.2f}s">',
        f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg_tools)"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
    ]

    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        svg.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

    svg.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" text-anchor="middle">Stack &amp; Technologies</text>')
    svg.append('</g>')

    # 9 tools spaced across the card
    n_tools = len(TOOLS)
    usable_w = W - PAD * 2
    slot_w = usable_w / n_tools
    icon_size = 40
    icon_y = TITLEBAR_H + 18
    text_y = icon_y + icon_size + 18

    for idx, (name, url) in enumerate(TOOLS):
        b64_src = fetch_b64(url)
        delay = BASE_START + 0.20 + (idx * STAGGER)
        cx = PAD + (idx * slot_w) + (slot_w / 2)
        ix = cx - (icon_size / 2)

        svg.append(
            f'<g class="tool-item" style="animation-delay: {delay:.2f}s">'
            f'<image href="{b64_src}" x="{ix:.1f}" y="{icon_y}" width="{icon_size}" height="{icon_size}"/>'
            f'<text x="{cx:.1f}" y="{text_y}" fill="{MUTED}" font-size="11" text-anchor="middle">{html.escape(name)}</text>'
            f'</g>'
        )

    svg.append('</svg>')
    return "".join(svg)

if __name__ == "__main__":
    content = render_tools_card()
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote {OUT_PATH} ({len(content)} bytes)")
