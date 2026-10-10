#!/usr/bin/env python3
"""Generates every animated SVG used by README.md into ./assets (SMIL animations, no JS)."""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "assets")
os.makedirs(OUT, exist_ok=True)

FONT = "'Segoe UI', 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', Consolas, 'Courier New', monospace"
BG = "#0A0F1C"
PANEL = "#0F1A2C"
TEAL = "#14B8A6"
MINT = "#5EEAD4"
CYAN = "#22D3EE"
VIOLET = "#8B5CF6"
AMBER = "#F59E0B"
ROSE = "#F43F5E"
MUTED = "#8B9BB4"
TEXT = "#D0D8E4"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def T(x, y, s, size=14, fill=TEXT, weight="400", anchor="start", family=None, extra=""):
    family = family or FONT
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{esc(s)}</text>')


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)


def svg_open(w, h, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">')


def fade_in(i, inner, step=0.15, base=0.2):
    return (f'<g opacity="0">{inner}<animate attributeName="opacity" from="0" to="1" '
            f'begin="{base + step * i:.2f}s" dur="0.6s" fill="freeze"/></g>')


# ---------------------------------------------------------------- HEADER
def header():
    W, H = 1200, 340
    o = [svg_open(W, H, "Muhammad Sanwal engineering portfolio")]
    o.append("""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#050B16"><animate attributeName="stop-color" values="#050B16;#07222B;#14123A;#050B16" dur="12s" repeatCount="indefinite"/></stop>
<stop offset="0.55" stop-color="#0A2530"><animate attributeName="stop-color" values="#0A2530;#17123F;#07222B;#0A2530" dur="12s" repeatCount="indefinite"/></stop>
<stop offset="1" stop-color="#150F35"><animate attributeName="stop-color" values="#150F35;#050B16;#0A2530;#150F35" dur="12s" repeatCount="indefinite"/></stop>
</linearGradient>
<linearGradient id="tg" gradientUnits="userSpaceOnUse" x1="80" y1="0" x2="680" y2="0" spreadMethod="reflect">
<stop offset="0" stop-color="#FFFFFF"/><stop offset="0.5" stop-color="#5EEAD4"/><stop offset="1" stop-color="#22D3EE"/>
<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="600 0" dur="5s" repeatCount="indefinite"/>
</linearGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
<animateTransform attributeName="patternTransform" type="translate" from="0 0" to="40 40" dur="6s" repeatCount="indefinite"/>
<path d="M40 0H0V40" fill="none" stroke="#5EEAD4" stroke-opacity="0.08"/>
</pattern>
<radialGradient id="core" cx="0.5" cy="0.5" r="0.5">
<stop offset="0" stop-color="#5EEAD4"/><stop offset="1" stop-color="#0D9488"/>
</radialGradient>
<radialGradient id="halo" cx="0.5" cy="0.5" r="0.5">
<stop offset="0" stop-color="#14B8A6" stop-opacity="0.35"/><stop offset="1" stop-color="#14B8A6" stop-opacity="0"/>
</radialGradient>
<linearGradient id="w1" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#14B8A6" stop-opacity="0.38"/><stop offset="1" stop-color="#14B8A6" stop-opacity="0.03"/>
</linearGradient>
<linearGradient id="w2" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#8B5CF6" stop-opacity="0.32"/><stop offset="1" stop-color="#8B5CF6" stop-opacity="0.03"/>
</linearGradient>
<clipPath id="clip"><rect width="1200" height="340"/></clipPath>
</defs>""")
    o.append(f'<g clip-path="url(#clip)">')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#grid)"/>')
    o.append('<circle cx="980" cy="130" r="190" fill="url(#halo)"><animate attributeName="r" values="170;205;170" dur="6s" repeatCount="indefinite"/></circle>')

    # floating particles
    for i in range(24):
        x = (i * 97 + 40) % 1200
        y0 = 50 + (i * 53) % 220
        r = 1.4 + (i % 3) * 0.8
        dur = 4 + (i % 5)
        col = [MINT, CYAN, "#C4B5FD"][i % 3]
        o.append(
            f'<circle cx="{x}" cy="{y0}" r="{r}" fill="{col}" opacity="0.3">'
            f'<animate attributeName="cy" values="{y0};{y0 - 34};{y0}" dur="{dur}s" begin="-{i * 0.4:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.15;0.95;0.15" dur="{dur}s" begin="-{i * 0.4:.1f}s" repeatCount="indefinite"/></circle>')

    # orbit system
    cx, cy = 980, 130
    for r, dur, direction, dash in [(52, 9, 1, "4 8"), (84, 14, -1, "2 10"), (116, 20, 1, "10 6")]:
        frm, to = (0, 360) if direction == 1 else (360, 0)
        o.append(
            f'<g><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{MINT}" stroke-opacity="0.35" stroke-dasharray="{dash}"/>'
            f'<circle cx="{cx + r}" cy="{cy}" r="5" fill="{CYAN}"/>'
            f'<circle cx="{cx - r}" cy="{cy}" r="3" fill="#C4B5FD"/>'
            f'<animateTransform attributeName="transform" type="rotate" from="{frm} {cx} {cy}" to="{to} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/></g>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="26" fill="url(#core)"><animate attributeName="r" values="24;30;24" dur="3s" repeatCount="indefinite"/></circle>')
    o.append(T(cx, cy + 6, "</>", 17, "#04201D", "800", "middle", MONO))

    # waves
    wave = "M0 30 Q150 0 300 30 T600 30 T900 30 T1200 30 T1500 30 T1800 30 T2100 30 T2400 30 V140 H0 Z"
    o.append(f'<g transform="translate(0 250)"><path d="{wave}" fill="url(#w2)"><animateTransform attributeName="transform" type="translate" from="-600 0" to="0 0" dur="14s" repeatCount="indefinite"/></path></g>')
    o.append(f'<g transform="translate(0 270)"><path d="{wave}" fill="url(#w1)"><animateTransform attributeName="transform" type="translate" from="0 0" to="-600 0" dur="9s" repeatCount="indefinite"/></path></g>')

    # corner brackets
    for d in ["M24 54 V24 H54", "M1176 54 V24 H1146", "M24 286 V316 H54", "M1176 286 V316 H1146"]:
        o.append(f'<path d="{d}" fill="none" stroke="{MINT}" stroke-width="2" stroke-opacity="0.5"><animate attributeName="stroke-opacity" values="0.2;0.8;0.2" dur="3s" repeatCount="indefinite"/></path>')

    # text
    o.append(f'<g opacity="0">{T(80, 90, "</>  SOFTWARE ENGINEERING PORTFOLIO", 14, MINT, "600", "start", MONO, "letter-spacing=\"4\"")}'
             '<animate attributeName="opacity" from="0" to="1" dur="1s" fill="freeze"/></g>')
    o.append(
        '<g opacity="0">'
        + T(80, 170, "MUHAMMAD SANWAL", 64, "url(#tg)", "800")
        + '<animate attributeName="opacity" from="0" to="1" begin="0.3s" dur="1s" fill="freeze"/>'
        '<animateTransform attributeName="transform" type="translate" from="-40 0" to="0 0" begin="0.3s" dur="1s" fill="freeze"/></g>')
    o.append(f'<rect x="80" y="188" width="0" height="4" rx="2" fill="{TEAL}"><animate attributeName="width" from="0" to="300" begin="0.8s" dur="1.2s" fill="freeze"/>'
             f'<animate attributeName="fill" values="{TEAL};{CYAN};{VIOLET};{TEAL}" dur="6s" repeatCount="indefinite"/></rect>')

    roles = ["Software Development", "AI Automation & Intelligent Workflows", "Odoo Enterprise & ERP Security"]
    for i, role in enumerate(roles):
        o.append(
            f'<g opacity="0">{T(80, 236, "› " + role, 26, "#E6EDF3", "600")}'
            f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.06;0.30;0.36;1" dur="9s" begin="{i * 3 + 1}s" repeatCount="indefinite"/></g>')
    o.append(T(80, 280, "BS Information Technology  ·  University of the Punjab  ·  Lahore, Pakistan", 14, MUTED, "400", "start", MONO))
    o.append("</g></svg>")
    save("header.svg", "".join(o))


# ---------------------------------------------------------------- SECTION BANNER
def banner(fname, tag, title, sub, c1=TEAL, c2=VIOLET):
    W, H = 1200, 92
    o = [svg_open(W, H, title)]
    o.append(f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0B1322"/><stop offset="1" stop-color="#121C33"/></linearGradient>
<linearGradient id="ac" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1200" y2="0"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
<linearGradient id="shine" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.09"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
<clipPath id="c"><rect x="0.5" y="0.5" width="1199" height="91" rx="18"/></clipPath>
</defs>""")
    o.append('<rect x="0.5" y="0.5" width="1199" height="91" rx="18" fill="url(#bg)" stroke="url(#ac)" stroke-width="1.5" stroke-opacity="0.7"/>')
    o.append('<g clip-path="url(#c)">')
    o.append('<rect x="-300" y="0" width="260" height="92" fill="url(#shine)"><animate attributeName="x" from="-300" to="1300" dur="4.5s" repeatCount="indefinite"/></rect>')
    o.append('<rect x="-200" y="88" width="200" height="3" fill="url(#ac)"><animate attributeName="x" from="-200" to="1200" dur="3.5s" repeatCount="indefinite"/></rect>')
    o.append('</g>')
    o.append(f'<rect x="26" y="22" width="5" height="48" rx="2.5" fill="url(#ac)"><animate attributeName="opacity" values="0.5;1;0.5" dur="2.4s" repeatCount="indefinite"/></rect>')
    o.append(T(50, 36, tag, 12, c1, "700", "start", MONO, 'letter-spacing="3"'))
    o.append(T(50, 69, title, 29, "#FFFFFF", "800"))
    o.append(T(1170, 62, sub, 14, MUTED, "400", "end"))
    for i in range(5):
        o.append(f'<circle cx="{1110 + i * 15}" cy="26" r="3" fill="{c1 if i % 2 == 0 else c2}"><animate attributeName="opacity" values="0.2;1;0.2" dur="1.8s" begin="{i * 0.3}s" repeatCount="indefinite"/></circle>')
    o.append("</svg>")
    save(fname, "".join(o))


# ---------------------------------------------------------------- DIVIDER
def divider():
    o = [svg_open(1200, 24, "divider")]
    o.append("""<defs><linearGradient id="l" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="#14B8A6" stop-opacity="0"/><stop offset="0.3" stop-color="#14B8A6"/><stop offset="0.7" stop-color="#8B5CF6"/><stop offset="1" stop-color="#8B5CF6" stop-opacity="0"/></linearGradient>
<radialGradient id="g"><stop offset="0" stop-color="#5EEAD4"/><stop offset="1" stop-color="#5EEAD4" stop-opacity="0"/></radialGradient></defs>""")
    o.append(f'<rect width="1200" height="24" fill="{BG}"/>')
    o.append('<rect x="0" y="11" width="1200" height="2" fill="url(#l)"/>')
    o.append('<circle cx="0" cy="12" r="9" fill="url(#g)"><animate attributeName="cx" from="0" to="1200" dur="5s" repeatCount="indefinite"/></circle>')
    o.append(f'<rect x="594" y="6" width="12" height="12" rx="2" fill="{BG}" stroke="{MINT}" stroke-width="1.5" transform="rotate(45 600 12)"><animateTransform attributeName="transform" type="rotate" from="45 600 12" to="405 600 12" dur="8s" repeatCount="indefinite"/></rect>')
    o.append("</svg>")
    save("divider.svg", "".join(o))


# ---------------------------------------------------------------- ABOUT
def about_cards():
    W = 1200
    interests = ["Software and full-stack development", "AI-powered applications and workflow automation",
                 "Odoo and enterprise resource planning", "ERP security monitoring and compliance",
                 "Database design and management", "API integration and system design"]
    principles = ["Understand the problem before choosing tools.", "Prefer maintainable and testable implementations.",
                  "Treat security as part of system design.", "Use automation to remove repetitive work.",
                  "Learn by building, testing, and improving."]
    H = 470
    o = [svg_open(W, H, "About Muhammad Sanwal")]
    o.append(f"""<defs>
<linearGradient id="pg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0F1A2C"/><stop offset="1" stop-color="#0B1322"/></linearGradient>
<linearGradient id="ig" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<linearGradient id="pgr" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{VIOLET}"/><stop offset="1" stop-color="#EC4899"/></linearGradient>
</defs>""")
    o.append(f'<rect width="{W}" height="{H}" rx="22" fill="{BG}"/>')
    # intro
    o.append(f'<rect x="14" y="14" width="1172" height="150" rx="18" fill="url(#pg)" stroke="{TEAL}" stroke-opacity="0.45"/>')
    o.append(f'<rect x="14" y="14" width="1172" height="150" rx="18" fill="none" stroke="{MINT}" stroke-width="2" stroke-dasharray="140 2500"><animate attributeName="stroke-dashoffset" from="0" to="-2640" dur="9s" repeatCount="indefinite"/></rect>')
    o.append(T(40, 52, "SOFTWARE DEVELOPER  |  IT STUDENT", 14, MINT, "700", "start", MONO, 'letter-spacing="3"'))
    lines = ["I am Muhammad Sanwal, a Bachelor of Science in Information Technology student at the University of the Punjab,",
             "Lahore, Pakistan. I am interested in building useful software, integrating AI into practical workflows, and developing",
             "secure enterprise systems. My work spans full-stack development, backend systems, databases, Odoo, and security monitoring."]
    for i, ln in enumerate(lines):
        o.append(fade_in(i, T(40, 88 + i * 26, ln, 15, TEXT), 0.4))
    # panels
    for px, title, col, items, grad, tagc in [(14, "ENGINEERING INTERESTS", TEAL, interests, "ig", "01"),
                                              (606, "WORKING PRINCIPLES", VIOLET, principles, "pgr", "02")]:
        o.append(f'<rect x="{px}" y="182" width="580" height="274" rx="18" fill="url(#pg)" stroke="{col}" stroke-opacity="0.45"/>')
        o.append(f'<rect x="{px}" y="182" width="580" height="5" rx="2.5" fill="url(#{grad})"><animate attributeName="opacity" values="0.5;1;0.5" dur="3s" repeatCount="indefinite"/></rect>')
        o.append(T(px + 28, 226, tagc, 13, col, "700", "start", MONO))
        o.append(T(px + 56, 226, title, 17, "#FFFFFF", "800", "start", None, 'letter-spacing="1.5"'))
        for i, it in enumerate(items):
            y = 266 + i * 31
            icon = (f'<circle cx="{px + 36}" cy="{y - 5}" r="9" fill="{col}" fill-opacity="0.16"/>'
                    f'<circle cx="{px + 36}" cy="{y - 5}" r="3.5" fill="{col}"><animate attributeName="r" values="3;5;3" dur="2.4s" begin="{i * 0.3}s" repeatCount="indefinite"/></circle>')
            o.append(fade_in(i, icon + T(px + 58, y, it, 15, TEXT), 0.18, 0.5))
    o.append("</svg>")
    save("about-cards.svg", "".join(o))


# ---------------------------------------------------------------- STACK
BRAND = {
    "C++": ("#3C8DD6", "C+"), "Java": ("#F89820", "Jv"), "Python": ("#4B8BBE", "Py"), "JavaScript": ("#F7DF1E", "JS"),
    "HTML5": ("#E34F26", "H5"), "CSS3": ("#1E90E0", "C3"), "React": ("#61DAFB", "Re"), "Vite": ("#8E8BFF", "Vi"),
    "Node.js": ("#5FA04E", "No"), "Tailwind CSS": ("#06B6D4", "Tw"),
    "MySQL": ("#4F9AC4", "My"), "PostgreSQL": ("#5B82E0", "Pg"), "Git": ("#F05032", "Gt"), "GitHub": ("#C9D1D9", "GH"),
    "VS Code": ("#2D9CDB", "VS"), "Docker": ("#2496ED", "Dk"), "Ubuntu": ("#E95420", "Ub"),
    "Odoo": ("#B87BB0", "Od"), "Wazuh": ("#00A9E0", "Wz"),
}


def stack():
    W = 1200
    cats = [("PROGRAMMING LANGUAGES", TEAL, ["C++", "Java", "Python", "JavaScript"]),
            ("WEB DEVELOPMENT", CYAN, ["HTML5", "CSS3", "React", "Vite", "Node.js", "Tailwind CSS"]),
            ("DATABASES & TOOLS", VIOLET, ["MySQL", "PostgreSQL", "Git", "GitHub", "VS Code", "Docker", "Ubuntu"]),
            ("ENTERPRISE & SECURITY", AMBER, ["Odoo", "Wazuh"])]
    body = []
    y = 14
    idx = 0
    for cname, col, items in cats:
        x, row, pos = 38, 0, []
        for it in items:
            w = len(it) * 9.4 + 66
            if x + w > 1162:
                x, row = 38, row + 1
            pos.append((it, x, row, w))
            x += w + 14
        ph = 62 + (row + 1) * 58 + 2
        body.append(f'<rect x="14" y="{y}" width="1172" height="{ph}" rx="18" fill="{PANEL}" stroke="{col}" stroke-opacity="0.4"/>')
        body.append(f'<rect x="14" y="{y + 20}" width="5" height="22" rx="2.5" fill="{col}"/>')
        body.append(T(36, y + 37, cname, 14, col, "700", "start", MONO, 'letter-spacing="3"'))
        for it, cx, r, w in pos:
            bc, ab = BRAND[it]
            cy = y + 58 + r * 58
            dur = 2.8 + (idx % 4) * 0.5
            chip = (
                f'<g transform="translate({cx:.1f} {cy})"><g>'
                f'<rect width="{w:.1f}" height="44" rx="22" fill="{bc}" fill-opacity="0.12" stroke="{bc}" stroke-opacity="0.75"/>'
                f'<circle cx="24" cy="22" r="14" fill="{bc}"/>'
                + T(24, 26.5, ab, 11, "#0A0F1C", "800", "middle")
                + T(46, 27, it, 15, "#E6EDF3", "600")
                + f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="{dur}s" begin="-{idx * 0.35:.2f}s" repeatCount="indefinite"/>'
                f'</g></g>')
            body.append(chip)
            idx += 1
        y += ph + 14
    H = y
    o = [svg_open(W, H, "Technology stack")]
    o.append(f'<rect width="{W}" height="{H}" rx="22" fill="{BG}"/>')
    o.extend(body)
    o.append("</svg>")
    save("stack.svg", "".join(o))


# ---------------------------------------------------------------- PROJECT CARDS
def chip_row(items, x0, y0, maxw, accent, base_i=0, h=28, gap=8):
    out, x, y = [], x0, y0
    for i, it in enumerate(items):
        w = len(it) * 7.6 + 26
        if x + w > x0 + maxw:
            x, y = x0, y + h + gap
        inner = (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="14" fill="{accent}" fill-opacity="0.13" stroke="{accent}" stroke-opacity="0.6"/>'
                 + T(f"{x + w / 2:.1f}", y + 18.5, it, 12, "#E6EDF3", "600", "middle", MONO))
        out.append(fade_in(base_i + i, inner, 0.12, 0.6))
        x += w + gap
    return "".join(out)


def project_card(fname, tag, title, tagline, desc, label, bullets, tech, a1, a2, note=None):
    W, H = 580, 580
    o = [svg_open(W, H, title)]
    o.append(f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0F1A2C"/><stop offset="1" stop-color="#0A1020"/></linearGradient>
<linearGradient id="ac" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="580" y2="0"><stop offset="0" stop-color="{a1}"/><stop offset="1" stop-color="{a2}"/></linearGradient>
<linearGradient id="tt" gradientUnits="userSpaceOnUse" x1="30" y1="0" x2="330" y2="0" spreadMethod="reflect"><stop offset="0" stop-color="{a1}"/><stop offset="1" stop-color="{a2}"/>
<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="300 0" dur="4s" repeatCount="indefinite"/></linearGradient>
<clipPath id="c"><rect x="1" y="1" width="578" height="{H - 2}" rx="20"/></clipPath>
</defs>""")
    o.append(f'<rect x="1" y="1" width="578" height="{H - 2}" rx="20" fill="url(#bg)" stroke="{a1}" stroke-opacity="0.3" stroke-width="1.5"/>')
    o.append(f'<g clip-path="url(#c)"><rect x="0" y="0" width="580" height="2" fill="{a1}" opacity="0.35"><animate attributeName="y" from="0" to="{H}" dur="5s" repeatCount="indefinite"/></rect></g>')
    o.append(f'<rect x="1" y="1" width="578" height="{H - 2}" rx="20" fill="none" stroke="url(#ac)" stroke-width="2.5" stroke-dasharray="200 2200"><animate attributeName="stroke-dashoffset" from="0" to="-2400" dur="6s" repeatCount="indefinite"/></rect>')
    pw = len(tag) * 8.4 + 44
    o.append(f'<rect x="30" y="26" width="{pw:.0f}" height="26" rx="13" fill="{a1}" fill-opacity="0.15" stroke="{a1}" stroke-opacity="0.7"/>')
    o.append(f'<circle cx="46" cy="39" r="4" fill="{a1}"><animate attributeName="opacity" values="0.3;1;0.3" dur="1.6s" repeatCount="indefinite"/></circle>')
    o.append(T(58, 43, tag, 11, a1, "700", "start", MONO, 'letter-spacing="2"'))
    o.append(T(30, 108, title, 42, "url(#tt)", "800"))
    o.append(T(30, 138, tagline, 15, "#E6EDF3", "600"))
    for i, ln in enumerate(desc):
        o.append(T(30, 168 + i * 20, ln, 13, MUTED))
    o.append(f'<rect x="30" y="232" width="520" height="1.5" fill="url(#ac)" opacity="0.5"/>')
    o.append(T(30, 262, label, 12, a1, "700", "start", MONO, 'letter-spacing="3"'))
    for i, b in enumerate(bullets):
        y = 292 + i * 27
        icon = (f'<circle cx="38" cy="{y - 4}" r="9" fill="{a1}" fill-opacity="0.16"/>'
                f'<path d="M33.5 {y - 4} l3 3 l5.5 -6" fill="none" stroke="{a1}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
        o.append(fade_in(i, icon + T(58, y, b, 14, TEXT), 0.15, 0.3))
    ty = 292 + len(bullets) * 27 + 20
    o.append(T(30, ty, "TECHNOLOGY STACK", 12, a2, "700", "start", MONO, 'letter-spacing="3"'))
    o.append(chip_row(tech, 30, ty + 14, 520, a2))
    if note:
        o.append(T(30, H - 20, note, 11, "#6B7A93", "400", "start", FONT, 'font-style="italic"'))
    o.append("</svg>")
    save(fname, "".join(o))


# ---------------------------------------------------------------- FOCUS CARDS
def focus_cards():
    cols = [("SOFTWARE", "</>", TEAL, ["Full-stack development", "Backend systems", "REST APIs", "Object-oriented programming", "Data structures and algorithms"]),
            ("AI & AUTOMATION", "AI", VIOLET, ["LLM-powered applications", "AI API integration", "Intelligent assistants", "Workflow automation", "Practical AI solutions"]),
            ("ENTERPRISE", "ERP", AMBER, ["Odoo development", "ERP workflows", "Module customization", "Business process automation", "System integration"]),
            ("SECURITY", "SEC", ROSE, ["Security event monitoring", "Detection and alerting", "Compliance evidence", "Application hardening", "Security architecture"])]
    W, H = 1200, 320
    o = [svg_open(W, H, "Engineering focus areas")]
    o.append(f'<defs><linearGradient id="pg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#101C30"/><stop offset="1" stop-color="#0A1120"/></linearGradient></defs>')
    o.append(f'<rect width="{W}" height="{H}" rx="22" fill="{BG}"/>')
    for i, (title, glyph, col, items) in enumerate(cols):
        x = 14 + i * 292
        g = [f'<g transform="translate({x} 14)"><g>']
        g.append(f'<rect width="274" height="292" rx="18" fill="url(#pg)" stroke="{col}" stroke-opacity="0.5"/>')
        g.append(f'<rect width="274" height="5" rx="2.5" fill="{col}"><animate attributeName="opacity" values="0.4;1;0.4" dur="2.6s" begin="{i * 0.4}s" repeatCount="indefinite"/></rect>')
        g.append(f'<circle cx="46" cy="52" r="24" fill="{col}" fill-opacity="0.15"/>')
        g.append(f'<circle cx="46" cy="52" r="31" fill="none" stroke="{col}" stroke-opacity="0.7" stroke-dasharray="5 7"><animateTransform attributeName="transform" type="rotate" from="0 46 52" to="360 46 52" dur="{10 + i * 2}s" repeatCount="indefinite"/></circle>')
        g.append(T(46, 57, glyph, 14, col, "800", "middle", MONO))
        g.append(T(92, 58, title, 17, "#FFFFFF", "800", "start", None, 'letter-spacing="1"'))
        g.append(f'<rect x="24" y="96" width="226" height="1.5" fill="{col}" opacity="0.4"/>')
        for j, it in enumerate(items):
            y = 136 + j * 30
            item = (f'<path d="M30 {y - 9} l5 5 l-5 5 l-5 -5 z" fill="{col}"/>' + T(46, y, it, 14, TEXT))
            g.append(fade_in(j, item, 0.15, 0.4 + i * 0.1))
        g.append(f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -4;0 0" dur="{3.4 + i * 0.4}s" begin="-{i}s" repeatCount="indefinite"/>')
        g.append('</g></g>')
        o.append("".join(g))
    o.append("</svg>")
    save("focus-cards.svg", "".join(o))


# ---------------------------------------------------------------- PIPELINE
def pipeline():
    W, H = 1200, 400
    o = [svg_open(W, H, "Odoo to Wazuh security pipeline")]
    o.append(f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0D1626"/><stop offset="1" stop-color="#0A0F1C"/></linearGradient>
<linearGradient id="nd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#14213A"/><stop offset="1" stop-color="#0E1830"/></linearGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#5EEAD4" stroke-opacity="0.06"/></pattern>
</defs>""")
    o.append(f'<rect width="{W}" height="{H}" rx="22" fill="url(#bg)"/><rect width="{W}" height="{H}" rx="22" fill="url(#grid)"/>')
    o.append(T(36, 44, "CURRENT ENGINEERING DIRECTION", 13, MINT, "700", "start", MONO, 'letter-spacing="4"'))
    paths = [("M200 200 H270", MINT), ("M440 200 H510", MINT), ("M680 200 C725 200 725 100 770 100", AMBER),
             ("M680 200 C725 200 725 300 770 300", ROSE), ("M940 100 C970 100 970 200 1000 200", AMBER),
             ("M940 300 C970 300 970 200 1000 200", ROSE)]
    for i, (d, col) in enumerate(paths):
        o.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity="0.35" stroke-width="2"/>')
        o.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2.5" stroke-dasharray="6 8"><animate attributeName="stroke-dashoffset" from="28" to="0" dur="1.2s" repeatCount="indefinite"/></path>')
        for k in range(2):
            o.append(f'<circle r="5" fill="{col}"><animateMotion dur="2.4s" begin="{k * 1.2 + i * 0.15:.2f}s" repeatCount="indefinite" path="{d}"/></circle>')
    o.append(T(235, 188, "events", 11, MUTED, "400", "middle", MONO))
    o.append(T(475, 188, "structured", 11, MUTED, "400", "middle", MONO))
    nodes = [(30, 152, "ODOO ENTERPRISE", "ERP event source", "#B87BB0", "Od"),
             (270, 152, "AEGISERP SENSOR", "Event collector", TEAL, "Ae"),
             (510, 152, "WAZUH MONITORING", "Decoders & rules", "#00A9E0", "Wz"),
             (770, 60, "DETECTION", "Rules & correlation", AMBER, "De"),
             (770, 260, "ALERTING", "Notifications", ROSE, "Al"),
             (1000, 152, "VISIBILITY", "& compliance evidence", MINT, "Ev")]
    for i, (x, y, title, subt, col, ab) in enumerate(nodes):
        w, h = 170, 96 if y == 152 else 80
        n = [f'<g transform="translate({x} {y})">']
        n.append(f'<rect width="{w}" height="{h}" rx="16" fill="url(#nd)" stroke="{col}" stroke-opacity="0.75" stroke-width="1.5"><animate attributeName="stroke-opacity" values="0.4;1;0.4" dur="3s" begin="{i * 0.4}s" repeatCount="indefinite"/></rect>')
        n.append(f'<circle cx="28" cy="{h / 2}" r="17" fill="{col}"/>')
        n.append(f'<circle cx="28" cy="{h / 2}" r="17" fill="none" stroke="{col}"><animate attributeName="r" values="17;27;17" dur="3s" begin="{i * 0.4}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.7;0;0.7" dur="3s" begin="{i * 0.4}s" repeatCount="indefinite"/></circle>')
        n.append(T(28, h / 2 + 4.5, ab, 12, "#0A0F1C", "800", "middle"))
        n.append(T(54, h / 2 - 4, title, 12, "#FFFFFF", "800"))
        n.append(T(54, h / 2 + 14, subt, 10.5, MUTED))
        n.append("</g>")
        o.append("".join(n))
    o.append(T(600, 378, "Odoo  →  Sensor  →  Wazuh  →  Detection + Alerting  →  Security visibility & evidence", 12, "#6B7A93", "400", "middle", MONO))
    o.append("</svg>")
    save("pipeline.svg", "".join(o))


# ---------------------------------------------------------------- EDUCATION
def education():
    W, H = 1200, 290
    o = [svg_open(W, H, "Education and achievements")]
    o.append(f"""<defs>
<linearGradient id="pg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#101C30"/><stop offset="1" stop-color="#0A1120"/></linearGradient>
<linearGradient id="tt" gradientUnits="userSpaceOnUse" x1="30" y1="0" x2="500" y2="0" spreadMethod="reflect"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="{MINT}"/>
<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="470 0" dur="5s" repeatCount="indefinite"/></linearGradient>
</defs>""")
    o.append(f'<rect width="{W}" height="{H}" rx="22" fill="{BG}"/>')
    # left
    o.append(f'<rect x="14" y="14" width="690" height="262" rx="18" fill="url(#pg)" stroke="{TEAL}" stroke-opacity="0.5"/>')
    o.append(f'<rect x="14" y="14" width="690" height="262" rx="18" fill="none" stroke="{MINT}" stroke-width="2" stroke-dasharray="160 1700"><animate attributeName="stroke-dashoffset" from="0" to="-1860" dur="8s" repeatCount="indefinite"/></rect>')
    o.append(T(44, 52, "EDUCATION", 13, TEAL, "700", "start", MONO, 'letter-spacing="4"'))
    o.append(T(44, 94, "Bachelor of Science in", 28, "url(#tt)", "800"))
    o.append(T(44, 128, "Information Technology", 28, "url(#tt)", "800"))
    o.append(T(44, 160, "University of the Punjab  ·  Lahore, Pakistan", 15, "#E6EDF3", "600"))
    o.append(f'<rect x="44" y="176" width="150" height="28" rx="14" fill="{TEAL}" fill-opacity="0.15" stroke="{TEAL}"/>')
    o.append(f'<circle cx="62" cy="190" r="4" fill="{MINT}"><animate attributeName="opacity" values="0.3;1;0.3" dur="1.5s" repeatCount="indefinite"/></circle>')
    o.append(T(76, 194.5, "2023 — PRESENT", 12, MINT, "700", "start", MONO))
    o.append(T(44, 232, "Academic interests include software engineering, database systems, data", 13.5, MUTED))
    o.append(T(44, 252, "structures, algorithms, web development, and artificial intelligence.", 13.5, MUTED))
    # right
    o.append(f'<rect x="722" y="14" width="464" height="262" rx="18" fill="url(#pg)" stroke="{VIOLET}" stroke-opacity="0.5"/>')
    o.append(T(750, 52, "ACADEMIC HIGHLIGHTS", 13, "#A78BFA", "700", "start", MONO, 'letter-spacing="4"'))
    hl = [("District-level recognition", "First position in matriculation at district level.", AMBER),
          ("Scholarship", "Fully funded scholarship at Akhuwat Institute.", CYAN),
          ("Practical development", "Software, AI application, and enterprise security projects.", ROSE)]
    for i, (t, d, col) in enumerate(hl):
        y = 92 + i * 60
        item = (f'<rect x="750" y="{y - 22}" width="5" height="44" rx="2.5" fill="{col}"/>'
                f'<circle cx="780" cy="{y}" r="14" fill="{col}" fill-opacity="0.16"/><circle cx="780" cy="{y}" r="4.5" fill="{col}"><animate attributeName="r" values="4;7;4" dur="2.4s" begin="{i * 0.5}s" repeatCount="indefinite"/></circle>'
                + T(806, y - 3, t, 15.5, "#FFFFFF", "700") + T(806, y + 17, d, 12, MUTED))
        o.append(fade_in(i, item, 0.3, 0.4))
    o.append("</svg>")
    save("education.svg", "".join(o))


# ---------------------------------------------------------------- CONNECT CARD
def connect_card():
    W, H = 1200, 120
    o = [svg_open(W, H, "Connect")]
    o.append(f"""<defs><linearGradient id="pg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0F2A2E"/><stop offset="1" stop-color="#1A1440"/></linearGradient></defs>""")
    o.append(f'<rect width="{W}" height="{H}" rx="20" fill="url(#pg)" stroke="{MINT}" stroke-opacity="0.4"/>')
    for i in range(14):
        x = 40 + i * 86
        o.append(f'<circle cx="{x}" cy="{20 + (i * 37) % 80}" r="2" fill="{MINT}" opacity="0.4"><animate attributeName="opacity" values="0.1;0.9;0.1" dur="{2 + i % 3}s" begin="-{i * 0.3:.1f}s" repeatCount="indefinite"/></circle>')
    o.append(T(600, 52, "Interested in software development, AI automation, enterprise applications,", 17, "#E6EDF3", "600", "middle"))
    o.append(T(600, 82, "and opportunities to learn through meaningful engineering work.", 17, "#E6EDF3", "600", "middle"))
    o.append("</svg>")
    save("connect-card.svg", "".join(o))


# ---------------------------------------------------------------- FOOTER
def footer():
    W, H = 1200, 240
    o = [svg_open(W, H, "Build with Purpose")]
    o.append(f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#06101C"/><stop offset="0.5" stop-color="#0A2530"/><stop offset="1" stop-color="#150F35"/></linearGradient>
<linearGradient id="tg" gradientUnits="userSpaceOnUse" x1="300" y1="0" x2="900" y2="0" spreadMethod="reflect"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.5" stop-color="{MINT}"/><stop offset="1" stop-color="{VIOLET}"/>
<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="600 0" dur="5s" repeatCount="indefinite"/></linearGradient>
<linearGradient id="w1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{TEAL}" stop-opacity="0.45"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0.05"/></linearGradient>
<linearGradient id="w2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{VIOLET}" stop-opacity="0.4"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0.05"/></linearGradient>
<clipPath id="c"><rect width="1200" height="240" rx="22"/></clipPath>
</defs>""")
    o.append('<g clip-path="url(#c)">')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    for i in range(20):
        x = (i * 61 + 30) % 1200
        y0 = 40 + (i * 41) % 130
        o.append(f'<circle cx="{x}" cy="{y0}" r="{1.5 + i % 3}" fill="{[MINT, CYAN, "#C4B5FD"][i % 3]}" opacity="0.3"><animate attributeName="cy" values="{y0};{y0 - 26};{y0}" dur="{4 + i % 4}s" begin="-{i * 0.5:.1f}s" repeatCount="indefinite"/><animate attributeName="opacity" values="0.1;0.9;0.1" dur="{4 + i % 4}s" begin="-{i * 0.5:.1f}s" repeatCount="indefinite"/></circle>')
    wave = "M0 30 Q150 0 300 30 T600 30 T900 30 T1200 30 T1500 30 T1800 30 T2100 30 T2400 30 V140 H0 Z"
    o.append(f'<g transform="translate(0 150)"><path d="{wave}" fill="url(#w2)"><animateTransform attributeName="transform" type="translate" from="-600 0" to="0 0" dur="13s" repeatCount="indefinite"/></path></g>')
    o.append(f'<g transform="translate(0 175)"><path d="{wave}" fill="url(#w1)"><animateTransform attributeName="transform" type="translate" from="0 0" to="-600 0" dur="8s" repeatCount="indefinite"/></path></g>')
    o.append(T(600, 96, "BUILD WITH PURPOSE", 54, "url(#tg)", "800", "middle", None, 'letter-spacing="6"'))
    o.append(f'<rect x="450" y="112" width="300" height="3" rx="1.5" fill="{TEAL}"><animate attributeName="width" values="40;300;40" dur="4s" repeatCount="indefinite"/><animate attributeName="x" values="580;450;580" dur="4s" repeatCount="indefinite"/></rect>')
    o.append(T(600, 146, "Learn  ·  Build  ·  Secure  ·  Automate", 16, "#E6EDF3", "500", "middle", MONO, 'letter-spacing="3"'))
    o.append("</g></svg>")
    save("footer.svg", "".join(o))


# ---------------------------------------------------------------- BUILD ALL
if __name__ == "__main__":
    header()
    divider()
    banner("banner-about.svg", "01 / PROFILE", "About Me", "Developer · learner · builder", TEAL, CYAN)
    banner("banner-stack.svg", "02 / TOOLKIT", "Technology Stack", "Languages, frameworks, databases & tools", CYAN, VIOLET)
    banner("banner-projects.svg", "03 / BUILDS", "Selected Projects", "Security, AI and full-stack work", VIOLET, "#EC4899")
    banner("banner-focus.svg", "04 / FOCUS", "Engineering Focus", "Where I invest my learning", AMBER, ROSE)
    banner("banner-stats.svg", "05 / ANALYTICS", "GitHub Analytics", "Activity, languages & consistency", TEAL, AMBER)
    banner("banner-education.svg", "06 / JOURNEY", "Education & Achievements", "Academic path and recognition", "#A78BFA", CYAN)
    banner("banner-connect.svg", "07 / CONTACT", "Let's Connect", "Open to learning and building", MINT, VIOLET)
    about_cards()
    stack()
    project_card("project-aegiserp.svg", "FYP DEVELOPMENT", "AEGISERP",
                 "Automated Security Visibility & Compliance Assurance",
                 ["A security-focused project targeting Odoo Enterprise and Wazuh",
                  "integration, designed to improve ERP security visibility and",
                  "compliance evidence."],
                 "DEVELOPMENT SCOPE",
                 ["Odoo login event monitoring", "Structured security event collection", "Sensor-to-monitoring integration",
                  "Wazuh decoders and detection rules", "Security hardening and compliance evidence"],
                 ["Odoo Enterprise", "Python", "Wazuh", "Linux", "Docker"], TEAL, CYAN,
                 note="FYP project. Lists current development goals, not a claim that every feature is complete.")
    project_card("project-fauri-madad.svg", "AI WEB APP", "FAURI MADAD",
                 "Voice-First Emergency First-Aid Assistant",
                 ["An AI-powered web application that provides structured first-aid",
                  "guidance through voice and text, with English and Urdu support."],
                 "FEATURES",
                 ["Voice and text interaction", "AI-generated emergency guidance", "Step-by-step first-aid instructions",
                  "Safety warnings and actions to avoid", "Rescue 1122 guidance", "Text-to-speech support"],
                 ["React", "Vite", "Tailwind CSS", "Gemini API", "Express", "Web Speech API", "Vercel"], VIOLET, "#EC4899")
    focus_cards()
    pipeline()
    education()
    connect_card()
    footer()
    print("Generated", len(os.listdir(OUT)), "assets in", OUT)
