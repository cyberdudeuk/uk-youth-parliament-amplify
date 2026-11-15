"""Ninth set of portal extensions: knowledge, transparency, alerts and news.

  glossary  data/glossary.json is the one master for new vocabulary. At build time every term is written into the
            design's knowledge graph (GRAPH) and glossary list (GLOSSARY), so the Glossary & graph screen, the command
            palette and the term tooltips all read the same words. check_site S16 fails a release that adds a tooltip
            term, an edge or a version without its glossary entry.
  product   Vision, mission, strategy, product specification, update schedule, roadmap (now, next, later) and the
            requirements backlog, each requirement traced to the screens that deliver it and the checks that prove it,
            plus how all of it is tracked on GitHub. From data/product.json; docs/product.md is generated from it and
            check_site S17 keeps every trace pointing at a real screen and check.
  notify    Alerts and notifications: which alerts appear (launch countdown, updated since your last visit, safety
            notices, dates coming up, upkeep), per-device preferences kept only in this browser, and ways to follow
            updates outside the portal (an Atom feed and GitHub watching) with nothing collected.
  strip     On every screen, under the explainer: the alerts that apply, each dismissible, then a news ticker chosen for
            the screen you are on. The ticker pauses on hover, on focus and with its own button, and stands still
            under reduced motion. Every item is a link.
"""
import json, os

from extend import PANEL, LABEL, SMALL
from extend4 import H2, CARD

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "https://github.com/cyberdudeuk/uk-youth-parliament-amplify"
GLOSS_DOC = REPO + "/blob/main/docs/glossary.md"


def _data(name):
    with open(os.path.join(R, "data", name), encoding="utf-8") as f:
        return json.load(f)


def _gl():
    return _data("glossary.json")


def graph_entries():
    """JS object entries for the design's GRAPH, one per glossary term that belongs in the graph."""
    out = []
    for t in _gl()["terms"]:
        if t.get("graph") is False: continue
        url, lab = (t["url"], t["urlLabel"]) if t["url"] else (GLOSS_DOC, "Amplify glossary")
        out.append(f'    {t["id"]}: {{ name: {json.dumps(t["term"])}, shape: {json.dumps(t["shape"])}, hue: {int(t["hue"])}, url: {json.dumps(url)}, '
                   f'urlLabel: {json.dumps(lab)}, def: {json.dumps(t["def"])}, also: {json.dumps(t["also"])}, edges: {json.dumps(t["edges"])} }},')
    return "\n".join(out)


def glossary_rows():
    """JS rows for the design's GLOSSARY list: [term, definition, hue, url]."""
    return "\n".join(f'        [{json.dumps(t["term"])}, {json.dumps(t["def"])}, {int(t["hue"])}, {json.dumps(t["url"] or GLOSS_DOC)}],'
                     for t in _gl()["terms"] if t.get("list") is not False)


def skos(meta):
    """The glossary as a SKOS concept scheme in JSON-LD, so other systems can reuse the vocabulary."""
    gl, base = _gl(), REPO + "/blob/main/docs/glossary.md#"
    concepts = [{"@id": base + t["id"], "@type": "skos:Concept", "skos:prefLabel": {"@value": t["term"], "@language": "en-GB"},
                 "skos:altLabel": [{"@value": a.strip(), "@language": "en-GB"} for a in t["also"].split(";") if a.strip()],
                 "skos:definition": {"@value": t["def"], "@language": "en-GB"}, "skos:inScheme": {"@id": base},
                 "skos:related": [{"@id": base + e} for e in t["edges"]], "dcterms:created": t["added"]} for t in gl["terms"]]
    doc = {"@context": {"skos": "http://www.w3.org/2004/02/skos/core#", "dcterms": "http://purl.org/dc/terms/"},
           "@graph": [{"@id": base, "@type": "skos:ConceptScheme", "dcterms:title": "Amplify glossary and thesaurus",
                       "dcterms:modified": gl["checked"], "dcterms:identifier": meta["build_id"]}] + concepts}
    return json.dumps(doc, indent=1, ensure_ascii=False) + "\n"


def feed(meta):
    """An Atom feed of What's new and the release log, for feed readers: following updates without giving anything."""
    from xml.sax.saxutils import escape as e
    lat, ch = _data("latest.json"), _data("changelog.json")
    rows = [(i["date"], i["title"], i["body"] + " Source: " + i["source"] + ".", i["url"], "news-" + i["date"] + "-" + i["cat"]) for i in lat["items"]]
    rows += [(r["date"], "Amplify " + r["version"] + ": " + r["title"], r["summary"], REPO + "/blob/main/CHANGELOG.md", "release-" + r["version"]) for r in ch["releases"]]
    rows.sort(key=lambda x: x[0], reverse=True)
    out = ['<?xml version="1.0" encoding="utf-8"?>', '<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en-GB">',
           '  <title>Amplify: what\'s new</title>', f'  <id>{REPO}#feed</id>', f'  <updated>{meta["built"]}T00:00:00Z</updated>',
           f'  <link rel="alternate" href="{REPO}"/>', '  <author><name>Amplify (independent, unofficial)</name></author>',
           '  <subtitle>Youth voice news and Amplify releases. Generated from data/latest.json and data/changelog.json.</subtitle>']
    for d, t, body, url, key in rows:
        out += ["  <entry>", f"    <title>{e(t)}</title>", f'    <link href="{e(url)}"/>', f"    <id>{REPO}#{e(key)}</id>",
                f"    <updated>{d}T00:00:00Z</updated>", f"    <summary>{e(body)}</summary>", "  </entry>"]
    return "\n".join(out + ["</feed>"]) + "\n"


