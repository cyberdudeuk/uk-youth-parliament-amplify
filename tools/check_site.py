"""Checks for the built portal in site/. Run: python3 -I tools/check_site.py

Same shape as check_repo.py: every rule names the defect or owner's rule it exists for, and every rule is proved by
a negative test at the end (a deliberately broken copy it must catch). Exit 1 on any problem or any uncaught break.

  S1  site/ is exactly what tools/build_site.py makes from app/ today: rebuilt into a temporary folder with the
      same build date, every file's SHA-256 matches (a hand edit to site/ is how a page drifts from its design)
  S2  no design-time drop-zone ships: no <image-slot> element, no "Drop the …" placeholder, no image-slot runtime
      (the design's six drop-zones would have shown "Drop the UKYP or partner logo" to the public)
  S3  the usual footer is on the portal: Disclaimers, Disclosures, Transparency, Contact, the contact form link,
      and the barcode and QR colophon (owner's rule: the usual footer on published artefacts)
  S4  no email address and no mailto: anywhere in site/: contact is by the contact form only (owner's rule, 3 Nov 2026)
  S5  the page says it is unofficial in all three places a reader can land: the splash, the masthead and the footer
      (the design names UKYP throughout; without this it reads as UKYP's own service)
  S6  every relative src/href in a site page resolves to a file in site/
  S7  nothing loads from a host a published artifact blocks: scripts only from the allowed CDNs, stylesheets only
      from Google Fonts, no remote image or tile (the design's map loaded a stylesheet from unpkg and street tiles
      from CARTO, and the CARTO tiles now return "API key required" images: found 15 November 2026)
  S8  site/build.json lists every file in site/ with the SHA-256 it has
"""
import copy, hashlib, json, os, re, sys, tempfile, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(R, "site")
sys.path.insert(0, os.path.join(R, "tools"))
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
NOT_AN_ADDRESS = re.compile(r"^(?:[\w.-]+@\d+x\.(?:png|jpg|webp))$")
SCRIPT_HOSTS = ("https://unpkg.com/", "https://cdnjs.cloudflare.com/", "https://cdn.jsdelivr.net/npm/")
STYLE_HOSTS = ("https://fonts.googleapis.com/",)
TEXT = (".html", ".js", ".json", ".svg", ".css", ".geojson")


def tree(root):
    out = {}
    for d, _, names in os.walk(root):
        for n in names:
            p = os.path.join(d, n); out[os.path.relpath(p, root).replace(os.sep, "/")] = open(p, "rb").read()
    return out


def s1(files, rebuilt):
    bad = []
    for f in sorted(set(files) | set(rebuilt)):
        if f not in rebuilt: bad.append(f"S1 site/{f} is not something the build makes: remove it or add it to the build")
        elif f not in files: bad.append(f"S1 site/{f} is missing: run tools/build_site.py")
        elif hashlib.sha256(files[f]).digest() != hashlib.sha256(rebuilt[f]).digest():
            bad.append(f"S1 site/{f} differs from a fresh build: edit app/ or the build, never site/ by hand")
    return bad


def s2(texts):
    bad = []
    for f, s in texts.items():
        if not f.endswith(".html"): continue
        if "<image-slot" in s: bad.append(f"S2 site/{f} ships an <image-slot> drop-zone")
        if re.search(r'placeholder="Drop the', s): bad.append(f"S2 site/{f} ships a 'Drop the …' placeholder")
        if "image-slot.js" in s: bad.append(f"S2 site/{f} loads the design-time image-slot runtime")
    return bad


def s3(texts):
    s = texts.get("index.html", ""); m = re.search(r"<footer\b.*?</footer>", s, re.S)
    if not m: return ["S3 site/index.html has no footer"]
    f = m.group(0); bad = []
    for need in ("Disclaimers", "Disclosures", "Transparency", "Contact", "issues/new?template=contact.yml", "./art/qr.svg", "./art/barcode.svg", "Colophon"):
        if need not in f: bad.append(f"S3 the footer lacks {need}")
    return bad


def s4(texts):
    bad = []
    for f, s in texts.items():
        if "mailto:" in s: bad.append(f"S4 site/{f} has a mailto: link: contact is by the contact form only")
        for m in EMAIL.finditer(s):
            if not NOT_AN_ADDRESS.match(m.group(0)): bad.append(f"S4 site/{f} carries an email address ({m.group(0)[:3]}…)")
    return bad


def s5(texts):
    s = texts.get("index.html", ""); bad = []
    splash = s.find("it says so on the screen."); head = re.search(r"<header\b.*?</header>", s, re.S); foot = re.search(r"<footer\b.*?</footer>", s, re.S)
    if splash < 0 or "unofficial prototype" not in s[splash:splash + 400]: bad.append("S5 the splash does not say the portal is an unofficial prototype")
    if not head or "Unofficial prototype" not in head.group(0): bad.append("S5 the masthead does not say the portal is an unofficial prototype")
    if not foot or "not endorsed by" not in foot.group(0): bad.append("S5 the footer does not disclaim endorsement")
    return bad


