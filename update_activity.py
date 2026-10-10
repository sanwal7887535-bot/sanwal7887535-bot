#!/usr/bin/env python3
"""Builds assets/activity.svg (animated contribution graph) from the GitHub GraphQL API.

Run by .github/workflows/activity.yml. Without GITHUB_TOKEN it writes a styled
placeholder so the README image never breaks.  `--sample PATH` writes a synthetic
preview to PATH (testing only, never used by the workflow).
"""
import json
import os
import random
import sys
import urllib.request
from datetime import date, timedelta

USER = os.environ.get("GH_USER", "sanwal7887535-bot")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "activity.svg")

FONT = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', Consolas, 'Courier New', monospace"
BG, PANEL, TEAL, MINT, VIOLET, MUTED, TEXT = "#0A0F1C", "#0F1A2C", "#14B8A6", "#5EEAD4", "#8B5CF6", "#8B9BB4", "#D0D8E4"
LEVELS = ["#16213A", "#0F766E", "#14B8A6", "#5EEAD4", "#CCFBF1"]

QUERY = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
totalContributions weeks{contributionDays{date contributionCount}}}}}}"""


def fetch(token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "activity-graph"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    cal = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = [[d["contributionCount"] for d in w["contributionDays"]] for w in cal["weeks"]]
    days = [(d["date"], d["contributionCount"]) for w in cal["weeks"] for d in w["contributionDays"]]
    return {"total": cal["totalContributions"], "weeks": weeks, "days": days}


def sample():
    random.seed(7)
    start = date.today() - timedelta(days=52 * 7)
    start -= timedelta(days=(start.weekday() + 1) % 7)
    weeks, days = [], []
    for w in range(53):
        wk = []
        for d in range(7):
            n = max(0, int(random.gauss(2.2, 3))) if random.random() > 0.35 else 0
            wk.append(n)
            days.append(((start + timedelta(days=w * 7 + d)).isoformat(), n))
        weeks.append(wk)
    return {"total": sum(c for _, c in days), "weeks": weeks, "days": days}


def streaks(days):
    counts = [c for _, c in days]
    best = run = 0
    for c in counts:
        run = run + 1 if c > 0 else 0
        best = max(best, run)
    cur, i = 0, len(counts) - 1
    if i >= 0 and counts[i] == 0:
        i -= 1
    while i >= 0 and counts[i] > 0:
        cur += 1
        i -= 1
    return cur, best


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def T(x, y, s, size=14, fill=TEXT, weight="400", anchor="start", family=FONT, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{esc(s)}</text>')


def render(data):
    W, H = 1200, 500
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Contribution activity">']
    o.append(f"""<defs>
