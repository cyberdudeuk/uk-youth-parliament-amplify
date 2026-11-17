"""Eleventh set of portal extensions: Inside Parliament (17 November 2026).

  parliament  A new Foundations screen on how Parliament actually runs, written for young people, in six tabs:
              Time (the parliamentary year, the sitting week with a chart of both Houses' hours, the Commons day
              and how to read the Order Paper), A day in the life (a Member of Youth Parliament, a backbench MP and
              a peer side by side), Who does what (Speaker, Leaders, whips, Lord Speaker, Crossbench Convenor,
              Procedure Committee, clerks; filterable by House), The building (1834 fire to Restoration and
              Renewal), Who changes the rules, and Use it and go further (with related campaigns and topics,
              filterable by where they live). Every fact names its source in data/parliament.json with V
              (official page) or S (secondary) provenance; roles are described, never named, and link to the
              official page that says who holds them now, so the screen cannot go stale when people change.
              It points to UK Youth Parliament and UK Parliament pages rather than repeating them.
              check_site S21 fails a build where a fact has no source, a source is unknown or unused, a role
              names a person, a tab has no panel, or the tabs lose their tablist semantics (defect D36).
"""
import json, os

from extend import PANEL, LABEL, SMALL, EYEBROW, H1, LEDE
from extend4 import H2, CARD

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = "color: rgb(var(--ink-rgb)); font-weight: 700; text-underline-offset: 3px;"
SEL = "min-width: 0; max-width: 100%; min-height: 36px; border: 1px solid rgb(var(--film-rgb) / 0.2); border-radius: 10px; background: rgb(var(--film-rgb) / 0.05); color: rgb(var(--ink-rgb)); padding: 6px 10px; font-size: 13px;"
BTN = "min-height: 32px; border: 1px solid rgb(var(--film-rgb) / 0.25); border-radius: 999px; background: transparent; color: rgb(var(--ink-rgb)); padding: 4px 12px; font-size: 12.5px; font-weight: 800; cursor: pointer;"


def data():
    with open(os.path.join(R, "data", "parliament.json"), encoding="utf-8") as f:
        return json.load(f)


