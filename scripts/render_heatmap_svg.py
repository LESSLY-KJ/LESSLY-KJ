#!/usr/bin/env python3
"""
Renders data/contributions.json as a GitHub contribution heatmap SVG:
- Dual-theme adaptive: adapts seamlessly between Dark Mode and Light Mode via CSS prefers-color-scheme.
- Starts immediately at 0.0s, completes by ~0.80s.
"""
import datetime
import json
import os

HERE = os.path.dirname(__file__)
IN_PATH = os.path.join(HERE, "..", "data", "contributions.json")
OUT_PATH = os.path.join(HERE, "..", "contrib-heatmap.svg")

# Palettes
DARK_PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#56e370"]
LIGHT_PALETTE = ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39", "#114f24"]

CELL = 12
GAP = 3
STEP = CELL + GAP
PAD = 22
LEFT_LABEL_W = 32
TOP_LABEL_H = 22
TITLEBAR_H = 34

COL_T = 0.012
ROW_T = 0.006
CELL_DUR = 0.20


def level_for(count):
    if count == 0:
        return 0
    if count <= 2:
        return 1
    if count <= 6:
        return 2
    if count <= 12:
        return 3
    if count <= 20:
        return 4
    return 5


def build_grid(days):
    if not days:
        return []
    first = datetime.date.fromisoformat(days[0]["date"])
    lead_pad = (first.weekday() + 1) % 7
    grid = []
    col = [None] * lead_pad
    for d in days:
        date = datetime.date.fromisoformat(d["date"])
        weekday = (date.weekday() + 1) % 7
        while len(col) < weekday:
            col.append(None)
        col.append((d["date"], d["count"], level_for(d["count"])))
        if len(col) == 7:
            grid.append(col)
            col = []
    if col:
        while len(col) < 7:
            col.append(None)
        grid.append(col)
    return grid


