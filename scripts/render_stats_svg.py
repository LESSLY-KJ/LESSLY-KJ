#!/usr/bin/env python3
"""
Renders streak tiles and monthly chart card as animated SVG:
Dual-theme adaptive: adapts tile backgrounds, bars, frames, and typography between Dark and Light.
"""
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "data", "contributions.json")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "stats.svg")

W, H = 840, 880
PAD = 20
TITLEBAR_H = 34
COLS, ROWS = 2, 3
GAP = 16
TILE_W = (W - PAD * 2 - GAP * (COLS - 1)) / COLS
TILE_H = 145
TILES_TOP = TITLEBAR_H + PAD + 6
CHART_TOP = TILES_TOP + ROWS * TILE_H + (ROWS - 1) * GAP + GAP

BASE_START = 0.65
TILE_STAGGER = 0.035
SLIDE_DUR = 0.20
COUNT_DUR = 0.35
FRAMES = 16
BAR_START = BASE_START + (TILE_STAGGER * 5) + 0.15
BAR_STAGGER = 0.05
BAR_DUR = 0.25

def short(d):
    if not d:
        return "N/A"
    return datetime.date.fromisoformat(d).strftime("%b %d")

def span(s):
    if not s or not s.get("length"):
        return "-"
    return f'{short(s.get("start"))} -> {short(s.get("end"))}'

if not os.path.exists(SRC):
    print(f"Error: {SRC} does not exist.")
    sys.exit(1)

with open(SRC, "r", encoding="utf-8") as f:
    data = json.load(f)

cur = data.get("current_streak", {"length": 0})
lng = data.get("longest_streak", {"length": 0})
best = data.get("best_day", {"count": 0, "date": "N/A"})
days_arr = data.get("days", [])
n_days = 365

tiles = [
    ("current streak", cur["length"], " days", span(cur), "green"),
    ("longest streak", lng["length"], " days", span(lng), "accent"),
    ("contributions", data.get("total_contributions", 0), "", "in the past 12 months", "ink"),
    ("active days", data.get("active_days", 0), f" / {n_days}", f'{data.get("active_days", 0) / n_days:.0%} of the year', "ink"),
    ("best day", best["count"], "", short(best["date"]), "ink"),
    ("avg / active day", data.get("avg_per_active_day", 0), "", "contributions", "ink"),
]

def fmt(v, like):
    return f"{v:,.1f}" if isinstance(like, float) else f"{int(round(v)):,}"

css = f"""
:root {{
  --bg-top: #111722;
  --bg-bot: #0d1117;
  --tile-bg: #161b22;
  --frame: #30363d;
  --sep: #30363d;
  --muted: #8b949e;
  --ink: #e6edf3;
  --green: #39d353;
  --bar: #238636;
  --accent: #58a6ff;
}}
@media (prefers-color-scheme: light) {{
  :root {{
    --bg-top: #ffffff;
    --bg-bot: #f6f8fa;
    --tile-bg: #ffffff;
    --frame: #d0d7de;
    --sep: #d8dee4;
    --muted: #656d76;
    --ink: #1f2328;
    --green: #1a7f37;
    --bar: #2da44e;
    --accent: #0969da;
  }}
}}
.card-frame {{ stroke: var(--frame); stroke-width: 1.2px; }}
.tile-box {{ fill: var(--tile-bg); stroke: var(--frame); stroke-width: 1.2px; }}
.sep-line {{ stroke: var(--sep); }}
.txt-muted {{ fill: var(--muted); }}
.txt-ink {{ fill: var(--ink); }}
.txt-green {{ fill: var(--green); }}
.txt-accent {{ fill: var(--accent); }}
.bar-fill {{ fill: var(--bar); }}
.bar-fill-highlight {{ fill: var(--green); }}

.t {{ opacity: 0; animation: in {SLIDE_DUR}s ease-out both; }}
@keyframes in {{ 0% {{ opacity: 0; transform: translateY(14px); }} 100% {{ opacity: 1; transform: translateY(0); }} }}
.b {{ transform-box: fill-box; transform-origin: bottom; transform: scaleY(0); animation: grow {BAR_DUR}s cubic-bezier(0.2, 0.8, 0.2, 1) both; }}
@keyframes grow {{ to {{ transform: scaleY(1); }} }}
@media (prefers-reduced-motion: reduce) {{
  .t, .b {{ opacity: 1 !important; transform: none !important; animation: none !important; }}
}}
""".strip()

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    f'<style>{css}</style>',
    f'<defs><linearGradient id="bg_stats" x1="0" y1="0" x2="0" y2="1">',
    f'<stop offset="0" stop-color="var(--bg-top)"/><stop offset="1" stop-color="var(--bg-bot)"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg_stats)"/>',
    f'<rect class="card-frame" x="0.6" y="0.6" width="{W-1.2:.1f}" height="{H-1.2:.1f}" rx="12" fill="none"/>',
    f'<line class="sep-line" x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}"/>',
]

