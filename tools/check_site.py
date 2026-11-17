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
  S9  nothing in a site page reaches another host before the visitor clicks: no external script, stylesheet,
      preconnect or font (defect D5: the design told unpkg and Google every visitor's IP address)
  S11 CHANGELOG.md, docs/registers.md and docs/research/ are exactly what tools/make_docs.py writes from data/ (no
      hand-kept copy)
  S12 every drawer screen has a tooltip and explainer in data/tooltips.json, and every term or control tooltip the
      page names (data-tip="term:..." or "ui:...") exists, so no tooltip is ever empty (owner's request, 15 Nov 2026)
  S13 the service design hangs together: every explainer persona has a service-design persona and the reverse,
      every story, journey stage and persona names a real persona and drawer screen, every story is proved by a real
      check id, and every blueprint layer has one cell per phase (UCD artefacts must not drift from the portal)
  S14 accuracy guards on what the page claims: no other organisation linked inside the UK Youth Parliament's name (D13),
      votes at 16 never stated as law while the Bill is before Parliament (D14), and the splash's typed manifesto line
      always credited as Amplify's own words, not a quotation (D15)
  S15 go-live readiness is honest: every passed or partial gate names evidence that is a real check (or a named
      workflow), every gate not passed names who must act, and every open item it cites exists in the registers
  S16 every new word is in the glossary, thesaurus, knowledge graph and tooltips at once: each glossary term is in a
      release (and no two releases share a version), written into the built graph and list, links only to real nodes, and every tooltip term has an entry
  S17 the product backlog and roadmap trace to real screens and real checks, and the alerts strip, Share button and a
      pausable, reduced-motion-safe news ticker are on the page
  S18 the privacy promise matches what the pledge form does: no "no name" claim while it asks for one, the name box
      says it is optional and saved only on this device, a "Clear my pledges from this device" control removes the
      pledges from storage, and every browser-storage access sits inside try/catch (defect D27)
  S19 while readiness gate G06 (a named safeguarding lead and procedure) is not passed, nothing on the portal invites
      a young person to sign up for research or as an ambassador: no sign-up link, the pause and its reason are on
      both screens and in the data, and the route to withdraw a research contribution stays (defect D25)
  S20 campaign art follows Brand & style: every Campaign kit asset exists, never uses the Caution hue (25), embeds
      the portal's own fonts (an SVG shown as an image cannot load web fonts), and the kit's posts carry no emoji or
      exclamation marks (defects D30 and D31, 16 November 2026; the guide's voice rule); and the kit offers one graphics
      pack holding every asset plus the platform sizes, linked from the screen (D32: the kit had no pack); every film
      listed exists with its poster frame and a transcript, and none plays by itself
  S21 Inside Parliament stays sourced and timeless: every fact in data/parliament.json names at least one source
      (editorial notes excepted), every source it names exists, every source is used, every source has an https link,
      a V or S provenance and a checked date, no role card names a person, every tab has its panel, and the tabs keep
      their tablist, tab and tabpanel semantics (defect D36, 17 November 2026); the same rules cover data/civic.json,
      where every section must also belong to a real tab and have a known type, and every age-ladder item must say
      which nation it applies to (defect D37: an age rule shown without its nation is wrong for three nations of four)
  S10 every CDN file the design runtime would fetch is mapped to the portal's own copy in window.__resources
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
    if re.search(r"Google Fonts|unpkg", f): bad.append("S3 the footer still says fonts or scripts come from Google or unpkg; they are served by the portal itself (defect D7)")
    for need in ("Disclaimers", "Disclosures", "Transparency", "Contact", "issues/new?template=contact.yml", "./art/qr.svg", "./art/barcode.svg", "Colophon"):
        if need not in f: bad.append(f"S3 the footer lacks {need}")
    return bad


def s4(texts):
    bad = []
    for f, s in texts.items():
        if re.search(r"mailto:\S", s): bad.append(f"S4 site/{f} has a mailto: link: contact is by the contact form only")
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
            if re.match(r"^(?:[a-z]+:|//|\{\{|data:|#)", v, re.I) or not v.strip() or v.startswith(" ") or "+" in v: continue
            q = os.path.normpath(os.path.join(os.path.dirname(f), urllib.parse.unquote(v))).replace(os.sep, "/")
            if q not in have: bad.append(f"S6 site/{f} loads {v}, which is not in site/")
    return bad


def s7(texts):
    bad = []
    for f, s in texts.items():
        if not f.endswith((".html", ".js")): continue
        for u in re.findall(r"""<script\b[^>]*?\bsrc\s*=\s*["']?((?:https?:)?//[^"'\s>]+)""", s, re.I):  # any case, spaced or unquoted (D23)
            if not u.startswith(SCRIPT_HOSTS): bad.append(f"S7 site/{f} loads a script from a blocked host: {u[:60]}")
        for u in re.findall(r"""<link[^>]+rel\s*=\s*["']stylesheet["'][^>]*href\s*=\s*["'](https?://[^"']+)""", s, re.I):
            if not u.startswith(STYLE_HOSTS): bad.append(f"S7 site/{f} loads a stylesheet from a blocked host: {u[:60]}")
        for u in re.findall(r"""<img[^>]+src\s*=\s*["'](https?://[^"']+)""", s, re.I):
            bad.append(f"S7 site/{f} loads a remote image, which a published artifact blocks: {u[:60]}")
        for u in re.findall(r"""tileLayer\(\s*["']([^"']+)""", s):
            bad.append(f"S7 site/{f} loads remote map tiles: {u[:60]}")
    return bad


def s9(texts):
    bad = []
    for f, s in texts.items():
        if not f.endswith(".html"): continue
        for tag in re.findall(r"<(?:script|link|img|iframe)\b[^>]*>", s, re.I):  # any case, any spacing (D10)
            m = re.search(r"""(?:src|href)\s*=\s*["']?(https?:)?//""", tag, re.I)
            if m: bad.append(f"S9 site/{f} reaches another host on load: {tag[:80]}")
    return bad


def s10(texts):
    page, sup = texts.get("index.html", ""), texts.get("support.js", "")
    m = re.search(r"window\.__resources\s*=\s*(\{.*?\});", page)
    mapped = json.loads(m.group(1)) if m else {}
    return [f"S10 the runtime would fetch {u} from the CDN: map it in window.__resources" for u in sorted(set(re.findall(r"https://unpkg\.com/[^\"'\s]+", sup))) if u not in mapped]


def s12(texts):
    page, raw = texts.get("index.html", ""), texts.get("data/tooltips.json", "")
    try: tt = json.loads(raw)
    except ValueError: return ["S12 site/data/tooltips.json is missing or not JSON"]
    bad = []
    screens = set(re.findall(r'\["([a-z0-9]+)", "[^"]+", "(?:dot|ring|sq|dia|bar|tri)", \d+', page))
    for sid in sorted(screens):
        if not (tt.get("screens", {}).get(sid) or {}).get("tip"): bad.append(f"S12 drawer screen {sid} has no tooltip")
    for kind, key in sorted(set(re.findall(r'data-tip="(term|ui):([a-z0-9]+)"', page))):
        pool = tt.get("terms" if kind == "term" else "ui", {})
        if key not in pool: bad.append(f"S12 the page names a {kind} tooltip {key} that data/tooltips.json does not define")
    if not screens: bad.append("S12 no drawer screens found in the page")
    return bad


def s13(texts):
    page = texts.get("index.html", "")
    try:
        tt, sd, man = (json.loads(texts.get(k, "")) for k in ("data/tooltips.json", "data/service-design.json", "build.json"))
    except ValueError:
        return ["S13 tooltips, service design or build.json is missing or not JSON"]
    bad, screens = [], set(re.findall(r'\["([a-z0-9]+)", "[^"]+", "(?:dot|ring|sq|dia|bar|tri)", \d+', page))
    checks = {c["id"] for c in man.get("checks", [])}
    tp = {p["id"] for p in tt.get("personas", [])} - {"everyone"}
    sp = {p["id"] for p in sd.get("personas", [])}
    for x in sorted(tp ^ sp): bad.append(f"S13 persona {x} is in only one of tooltips.json and service-design.json")
    for p in sd.get("personas", []):
        for sc in [p["starts"]] + p["uses"]:
            if sc not in screens: bad.append(f"S13 persona {p['id']} names a screen {sc} that is not in the drawer")
    for x in sd.get("stories", []):
        if x["persona"] not in sp: bad.append(f"S13 story {x['id']} names an unknown persona {x['persona']}")
        if x["screen"] not in screens: bad.append(f"S13 story {x['id']} names a screen {x['screen']} that is not in the drawer")
        for c in x["proved"]:
            if c not in checks: bad.append(f"S13 story {x['id']} is proved by {c}, which is not a check")
    for j in sd.get("journeys", []):
        if j["persona"] not in sp: bad.append(f"S13 journey {j['id']} names an unknown persona")
        for g in j["stages"]:
            if g["screen"] not in screens: bad.append(f"S13 journey {j['id']} stage {g['stage']} names a screen {g['screen']} that is not in the drawer")
    for b in sd.get("blueprints", []):
        for l in b["layers"]:
            if len(l["cells"]) != len(b["phases"]): bad.append(f"S13 blueprint {b['id']} layer {l['layer']} has {len(l['cells'])} cells for {len(b['phases'])} phases")
    return bad


ACCURACY = [  # (pattern that must not appear, why) - each from a defect found in review
    (r"</a>\s*Parliament", "S14 a link ends just before 'Parliament', so another organisation reads as part of the UK Youth Parliament's name (D13)"),
    (r"(?i)(?:get|gets|getting|have|has) the vote at(?:&nbsp;|\s)+16", "S14 the page states votes at 16 as law; the Bill is still before Parliament (D14)"),
    (r"(?i)public sharing is on|can appear on the pledge wall|direct messaging to adults", "S14 the page claims public sharing, a pledge wall or messaging; the portal has none: pledges stay on this device (D26)"),
    (r"(?i)one message on the day it comes back", "S14 the page promises a message on the day the petition comes back; nothing is collected, so no one can be sent one (D26)"),
    (r"(?i)relaunch is being planned", "S14 the page says a relaunch is planned; no source says so (D26)"),
    (r"(?i)a named adult confirms", "S14 the page says a named adult confirms a pledge; nothing in the portal does that (D26)"),
]


def s14(texts):
    page, bad = texts.get("index.html", ""), []
    for pat, why in ACCURACY:
        if re.search(pat, page): bad.append(why)
    if "MANIFESTO = " in page and "it is not a quotation" not in page:
        bad.append("S14 the splash types a manifesto line without saying it is Amplify's own words, not a quotation (D15)")
    return bad


NAMED_EVIDENCE = {"CodeQL", "health.yml", "upkeep task"}
PR_EVIDENCE = re.compile(r"^PR #(\d+)$")  # a merged pull request: the gate's note must record the merge and its UTC time (D28)
OWNER_DECISION = "Owner decision"          # an owner's stated decision: the note must say when it was closed and what was decided


def s15(texts):
    try:
        rd, man, reg = (json.loads(texts.get(k, "")) for k in ("data/readiness.json", "build.json", "data/registers.json"))
    except ValueError:
        return ["S15 readiness, build.json or registers is missing or not JSON"]
    checks = {c["id"] for c in man.get("checks", [])} | NAMED_EVIDENCE
    opens = {o["id"] for o in reg.get("open", [])}
    bad = []
    for g in rd.get("gates", []):
        if g["status"] in ("Pass", "Partial") and not g["evidence"]: bad.append(f"S15 gate {g['id']} is {g['status']} with no evidence")
        for e in g["evidence"]:
            m = PR_EVIDENCE.match(e)
            if m:
                if not re.search(r"pull request " + m.group(1) + r"\b.*\bmerged\b.*\bUTC\b", g["note"]): bad.append(f"S15 gate {g['id']} cites {e} but its note does not record the merge and its UTC time (D28)")
            elif e == OWNER_DECISION:
                if not re.match(r"Closed \d{1,2} \w{3} \d{4}: owner ", g["note"]): bad.append(f"S15 gate {g['id']} cites an owner decision but its note does not say when it was closed and what the owner decided")
            elif e not in checks: bad.append(f"S15 gate {g['id']} cites {e}, which is not a check")
        if g["status"] != "Pass" and not g["who"]: bad.append(f"S15 gate {g['id']} is {g['status']} but names nobody who must act")
        for o in re.findall(r"\bO\d+\b", g["who"] + " " + g["note"]):
            if o not in opens: bad.append(f"S15 gate {g['id']} cites open item {o}, which is not in the registers")
    return bad


def s16(texts):
    """S16 every new word is in the glossary, the thesaurus, the graph and the tooltips at once."""
    try:
        gl, tt, ch = (json.loads(texts.get(k, "")) for k in ("data/glossary.json", "data/tooltips.json", "data/changelog.json"))
    except ValueError:
        return ["S16 glossary, tooltips or changelog is missing or not JSON"]
    page, bad = texts.get("index.html", ""), []
    terms = {t["id"]: t for t in gl.get("terms", [])}
    if len(terms) != len(gl.get("terms", [])): bad.append("S16 two glossary terms share an id")
    m = re.search(r"\n  GRAPH = \{(.*?)\n  \};", page, re.S)
    nodes = set(re.findall(r"^    (\w+): \{ name:", m.group(1), re.M)) if m else set()
    versions = {r["version"] for r in ch.get("releases", [])}
    if len(versions) != len(ch.get("releases", [])): bad.append("S16 two releases share a version: give each release its own version (D35)")
    for t in terms.values():
        for k in ("term", "def", "also", "added"):
            if not str(t.get(k, "")).strip(): bad.append(f"S16 glossary term {t.get('id')} has no {k}")
        if t.get("added") not in versions: bad.append(f"S16 glossary term {t['id']} says it was added in {t.get('added')}, which is not a release")
        if t.get("graph") is not False and t["id"] not in nodes: bad.append(f"S16 glossary term {t['id']} is not in the knowledge graph")
        for e in t.get("edges", []):
            if e not in nodes: bad.append(f"S16 glossary term {t['id']} links to {e}, which is not in the knowledge graph")
        if t.get("list") is not False and json.dumps(t["term"]) + ", " + json.dumps(t["def"]) not in page: bad.append(f"S16 glossary term {t['id']} is not in the glossary list")
    for k, e in tt.get("terms", {}).items():
        if k not in terms: bad.append(f"S16 tooltip term {k} has no glossary entry: add it to data/glossary.json")
        elif e.get("term") != terms[k]["term"]: bad.append(f"S16 tooltip term {k} is called {e.get('term')!r} but the glossary says {terms[k]['term']!r}")
    for k in set(re.findall(r'data-tip="term:([\w-]+)"', page)):
        if k not in terms: bad.append(f"S16 a term tooltip ({k}) has no glossary entry")
    bad += parses(page)
    return bad


def parses(page):
    """D20: the injected vocabulary must leave GRAPH and GLOSSARY valid JavaScript, or the whole page fails to start."""
    import shutil, subprocess
    g = re.search(r"\n  GRAPH = (\{.*?\n  \});", page, re.S); l = re.search(r"\n  GLOSSARY = (\[.*?\n      \]);", page, re.S)
    if not g or not l: return ["S16 the page has no GRAPH or GLOSSARY to check"]
    node = shutil.which("node")
    if not node: print("note: S16 could not parse GRAPH and GLOSSARY: node is not installed"); return []
    js = "const v=[" + g.group(1) + "," + l.group(1) + "];if(!v[0]||!v[1].length)process.exit(2);"
    r = subprocess.run([node, "-e", js], capture_output=True, text=True)
    return [] if r.returncode == 0 else ["S16 GRAPH or GLOSSARY is not valid JavaScript, so the portal would not start (D20): " + (r.stderr.strip().splitlines() or ["?"])[-1][:120]]


SCREEN_ID = re.compile(r'^\s*\["([a-z0-9]+)", "[^"]+", "(?:dot|ring|sq|dia|bar|tri)", ', re.M)


def s17(texts):
    """S17 the backlog and roadmap trace to real screens and real checks; the strip and ticker are in place."""
    try:
        pd, man = (json.loads(texts.get(k, "")) for k in ("data/product.json", "build.json"))
    except ValueError:
        return ["S17 product.json or build.json is missing or not JSON"]
    page, bad = texts.get("index.html", ""), []
    screens = set(SCREEN_ID.findall(page))
    checks = {c["id"] for c in man.get("checks", [])} | NAMED_EVIDENCE
    ids = [b["id"] for b in pd.get("backlog", [])]
    if len(set(ids)) != len(ids): bad.append("S17 two requirements share an id")
    for b in pd.get("backlog", []):
        if not re.fullmatch(r"REQ-\d{2,}", b["id"]): bad.append(f"S17 {b['id']} is not a REQ-nn id")
        if b["moscow"] not in ("Must", "Should", "Could", "Won't"): bad.append(f"S17 {b['id']} has no MoSCoW priority")
        if b["status"] not in ("Done", "In progress", "Planned", "Waiting on owner"): bad.append(f"S17 {b['id']} has an unknown status {b['status']!r}")
        if not b.get("from"): bad.append(f"S17 {b['id']} does not say where it came from")
        for x in b["screens"]:
            if x not in screens: bad.append(f"S17 {b['id']} is delivered on {x}, which is not a screen")
        for c in b["checks"]:
            if c not in checks: bad.append(f"S17 {b['id']} is proved by {c}, which is not a check")
        if b["status"] == "Done" and not b["checks"]: bad.append(f"S17 {b['id']} is Done with no check proving it")
    for lane in pd.get("roadmap", []):
        for it in lane["items"]:
            for r in it["reqs"]:
                if r not in ids: bad.append(f"S17 the roadmap ({lane['lane']}) cites {r}, which is not in the backlog")
    for need, why in (('aria-label="News for this screen"', "the news ticker"), ('aria-pressed="{{ tkPaused }}"', "the ticker's pause button"),
                      ("prefers-reduced-motion: reduce) { .amp-tk-track { animation: none; } .amp-tk-dup { display: none !important; }", "the ticker standing still under reduced motion, without its duplicate (D21)"),
                      ('aria-label="Alerts for you"', "the alerts strip"), ('aria-controls="amp-share-menu"', "the Share button")):
        if need not in page: bad.append(f"S17 the page has lost {why}")
    return bad


STORAGE = re.compile(r"\b(?:localStorage|sessionStorage)\.(?:getItem|setItem|removeItem|clear)\(")


def s18(texts):
    """S18 the privacy promise matches what the pledge form does (D27)."""
    page, bad = texts.get("index.html", ""), []
    try: sg = json.loads(texts.get("data/safeguards.json", ""))
    except ValueError: return ["S18 data/safeguards.json is missing or not JSON"]
    asks_name = "Name or initials" in page
    for t in sg.get("parents", []) + [a.get("how", "") for a in sg.get("audiences", [])]:
        if asks_name and re.search(r"(?i)\bno name\b|asks for no[^.]*\bname\b", t): bad.append("S18 the safeguards say Amplify asks for no name, but the pledge form asks for a name or initials (D27)")
    if asks_name and "Name or initials (optional)" not in page: bad.append("S18 the pledge form's name box does not say it is optional (D27)")
    if asks_name and "Saved only on this device" not in page: bad.append("S18 the pledge form does not say the name is saved only on this device (D27)")
    if not re.search(r'onClick="\{\{ clearPledges \}\}"[^>]*>Clear my pledges from this device</button>', page): bad.append("S18 the pledge screen has lost its 'Clear my pledges from this device' button (D27)")
    m = re.search(r"\n  ampClearPledges\(\) \{(.*?)\n  \}", page, re.S)
    if not m or "delete p.userPledges" not in m.group(1) or "userPledges: []" not in m.group(1): bad.append("S18 clearing pledges no longer removes them from the screen and from browser storage (D27)")
    for x in STORAGE.finditer(page):
        before = page[max(0, x.start() - 400):x.start()]
        t = before.rfind("try {"); c = before.rfind("} catch")
        if t < 0 or c > t: bad.append(f"S18 browser storage is used outside try/catch, so a blocked store would break the page: …{page[x.start():x.start() + 50]}… (D27)")
    return bad


def s19(texts):
    """S19 while G06 is open, nothing invites a young person to sign up for research or as an ambassador (D25)."""
    try:
        rd, rs, iv = (json.loads(texts.get(k, "")) for k in ("data/readiness.json", "data/research.json", "data/involve.json"))
    except ValueError:
        return ["S19 readiness, research or involve data is missing or not JSON"]
    g06 = next((g for g in rd.get("gates", []) if g["id"] == "G06"), None)
    if g06 is None: return ["S19 readiness gate G06 (safeguarding lead and procedure) has gone from data/readiness.json"]
    if g06["status"] == "Pass": return []
    page, bad = texts.get("index.html", ""), []
    for hole, what in (("{{ amRegister }}", "the ambassador sign-up form"), ("{{ rsInterest }}", "registering interest in research"), ("{{ rsForm }}", "the research sign-up form"), ("template=ambassador.yml", "the ambassador sign-up form")):
        if hole in page: bad.append(f"S19 G06 is {g06['status']} but the portal links to {what} (D25)")
    for need, where in (("Signing up is paused", "Ambassadors & champions"), ("Joining the research panel is paused", "Research & design")):
        if need not in page: bad.append(f"S19 the {where} screen does not say signing up is paused (D25)")
    if "{{ rsWithdraw }}" not in page: bad.append("S19 the Research & design screen has lost the route to withdraw a research contribution, which must always stay (D25)")
    su = rs.get("sign_up", {})
    if su.get("form_url"): bad.append("S19 data/research.json has a sign-up form while G06 is open (D25)")
    if "paused" not in su.get("status_when_empty", "") or "safeguarding lead" not in su.get("status_when_empty", ""): bad.append("S19 data/research.json does not say sign-up is paused until a safeguarding lead is in place (D25)")
    if "aused" not in iv.get("ambassadors", {}).get("status", ""): bad.append("S19 data/involve.json does not say ambassador sign-ups are paused (D25)")
    if "aused" not in g06.get("note", ""): bad.append("S19 gate G06's note does not say what is paused (D25)")
    return bad


def s11(read):
    import make_docs
    bad = []
    for path, fn in make_docs.DOCS.items():
        want = fn()
        if read(path) != want: bad.append(f"S11 {path} differs from data/: run tools/build_site.py")
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


CAUTION = re.compile(r"oklch\([^)]*\s25(?:\.0)?\s*(?:/|\))")
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\u2B55]")


def s20(t, files=None):
    bad = []
    pack = (files or {}).get("art/amplify-graphics-pack.zip")
    if files is not None:
        if pack is None: bad.append("S20 the graphics pack art/amplify-graphics-pack.zip is missing (D32)")
        else:
            import io, zipfile
            zf = zipfile.ZipFile(io.BytesIO(pack)); names = set(zf.namelist())
            if any(i.compress_type != zipfile.ZIP_STORED for i in zf.infolist()):
                bad.append("S20 the graphics pack is compressed, so it cannot rebuild byte for byte on another zlib (D33)")
            try: need = [a["file"].split("/")[-1] for a in json.loads(t.get("data/involve.json", "{}"))["campaign"]["assets"]]
            except Exception: need = []
            for n in need + ["../README.txt", "../platform/hero-16x9.svg", "../platform/story-1080x1920.svg", "../platform/carousel-6.svg"]:
                full = "amplify-graphics-pack/" + ("print/" + n if not n.startswith("../") else n[3:])
                if full not in names: bad.append(f"S20 the graphics pack lacks {full} (D32)")
        if 'href="./art/amplify-graphics-pack.zip"' not in t.get("index.html", ""): bad.append("S20 the Campaign kit does not link the graphics pack (D32)")
        for v in json.loads(t.get("data/involve.json", "{}")).get("campaign", {}).get("videos", []):
            for k in ("file", "poster"):
                if v.get(k) not in files: bad.append(f"S20 campaign video {k} {v.get(k)} is missing")
            if len(v.get("transcript", "")) < 40: bad.append(f"S20 campaign video {v.get('file')} has no transcript (accessibility)")
        if re.search(r"<video[^>]*\bautoplay", t.get("index.html", ""), re.I): bad.append("S20 a campaign video plays by itself (motion must never be required)")
        page = t.get("index.html", "")
        for need in ('property="og:image" content="https://cyberdudeuk.github.io/uk-youth-parliament-amplify/site/media/campaign/share-card.jpg"', 'name="twitter:card" content="summary_large_image"', 'property="og:image:alt"'):
            if need not in page: bad.append(f"S20 the portal page lacks its link preview: {need.split(' content')[0]} (D34)")
        if "media/campaign/share-card.jpg" not in files: bad.append("S20 the link preview image media/campaign/share-card.jpg is missing (D34)")
    try: kit = json.loads(t.get("data/involve.json", "{}"))["campaign"]
    except Exception: return ["S20 data/involve.json has no campaign kit"]
    for a in kit.get("assets", []):
        svg = t.get(a["file"])
        if svg is None: bad.append(f"S20 campaign asset {a['file']} is missing"); continue
        if CAUTION.search(svg): bad.append(f"S20 {a['file']} uses the Caution hue (25), reserved for failure states (D30)")
        if "@font-face" not in svg or "data:font/woff2;base64," not in svg: bad.append(f"S20 {a['file']} does not embed its fonts (D31)")
    for post in kit.get("posts", []):
        if EMOJI.search(post["text"]) or "!" in post["text"]: bad.append(f"S20 the {post['channel']} post has an emoji or exclamation mark (voice rule)")
    return bad


def texts_of(files):
    return {f: b.decode("utf-8", "replace") for f, b in files.items() if f.endswith(TEXT)}


S21_FACTS = ("year", "week", "day", "orderpaper", "life", "roles", "building", "rules", "use")
S21_NAMES = re.compile(r"\b(?:Sir|Lady|Baroness|Earl|Dame|Rt Hon|Mr|Mrs|Ms|Dr) [A-Z][a-z]+|\bLord (?!Speaker\b|Chancellor\b|President\b|Chief\b)[A-Z][a-z]+|\b(?:Hoyle|Campbell|Forsyth|Kinnoull|Basildon|Kennedy)\b")


def s21(texts):
    """S21 Inside Parliament stays sourced and timeless (D36)."""
    raw, page = texts.get("data/parliament.json", ""), texts.get("index.html", "")
    try: pa = json.loads(raw)
    except ValueError: return ["S21 site/data/parliament.json is missing or not JSON"]
    bad, srcs = [], {x.get("id"): x for x in pa.get("sources", [])}
    used = set()
    for x in pa.get("sources", []):
        if not str(x.get("url", "")).startswith("https://"): bad.append(f"S21 source {x.get('id')} has no https link")
        if x.get("provenance") not in ("V", "S"): bad.append(f"S21 source {x.get('id')} has no V or S provenance")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(x.get("checked", ""))): bad.append(f"S21 source {x.get('id')} has no checked date")
    def take(where, ids, editorial=False):
        if not ids and not editorial: bad.append(f"S21 {where} states a fact with no source")
        for i in ids or []:
            used.add(i)
            if i not in srcs: bad.append(f"S21 {where} names source {i}, which is not in data/parliament.json")
    for k in S21_FACTS:
        for n, x in enumerate(pa.get(k, [])):
            take(f"{k}[{n}]", x.get("src"), x.get("editorial", False))
            if x.get("own_src"): take(f"{k}[{n}] own_src", [x["own_src"]])
    for k in ("week_note_src", "building_note_src"): take(k, pa.get(k))
    take("chart", (pa.get("chart") or {}).get("src"))
    for i in sorted(set(srcs) - used): bad.append(f"S21 source {i} is listed but nothing on the screen uses it")
    for r in pa.get("roles", []):
        m = S21_NAMES.search(" ".join(str(r.get(k, "")) for k in ("role", "d", "youth")))
        if m: bad.append(f"S21 role {r.get('id')} names a person ({m.group(0)}): describe the role and link to who holds it now")
        if not str(r.get("who_url", "")).startswith("https://"): bad.append(f"S21 role {r.get('id')} has no link to who holds it now")
    if 'role="tablist" aria-label="Inside Parliament"' not in page: bad.append("S21 the Inside Parliament tabs are not a labelled tablist")
    if 'role="tab" id="{{ t.tid }}" aria-controls="{{ t.pid }}" aria-selected="{{ t.sel }}"' not in page: bad.append("S21 the Inside Parliament tabs lost their tab semantics")
    for t in pa.get("tabs", []):
        if f'role="tabpanel" id="pa-panel-{t.get("id")}" aria-labelledby="pa-tab-{t.get("id")}"' not in page: bad.append(f"S21 tab {t.get('id')} has no panel")
    return bad


S21_TYPES = ("ladder", "table", "steps", "cards", "gaps")


def s21_civic(texts):
    """S21 for data/civic.json, the generic sourced-screen engine (D37)."""
    raw, page = texts.get("data/civic.json", ""), texts.get("index.html", "")
    try: cv = json.loads(raw)
    except ValueError: return ["S21 site/data/civic.json is missing or not JSON"]
    bad, srcs, used = [], {x.get("id"): x for x in cv.get("sources", [])}, set()
    tabs, nations = {t.get("id") for t in cv.get("tabs", [])}, set(cv.get("nations", []))
    for x in cv.get("sources", []):
        if not str(x.get("url", "")).startswith("https://"): bad.append(f"S21 civic source {x.get('id')} has no https link")
        if x.get("provenance") not in ("V", "S"): bad.append(f"S21 civic source {x.get('id')} has no V or S provenance")
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(x.get("checked", ""))): bad.append(f"S21 civic source {x.get('id')} has no checked date")
    def take(where, ids, editorial=False):
        if not ids and not editorial: bad.append(f"S21 civic {where} states a fact with no source")
        for i in ids or []:
            used.add(i)
            if i not in srcs: bad.append(f"S21 civic {where} names source {i}, which is not in data/civic.json")
    for n, sec in enumerate(cv.get("sections", [])):
        w = f"section {n} ({sec.get('h', '')[:30]})"
        if sec.get("tab") not in tabs: bad.append(f"S21 civic {w} belongs to no tab")
        if sec.get("type") not in S21_TYPES: bad.append(f"S21 civic {w} has unknown type {sec.get('type')}")
        if sec.get("type") == "table": take(w, sec.get("src"))
        elif sec.get("src"): take(w, sec.get("src"))
        if sec.get("type") == "gaps":
            for it in sec.get("items", []):
                if it.get("status") not in ("Built in this release", "Partly", "Next", "On Amplify"): bad.append(f"S21 civic gap {it.get('t', '')[:30]} has an unknown status")
            continue
        for k, it in enumerate(sec.get("items", [])):
            take(f"{w} item {k}", it.get("src"), it.get("editorial", False))
            if sec.get("type") == "ladder":
                wh = it.get("where") or []
                if not wh: bad.append(f"S21 civic {w} item {k} gives an age rule with no nation (D37)")
                for x in wh:
                    if x not in nations: bad.append(f"S21 civic {w} item {k} names an unknown nation {x}")
    for t in sorted(tabs):
        if not any(sec.get("tab") == t for sec in cv.get("sections", [])): bad.append(f"S21 civic tab {t} has no sections")
    for i in sorted(set(srcs) - used): bad.append(f"S21 civic source {i} is listed but nothing on the screen uses it")
    if 'role="tablist" aria-label="Every way to take part"' not in page: bad.append("S21 the Every way to take part tabs are not a labelled tablist")
    if 'role="tabpanel" id="cv-panel"' not in page: bad.append("S21 the Every way to take part tabs have no panel")
    return bad


