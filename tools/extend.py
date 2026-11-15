"""Portal extensions the build adds to the design: four screens, their data, icons and motion.

Each piece is a transform (name, reason, old, new, count) applied by build_site.py with the same exactly-N-matches
rule (B1). The screens read their content from data/*.json, the single source of truth for sources, updates,
safeguards, priorities and registers; nothing on them is hand-typed into the page.

  sources  Trusted sources: a filterable directory of official and voluntary-sector youth sources
  latest   What's new: dated, sourced changes since the design was made
  trust    Safeguards & audiences: who the portal is for (including parents and carers), the frameworks it follows,
           how it reaches every voice, and how it stays user-centred
  health   Portal health: the self-reporting screen (freshness, provenance, checks, defect and open registers)
"""

# --- logic added to the design's component class -------------------------------------------------------------

LOGIC = r'''
  async loadAmplifyData() {
    const get = async (f) => { try { const r = await fetch(new URL(f, document.baseURI).href, { cache: "no-store" }); return r.ok ? await r.json() : null; } catch (e) { return null; } };
    const [src, lat, sg, mo, reg, bld, ch, hp, ln, ig, ab] = await Promise.all(["./data/youth-sources.json", "./data/latest.json", "./data/safeguards.json", "./data/moscow.json", "./data/registers.json", "./build.json", "./data/changelog.json", "./data/help.json", "./data/launch.json", "./data/integrity.json", "./data/about.json"].map(get));
    this.setState({ amp: { src, lat, sg, mo, reg, bld, ch, hp, ln, ig, ab, loaded: true, failed: !(src && lat && sg) } });
  }
  ampDays(d) { const t = Date.parse(String(d) + "T00:00:00Z"); return isNaN(t) ? null : Math.floor((Date.now() - t) / 864e5); }
  ampDate(d) { const t = new Date(String(d) + "T00:00:00Z"); return isNaN(t) ? String(d) : t.toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric", timeZone: "UTC" }); }
  ampAdd(d, n) { const t = Date.parse(String(d) + "T00:00:00Z"); return isNaN(t) ? null : new Date(t + n * 864e5).toISOString().slice(0, 10); }
  ampIcon(name, color, size) {
    const z = size || 18, u = "url(./vendor/icons/" + name + ".svg)";
    return "display:inline-block;flex:0 0 " + z + "px;width:" + z + "px;height:" + z + "px;-webkit-mask:" + u + " center/contain no-repeat;mask:" + u + " center/contain no-repeat;background:" + color + ";";
  }
  ampFresh(checked, days) {
    const age = this.ampDays(checked);
    if (age === null) return { label: "Undated", hue: 25, age: "?" };
    if (age <= days) return { label: "Fresh", hue: 145, age };
    if (age <= Math.round(days * 1.5)) return { label: "Review due", hue: 70, age };
    return { label: "Overdue", hue: 25, age };
  }
  ampChip(on, hue) {
    return "display:inline-flex;align-items:center;gap:7px;min-height:36px;border-radius:999px;padding:6px 13px;font-size:13px;font-weight:600;cursor:pointer;border:1px solid " +
      (on ? "oklch(var(--t2) 0.16 " + hue + " / 0.85)" : "rgb(var(--film-rgb) / 0.18)") + ";background:" + (on ? "oklch(var(--t1) 0.16 " + hue + " / 0.24)" : "rgb(var(--film-rgb) / 0.04)") +
      ";color:" + (on ? "oklch(var(--t4) 0.14 " + hue + ")" : "rgb(var(--ink-rgb) / 0.86)") + ";";
  }
  ampVals(s) {
    const A = s.amp || {}, src = A.src || { sources: [], themes: {}, audiences: {} }, lat = A.lat || { items: [], categories: {} };
    const sg = A.sg || { audiences: [], parents: [], frameworks: [], every_voice: [], ucd: [] }, mo = A.mo || { rows: [] }, reg = A.reg || { defects: [], open: [] }, bld = A.bld || {};
    const TI = { voice: "megaphone", democracy: "vote", rights: "scale", safety: "shield-check", wellbeing: "heart-pulse", work: "coins", evidence: "chart-column", policy: "scroll-text", inclusion: "users" };
    const TH = { voice: 175, democracy: 215, rights: 300, safety: 25, wellbeing: 340, work: 70, evidence: 145, policy: 260, inclusion: 120 };
    const PV = { V: "Verified", S: "Search-sourced", K: "Lead, to confirm" };
    const PH = { V: 145, S: 215, K: 70 };
    const NATIONS = ["UK", "England", "Scotland", "Wales", "Northern Ireland"];
    const q = (s.srcQ || "").trim().toLowerCase();
    const inNation = (x) => s.srcNation === "all" || x.nations.indexOf(s.srcNation) >= 0 || (s.srcNation !== "UK" && x.nations.indexOf("UK") >= 0);
    const inAud = (x) => s.srcAud === "all" || (x.audiences || []).indexOf(s.srcAud) >= 0;
    const inQ = (x) => !q || (x.name + " " + x.what + " " + x.use + " " + x.kind).toLowerCase().indexOf(q) >= 0;
    const base = src.sources.filter((x) => inNation(x) && inAud(x) && inQ(x));
    const shown = base.filter((x) => s.srcTheme === "all" || x.theme === s.srcTheme);
    const themeChips = [["all", "All themes", 175, "layers"]].concat(Object.keys(src.themes).map((k) => [k, src.themes[k], TH[k] || 175, TI[k] || "layers"])).map(([k, label, hue, ic]) => {
      const n = k === "all" ? base.length : base.filter((x) => x.theme === k).length;
      return { label, count: String(n), pressed: s.srcTheme === k ? "true" : "false", style: this.ampChip(s.srcTheme === k, hue), icon: this.ampIcon(ic, "currentColor", 15), pick: () => this.setState({ srcTheme: k }) };
    });
    const nationChips = [["all", "Anywhere"]].concat(NATIONS.map((n) => [n, n])).map(([k, label]) => ({ label, pressed: s.srcNation === k ? "true" : "false", style: this.ampChip(s.srcNation === k, 215), pick: () => this.setState({ srcNation: k }) }));
    const audChips = [["all", "Everyone"]].concat(Object.keys(src.audiences || {}).map((k) => [k, src.audiences[k]])).map(([k, label]) => ({ label, pressed: s.srcAud === k ? "true" : "false", style: this.ampChip(s.srcAud === k, 300), pick: () => this.setState({ srcAud: k }) }));
    const cards = shown.map((x) => {
      const hue = TH[x.theme] || 175, f = this.ampFresh(x.checked, x.review_days || 90);
      return {
        name: x.name, kind: x.kind, nations: x.nations.join(" · "), what: x.what, use: x.use, url: x.url,
        contact: x.contact || "", hasContact: !!x.contact, note: x.note || "", hasNote: !!x.note,
        aud: (x.audiences || []).map((a) => (src.audiences || {})[a] || a).join(", "),
        prov: PV[x.provenance] || x.provenance, provStyle: "color:oklch(var(--t4) 0.14 " + (PH[x.provenance] || 25) + ");",
        checked: "Checked " + this.ampDate(x.checked) + " · " + f.label,
        icon: this.ampIcon(TI[x.theme] || "layers", "oklch(var(--t3) 0.16 " + hue + ")", 20),
        bar: "border-top:3px solid oklch(var(--t2) 0.16 " + hue + ");",
        tag: (src.themes || {})[x.theme] || x.theme
      };
    });
    const themesK = Object.keys(src.themes || {});
    const panHead = themesK.map((k) => ({ label: src.themes[k] }));
    const panRows = ["England", "Scotland", "Wales", "Northern Ireland"].map((n) => ({ nation: n, cells: themesK.map((k) => {
      const own = src.sources.filter((x) => x.theme === k && x.nations.indexOf(n) >= 0).length, uk = src.sources.filter((x) => x.theme === k && x.nations.indexOf("UK") >= 0).length;
      return { v: own + " + " + uk, sr: own + " specific to " + n + ", " + uk + " UK-wide", style: "padding:8px;text-align:center;border-radius:6px;white-space:nowrap;font-variant-numeric:tabular-nums;background:oklch(var(--t1) 0.15 " + (own ? 145 : uk ? 70 : 25) + " / " + (own ? 0.2 : 0.12) + ");" };
    }) }));
    const CI = { law: "landmark", pay: "coins", safety: "life-buoy", data: "chart-line", voice: "megaphone", strategy: "compass" };
    const CH = { law: 215, pay: 70, safety: 25, data: 145, voice: 175, strategy: 300 };
    const latItems = lat.items.slice().sort((a, b) => (a.date < b.date ? 1 : -1)).filter((x) => s.latestCat === "all" || x.cat === s.latestCat).map((x) => ({
      date: this.ampDate(x.date), cat: (lat.categories || {})[x.cat] || x.cat, title: x.title, body: x.body, url: x.url, source: x.source,
      prov: PV[x.provenance] || x.provenance, provStyle: "color:oklch(var(--t4) 0.14 " + (PH[x.provenance] || 25) + ");",
      status: x.status || "", hasStatus: !!x.status,
      icon: this.ampIcon(CI[x.cat] || "newspaper", "oklch(var(--t3) 0.16 " + (CH[x.cat] || 175) + ")", 20),
      dot: "flex:0 0 12px;width:12px;height:12px;border-radius:50%;margin-top:6px;background:oklch(var(--t2) 0.18 " + (CH[x.cat] || 175) + ");box-shadow:0 0 0 5px oklch(var(--t2) 0.18 " + (CH[x.cat] || 175) + " / 0.18);"
    }));
    const latChips = [["all", "Everything"]].concat(Object.keys(lat.categories || {}).map((k) => [k, lat.categories[k]])).map(([k, label]) => ({ label, pressed: s.latestCat === k ? "true" : "false", style: this.ampChip(s.latestCat === k, CH[k] || 175), pick: () => this.setState({ latestCat: k }) }));
    const SH = (t) => /^Met|Aligned/.test(t) ? 145 : /^Partly|Guidance/.test(t) ? 70 : /Open/.test(t) ? 25 : 215;
    const frameworks = sg.frameworks.map((x) => ({ name: x.name, owner: x.owner + " · " + x.nations.join(", "), kind: x.kind, how: x.how, url: x.url, status: x.status,
      pill: "display:inline-block;border-radius:999px;padding:3px 10px;font-size:12px;font-weight:700;background:oklch(var(--t1) 0.16 " + SH(x.status) + " / 0.22);color:oklch(var(--t4) 0.14 " + SH(x.status) + ");",
      prov: PV[x.provenance] || x.provenance, provStyle: "color:oklch(var(--t4) 0.14 " + (PH[x.provenance] || 25) + ");" }));
    const AI = { "1113": "sparkles", "1417": "megaphone", "1825": "briefcase", parents: "heart-handshake", allies: "handshake" };
    const audiences = sg.audiences.map((x) => ({ name: x.name, need: x.need, how: x.how, icon: this.ampIcon(AI[x.id] || "users", "oklch(var(--t3) 0.16 300)", 22) }));
    // Health: freshness of every data set and every source, provenance mix, checks, registers.
    const sets = [["Trusted sources", src], ["What's new", lat], ["Safeguards & frameworks", sg], ["Coverage priorities", mo], ["Registers", reg], ["Release log", A.ch || {}], ["Help & adoption", A.hp || {}], ["Launch plan", A.ln || {}], ["Content integrity", A.ig || {}]].map(([label, d]) => {
      const f = this.ampFresh(d.checked, d.review_days || 30);
      return { label, checked: d.checked ? this.ampDate(d.checked) : "Not loaded", next: d.checked ? this.ampDate(this.ampAdd(d.checked, d.review_days || 30)) : "—", state: A.loaded ? f.label : "Loading",
        dot: "flex:0 0 10px;width:10px;height:10px;border-radius:50%;background:oklch(var(--t2) 0.18 " + (A.loaded ? f.hue : 215) + ");", pulse: f.label === "Fresh" ? "amp-pulse" : "" };
    });
    const overdue = src.sources.filter((x) => this.ampFresh(x.checked, x.review_days || 90).label !== "Fresh");
    const helplines = src.sources.filter((x) => x.contact);
    const count = (p) => String(src.sources.filter((x) => x.provenance === p).length);
    const healthy = A.loaded && !A.failed && overdue.length === 0 && sets.every((x) => x.state === "Fresh");
    return {
      sSources: s.screen === "sources", sLatest: s.screen === "latest", sTrust: s.screen === "trust", sHealth: s.screen === "health",
      ampFailed: !!A.failed, ampOk: !A.failed,
      srcQ: s.srcQ, setSrcQ: (e) => this.setState({ srcQ: e.target.value }), clearSrc: () => this.setState({ srcQ: "", srcTheme: "all", srcNation: "all", srcAud: "all" }),
      themeChips, nationChips, audChips, srcCards: cards, srcCount: cards.length + " of " + src.sources.length + " sources", srcNone: A.loaded && cards.length === 0,
      moscow: mo.rows.map((r) => ({ p: r.p, theme: r.theme, where: r.where, status: r.status,
        pStyle: "font-family:'Space Mono',monospace;font-size:11px;font-weight:700;letter-spacing:0.06em;color:oklch(var(--t4) 0.15 " + ({ Must: 25, Should: 70, Could: 215 }[r.p] || 300) + ");" })),
      panHead, panRows, panCols: "display:grid;grid-template-columns:140px repeat(" + Math.max(1, themesK.length) + ", minmax(0, 1fr));gap:3px;",
      latChips, latItems, latAsOf: lat.checked ? "Checked " + this.ampDate(lat.checked) : "Loading",
      audiences, parentsTips: sg.parents.map((t, i) => ({ t, n: String(i + 1) })), frameworks, everyVoice: sg.every_voice || [], langs: sg.languages || [], ageIntro: (sg.age_access || {}).intro || "", ageBands: ((sg.age_access || {}).bands || []).map((b) => ({ b })), ageRows: ((sg.age_access || {}).rows || []).map((r) => ({ what: r.what, cells: [r.u13, r.a1315, r.a1617, r.a18].map((c, i) => ({ c, band: ((sg.age_access || {}).bands || [])[i] || "", style: "padding:8px;border-radius:8px;font-size:12.5px;line-height:1.4;background:oklch(var(--t1) 0.15 " + (/^Yourself/.test(c) ? 145 : /^No$/.test(c) ? 25 : 70) + " / 0.14);" })), why: r.why, prov: { V: "Verified", S: "Search-sourced", K: "Lead, to confirm" }[r.provenance] || r.provenance })), onBehalf: ((sg.age_access || {}).on_behalf || []).map((t) => ({ t })), icAge: this.ampIcon("users", "oklch(var(--t3) 0.16 70)", 18), deafTips: (sg.deaf || []).map((t, i) => ({ t, n: String(i + 1) })), icDeaf: this.ampIcon("accessibility", "oklch(var(--t3) 0.16 215)", 18), icLang: this.ampIcon("messages-square", "oklch(var(--t3) 0.16 120)", 18), ucd: (sg.ucd || []).map((t) => ({ t })),
      hBuild: bld.build_id || "Unknown build", hBuilt: bld.built ? this.ampDate(bld.built) : "—", hSets: sets,
      hStatus: !A.loaded ? "Checking…" : healthy ? "Healthy" : A.failed ? "Data could not load" : "Needs attention",
      hStatusStyle: "font-size:30px;font-weight:900;letter-spacing:-0.03em;color:oklch(var(--t4) 0.16 " + (!A.loaded ? 215 : healthy ? 145 : 25) + ");",
      hIcon: this.ampIcon(healthy ? "circle-check" : "triangle-alert", "oklch(var(--t3) 0.18 " + (healthy ? 145 : 25) + ")", 34),
      hOverdue: String(overdue.length), hHelplines: String(helplines.length), hV: count("V"), hS: count("S"), hK: count("K"), hTotal: String(src.sources.length),
      hOverdueList: overdue.map((x) => ({ name: x.name, checked: this.ampDate(x.checked) })), hAllFresh: overdue.length === 0,
      hChecks: (bld.checks || []).map((c) => ({ id: c.id, what: c.what })), hDefects: reg.defects || [], hOpen: reg.open || [],
      icSources: this.ampIcon("book-open-check", "oklch(var(--t3) 0.16 215)", 16), icLatest: this.ampIcon("newspaper", "oklch(var(--t3) 0.16 70)", 16),
      icTrust: this.ampIcon("shield-check", "oklch(var(--t3) 0.16 25)", 16), icHealth: this.ampIcon("activity", "oklch(var(--t3) 0.16 145)", 16),
      icExt: this.ampIcon("external-link", "currentColor", 13), icSearch: this.ampIcon("search", "rgb(var(--ink-rgb) / 0.7)", 16),
      icBug: this.ampIcon("bug", "oklch(var(--t3) 0.16 25)", 16), icTodo: this.ampIcon("list-todo", "oklch(var(--t3) 0.16 70)", 16),
      icParent: this.ampIcon("heart-handshake", "oklch(var(--t3) 0.16 340)", 18), icGlobe: this.ampIcon("globe", "oklch(var(--t3) 0.16 120)", 18),
      icUcd: this.ampIcon("users", "oklch(var(--t3) 0.16 215)", 18), icCheck: this.ampIcon("list-checks", "oklch(var(--t3) 0.16 145)", 16)
    };
  }
  navIcon(id, shape) {
    const N = { corner: "scale", route: "route", state: "landmark", issues: "layers", guide: "compass", hub: "megaphone", momentum: "trending-up", plan: "calendar-range",
      coal: "handshake", kit: "package", pledge: "hand-heart", radar: "radar", policy: "scroll-text", map: "map", acad: "graduation-cap", ysc: "messages-square",
      post: "file-search", track: "list-checks", prof: "users", incl: "accessibility", res: "library", ai: "sparkles", brand: "palette", care: "heart-handshake",
      graph: "network", sources: "book-open-check", latest: "newspaper", trust: "shield-check", health: "activity" };
    const n = N[id];
    if (!n) return this.ICONS[shape];
    const u = "url(./vendor/icons/" + n + ".svg)";
    return "flex:0 0 16px;width:16px;height:16px;-webkit-mask:" + u + " center/contain no-repeat;mask:" + u + " center/contain no-repeat;background:";
  }
'''

