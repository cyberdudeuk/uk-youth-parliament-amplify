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
# v2, 16 Nov 2026: redesigned from a scan of award-winning youth campaigns (Give an X, Bite Back, This Girl Can,
# #LikeAGirl, She Can STEM; see docs/campaign-design-brief.md), built only from Brand & style pieces:
#   aurora ground (the guide's ambient aurora, made static), liquid-glass cards (155deg film, hairline, top sheen),
#   die-cut stickers (the six primitives with a keyline), the ring mark (a ring round one word, like marking a ballot),
#   Chivo 900 display with tight tracking, Space Mono for labels, data and provenance.
# Hue carries meaning: launch and taking part 175, STEM 300, girls and young women 145, careers and leverage 70.
# Caution (25) is never used here: v1 used it for dates, a brand defect that check_art_brand() now blocks.
# Fonts are embedded (the portal's own vendored OFL woff2 files) because an SVG shown as <img> cannot load web fonts;
# without them the posters fell back to Arial.
import base64
import os
from xml.sax.saxutils import escape

INK, PAPER, MIST = "#06100f", "#f6fbfa", "#d8efe9"
DISPLAY, LABEL, BODY = "Chivo", "Space Mono", "Atkinson Hyperlegible"
FONT = f"{BODY}, {DISPLAY}, Arial, sans-serif"
_FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "vendor", "fonts")
_FONT_FILES = ((DISPLAY, 900, "chivo-latin-900-normal.woff2"), (LABEL, 700, "space-mono-latin-700-normal.woff2"),
               (BODY, 700, "atkinson-hyperlegible-latin-700-normal.woff2"))
CAMPAIGN_HUES = {"launch": 175, "stem": 300, "girls": 145, "careers": 70}


def _fontface():
    out = []
    for fam, wt, f in _FONT_FILES:
        with open(os.path.join(_FONT_DIR, f), "rb") as fh:  # closed after reading (CodeQL alert 319)
            b64 = base64.b64encode(fh.read()).decode()
        out.append(f"@font-face{{font-family:'{fam}';font-weight:{wt};src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
    return "<style>" + "".join(out) + "</style>"


def _doc2(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet" '
            f'role="img" aria-label="{escape(label)}"><title>{escape(label)}</title><defs>{_fontface()}'
            f'<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>'
            f'<filter id="lift" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#000" flood-opacity="0.35"/></filter>'
            f'<linearGradient id="film" gradientTransform="rotate(65 .5 .5)"><stop offset="0" stop-color="#fff" stop-opacity="0.10"/>'
            f'<stop offset="1" stop-color="#fff" stop-opacity="0.03"/></linearGradient></defs>{body}</svg>\n')


def _text(x, y, s, size, weight=700, fill=INK, anchor="start", spacing=0, family=None):
    fam = family or (DISPLAY if weight >= 900 else BODY)
    return (f'<text x="{x}" y="{y}" font-family="{fam}, Arial, sans-serif" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}" letter-spacing="{spacing}">{escape(s)}</text>')


def _label(x, y, s, size, fill, anchor="start"):
    return _text(x, y, s.upper(), size, 700, fill, anchor, round(size * 0.08, 1), LABEL)


def _display(x, y, lines, size, fill, gap=None):
    gap = gap or size * 0.98
    return "".join(_text(x, y + i * gap, s, size, 900, fill, spacing=round(-size * 0.035, 1)) for i, s in enumerate(lines))


def _lines(x, y, lines, size, gap, **k):
    return "".join(_text(x, y + i * gap, s, size, **k) for i, s in enumerate(lines))


def _aurora(w, h, hues, dark=True):
    a = 0.55 if dark else 0.30
    spots = [(0.15, 0.12, 0.55), (0.85, 0.22, 0.45), (0.30, 0.55, 0.40), (0.90, 0.75, 0.50)]
    out = []
    for i, (fx, fy, fr) in enumerate(spots):
        hue = hues[i % len(hues)]
        out.append(f'<circle cx="{w * fx:.0f}" cy="{h * fy:.0f}" r="{min(w, h) * fr:.0f}" fill="{_c(0.62, 0.17, hue, a)}" filter="url(#blur)"/>')
    return "".join(out)


def _glass(x, y, w, h, r=22, dark=True):
    edge = "rgba(255,255,255,0.22)" if dark else "rgba(6,16,15,0.12)"
    fill = "url(#film)" if dark else "rgba(255,255,255,0.72)"
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{edge}" stroke-width="1"/>'
            f'<path d="M{x + r} {y + 1.5} H{x + w - r}" stroke="rgba(255,255,255,{0.45 if dark else 0.9})" stroke-width="1.2" stroke-linecap="round"/>')


