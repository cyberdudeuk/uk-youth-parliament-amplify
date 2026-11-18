"""Twelfth set of portal extensions: Every way to take part (17 November 2026).

  civic   A new Foundations screen on young people's political and civic participation, in seven tabs: By age (what
          opens up at each age, filterable by nation), Vote (ages by nation, registering, voter ID, why it matters),
          Stand and serve (candidacy, trustee, governor, jury), Influence (MPs, peers, committee evidence in three
          legislatures, consultations, citizens' assemblies, participatory budgeting), How laws are made, Civic life
          (volunteering, protest rights by nation with safeguarding, UNCRC Article 12) and Gaps (a register of
          participation gaps and where Amplify stands on each, filterable by domain and status).

          It is drawn by a generic sourced-screen engine: data/civic.json holds tabs and typed sections (ladder,
          table, steps, cards, gaps), each fact with source ids and V or S provenance. A new sourced screen can reuse
          the engine by adding a data file. check_site S21 now covers every sourced screen (Inside Parliament and
          this one) with the same rules, and adds two for the engine: every section belongs to a real tab and has a
          known type, and every age-ladder item says which nation it applies to (defect D37: an age rule shown
          without its nation is wrong for three nations out of four).
"""
import json, os

from extend import PANEL, LABEL, SMALL, EYEBROW, H1, LEDE
from extend4 import H2, CARD
from extend11 import A, SEL, BTN, CITES

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TYPES = ("ladder", "table", "steps", "cards", "gaps")


def data():
    with open(os.path.join(R, "data", "civic.json"), encoding="utf-8") as f:
        return json.load(f)