for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dot}"/>')
parts.append(f'<text class="txt-muted" x="{W/2}" y="{TITLEBAR_H/2 + 4}" font-size="12" text-anchor="middle">Contribution Insights</text>')

for i, (label, value, suffix, caption, col_type) in enumerate(tiles):
    col, row = i % COLS, i // COLS
    x = PAD + col * (TILE_W + GAP)
    y = TILES_TOP + row * (TILE_H + GAP)
    start = BASE_START + (i * TILE_STAGGER)
    count_start = start + SLIDE_DUR * 0.4

    num_class = f"txt-{col_type}"

    parts.append(f'<g class="t" style="animation-delay:{start:.2f}s">')
    parts.append(f'<rect class="tile-box" x="{x:.1f}" y="{y}" width="{TILE_W:.1f}" height="{TILE_H}" rx="10"/>')
    parts.append(f'<text class="txt-muted" x="{x+22:.1f}" y="{y+36}" font-size="18">{label.upper()}</text>')

    num_y = y + 94
    for k in range(1, FRAMES + 1):
        p = k / FRAMES
        v = value * (1 - (1 - p) ** 3)
        t_on = count_start + COUNT_DUR * (k - 1) / FRAMES
        t_off = count_start + COUNT_DUR * k / FRAMES
        anim = f'<set attributeName="opacity" to="1" begin="{t_on:.3f}s"/>'
        if k < FRAMES:
            anim += f'<set attributeName="opacity" to="0" begin="{t_off:.3f}s"/>'
        parts.append(
            f'<text class="{num_class}" x="{x+22:.1f}" y="{num_y}" opacity="0" font-size="46" font-weight="700">'
            f'{fmt(v, value)}<tspan class="txt-muted" font-size="20" font-weight="400">{suffix}</tspan>'
            f'{anim}</text>'
        )
    parts.append(f'<text class="txt-muted" x="{x+22:.1f}" y="{y+126}" font-size="16">{caption}</text>')
    parts.append('</g>')

monthly = data.get("monthly", [])
chart_x, chart_w = PAD, W - PAD * 2
chart_h = H - PAD - CHART_TOP
parts.append(f'<g class="t" style="animation-delay:{BAR_START - 0.10:.2f}s">')
parts.append(f'<rect class="tile-box" x="{chart_x}" y="{CHART_TOP}" width="{chart_w}" height="{chart_h}" rx="10"/>')
parts.append(f'<text class="txt-muted" x="{chart_x+22}" y="{CHART_TOP+36}" font-size="18">MONTHLY ACTIVITY</text>')
parts.append('</g>')

plot_top = CHART_TOP + 56
plot_h = chart_h - 80
plot_baseline = plot_top + plot_h
max_count = max([m["total"] for m in monthly] or [1])
n_bars = len(monthly)
bar_gap = 22
bar_w = (chart_w - 44 - (bar_gap * (n_bars - 1))) / n_bars if n_bars else 30

for idx, m in enumerate(monthly):
    bx = chart_x + 22 + idx * (bar_w + bar_gap)
    val = m["total"]
    h_bar = max(3, (val / max_count) * plot_h) if max_count else 3
    by = plot_baseline - h_bar
    m_name = datetime.datetime.strptime(m["month"], "%Y-%m").strftime("%b")
    bar_delay = BAR_START + idx * BAR_STAGGER
    fill_cls = "bar-fill-highlight" if val == max_count and val > 0 else "bar-fill"

    parts.append(
        f'<rect class="b {fill_cls}" x="{bx:.1f}" y="{by:.1f}" width="{bar_w:.1f}" height="{h_bar:.1f}" rx="3" '
        f'style="animation-delay:{bar_delay:.2f}s"/>'
    )
    parts.append(f'<text class="txt-muted" x="{bx + bar_w/2:.1f}" y="{plot_baseline + 27}" font-size="14" text-anchor="middle">{m_name}</text>')
    if val > 0:
        parts.append(f'<text class="t txt-ink" style="animation-delay:{bar_delay + 0.25:.2f}s" '
                     f'x="{bx + bar_w/2:.1f}" y="{by - 8:.1f}" font-size="14" text-anchor="middle">{val}</text>')

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"wrote {OUT}: {W} x {H}, {len(svg)} bytes")