def _shape(kind, x, y, s, fill, stroke="none", sw=0):
    st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"'
    if kind == "circle":
        return f'<circle cx="{x}" cy="{y}" r="{s / 2:.1f}" fill="{fill}"{st}/>'
    if kind == "ring":
        return (f'<circle cx="{x}" cy="{y}" r="{s / 2:.1f}" fill="none" stroke="{stroke if sw else fill}" stroke-width="{s * 0.30 + sw:.1f}"/>'
                + (f'<circle cx="{x}" cy="{y}" r="{s / 2:.1f}" fill="none" stroke="{fill}" stroke-width="{s * 0.30:.1f}"/>' if sw else ""))
    if kind == "square":
        return f'<rect x="{x - s / 2:.1f}" y="{y - s / 2:.1f}" width="{s}" height="{s}" rx="{s * 0.14:.1f}" fill="{fill}"{st}/>'
    if kind == "diamond":
        return f'<rect x="{x - s * 0.36:.1f}" y="{y - s * 0.36:.1f}" width="{s * 0.72:.1f}" height="{s * 0.72:.1f}" rx="{s * 0.09:.1f}" transform="rotate(45 {x} {y})" fill="{fill}"{st}/>'
    if kind == "bar":
        return f'<rect x="{x - s:.1f}" y="{y - s * 0.22:.1f}" width="{s * 2}" height="{s * 0.44:.1f}" rx="{s * 0.22:.1f}" fill="{fill}"{st}/>'
    hgt = s * 0.866  # triangle
    return f'<path d="M{x:.1f} {y - hgt * 0.6:.1f} L{x + s / 2:.1f} {y + hgt * 0.4:.1f} L{x - s / 2:.1f} {y + hgt * 0.4:.1f}Z" fill="{fill}"{st}/>'


def sticker(kind, x, y, s, hue, text="", rot=0, size=None):
    """A die-cut sticker: one primitive with a white keyline and a Space Mono word. Rotation stays within 8 degrees."""
    rot = max(-8, min(8, rot))
    body = _shape(kind, 0, 0, s, _c(0.80, 0.15, hue), "#ffffff", s * 0.07)
    if text:
        size = size or s * 0.13
        words = text.upper().split("\n")
        for i, t in enumerate(words):
            body += _text(0, (i - (len(words) - 1) / 2) * size * 1.2 + size * 0.36, t, size, 700, INK, "middle", 0.5, LABEL)
    return f'<g transform="translate({x} {y}) rotate({rot})" filter="url(#lift)">{body}</g>'


def ring_mark(cx, cy, rx, ry, hue, sw=6):
    """The ring primitive drawn round a word, slightly tilted, like marking a ballot paper."""
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{_c(0.82, 0.16, hue)}" '
            f'stroke-width="{sw}" transform="rotate(-4 {cx} {cy})" stroke-linecap="round"/>')


def _qr(qr_svg, x, y, label, fill=INK, dark=True):
    # the QR is 33 modules at scale 3 (99 px square), on a white tile with an 8 px quiet zone
    return (f'<g transform="translate({x} {y})"><rect x="-10" y="-10" width="119" height="119" rx="14" fill="#fff"/>{qr_svg}</g>'
            + _label(x + 50, y + 128, label, 9.5, MIST if dark else INK, "middle"))


def _footer(w, h, dark=True):
    return (f'<rect x="0" y="{h - 40}" width="{w}" height="40" fill="{INK}"/>'
            + _text(28, h - 16, "Amplify is independent and unofficial: not a service of the UK Youth Parliament, NYA or UK Parliament.", 10.5, 700, MIST))


UKPW = "UK Parliament Week · 23–29 Nov 2026"