LOGIC9 = r'''
  ampNote() {
    if (this._note) return this._note;
    let n = {};
    try { n = JSON.parse(window.localStorage.getItem("amp-notify") || "{}") || {}; } catch (e) { n = {}; }
    this._note = { off: n.off || [], dismissed: n.dismissed || [], seen: n.seen || "", paused: !!n.paused, first: !n.seen };
    return this._note;
  }
  ampNoteSave(patch) {
    const n = Object.assign(this.ampNote(), patch); this._note = n;
    try { window.localStorage.setItem("amp-notify", JSON.stringify({ off: n.off, dismissed: n.dismissed, seen: n.seen, paused: n.paused })); }
    catch (e) { /* storage unavailable: keep it in memory for this visit */ }
    this.setState({ noteTick: (this.state.noteTick || 0) + 1 });
  }
  async ampShareNow() {
    const here = (location.href || "").split("#")[0] + "#" + (this.state.screen || "home");
    const title = "Amplify: " + (this.ampScreenName(this.state.screen) || "youth voice, carried further");
    try {
      if (navigator.share) { await navigator.share({ title, text: "Youth voice, carried further.", url: here }); this.setState({ shareMsg: "Shared." }); return; }
    } catch (e) { if (e && e.name === "AbortError") return; /* blocked here: offer the menu instead */ }
    this.setState({ shareOpen: !this.state.shareOpen, shareMsg: "" });
  }
  ampScreenName(id) { let n = ""; this.GROUPS.forEach(([g, items]) => items.forEach(([k, lbl]) => { if (k === id) n = lbl; })); return n; }
  ampAlerts(s) {
    const A = s.amp || {}, ch = A.ch || { releases: [] }, lat = (A.lat || {}).items || [], src = (A.src || {}).sources || [];
    const n = this.ampNote(), out = [], go = (screen) => () => this.setState({ screen });
    const launch = ch.releases.find((r) => r.status === "Planned launch");
    if (launch) { const d = -this.ampDays(launch.date);
      if (d >= 0) out.push({ id: "launch-" + launch.version, pref: "launch", level: "info", text: d === 0 ? "Amplify launches today, at UK Parliament Week." : "Amplify launches in " + d + (d === 1 ? " day" : " days") + ", on " + this.ampDate(launch.date) + ", at UK Parliament Week.", act: "Launch plans", go: go("launch") }); }
    if (ch.current && n.seen && n.seen !== ch.current) out.push({ id: "release-" + ch.current, pref: "release", level: "info", text: "Updated since your last visit: release " + ch.current + ". The drawer flags what is new (NEW) and changed (UPD).", act: "See what changed", go: () => { this.ampNoteSave({ seen: ch.current }); this.setState({ screen: "changes" }); } });
    lat.filter((i) => i.cat === "safety" && i.status && this.ampDays(i.date) >= 0 && this.ampDays(i.date) <= 120).forEach((i) =>
      out.push({ id: "safety-" + i.date, pref: "safety", level: "safety", text: "Safety notice: " + i.title + " (" + i.status.toLowerCase() + ").", act: "Read it", go: go("latest") }));
    lat.filter((i) => { const d = -this.ampDays(i.date); return d > 0 && d <= 21 && !(launch && i.date === launch.date); }).forEach((i) =>
      out.push({ id: "date-" + i.date + "-" + i.cat, pref: "dates", level: "info", text: "Coming up on " + this.ampDate(i.date) + ": " + i.title + ".", act: "What's new", go: go("latest") }));
    if (["sources", "health", "golive", "product", "notify"].indexOf(s.screen) >= 0) {
      const due = src.filter((x) => this.ampFresh(x.checked, x.review_days || 90).label === "Overdue").length;
      if (due) out.push({ id: "upkeep-" + due, pref: "upkeep", level: "warn", text: due + (due === 1 ? " source is" : " sources are") + " past the re-check date. The weekly upkeep re-verifies them, oldest first.", act: "Portal health", go: go("health") });
    }
    return out;
  }
  // The news ticker's sense of "relevant here". Returns a score for one news item on one screen, or -1 to leave it
  // out. The ticker shows the highest scores first, up to eight items.
  ampTickerScore(item, screen, cats) {
    const want = cats[screen] || cats["*"] || [], age = this.ampDays(item.date);
    if (age === null) return -1;
    let score = want.indexOf(item.cat) >= 0 ? 100 : (want.length ? 10 : 50);
    if (age < 0) score += 30;                               // coming up beats past
    score += Math.max(0, 40 - Math.floor(Math.abs(age) / 7)); // fresher is better, a point a week for 40 weeks
    if (item.cat === "safety" && item.status && age <= 120) score += 60; // a live safety notice leads everywhere
    return score;
  }
  ampVals9(s) {
    const A = s.amp || {}, pd = A.pd || { strategy: [], spec: { in: [], out: [], constraints: [] }, schedule: [], roadmap: [], backlog: [], github: [] };
    const gl = (A.gl || { terms: [] }).terms, ch = A.ch || {}, latD = A.lat || { items: [], categories: {} }, n = this.ampNote();
    const W = {}; ((A.bld || {}).checks || []).forEach((c) => { W[c.id] = c.what; });
    const L = {}; this.GROUPS.forEach(([g, items]) => items.forEach(([id, lbl]) => { L[id] = lbl; }));
    const pill = (h) => "display:inline-block;border-radius:999px;padding:2px 9px;font-family:'Space Mono',monospace;font-size:11px;font-weight:700;background:oklch(var(--t1) 0.16 " + h + " / 0.28);color:oklch(var(--t4) 0.15 " + h + ");";
    const MH = { Must: 25, Should: 70, Could: 175, "Won't": 300 }, SH = { Done: 145, "In progress": 70, Planned: 215, "Waiting on owner": 25 };
    if (n.first && ch.current && !this._noteInit) { this._noteInit = true; Promise.resolve().then(() => this.ampNoteSave({ seen: ch.current, first: false })); }
    if (s.screen === "changes" && ch.current && n.seen && n.seen !== ch.current) Promise.resolve().then(() => this.ampNoteSave({ seen: ch.current }));
    const fm = s.pdFm || "All", fs = s.pdFs || "All";
    const rows = pd.backlog.filter((b) => (fm === "All" || b.moscow === fm) && (fs === "All" || b.status === fs));
    const alerts = this.ampAlerts(s), shown = alerts.filter((a) => (a.pref === "safety" || n.off.indexOf(a.pref) < 0) && n.dismissed.indexOf(a.id) < 0);
    const lv = { info: [215, "Notice"], warn: [70, "Check"], safety: [25, "Safety"] };
    const tk = (latD.ticker || {}), cats = tk.screens || {}, items = (latD.items || []).map((i) => ({ i, sc: this.ampTickerScore(i, s.screen, cats) }))
      .filter((x) => x.sc >= 0).sort((a, b) => b.sc - a.sc).slice(0, 8).map((x) => x.i);
    const tkItems = items.map((i, k) => ({ key: "tk" + k, url: i.url, cat: (latD.categories || {})[i.cat] || i.cat, date: this.ampDate(i.date), title: i.title, source: i.source,
      label: i.title + ". " + ((latD.categories || {})[i.cat] || i.cat) + ", " + this.ampDate(i.date) + ", from " + i.source + ". Opens in a new tab." }));
    const prefs = [["launch", "Launch countdown", "Days to the launch at UK Parliament Week."], ["release", "Updated since your last visit", "When a new release lands, with a link to what changed."],
      ["dates", "Dates coming up", "Things happening in the next three weeks, from What's new."], ["upkeep", "Upkeep notices", "On the source and health screens: sources past their re-check date."],
      ["ticker", "News ticker", "The strip of news for the screen you are on."]];
    return {
      sProduct: s.screen === "product", sNotify: s.screen === "notify",
      icProduct: this.ampIcon("milestone", "oklch(var(--t3) 0.16 70)", 16), icNotify: this.ampIcon("bell", "oklch(var(--t3) 0.16 215)", 16),
      icBell: this.ampIcon("bell-ring", "currentColor", 15), icRss: this.ampIcon("rss", "currentColor", 15), icNews: this.ampIcon("newspaper", "oklch(var(--t3) 0.16 70)", 15),
      pdVision: pd.vision || "", pdMission: pd.mission || "", pdChecked: pd.checked ? this.ampDate(pd.checked) : "",
      pdStrategy: pd.strategy.map((p) => ({ pillar: p.pillar, what: p.what })),
      pdWhat: (pd.spec || {}).what || "", pdWho: (pd.spec || {}).who || "",
      pdIn: ((pd.spec || {}).in || []).map((t) => ({ t })), pdOut: ((pd.spec || {}).out || []).map((t) => ({ t })), pdCons: ((pd.spec || {}).constraints || []).map((t) => ({ t })),
      pdSchedule: pd.schedule.map((r) => ({ what: r.what, when: r.when, how: r.how })),
      pdLanes: pd.roadmap.map((l) => ({ lane: l.lane, items: l.items.map((it) => ({ t: it.t, reqs: it.reqs.map((r) => ({ r, go: () => this.setState({ pdFm: "All", pdFs: "All", pdAt: r }) })) })) })),
      pdFm: fm, pdFs: fs, pdShown: String(rows.length), pdTotal: String(pd.backlog.length),
      setPdFm: (e) => this.setState({ pdFm: e.target.value }), setPdFs: (e) => this.setState({ pdFs: e.target.value }),
      pdCounts: ["Done", "In progress", "Planned", "Waiting on owner"].map((k) => ({ k, n: String(pd.backlog.filter((b) => b.status === k).length), style: pill(SH[k]) })),
      pdRows: rows.map((b) => ({ id: b.id, title: b.title, from: b.from, moscow: b.moscow, status: b.status, mStyle: pill(MH[b.moscow] || 175), sStyle: pill(SH[b.status] || 175),
        at: s.pdAt === b.id ? "outline: 2px solid oklch(var(--t2) 0.18 70); outline-offset: 2px;" : "",
        screens: b.screens.map((id) => ({ label: L[id] || id, go: () => this.setState({ screen: id }) })), checks: b.checks.map((c) => ({ c, what: W[c] || c })) })),
      pdGit: pd.github.map((g, k) => ({ n: String(k + 1), step: g.step, what: g.what, where: g.where })),
      pdRepo: REPO_URL, pdIssues: REPO_URL + "/issues", pdPulls: REPO_URL + "/pulls", pdActions: REPO_URL + "/actions", pdDoc: REPO_URL + "/blob/main/docs/product.md",
      pdFollow: REPO_URL + "/issues?q=is%3Aissue+is%3Aopen+label%3Afollow-up", pdGlossDoc: REPO_URL + "/blob/main/docs/glossary.md",
      pdRelease: ch.current || "", pdWords: gl.filter((t) => t.added === ch.current).map((t) => ({ term: t.term, def: t.def, also: t.also, go: () => this.setState({ screen: "graph", node: t.graph === false ? s.node : t.id }) })),
      pdWordsN: String(gl.filter((t) => t.added === ch.current).length), glTotal: String(gl.length),
      alShow: shown.length > 0 && !s.splash, alerts: shown.map((a) => ({ id: a.id, text: a.text, act: a.act, go: a.go, tag: lv[a.level][1],
        box: "display:flex;flex-wrap:wrap;align-items:center;gap:6px 12px;border-radius:14px;padding:8px 12px;font-size:13.5px;line-height:1.45;border:1px solid oklch(var(--t2) 0.16 " + lv[a.level][0] + " / 0.6);background:oklch(var(--t1) 0.16 " + lv[a.level][0] + " / 0.12);",
        tagStyle: pill(lv[a.level][0]), dismiss: () => this.ampNoteSave({ dismissed: n.dismissed.concat([a.id]) }), dLabel: "Dismiss: " + a.text })),
      ntAll: alerts.map((a) => ({ text: a.text, tag: lv[a.level][1], tagStyle: pill(lv[a.level][0]), hidden: n.dismissed.indexOf(a.id) >= 0 || (a.pref !== "safety" && n.off.indexOf(a.pref) >= 0),
        restore: () => this.ampNoteSave({ dismissed: n.dismissed.filter((x) => x !== a.id), off: n.off.filter((x) => x !== a.pref) }) })),
      ntNone: alerts.length === 0, ntDismissedN: String(n.dismissed.length),
      ntPrefs: prefs.map(([k, lbl, why]) => ({ k, lbl, why, on: n.off.indexOf(k) < 0, toggle: (e) => this.ampNoteSave({ off: e.target.checked ? n.off.filter((x) => x !== k) : n.off.concat([k]) }) })),
      ntReset: () => this.ampNoteSave({ off: [], dismissed: [], paused: false }),
      ntFeed: REPO_URL.replace("https://github.com/", "https://raw.githubusercontent.com/") + "/main/site/feed.xml", ntWatch: REPO_URL + "/subscription", ntReleases: REPO_URL + "/releases.atom",
      shBtn: () => this.ampShareNow(), shOpen: !!s.shareOpen, shExpanded: s.shareOpen ? "true" : "false", shMsg: s.shareMsg || "",
      shClose: () => this.setState({ shareOpen: false }),
      shLinks: this.ampShare("Amplify: " + (this.ampScreenName(s.screen) || "youth voice"), (location.href || "").split("#")[0] + "#" + (s.screen || "home")),
      shCopy: () => { this.copy((location.href || "").split("#")[0] + "#" + (s.screen || "home"), "shlink"); this.setState({ shareMsg: "Link copied. Until the owner shares the portal publicly, others may not be able to open it." }); },
      shCopyLabel: s.copied === "shlink" ? "Link copied" : "Copy link to this screen", shIcon: this.ampIcon("external-link", "currentColor", 14),
      tkShow: tkItems.length > 0 && n.off.indexOf("ticker") < 0 && !s.splash && s.screen !== "latest", tkItems,
      tkPaused: n.paused ? "true" : "false", tkBtn: n.paused ? "Play the news" : "Pause the news", tkIcon: this.ampIcon(n.paused ? "play" : "pause", "currentColor", 14),
      tkToggle: () => this.ampNoteSave({ paused: !n.paused }), tkAll: () => this.setState({ screen: "latest" }),
      tkDur: "animation-duration: " + Math.max(24, tkItems.length * 7) + "s;"
    };
  }
'''.replace("REPO_URL", '"' + REPO + '"')

