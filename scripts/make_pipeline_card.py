#!/usr/bin/env python3
"""
Generates an animated End-to-End Analytics Workflow Pipeline SVG:
- Dark/Light dual-theme adaptive.
- Proportional dimensions (840x980) matching stats.svg with zero stretching.
- Increased font sizes, spacious stage cards, perfectly padded text that never overflows.
"""
import html
import os

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "pipeline-card.svg")

W = 840
H = 980
PAD = 22
TITLEBAR_H = 34

STAGES = [
    {
        "step": "STAGE 01",
        "name": "DATA INGESTION & AUDIT",
        "tag": "SQL • PANDAS • ETL PIPELINES",
        "tag_type": "accent",
        "desc": "Connecting to databases, querying tables, resolving missing values & schema anomalies.",
        "icon": "1",
        "badge": "1.2M+ Records Cleaned",
        "badge_type": "green",
        "y": 140
    },
    {
        "step": "STAGE 02",
        "name": "EXPLORATORY DATA ANALYSIS",
        "tag": "NUMPY • STATS • DATA VIZ",
        "tag_type": "green",
        "desc": "Statistical distribution modeling, hypothesis testing & customer cohort segmentation.",
        "icon": "2",
        "badge": "45+ Features Engineered",
        "badge_type": "accent",
        "y": 320
    },
    {
        "step": "STAGE 03",
        "name": "PREDICTIVE MODELING & ML",
        "tag": "SCIKIT-LEARN • EVALUATION",
        "tag_type": "gold",
        "desc": "Supervised classification, clustering & 5-fold cross-validation for model stability.",
        "icon": "3",
        "badge": "86.4% Model ROC-AUC",
        "badge_type": "gold",
        "y": 500
    },
    {
        "step": "STAGE 04",
        "name": "EXECUTIVE DASHBOARDING",
        "tag": "POWER BI • EXCEL • REPORTING",
        "tag_type": "purple",
        "desc": "Translating analytics into executive KPIs, churn monitors & strategic business reports.",
        "icon": "4",
        "badge": "12 Decision KPIs Built",
        "badge_type": "purple",
        "y": 680
    }
]