def poster_involve(qr_svg):
    """Loud register. Launch and taking part (175). Placard poster: the ways in are stickers you can point at."""
    w, h, hue = 595, 842, CAMPAIGN_HUES["launch"]
    b = [f'<rect width="{w}" height="{h}" fill="{INK}"/>', _aurora(w, h, [175, 145, 300, 175])]
    b.append(_label(32, 58, "Amplify · launches 23 Nov 2026", 12, _c(0.85, 0.13, hue)))
    b.append(ring_mark(177, 207, 165, 54, hue, 7))  # behind the text, sized to "build it" (298 px at 96 px Chivo 900)
    b.append(_display(28, 150, ["Help", "build it."], 96, "#ffffff", 92))
    b.append(_lines(32, 300, ["No coding needed. Pick one:"], 19, 24, weight=700, fill=MIST))
    picks = [("circle", 120, 395, 150, 175, "Check\na fact", -6), ("diamond", 300, 385, 160, 300, "Test it\nwith a\nscreen\nreader", 4),
             ("square", 470, 410, 130, 70, "Suggest\nan idea", 7), ("triangle", 175, 560, 170, 145, "Design a\nposter", -3),
             ("ring", 420, 575, 140, 300, "", 0), ("bar", 420, 575, 0.1, 300, "", 0)]
    for k, x, y, s, hh, t, r in picks[:4]:
        b.append(sticker(k, x, y, s, hh, t, r, 14))
    b.append(sticker("ring", 425, 560, 150, 175, "", 5))
    b.append(_text(425, 556, "WRITE", 13, 700, "#ffffff", "middle", 0.5, LABEL) + _text(425, 573, "CODE", 13, 700, "#ffffff", "middle", 0.5, LABEL))
    b.append(_glass(28, 660, w - 56, 136, 22))
    b.append(_label(48, 700, UKPW, 11, _c(0.85, 0.13, hue)))
    b.append(_lines(48, 734, ["Youth voice, carried further. Free, no sign-in,", "open source and built in the open."], 15, 21, weight=700, fill="#ffffff"))
    b.append(_qr(qr_svg, w - 150, 676, "", INK))
    b.append(_footer(w, h))
    return _doc2(w, h, "".join(b), "Poster: Help build it. No coding needed. Pick one: check a fact, test it with a screen reader, suggest an idea, design a poster, write code. UK Parliament Week, 23 to 29 November 2026. QR code to open Amplify.")


def poster_stem(qr_svg):
    """Loud register. STEM (300) with girls and young women (145). Mantra, then the number and what it means."""
    w, h = 595, 842
    b = [f'<rect width="{w}" height="{h}" fill="{INK}"/>', _aurora(w, h, [300, 145, 300, 175])]
    b.append(_label(32, 58, "STEM spotlight · Amplify", 12, _c(0.85, 0.14, 300)))
    b.append(ring_mark(231, 249, 78, 35, 145, 6))  # behind "ship" (124 px at 64 px, after "Girls ")
    b.append(_display(28, 140, ["Girls code.", "Girls engineer.", "Girls ship."], 64, "#ffffff", 66))
    for k, x, y, s, hh, t, r in (("circle", 470, 330, 92, 300, "Code\nclub", 6), ("diamond", 395, 360, 92, 145, "Cyber", -5),
                                 ("square", 520, 410, 78, 70, "Data\n+ AI", 4)):
        b.append(sticker(k, x, y, s, hh, t, r, 11))
    b.append(_glass(28, 430, w - 56, 190, 22))
    b.append(_text(48, 512, "27.2%", 64, 900, _c(0.85, 0.15, 145), spacing=-2))
    b.append(_lines(250, 478, ["of the UK's core STEM", "workforce are women.", "You can move that", "number."], 17, 22, weight=700, fill="#ffffff"))
    b.append(_label(48, 600, "Source: WISE workforce data, Sep 2025", 9.5, MIST))
    b.append(_lines(32, 668, ["Free coding clubs, cyber and engineering", "competitions, and a real DevOps pipeline", "to learn on. Open to beginners."], 15, 21, weight=700, fill=MIST))
    b.append(_text(32, 760, "You belong in tech.", 26, 900, _c(0.85, 0.15, 145), spacing=-0.8))
    b.append(_qr(qr_svg, w - 150, 652, "", INK))
    b.append(_footer(w, h))
    return _doc2(w, h, "".join(b), "Poster: Girls code. Girls engineer. Girls ship. 27.2% of the UK's core STEM workforce are women (WISE, September 2025): you can move that number. You belong in tech. QR code to open Amplify.")


