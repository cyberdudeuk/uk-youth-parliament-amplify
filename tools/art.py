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


def _doc(w, h, r, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice" '
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
    for side, sign in (("gov", -1), ("opp", 1)):
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