# --- shared fragments for the template ---------------------------------------------------------------------

EYEBROW = "display: flex; align-items: center; gap: 9px; font-family: 'Space Mono', monospace; font-size: 10.5px; letter-spacing: 0.16em; text-transform: uppercase;"
H1 = "margin: 4px 0 6px; font-size: 27px; font-weight: 900; letter-spacing: -0.035em; text-wrap: balance;"
LEDE = "margin: 0; font-size: 15px; line-height: 1.55; color: rgb(var(--ink-rgb) / 0.82); max-width: 68ch;"
PANEL = "border: 1px solid rgb(var(--film-rgb) / 0.12); border-radius: 22px; background: rgb(var(--film-rgb) / 0.04); padding: 20px 22px;"
LABEL = "font-family: 'Space Mono', monospace; font-size: 10.5px; letter-spacing: 0.14em; text-transform: uppercase; color: rgb(var(--ink-rgb) / 0.78);"
SMALL = "font-size: 12.5px; line-height: 1.55; color: rgb(var(--ink-rgb) / 0.8);"
LINK = "display: inline-flex; align-items: center; gap: 6px; font-size: 13px; font-weight: 700;"


def chips(lst, label):
    return f'''<div role="group" aria-label="{label}" style="display: flex; flex-wrap: wrap; gap: 8px;">
              <sc-for list="{{{{ {lst} }}}}" as="c" hint-placeholder-count="5">
                <button type="button" onClick="{{{{ c.pick }}}}" aria-pressed="{{{{ c.pressed }}}}" style="{{{{ c.style }}}}">{{{{ c.label }}}}</button>
              </sc-for>
            </div>'''


