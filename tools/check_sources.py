"""Checks for the portal's content data (data/*.json) and the staleness of what it tells young people.
Run: python3 -I tools/check_sources.py [--today YYYY-MM-DD] [--online] [--report FILE]

Same shape as check_repo.py and check_site.py: every rule names the defect it exists for, and every rule is proved
by a negative test (a deliberately broken copy it must catch). --online adds C8, which fetches every link; the
weekly health workflow runs it on GitHub's runners, where the network is open.

  C1  every source is well formed: unique id, a known theme, nations and audiences, a V/S/K provenance, an https
      link, a checked date and a review cadence (a card with no date cannot say how sure it is)
  C2  every update is dated, categorised, sourced with an https link and has a provenance
  C3  nothing is past its review date: each data set and each source is checked within its cadence; past 1.5 times
      the cadence it fails (defect D3: a closed helpline stayed listed because nothing asked for a re-check)
  C4  no retired service is offered anywhere in site/ or the data, except where an update explains it closed
      (defects D3 and D4: HOPELINE247 and The Mix's old phone line)
  C5  helplines are re-checked at least every 30 days, and every helpline names how to contact it
  C6  every framework has a known status; every K (background knowledge) entry is covered by an open-register item
  C7  every nation of the UK has at least one nation-specific source, so coverage is pan-UK, not England by default
  C9  every screen in the drawer has a content-integrity class, Sample, Model and Generated screens say why, and the
      known sample content (the seed pledges, the sample profile) is classified as Sample (owner's rule, 15 Nov 2026:
      flag dummy and synthetic content explicitly)
  C8  (online only) every link answers: 2xx or 3xx, or a 401/403/405/429 from a host that refuses robots, which is
      reported, not failed
"""
import argparse, copy, datetime, glob, json, os, re, sys, urllib.request

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(R, "data")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
RETIRED = ["HOPELINE247", "HopeLine247", "0800 068 4141", "0808 808 4994"]
RETIRED_OK = {"data/latest.json", "data/registers.json", "data/changelog.json", "site/data/changelog.json", "site/data/latest.json", "site/data/registers.json", "site/build.json"}  # where the closures are explained
STATUSES = {"Met", "Met by design", "Met for a signposting tool", "Partly met", "Guidance added", "Signposting", "Aligned",
            "Out of scope by design", "Not triggered", "Open"}
NATIONS = {"UK", "England", "Scotland", "Wales", "Northern Ireland"}


def load():
    return {os.path.basename(p): json.load(open(p, encoding="utf-8")) for p in glob.glob(os.path.join(D, "*.json"))}


def days(a, b):
    return (b - datetime.date.fromisoformat(a)).days


def c1(d):
    y = d["youth-sources.json"]; bad = []; seen = set()
    for s in y["sources"]:
        i = s.get("id", "?")
        if i in seen: bad.append(f"C1 source {i} is listed twice")
        seen.add(i)
        for k in ("name", "theme", "nations", "kind", "url", "what", "use", "provenance", "checked", "review_days", "audiences"):
            if k not in s: bad.append(f"C1 source {i} has no {k}")
        if s.get("theme") not in y["themes"]: bad.append(f"C1 source {i} has an unknown theme {s.get('theme')}")
        if not set(s.get("nations", [])) <= NATIONS or not s.get("nations"): bad.append(f"C1 source {i} has unknown nations")
        if not set(s.get("audiences", [])) <= set(y["audiences"]) or not s.get("audiences"): bad.append(f"C1 source {i} has unknown audiences")
        if s.get("provenance") not in ("V", "S", "K"): bad.append(f"C1 source {i} has no V/S/K provenance")
        if not str(s.get("url", "")).startswith("https://"): bad.append(f"C1 source {i} link is not https")
    return bad


def c2(d):
    l = d["latest.json"]; bad = []
    for x in l["items"]:
        t = x.get("title", "?")
        try: datetime.date.fromisoformat(x.get("date", ""))
        except ValueError: bad.append(f"C2 update '{t}' has no ISO date")
        if x.get("cat") not in l["categories"]: bad.append(f"C2 update '{t}' has an unknown category")
        if not str(x.get("url", "")).startswith("https://") or not x.get("source"): bad.append(f"C2 update '{t}' is not sourced")
        if x.get("provenance") not in ("V", "S", "K"): bad.append(f"C2 update '{t}' has no provenance")
    return bad


def c3(d, today):
    bad = []
    for f, x in d.items():
        if "checked" in x:
            age, cad = days(x["checked"], today), x.get("review_days", 30)
            if age > cad * 1.5: bad.append(f"C3 data/{f} was last checked {age} days ago; its cadence is {cad}")
    for s in d["youth-sources.json"]["sources"]:
        age, cad = days(s["checked"], today), s.get("review_days", 90)
        if age > cad * 1.5: bad.append(f"C3 source {s['id']} was last checked {age} days ago; its cadence is {cad}")
    return bad


def c4(texts):
    bad = []
    for f, s in texts.items():
        if f in RETIRED_OK: continue
        for r in RETIRED:
            if r in s: bad.append(f"C4 {f} still offers a retired service: {r}")
    return bad


def c5(d):
    bad = []
    for s in d["youth-sources.json"]["sources"]:
        if s.get("kind") == "Helpline" or s.get("contact"):
            if s.get("review_days", 999) > 30: bad.append(f"C5 helpline {s['id']} is reviewed less often than every 30 days")
            if not s.get("contact"): bad.append(f"C5 helpline {s['id']} does not say how to contact it")
    return bad


