"""Platform-sized campaign graphics for the graphics pack: key visuals for every channel and a six-slide carousel,
built from tools/art.py's own primitives so they match the posters and the Brand & style guide (16 Nov 2026).
The QR code on each one opens the live portal."""
import re

import segno

import art as A

LIVE = "https://cyberdudeuk.github.io/uk-youth-parliament-amplify/"
W_ = {"carried further.": 7.32, "Youth": 2.74}  # Chivo 900 width per 1 px of size (measured)
c, INK, MIST = A._c, A.INK, A.MIST
DISC = "Amplify is independent and unofficial: not a service of the UK Youth Parliament, NYA or UK Parliament."


def qr_tile(x, y, size, label=None, dark=True):
    q = segno.make(LIVE, error="m").svg_inline(scale=1, border=0, dark=INK, light="#ffffff")
    q = re.sub(r'width="\d+" height="\d+"', f'width="{size}" height="{size}" viewBox="0 0 33 33"', q, count=1)
    pad = size * 0.09
    out = f'<rect x="{x - pad}" y="{y - pad}" width="{size + 2 * pad}" height="{size + 2 * pad}" rx="{size * 0.12}" fill="#fff"/><g transform="translate({x} {y})">{q}</g>'
    if label: out += A._label(x + size / 2, y + size + pad + size * 0.16, label, max(10, size * 0.085), MIST if dark else INK, "middle")
    return out


def footer(w, h, size):
    bar = size * 2.6
    return f'<rect x="0" y="{h - bar}" width="{w}" height="{bar}" fill="{INK}"/>' + A._text(size * 2.4, h - bar * 0.38, DISC, size, 700, MIST)


def key_visual(w, h):
    port = h > w * 1.05
    pad = w * 0.06
    fs = max(11, w * 0.0125) if not port else w / 72  # the disclaimer must fit one line (it ran off the edge at w * 0.02)
    b = [f'<rect width="{w}" height="{h}" fill="{INK}"/>', A._aurora(w, h, [175, 300, 145, 175])]
    left = (w - 2 * pad) * (0.56 if not port else 1.0)
    S = min(left / W_["carried further."], h * (0.15 if not port else 0.085))
    lab = max(11, S * 0.19)
    top = pad * (0.8 if not port else 1.6)
    b.append(A._label(pad, top + lab, "Amplify \u00b7 launches Monday 23 Nov 2026", lab, c(0.85, 0.13, 175)))
    y1 = top + lab * 2.2 + S * 0.92
    b.append(A.ring_mark(pad + W_["Youth"] * S / 2, y1 - 0.36 * S, W_["Youth"] * S / 2 + S * 0.16, S * 0.52, 175, max(4, S * 0.07)))
    b.append(A._display(pad - S * 0.03, y1, ["Youth voice,", "carried further."], S, "#ffffff", S * 1.0))
    yl = y1 + S * 1.0 + S * 0.62
    b.append(A._label(pad, yl, "UK Parliament Week \u00b7 23\u201329 Nov 2026", lab * 1.05, MIST))
    ment = ["Special mentions: STEM, girls and young women", "in tech, and Government Digital and Data careers."]
    b.append(A._lines(pad, yl + lab * 2.3, ment, lab * 1.15, lab * 1.6, weight=700, fill="#ffffff"))
    if not port:
        x0 = pad + left + w * 0.04
        colw = w - pad - x0
        q = min(h * 0.30, colw * 0.42)
        st = min(h * 0.20, colw * 0.26)
        b.append(A.sticker("circle", x0 + st * 0.6, pad + st * 0.7, st, 300, "STEM", -6, st * 0.15))
        b.append(A.sticker("triangle", x0 + st * 1.95, pad + st * 0.85, st * 1.12, 145, "Girls\nin tech", 5, st * 0.12))
        b.append(A.sticker("square", x0 + st * 3.25, pad + st * 0.75, st * 0.9, 70, "Data\ncareers", 4, st * 0.12))
        b.append(qr_tile(w - pad - q, h - fs * 2.6 - q - q * 0.42, q, "Scan to open Amplify"))
        b.append(A._lines(x0, h - fs * 2.6 - q * 1.05, ["Free. No sign-in.", "Help build it:", "no coding needed."], lab * 1.15, lab * 1.6, weight=700, fill="#ffffff"))
    else:
        st = w * 0.19
        ys = yl + lab * 6.5 + st * 0.5
        b.append(A.sticker("circle", pad + st * 0.6, ys, st, 300, "STEM", -6, st * 0.15))
        b.append(A.sticker("triangle", pad + st * 1.95, ys + st * 0.05, st * 1.12, 145, "Girls\nin tech", 5, st * 0.12))
        b.append(A.sticker("square", pad + st * 3.3, ys, st * 0.9, 70, "Data\ncareers", 4, st * 0.12))
        q = w * 0.24
        b.append(qr_tile(w - pad - q, h - fs * 2.6 - q - q * 0.45, q, "Scan to open Amplify"))
        b.append(A._lines(pad, h - fs * 2.6 - q * 1.0, ["Free. No sign-in.", "Open source.", "Help build it:", "no coding needed."], lab * 1.4, lab * 1.9, weight=700, fill="#ffffff"))
    b.append(footer(w, h, fs))
    return A._doc2(w, h, "".join(b), "Amplify. Youth voice, carried further. Launches Monday 23 November 2026, UK Parliament Week. Special mentions: STEM, girls and young women in tech, Government Digital and Data careers. QR code to open Amplify. Amplify is independent and unofficial.")


