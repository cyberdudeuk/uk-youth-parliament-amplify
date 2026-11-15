"""The portal's still illustrations, drawn in code from the design's own six primitives.

The design's Brand & style screen allows six shapes only (circle, ring, square, diamond, bar, triangle) and one hue
per cornerstone: Participation 175, Equality 145, Education 300, Empowerment 70. In the design these spots were
image drop-zones ("Drop the UKYP or partner logo", "Hero image — MYPs at the annual sitting"); a published page
cannot show a drop-zone, and no photograph is licensed for this portal, so each becomes an illustration that
follows the brand rules. Each function returns a complete SVG document (served as an <img>, so it reads the same
in either theme: mid-tone fills over a translucent ground).
"""
import math

HUE = {"participation": 175, "equality": 145, "education": 300, "empowerment": 70}


def _c(l, c, h, a=1.0):
    return f"oklch({l} {c} {h} / {a})"


def _doc(w, h, r, body, label, fit="slice"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid {fit}" '
            f'role="img" aria-label="{label}"><title>{label}</title>'
            f'<defs><clipPath id="k"><rect width="{w}" height="{h}" rx="{r}"/></clipPath></defs>'
            f'<g clip-path="url(#k)">{body}</g></svg>\n')


def _ground(w, h, hue):
    return (f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{_c(0.62, 0.13, hue, 0.22)}"/>'
            f'<stop offset="1" stop-color="{_c(0.55, 0.10, hue, 0.06)}"/></linearGradient></defs>'
            f'<rect width="{w}" height="{h}" fill="url(#g)"/>')


def diamond(x, y, s, fill):
    return f'<rect x="{x - s / 2:.1f}" y="{y - s / 2:.1f}" width="{s}" height="{s}" rx="{s * 0.12:.1f}" transform="rotate(45 {x:.1f} {y:.1f})" fill="{fill}"/>'


def triangle(x, y, s, fill):
    hgt = s * 0.866
    return f'<path d="M{x:.1f} {y - hgt * 0.6:.1f} L{x + s / 2:.1f} {y + hgt * 0.4:.1f} L{x - s / 2:.1f} {y + hgt * 0.4:.1f}Z" fill="{fill}"/>'


def hero():
    """The annual sitting: two facing benches of members either side of the aisle, the Speaker's chair a diamond."""
    w, h = 680, 172
    hues = [175, 145, 300, 70]
    out = [_ground(w, h, 175)]
    out.append(f'<rect x="0" y="{h / 2 - 9}" width="{w}" height="18" fill="{_c(0.7, 0.05, 175, 0.10)}"/>')  # the aisle
    k = 0
    for _side, sign in (("gov", -1), ("opp", 1)):
        for row in range(3):
            y = h / 2 + sign * (26 + row * 20)
            for i in range(26):
                x = 40 + i * 24 + (row % 2) * 12
                hue = hues[(i * 7 + row * 3 + k) % 4]
                if (i * 5 + row * 11 + (1 if sign > 0 else 0)) % 9 == 0:
                    out.append(f'<circle cx="{x}" cy="{y}" r="6.5" fill="none" stroke="{_c(0.8, 0.14, hue, 0.8)}" stroke-width="2"/>')
                else:
                    out.append(f'<circle cx="{x}" cy="{y}" r="6.5" fill="{_c(0.74, 0.15, hue, 0.85)}"/>')
            k += 1
    out.append(diamond(w - 26, h / 2, 16, _c(0.86, 0.15, 70, 0.95)))
    out.append(f'<rect x="{w / 2 - 22}" y="{h / 2 - 3}" width="44" height="6" rx="3" fill="{_c(0.86, 0.12, 175, 0.9)}"/>')
    return _doc(w, h, 18, "".join(out), "Illustration: members seated on facing benches at the annual sitting")