def poster_careers(qr_svg):
    """Clean register. Careers and leverage (70). Roles as identities: real Government Digital and Data job titles."""
    w, h, hue = 595, 842, CAMPAIGN_HUES["careers"]
    roles = ["Business architect", "Data architect", "Enterprise architect", "Network architect", "Security architect",
             "Solution architect", "Technical architect"]
    b = [f'<rect width="{w}" height="{h}" fill="{PAPER}"/>', _aurora(w, h, [70, 175, 70, 300], dark=False)]
    b.append(_label(32, 58, "Careers · Government Digital and Data", 11.5, _c(0.42, 0.11, hue)))
    b.append(_display(28, 135, ["Data architect.", "Security architect."], 50, INK, 54))
    b.append(ring_mark(128, 260, 118, 58, hue, 8))  # behind "You" (200 px at 110 px)
    b.append(_display(28, 300, ["You."], 110, INK))
    b.append(_glass(28, 336, w - 56, 284, 22, dark=False))
    b.append(_label(48, 368, "Seven architecture roles in government", 10.5, INK))
    kinds = ["circle", "ring", "square", "diamond", "bar", "triangle", "circle"]
    for i, r in enumerate(roles):
        y = 402 + i * 30
        b.append(_shape(kinds[i], 62, y - 6, 16 if kinds[i] != "bar" else 9, _c(0.70, 0.15, [70, 175, 300, 145][i % 4])))
        b.append(_text(88, y, r, 16, 700, INK))
    b.append(_lines(32, 662, ["Routes in include the GDS TechTrack", "Level 4 apprenticeship, Civil Service", "apprenticeships and the Fast Stream.",
                              "Many need no degree."], 14, 19, weight=700, fill=INK))
    b.append(_label(32, 752, "Roles: Government Digital and Data", 9, _c(0.38, 0.05, 175)))
    b.append(_label(32, 766, "Profession Capability Framework", 9, _c(0.38, 0.05, 175)))
    b.append(_qr(qr_svg, w - 150, 652, "Scan for routes in", INK, dark=False))
    b.append(_footer(w, h))
    return _doc2(w, h, "".join(b), "Poster: Data architect. Security architect. You. The seven architecture roles in Government Digital and Data, and routes in such as the GDS TechTrack apprenticeship. QR code to open Amplify.")


def poster_remix(qr_svg):
    """Clean register. Taking part (175). A write-your-own placard for UK Parliament Week groups. No names, no ages."""
    w, h, hue = 595, 842, CAMPAIGN_HUES["launch"]
    b = [f'<rect width="{w}" height="{h}" fill="{PAPER}"/>', _aurora(w, h, [175, 300, 70, 145], dark=False)]
    b.append(_label(32, 58, "Write your own · " + UKPW, 11, _c(0.42, 0.11, hue)))
    b.append(_display(28, 140, ["If I could", "change one", "thing, it'd be"], 62, INK, 62))
    b.append(_glass(28, 300, w - 56, 300, 22, dark=False))
    for i in range(4):
        b.append(f'<rect x="56" y="{372 + i * 62}" width="{w - 112}" height="3" rx="1.5" fill="{_c(0.55, 0.10, hue, 0.7)}"/>')
    b.append(sticker("diamond", w - 72, 300, 78, 70, "Your\nidea", 6, 11))
    b.append(_lines(32, 650, ["Take it to your MP, your council or your youth", "council. Amplify shows you how, step by step."], 15, 21, weight=700, fill=INK))
    b.append(_label(32, 712, "Don't write your name or age on it", 9.5, _c(0.38, 0.05, 175)))
    b.append(_qr(qr_svg, w - 150, 652, "Scan to open Amplify", INK, dark=False))
    b.append(_footer(w, h))
    return _doc2(w, h, "".join(b), "Poster to fill in: If I could change one thing, it'd be... Take it to your MP, your council or your youth council. Amplify shows you how. Don't write your name or age on it. QR code to open Amplify.")