def render_pipeline_card():
    BASE_START = 1.00
    STAGE_STAGGER = 0.15

    css = """
:root {
  --bg-top: #111722;
  --bg-bot: #0d1117;
  --tile-bg: #161b22;
  --badge-bg: #0d1117;
  --step-circle-bg: #21262d;
  --frame: #30363d;
  --sep: #30363d;
  --muted: #8b949e;
  --ink: #e6edf3;
  --green: #39d353;
  --accent: #58a6ff;
  --gold: #d29922;
  --purple: #bc8cff;
}
@media (prefers-color-scheme: light) {
  :root {
    --bg-top: #ffffff;
    --bg-bot: #f6f8fa;
    --tile-bg: #ffffff;
    --badge-bg: #f6f8fa;
    --step-circle-bg: #eaeef2;
    --frame: #d0d7de;
    --sep: #d8dee4;
    --muted: #656d76;
    --ink: #1f2328;
    --green: #1a7f37;
    --accent: #0969da;
    --gold: #9a6700;
    --purple: #8250df;
  }
}
.card-frame { stroke: var(--frame); stroke-width: 1.2px; }
.tile-box { fill: var(--tile-bg); stroke: var(--frame); stroke-width: 1.2px; }
.sep-line { stroke: var(--sep); }
.txt-muted { fill: var(--muted); }
.txt-ink { fill: var(--ink); }
.txt-green { fill: var(--green); }
.txt-accent { fill: var(--accent); }
.txt-gold { fill: var(--gold); }
.txt-purple { fill: var(--purple); }

.tag-green { fill: var(--green); }
.tag-accent { fill: var(--accent); }
.tag-gold { fill: var(--gold); }
.tag-purple { fill: var(--purple); }

.badge-green { fill: var(--badge-bg); stroke: var(--green); stroke-width: 1.2px; }
.badge-accent { fill: var(--badge-bg); stroke: var(--accent); stroke-width: 1.2px; }
.badge-gold { fill: var(--badge-bg); stroke: var(--gold); stroke-width: 1.2px; }
.badge-purple { fill: var(--badge-bg); stroke: var(--purple); stroke-width: 1.2px; }

.circle-green { fill: var(--step-circle-bg); stroke: var(--green); stroke-width: 2.2px; }
.circle-accent { fill: var(--step-circle-bg); stroke: var(--accent); stroke-width: 2.2px; }
.circle-gold { fill: var(--step-circle-bg); stroke: var(--gold); stroke-width: 2.2px; }
.circle-purple { fill: var(--step-circle-bg); stroke: var(--purple); stroke-width: 2.2px; }

.fade-in {
  opacity: 0;
  animation: slideIn 0.35s cubic-bezier(0.2, 0.8, 0.2, 1) both;
}
@keyframes slideIn {
  0% { opacity: 0; transform: translateY(14px); }
  100% { opacity: 1; transform: translateY(0); }
}
@media (prefers-reduced-motion: reduce) {
  .fade-in { opacity: 1 !important; transform: none !important; animation: none !important; }
}
""".strip()

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        f'<style>{css}</style>',
        '<defs>',
        f'<linearGradient id="bg_pipeline" x1="0" y1="0" x2="0" y2="1">',
        f'<stop offset="0" stop-color="var(--bg-top)"/><stop offset="1" stop-color="var(--bg-bot)"/>',
        '</linearGradient>',
        '</defs>',
        f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg_pipeline)"/>',
        f'<rect class="card-frame" x="0.6" y="0.6" width="{W-1.2:.1f}" height="{H-1.2:.1f}" rx="12" fill="none"/>',
        f'<line class="sep-line" x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}"/>',
    ]

    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
    parts.append(f'<text class="txt-muted" x="{W/2}" y="{TITLEBAR_H/2 + 4}" font-size="12" text-anchor="middle">Analytics Methodology &amp; Pipeline</text>')

    # Top Header within card - Bigger, clearer typography
    parts.append(f'<g class="fade-in" style="animation-delay: {BASE_START:.2f}s">')
    parts.append(f'<text class="txt-ink" x="{W/2}" y="76" font-size="21" font-weight="700" text-anchor="middle">HOW I TURN RAW DATA INTO BUSINESS VALUE</text>')
    parts.append(f'<text class="txt-muted" x="{W/2}" y="103" font-size="14.5" text-anchor="middle">The 4-stage analytical framework applied across all my projects</text>')
    parts.append('</g>')

    card_box_w = W - PAD * 2
    card_box_h = 148

    for idx, s in enumerate(STAGES):
        delay = BASE_START + idx * STAGE_STAGGER
        box_y = s["y"]
        step_txt = html.escape(s["step"])
        name_txt = html.escape(s["name"])
        desc_txt = html.escape(s["desc"])
        tag_txt = html.escape(s["tag"])
        badge_txt = html.escape(s["badge"])

        parts.append(f'<g class="fade-in" style="animation-delay: {delay:.2f}s">')
        parts.append(f'<rect class="tile-box" x="{PAD}" y="{box_y}" width="{card_box_w}" height="{card_box_h}" rx="10"/>')

        # Circle indicator
        cx, cy = PAD + 42, box_y + card_box_h / 2 - 4
        parts.append(f'<circle class="circle-{s["tag_type"]}" cx="{cx}" cy="{cy}" r="24"/>')
        parts.append(f'<text class="txt-ink" x="{cx}" y="{cy + 7}" font-size="20" font-weight="700" text-anchor="middle">{s["icon"]}</text>')

        # Step + Title (Larger & clearer font: 17px)
        tx = PAD + 82
        parts.append(f'<text x="{tx}" y="{box_y + 38}" font-size="17" font-weight="700">')
        parts.append(f'<tspan class="tag-{s["tag_type"]}">{step_txt}</tspan>')
        parts.append(f'<tspan class="txt-muted">  |  </tspan>')
        parts.append(f'<tspan class="txt-ink">{name_txt}</tspan>')
        parts.append('</text>')

        # Description (Larger font: 14px, safely within box width)
        parts.append(f'<text class="txt-muted" x="{tx}" y="{box_y + 74}" font-size="14">{desc_txt}</text>')

        # Tag (13px, bold monospace)
        parts.append(f'<text class="tag-{s["tag_type"]}" x="{tx}" y="{box_y + 116}" font-size="13" font-weight="700" letter-spacing="0.5">{tag_txt}</text>')

        # Badge pill (Well-proportioned: 240x36 with 13.5px bold font)
        badge_w, badge_h = 240, 36
        badge_x = PAD + card_box_w - badge_w - 20
        badge_y = box_y + 92
        parts.append(f'<rect class="badge-{s["badge_type"]}" x="{badge_x}" y="{badge_y}" width="{badge_w}" height="{badge_h}" rx="6"/>')
        parts.append(f'<text class="tag-{s["badge_type"]}" x="{badge_x + badge_w/2}" y="{badge_y + 23}" font-size="13.5" font-weight="700" text-anchor="middle">{badge_txt}</text>')

        parts.append('</g>')

        # Flow indicator arrow to next stage
        if idx < len(STAGES) - 1:
            arrow_y = box_y + card_box_h + 10
            parts.append(f'<g class="fade-in" style="animation-delay: {delay + 0.05:.2f}s">')
            parts.append(f'<text class="txt-muted" x="{PAD + 42}" y="{arrow_y + 16}" font-size="20" text-anchor="middle">&#8595;</text>')
            parts.append('</g>')

    # Bottom footer line
    foot_y = 895
    parts.append(f'<g class="fade-in" style="animation-delay: {BASE_START + 0.60:.2f}s">')
    parts.append(f'<line class="sep-line" x1="{PAD}" y1="{foot_y}" x2="{W - PAD}" y2="{foot_y}"/>')
    parts.append(f'<text class="txt-green" x="{W/2}" y="{foot_y + 36}" font-size="14.5" font-weight="700" text-anchor="middle">RESULT: Clean Code  &#8226;  Validated Science  &#8226;  Actionable Business Decisions</text>')
    parts.append('</g>')

    parts.append('</svg>')
    return "".join(parts)


if __name__ == "__main__":
    content = render_pipeline_card()
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote {OUT_PATH} ({len(content)} bytes)")