def render(data):
    days = data.get("days", [])
    grid = build_grid(days)
    n_cols = len(grid)
    art_w = n_cols * STEP
    art_h = 7 * STEP

    month_labels = []
    seen_months = set()
    for ci, column in enumerate(grid):
        for cell in column:
            if cell is None:
                continue
            date = datetime.date.fromisoformat(cell[0])
            key = (date.year, date.month)
            if key not in seen_months and date.day <= 7:
                seen_months.add(key)
                month_labels.append((ci, date.strftime("%b")))
            break

    canvas_w = 860
    stats_h = 82
    canvas_h = TITLEBAR_H + TOP_LABEL_H + art_h + stats_h + PAD

    css = f"""
:root {{
  --bg-top: #0e1522;
  --bg-bot: #0a0e14;
  --frame: #30363d;
  --sep: #30363d;
  --muted: #8b949e;
  --text: #c9d1d9;
  --accent: #58a6ff;
  --green: #3fb950;
  --gold: #d29922;
  --l0: #161b22;
  --l1: #0e4429;
  --l2: #006d32;
  --l3: #26a641;
  --l4: #39d353;
  --l5: #56e370;
}}
@media (prefers-color-scheme: light) {{
  :root {{
    --bg-top: #ffffff;
    --bg-bot: #f6f8fa;
    --frame: #d0d7de;
    --sep: #d8dee4;
    --muted: #656d76;
    --text: #1f2328;
    --accent: #0969da;
    --green: #1a7f37;
    --gold: #9a6700;
    --l0: #ebedf0;
    --l1: #9be9a8;
    --l2: #40c463;
    --l3: #30a14e;
    --l4: #216e39;
    --l5: #114f24;
  }}
}}
.card-frame {{ stroke: var(--frame); stroke-width: 1.2px; }}
.sep-line {{ stroke: var(--sep); }}
.txt-muted {{ fill: var(--muted); }}
.txt-main {{ fill: var(--text); }}
.txt-accent {{ fill: var(--accent); }}
.txt-green {{ fill: var(--green); }}
.txt-gold {{ fill: var(--gold); }}

.lvl-0 {{ fill: var(--l0); }}
.lvl-1 {{ fill: var(--l1); }}
.lvl-2 {{ fill: var(--l2); }}
.lvl-3 {{ fill: var(--l3); }}
.lvl-4 {{ fill: var(--l4); }}
.lvl-5 {{ fill: var(--l5); }}

@keyframes cellGlow {{
  0% {{ opacity: 0; transform: scale(0.6); }}
  40% {{ opacity: 1; transform: scale(1.15); }}
  100% {{ opacity: 1; transform: scale(1); }}
}}
@keyframes emptyCell {{
  0% {{ opacity: 0; transform: scale(0.8); }}
  100% {{ opacity: 1; transform: scale(1); }}
}}
.cell-active {{
  transform-box: fill-box;
  transform-origin: center;
  opacity: 0;
  animation: cellGlow {CELL_DUR:.2f}s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}}
.cell-empty {{
  transform-box: fill-box;
  transform-origin: center;
  opacity: 0;
  animation: emptyCell 0.35s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}}
@media (prefers-reduced-motion: reduce) {{
  .cell-active, .cell-empty {{ opacity: 1 !important; animation: none !important; }}
}}
""".strip()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{canvas_w}" height="{canvas_h}" '
        f'viewBox="0 0 {canvas_w} {canvas_h}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        f'<style>{css}</style>',
        '<defs>',
        f'<linearGradient id="hbg" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0" stop-color="var(--bg-top)"/><stop offset="1" stop-color="var(--bg-bot)"/>',
        '</linearGradient>',
        '</defs>',
        f'<rect width="{canvas_w}" height="{canvas_h}" rx="10" fill="url(#hbg)"/>',
        f'<rect class="card-frame" x="0.6" y="0.6" width="{canvas_w-1.2:.1f}" height="{canvas_h-1.2:.1f}" rx="10" fill="none"/>',
        f'<line class="sep-line" x1="0" y1="{TITLEBAR_H}" x2="{canvas_w}" y2="{TITLEBAR_H}" stroke-opacity="0.8"/>',
    ]

    # Window controls
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

    parts.append(f'<text class="txt-muted" x="{canvas_w/2}" y="{TITLEBAR_H/2 + 4}" font-size="12" '
                 f'text-anchor="middle">Contributions Activity</text>')

    grid_top = TITLEBAR_H + TOP_LABEL_H
    grid_left = PAD + LEFT_LABEL_W

    for ci, label in month_labels:
        x = grid_left + ci * STEP
        parts.append(f'<text class="txt-muted" x="{x}" y="{TITLEBAR_H + 15}" font-size="10">{label}</text>')

    for wi, wname in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        y = grid_top + wi * STEP + CELL * 0.78
        parts.append(f'<text class="txt-muted" x="{PAD}" y="{y:.1f}" font-size="9">{wname}</text>')

    for ci, column in enumerate(grid):
        gx = grid_left + ci * STEP
        for ri, cell in enumerate(column):
            if cell is None:
                continue
            date_s, count, lvl = cell
            gy = grid_top + ri * STEP
            delay = ci * COL_T + ri * ROW_T
            plural = "s" if count != 1 else ""
            anim_cls = "cell-active" if lvl > 0 else "cell-empty"
            parts.append(
                f'<rect class="{anim_cls} lvl-{lvl}" x="{gx}" y="{gy}" width="{CELL}" height="{CELL}" rx="2.5" '
                f'style="animation-delay:{delay:.3f}s">'
                f'<title>{date_s}: {count} contribution{plural}</title></rect>'
            )

    # Legend
    leg_y = grid_top + art_h + 8
    leg_x = canvas_w - PAD - (len(DARK_PALETTE) * (CELL - 1) + 65)
    parts.append(f'<text class="txt-muted" x="{leg_x}" y="{leg_y + CELL*0.8:.1f}" font-size="10" text-anchor="end">Less</text>')
    lx = leg_x + 8
    for lvl in range(len(DARK_PALETTE)):
        parts.append(f'<rect class="lvl-{lvl}" x="{lx}" y="{leg_y}" width="{CELL-1}" height="{CELL-1}" rx="2"/>')
        lx += CELL
    parts.append(f'<text class="txt-muted" x="{lx + 4}" y="{leg_y + CELL*0.8:.1f}" font-size="10">More</text>')

    sep_y = leg_y + CELL + 12
    parts.append(f'<line class="sep-line" x1="0" y1="{sep_y}" x2="{canvas_w}" y2="{sep_y}" stroke-opacity="0.8"/>')

    cs = data.get("current_streak", {}).get("length", 0)
    ls = data.get("longest_streak", {}).get("length", 0)
    total = data.get("total_contributions", 0)
    best = data.get("best_day", {"count": 0, "date": "N/A"})
    rng = data.get("range", {"start": "", "end": ""})

    ly = sep_y + 22
    parts.append(f'<text x="{PAD}" y="{ly}" font-size="13">'
                 f'<tspan class="txt-green" font-weight="700">{total:,}</tspan>'
                 f'<tspan class="txt-muted"> contributions in the past 12 months</tspan></text>')
    parts.append(f'<text class="txt-muted" x="{canvas_w - PAD}" y="{ly}" font-size="11" text-anchor="end">'
                 f'{rng["start"]} &#8594; {rng["end"]}</text>')
    ly += 22
    parts.append(f'<text class="txt-muted" x="{PAD}" y="{ly}" font-size="12">current streak '
                 f'<tspan class="txt-accent" font-weight="700">{cs} days</tspan>'
                 f'<tspan class="txt-muted">   &#183;   longest streak </tspan>'
                 f'<tspan class="txt-accent" font-weight="700">{ls} days</tspan></text>')
    parts.append(f'<text class="txt-muted" x="{canvas_w - PAD}" y="{ly}" font-size="11" text-anchor="end">'
                 f'best day <tspan class="txt-gold" font-weight="700">{best["count"]}</tspan> on {best["date"]}</text>')

    parts.append("</svg>")
    return "".join(parts)


if __name__ == "__main__":
    if not os.path.exists(IN_PATH):
        print(f"Error: {IN_PATH} does not exist. Run fetch_contributions.py first.")
        exit(1)
    with open(IN_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    svg = render(data)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"Wrote {OUT_PATH} ({len(svg)} bytes)")