LOGIC11 = r'''
  ampVals11(s) {
    const A = s.amp || {}, pa = A.pa || {};
    const arr = (x) => (Array.isArray(x) ? x : []);
    const tabs = arr(pa.tabs), ids = tabs.map((t) => t.id), tab = ids.indexOf(s.paTab) >= 0 ? s.paTab : (ids[0] || "time");
    const SRC = {}; arr(pa.sources).forEach((x) => { SRC[x.id] = x; });
    const pill = (h) => "display:inline-block;border-radius:999px;padding:1px 8px;font-family:'Space Mono',monospace;font-size:10.5px;font-weight:700;background:oklch(var(--t1) 0.16 " + h + " / 0.28);color:oklch(var(--t4) 0.15 " + h + ");";
    const cite = (list) => arr(list).map((id) => { const x = SRC[id] || {}; const off = x.provenance === "V";
      return { label: x.label || id, url: x.url || "#", prov: off ? "Official" : "Secondary", pStyle: pill(off ? 145 : 70) }; });
    const ed = (x) => ({ editorial: !!x.editorial, edStyle: pill(300) });
    const L = {}; this.GROUPS.forEach(([g, items]) => items.forEach(([id, lbl]) => { L[id] = lbl; }));
    const go = (id) => () => this.setState({ screen: id }, () => { try { window.scrollTo(0, 0); } catch (e) { /* no window */ } });
    const H = { Commons: 145, Lords: 300, Both: 70, "Westminster Hall": 215 };
    const house = s.paHouse || "All", rel = s.paRel || "All";
    const weekBy = {}; arr(pa.week).forEach((w) => { (weekBy[w.house] = weekBy[w.house] || []).push(w); });
    const pct = (h) => Math.max(0, Math.min(100, ((h - 8) / 16) * 100)).toFixed(2) + "%";
    const bar = (span, hue) => (span ? { has: true, style: "position:absolute;top:0;bottom:0;left:" + pct(span[0]) + ";width:calc(" + pct(span[1]) + " - " + pct(span[0]) + ");border-radius:6px;background:oklch(var(--t2) 0.15 " + hue + " / 0.85);",
      label: ((x) => { const f = (v) => { const hh = Math.floor(v), mm = Math.round((v - hh) * 60), ap = hh >= 12 ? "pm" : "am", h12 = ((hh + 11) % 12) + 1; return h12 + (mm ? "." + String(mm).padStart(2, "0") : "") + ap; }; return f(x[0]) + " to " + f(x[1]); })(span) } : { has: false, style: "", label: "not normally sitting" });
    const ch = pa.chart || { days: [], src: [] };
    const relItems = arr((pa.related || {}).items);
    const relSt = ["All"].concat(Array.from(new Set(relItems.map((x) => x.status))));
    const SH = { "On Amplify": 145, "Linked to its owner": 215, Candidate: 70 };
    const paKey = (e) => { const cur = ((e.currentTarget && e.currentTarget.id) || "").replace("pa-tab-", ""); let i = ids.indexOf(cur) >= 0 ? ids.indexOf(cur) : ids.indexOf(tab); if (i < 0) return;
      if (e.key === "ArrowRight") i = (i + 1) % ids.length; else if (e.key === "ArrowLeft") i = (i - 1 + ids.length) % ids.length;
      else if (e.key === "Home") i = 0; else if (e.key === "End") i = ids.length - 1; else return;
      e.preventDefault(); this.setState({ paTab: ids[i] }, () => { const b = document.getElementById("pa-tab-" + ids[i]); if (b) b.focus(); }); };
    const roles = arr(pa.roles).filter((r) => house === "All" || r.house === house || r.house === "Both");
    return {
      sParliament: s.screen === "parliament",
      icParliament: this.ampIcon("vote", "oklch(var(--t3) 0.16 145)", 16),
      paLede: pa.lede || "", paChecked: pa.checked || "", paRule: pa.rule || "",
      paTabs: tabs.map((t) => ({ label: t.label, tid: "pa-tab-" + t.id, pid: "pa-panel-" + t.id, sel: tab === t.id ? "true" : "false",
        icon: this.ampIcon(t.icon, tab === t.id ? "oklch(var(--t4) 0.15 145)" : "rgb(var(--ink-rgb) / 0.75)", 15),
        style: "display:inline-flex;align-items:center;gap:7px;min-height:40px;padding:8px 14px;border-radius:999px;cursor:pointer;font-size:13.5px;font-weight:800;border:1px solid " + (tab === t.id ? "oklch(var(--t2) 0.15 145 / 0.9);background:oklch(var(--t1) 0.16 145 / 0.3);color:rgb(var(--ink-rgb));" : "rgb(var(--film-rgb) / 0.2);background:transparent;color:rgb(var(--ink-rgb) / 0.86);"),
        go: () => this.setState({ paTab: t.id }), key: (e) => paKey(e) })),
      paTime: tab === "time", paLife: tab === "life", paRoles: tab === "roles", paBuilding: tab === "building", paRulesTab: tab === "rules", paGo: tab === "go",
      paYear: arr(pa.year).map((x) => ({ t: x.t, d: x.d, cites: cite(x.src), ...ed(x) })),
      paWeek: Object.keys(weekBy).map((h) => ({ house: h, hStyle: pill(H[h] || 175), rows: weekBy[h].map((w) => ({ day: w.day, hours: w.hours, cites: cite(w.src) })) })),
      paWeekNote: pa.week_note || "", paWeekNoteCites: cite(pa.week_note_src),
      paChart: arr(ch.days).map((d) => ({ day: d.day, c: bar(d.commons, 145), l: bar(d.lords, 300) })),
      paChartNote: ch.note || "", paChartCites: cite(ch.src),
      paChartTicks: [8, 12, 16, 20, 24].map((h) => ({ t: (h === 24 ? "12am" : h === 12 ? "12pm" : (h > 12 ? h - 12 + "pm" : h + "am")), style: "position:absolute;top:0;left:" + pct(h) + ";transform:translateX(-50%);" })),
      paDay: arr(pa.day).map((x) => ({ when: x.when, what: x.what, d: x.d, cites: cite(x.src) })),
      paOP: arr(pa.orderpaper).map((x) => ({ part: x.part, d: x.d, cites: cite(x.src) })),
      paLifeIntro: pa.life_intro || "",
      paLifeCards: arr(pa.life).map((x) => ({ role: x.role, who: x.who, time: x.time, where: x.where, rhythm: arr(x.rhythm).map((t) => ({ t })),
        own: x.own, ownUrl: (SRC[x.own_src] || {}).url || "#", cites: cite(x.src), top: "border-top: 4px solid oklch(var(--t2) 0.15 " + (x.hue || 175) + ");" })),
      paHouse: house, setPaHouse: (e) => this.setState({ paHouse: e.target.value }),
      paRoleShown: String(roles.length), paRoleTotal: String(arr(pa.roles).length),
      paRoleCards: roles.map((r) => ({ role: r.role, house: r.house, hStyle: pill(H[r.house] || 175), d: r.d, youth: r.youth, who: r.who_url, cites: cite(r.src) })),
      paBuild: arr(pa.building).map((x) => ({ date: x.date, what: x.what, cites: cite(x.src) })),
      paBuildNote: pa.building_note || "", paBuildNoteCites: cite(pa.building_note_src),
      paRulesIntro: pa.rules_intro || "",
      paRules: arr(pa.rules).map((x) => ({ t: x.t, d: x.d, cites: cite(x.src), ...ed(x) })),
      paUse: arr(pa.use).map((x) => ({ t: x.t, d: x.d, hasScreen: !!(x.screen && L[x.screen]), screenLabel: L[x.screen] || "", go: go(x.screen), hasUrl: !!x.url, url: x.url || "#", cites: cite(x.src) })),
      paRelIntro: (pa.related || {}).intro || "", paRel: rel, setPaRel: (e) => this.setState({ paRel: e.target.value }),
      paRelOpts: relSt.map((v) => ({ v, label: v === "All" ? "All" : v })),
      paRelItems: relItems.filter((x) => rel === "All" || x.status === rel).map((x) => ({ t: x.t, kind: x.kind, status: x.status, sStyle: pill(SH[x.status] || 175),
        hasScreen: !!(x.screen && L[x.screen]), screenLabel: L[x.screen] || "", go: go(x.screen) })),
      paRelShown: String(relItems.filter((x) => rel === "All" || x.status === rel).length), paRelTotal: String(relItems.length),
      paSources: arr(pa.sources).map((x) => ({ label: x.label, url: x.url, prov: x.provenance === "V" ? "Official" : "Secondary", pStyle: pill(x.provenance === "V" ? 145 : 70), checked: x.checked })),
      paSrcN: String(arr(pa.sources).length), paSrcV: String(arr(pa.sources).filter((x) => x.provenance === "V").length)
    };
  }
'''