def run(files, rebuilt):
    t = texts_of(files)
    return s1(files, rebuilt) + s2(t) + s3(t) + s4(t) + s5(t) + s6(t, set(files)) + s7(t) + s8(files) + s9(t) + s10(t) + s12(t) + s13(t) + s14(t) + s15(t) + s16(t) + s17(t) + s18(t) + s19(t) + s20(t, files) + s21(t) + s21_civic(t)


if __name__ == "__main__":
    import build_site
    files = tree(SITE)
    if "build.json" not in files: sys.exit("S1 site/ has not been built: run python3 -I tools/build_site.py")
    date = json.loads(files["build.json"])["built"]
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "site"); build_site.build(date, out); rebuilt = tree(out)
    rd = lambda p: open(os.path.join(R, p), encoding='utf-8').read() if os.path.exists(os.path.join(R, p)) else None
    bad = run(files, rebuilt) + s11(rd)
    print(f"amplify site: {len(files)} files, build of {date}, S1-S21 problems: {len(bad)}")
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
    expect("S3", s3(texts_of(broken(idx, lambda s: s.replace("Disclosures</h2>", "Disclosures</h2><p>Fonts load from Google Fonts.</p>")))))
    expect("S4", s4(texts_of(broken(idx, lambda s: s + "write to team" + "@" + "example.gov.uk"))))
    expect("S4", s4(texts_of(broken(idx, lambda s: s + '<a href="mail' + 'to:x">x</a>'))))
    expect("S5", s5(texts_of(broken(idx, lambda s: s.replace("Unofficial prototype</span>\n    </div>", "</span>\n    </div>").replace('title="Not a service of the UK Youth Parliament, the National Youth Agency or UK Parliament"', "").replace(">Unofficial prototype</span>", "></span>")))))
    expect("S6", s6(texts_of(broken(idx, lambda s: s + '<img src="./art/missing.svg">')), set(files)))
    expect("S7", s7(texts_of(broken("Local Routes Map.html", lambda s: s + '<link rel="stylesheet" href="https://unpkg.com/x.css">'))))
    expect("S7", s7(texts_of(broken("Local Routes Map.html", lambda s: s + 'L.tileLayer("https://{s}.basemaps.cartocdn.com/{z}/{x}/{y}.png")'))))
    expect("S8", s8(broken("art/qr.svg", lambda s: s + " ")))
    expect("S11", s11(lambda p: "edited by hand" if p == "CHANGELOG.md" else rd(p)))
    expect("S11", s11(lambda p: "edited by hand" if p == "docs/research/consent-forms.md" else rd(p)))   # a hand-kept research doc
    expect("S9", s9(texts_of(broken(idx, lambda s: s + '<link rel="preconnect" href="https://fonts.gstatic.com">'))))
    expect("S14", s14(texts_of(broken(idx, lambda s: s.replace("Independent &middot; not a UKYP service", '<a href="https://www.ukyouth.org/">UK Youth</a> Parliament')))))
    expect("S14", s14(texts_of(broken(idx, lambda s: s.replace("Votes at 16 is in the&nbsp;Lords.", "We get the vote at&nbsp;16.")))))
    expect("S14", s14(texts_of(broken(idx, lambda s: s.replace("it is not a quotation", "it is a line")))))
    expect("S14", s14(texts_of(broken(idx, lambda s: s + '"Your child gets the vote at 16."'))))   # a template states it as law
    rdj = "data/readiness.json"
    expect("S15", s15(texts_of(broken(rdj, lambda s: json.dumps({**json.loads(s), "gates": [{**json.loads(s)["gates"][0], "evidence": ["Z9"]}]})))))       # evidence is not a check
    expect("S15", s15(texts_of(broken(rdj, lambda s: json.dumps({**json.loads(s), "gates": [{**json.loads(s)["gates"][5], "who": ""}]})))))           # open gate, nobody to act
    expect("S15", s15(texts_of(broken(rdj, lambda s: json.dumps({**json.loads(s), "gates": [{**json.loads(s)["gates"][5], "who": "Owner (O99)"}]})))))  # cites a missing open item
    gate = lambda gid: next(g for g in json.loads(files[rdj].decode())["gates"] if g["id"] == gid)
    expect("S15", s15(texts_of(broken(rdj, lambda s: json.dumps({**json.loads(s), "gates": [{**gate("G19"), "note": "Closed."}]})))))      # PR evidence, merge not recorded (D28)
    expect("S15", s15(texts_of(broken(rdj, lambda s: json.dumps({**json.loads(s), "gates": [{**gate("G20"), "note": "Fine."}]})))))       # owner decision, undated (D28)
    expect("S14", s14(texts_of(broken(idx, lambda s: s.replace("this prototype has no public pledge wall and no messaging", "Public sharing is on, your first name and initial can appear on the pledge wall")))))  # D26
    expect("S14", s14(texts_of(broken(idx, lambda s: s.replace("A pledge here stays on this device: nothing is collected or sent.", "Pledging means you get one message on the day it comes back.")))))  # D26
    expect("S14", s14(texts_of(broken(idx, lambda s: s.replace("A pledge is a promise to sign any new petition", "A relaunch is being planned for the autumn term; a pledge is a promise to sign")))))  # D26
    expect("S14", s14(texts_of(broken(idx, lambda s: s.replace("Ask a trusted adult before you pledge.", "A named adult confirms on your behalf.")))))  # D26
    sdj = "data/service-design.json"
    def edit(fn):  # change the parsed data, not the text, so the break survives any reformatting
        def go(s):
            d = json.loads(s); fn(d); return json.dumps(d)
        return go
    expect("S13", s13(texts_of(broken(sdj, edit(lambda d: d["stories"][0].update(screen="nowhere"))))))      # a story on no screen
    expect("S13", s13(texts_of(broken(sdj, edit(lambda d: d["stories"][0].update(proved=["Z9"]))))))         # proved by no check
    expect("S13", s13(texts_of(broken(sdj, edit(lambda d: d["blueprints"][0]["layers"][0]["cells"].pop())))))  # a blueprint cell lost
    expect("S13", s13(texts_of(broken("data/tooltips.json", edit(lambda d: d["personas"].pop())))))          # personas drift
    tj = "data/tooltips.json"
    expect("S12", s12(texts_of(broken(tj, lambda s: s.replace('"stem": {"tip"', '"stem-gone": {"tip"').replace('"stem": {\n   "tip"', '"stem-gone": {\n   "tip"')))))  # a screen loses its tooltip
    expect("S12", s12(texts_of(broken(idx, lambda s: s + '<span data-tip="term:nosuchterm">x</span>'))))   # a tooltip with no text
    expect("S9", s9(texts_of(broken(idx, lambda s: s + '<SCRIPT SRC="https://cdn.example/x.js"></SCRIPT>'))))   # upper case (D10)
    expect("S9", s9(texts_of(broken(idx, lambda s: s + '<script src = //cdn.example/x.js></script>'))))          # spaced, unquoted (D10)
    expect("S7", s7(texts_of(broken(idx, lambda s: s + '<IMG SRC="https://cdn.example/a.png">'))))                # upper case (D10)
    expect("S7", s7(texts_of(broken(idx, lambda s: s + '<SCRIPT SRC = "https://cdn.example/x.js"></SCRIPT>'))))   # upper case, spaced (D23)
    expect("S7", s7(texts_of(broken(idx, lambda s: s + '<script src=//cdn.example/x.js></script>'))))            # unquoted, protocol-relative (D23)
    expect("S10", s10(texts_of(broken(idx, lambda s: s.replace("window.__resources", "window.__unused")))))
    glj, pdj = "data/glossary.json", "data/product.json"
    expect("S16", s16(texts_of(broken(glj, edit(lambda d: d["terms"].pop([t["id"] for t in d["terms"]].index("ci")))))))   # a tooltip term with no glossary entry
    expect("S16", s16(texts_of(broken(glj, edit(lambda d: d["terms"][4]["edges"].append("nowhere"))))))                   # an edge to no node
    expect("S16", s16(texts_of(broken(glj, edit(lambda d: d["terms"][4].update(added="9.9.9"))))))                         # added in no release
    expect("S16", s16(texts_of(broken("data/changelog.json", edit(lambda d: d["releases"].append(dict(d["releases"][1])))))))  # two releases share a version (D35)
    expect("S16", s16(texts_of(broken(idx, lambda s: s.replace("\n    safeguarding: { name:", "\n    safeguardingX: { name:")))))   # injection lost
    expect("S16", s16(texts_of(broken(idx, lambda s: s.replace(",  // the design's last entry has no trailing comma", "")))))  # the comma lost (D20)
    expect("S17", s17(texts_of(broken(pdj, edit(lambda d: d["backlog"][0].update(screens=["nowhere"]))))))                # traced to no screen
    expect("S17", s17(texts_of(broken(pdj, edit(lambda d: d["backlog"][0].update(checks=["Z9"]))))))                      # proved by no check
    expect("S17", s17(texts_of(broken(pdj, edit(lambda d: d["roadmap"][0]["items"][0]["reqs"].append("REQ-99"))))))      # roadmap cites a missing requirement
    expect("S17", s17(texts_of(broken(idx, lambda s: s.replace('aria-pressed="{{ tkPaused }}"', "")))))                   # ticker cannot be paused
    sgj = "data/safeguards.json"
    expect("S18", s18(texts_of(broken(sgj, edit(lambda d: d["parents"].__setitem__(0, "Amplify asks for no account, no name and no contact details."))))))  # the old claim (D27)
    expect("S18", s18(texts_of(broken(idx, lambda s: s.replace("Name or initials (optional)", "Name or initials")))))                 # name not marked optional
    expect("S18", s18(texts_of(broken(idx, lambda s: s.replace(">Clear my pledges from this device</button>", ">Clear</button>")))))  # clear control lost
    expect("S18", s18(texts_of(broken(idx, lambda s: s.replace("delete p.userPledges;", "")))))                                     # clears the screen, not storage
    expect("S18", s18(texts_of(broken(idx, lambda s: s + "<script>localStorage.setItem('userPledges', '[]');</script>"))))           # storage outside try/catch
    ivj, rsj = "data/involve.json", "data/research.json"
    expect("S19", s19(texts_of(broken(idx, lambda s: s.replace("{{ amPaused }}", "{{ amPaused }} <a href=\"{{ amRegister }}\">Open the form</a>")))))  # sign-up link back (D25)
    expect("S19", s19(texts_of(broken(idx, lambda s: s.replace("Joining the research panel is paused", "Join the research panel")))))          # pause notice lost
    expect("S19", s19(texts_of(broken(idx, lambda s: s.replace("{{ rsWithdraw }}", "#")))))                                                   # withdrawal lost
    expect("S19", s19(texts_of(broken(rsj, edit(lambda d: d["sign_up"].update(form_url="https://forms.example/x"))))))                      # a form while G06 is open
    expect("S19", s19(texts_of(broken(ivj, edit(lambda d: d["ambassadors"].update(status="Pilot. Until then you can register interest."))))))  # pause gone from data
    expect("S20", s20(texts_of(broken("art/poster-stem.svg", lambda s: s.replace("oklch(0.85 0.15 145 / 1.0)", "oklch(0.45 0.14 25 / 1.0)", 1)))))  # caution hue as decoration (D30)
    expect("S20", s20(texts_of(broken("art/social-card.svg", lambda s: s.replace("@font-face", "@font-gone")))))                    # fonts not embedded (D31)
    expect("S20", s20(texts_of(broken(ivj, edit(lambda d: d["campaign"]["assets"].append({"name": "x", "file": "art/none.svg", "alt": "x"}))))))  # asset missing
    expect("S20", s20(texts_of(broken(ivj, edit(lambda d: d["campaign"]["posts"][0].update(text="Launching soon \U0001F389"))))))  # emoji in a post
    nopack = copy.copy(files); nopack.pop("art/amplify-graphics-pack.zip")
    expect("S20", s20(texts_of(nopack), nopack))
    import io as _io, zipfile as _zf
    buf = _io.BytesIO()
    with _zf.ZipFile(buf, "w", _zf.ZIP_DEFLATED) as z:
        for i in _zf.ZipFile(_io.BytesIO(files["art/amplify-graphics-pack.zip"])).infolist(): z.writestr(i.filename, b"x", _zf.ZIP_DEFLATED)
    deflated = copy.copy(files); deflated["art/amplify-graphics-pack.zip"] = buf.getvalue()
    expect("S20", s20(texts_of(deflated), deflated))                                                                 # compressed pack (D33)
    expect("S20", s20(texts_of(broken(idx, lambda s: s.replace('property="og:image"', 'property="og:img"'))), files))  # preview image tag lost (D34)
    nocard = copy.copy(files); nocard.pop("media/campaign/share-card.jpg")
    expect("S20", s20(texts_of(nocard), nocard))                                                                     # preview image missing (D34)
    novid = copy.copy(files); novid.pop("media/campaign/short-girls-ship.mp4")
    expect("S20", s20(texts_of(novid), novid))                                                                       # a film missing
    expect("S20", s20(texts_of(broken(ivj, edit(lambda d: d["campaign"]["videos"][0].update(transcript="")))), files))  # transcript lost
    expect("S20", s20(texts_of(broken(idx, lambda s: s.replace("<video controls", "<video autoplay controls", 1))), files))  # autoplay added                                                                     # pack missing (D32)
    expect("S20", s20(texts_of(broken(idx, lambda s: s.replace('href="./art/amplify-graphics-pack.zip"', 'href="#"'))), files))  # link lost (D32)
    paj = "data/parliament.json"
    expect("S21", s21(texts_of(broken(paj, edit(lambda d: d["year"][0].update(src=[]))))))                        # a fact with no source (D36)
    expect("S21", s21(texts_of(broken(paj, edit(lambda d: d["roles"][0].update(src=["nosuch"]))))))               # an unknown source
    expect("S21", s21(texts_of(broken(paj, edit(lambda d: d["sources"].append({"id": "spare", "label": "x", "url": "https://x.example", "provenance": "V", "checked": "2026-11-17"}))))))  # a source nothing uses
    expect("S21", s21(texts_of(broken(paj, edit(lambda d: d["sources"][0].update(provenance="K"))))))              # no V or S provenance
    expect("S21", s21(texts_of(broken(paj, edit(lambda d: d["roles"][0].update(d="Currently Sir Lindsay Hoyle chairs debates."))))))  # a role names a person
    expect("S21", s21(texts_of(broken(paj, edit(lambda d: d["roles"][4].update(d="Lord Forsyth presides."))))))   # a peer named in a role card
    expect("S21", s21(texts_of(broken(idx, lambda s: s.replace('role="tablist" aria-label="Inside Parliament"', 'aria-label="Inside Parliament"')))))  # tablist lost
    expect("S21", s21(texts_of(broken(idx, lambda s: s.replace('role="tabpanel" id="pa-panel-rules"', 'id="pa-panel-rules"')))))  # a panel lost
    cvj = "data/civic.json"
    expect("S21", s21_civic(texts_of(broken(cvj, edit(lambda d: d["sections"][1]["items"][0].update(src=[]) if d["sections"][1].get("items") else d["sections"][0]["items"][0].update(src=[]))))))  # a civic fact with no source
    expect("S21", s21_civic(texts_of(broken(cvj, edit(lambda d: d["sections"][0].update(type="poster"))))))   # an unknown section type
    expect("S21", s21_civic(texts_of(broken(cvj, edit(lambda d: d["sections"][0]["items"][1].update(where=[]))))))  # an age rule with no nation (D37)
    expect("S21", s21_civic(texts_of(broken(cvj, edit(lambda d: d["sections"][0].update(tab="nowhere"))))))  # a section in no tab
    expect("S21", s21_civic(texts_of(broken(idx, lambda s: s.replace('role="tablist" aria-label="Every way to take part"', 'aria-label="Every way to take part"')))))  # tablist lost
    sys.exit(1 if fails else 0)