def c6(d):
    sg, reg = d["safeguards.json"], d["registers.json"]; bad = []
    for f in sg["frameworks"]:
        if f.get("status") not in STATUSES: bad.append(f"C6 framework {f.get('id')} has an unknown status {f.get('status')}")
    ks = [f["id"] for f in sg["frameworks"] if f.get("provenance") == "K"]
    if ks and not any("K" in o["what"] and "framework" in o["what"].lower() for o in reg["open"]):
        bad.append("C6 K-labelled frameworks exist but no open-register item says they need checking")
    return bad


def c7(d):
    have = {n for s in d["youth-sources.json"]["sources"] for n in s["nations"]}
    return [f"C7 no source is specific to {n}" for n in ("England", "Scotland", "Wales", "Northern Ireland") if n not in have]


def c9(d, page):
    ig = d["integrity.json"]; got = {x["screen"]: x for x in ig["screens"]}; bad = []
    ids = re.findall(r'\["([a-z0-9]+)", "[^"]+", "(?:dot|ring|sq|dia|bar|tri)", \d+', page)
    for i in ids:
        if i not in got: bad.append(f"C9 screen {i} has no content-integrity class")
    for x in ig["screens"]:
        if x["class"] not in ig["classes"]: bad.append(f"C9 screen {x['screen']} has an unknown class {x['class']}")
        if x["class"] in ("Sample", "Model", "Generated") and len(x.get("why", "")) < 40: bad.append(f"C9 screen {x['screen']} is {x['class']} but does not say why")
    for marker, scr in (("Amara O.", "pledge"), ("Sample profile", "prof")):
        if marker in page and got.get(scr, {}).get("class") != "Sample": bad.append(f"C9 '{marker}' appears on {scr} but the screen is not classified Sample")
    return bad


def c8(d, report):
    urls = sorted({s["url"] for s in d["youth-sources.json"]["sources"]} | {x["url"] for x in d["latest.json"]["items"]} |
                  {f["url"] for f in d["safeguards.json"]["frameworks"]})
    bad, rows = [], []
    for u in urls:
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (amplify-portal link check)"})
            code = urllib.request.urlopen(req, timeout=25).status
        except urllib.error.HTTPError as e: code = e.code
        except Exception as e: code = f"error: {type(e).__name__}"
        ok = isinstance(code, int) and code < 400
        soft = isinstance(code, int) and code in (401, 403, 405, 429)
        rows.append({"url": u, "status": code, "ok": ok, "soft": soft})
        if not ok and not soft: bad.append(f"C8 {u} answered {code}")
    if report:
        json.dump({"checked": datetime.date.today().isoformat(), "links": rows}, open(report, "w"), indent=1)
    return bad


def texts_all():
    t = {}
    for base in ("data", "site"):
        for p in glob.glob(os.path.join(R, base, "**", "*"), recursive=True):
            if os.path.isfile(p) and p.endswith((".json", ".html", ".js")) and "/vendor/" not in p:
                t[os.path.relpath(p, R).replace(os.sep, "/")] = open(p, encoding="utf-8", errors="replace").read()
    return t


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--today", default=datetime.date.today().isoformat())
    ap.add_argument("--online", action="store_true"); ap.add_argument("--report")
    a = ap.parse_args(); today = datetime.date.fromisoformat(a.today)
    d = load(); t = texts_all()
    page = t.get("site/index.html", "")
    bad = c1(d) + c2(d) + c3(d, today) + c4(t) + c5(d) + c6(d) + c7(d) + c9(d, page)
    bad += [f"C1 data/{f} carries an email address" for f, s in t.items() if f.startswith("data/") and EMAIL.search(s)]
    if a.online: bad += c8(d, a.report)
    n = len(d["youth-sources.json"]["sources"])
    print(f"amplify content: {n} sources, {len(d['latest.json']['items'])} updates, as of {today}, C1-C9 problems: {len(bad)}")
    if bad:
        print("\n".join(bad[:60])); sys.exit(1)

    fails = 0
    def expect(rule, got):
        global fails
        hit = any(b.startswith(rule) for b in got); fails += not hit
        print(("caught     " if hit else "NOT CAUGHT ") + rule)
    x = copy.deepcopy(d); x["youth-sources.json"]["sources"][0]["provenance"] = "maybe"; expect("C1", c1(x))
    x = copy.deepcopy(d); x["youth-sources.json"]["sources"].append(copy.deepcopy(x["youth-sources.json"]["sources"][0])); expect("C1", c1(x))
    x = copy.deepcopy(d); x["latest.json"]["items"][0]["url"] = "http://example.org"; expect("C2", c2(x))
    x = copy.deepcopy(d); x["latest.json"]["items"][0]["date"] = "last week"; expect("C2", c2(x))
    expect("C3", c3(d, today + datetime.timedelta(days=400)))                                         # a year with no re-check
    expect("C4", c4({"site/index.html": "Papyrus HOPELINE247 0800 068 4141"}))                         # the closed helpline back
    x = copy.deepcopy(d); h = next(s for s in x["youth-sources.json"]["sources"] if s.get("contact")); h["review_days"] = 365; expect("C5", c5(x))
    x = copy.deepcopy(d); x["safeguards.json"]["frameworks"][0]["status"] = "Fine"; expect("C6", c6(x))
    x = copy.deepcopy(d); x["registers.json"]["open"] = []; expect("C6", c6(x))
    x = copy.deepcopy(d); x["youth-sources.json"]["sources"] = [s for s in x["youth-sources.json"]["sources"] if "Wales" not in s["nations"]]; expect("C7", c7(x))
    x = copy.deepcopy(d); x["integrity.json"]["screens"] = [y for y in x["integrity.json"]["screens"] if y["screen"] != "pledge"]; expect("C9", c9(x, page))
    x = copy.deepcopy(d); next(y for y in x["integrity.json"]["screens"] if y["screen"] == "prof")["class"] = "Sourced"; expect("C9", c9(x, page))
    sys.exit(1 if fails else 0)