CSS11 = '''
  .amp-pa-panel { animation: none; }
  @media (prefers-reduced-motion: no-preference) { .amp-pa-panel { animation: ampPaIn 0.28s ease-out; } @keyframes ampPaIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: none; } } }
  .amp-pa-tl { position: relative; padding-left: 22px; }
  .amp-pa-tl::before { content: ""; position: absolute; left: 7px; top: 6px; bottom: 6px; width: 2px; border-radius: 2px; background: oklch(var(--t2) 0.12 145 / 0.5); }
'''

CITES = ('<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 4px 8px; @SMALL@"><span style="font-weight: 800;">Source</span>'
         '<sc-for list="{{ @V@.cites }}" as="c" hint-placeholder-count="1"><span style="display: inline-flex; flex-wrap: wrap; align-items: center; gap: 4px;">'
         '<a href="{{ c.url }}" target="_blank" rel="noopener" style="@A@ font-weight: 600;">{{ c.label }}</a><span style="{{ c.pStyle }}">{{ c.prov }}</span></span></sc-for>'
         '<sc-if value="{{ @V@.editorial }}" hint-placeholder-val="{{ false }}"><span style="{{ @V@.edStyle }}">Amplify&rsquo;s note</span></sc-if></div>')


def cites(v):
    return CITES.replace("@V@", v)