SCREENS = f'''
        <sc-if value="{{{{ sSources }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          <div>
            <div style="{EYEBROW} color: oklch(var(--t3) 0.16 215);"><span aria-hidden="true" style="{{{{ icSources }}}}"></span>Sources &amp; updates</div>
            <h1 style="{H1}">Trusted sources, checked and dated</h1>
            <p style="{LEDE}">Official bodies, parliaments, regulators and the voluntary sector, for young people, parents and carers, and adult allies. Every card says when it was checked and how sure we are.</p>
          </div>
          <sc-if value="{{{{ ampFailed }}}}" hint-placeholder-val="{{{{ false }}}}">
            <p role="alert" style="{PANEL} margin: 0;">The source list could not load. Nothing is shown rather than a guess. Try again, or use the helplines on Safeguarding &amp; support.</p>
          </sc-if>
          <div style="{PANEL} display: flex; flex-direction: column; gap: 12px;">
            <label for="amp-src-q" style="{LABEL}">Search sources</label>
            <div style="display: flex; align-items: center; gap: 8px; border: 1px solid rgb(var(--film-rgb) / 0.18); border-radius: 12px; background: rgb(var(--film-rgb) / 0.06); padding: 0 12px;">
              <span aria-hidden="true" style="{{{{ icSearch }}}}"></span>
              <input id="amp-src-q" type="search" value="{{{{ srcQ }}}}" onChange="{{{{ setSrcQ }}}}" placeholder="voting, helpline, NEET, Wales&hellip;" style="flex: 1 1 auto; min-width: 0; border: 0; background: transparent; color: rgb(var(--ink-rgb)); padding: 11px 0; font-size: 16px;" />
            </div>
            <div style="{LABEL}">Theme</div>
            {chips("themeChips", "Filter by theme")}
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px;">
              <div><div style="{LABEL} margin-bottom: 8px;">Nation</div>{chips("nationChips", "Filter by nation")}</div>
              <div><div style="{LABEL} margin-bottom: 8px;">Who it is for</div>{chips("audChips", "Filter by audience")}</div>
            </div>
            <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 10px;">
              <p aria-live="polite" style="margin: 0; {SMALL}">{{{{ srcCount }}}}</p>
              <button type="button" onClick="{{{{ clearSrc }}}}" style="min-height: 36px; border: 1px solid rgb(var(--film-rgb) / 0.18); border-radius: 999px; background: transparent; color: rgb(var(--ink-rgb) / 0.86); padding: 6px 14px; font-size: 13px; cursor: pointer;">Clear filters</button>
            </div>
          </div>
          <sc-if value="{{{{ srcNone }}}}" hint-placeholder-val="{{{{ false }}}}">
            <p style="{PANEL} margin: 0;">No source matches those filters. Clear them to see all sources.</p>
          </sc-if>
          <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 290px), 1fr)); gap: 14px;">
            <sc-for list="{{{{ srcCards }}}}" as="x" hint-placeholder-count="6">
              <article class="amp-card" style="{PANEL} {{{{ x.bar }}}} display: flex; flex-direction: column; gap: 9px;">
                <div style="display: flex; align-items: center; gap: 10px;"><span aria-hidden="true" style="{{{{ x.icon }}}}"></span><span style="{LABEL}">{{{{ x.tag }}}} &middot; {{{{ x.kind }}}}</span></div>
                <h2 style="margin: 0; font-size: 16.5px; font-weight: 800; line-height: 1.3; letter-spacing: -0.015em;">{{{{ x.name }}}}</h2>
                <p style="margin: 0; font-size: 13.5px; line-height: 1.55;">{{{{ x.what }}}}</p>
                <sc-if value="{{{{ x.hasContact }}}}" hint-placeholder-val="{{{{ false }}}}"><p style="margin: 0; font-family: 'Space Mono', monospace; font-size: 12.5px; font-weight: 700; color: oklch(var(--t4) 0.16 25);">{{{{ x.contact }}}}</p></sc-if>
                <p style="margin: 0; {SMALL}"><span style="font-weight: 700;">Use it to:</span> {{{{ x.use }}}}</p>
                <sc-if value="{{{{ x.hasNote }}}}" hint-placeholder-val="{{{{ false }}}}"><p style="margin: 0; {SMALL} font-style: italic;">{{{{ x.note }}}}</p></sc-if>
                <p style="margin: 0; {SMALL}">For: {{{{ x.aud }}}} &middot; {{{{ x.nations }}}}</p>
                <div style="margin-top: auto; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 8px; padding-top: 8px; border-top: 1px solid rgb(var(--film-rgb) / 0.1);">
                  <span style="font-size: 12px;"><span style="{{{{ x.provStyle }}}} font-weight: 700;">{{{{ x.prov }}}}</span> &middot; {{{{ x.checked }}}}</span>
                  <a href="{{{{ x.url }}}}" target="_blank" rel="noopener" style="{LINK}">Open site<span aria-hidden="true" style="{{{{ icExt }}}}"></span><span class="amp-sr"> (opens in a new tab)</span></a>
                </div>
              </article>
            </sc-for>
          </div>
          <div style="{PANEL}">
            <div style="{LABEL} margin-bottom: 4px;">Coverage across the UK</div>
            <p style="margin: 0 0 12px; {SMALL}">Sources specific to each nation, plus those that cover the whole UK. Amber means only UK-wide sources so far: an honest gap, not a hidden one.</p>
            <div role="region" aria-label="Coverage across the UK" tabindex="0" style="overflow-x: auto;">
              <div role="table" aria-label="Number of sources by nation and theme: nation-specific plus UK-wide" style="display: flex; flex-direction: column; gap: 3px; min-width: 760px; font-size: 13px;">
                <div role="row" style="{{{{ panCols }}}}"><span role="columnheader" style="padding: 8px; {LABEL}">Nation</span><sc-for list="{{{{ panHead }}}}" as="h" hint-placeholder-count="9"><span role="columnheader" style="padding: 8px 4px; text-align: center; {LABEL} letter-spacing: 0.04em;">{{{{ h.label }}}}</span></sc-for></div>
                <sc-for list="{{{{ panRows }}}}" as="r" hint-placeholder-count="4"><div role="row" style="{{{{ panCols }}}}"><span role="rowheader" style="padding: 8px; font-weight: 700;">{{{{ r.nation }}}}</span><sc-for list="{{{{ r.cells }}}}" as="c" hint-placeholder-count="9"><span role="cell" style="{{{{ c.style }}}}"><span aria-hidden="true">{{{{ c.v }}}}</span><span class="amp-sr">{{{{ c.sr }}}}</span></span></sc-for></div></sc-for>
              </div>
            </div>
          </div>
          <div style="{PANEL}">
            <div style="{LABEL} margin-bottom: 4px;">Coverage by priority (MoSCoW)</div>
            <p style="margin: 0 0 12px; {SMALL}">What the portal must, should and could cover, where each lives, and what is still open.</p>
            <div role="table" aria-label="Coverage by priority: theme, where it is covered, and status" style="display: flex; flex-direction: column; font-size: 13px;">
              <div role="row" class="amp-row4" style="display: grid; grid-template-columns: 120px minmax(0, 1.2fr) minmax(0, 1.6fr) minmax(0, 1.4fr); gap: 10px; padding: 8px 4px;"><span role="columnheader" style="{LABEL}">Priority</span><span role="columnheader" style="{LABEL}">Theme</span><span role="columnheader" style="{LABEL}">Where</span><span role="columnheader" style="{LABEL}">Status</span></div>
              <sc-for list="{{{{ moscow }}}}" as="m" hint-placeholder-count="6">
                <div role="row" class="amp-row4" style="display: grid; grid-template-columns: 120px minmax(0, 1.2fr) minmax(0, 1.6fr) minmax(0, 1.4fr); gap: 10px; padding: 9px 4px; border-top: 1px solid rgb(var(--film-rgb) / 0.1);"><span role="cell" style="{{{{ m.pStyle }}}}">{{{{ m.p }}}}</span><span role="cell" style="font-weight: 700;">{{{{ m.theme }}}}</span><span role="cell">{{{{ m.where }}}}</span><span role="cell">{{{{ m.status }}}}</span></div>
              </sc-for>
            </div>
          </div>
        </div>
        </sc-if>

        <sc-if value="{{{{ sLatest }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          <div>
            <div style="{EYEBROW} color: oklch(var(--t3) 0.16 70);"><span aria-hidden="true" style="{{{{ icLatest }}}}"></span>Sources &amp; updates &middot; {{{{ latAsOf }}}}</div>
            <h1 style="{H1}">What has changed for young people</h1>
            <p style="{LEDE}">Dated changes in law, pay, safety, data and youth voice, newest first, each with its source and how sure we are. Things announced are marked as announced, not done.</p>
          </div>
          {chips("latChips", "Filter updates by category")}
          <ol style="list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 12px;">
            <sc-for list="{{{{ latItems }}}}" as="x" hint-placeholder-count="5">
              <li class="amp-card" style="{PANEL} display: flex; gap: 16px;">
                <span aria-hidden="true" style="{{{{ x.dot }}}}"></span>
                <div style="flex: 1 1 auto; min-width: 0; display: flex; flex-direction: column; gap: 7px;">
                  <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 10px;"><span aria-hidden="true" style="{{{{ x.icon }}}}"></span><span style="{LABEL}"><time>{{{{ x.date }}}}</time> &middot; {{{{ x.cat }}}}</span>
                    <sc-if value="{{{{ x.hasStatus }}}}" hint-placeholder-val="{{{{ false }}}}"><span style="border: 1px solid rgb(var(--film-rgb) / 0.2); border-radius: 999px; padding: 2px 9px; font-size: 12px; font-weight: 700;">{{{{ x.status }}}}</span></sc-if></div>
                  <h2 style="margin: 0; font-size: 17px; font-weight: 800; letter-spacing: -0.015em;">{{{{ x.title }}}}</h2>
                  <p style="margin: 0; font-size: 14px; line-height: 1.6; max-width: 72ch;">{{{{ x.body }}}}</p>
                  <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 12px; font-size: 12.5px;">
                    <span><span style="{{{{ x.provStyle }}}} font-weight: 700;">{{{{ x.prov }}}}</span> &middot; {{{{ x.source }}}}</span>
                    <a href="{{{{ x.url }}}}" target="_blank" rel="noopener" style="{LINK}">Source<span aria-hidden="true" style="{{{{ icExt }}}}"></span><span class="amp-sr"> (opens in a new tab)</span></a>
                  </div>
                </div>
              </li>
            </sc-for>
          </ol>
        </div>
        </sc-if>

        <sc-if value="{{{{ sTrust }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          <div>
            <div style="{EYEBROW} color: oklch(var(--t3) 0.16 25);"><span aria-hidden="true" style="{{{{ icTrust }}}}"></span>Sources &amp; updates</div>
            <h1 style="{H1}">Safe for every young person, and for the adults behind them</h1>
            <p style="{LEDE}">Who Amplify is for, the rules it follows, how it reaches every voice, and what parents, carers and anyone with parental responsibility need to know.</p>
          </div>
          <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 250px), 1fr)); gap: 12px;">
            <sc-for list="{{{{ audiences }}}}" as="a" hint-placeholder-count="5">
              <div class="amp-card" style="{PANEL} display: flex; flex-direction: column; gap: 8px;">
                <span aria-hidden="true" style="{{{{ a.icon }}}}"></span>
                <h2 style="margin: 0; font-size: 15.5px; font-weight: 800; line-height: 1.3;">{{{{ a.name }}}}</h2>
                <p style="margin: 0; {SMALL}"><span style="font-weight: 700;">Needs:</span> {{{{ a.need }}}}</p>
                <p style="margin: 0; {SMALL}"><span style="font-weight: 700;">Here:</span> {{{{ a.how }}}}</p>
              </div>
            </sc-for>
          </div>
          <section aria-labelledby="amp-parents" style="border: 1px solid oklch(var(--t1) 0.16 340 / 0.4); border-radius: 24px; background: linear-gradient(150deg, oklch(var(--t1) 0.16 340 / 0.14), rgb(var(--film-rgb) / 0.03)); padding: 22px 24px;">
            <div style="{EYEBROW} color: oklch(var(--t3) 0.16 340); margin-bottom: 6px;"><span aria-hidden="true" style="{{{{ icParent }}}}"></span>For parents, carers and guardians</div>
            <h2 id="amp-parents" style="margin: 0 0 14px; font-size: 20px; font-weight: 900; letter-spacing: -0.03em;">Backing a young campaigner, safely</h2>
            <ol style="margin: 0; padding: 0; list-style: none; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr)); gap: 12px;">
              <sc-for list="{{{{ parentsTips }}}}" as="t" hint-placeholder-count="6">
                <li style="display: flex; gap: 12px;"><span aria-hidden="true" style="flex: 0 0 26px; height: 26px; display: grid; place-items: center; border-radius: 50%; background: oklch(var(--t2) 0.16 340); color: var(--on-accent); font-family: 'Space Mono', monospace; font-size: 12px; font-weight: 700;">{{{{ t.n }}}}</span><span style="font-size: 13.5px; line-height: 1.55;">{{{{ t.t }}}}</span></li>
              </sc-for>
            </ol>
            <p style="margin: 14px 0 0; {SMALL}">More for adults: open Trusted sources and choose <span style="font-weight: 700;">Parents &amp; carers</span>.</p>
          </section>
          <section aria-labelledby="amp-age" style="{PANEL}">
            <div style="{EYEBROW} color: oklch(var(--t3) 0.16 70); margin-bottom: 6px;"><span aria-hidden="true" style="{{{{ icAge }}}}"></span>Age and access</div>
            <h2 id="amp-age" style="margin: 0 0 8px; font-size: 19px; font-weight: 800; letter-spacing: -0.025em;">What you can do yourself at each age, and when an adult acts for you</h2>
            <p style="margin: 0 0 14px; font-size: 13.5px; line-height: 1.55; max-width: 76ch;">{{{{ ageIntro }}}}</p>
            <div role="table" aria-label="Routes by age band: yourself, with an adult, or an adult on your behalf" style="display: flex; flex-direction: column; gap: 6px;">
              <div role="row" class="amp-row4 amp-agehead" style="display: grid; grid-template-columns: minmax(0, 1.4fr) repeat(4, minmax(0, 1fr)); gap: 6px;"><span role="columnheader" style="{LABEL} padding: 6px;">Route</span><sc-for list="{{{{ ageBands }}}}" as="b" hint-placeholder-count="4"><span role="columnheader" style="{LABEL} padding: 6px;">{{{{ b.b }}}}</span></sc-for></div>
              <sc-for list="{{{{ ageRows }}}}" as="r" hint-placeholder-count="6">
                <div role="row" class="amp-row4" style="display: grid; grid-template-columns: minmax(0, 1.4fr) repeat(4, minmax(0, 1fr)); gap: 6px; padding-top: 6px; border-top: 1px solid rgb(var(--film-rgb) / 0.1);">
                  <span role="rowheader" style="padding: 6px; font-size: 13.5px; font-weight: 800; line-height: 1.35;">{{{{ r.what }}}}<span style="display: block; font-weight: 400; {SMALL} margin-top: 3px;">{{{{ r.why }}}} <span style="font-style: italic;">({{{{ r.prov }}}})</span></span></span>
                  <sc-for list="{{{{ r.cells }}}}" as="c" hint-placeholder-count="4"><span role="cell" style="{{{{ c.style }}}}"><span class="amp-agelabel" style="display: none; font-weight: 700;">{{{{ c.band }}}}: </span>{{{{ c.c }}}}</span></sc-for>
                </div>
              </sc-for>
            </div>
            <h3 style="margin: 18px 0 8px; font-size: 15.5px; font-weight: 800;">Acting on a young person's behalf: for parents, carers and adult allies</h3>
            <ul style="margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 6px;"><sc-for list="{{{{ onBehalf }}}}" as="o" hint-placeholder-count="6"><li style="font-size: 13.5px; line-height: 1.5;">{{{{ o.t }}}}</li></sc-for></ul>
          </section>
          <section aria-labelledby="amp-voices" style="{PANEL}">
            <div style="{EYEBROW} color: oklch(var(--t3) 0.16 120); margin-bottom: 6px;"><span aria-hidden="true" style="{{{{ icGlobe }}}}"></span>Every voice</div>
            <h2 id="amp-voices" style="margin: 0 0 14px; font-size: 19px; font-weight: 800; letter-spacing: -0.025em;">Reaching young people of every background, language and place</h2>
            <dl style="margin: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr)); gap: 12px 18px;">
              <sc-for list="{{{{ everyVoice }}}}" as="v" hint-placeholder-count="6">
                <div style="border-left: 3px solid oklch(var(--t2) 0.16 120); padding-left: 12px;"><dt style="font-size: 14px; font-weight: 700; line-height: 1.35;">{{{{ v.who }}}}</dt><dd style="margin: 4px 0 0; {SMALL}">{{{{ v.how }}}}</dd></div>
              </sc-for>
            </dl>
          </section>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 340px), 1fr)); gap: 14px;">
            <section aria-labelledby="amp-deaf" style="{PANEL}">
              <div style="{EYEBROW} color: oklch(var(--t3) 0.16 215); margin-bottom: 6px;"><span aria-hidden="true" style="{{{{ icDeaf }}}}"></span>d/Deaf participation</div>
              <h2 id="amp-deaf" style="margin: 0 0 12px; font-size: 18px; font-weight: 800; letter-spacing: -0.02em;">A checklist for campaigns that include d/Deaf young people</h2>
              <ol style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 9px;">
                <sc-for list="{{{{ deafTips }}}}" as="t" hint-placeholder-count="6"><li style="display: flex; gap: 10px; font-size: 13.5px; line-height: 1.5;"><span aria-hidden="true" style="flex: 0 0 22px; height: 22px; display: grid; place-items: center; border-radius: 50%; background: oklch(var(--t2) 0.16 215); color: var(--on-accent); font-family: 'Space Mono', monospace; font-size: 11px; font-weight: 700;">{{{{ t.n }}}}</span><span>{{{{ t.t }}}}</span></li></sc-for>
              </ol>
            </section>
            <section aria-labelledby="amp-langs" style="{PANEL}">
              <div style="{EYEBROW} color: oklch(var(--t3) 0.16 120); margin-bottom: 6px;"><span aria-hidden="true" style="{{{{ icLang }}}}"></span>Languages of the UK</div>
              <h2 id="amp-langs" style="margin: 0 0 12px; font-size: 18px; font-weight: 800; letter-spacing: -0.02em;">Official, regional and sign languages, and what Amplify supports</h2>
              <dl style="margin: 0; display: flex; flex-direction: column; gap: 10px;">
                <sc-for list="{{{{ langs }}}}" as="l" hint-placeholder-count="7"><div style="border-left: 3px solid oklch(var(--t2) 0.16 120); padding-left: 12px;"><dt style="font-size: 14px; font-weight: 800;">{{{{ l.lang }}}} <span style="font-weight: 400; {SMALL}">&middot; {{{{ l.where }}}}</span></dt><dd style="margin: 3px 0 0; {SMALL}">{{{{ l.status }}}}</dd></div></sc-for>
              </dl>
            </section>
          </div>
          <section aria-labelledby="amp-frameworks" style="{PANEL}">
            <div style="{EYEBROW} color: oklch(var(--t3) 0.16 25); margin-bottom: 6px;"><span aria-hidden="true" style="{{{{ icCheck }}}}"></span>Rules we follow</div>
            <h2 id="amp-frameworks" style="margin: 0 0 14px; font-size: 19px; font-weight: 800; letter-spacing: -0.025em;">Law, codes, standards and strategies, and how Amplify meets each</h2>
            <div style="display: flex; flex-direction: column; gap: 10px;">
              <sc-for list="{{{{ frameworks }}}}" as="f" hint-placeholder-count="6">
                <div class="amp-card" style="border: 1px solid rgb(var(--film-rgb) / 0.1); border-radius: 16px; padding: 14px 16px; display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 6px 14px; align-items: start;">
                  <div style="min-width: 0;"><div style="font-size: 14.5px; font-weight: 800; line-height: 1.35;">{{{{ f.name }}}}</div><div style="{SMALL}">{{{{ f.kind }}}} &middot; {{{{ f.owner }}}}</div></div>
                  <span style="{{{{ f.pill }}}}">{{{{ f.status }}}}</span>
                  <p style="grid-column: 1 / -1; margin: 0; font-size: 13.5px; line-height: 1.55;">{{{{ f.how }}}}</p>
                  <div style="grid-column: 1 / -1; display: flex; flex-wrap: wrap; gap: 12px; font-size: 12px;"><span style="{{{{ f.provStyle }}}} font-weight: 700;">{{{{ f.prov }}}}</span><a href="{{{{ f.url }}}}" target="_blank" rel="noopener" style="{LINK} font-size: 12px;">Read it<span aria-hidden="true" style="{{{{ icExt }}}}"></span><span class="amp-sr"> (opens in a new tab)</span></a></div>
                </div>
              </sc-for>
            </div>
          </section>
          <section aria-labelledby="amp-ucd" style="{PANEL}">
            <div style="{EYEBROW} color: oklch(var(--t3) 0.16 215); margin-bottom: 6px;"><span aria-hidden="true" style="{{{{ icUcd }}}}"></span>Designed with its users</div>
            <h2 id="amp-ucd" style="margin: 0 0 12px; font-size: 19px; font-weight: 800; letter-spacing: -0.025em;">How Amplify stays user-centred, and where it has not been tested yet</h2>
            <ul style="margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 8px;">
              <sc-for list="{{{{ ucd }}}}" as="u" hint-placeholder-count="4"><li style="font-size: 13.5px; line-height: 1.55;">{{{{ u.t }}}}</li></sc-for>
            </ul>
          </section>
        </div>
        </sc-if>

        <sc-if value="{{{{ sHealth }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          <div>
            <div style="{EYEBROW} color: oklch(var(--t3) 0.16 145);"><span aria-hidden="true" style="{{{{ icHealth }}}}"></span>Sources &amp; updates &middot; build {{{{ hBuild }}}}</div>
            <h1 style="{H1}">Portal health</h1>
            <p style="{LEDE}">This page checks itself every time it opens: how fresh each data set is, how sure each source is, which checks guard the build, and what is still open. It reports; it never hides a problem.</p>
          </div>
          <div class="amp-card" style="{PANEL} display: flex; flex-wrap: wrap; align-items: center; gap: 18px;">
            <span aria-hidden="true" style="{{{{ hIcon }}}}"></span>
            <div style="flex: 1 1 260px;"><div role="status" style="{{{{ hStatusStyle }}}}">{{{{ hStatus }}}}</div><div style="{SMALL}">Built {{{{ hBuilt }}}} &middot; {{{{ hTotal }}}} sources &middot; {{{{ hHelplines }}}} helplines &middot; {{{{ hOverdue }}}} past their review date</div></div>
            <div style="display: flex; gap: 18px; flex-wrap: wrap;">
              <div><div class="amp-count" style="font-size: 26px; font-weight: 900;">{{{{ hV }}}}</div><div style="{LABEL}">Verified</div></div>
              <div><div class="amp-count" style="font-size: 26px; font-weight: 900;">{{{{ hS }}}}</div><div style="{LABEL}">Search-sourced</div></div>
              <div><div class="amp-count" style="font-size: 26px; font-weight: 900;">{{{{ hK }}}}</div><div style="{LABEL}">Leads</div></div>
            </div>
          </div>
          <div style="{PANEL}">
            <div style="{LABEL} margin-bottom: 10px;">Freshness</div>
            <div role="table" aria-label="Each data set, when it was last checked, when it is next due, and its state" style="display: flex; flex-direction: column; font-size: 13.5px;">
              <div role="row" style="display: grid; grid-template-columns: minmax(0, 2fr) repeat(3, minmax(0, 1fr)); gap: 8px; padding: 8px 4px;"><span role="columnheader" style="{LABEL}">Data set</span><span role="columnheader" style="{LABEL}">Checked</span><span role="columnheader" style="{LABEL}">Next review</span><span role="columnheader" style="{LABEL}">State</span></div>
              <sc-for list="{{{{ hSets }}}}" as="d" hint-placeholder-count="5">
                <div role="row" style="display: grid; grid-template-columns: minmax(0, 2fr) repeat(3, minmax(0, 1fr)); gap: 8px; padding: 9px 4px; border-top: 1px solid rgb(var(--film-rgb) / 0.1);"><span role="cell" style="font-weight: 700;">{{{{ d.label }}}}</span><span role="cell">{{{{ d.checked }}}}</span><span role="cell">{{{{ d.next }}}}</span><span role="cell" style="display: inline-flex; align-items: center; gap: 8px;"><span aria-hidden="true" class="{{{{ d.pulse }}}}" style="{{{{ d.dot }}}}"></span>{{{{ d.state }}}}</span></div>
              </sc-for>
            </div>
            <sc-if value="{{{{ hAllFresh }}}}" hint-placeholder-val="{{{{ true }}}}"><p style="margin: 12px 0 0; {SMALL}">Every source is inside its review window.</p></sc-if>
            <ul style="margin: 12px 0 0; padding-left: 18px; {SMALL}"><sc-for list="{{{{ hOverdueList }}}}" as="o" hint-placeholder-count="0"><li>{{{{ o.name }}}}: last checked {{{{ o.checked }}}}</li></sc-for></ul>
          </div>
          <div style="{PANEL}">
            <div style="{LABEL} margin-bottom: 6px;">Content integrity: what kind of content each screen holds</div>
            <dl style="margin: 0 0 12px; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr)); gap: 8px 16px;"><sc-for list="{{{{ igClasses }}}}" as="c" hint-placeholder-count="5"><div><dt style="{{{{ c.style }}}}">{{{{ c.k }}}}</dt><dd style="margin: 2px 0 0; {SMALL}">{{{{ c.v }}}}</dd></div></sc-for></dl>
            <div role="table" aria-label="Each screen, its content class and why" style="display: flex; flex-direction: column; font-size: 13px;">
              <div role="row" class="amp-row4" style="display: grid; grid-template-columns: minmax(0, 1fr) 110px minmax(0, 3fr); gap: 10px; padding: 8px 4px;"><span role="columnheader" style="{LABEL}">Screen</span><span role="columnheader" style="{LABEL}">Class</span><span role="columnheader" style="{LABEL}">Why</span></div>
              <sc-for list="{{{{ igRows }}}}" as="r" hint-placeholder-count="8"><div role="row" class="amp-row4" style="display: grid; grid-template-columns: minmax(0, 1fr) 110px minmax(0, 3fr); gap: 10px; padding: 8px 4px; border-top: 1px solid rgb(var(--film-rgb) / 0.1);"><span role="cell" style="font-weight: 700;">{{{{ r.screen }}}}</span><span role="cell" style="{{{{ r.style }}}}">{{{{ r.cls }}}}</span><span role="cell">{{{{ r.why }}}}</span></div></sc-for>
            </div>
          </div>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr)); gap: 14px;">
            <div style="{PANEL}">
              <div style="{EYEBROW} color: oklch(var(--t3) 0.16 145); margin-bottom: 10px;"><span aria-hidden="true" style="{{{{ icCheck }}}}"></span>Checks guarding every build</div>
              <ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 7px;">
                <sc-for list="{{{{ hChecks }}}}" as="c" hint-placeholder-count="8"><li style="display: flex; gap: 10px; font-size: 13px; line-height: 1.45;"><span style="flex: 0 0 34px; font-family: 'Space Mono', monospace; font-weight: 700; color: oklch(var(--t4) 0.14 145);">{{{{ c.id }}}}</span><span>{{{{ c.what }}}}</span></li></sc-for>
              </ul>
              <p style="margin: 12px 0 0; {SMALL}">Each check is proved by a deliberate break before it is trusted. A passing check is evidence, not proof.</p>
            </div>
            <div style="display: flex; flex-direction: column; gap: 14px;">
              <div style="{PANEL}">
                <div style="{EYEBROW} color: oklch(var(--t3) 0.16 25); margin-bottom: 10px;"><span aria-hidden="true" style="{{{{ icBug }}}}"></span>Defects found and fixed</div>
                <ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 9px;">
                  <sc-for list="{{{{ hDefects }}}}" as="d" hint-placeholder-count="4"><li style="font-size: 13px; line-height: 1.5;"><span style="font-family: 'Space Mono', monospace; font-weight: 700;">{{{{ d.id }}}}</span> {{{{ d.what }}}} <span style="color: rgb(var(--ink-rgb) / 0.72);">Fix: {{{{ d.fix }}}} Check: {{{{ d.check }}}}.</span></li></sc-for>
                </ul>
              </div>
              <div style="{PANEL}">
                <div style="{EYEBROW} color: oklch(var(--t3) 0.16 70); margin-bottom: 10px;"><span aria-hidden="true" style="{{{{ icTodo }}}}"></span>Still open, and who must act</div>
                <ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 9px;">
                  <sc-for list="{{{{ hOpen }}}}" as="o" hint-placeholder-count="4"><li style="font-size: 13px; line-height: 1.5;"><span style="font-family: 'Space Mono', monospace; font-weight: 700;">{{{{ o.id }}}}</span> {{{{ o.what }}}} <span style="color: rgb(var(--ink-rgb) / 0.72);">Who: {{{{ o.who }}}}.</span></li></sc-for>
                </ul>
              </div>
            </div>
          </div>
        </div>
        </sc-if>
'''