<linearGradient id="pg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0F1A2C"/><stop offset="1" stop-color="#0A1120"/></linearGradient>
<linearGradient id="ar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{TEAL}" stop-opacity="0.5"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0.02"/></linearGradient>
<linearGradient id="ln" gradientUnits="userSpaceOnUse" x1="44" y1="0" x2="1156" y2="0"><stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
</defs>""")
    o.append(f'<rect width="{W}" height="{H}" rx="22" fill="{BG}"/>')
    o.append(f'<rect x="14" y="14" width="1172" height="472" rx="18" fill="url(#pg)" stroke="{TEAL}" stroke-opacity="0.45"/>')
    o.append(f'<rect x="14" y="14" width="1172" height="472" rx="18" fill="none" stroke="{MINT}" stroke-width="2" stroke-dasharray="180 3000"><animate attributeName="stroke-dashoffset" from="0" to="-3180" dur="10s" repeatCount="indefinite"/></rect>')
    o.append(T(44, 56, "CONTRIBUTION ACTIVITY", 14, MINT, "700", "start", MONO, 'letter-spacing="4"'))
    o.append(T(1156, 56, "last 12 months", 13, MUTED, "400", "end", MONO))

    live = data is not None
    if live:
        cur, best = streaks(data["days"])
        total = data["total"]
        busiest = max(c for _, c in data["days"])
        stats = [(f"{total:,}", "contributions", TEAL), (str(cur), "day current streak", "#F59E0B"),
                 (str(best), "day longest streak", VIOLET), (str(busiest), "best single day", "#F43F5E")]
    else:
        stats = [("—", "contributions", TEAL), ("—", "current streak", "#F59E0B"),
                 ("—", "longest streak", VIOLET), ("—", "best single day", "#F43F5E")]
    for i, (big, small, col) in enumerate(stats):
        x = 44 + i * 280
        o.append(f'<rect x="{x}" y="74" width="260" height="52" rx="14" fill="{col}" fill-opacity="0.12" stroke="{col}" stroke-opacity="0.6"/>')
        o.append(T(x + 18, 108, big, 26, "#FFFFFF", "800"))
        o.append(T(x + 242, 106, small, 12, MUTED, "400", "end"))

    weeks = data["weeks"] if live else [[0] * 7 for _ in range(53)]
    n = len(weeks)
    totals = [sum(w) for w in weeks]
    mx = max(max(totals), 1)
    x0, x1, ytop, ybot = 44, 1156, 150, 270
    step = (x1 - x0) / max(n - 1, 1)
    pts = [(x0 + i * step, ybot - (t / mx) * (ybot - ytop)) for i, t in enumerate(totals)]
    for g in range(4):
        gy = ytop + g * (ybot - ytop) / 3
        o.append(f'<line x1="{x0}" y1="{gy:.1f}" x2="{x1}" y2="{gy:.1f}" stroke="#FFFFFF" stroke-opacity="0.06"/>')
    line = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    area = line + f" L{x1} {ybot} L{x0} {ybot} Z"
    o.append(f'<path d="{area}" fill="url(#ar)" opacity="0"><animate attributeName="opacity" from="0" to="1" begin="1s" dur="1.5s" fill="freeze"/></path>')
    o.append(f'<path d="{line}" pathLength="1" fill="none" stroke="url(#ln)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1" stroke-dashoffset="1"><animate attributeName="stroke-dashoffset" from="1" to="0" dur="2.4s" fill="freeze"/></path>')
    lx, ly = pts[-1]
    o.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="5" fill="{MINT}"><animate attributeName="r" values="4;8;4" dur="2s" repeatCount="indefinite"/></circle>')
    o.append(T(44, 292, "weekly contributions", 11, MUTED, "400", "start", MONO))

    # heatmap
    cell, gap, hx, hy = 17, 4, 44, 308
    maxd = max((c for w in weeks for c in w), default=0)
    for wi, w in enumerate(weeks):
        for di, c in enumerate(w):
            lvl = 0 if c == 0 or maxd == 0 else min(4, 1 + int(3.999 * c / maxd))
            x, y = hx + wi * (cell + gap), hy + di * (cell + gap)
            delay = 0.5 + wi * 0.03
            o.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="4" fill="{LEVELS[lvl]}" opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.4s" fill="freeze"/></rect>')
    # legend
    o.append(T(44, 468, "Less", 12, MUTED))
    for i, col in enumerate(LEVELS):
        o.append(f'<rect x="{82 + i * 22}" y="456" width="16" height="16" rx="4" fill="{col}"/>')
    o.append(T(198, 468, "More", 12, MUTED))
    foot = "Auto-refreshed every 12 hours by GitHub Actions" if live else "Refreshes automatically via GitHub Actions"
    o.append(T(1156, 468, foot, 12, "#6B7A93", "400", "end", FONT, 'font-style="italic"'))
    o.append("</svg>")
    return "".join(o)


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--sample":
        open(sys.argv[2], "w", encoding="utf-8").write(render(sample()))
        print("sample written")
        return
    token = os.environ.get("GITHUB_TOKEN")
    data = None
    if token:
        try:
            data = fetch(token)
        except Exception as e:  # keep the previous graph if the API hiccups
            print("fetch failed:", e, file=sys.stderr)
            if os.path.exists(OUT):
                return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(render(data))
    print("activity.svg written (live data)" if data else "activity.svg written (placeholder)")


if __name__ == "__main__":
    main()