def note_cites(var):
    return ('<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 4px 8px; @SMALL@"><span style="font-weight: 800;">Source</span>'
            f'<sc-for list="{{{{ {var} }}}}" as="c" hint-placeholder-count="1"><a href="{{{{ c.url }}}}" target="_blank" rel="noopener" style="@A@ font-weight: 600;">{{{{ c.label }}}}</a><span style="{{{{ c.pStyle }}}}">{{{{ c.prov }}}}</span></sc-for></div>')


def screen():
    out = '''
        <sc-if value="{{ sParliament }}" hint-placeholder-val="{{ false }}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          <div>
            <div style="@EYEBROW@ color: oklch(var(--t3) 0.16 145);"><span aria-hidden="true" style="{{ icParliament }}"></span>Foundations</div>
            <h1 style="@H1@">Inside Parliament</h1>
            <p style="@LEDE@">{{ paLede }}</p>
            <p style="margin: 8px 0 0; @SMALL@">Every fact names its source: <span style="font-weight: 800;">Official</span> means checked on the official page itself, <span style="font-weight: 800;">Secondary</span> a reputable secondary source. Last checked {{ paChecked }}.</p>
          </div>
          <div role="tablist" aria-label="Inside Parliament" style="display: flex; flex-wrap: wrap; gap: 8px;">
            <sc-for list="{{ paTabs }}" as="t" hint-placeholder-count="6"><button type="button" role="tab" id="{{ t.tid }}" aria-controls="{{ t.pid }}" aria-selected="{{ t.sel }}" onClick="{{ t.go }}" onKeyDown="{{ t.key }}" style="{{ t.style }}"><span aria-hidden="true" style="{{ t.icon }}"></span>{{ t.label }}</button></sc-for>
          </div>

          <sc-if value="{{ paTime }}" hint-placeholder-val="{{ true }}">
          <div role="tabpanel" id="pa-panel-time" aria-labelledby="pa-tab-time" class="amp-pa-panel" style="display: flex; flex-direction: column; gap: 16px;">
            <section style="@PANEL@"><h2 style="@H2@">The parliamentary year</h2>
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 240px), 1fr)); gap: 8px;"><sc-for list="{{ paYear }}" as="x" hint-placeholder-count="5"><div style="@CARD@"><div style="font-size: 14.5px; font-weight: 900;">{{ x.t }}</div><div style="font-size: 13.5px; line-height: 1.55;">{{ x.d }}</div>''' + cites("x") + '''</div></sc-for></div></section>
            <section style="@PANEL@"><h2 style="@H2@">The sitting week at a glance</h2>
              <p style="margin: 0 0 10px; @SMALL@">{{ paChartNote }}</p>
              <figure style="margin: 0;" aria-label="Normal sitting hours of the House of Commons and the House of Lords, Monday to Friday">
                <div style="position: relative; height: 18px; margin: 0 0 4px 62px; @SMALL@" aria-hidden="true"><sc-for list="{{ paChartTicks }}" as="k" hint-placeholder-count="5"><span style="{{ k.style }}">{{ k.t }}</span></sc-for></div>
                <ul style="list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 8px;"><sc-for list="{{ paChart }}" as="d" hint-placeholder-count="5"><li style="display: grid; grid-template-columns: 54px minmax(0, 1fr); gap: 8px; align-items: center;">
                  <span style="font-family: 'Space Mono', monospace; font-size: 12px; font-weight: 700;">{{ d.day }}</span>
                  <div style="display: flex; flex-direction: column; gap: 3px;">
                    <div style="position: relative; height: 14px; border-radius: 6px; background: rgb(var(--film-rgb) / 0.06);"><sc-if value="{{ d.c.has }}" hint-placeholder-val="{{ true }}"><span style="{{ d.c.style }}"></span></sc-if><span class="amp-sr">Commons {{ d.c.label }}</span></div>
                    <div style="position: relative; height: 14px; border-radius: 6px; background: rgb(var(--film-rgb) / 0.06);"><sc-if value="{{ d.l.has }}" hint-placeholder-val="{{ true }}"><span style="{{ d.l.style }}"></span></sc-if><span class="amp-sr">Lords {{ d.l.label }}</span></div>
                  </div></li></sc-for></ul>
                <figcaption style="display: flex; flex-wrap: wrap; gap: 6px 16px; margin-top: 10px; @SMALL@"><span><span aria-hidden="true" style="display: inline-block; width: 12px; height: 12px; border-radius: 3px; vertical-align: -1px; background: oklch(var(--t2) 0.15 145 / 0.85);"></span> House of Commons (upper bar)</span><span><span aria-hidden="true" style="display: inline-block; width: 12px; height: 12px; border-radius: 3px; vertical-align: -1px; background: oklch(var(--t2) 0.15 300 / 0.85);"></span> House of Lords (lower bar)</span></figcaption>
              </figure>
              <div style="margin-top: 8px;">''' + note_cites("paChartCites") + '''</div>
            </section>
            <section style="@PANEL@"><h2 style="@H2@">Sitting hours, in full</h2>
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr)); gap: 8px;"><sc-for list="{{ paWeek }}" as="g" hint-placeholder-count="3"><div style="@CARD@"><span style="{{ g.hStyle }} align-self: flex-start;">{{ g.house }}</span>
                <sc-for list="{{ g.rows }}" as="r" hint-placeholder-count="3"><div style="display: flex; flex-direction: column; gap: 2px; padding-top: 6px; border-top: 1px solid rgb(var(--film-rgb) / 0.08);"><span style="font-size: 13.5px; font-weight: 800;">{{ r.day }}</span><span style="font-size: 13.5px;">{{ r.hours }}</span></div></sc-for></div></sc-for></div>
              <p style="margin: 10px 0 6px; font-size: 13.5px; line-height: 1.55;">{{ paWeekNote }}</p>''' + note_cites("paWeekNoteCites") + '''
            </section>
            <section style="@PANEL@"><h2 style="@H2@">A Commons sitting day, in order</h2>
              <ol class="amp-pa-tl" style="margin: 0; list-style: none; display: flex; flex-direction: column; gap: 10px;"><sc-for list="{{ paDay }}" as="x" hint-placeholder-count="6"><li style="@CARD@"><div style="display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 10px;"><span style="@LABEL@">{{ x.when }}</span><span style="font-size: 14.5px; font-weight: 900;">{{ x.what }}</span></div><div style="font-size: 13.5px; line-height: 1.55;">{{ x.d }}</div>''' + cites("x") + '''</li></sc-for></ol></section>
            <section style="@PANEL@"><h2 style="@H2@">How to read the <span data-tip="term:orderpaper" tabindex="0" style="text-decoration: underline dotted; text-underline-offset: 3px;">Order Paper</span></h2>
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 240px), 1fr)); gap: 8px;"><sc-for list="{{ paOP }}" as="x" hint-placeholder-count="5"><div style="@CARD@"><div style="font-size: 14.5px; font-weight: 900;">{{ x.part }}</div><div style="font-size: 13.5px; line-height: 1.55;">{{ x.d }}</div>''' + cites("x") + '''</div></sc-for></div></section>
          </div>
          </sc-if>

          <sc-if value="{{ paLife }}" hint-placeholder-val="{{ false }}">
          <div role="tabpanel" id="pa-panel-life" aria-labelledby="pa-tab-life" class="amp-pa-panel" style="display: flex; flex-direction: column; gap: 16px;">
            <section style="@PANEL@"><h2 style="@H2@">A Member of Youth Parliament, an MP and a peer, side by side</h2><p style="margin: 0 0 12px; @SMALL@">{{ paLifeIntro }}</p>
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr)); gap: 10px;"><sc-for list="{{ paLifeCards }}" as="x" hint-placeholder-count="3"><article style="@CARD@ {{ x.top }}">
                <h3 style="margin: 0; font-size: 16px; font-weight: 900;">{{ x.role }}</h3>
                <div><div style="@LABEL@">Who</div><div style="font-size: 13.5px; line-height: 1.55;">{{ x.who }}</div></div>
                <div><div style="@LABEL@">Time</div><div style="font-size: 13.5px; line-height: 1.55;">{{ x.time }}</div></div>
                <div><div style="@LABEL@">Where</div><div style="font-size: 13.5px; line-height: 1.55;">{{ x.where }}</div></div>
                <div><div style="@LABEL@">What fills the days</div><ul style="margin: 2px 0 0; padding-left: 18px; font-size: 13.5px; line-height: 1.5;"><sc-for list="{{ x.rhythm }}" as="r" hint-placeholder-count="3"><li>{{ r.t }}</li></sc-for></ul></div>
                <a href="{{ x.ownUrl }}" target="_blank" rel="noopener" style="@A@ font-size: 13.5px;">{{ x.own }}</a>''' + cites("x") + '''</article></sc-for></div></section>
          </div>
          </sc-if>

          <sc-if value="{{ paRoles }}" hint-placeholder-val="{{ false }}">
          <div role="tabpanel" id="pa-panel-roles" aria-labelledby="pa-tab-roles" class="amp-pa-panel" style="display: flex; flex-direction: column; gap: 16px;">
            <section style="@PANEL@"><h2 style="@H2@">Who keeps Parliament working</h2>
              <p style="margin: 0 0 10px; @SMALL@">Roles, not names: who holds each role changes, so each card links to the official page that says who holds it now. Showing {{ paRoleShown }} of {{ paRoleTotal }}.</p>
              <label style="display: flex; flex-wrap: wrap; align-items: center; gap: 6px; font-size: 12.5px; margin-bottom: 10px;">House <select value="{{ paHouse }}" onChange="{{ setPaHouse }}" style="@SEL@"><option value="All">All</option><option value="Commons">Commons</option><option value="Lords">Lords</option></select></label>
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr)); gap: 8px;"><sc-for list="{{ paRoleCards }}" as="x" hint-placeholder-count="8"><article style="@CARD@">
                <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 6px 10px;"><h3 style="margin: 0; font-size: 15px; font-weight: 900;">{{ x.role }}</h3><span style="{{ x.hStyle }}">{{ x.house }}</span></div>
                <div style="font-size: 13.5px; line-height: 1.55;">{{ x.d }}</div>
                <div style="font-size: 13px; line-height: 1.5;"><span style="font-weight: 800;">Why it matters to you:</span> {{ x.youth }}</div>
                <a href="{{ x.who }}" target="_blank" rel="noopener" style="@A@ font-size: 13px;">Who holds this role now</a>''' + cites("x") + '''</article></sc-for></div></section>
          </div>
          </sc-if>

          <sc-if value="{{ paBuilding }}" hint-placeholder-val="{{ false }}">
          <div role="tabpanel" id="pa-panel-building" aria-labelledby="pa-tab-building" class="amp-pa-panel" style="display: flex; flex-direction: column; gap: 16px;">
            <section style="@PANEL@"><h2 style="@H2@">From the fire of 1834 to Restoration and Renewal</h2>
              <ol class="amp-pa-tl" style="margin: 0; list-style: none; display: flex; flex-direction: column; gap: 10px;"><sc-for list="{{ paBuild }}" as="x" hint-placeholder-count="8"><li style="@CARD@"><span style="@LABEL@">{{ x.date }}</span><div style="font-size: 13.5px; line-height: 1.55;">{{ x.what }}</div>''' + cites("x") + '''</li></sc-for></ol>
              <p style="margin: 12px 0 6px; font-size: 13.5px; line-height: 1.55;">{{ paBuildNote }}</p>''' + note_cites("paBuildNoteCites") + '''</section>
          </div>
          </sc-if>

          <sc-if value="{{ paRulesTab }}" hint-placeholder-val="{{ false }}">
          <div role="tabpanel" id="pa-panel-rules" aria-labelledby="pa-tab-rules" class="amp-pa-panel" style="display: flex; flex-direction: column; gap: 16px;">
            <section style="@PANEL@"><h2 style="@H2@">Who changes the rules</h2><p style="margin: 0 0 12px; @SMALL@">{{ paRulesIntro }}</p>
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr)); gap: 8px;"><sc-for list="{{ paRules }}" as="x" hint-placeholder-count="5"><div style="@CARD@"><div style="font-size: 14.5px; font-weight: 900;">{{ x.t }}</div><div style="font-size: 13.5px; line-height: 1.55;">{{ x.d }}</div>''' + cites("x") + '''</div></sc-for></div></section>
          </div>
          </sc-if>

          <sc-if value="{{ paGo }}" hint-placeholder-val="{{ false }}">
          <div role="tabpanel" id="pa-panel-go" aria-labelledby="pa-tab-go" class="amp-pa-panel" style="display: flex; flex-direction: column; gap: 16px;">
            <section style="@PANEL@"><h2 style="@H2@">Use it in your campaign</h2>
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 240px), 1fr)); gap: 8px;"><sc-for list="{{ paUse }}" as="x" hint-placeholder-count="7"><div style="@CARD@"><div style="font-size: 14.5px; font-weight: 900;">{{ x.t }}</div><div style="font-size: 13.5px; line-height: 1.55;">{{ x.d }}</div>
                <div style="display: flex; flex-wrap: wrap; gap: 6px 14px; font-size: 13px;"><sc-if value="{{ x.hasScreen }}" hint-placeholder-val="{{ false }}"><button type="button" onClick="{{ x.go }}" style="@BTN@">Open {{ x.screenLabel }}</button></sc-if><sc-if value="{{ x.hasUrl }}" hint-placeholder-val="{{ false }}"><a href="{{ x.url }}" target="_blank" rel="noopener" style="@A@">Go to the official page</a></sc-if></div>''' + cites("x") + '''</div></sc-for></div></section>
            <section style="@PANEL@"><h2 style="@H2@">Related campaigns, themes and topics</h2><p style="margin: 0 0 10px; @SMALL@">{{ paRelIntro }} Showing {{ paRelShown }} of {{ paRelTotal }}.</p>
              <label style="display: flex; flex-wrap: wrap; align-items: center; gap: 6px; font-size: 12.5px; margin-bottom: 10px;">Where it lives <select value="{{ paRel }}" onChange="{{ setPaRel }}" style="@SEL@"><sc-for list="{{ paRelOpts }}" as="o" hint-placeholder-count="4"><option value="{{ o.v }}">{{ o.label }}</option></sc-for></select></label>
              <ul style="list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 6px;"><sc-for list="{{ paRelItems }}" as="x" hint-placeholder-count="6"><li style="@CARD@ flex-direction: row; flex-wrap: wrap; align-items: center; gap: 6px 10px;"><span style="@LABEL@">{{ x.kind }}</span><span style="flex: 1 1 260px; min-width: 0; font-size: 13.5px; font-weight: 700;">{{ x.t }}</span><span style="{{ x.sStyle }}">{{ x.status }}</span><sc-if value="{{ x.hasScreen }}" hint-placeholder-val="{{ false }}"><button type="button" onClick="{{ x.go }}" style="@BTN@">{{ x.screenLabel }}</button></sc-if></li></sc-for></ul></section>
          </div>
          </sc-if>

          <section style="@PANEL@"><h2 style="@H2@">Sources for this screen</h2><p style="margin: 0 0 10px; @SMALL@">{{ paSrcN }} sources, {{ paSrcV }} of them official pages. {{ paRule }}</p>
            <ul style="margin: 0; padding-left: 18px; display: flex; flex-direction: column; gap: 4px; font-size: 13px; line-height: 1.5;"><sc-for list="{{ paSources }}" as="x" hint-placeholder-count="6"><li><a href="{{ x.url }}" target="_blank" rel="noopener" style="@A@ font-weight: 600;">{{ x.label }}</a> <span style="{{ x.pStyle }}">{{ x.prov }}</span> <span style="@SMALL@">checked {{ x.checked }}</span></li></sc-for></ul></section>
        </div>
        </sc-if>
'''
    for k, v in (("@PANEL@", PANEL), ("@H2@", H2), ("@CARD@", CARD), ("@SMALL@", SMALL), ("@LABEL@", LABEL), ("@SEL@", SEL), ("@BTN@", BTN),
                 ("@A@", A), ("@EYEBROW@", EYEBROW), ("@H1@", H1), ("@LEDE@", LEDE)):
        out = out.replace(k, v)
    return out