LOGIC12 = r'''
  ampVals12(s) {
    const A = s.amp || {}, cv = A.cv || {};
    const arr = (x) => (Array.isArray(x) ? x : []);
    const tabs = arr(cv.tabs), ids = tabs.map((t) => t.id), tab = ids.indexOf(s.cvTab) >= 0 ? s.cvTab : (ids[0] || "age");
    const SRC = {}; arr(cv.sources).forEach((x) => { SRC[x.id] = x; });
    const pill = (h) => "display:inline-block;border-radius:999px;padding:1px 8px;font-family:'Space Mono',monospace;font-size:10.5px;font-weight:700;background:oklch(var(--t1) 0.16 " + h + " / 0.28);color:oklch(var(--t4) 0.15 " + h + ");";
    const cite = (list) => arr(list).map((id) => { const x = SRC[id] || {}; const off = x.provenance === "V";
      return { label: x.label || id, url: x.url || "#", prov: off ? "Official" : "Secondary", pStyle: pill(off ? 145 : 70) }; });
    const L = {}; this.GROUPS.forEach(([g, items]) => items.forEach(([id, lbl]) => { L[id] = lbl; }));
    const go = (id) => () => this.setState({ screen: id }, () => { try { window.scrollTo(0, 0); } catch (e) { /* no window */ } });
    const link = (x) => ({ hasScreen: !!(x.screen && x.screen !== "civic" && L[x.screen]), screenLabel: L[x.screen] || "", go: go(x.screen), hasUrl: !!x.url, url: x.url || "#" });
    const nat = s.cvNation || "All", dom = s.cvDomain || "All", st = s.cvStatus || "All";
    const fits = (where) => nat === "All" || arr(where).some((w) => w === nat || w === "UK" || (w === "England and Wales" && (nat === "England" || nat === "Wales")));
    const NH = { UK: 175, England: 25, Scotland: 215, Wales: 145, "Northern Ireland": 70, "England and Wales": 300 };
    const SH = { Partly: 70, Next: 215, "On Amplify": 145 };
    const keyNav = (e) => { const cur = ((e.currentTarget && e.currentTarget.id) || "").replace("cv-tab-", ""); let i = ids.indexOf(cur) >= 0 ? ids.indexOf(cur) : ids.indexOf(tab); if (i < 0) return;
      if (e.key === "ArrowRight") i = (i + 1) % ids.length; else if (e.key === "ArrowLeft") i = (i - 1 + ids.length) % ids.length;
      else if (e.key === "Home") i = 0; else if (e.key === "End") i = ids.length - 1; else return;
      e.preventDefault(); this.setState({ cvTab: ids[i] }, () => { const b = document.getElementById("cv-tab-" + ids[i]); if (b) b.focus(); }); };
    const sections = arr(cv.sections).filter((x) => x.tab === tab).map((x, n) => {
      const base = { key: tab + "-" + n, h: x.h || "", intro: x.intro || "", hasIntro: !!x.intro, note: x.note || "", hasNote: !!x.note, cites: cite(x.src), hasCites: arr(x.src).length > 0,
        isLadder: x.type === "ladder", isTable: x.type === "table", isSteps: x.type === "steps", isCards: x.type === "cards", isGaps: x.type === "gaps" };
      if (x.type === "ladder") {
        const shown = arr(x.items).filter((it) => fits(it.where));
        base.items = shown.map((it) => ({ age: it.age, t: it.t, d: it.d, where: arr(it.where).map((w) => ({ w, style: pill(NH[w] || 175) })), cites: cite(it.src), editorial: !!it.editorial, edStyle: pill(300), ...link(it) }));
        base.shown = String(shown.length); base.total = String(arr(x.items).length);
      } else if (x.type === "table") {
        const cols = arr(x.cols);
        base.rows = arr(x.rows).map((r) => ({ head: r[0], cells: cols.slice(1).map((c, i) => ({ c, v: r[i + 1] })) }));
      } else if (x.type === "gaps") {
        const all = arr(x.items), shown = all.filter((it) => (dom === "All" || it.domain === dom) && (st === "All" || it.status === st));
        base.items = shown.map((it) => ({ t: it.t, domain: it.domain, status: it.status, sStyle: pill(SH[it.status] || 175), dStyle: pill(it.domain === "Political" ? 25 : 175), ...link(it) }));
        base.shown = String(shown.length); base.total = String(all.length);
        base.counts = Array.from(new Set(all.map((it) => it.status))).map((k) => ({ k, n: String(all.filter((it) => it.status === k).length), style: pill(SH[k] || 175) }));
        base.domOpts = ["All"].concat(Array.from(new Set(all.map((it) => it.domain)))).map((v) => ({ v }));
        base.stOpts = ["All"].concat(Array.from(new Set(all.map((it) => it.status)))).map((v) => ({ v }));
      } else {
        base.items = arr(x.items).map((it, i) => ({ n: String(i + 1), t: it.t, d: it.d, cites: cite(it.src), editorial: !!it.editorial, edStyle: pill(300), ...link(it) }));
      }
      return base;
    });
    return {
      sCivic: s.screen === "civic",
      icCivic: this.ampIcon("heart-handshake", "oklch(var(--t3) 0.16 215)", 16),
      cvLede: cv.lede || "", cvChecked: cv.checked || "", cvRule: cv.rule || "",
      cvTabs: tabs.map((t) => ({ label: t.label, tid: "cv-tab-" + t.id, pid: "cv-panel", sel: tab === t.id ? "true" : "false", key: keyNav,
        icon: this.ampIcon(t.icon, tab === t.id ? "oklch(var(--t4) 0.15 215)" : "rgb(var(--ink-rgb) / 0.75)", 15),
        style: "display:inline-flex;align-items:center;gap:7px;min-height:40px;padding:8px 14px;border-radius:999px;cursor:pointer;font-size:13.5px;font-weight:800;border:1px solid " + (tab === t.id ? "oklch(var(--t2) 0.15 215 / 0.9);background:oklch(var(--t1) 0.16 215 / 0.3);color:rgb(var(--ink-rgb));" : "rgb(var(--film-rgb) / 0.2);background:transparent;color:rgb(var(--ink-rgb) / 0.86);"),
        go: () => this.setState({ cvTab: t.id }) })),
      cvTabLabel: (tabs.find((t) => t.id === tab) || {}).label || "", cvTabId: "cv-tab-" + tab,
      cvSections: sections,
      cvNation: nat, setCvNation: (e) => this.setState({ cvNation: e.target.value }), cvNatOpts: ["All"].concat(arr(cv.nations).filter((x) => x !== "UK" && x !== "England and Wales")).map((v) => ({ v })),
      cvDomain: dom, setCvDomain: (e) => this.setState({ cvDomain: e.target.value }), cvStatus: st, setCvStatus: (e) => this.setState({ cvStatus: e.target.value }),
      cvSources: arr(cv.sources).map((x) => ({ label: x.label, url: x.url, prov: x.provenance === "V" ? "Official" : "Secondary", pStyle: pill(x.provenance === "V" ? 145 : 70), checked: x.checked })),
      cvSrcN: String(arr(cv.sources).length), cvSrcV: String(arr(cv.sources).filter((x) => x.provenance === "V").length)
    };
  }
'''

