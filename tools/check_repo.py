"""Checks for the Amplify portal repository. Run: python3 -I tools/check_repo.py

Each rule names the owner's rule or the defect it exists for, and each is proved by a negative test at the end
(a deliberately broken copy it must catch). Exit 1 on any problem or any rule that fails to catch its break.

  R1  no email address in any tracked text file: contact is by the issue form only (owner's rule, 3 November 2026)
  R2  no deck or film in the repository unless the owner says so for that piece (owner's rule); this portal has none
  R3  no blueprint or input file (uploads/, scraps/, scratch/, bp/, extract/, office documents, PDFs): they are not
      kept once their features are built (owner's rule, 8 November 2026)
  R4  every portal file is the source artifact's bytes: present, and its SHA-256 matches tools/sources.json
      (copies are made on the server, never retyped; a retyped copy is how a page silently drifts)
  R5  the petition snapshot is dated: tools/sources.json records the summary's own fetched date, and they agree;
      the file must also name its source (a summary made from Parliament's record; R5 was first written against
      an assumed raw-record shape, data.attributes.updated_at, before the file was seen: 9 November 2026)
      (the estate review's open action for this portal: "Date the petition snapshot on the page")
  R6  every relative src/href in the pages resolves to a tracked file (a page that loads a missing file is broken)
  R8  the public entry page (index.html at the root, served by GitHub Pages) opens the built portal in site/, never
      the unbuilt design in app/, and never names itself as a UK Youth Parliament service (D22; vaccinated against
      a redirect to app/ and a UKYP title)
  R9  the checks lint the Python (Ruff) and JavaScript (ESLint) and fail on any finding (D24; vaccinated against a
      checks workflow without the lint step)
  R7  people decide the irreversible: no GitHub workflow merges, pushes, force-pushes, deletes a branch, repository or
      release, publishes a release or a site, or asks for write access to contents (vaccinated against a workflow
      that runs gh pr merge)
"""
import copy, hashlib, json, os, re, subprocess, sys, urllib.parse

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = json.load(open(os.path.join(R, "tools", "sources.json"), encoding="utf-8"))
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
MEDIA = re.compile(r"(?i)(^|/)[^/]*\b(deck|film|video|showreel|newsreel|trailer|screening)\b[^/]*\.(html?|jsx)$|(^|/)(deck-stage\.js|animations-v\d+\.jsx)$")
INPUTS = re.compile(r"(?i)(^|/)(uploads|scraps|scratch|bp|extract|blueprints?)/|\.(pdf|docx?|pptx?|xlsx?)$")
TEXT = (".html", ".htm", ".js", ".jsx", ".json", ".md", ".yml", ".yaml", ".txt", ".css", ".py", ".csv")
# Strings that look like addresses but are not ones: npm-style scoped names and image-density suffixes.
NOT_AN_ADDRESS = re.compile(r"^(?:[\w.-]+@\d+x\.(?:png|jpg|webp))$")

def r1(texts):
    bad = []
    for f, s in texts.items():
        for m in EMAIL.finditer(s):
            if not NOT_AN_ADDRESS.match(m.group(0)):
                bad.append(f"R1 {f} carries an email address ({m.group(0)[:3]}…): contact is by the issue form only")
    return bad

def r2(tracked):
    return [f"R2 {f} is a deck or film: decks and films are not kept in a repository" for f in tracked if MEDIA.search(f)]

def r3(tracked):
    return [f"R3 {f} is a blueprint or input file: not kept once its features are built" for f in tracked if INPUTS.search(f)]

def r4(src, read):
    bad = []
    for path, e in src["files"].items():
        b = read(path)
        if b is None: bad.append(f"R4 {path} is missing (expected from the artifact's {e['from']})"); continue
        h = hashlib.sha256(b).hexdigest()
        if h != e["sha256"]: bad.append(f"R4 {path} is not the source bytes: {h[:12]} where the artifact has {e['sha256'][:12]}")
    return bad

def r5(src, read):
    p = src["petition"]; path = next(k for k in src["files"] if k.endswith(f"petition-{p['number']}.json"))
    b = read(path)
    if b is None: return [f"R5 {path} is missing"]
    try: rec = json.loads(b); stamp = rec["fetched"]
    except Exception: return [f"R5 {path} has no fetched date to date it by"]
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(stamp)): return [f"R5 {path} has a fetched value that is not a date: {stamp!r}"]
    if not str(rec.get("source", "")).startswith("https://petition.parliament.uk/"): return [f"R5 {path} does not name its source on petition.parliament.uk"]
    if not p.get("snapshot_date"): return [f"R5 the petition snapshot is undated: record {stamp} in tools/sources.json"]
    if p["snapshot_date"] != stamp: return [f"R5 tools/sources.json dates the snapshot {p['snapshot_date']} but the record says {stamp}"]
    return []

def r6(texts, tracked):
    have = set(tracked); bad = []
    for f, s in texts.items():
        if not f.endswith((".html", ".htm")): continue
        d = os.path.dirname(f)
        for v in re.findall(r"""(?:src|href)\s*=\s*["']([^"'#?]+)""", s):
            if re.match(r"^(?:[a-z]+:|//|\{\{|data:|#)", v, re.I) or not v.strip(): continue
            if v.startswith(" ") or "+" in v: continue  # a JavaScript string being built, not a link (D8)
            q = os.path.normpath(os.path.join(d, urllib.parse.unquote(v)))
            if q not in have: bad.append(f"R6 {f} loads {v}, which is not in the repository")
    return bad