GROUP_T = '''
    ["Sources & updates", [
      ["sources", "Trusted sources", "sq", 215, {nsrc}, "NEW", "trusted sources directory official government parliament regulator charity helpline commissioner parents carers allies nation Scotland Wales Northern Ireland England filter verified"],
      ["latest", "What's new", "bar", 70, {nlat}, "NEW", "latest news updates changes votes at 16 bill minimum wage NEET social media ban strategy helpline closed"],
      ["trust", "Safeguards & audiences", "dia", 25, 5, "NEW", "safeguards frameworks Children's code ICO Online Safety Act Ofcom parents carers guardians parental responsibility audiences DEI inclusion every voice UCD Lundy"],
      ["health", "Portal health", "ring", 145, 4, "NEW", "health self check freshness staleness provenance checks defects open register status"]
    ]]'''

MOTION_CSS = '''
  /* Motion added by the build: one purposeful entrance per screen, staggered cards, a live pulse. All of it stops
     under the in-app motion switch and under prefers-reduced-motion (the two rules below this block). */
  @keyframes amp-rise { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: none; } }
  @keyframes amp-pulse { 0%, 100% { box-shadow: 0 0 0 0 oklch(0.75 0.17 145 / 0.55); } 70% { box-shadow: 0 0 0 8px oklch(0.75 0.17 145 / 0); } }
  main > div { animation: amp-rise .42s cubic-bezier(.2,.7,.2,1) both; }
  .amp-card { animation: amp-rise .5s cubic-bezier(.2,.7,.2,1) both; transition: transform .18s ease, border-color .18s ease; }
  .amp-card:nth-child(2) { animation-delay: .04s; } .amp-card:nth-child(3) { animation-delay: .08s; } .amp-card:nth-child(4) { animation-delay: .12s; }
  .amp-card:nth-child(5) { animation-delay: .16s; } .amp-card:nth-child(n+6) { animation-delay: .2s; }
  .amp-card:hover { transform: translateY(-2px); }
  .amp-pulse { animation: amp-pulse 2.2s ease-out infinite; }
  main [role="region"], .amp-card, main [role="table"] { position: relative; }
  .amp-sr { position: absolute !important; left: 0; top: 0; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0; }
  @media (max-width: 420px) { main div[style*="grid-template-columns"]:not([role="row"]) { grid-template-columns: minmax(0, 1fr) !important; } main a { overflow-wrap: anywhere; max-width: 100%; white-space: normal !important; flex-shrink: 1 !important; box-sizing: border-box; } main a span { min-width: 0; overflow-wrap: anywhere; } }
  @media (max-width: 640px) { .amp-row4 { grid-template-columns: minmax(0, 1fr) !important; gap: 2px !important; } .amp-agehead { display: none !important; } .amp-agelabel { display: inline !important; } }
  main button:focus-visible, main a:focus-visible, main input:focus-visible, footer a:focus-visible { outline: 3px solid oklch(0.8 0.17 70); outline-offset: 2px; }
'''