CSS12 = '''
  .amp-cv-panel { animation: none; }
  @media (prefers-reduced-motion: no-preference) { .amp-cv-panel { animation: ampPaIn 0.28s ease-out; } }
  .amp-cv-age { flex: 0 0 auto; min-width: 72px; text-align: center; border-radius: 12px; padding: 6px 8px; font-family: 'Space Mono', monospace; font-size: 13px; font-weight: 700; background: oklch(var(--t1) 0.16 215 / 0.3); }
'''


def cites(v):
    return CITES.replace("@V@", v)


def links(v):
    return (f'<div style="display: flex; flex-wrap: wrap; gap: 6px 14px; font-size: 13px;"><sc-if value="{{{{ {v}.hasScreen }}}}" hint-placeholder-val="{{{{ false }}}}"><button type="button" onClick="{{{{ {v}.go }}}}" style="@BTN@">Open {{{{ {v}.screenLabel }}}}</button></sc-if>'
            f'<sc-if value="{{{{ {v}.hasUrl }}}}" hint-placeholder-val="{{{{ false }}}}"><a href="{{{{ {v}.url }}}}" target="_blank" rel="noopener" style="@A@">Go to the official page</a></sc-if></div>')


def screen():
    out = '''
        <sc-if value="{{ sCivic }}" hint-placeholder-val="{{ false }}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          <div>
            <div style="@EYEBROW@ color: oklch(var(--t3) 0.16 215);"><span aria-hidden="true" style="{{ icCivic }}"></span>Foundations</div>
            <h1 style="@H1@">Every way to take part</h1>
            <p style="@LEDE@">{{ cvLede }}</p>
            <p style="margin: 8px 0 0; @SMALL@">Every fact names its source: <span style="font-weight: 800;">Official</span> means a government, Parliament, regulator or council page, <span style="font-weight: 800;">Secondary</span> a reputable secondary source. Last checked {{ cvChecked }}. Not legal advice: check the official page before you act.</p>
          </div>
          <div role="tablist" aria-label="Every way to take part" style="display: flex; flex-wrap: wrap; gap: 8px;">
            <sc-for list="{{ cvTabs }}" as="t" hint-placeholder-count="7"><button type="button" role="tab" id="{{ t.tid }}" aria-controls="{{ t.pid }}" aria-selected="{{ t.sel }}" onClick="{{ t.go }}" onKeyDown="{{ t.key }}" style="{{ t.style }}"><span aria-hidden="true" style="{{ t.icon }}"></span>{{ t.label }}</button></sc-for>
          </div>
          <div role="tabpanel" id="cv-panel" aria-labelledby="{{ cvTabId }}" class="amp-cv-panel" style="display: flex; flex-direction: column; gap: 16px;">
            <sc-for list="{{ cvSections }}" as="sec" hint-placeholder-count="3"><section style="@PANEL@"><h2 style="@H2@">{{ sec.h }}</h2>
              <sc-if value="{{ sec.hasIntro }}" hint-placeholder-val="{{ false }}"><p style="margin: 0 0 10px; @SMALL@">{{ sec.intro }}</p></sc-if>

              <sc-if value="{{ sec.isLadder }}" hint-placeholder-val="{{ true }}">
                <label style="display: flex; flex-wrap: wrap; align-items: center; gap: 6px; font-size: 12.5px; margin-bottom: 10px;">Nation <select value="{{ cvNation }}" onChange="{{ setCvNation }}" style="@SEL@"><sc-for list="{{ cvNatOpts }}" as="o" hint-placeholder-count="5"><option value="{{ o.v }}">{{ o.v }}</option></sc-for></select> <span style="@SMALL@">Showing {{ sec.shown }} of {{ sec.total }}</span></label>
                <ol style="list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 8px;"><sc-for list="{{ sec.items }}" as="x" hint-placeholder-count="6"><li style="@CARD@ flex-direction: row; flex-wrap: wrap; align-items: flex-start; gap: 10px 14px;">
                  <span class="amp-cv-age">{{ x.age }}</span>
                  <div style="flex: 1 1 280px; min-width: 0; display: flex; flex-direction: column; gap: 6px;">
                    <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 6px 10px;"><span style="font-size: 14.5px; font-weight: 900;">{{ x.t }}</span><sc-for list="{{ x.where }}" as="w" hint-placeholder-count="2"><span style="{{ w.style }}">{{ w.w }}</span></sc-for></div>
                    <div style="font-size: 13.5px; line-height: 1.55;">{{ x.d }}</div>''' + links("x") + cites("x") + '''
                  </div></li></sc-for></ol>
              </sc-if>

              <sc-if value="{{ sec.isTable }}" hint-placeholder-val="{{ false }}">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 230px), 1fr)); gap: 8px;"><sc-for list="{{ sec.rows }}" as="r" hint-placeholder-count="4"><div style="@CARD@"><h3 style="margin: 0; font-size: 15.5px; font-weight: 900;">{{ r.head }}</h3>
                  <dl style="margin: 0; display: flex; flex-direction: column; gap: 6px;"><sc-for list="{{ r.cells }}" as="c" hint-placeholder-count="4"><div><dt style="@LABEL@">{{ c.c }}</dt><dd style="margin: 2px 0 0; font-size: 14px; font-weight: 700;">{{ c.v }}</dd></div></sc-for></dl></div></sc-for></div>
              </sc-if>

              <sc-if value="{{ sec.isSteps }}" hint-placeholder-val="{{ false }}">
                <ol class="amp-pa-tl" style="margin: 0; list-style: none; display: flex; flex-direction: column; gap: 10px;"><sc-for list="{{ sec.items }}" as="x" hint-placeholder-count="5"><li style="@CARD@"><div style="display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 10px;"><span style="@LABEL@">Step {{ x.n }}</span><span style="font-size: 14.5px; font-weight: 900;">{{ x.t }}</span></div><div style="font-size: 13.5px; line-height: 1.55;">{{ x.d }}</div>''' + links("x") + cites("x") + '''</li></sc-for></ol>
              </sc-if>

              <sc-if value="{{ sec.isCards }}" hint-placeholder-val="{{ false }}">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr)); gap: 8px;"><sc-for list="{{ sec.items }}" as="x" hint-placeholder-count="4"><div style="@CARD@"><div style="font-size: 14.5px; font-weight: 900;">{{ x.t }}</div><div style="font-size: 13.5px; line-height: 1.55;">{{ x.d }}</div>''' + links("x") + cites("x") + '''</div></sc-for></div>
              </sc-if>

              <sc-if value="{{ sec.isGaps }}" hint-placeholder-val="{{ false }}">
                <div style="display: flex; flex-wrap: wrap; gap: 8px 18px; align-items: center; margin-bottom: 10px;">
                  <label style="display: flex; flex-wrap: wrap; align-items: center; gap: 6px; font-size: 12.5px;">Domain <select value="{{ cvDomain }}" onChange="{{ setCvDomain }}" style="@SEL@"><sc-for list="{{ sec.domOpts }}" as="o" hint-placeholder-count="3"><option value="{{ o.v }}">{{ o.v }}</option></sc-for></select></label>
                  <label style="display: flex; flex-wrap: wrap; align-items: center; gap: 6px; font-size: 12.5px;">Status <select value="{{ cvStatus }}" onChange="{{ setCvStatus }}" style="@SEL@"><sc-for list="{{ sec.stOpts }}" as="o" hint-placeholder-count="4"><option value="{{ o.v }}">{{ o.v }}</option></sc-for></select></label>
                  <sc-for list="{{ sec.counts }}" as="c" hint-placeholder-count="3"><span style="font-size: 13px;"><span style="{{ c.style }}">{{ c.k }}</span> {{ c.n }}</span></sc-for>
                  <span style="@SMALL@">Showing {{ sec.shown }} of {{ sec.total }}</span>
                </div>
                <ul style="list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 6px;"><sc-for list="{{ sec.items }}" as="x" hint-placeholder-count="8"><li style="@CARD@ flex-direction: row; flex-wrap: wrap; align-items: center; gap: 6px 10px;"><span style="{{ x.dStyle }}">{{ x.domain }}</span><span style="flex: 1 1 260px; min-width: 0; font-size: 13.5px; font-weight: 700;">{{ x.t }}</span><span style="{{ x.sStyle }}">{{ x.status }}</span><sc-if value="{{ x.hasScreen }}" hint-placeholder-val="{{ false }}"><button type="button" onClick="{{ x.go }}" style="@BTN@">{{ x.screenLabel }}</button></sc-if></li></sc-for></ul>
              </sc-if>

              <sc-if value="{{ sec.hasNote }}" hint-placeholder-val="{{ false }}"><p style="margin: 10px 0 0; font-size: 13.5px; line-height: 1.55;">{{ sec.note }}</p></sc-if>
              <sc-if value="{{ sec.hasCites }}" hint-placeholder-val="{{ false }}"><div style="margin-top: 8px; display: flex; flex-wrap: wrap; align-items: center; gap: 4px 8px; @SMALL@"><span style="font-weight: 800;">Source</span><sc-for list="{{ sec.cites }}" as="c" hint-placeholder-count="2"><a href="{{ c.url }}" target="_blank" rel="noopener" style="@A@ font-weight: 600;">{{ c.label }}</a><span style="{{ c.pStyle }}">{{ c.prov }}</span></sc-for></div></sc-if>
            </section></sc-for>
          </div>

          <section style="@PANEL@"><h2 style="@H2@">Sources for this screen</h2><p style="margin: 0 0 10px; @SMALL@">{{ cvSrcN }} sources, {{ cvSrcV }} of them official pages. {{ cvRule }}</p>
            <ul style="margin: 0; padding-left: 18px; display: flex; flex-direction: column; gap: 4px; font-size: 13px; line-height: 1.5;"><sc-for list="{{ cvSources }}" as="x" hint-placeholder-count="6"><li><a href="{{ x.url }}" target="_blank" rel="noopener" style="@A@ font-weight: 600;">{{ x.label }}</a> <span style="{{ x.pStyle }}">{{ x.prov }}</span> <span style="@SMALL@">checked {{ x.checked }}</span></li></sc-for></ul></section>
        </div>
        </sc-if>
'''
    for k, v in (("@PANEL@", PANEL), ("@H2@", H2), ("@CARD@", CARD), ("@SMALL@", SMALL), ("@LABEL@", LABEL), ("@SEL@", SEL), ("@BTN@", BTN),
                 ("@A@", A), ("@EYEBROW@", EYEBROW), ("@H1@", H1), ("@LEDE@", LEDE)):
        out = out.replace(k, v)
    return out