def corner(name):
    w, h = 320, 104
    hue = HUE[name]
    fill = _c(0.76, 0.15, hue, 0.9)
    soft = _c(0.76, 0.15, hue, 0.35)
    out = [_ground(w, h, hue)]
    if name == "participation":  # a circle of people around one voice
        cx, cy = w / 2, h / 2
        out.append(f'<circle cx="{cx}" cy="{cy}" r="34" fill="none" stroke="{soft}" stroke-width="2"/>')
        for i in range(10):
            a = i / 10 * 2 * math.pi
            out.append(f'<circle cx="{cx + 34 * math.cos(a):.1f}" cy="{cy + 34 * math.sin(a):.1f}" r="7" fill="{fill}"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="11" fill="{_c(0.88, 0.14, hue)}"/>')
        for i, x in enumerate((50, 76, w - 76, w - 50)):
            out.append(f'<circle cx="{x}" cy="{cy}" r="{5 + (i % 2) * 2}" fill="{soft}"/>')
    elif name == "equality":  # equal bars, every hue, one baseline
        hues = [175, 145, 300, 70, 20, 175, 145, 300, 70]
        for i, hh in enumerate(hues):
            x = 34 + i * 30
            out.append(f'<rect x="{x}" y="28" width="18" height="52" rx="4" fill="{_c(0.75, 0.15, hh, 0.88)}"/>')
        out.append(f'<rect x="24" y="84" width="{w - 48}" height="3" rx="1.5" fill="{soft}"/>')
    elif name == "education":  # blocks that build, square on square
        for i in range(5):
            for j in range(i + 1):
                x, y = 60 + i * 26, 84 - j * 22
                out.append(f'<rect x="{x}" y="{y - 18}" width="20" height="20" rx="3" fill="{fill if j == i else soft}"/>')
        out.append(triangle(222, 40, 30, _c(0.86, 0.14, hue)))
        out.append(f'<circle cx="262" cy="64" r="9" fill="none" stroke="{fill}" stroke-width="2.5"/>')
    elif name == "empowerment":  # a voice carried outwards, rising
        x0, y0 = 70, h / 2
        out.append(triangle(x0, y0, 30, _c(0.86, 0.15, hue)))
        for i, r in enumerate((26, 44, 62, 80)):
            out.append(f'<path d="M{x0 + r * 0.5:.1f} {y0 - r * 0.62:.1f} A{r} {r} 0 0 1 {x0 + r * 0.5:.1f} {y0 + r * 0.62:.1f}" '
                       f'fill="none" stroke="{_c(0.78, 0.15, hue, 0.85 - i * 0.18)}" stroke-width="3" stroke-linecap="round"/>')
        for i in range(4):
            out.append(f'<rect x="{196 + i * 24}" y="{78 - i * 14}" width="16" height="{12 + i * 14}" rx="3" fill="{soft if i < 3 else fill}"/>')
        out.append(diamond(280, 18, 10, _c(0.88, 0.14, hue)))
    labels = {"participation": "young people in a circle around one speaker",
              "equality": "equal bars of every colour on one baseline",
              "education": "building blocks rising to a point",
              "empowerment": "a voice carried outwards and upwards"}
    return _doc(w, h, 14, "".join(out), f"Illustration for {name.title()}: {labels[name]}")


def favicon():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#06100f"/>'
            '<circle cx="27" cy="27" r="12" fill="none" stroke="#5eead4" stroke-width="6"/>'
            '<rect x="35" y="35" width="14" height="14" rx="2" transform="rotate(45 42 42)" fill="#fcd34d"/></svg>\n')


# --- campaign collateral (Campaign kit screen) ---------------------------------------------------------------
# Posters and cards follow the same brand rules: the six primitives, the four cornerstone hues, no photographs.
# Text uses the portal's own type stack; when printed from a browser without the fonts it falls back to Arial.
FONT = "Atkinson Hyperlegible, Chivo, Arial, sans-serif"
INK, PAPER = "#06100f", "#f6fbfa"


def _text(x, y, s, size, weight=700, fill=INK, anchor="start", spacing=0):
    from xml.sax.saxutils import escape
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}" letter-spacing="{spacing}">{escape(s)}</text>')


def _lines(x, y, lines, size, gap, **k):
    return "".join(_text(x, y + i * gap, s, size, **k) for i, s in enumerate(lines))


def _confetti(w, h, n, seed, scale=1.0):
    hues, out = list(HUE.values()), []
    for i in range(n):
        x = (i * 97 + seed * 31) % w
        y = (i * 59 + seed * 17) % h
        s = (10 + (i * 7) % 14) * scale
        hue, f = hues[i % 4], _c(0.74, 0.15, hues[i % 4], 0.55)
        kind = (i + seed) % 4
        if kind == 0:
            out.append(f'<circle cx="{x}" cy="{y}" r="{s / 2:.1f}" fill="{f}"/>')
        elif kind == 1:
            out.append(diamond(x, y, s * 0.8, f))
        elif kind == 2:
            out.append(triangle(x, y, s, f))
        else:
            out.append(f'<circle cx="{x}" cy="{y}" r="{s / 2:.1f}" fill="none" stroke="{_c(0.7, 0.15, hue, 0.6)}" stroke-width="2.5"/>')
    return "".join(out)


def _qr(qr_svg, x, y, label):
    # the QR is 33 modules at scale 3 (99 px square), on a white tile with an 8 px quiet zone
    return (f'<g transform="translate({x} {y})"><rect x="-8" y="-8" width="115" height="115" rx="10" fill="#fff"/>{qr_svg}</g>'
            + _text(x + 50, y + 124, label, 11, 700, anchor="middle"))


def _footer(w, h):
    return (f'<rect x="0" y="{h - 46}" width="{w}" height="46" fill="{INK}"/>'
            + _text(28, h - 18, "Amplify is independent and unofficial: not a service of the UK Youth Parliament, NYA or UK Parliament.", 11, 600, "#d8efe9"))