def social_card():
    w = h = 1080
    b = [f'<rect width="{w}" height="{h}" fill="{INK}"/>', _aurora(w, h, [175, 300, 145, 300])]  # amber blurs to brown on ink, so it stays a sticker
    b.append(_glass(80, 300, 920, 480, 32))
    b.append(_label(140, 390, "Amplify", 28, _c(0.85, 0.13, 175)))
    b.append(ring_mark(276, 473, 162, 62, 175, 9))  # behind "Youth" (285 px at 104 px)
    b.append(_display(134, 510, ["Youth voice,", "carried further."], 104, "#ffffff", 108))
    b.append(_label(140, 720, UKPW, 26, MIST))
    for k, x, y, s, hh, t, r in (("circle", 170, 190, 150, 175, "Your\nvoice", -6), ("diamond", 900, 210, 170, 300, "STEM", 6),
                                 ("triangle", 880, 900, 190, 145, "Girls\nship", -4), ("square", 210, 900, 140, 70, "Careers", 5)):
        b.append(sticker(k, x, y, s, hh, t, r, 20))
    return _doc2(w, h, "".join(b), "Social card: Amplify. Youth voice, carried further. UK Parliament Week, 23 to 29 November 2026.")


def badge_ambassador():
    w = h = 400
    cx = cy = 200
    kinds = ["circle", "ring", "square", "diamond", "bar", "triangle"]
    ring = "".join(_shape(kinds[a % 6], cx + 150 * math.cos(a * math.pi / 9), cy + 150 * math.sin(a * math.pi / 9),
                          20 if kinds[a % 6] != "bar" else 11, _c(0.80, 0.15, list(HUE.values())[a % 4])) for a in range(18))
    b = [f'<circle cx="{cx}" cy="{cy}" r="196" fill="#ffffff"/>', f'<circle cx="{cx}" cy="{cy}" r="186" fill="{INK}"/>',
         f'<g clip-path="url(#bk)">{_aurora(w, h, [175, 300, 145, 175])}</g>', ring,
         f'<circle cx="{cx}" cy="{cy}" r="116" fill="none" stroke="{_c(0.82, 0.14, 175)}" stroke-width="9"/>',
         _shape("diamond", cx, cy - 28, 64, _c(0.86, 0.15, 70)),
         _text(cx, cy + 44, "AMBASSADOR", 25, 900, "#ffffff", "middle", -0.5),
         _label(cx, cy + 76, "Amplify", 13, _c(0.85, 0.13, 175), "middle")]
    return _doc2(w, h, f'<defs><clipPath id="bk"><circle cx="{cx}" cy="{cy}" r="186"/></clipPath></defs>' + "".join(b), "Badge: Amplify ambassador")


def sticker_sheet():
    """A4 sheet of die-cut stickers for laptops, notebooks and placards. Every sticker is one primitive in a meaningful hue."""
    w, h = 595, 842
    items = [("circle", "My\nvoice", 175), ("diamond", "Girls\nship", 145), ("square", "I code", 300), ("triangle", "Ask\nyour MP", 175),
             ("ring", "", 70), ("bar", "Built in the open", 175), ("circle", "Data\n+ AI", 300), ("diamond", "Check\nthe facts", 145),
             ("square", "No coding\nneeded", 175), ("triangle", "Future\narchitect", 70), ("circle", "You\nbelong", 145), ("square", "UKPW\n2026", 175)]
    b = [f'<rect width="{w}" height="{h}" fill="{PAPER}"/>']
    b.append(_label(32, 52, "Amplify sticker sheet · cut along the white keyline", 11, INK))
    for i, (k, t, hue) in enumerate(items):
        col, row = i % 3, i // 3
        x, y = 105 + col * 192, 160 + row * 172
        s = 130 if k != "bar" else 76
        b.append(sticker(k, x, y, s, hue, t, ((i * 5) % 13) - 6, 12.5))
        if k == "ring":
            b.append(_text(x, y + 6, "AMPLIFY", 13, 700, INK, "middle", 0.5, LABEL))
    b.append(_footer(w, h))
    return _doc2(w, h, "".join(b), "Sticker sheet: twelve Amplify stickers built from the six brand shapes, with words such as My voice, Girls ship, I code, Ask your MP and You belong.")