STRIP = '''
        <div class="amp-share" style="position: relative; display: flex; justify-content: flex-end; flex-wrap: wrap; align-items: center; gap: 6px 10px; margin-bottom: -6px;">
          <span aria-live="polite" style="font-size: 12.5px; color: rgb(var(--ink-rgb) / 0.82);">{{ shMsg }}</span>
          <button onClick="{{ shBtn }}" aria-expanded="{{ shExpanded }}" aria-controls="amp-share-menu" data-tip="ui:share" style="display: inline-flex; align-items: center; gap: 6px; min-height: 34px; border: 1px solid rgb(var(--film-rgb) / 0.25); border-radius: 999px; background: rgb(var(--film-rgb) / 0.05); color: rgb(var(--ink-rgb)); padding: 5px 13px; font-size: 12.5px; font-weight: 800; cursor: pointer;"><span aria-hidden="true" style="{{ shIcon }}"></span>Share</button>
          <sc-if value="{{ shOpen }}" hint-placeholder-val="{{ false }}">
          <div id="amp-share-menu" role="group" aria-label="Share this screen" style="position: absolute; top: calc(100% + 6px); right: 0; z-index: 30; width: min(300px, calc(100vw - 32px)); display: flex; flex-direction: column; gap: 6px; border-radius: 14px; border: 1px solid rgb(var(--film-rgb) / 0.22); background: var(--bg2); box-shadow: 0 12px 30px rgb(0 0 0 / 0.35); padding: 10px;">
            <button onClick="{{ shCopy }}" style="min-height: 34px; border: 1px solid rgb(var(--film-rgb) / 0.25); border-radius: 10px; background: transparent; color: rgb(var(--ink-rgb)); font-size: 13px; font-weight: 800; cursor: pointer;">{{ shCopyLabel }}</button>
            <sc-for list="{{ shLinks }}" as="l" hint-placeholder-count="3"><a href="{{ l.href }}" target="_blank" rel="noopener" style="display: block; min-height: 30px; padding: 6px 8px; color: rgb(var(--ink-rgb)); font-size: 13px; font-weight: 700; text-underline-offset: 3px;">Share to {{ l.label }}</a></sc-for>
            <p style="margin: 0; font-size: 12px; line-height: 1.45; color: rgb(var(--ink-rgb) / 0.8);">Sharing opens that service in a new tab. Amplify does not see or keep what you share.</p>
            <button onClick="{{ shClose }}" style="align-self: flex-end; min-height: 30px; border: none; background: transparent; color: rgb(var(--ink-rgb)); font-size: 12.5px; text-decoration: underline; cursor: pointer;">Close</button>
          </div>
          </sc-if>
        </div>
        <sc-if value="{{ alShow }}" hint-placeholder-val="{{ false }}">
        <section aria-label="Alerts for you" style="display: flex; flex-direction: column; gap: 6px;">
          <sc-for list="{{ alerts }}" as="a" hint-placeholder-count="1"><div style="{{ a.box }}"><span aria-hidden="true" style="{{ icBell }}"></span><span style="{{ a.tagStyle }}">{{ a.tag }}</span><span style="flex: 1 1 240px; min-width: 0;">{{ a.text }}</span><button onClick="{{ a.go }}" style="min-height: 32px; border: 1px solid rgb(var(--film-rgb) / 0.25); border-radius: 999px; background: transparent; color: rgb(var(--ink-rgb)); padding: 4px 12px; font-size: 12.5px; font-weight: 800; cursor: pointer;">{{ a.act }}</button><button onClick="{{ a.dismiss }}" aria-label="{{ a.dLabel }}" style="min-width: 32px; min-height: 32px; border: none; border-radius: 999px; background: transparent; color: rgb(var(--ink-rgb) / 0.8); font-size: 18px; line-height: 1; cursor: pointer;">&times;</button></div></sc-for>
        </section>
        </sc-if>
        <sc-if value="{{ tkShow }}" hint-placeholder-val="{{ false }}">
        <section class="amp-tk" data-paused="{{ tkPaused }}" aria-label="News for this screen" style="display: flex; align-items: center; gap: 8px; min-width: 0; border-radius: 14px; border: 1px solid rgb(var(--film-rgb) / 0.16); background: rgb(var(--film-rgb) / 0.05); padding: 4px 6px 4px 10px;">
          <span aria-hidden="true" style="{{ icNews }}"></span>
          <span style="font-family: 'Space Mono', monospace; font-size: 10.5px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: oklch(var(--t3) 0.16 70); flex: 0 0 auto;">News</span>
          <div class="amp-tk-view" style="flex: 1 1 0; min-width: 0; overflow: hidden;">
            <div class="amp-tk-track" style="{{ tkDur }}">
              <ul class="amp-tk-list" role="list" style="display: flex; gap: 28px; margin: 0; padding: 0 28px 0 0; list-style: none;"><sc-for list="{{ tkItems }}" as="t" hint-placeholder-count="3"><li style="flex: 0 0 auto;"><a href="{{ t.url }}" target="_blank" rel="noopener" aria-label="{{ t.label }}" style="display: inline-flex; align-items: baseline; gap: 8px; min-height: 30px; padding: 4px 0; color: rgb(var(--ink-rgb)); text-decoration: none; font-size: 13.5px; white-space: nowrap;"><span style="font-family: 'Space Mono', monospace; font-size: 11px; color: rgb(var(--ink-rgb) / 0.75);">{{ t.date }} &middot; {{ t.cat }}</span><span style="font-weight: 700; text-decoration: underline; text-underline-offset: 3px;">{{ t.title }}</span></a></li></sc-for></ul>
              <ul class="amp-tk-list amp-tk-dup" aria-hidden="true" style="display: flex; gap: 28px; margin: 0; padding: 0 28px 0 0; list-style: none;"><sc-for list="{{ tkItems }}" as="t" hint-placeholder-count="3"><li style="flex: 0 0 auto;"><a href="{{ t.url }}" tabindex="-1" target="_blank" rel="noopener" style="display: inline-flex; align-items: baseline; gap: 8px; min-height: 30px; padding: 4px 0; color: rgb(var(--ink-rgb)); text-decoration: none; font-size: 13.5px; white-space: nowrap;"><span style="font-family: 'Space Mono', monospace; font-size: 11px; color: rgb(var(--ink-rgb) / 0.75);">{{ t.date }} &middot; {{ t.cat }}</span><span style="font-weight: 700; text-decoration: underline; text-underline-offset: 3px;">{{ t.title }}</span></a></li></sc-for></ul>
            </div>
          </div>
          <button onClick="{{ tkToggle }}" aria-pressed="{{ tkPaused }}" class="amp-tk-btn" style="flex: 0 0 auto; display: inline-flex; align-items: center; gap: 6px; min-height: 32px; border: 1px solid rgb(var(--film-rgb) / 0.25); border-radius: 999px; background: transparent; color: rgb(var(--ink-rgb)); padding: 4px 11px; font-size: 12px; font-weight: 800; cursor: pointer;"><span aria-hidden="true" style="{{ tkIcon }}"></span><span class="amp-tk-btn-label">{{ tkBtn }}</span></button>
          <button onClick="{{ tkAll }}" style="flex: 0 0 auto; min-height: 32px; border: none; background: transparent; color: rgb(var(--ink-rgb)); padding: 4px 8px; font-size: 12px; font-weight: 800; text-decoration: underline; cursor: pointer;">All news</button>
        </section>
        </sc-if>
'''