def poster_involve(qr_svg):
    w, h = 595, 842
    body = [f'<rect width="{w}" height="{h}" fill="{PAPER}"/>', _confetti(w, 330, 42, 3),
            f'<rect x="28" y="300" width="{w - 56}" height="6" rx="3" fill="{_c(0.7, 0.15, 175)}"/>',
            _text(28, 360, "AMPLIFY", 18, 800, _c(0.45, 0.12, 175), spacing=4),
            _lines(28, 410, ["Help build the", "portal that carries", "youth voice further"], 40, 46, weight=900),
            _lines(28, 570, ["No coding needed. Check a fact, test it with", "your screen reader, suggest an idea, design a",
                             "poster, or write code: every bit helps."], 15, 22, weight=600),
            _lines(28, 660, ["Launching in UK Parliament Week", "23 to 29 November 2026"], 16, 22, weight=800, fill=_c(0.45, 0.14, 25)),
            _qr(qr_svg, w - 158, 590, "Scan to open Amplify"), _footer(w, h)]
    return _doc(w, h, 0, "".join(body), "Poster: Help build the portal that carries youth voice further. Launching in UK Parliament Week, 23 to 29 November 2026.", "meet")


def poster_stem(qr_svg):
    w, h = 595, 842
    hue = 300
    grid = []
    for r in range(9):
        for c in range(13):
            if (r * 5 + c * 3) % 4 == 0:
                grid.append(f'<rect x="{28 + c * 42}" y="{40 + r * 30}" width="{18 + (c % 3) * 8}" height="8" rx="4" fill="{_c(0.72, 0.15, [175, 145, 300, 70][(r + c) % 4], 0.7)}"/>')
    body = [f'<rect width="{w}" height="{h}" fill="{INK}"/>', "".join(grid),
            _text(28, 350, "STEM SPOTLIGHT", 16, 800, _c(0.82, 0.14, 175), spacing=4),
            _lines(28, 400, ["Girls code.", "Girls engineer.", "Girls ship."], 46, 52, weight=900, fill="#ffffff"),
            _lines(28, 580, ["Coding clubs, cyber and engineering competitions,", "enterprise architecture and a real DevOps pipeline",
                             "to learn on. Free, and open to beginners."], 15, 22, weight=600, fill="#d8efe9"),
            _text(28, 670, "You belong in tech.", 20, 900, _c(0.82, 0.16, 70)),
            _qr(qr_svg, w - 158, 590, ""), _text(w - 108, 726, "Scan to open Amplify", 11, 700, "#d8efe9", "middle"),
            diamond(w - 60, 360, 34, _c(0.8, 0.16, hue, 0.9)), _footer(w, h)]
    return _doc(w, h, 0, "".join(body), "Poster: Girls code. Girls engineer. Girls ship. You belong in tech.", "meet")


def social_card():
    w = h = 1080
    body = [f'<rect width="{w}" height="{h}" fill="{INK}"/>', _confetti(w, h, 70, 7, 2.2),
            f'<rect x="90" y="330" width="900" height="420" rx="40" fill="{PAPER}"/>',
            _text(140, 420, "AMPLIFY", 30, 800, _c(0.45, 0.12, 175), spacing=6),
            _lines(140, 500, ["Youth voice,", "carried further."], 72, 84, weight=900),
            _text(140, 700, "UK Parliament Week · 23 to 29 November 2026", 30, 700, _c(0.45, 0.14, 25))]
    return _doc(w, h, 0, "".join(body), "Social card: Amplify. Youth voice, carried further. UK Parliament Week, 23 to 29 November 2026.", "meet")


def badge_ambassador():
    w = h = 400
    cx = cy = 200
    ring = "".join(f'<circle cx="{cx + 150 * math.cos(a * math.pi / 12):.1f}" cy="{cy + 150 * math.sin(a * math.pi / 12):.1f}" r="9" fill="{_c(0.76, 0.15, list(HUE.values())[a % 4])}"/>' for a in range(24))
    body = [f'<circle cx="{cx}" cy="{cy}" r="190" fill="{INK}"/>', ring,
            f'<circle cx="{cx}" cy="{cy}" r="118" fill="none" stroke="{_c(0.8, 0.14, 175)}" stroke-width="10"/>',
            diamond(cx, cy - 22, 54, _c(0.86, 0.15, 70)),
            _text(cx, cy + 52, "AMBASSADOR", 21, 900, "#ffffff", "middle", 2),
            _text(cx, cy + 80, "AMPLIFY", 14, 700, _c(0.82, 0.12, 175), "middle", 4)]
    return _doc(w, h, 200, "".join(body), "Badge: Amplify ambassador", "meet")