ANCHOR = '\n      ["parliament", "Inside Parliament", "sq", 145, 6, "NEW",'
NAV12 = '\n      ["civic", "Every way to take part", "dot", 215, 7, "NEW", "take part civic political participation vote register voter id age ladder stand for election trustee governor jury write to MP peer evidence consultation citizens assembly participatory budgeting bill law volunteering protest rights UNCRC gaps"],'


def transforms():
    return [
        ("ext12-load", "the civic data loads with the rest", '"./data/parliament.json"].map(get));', '"./data/parliament.json", "./data/civic.json"].map(get));', 1),
        ("ext12-load-vars", "name it", "gl, pd, pa] =", "gl, pd, pa, cv] =", 1),
        ("ext12-load-state", "keep it in state", "gl, pd, pa, loaded", "gl, pd, pa, cv, loaded", 1),
        ("ext12-nav", "Every way to take part sits before Inside Parliament in Foundations", ANCHOR, NAV12 + ANCHOR, 1),
        ("ext12-hash", "the screen can be linked to", "|notify|parliament)$/.test(id)", "|notify|parliament|civic)$/.test(id)", 1),
        ("ext12-icon", "its drawer icon", 'parliament: "vote" };', 'parliament: "vote", civic: "heart-handshake" };', 1),
        ("ext12-css", "panel motion (reduced-motion safe) and the age badge", "  .amp-sr {", CSS12 + "\n  .amp-sr {", 1),
        ("ext12-logic", "Every way to take part values", "  async loadPetition() {", LOGIC12 + "\n  async loadPetition() {", 1),
        ("ext12-vals", "its values join renderVals", "...this.ampVals11(s),", "...this.ampVals11(s), ...this.ampVals12(s),", 1),
        ("ext12-screen", "the Every way to take part screen", '        <div data-slot="portal-end" style="display: none;"></div>', screen() + '\n        <div data-slot="portal-end" style="display: none;"></div>', 1),
    ]