CSS9 = '''
  .amp-tk-track { display: flex; width: max-content; animation-name: amp-tk; animation-timing-function: linear; animation-iteration-count: infinite; }
  .amp-tk[data-paused="true"] .amp-tk-track, .amp-tk:hover .amp-tk-track, .amp-tk:focus-within .amp-tk-track { animation-play-state: paused; }
  .amp-tk[data-paused="true"] .amp-tk-view { overflow-x: auto; }
  @keyframes amp-tk { from { transform: translateX(0); } to { transform: translateX(-50%); } }
  @media (prefers-reduced-motion: reduce) { .amp-tk-track { animation: none; } .amp-tk-dup { display: none !important; } .amp-tk-view { overflow-x: auto; } }
  @media (max-width: 560px) { .amp-tk-btn-label { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; } }
  @media print { .amp-tk { display: none !important; } }
'''

HEAD = '''<div>
            <div style="display: flex; align-items: center; gap: 9px; font-family: 'Space Mono', monospace; font-size: 10.5px; letter-spacing: 0.16em; text-transform: uppercase; color: oklch(var(--t3) 0.16 @HUE@);"><span aria-hidden="true" style="{{ @IC@ }}"></span>Sources &amp; updates</div>
            <h1 style="margin: 4px 0 6px; font-size: 27px; font-weight: 900; letter-spacing: -0.035em; text-wrap: balance;">@TITLE@</h1>
            <p style="margin: 0; font-size: 15px; line-height: 1.55; color: rgb(var(--ink-rgb) / 0.82); max-width: 68ch;">@LEDE@</p>
          </div>'''