STATE = '      ["state", "Anatomy of the state", "sq", 145, 6, "NEW", "parliament government departments devolved local authority arms length civil society layers levers"],'
NAV11 = '\n      ["parliament", "Inside Parliament", "sq", 145, 6, "NEW", "inside parliament day in the life MP MYP peer lords commons speaker whips order paper sitting hours parliamentary year week day building palace westminster 1834 fire procedure committee rules"],'


def transforms():
    return [
        ("ext11-load", "the Inside Parliament data loads with the rest", '"./data/glossary.json", "./data/product.json"].map(get));', '"./data/glossary.json", "./data/product.json", "./data/parliament.json"].map(get));', 1),
        ("ext11-load-vars", "name it", "cm, tt, iv, rs, sd, rd, gl, pd] =", "cm, tt, iv, rs, sd, rd, gl, pd, pa] =", 1),
        ("ext11-load-state", "keep it in state", "cm, tt, iv, rs, sd, rd, gl, pd, loaded", "cm, tt, iv, rs, sd, rd, gl, pd, pa, loaded", 1),
        ("ext11-nav", "Inside Parliament sits after Anatomy of the state in Foundations", STATE, STATE + NAV11, 1),
        ("ext11-hash", "the screen can be linked to", "|golive|product|notify)$/.test(id)", "|golive|product|notify|parliament)$/.test(id)", 1),
        ("ext11-icon", "its drawer icon", 'research: "pencil-ruler" };', 'research: "pencil-ruler", parliament: "vote" };', 1),
        ("ext11-css", "tab panel motion (reduced-motion safe) and the timeline rule", "  .amp-sr {", CSS11 + "\n  .amp-sr {", 1),
        ("ext11-logic", "Inside Parliament values", "  async loadPetition() {", LOGIC11 + "\n  async loadPetition() {", 1),
        ("ext11-vals", "its values join renderVals", "...this.ampVals9(s),", "...this.ampVals9(s), ...this.ampVals11(s),", 1),
        ("ext11-screen", "the Inside Parliament screen", '        <div data-slot="portal-end" style="display: none;"></div>', screen() + '\n        <div data-slot="portal-end" style="display: none;"></div>', 1),
    ]