def slide(w, h, n, total, hue, label, lines, ring_word=None, body=None, extra="", source=None, size=None, qr=False, alt=""):
    pad = w * 0.075
    b = [f'<rect width="{w}" height="{h}" fill="{INK}"/>', A._aurora(w, h, [hue, 175 if hue != 175 else 300, hue, 145])]
    b.append(A._label(pad, pad + 26, label, 26, c(0.86, 0.13, hue)))
    b.append(A._label(w - pad, pad + 26, f"{n}/{total}", 26, MIST, "end"))
    S = size or 120
    y1 = h * 0.30
    if ring_word:
        i, off, wf = ring_word  # line index, x offset and word width, both per 1 px of size (measured in Chivo 900)
        b.append(A.ring_mark(pad + off * S + wf * S / 2, y1 + i * S * 1.02 - 0.36 * S, wf * S / 2 + S * 0.16, S * 0.52, hue, 9))
    b.append(A._display(pad - 4, y1, lines, S, "#ffffff", S * 1.02))
    if body:
        yb = y1 + len(lines) * S * 1.02 + 40
        b.append(A._lines(pad, yb, body, 40, 54, weight=700, fill=MIST))
    if source: b.append(A._label(pad, h - 150, source, 20, MIST))
    b.append(extra)
    if qr: b.append(qr_tile(w - pad - 260, h - 470, 260, "Scan to open Amplify"))
    b.append(footer(w, h, 17))
    return A._doc2(w, h, "".join(b), alt)


def carousel():
    w, h, T = 1080, 1350, 6
    s = []
    s.append(slide(w, h, 1, T, 175, "Amplify", ["Your voice.", "Carried", "further."], (0, 0, 2.29), ["A free youth voice portal launches", "on Monday 23 November."], size=150,
                   extra=A.sticker("circle", 760, 1030, 170, 175, "Your\nvoice", -6, 24) + A.sticker("diamond", 930, 900, 150, 300, "STEM", 6, 22),
                   alt="Your voice. Carried further. A free youth voice portal launches on Monday 23 November."))
    s.append(slide(w, h, 2, T, 175, "UK Parliament Week · 23–29 Nov", ["It's about", "you."], (1, 0, 1.95),
                   ["Trusted sources, safe ways to take part", "and campaign tools for every age,", "across England, Scotland, Wales and", "Northern Ireland. No sign-in."], size=150,
                   extra=A.sticker("triangle", 880, 1060, 190, 145, "Ask\nyour MP", -4, 22),
                   alt="It's about you. Trusted sources, safe ways to take part and campaign tools for every age, across the UK. No sign-in."))
    s.append(slide(w, h, 3, T, 300, "STEM spotlight", ["Girls code.", "Girls engineer.", "Girls ship."], (2, 2.20, 2.18), ["Free coding clubs, cyber and engineering", "competitions, and a real DevOps", "pipeline to learn on."], size=118,
                   extra=A.sticker("circle", 900, 1010, 150, 300, "Code\nclub", 6, 22),
                   alt="STEM spotlight. Girls code. Girls engineer. Girls ship. Free coding clubs, cyber and engineering competitions, and a real DevOps pipeline to learn on."))
    num = (A._text(81, 560, "27.2%", 190, 900, c(0.86, 0.15, 145), spacing=-6) +
           A._lines(81, 640, ["of the UK's core STEM workforce", "are women. You can move that number."], 40, 54, weight=700, fill="#ffffff") +
           A._text(81, 920, "+149%", 150, 900, c(0.86, 0.15, 145), spacing=-5) +
           A._lines(81, 990, ["girls' A-level computing entries,", "2019 to 2025."], 40, 54, weight=700, fill="#ffffff"))
    s.append(slide(w, h, 4, T, 145, "Girls and young women in tech", [], extra=num, source="Sources: WISE workforce data, Sep 2025; WISE, STEM after COVID-19, 2026",
                   alt="27.2% of the UK's core STEM workforce are women: you can move that number. Girls' A-level computing entries rose 149% from 2019 to 2025. Sources: WISE."))
    s.append(slide(w, h, 5, T, 70, "Careers · Government Digital and Data", ["Data architect.", "Security", "architect.", "You."], (3, 0, 2.05),
                   ["Seven architecture roles. Routes in", "include the GDS TechTrack apprenticeship."], size=112,
                   extra=A.sticker("square", 900, 1100, 150, 70, "Future\narchitect", 5, 20),
                   alt="Data architect. Security architect. You. Seven architecture roles in Government Digital and Data. Routes in include the GDS TechTrack apprenticeship."))
    s.append(slide(w, h, 6, T, 175, "Launches Monday 23 Nov 2026", ["Help", "build it."], (1, 0, 3.34), ["No coding needed. Check a fact,", "test it with a screen reader or", "suggest an idea."], size=150, qr=True,
                   alt="Help build it. No coding needed. Check a fact, test it with a screen reader or suggest an idea. QR code to open Amplify."))
    return s


SIZES = {"hero-16x9": (1600, 900), "header-3x1": (1800, 600), "linkedin-1200x627": (1200, 627),
         "portrait-1080x1350": (1080, 1350), "story-1080x1920": (1080, 1920)}


def pack():
    """Every platform graphic, by file name."""
    out = {f"{n}.svg": key_visual(w, h) for n, (w, h) in SIZES.items()}
    out.update({f"carousel-{i}.svg": s for i, s in enumerate(carousel(), 1)})
    return out