SEL = "min-width: 0; max-width: 100%; min-height: 36px; border: 1px solid rgb(var(--film-rgb) / 0.2); border-radius: 10px; background: rgb(var(--film-rgb) / 0.05); color: rgb(var(--ink-rgb)); padding: 6px 10px; font-size: 13px;"
BTN = "min-height: 32px; border: 1px solid rgb(var(--film-rgb) / 0.25); border-radius: 999px; background: transparent; color: rgb(var(--ink-rgb)); padding: 4px 12px; font-size: 12.5px; font-weight: 800; cursor: pointer;"
A = "color: rgb(var(--ink-rgb)); font-weight: 700; text-underline-offset: 3px;"


def _opts(vals):
    return "".join(f'<option value="{v}">{"All" if v == "All" else v}</option>' for v in vals)


def screens():
    pd = _data("product.json")
    ms = ["All"] + [m for m in ("Must", "Should", "Could", "Won't") if any(b["moscow"] == m for b in pd["backlog"])]
    st = ["All"] + [x for x in ("Done", "In progress", "Planned", "Waiting on owner") if any(b["status"] == x for b in pd["backlog"])]
    product = '''
        <sc-if value="{{ sProduct }}" hint-placeholder-val="{{ false }}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          ''' + HEAD.replace("@HUE@", "70").replace("@IC@", "icProduct").replace("@TITLE@", "Product, roadmap &amp; backlog").replace("@LEDE@", "Where Amplify is going and why, what it is and is not, when it is updated, and every requirement with the screens that deliver it and the checks that prove it. Reviewed every 30 days; last checked {{ pdChecked }}.") + '''
          <section style="@PANEL@"><h2 style="@H2@">Vision</h2><p style="margin: 0 0 8px; font-size: 18px; font-weight: 800; line-height: 1.4; text-wrap: balance;">{{ pdVision }}</p><p style="margin: 0; font-size: 14px; line-height: 1.55;"><span style="font-weight: 800;">Mission:</span> {{ pdMission }}</p></section>
          <section style="@PANEL@"><h2 style="@H2@">Strategy</h2><div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 210px), 1fr)); gap: 8px;"><sc-for list="{{ pdStrategy }}" as="p" hint-placeholder-count="5"><div style="@CARD@"><div style="font-size: 14.5px; font-weight: 900;">{{ p.pillar }}</div><div style="@SMALL@">{{ p.what }}</div></div></sc-for></div></section>
          <section style="@PANEL@"><h2 style="@H2@">Product specification</h2>
            <p style="margin: 0 0 6px; font-size: 14px; line-height: 1.55;"><span style="font-weight: 800;">What it is:</span> {{ pdWhat }}</p>
            <p style="margin: 0 0 10px; font-size: 14px; line-height: 1.55;"><span style="font-weight: 800;">Who it is for:</span> {{ pdWho }}</p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 230px), 1fr)); gap: 8px;">
              <div style="@CARD@"><div style="@LABEL@">In scope</div><ul style="margin: 0; padding-left: 18px; font-size: 13.5px; line-height: 1.5;"><sc-for list="{{ pdIn }}" as="x" hint-placeholder-count="4"><li>{{ x.t }}</li></sc-for></ul></div>
              <div style="@CARD@"><div style="@LABEL@">Out of scope</div><ul style="margin: 0; padding-left: 18px; font-size: 13.5px; line-height: 1.5;"><sc-for list="{{ pdOut }}" as="x" hint-placeholder-count="4"><li>{{ x.t }}</li></sc-for></ul></div>
              <div style="@CARD@"><div style="@LABEL@">Constraints</div><ul style="margin: 0; padding-left: 18px; font-size: 13.5px; line-height: 1.5;"><sc-for list="{{ pdCons }}" as="x" hint-placeholder-count="4"><li>{{ x.t }}</li></sc-for></ul></div>
            </div></section>
          <section style="@PANEL@"><h2 style="@H2@">Update schedule</h2><div style="display: flex; flex-direction: column; gap: 6px;"><sc-for list="{{ pdSchedule }}" as="r" hint-placeholder-count="6"><div style="@CARD@ flex-direction: row; flex-wrap: wrap; align-items: baseline; gap: 4px 12px;"><span style="flex: 1 1 220px; min-width: 0; font-size: 14px; font-weight: 800;">{{ r.what }}</span><span style="flex: 1 1 180px; min-width: 0; font-size: 13.5px;">{{ r.when }}</span><span style="@LABEL@">{{ r.how }}</span></div></sc-for></div></section>
          <section style="@PANEL@"><h2 style="@H2@">Roadmap</h2><div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 240px), 1fr)); gap: 8px;"><sc-for list="{{ pdLanes }}" as="l" hint-placeholder-count="3"><div style="@CARD@"><div style="font-size: 15px; font-weight: 900;">{{ l.lane }}</div><sc-for list="{{ l.items }}" as="it" hint-placeholder-count="2"><div style="font-size: 13.5px; line-height: 1.5;">{{ it.t }} <sc-for list="{{ it.reqs }}" as="q" hint-placeholder-count="1"><button onClick="{{ q.go }}" style="border: none; background: transparent; padding: 0 3px; color: rgb(var(--ink-rgb)); font-family: 'Space Mono', monospace; font-size: 11.5px; font-weight: 700; text-decoration: underline; cursor: pointer;">{{ q.r }}</button></sc-for></div></sc-for></div></sc-for></div></section>
          <section style="@PANEL@"><h2 style="@H2@">Requirements backlog</h2>
            <p style="margin: 0 0 10px; @SMALL@">Every request, prioritised with MoSCoW, with its status, where it came from, the screens that deliver it and the checks that prove it. Showing {{ pdShown }} of {{ pdTotal }}.</p>
            <div style="display: flex; flex-wrap: wrap; gap: 8px 18px; align-items: center; margin-bottom: 10px;">
              <label style="display: flex; flex-wrap: wrap; align-items: center; gap: 6px; font-size: 12.5px;">Priority <select value="{{ pdFm }}" onChange="{{ setPdFm }}" style="@SEL@">''' + _opts(ms) + '''</select></label>
              <label style="display: flex; flex-wrap: wrap; align-items: center; gap: 6px; font-size: 12.5px;">Status <select value="{{ pdFs }}" onChange="{{ setPdFs }}" style="@SEL@">''' + _opts(st) + '''</select></label>
              <sc-for list="{{ pdCounts }}" as="c" hint-placeholder-count="4"><span style="font-size: 13px;"><span style="{{ c.style }}">{{ c.k }}</span> {{ c.n }}</span></sc-for>
            </div>
            <div style="display: flex; flex-direction: column; gap: 8px;"><sc-for list="{{ pdRows }}" as="b" hint-placeholder-count="4"><article class="amp-req" style="@CARD@ {{ b.at }}"><div style="display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 10px;"><span style="@LABEL@">{{ b.id }}</span><span style="{{ b.mStyle }}">{{ b.moscow }}</span><span style="{{ b.sStyle }}">{{ b.status }}</span><span style="flex: 1 1 260px; min-width: 0; font-size: 14px; font-weight: 700;">{{ b.title }}</span></div>
              <div style="display: flex; flex-wrap: wrap; gap: 4px 10px; font-size: 12.5px;"><span style="font-weight: 800;">Delivered on</span><sc-for list="{{ b.screens }}" as="x" hint-placeholder-count="2"><button onClick="{{ x.go }}" style="border: none; background: transparent; padding: 0; color: rgb(var(--ink-rgb)); font-size: 12.5px; text-decoration: underline; cursor: pointer;">{{ x.label }}</button></sc-for><span style="font-weight: 800;">Proved by</span><sc-for list="{{ b.checks }}" as="c" hint-placeholder-count="2"><span title="{{ c.what }}" style="font-family: 'Space Mono', monospace; font-weight: 700;">{{ c.c }}</span></sc-for></div>
              <div style="@SMALL@">From: {{ b.from }}</div></article></sc-for></div>
          </section>
          <section style="@PANEL@"><h2 style="@H2@">New words in release {{ pdRelease }}</h2><p style="margin: 0 0 10px; @SMALL@">Each release adds its new terms to the glossary, the thesaurus (other names), the knowledge graph and the tooltips at the same time, and the build fails if one is missing. {{ pdWordsN }} new in this release, {{ glTotal }} added so far. <a href="{{ pdGlossDoc }}" target="_blank" rel="noopener" style="@A@">Glossary on GitHub</a></p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 240px), 1fr)); gap: 8px;"><sc-for list="{{ pdWords }}" as="w" hint-placeholder-count="4"><div style="@CARD@"><button onClick="{{ w.go }}" style="align-self: flex-start; border: none; background: transparent; padding: 0; color: rgb(var(--ink-rgb)); font-size: 14px; font-weight: 900; text-decoration: underline; text-underline-offset: 3px; cursor: pointer; text-align: left;">{{ w.term }}</button><div style="font-size: 13px; line-height: 1.5;">{{ w.def }}</div><div style="@SMALL@">Also: {{ w.also }}</div></div></sc-for></div></section>
          <section style="@PANEL@"><h2 style="@H2@">How it is traced, tracked and managed on GitHub</h2>
            <ol style="margin: 0 0 10px; padding-left: 20px; display: flex; flex-direction: column; gap: 6px; font-size: 13.5px; line-height: 1.5;"><sc-for list="{{ pdGit }}" as="g" hint-placeholder-count="6"><li><span style="font-weight: 800;">{{ g.step }}.</span> {{ g.what }} <span style="font-family: 'Space Mono', monospace; font-size: 12px; overflow-wrap: anywhere;">{{ g.where }}</span></li></sc-for></ol>
            <p style="margin: 0; display: flex; flex-wrap: wrap; gap: 6px 16px; font-size: 13.5px;"><a href="{{ pdIssues }}" target="_blank" rel="noopener" style="@A@">Issues</a><a href="{{ pdPulls }}" target="_blank" rel="noopener" style="@A@">Pull requests</a><a href="{{ pdActions }}" target="_blank" rel="noopener" style="@A@">Checks and workflows</a><a href="{{ pdFollow }}" target="_blank" rel="noopener" style="@A@">Follow-ups due</a><a href="{{ pdDoc }}" target="_blank" rel="noopener" style="@A@">This page as a document</a></p>
          </section>
        </div>
        </sc-if>
'''
    notify = '''
        <sc-if value="{{ sNotify }}" hint-placeholder-val="{{ false }}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          ''' + HEAD.replace("@HUE@", "215").replace("@IC@", "icNotify").replace("@TITLE@", "Alerts &amp; notifications").replace("@LEDE@", "Choose which alerts appear at the top of each screen, bring back ones you dismissed, and follow updates from outside the portal. Your choices stay in this browser only: nothing is sent anywhere, and there is no account.") + '''
          <section style="@PANEL@"><h2 style="@H2@">Alerts right now</h2><sc-if value="{{ ntNone }}" hint-placeholder-val="{{ false }}"><p style="margin: 0; @SMALL@">Nothing to alert you about today.</p></sc-if>
            <div style="display: flex; flex-direction: column; gap: 6px;"><sc-for list="{{ ntAll }}" as="a" hint-placeholder-count="3"><div style="@CARD@ flex-direction: row; flex-wrap: wrap; align-items: center; gap: 6px 10px;"><span style="{{ a.tagStyle }}">{{ a.tag }}</span><span style="flex: 1 1 240px; min-width: 0; font-size: 13.5px;">{{ a.text }}</span><sc-if value="{{ a.hidden }}" hint-placeholder-val="{{ false }}"><button onClick="{{ a.restore }}" style="@BTN@">Show again</button></sc-if></div></sc-for></div></section>
          <section style="@PANEL@"><h2 style="@H2@">What to show</h2><p style="margin: 0 0 10px; @SMALL@">Safety notices always show, because they may matter to someone's safety; you can still dismiss each one once you have read it.</p>
            <div style="display: flex; flex-direction: column; gap: 8px;"><sc-for list="{{ ntPrefs }}" as="p" hint-placeholder-count="5"><label style="display: flex; align-items: flex-start; gap: 10px; font-size: 14px; line-height: 1.45; cursor: pointer;"><input type="checkbox" checked="{{ p.on }}" onChange="{{ p.toggle }}" style="width: 22px; height: 22px; margin: 1px 0 0; flex: 0 0 auto;"><span><span style="font-weight: 800;">{{ p.lbl }}</span><br><span style="@SMALL@">{{ p.why }}</span></span></label></sc-for></div>
            <p style="margin: 12px 0 0;"><button onClick="{{ ntReset }}" style="@BTN@">Reset my choices</button> <span style="@SMALL@">{{ ntDismissedN }} dismissed.</span></p></section>
          <section style="@PANEL@"><h2 style="@H2@">Follow updates from outside the portal</h2>
            <ul style="margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 8px; font-size: 13.5px; line-height: 1.5;">
              <li><span style="font-weight: 800;">A news feed.</span> Add this address to any feed reader to get What's new and every release: <span style="font-family: 'Space Mono', monospace; font-size: 12px; overflow-wrap: anywhere;">{{ ntFeed }}</span></li>
              <li><span style="font-weight: 800;">GitHub.</span> With a GitHub account (13 or over), <a href="{{ ntWatch }}" target="_blank" rel="noopener" style="@A@">watch the repository</a> and choose Releases, or follow the <a href="{{ ntReleases }}" target="_blank" rel="noopener" style="@A@">releases feed</a>.</li>
              <li><span style="font-weight: 800;">Follow-ups.</span> Every Monday a public issue lists what is due: open items, dates and re-checks. See it on the Product screen.</li>
            </ul></section>
          <section style="@PANEL@"><h2 style="@H2@">What we never do</h2><ul style="margin: 0; padding-left: 20px; font-size: 13.5px; line-height: 1.55;"><li>Ask for an email address, a phone number or an account to send you updates.</li><li>Send push notifications, or track what you read.</li><li>Use alerts to sell, campaign for a party, or rush you.</li></ul><p style="margin: 10px 0 0; @SMALL@">What this portal keeps on your device, and nowhere else: your Explain-for choice, your alert choices, which alerts you dismissed, the last release you saw and whether the news is paused (browser storage named amp-persona and amp-notify). Reset my choices clears the alert ones; your browser's settings clear all of it.</p></section>
        </div>
        </sc-if>
'''
    out = product + notify
    for k, v in (("@PANEL@", PANEL), ("@H2@", H2), ("@CARD@", CARD), ("@SMALL@", SMALL), ("@LABEL@", LABEL), ("@SEL@", SEL), ("@BTN@", BTN), ("@A@", A)):
        out = out.replace(k, v)
    return out