def transforms(nsrc, nlat):
    GROUP = GROUP_T.replace("{nsrc}", str(nsrc)).replace("{nlat}", str(nlat))
    return [
        ("ext-motion-css", "purposeful motion and focus styles, switched off by the existing motion rules that follow",
         '  body[data-motion="off"] *, body[data-motion="off"] *::before, body[data-motion="off"] *::after',
         MOTION_CSS + '  body[data-motion="off"] *, body[data-motion="off"] *::before, body[data-motion="off"] *::after', 1),
        ("ext-hash", "the four new screens can be linked to and opened from the address",
         "|corner|route|state|issues|guide)$/.test(id)", "|corner|route|state|issues|guide|sources|latest|trust|health)$/.test(id)", 1),
        ("ext-state", "filters for the new screens start open",
         'kitAudience: "teacher", copied: "",', 'kitAudience: "teacher", copied: "", srcTheme: "all", srcNation: "all", srcAud: "all", srcQ: "", latestCat: "all", amp: null,', 1),
        ("ext-load", "load the data the new screens read, alongside the petition snapshot",
         "    this.loadPetition();\n", "    this.loadPetition();\n    this.loadAmplifyData();\n", 1),
        ("ext-logic", "the new screens' logic: data loading, freshness, filters, icons",
         "  async loadPetition() {", LOGIC + "\n  async loadPetition() {", 1),
        ("ext-group", "the new screens join the drawer as their own group, after Capability",
         '["graph", "Glossary & graph", "ring", 145, 4, "NEW", "knowledge graph glossary thesaurus definitions terms jargon synonyms"]\n    ]]\n  ];',
         '["graph", "Glossary & graph", "ring", 145, 4, "NEW", "knowledge graph glossary thesaurus definitions terms jargon synonyms"]\n    ]],' + GROUP + '\n  ];', 1),
        ("ext-vals", "the new screens' values join renderVals",
         'sIssues: s.screen === "issues", sCare: s.screen === "care",', '...this.ampVals(s), ...this.ampVals2(s), sIssues: s.screen === "issues", sCare: s.screen === "care",', 1),
        ("ext-nav-icons", "professional, contextual icons in the drawer, coloured by each section's hue",
         'icon: this.ICONS[shape] + "oklch(var(--t2) 0.16 " + hue + ");",', 'icon: this.navIcon(id, shape) + "oklch(var(--t2) 0.16 " + hue + ");",', 1),
        ("ext-screens", "the four new screens",
         '        <div data-slot="portal-end" style="display: none;"></div>', SCREENS + '\n        <div data-slot="portal-end" style="display: none;"></div>', 1),
    ]