IRREVERSIBLE = [(r"\bgh\s+pr\s+merge\b", "merges a pull request"), (r"\bgit\s+push\b", "pushes"), (r"--force\b", "forces a change"),
                (r"\bgh\s+(?:repo|release)\s+delete\b", "deletes a repository or release"), (r"\bgh\s+release\s+create\b", "publishes a release"),
                (r"actions/deploy-pages|peaceiris/actions-gh-pages", "publishes a site"), (r"\bcontents\s*:\s*write\b", "asks to write to the repository"),
                (r"\bgh\s+issue\s+delete\b", "deletes an issue"), (r"\bgh\s+api\s+.*-X\s*DELETE", "deletes through the API")]

def r7(texts):
    bad = []
    for f, s in texts.items():
        if not f.startswith(".github/workflows/"): continue
        for pat, what in IRREVERSIBLE:
            if re.search(pat, s, re.I): bad.append(f"R7 {f} {what}: only a person does that")
    return bad

def r8(read):
    b = read("index.html")
    if b is None: return ["R8 there is no index.html at the root for GitHub Pages to serve"]
    s = b.decode("utf-8", "replace"); bad = []
    m = re.search(r'http-equiv="refresh"\s+content="0;\s*url=([^"]+)"', s, re.I)
    if not m or not m.group(1).startswith("site/index.html"): bad.append("R8 index.html does not send visitors to the built portal, site/index.html (D22)")
    if re.search(r'(href|url)=["\']?app/', s, re.I): bad.append("R8 index.html points visitors at the unbuilt design in app/ (D22)")
    t = re.search(r"<title>(.*?)</title>", s, re.S | re.I)
    if not t or re.search(r"\bUK Youth Parliament\b", t.group(1), re.I) or "unofficial" not in t.group(1).lower(): bad.append("R8 the entry page title must say Amplify is unofficial and must not name it as a UK Youth Parliament service (D22, D13)")
    return bad

def r9(read):
    wf = (read(".github/workflows/checks.yml") or b"").decode("utf-8", "replace"); bad = []
    if "ruff check ." not in wf or "npx eslint ." not in wf: bad.append("R9 .github/workflows/checks.yml does not run both linters (ruff check . and npx eslint .) (D24)")
    for f in ("ruff.toml", "eslint.config.mjs"):
        if read(f) is None: bad.append(f"R9 {f} is missing (D24)")
    return bad

def run(tracked, texts, src, read):
    return r1(texts) + r2(tracked) + r3(tracked) + r4(src, read) + r5(src, read) + r6(texts, tracked) + r7(texts) + r8(read) + r9(read)

tracked = subprocess.run(["git", "ls-files"], cwd=R, capture_output=True, text=True).stdout.splitlines()
def read(path):
    try: return open(os.path.join(R, path), "rb").read()
    except FileNotFoundError: return None
texts = {f: (read(f) or b"").decode("utf-8", "replace") for f in tracked if f.endswith(TEXT)}

bad = run(tracked, texts, SRC, read)
print(f"amplify: {len(tracked)} tracked files, {len(SRC['files'])} from the artifact, R1-R8 problems: {len(bad)}")
if bad:
    print("\n".join(bad[:40])); sys.exit(1)

fails = 0
def expect(rule, got):
    global fails
    hit = any(b.startswith(rule) for b in got); fails += not hit
    print(("caught     " if hit else "NOT CAUGHT ") + rule)
page = next(k for k in SRC["files"] if k.endswith(".dc.html"))
expect("R1", r1({"README.md": "Write to team" + "@" + "example.gov.uk"}))                     # an address in prose
expect("R2", r2(tracked + ["app/Amplify Showreel.dc.html"]))                                   # a film added
expect("R2", r2(tracked + ["app/deck-stage.js"]))                                              # a deck runtime added
expect("R3", r3(tracked + ["app/uploads/brief.pdf"]))                                          # an input upload
expect("R3", r3(tracked + ["app/scraps/notes.txt"]))
expect("R4", r4(SRC, lambda p: (read(p) + b" ") if p == page else read(p)))                    # one byte changed
expect("R4", r4(SRC, lambda p: None if p == page else read(p)))                                # a file lost
s = copy.deepcopy(SRC); s["petition"]["snapshot_date"] = None; expect("R5", r5(s, read))       # undated snapshot
s = copy.deepcopy(SRC); s["petition"]["snapshot_date"] = "2000-01-01"; expect("R5", r5(s, read))           # wrong date
pet = next(k for k in SRC["files"] if k.endswith(".json") and "petition" in k)
def strip(key): return lambda p: json.dumps({k: v for k, v in json.loads(read(p)).items() if k != key}).encode() if p == pet else read(p)
expect("R5", r5(SRC, strip("fetched")))                                                        # summary with no date
expect("R5", r5(SRC, strip("source")))                                                         # summary with no source
expect("R6", r6({page: '<script src="missing-runtime.js"></script>'}, tracked))                # a page loads a missing file
expect("R7", r7({".github/workflows/x.yml": "run: gh pr merge 5 --squash"}))                 # a workflow that merges
expect("R7", r7({".github/workflows/x.yml": "permissions:\n  contents: write"}))              # one that may write
ent = (read("index.html") or b"").decode()
expect("R8", r8(lambda p: ent.replace("url=site/index.html", "url=app/Amplify%20Portal.dc.html").encode() if p == "index.html" else read(p)))   # redirect to the design (D22)
expect("R8", r8(lambda p: ent.replace("<title>Amplify: youth voice, carried further (independent, unofficial)</title>", "<title>UK Youth Parliament: Amplify portal</title>").encode() if p == "index.html" else read(p)))  # a UKYP title
_ck = (read(".github/workflows/checks.yml") or b"").decode()
expect("R9", r9(lambda p: _ck.replace("npx eslint .", "echo").encode() if p == ".github/workflows/checks.yml" else read(p)))   # a checks workflow without the lint step (D24)
sys.exit(1 if fails else 0)