GOLIVE = '      ["golive", "Go-live readiness", "tri", 145, 4, "NEW", "go live readiness launch checklist gates tests routines release blockers moscow"]'
NAV9 = ('\n      ["product", "Product & roadmap", "sq", 70, 25, "NEW", "product vision strategy specification roadmap backlog requirements update schedule traceability github issues milestones"],'
        '\n      ["notify", "Alerts & notifications", "dot", 215, 5, "NEW", "alerts notifications notify updates feed rss atom subscribe watch news ticker preferences dismiss"]')


def transforms():
    gl_graph, gl_rows = graph_entries(), glossary_rows()
    return [
        ("ext9-load", "the glossary and product data load with the rest", '"./data/readiness.json"].map(get));', '"./data/readiness.json", "./data/glossary.json", "./data/product.json"].map(get));', 1),
        ("ext9-load-vars", "name them", "cm, tt, iv, rs, sd, rd] =", "cm, tt, iv, rs, sd, rd, gl, pd] =", 1),
        ("ext9-load-state", "keep them in state", "cm, tt, iv, rs, sd, rd, loaded", "cm, tt, iv, rs, sd, rd, gl, pd, loaded", 1),
        ("ext9-graph", "new vocabulary joins the knowledge graph, from data/glossary.json", "\n  };\n\n  ALLIES = [", ",  // the design's last entry has no trailing comma\n" + gl_graph + "\n  };\n\n  ALLIES = [", 1),
        ("ext9-glossary", "new vocabulary joins the glossary list, from data/glossary.json", "      ];\n\n  STANDARDS = [", "        ,\n" + gl_rows + "\n      ];\n\n  STANDARDS = [", 1),
        ("ext9-tip-terms", "term tooltips read the glossary first, so tooltip and glossary always agree",
         'if (kind === "term") { const e = (tt.terms || {})[id]; return e ? e.term + ": " + e.tip : ""; }',
         'if (kind === "term") { const g = (((this.state.amp || {}).gl || {}).terms || []).find((t) => t.id === id); if (g) return g.term + ": " + g.def; const e = (tt.terms || {})[id]; return e ? e.term + ": " + e.tip : ""; }', 1),
        ("ext9-nav", "Product and Alerts sit after Go-live readiness", GOLIVE + "\n    ]],", GOLIVE + "," + NAV9 + "\n    ]],", 1),
        ("ext9-hash", "the screens can be linked to", "|research|service|golive)$/.test(id)", "|research|service|golive|product|notify)$/.test(id)", 1),
        ("ext9-css", "ticker motion, pause and reduced-motion styles", "  .amp-sr {", CSS9 + "\n  .amp-sr {", 1),
        ("ext9-logic", "alerts, notification choices, ticker and product logic", "  async loadPetition() {", LOGIC9 + "\n  async loadPetition() {", 1),
        ("ext9-vals", "their values join renderVals", "...this.ampVals8(s),", "...this.ampVals8(s), ...this.ampVals9(s),", 1),
        ("ext9-strip", "alerts and the news ticker at the top of every screen, under the explainer",
         '        <sc-if value="{{ tbShow }}" hint-placeholder-val="{{ false }}">', STRIP + '        <sc-if value="{{ tbShow }}" hint-placeholder-val="{{ false }}">', 1),
        ("ext9-screens", "the Product and Alerts screens", '        <div data-slot="portal-end" style="display: none;"></div>', screens() + '\n        <div data-slot="portal-end" style="display: none;"></div>', 1),
    ]