def s6(texts, have):
    bad = []
    for f, s in texts.items():
        if not f.endswith(".html"): continue
        for v in re.findall(r"""(?:src|href)\s*=\s*["']([^"'#?]+)""", s):
            if re.match(r"^(?:[a-z]+:|//|\{\{|data:|#)", v, re.I) or not v.strip(): continue
            q = os.path.normpath(os.path.join(os.path.dirname(f), urllib.parse.unquote(v))).replace(os.sep, "/")
            if q not in have: bad.append(f"S6 site/{f} loads {v}, which is not in site/")
    return bad


def s7(texts):
    bad = []
    for f, s in texts.items():
        if not f.endswith((".html", ".js")): continue
        for u in re.findall(r"""<script[^>]+src=["'](https?://[^"']+)""", s):
            if not u.startswith(SCRIPT_HOSTS): bad.append(f"S7 site/{f} loads a script from a blocked host: {u[:60]}")
        for u in re.findall(r"""<link[^>]+rel=["']stylesheet["'][^>]*href=["'](https?://[^"']+)""", s):
            if not u.startswith(STYLE_HOSTS): bad.append(f"S7 site/{f} loads a stylesheet from a blocked host: {u[:60]}")
        for u in re.findall(r"""<img[^>]+src=["'](https?://[^"']+)""", s):
            bad.append(f"S7 site/{f} loads a remote image, which a published artifact blocks: {u[:60]}")
        for u in re.findall(r"""tileLayer\(\s*["']([^"']+)""", s):
            bad.append(f"S7 site/{f} loads remote map tiles: {u[:60]}")
    return bad


def s8(files):
    try: man = json.loads(files["build.json"])
    except Exception: return ["S8 site/build.json is missing or not JSON"]
    bad = []
    for f, b in files.items():
        if f == "build.json": continue
        if man["files"].get(f) != hashlib.sha256(b).hexdigest(): bad.append(f"S8 build.json does not record site/{f} as it is")
    for f in man["files"]:
        if f not in files: bad.append(f"S8 build.json lists site/{f}, which does not exist")
    return bad


def texts_of(files):
    return {f: b.decode("utf-8", "replace") for f, b in files.items() if f.endswith(TEXT)}


def run(files, rebuilt):
    t = texts_of(files)
    return s1(files, rebuilt) + s2(t) + s3(t) + s4(t) + s5(t) + s6(t, set(files)) + s7(t) + s8(files)


if __name__ == "__main__":
    import build_site
    files = tree(SITE)
    if "build.json" not in files: sys.exit("S1 site/ has not been built: run python3 -I tools/build_site.py")
    date = json.loads(files["build.json"])["built"]
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "site"); build_site.build(date, out); rebuilt = tree(out)
    bad = run(files, rebuilt)
    print(f"amplify site: {len(files)} files, build of {date}, S1-S8 problems: {len(bad)}")
    if bad:
        print("\n".join(bad[:40])); sys.exit(1)

    fails = 0
    def expect(rule, got):
        global fails
        hit = any(b.startswith(rule) for b in got); fails += not hit
        print(("caught     " if hit else "NOT CAUGHT ") + rule)
    def broken(path, fn):
        f = copy.copy(files); f[path] = fn(f[path].decode()).encode(); return f
    idx = "index.html"
    expect("S1", s1(broken(idx, lambda s: s + " "), rebuilt))                                       # a hand edit to site/
    expect("S1", s1({k: v for k, v in files.items() if k != "art/hero.svg"}, rebuilt))             # a built file lost
    expect("S2", s2(texts_of(broken(idx, lambda s: s + '<image-slot id="x" placeholder="Drop the logo"></image-slot>'))))
    expect("S2", s2(texts_of(broken(idx, lambda s: s + '<script src="./image-slot.js"></script>'))))
    expect("S3", s3(texts_of(broken(idx, lambda s: re.sub(r"<footer\b.*?</footer>", "", s, flags=re.S)))))  # footer dropped
    expect("S3", s3(texts_of(broken(idx, lambda s: s.replace("./art/qr.svg", "./art/none.svg")))))       # colophon lost its QR
    expect("S4", s4(texts_of(broken(idx, lambda s: s + "write to team" + "@" + "example.gov.uk"))))
    expect("S4", s4(texts_of(broken(idx, lambda s: s + '<a href="mail' + 'to:x">x</a>'))))
    expect("S5", s5(texts_of(broken(idx, lambda s: s.replace("Unofficial prototype</span>\n    </div>", "</span>\n    </div>").replace('title="Not a service of the UK Youth Parliament, the National Youth Agency or UK Parliament"', "").replace(">Unofficial prototype</span>", "></span>")))))
    expect("S6", s6(texts_of(broken(idx, lambda s: s + '<img src="./art/missing.svg">')), set(files)))
    expect("S7", s7(texts_of(broken("Local Routes Map.html", lambda s: s + '<link rel="stylesheet" href="https://unpkg.com/x.css">'))))
    expect("S7", s7(texts_of(broken("Local Routes Map.html", lambda s: s + 'L.tileLayer("https://{s}.basemaps.cartocdn.com/{z}/{x}/{y}.png")'))))
    expect("S8", s8(broken("art/qr.svg", lambda s: s + " ")))
    sys.exit(1 if fails else 0)
