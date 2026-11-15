"""Fourth set of portal extensions: tooltips and explainers for every persona, and the Get involved group.

  tooltips     One accessible tooltip for the whole page, outside the React tree, shown on hover or keyboard focus of
               anything marked data-tip (every drawer item, the header controls and terms in the new screens). It stays
               while the pointer is over it, Escape closes it, and it never covers what it explains (WCAG 1.4.13).
  explainer    A bar on every screen saying what the screen is for, tailored to the persona the reader picks. The pick
               stays on the device (browser storage inside try/catch, with an in-memory fallback) and is never sent.
  involve      Ways to help build, check and look after the portal, by time and skill, with the contribution rules
  ambassadors  Supporter, champion and ambassador levels; a pilot until the owner confirms it can run safely (O12)
  campaign     Posters, a social card and badge drawn in code, template posts, an assembly script and key dates
  learn        Ready-to-run training sessions with audiences, timings, outcomes and the screens to use
  stem         The STEM spotlight: sourced facts, free opportunities by path, and a DevOps path built on this repo
All text comes from data/tooltips.json and data/involve.json; persona options are read from the data at build time
because an HTML parser drops anything inside a <select> that is not an <option>.
"""
import html
import json
import os

from extend import EYEBROW, H1, LEDE, PANEL, LABEL, SMALL, LINK

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGIC4 = r'''
  ampTipText(key) {
    const tt = (this.state.amp || {}).tt || {}, p = this.state.persona || "everyone";
    const [kind, id] = String(key || "").split(":");
    if (kind === "nav") { const e = (tt.screens || {})[id]; if (!e) return ""; const extra = (e.for || {})[p]; return e.tip + (extra ? " " + extra : ""); }
    if (kind === "term") { const e = (tt.terms || {})[id]; return e ? e.term + ": " + e.tip : ""; }
    if (kind === "ui") return (tt.ui || {})[id] || "";
    return "";
  }
  ampTipsOn() {
    if (this._tip || typeof document === "undefined") return;
    const el = document.createElement("div");
    el.id = "amp-tip"; el.setAttribute("role", "tooltip"); el.className = "amp-tip"; el.hidden = true;
    document.body.appendChild(el); this._tip = el;
    const hide = () => { if (this._tipFor) this._tipFor.removeAttribute("aria-describedby"); this._tipFor = null; el.hidden = true; };
    const show = (n) => {
      const text = this.ampTipText(n.getAttribute("data-tip"));
      if (!text) return hide();
      if (this._tipFor && this._tipFor !== n) this._tipFor.removeAttribute("aria-describedby");
      el.textContent = text; el.hidden = false; n.setAttribute("aria-describedby", "amp-tip"); this._tipFor = n;
      const r = n.getBoundingClientRect(), w = Math.min(320, window.innerWidth - 16);
      el.style.maxWidth = w + "px";
      if (String(n.getAttribute("data-tip")).indexOf("nav:") === 0 && r.right + 12 + w < window.innerWidth) {
        // drawer items: beside the item, so the tooltip never covers the items above or below it
        el.style.left = (r.right + 10) + "px"; el.style.top = Math.max(8, Math.min(r.top, window.innerHeight - el.offsetHeight - 8)) + "px";
      } else {
        const left = Math.max(8, Math.min(r.left, window.innerWidth - w - 8));
        const below = r.bottom + 8 + el.offsetHeight < window.innerHeight;
        el.style.left = left + "px"; el.style.top = (below ? r.bottom + 8 : Math.max(8, r.top - el.offsetHeight - 8)) + "px";
      }
    };
    const find = (t) => (t && t.closest ? t.closest("[data-tip]") : null);
    this._tipH = {
      over: (e) => { const n = find(e.target); if (n) show(n); },
      out: (e) => { const to = e.relatedTarget; if (this._tipFor && !(to && (this._tipFor.contains(to) || el.contains(to)))) hide(); },
      leave: (e) => { const to = e.relatedTarget; if (!(to && this._tipFor && this._tipFor.contains(to))) hide(); },
      focus: (e) => { const n = find(e.target); if (n) show(n); else hide(); },
      blur: () => hide(),
      key: (e) => { if (e.key === "Escape" && !el.hidden) hide(); },
      scroll: () => { const f = this._tipFor; if (f && document.activeElement === f) show(f); else hide(); }  // keep a focused trigger's tooltip (D12)
    };
    document.addEventListener("mouseover", this._tipH.over); document.addEventListener("mouseout", this._tipH.out);
    el.addEventListener("mouseleave", this._tipH.leave);
    document.addEventListener("focusin", this._tipH.focus); document.addEventListener("focusout", this._tipH.blur);
    document.addEventListener("keydown", this._tipH.key); window.addEventListener("scroll", this._tipH.scroll, true);
  }
  ampTipsOff() {
    if (!this._tip) return;
    const h = this._tipH;
    document.removeEventListener("mouseover", h.over); document.removeEventListener("mouseout", h.out);
    document.removeEventListener("focusin", h.focus); document.removeEventListener("focusout", h.blur);
    document.removeEventListener("keydown", h.key); window.removeEventListener("scroll", h.scroll, true);
    this._tip.remove(); this._tip = null;
  }
  ampPersona() { try { return window.localStorage.getItem("amp-persona") || "everyone"; } catch (e) { return "everyone"; } }
  ampVals4(s) {
    const A = s.amp || {}, tt = A.tt || { personas: [], screens: {}, terms: {} }, iv = A.iv || {};
    const inv = iv.involve || { ways: [], roles: [], rules: [], how: [] }, amb = iv.ambassadors || { tiers: [], promise: [], conduct: [] };
    const cp = iv.campaign || { assets: [], posts: [], hashtags: [], moments: [], assembly: { steps: [] } };
    const ln = iv.learn || { modules: [] }, st = iv.stem || { facts: [], paths: [], devops: { steps: [] } };
    const src = (A.src || { sources: [] }).sources, byId = {}; src.forEach((x) => { byId[x.id] = x; });
    const label = (id) => { try { return this.screenLabel(id) || id; } catch (e) { return id; } };
    const go = (id) => () => this.setState({ screen: id });
    const p = s.persona || "everyone", pe = (tt.personas || []).find((x) => x.id === p) || {};
    const scr = (tt.screens || {})[s.screen] || null, extra = scr && (scr.for || {})[p];
    const repo = iv.repo || "";
    const PV = { V: "Verified", S: "Search-sourced", K: "Lead, to confirm" };
    return {
      sInvolve: s.screen === "involve", sAmbassadors: s.screen === "ambassadors", sCampaign: s.screen === "campaign", sLearn: s.screen === "learn", sStem: s.screen === "stem",
      exShow: !!scr && !s.splash, exTip: scr ? scr.tip : "", exFor: extra || pe.lens || "", exHasFor: !!(extra || (p !== "everyone" && pe.lens)), exWho: pe.label || "Everyone",
      persona: p, setPersona: (e) => { const v = e.target.value; try { window.localStorage.setItem("amp-persona", v); } catch (err) { /* storage unavailable: keep it in memory */ } this.setState({ persona: v }); },
      ivIntro: inv.intro || "", ivRepo: repo, ivContrib: repo + "/blob/main/CONTRIBUTING.md", ivGood: repo + "/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22",
      ivWays: inv.ways.map((w) => ({ time: w.time, icon: this.ampIcon(w.icon, "oklch(var(--t3) 0.16 175)", 18), items: w.items.map((i) => ({ t: i.t, how: i.how, go: go(i.screen), where: label(i.screen) })) })),
      ivRoles: inv.roles, ivRules: inv.rules.map((t) => ({ t })), ivHow: inv.how.map((h, k) => ({ n: String(k + 1), s: h.s, d: h.d })),
      amStatus: amb.status || "", amIntro: amb.intro || "", amTiers: amb.tiers.map((t) => ({ tier: t.tier, who: t.who, time: t.time, does: t.does.map((d) => ({ d })) })),
      amPromise: amb.promise.map((t) => ({ t })), amConduct: amb.conduct.map((t) => ({ t })),
      amRegister: repo + "/issues/new?template=" + (amb.register || "ambassador.yml"),
      cpIntro: cp.intro || "", cpAssets: cp.assets.map((a) => ({ name: a.name, href: "./" + a.file, src: "./" + a.file, alt: a.alt })),
      cpPosts: cp.posts.map((x, k) => ({ channel: x.channel, text: x.text, copy: () => this.copy(x.text, "post" + k), copied: s.copied === "post" + k ? "Copied" : "Copy" })),
      cpSocial: cp.social_note || "", cpTags: (cp.hashtags || []).join("  "), cpTagNote: cp.hashtag_note || "",
      cpAsmTitle: (cp.assembly || {}).title || "", cpAsm: ((cp.assembly || {}).steps || []).map((t, k) => ({ n: String(k + 1), t })),
      cpMoments: cp.moments.map((m) => ({ when: m.when, what: m.what, prov: PV[m.prov] || m.prov })), cpMomNote: cp.moments_note || "",
      lnIntro: ln.intro || "",
      lnMods: ln.modules.map((m) => ({ id: m.id, t: m.t, who: m.who, mins: m.mins + " min", out: m.out.map((o) => ({ o })), steps: m.steps.map((x) => ({ x })), screens: m.screens.map((id) => ({ label: label(id), go: go(id) })) })),
      stIntro: st.intro || "", stNote: st.note || "", stDevIntro: (st.devops || {}).intro || "",
      stFacts: st.facts.map((f) => ({ f: f.f, src: f.src, url: f.url })),
      stPaths: st.paths.map((x) => ({ p: x.p, first: x.first, icon: this.ampIcon(x.icon, "oklch(var(--t3) 0.16 200)", 18),
        items: x.ids.map((id) => byId[id]).filter(Boolean).map((o) => ({ name: o.name, what: o.what, url: o.url, nations: o.nations.join(" · "), prov: PV[o.provenance] || o.provenance })) })),
      stDev: ((st.devops || {}).steps || []).map((x, k) => ({ n: String(k + 1), s: x.s, d: x.d, where: x.where })),
      icInvolve: this.ampIcon("git-pull-request", "oklch(var(--t3) 0.16 175)", 16), icAmb: this.ampIcon("award", "oklch(var(--t3) 0.16 70)", 16),
      icCamp: this.ampIcon("rocket", "oklch(var(--t3) 0.16 25)", 16), icLearn: this.ampIcon("presentation", "oklch(var(--t3) 0.16 300)", 16),
      icStem: this.ampIcon("cpu", "oklch(var(--t3) 0.16 200)", 16), icHelp: this.ampIcon("circle-help", "oklch(var(--t3) 0.16 215)", 16)
    };
  }
'''

TIP_CSS = '''
  .amp-tip { position: fixed; z-index: 90; padding: 9px 12px; border-radius: 12px; font: 600 13px/1.45 'Atkinson Hyperlegible', Chivo, sans-serif;
    color: #f3faf8; background: #0b1f1c; border: 1px solid rgba(94, 234, 212, 0.55); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35); pointer-events: auto; }
  .amp-tip[hidden] { display: none; }
  .amp-term { text-decoration: underline dotted; text-underline-offset: 3px; cursor: help; border-radius: 4px; }
  .amp-term:focus-visible { outline: 3px solid oklch(0.8 0.15 175); outline-offset: 2px; }
  body[data-motion="off"] .amp-tip { transition: none; }
'''


def term(key, text):
    return f'<span class="amp-term" tabindex="0" data-tip="term:{key}">{text}</span>'


def _personas():
    d = json.load(open(os.path.join(R, "data", "tooltips.json"), encoding="utf-8"))
    return "".join(f'<option value="{html.escape(p["id"])}">{html.escape(p["label"])}</option>' for p in d["personas"])


def explainer():
    return f'''
        <sc-if value="{{{{ exShow }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div role="note" aria-label="What this screen is for" class="amp-explainer" style="display: flex; flex-wrap: wrap; align-items: center; gap: 10px 14px; border-radius: 16px; padding: 10px 14px; border: 1px solid oklch(var(--t1) 0.16 215 / 0.45); background: oklch(var(--t1) 0.16 215 / 0.1); font-size: 13.5px; line-height: 1.5;">
          <span aria-hidden="true" style="{{{{ icHelp }}}}"></span>
          <span style="flex: 1 1 300px; min-width: 0;"><span style="font-weight: 800;">This screen:</span> {{{{ exTip }}}}<sc-if value="{{{{ exHasFor }}}}" hint-placeholder-val="{{{{ false }}}}"> <span style="color: rgb(var(--ink-rgb) / 0.8);">For {{{{ exWho }}}}: {{{{ exFor }}}}</span></sc-if></span>
          <label data-tip="ui:persona" style="display: flex; flex-wrap: wrap; align-items: center; gap: 6px 8px; flex: 0 1 auto; min-width: 0; max-width: 100%; font-size: 12.5px; color: rgb(var(--ink-rgb) / 0.8);">Explain for
            <select value="{{{{ persona }}}}" onChange="{{{{ setPersona }}}}" style="min-width: 0; max-width: 100%; min-height: 36px; border: 1px solid rgb(var(--film-rgb) / 0.2); border-radius: 10px; background: rgb(var(--film-rgb) / 0.05); color: rgb(var(--ink-rgb)); padding: 6px 10px; font-size: 13px;">{_personas()}</select>
          </label>
        </div>
        </sc-if>
'''


def head(icon, hue, title, lede):
    return f'''<div>
            <div style="{EYEBROW} color: oklch(var(--t3) 0.16 {hue});"><span aria-hidden="true" style="{{{{ {icon} }}}}"></span>Get involved</div>
            <h1 style="{H1}">{title}</h1>
            <p style="{LEDE}">{lede}</p>
          </div>'''


def ext(url_hole, label):
    return f'<a href="{{{{ {url_hole} }}}}" target="_blank" rel="noopener noreferrer" style="{LINK}">{label}<span aria-hidden="true" style="{{{{ icExt }}}}"></span><span class="amp-sr"> (opens in a new tab)</span></a>'


H2 = "margin: 0 0 10px; font-size: 17px; font-weight: 800;"
CARD = "border: 1px solid rgb(var(--film-rgb) / 0.1); border-radius: 16px; padding: 12px 14px; display: flex; flex-direction: column; gap: 6px;"
GOBTN = "align-self: flex-start; border: 0; background: transparent; padding: 4px 0; color: oklch(var(--t4) 0.15 175); font-size: 12.5px; font-weight: 700; text-decoration: underline; cursor: pointer;"
NOTE = "border-radius: 16px; padding: 12px 16px; font-size: 13.5px; line-height: 1.55;"
OL = "margin: 0; padding-left: 22px; display: flex; flex-direction: column; gap: 6px; font-size: 13.5px; line-height: 1.5;"

SCREENS4 = f'''
        <sc-if value="{{{{ sInvolve }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          {head("icInvolve", 175, "Help build and look after Amplify", "{{ ivIntro }}")}
          <div style="display: flex; flex-wrap: wrap; gap: 12px 20px;">{ext("ivRepo", "The code on GitHub")} {ext("ivContrib", "How to contribute")} {ext("ivGood", "Good first issues")}</div>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr)); gap: 14px;">
            <sc-for list="{{{{ ivWays }}}}" as="w" hint-placeholder-count="4">
              <section class="amp-card" style="{PANEL} display: flex; flex-direction: column; gap: 10px;">
                <h2 style="margin: 0; display: flex; align-items: center; gap: 8px; font-size: 17px; font-weight: 800;"><span aria-hidden="true" style="{{{{ w.icon }}}}"></span>{{{{ w.time }}}}</h2>
                <sc-for list="{{{{ w.items }}}}" as="i" hint-placeholder-count="3"><div style="{CARD}"><div style="font-size: 14px; font-weight: 800;">{{{{ i.t }}}}</div><div style="{SMALL}">{{{{ i.how }}}}</div><button type="button" onClick="{{{{ i.go }}}}" style="{GOBTN}">Go to {{{{ i.where }}}}</button></div></sc-for>
              </section>
            </sc-for>
          </div>
          <section style="{PANEL}"><h2 style="{H2}">How a change gets in</h2><p style="margin: 0 0 10px; {SMALL}">This portal is built the way professional teams work: {term("opensource", "open source")}, {term("issue", "issues")}, {term("pullrequest", "pull requests")} and {term("ci", "continuous integration")}.</p>
            <ol style="{OL}"><sc-for list="{{{{ ivHow }}}}" as="h" hint-placeholder-count="5"><li><span style="font-weight: 800;">{{{{ h.s }}}}.</span> {{{{ h.d }}}}</li></sc-for></ol></section>
          <section style="{PANEL}"><h2 style="{H2}">Roles you could take on</h2><div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 240px), 1fr)); gap: 10px;"><sc-for list="{{{{ ivRoles }}}}" as="r" hint-placeholder-count="6"><div style="{CARD}"><div style="font-size: 14px; font-weight: 800;">{{{{ r.r }}}}</div><div style="{SMALL}">{{{{ r.d }}}}</div></div></sc-for></div></section>
          <div role="note" style="{NOTE} border: 1px solid oklch(var(--t1) 0.16 25 / 0.45); background: oklch(var(--t1) 0.16 25 / 0.1);"><div style="font-weight: 800; margin-bottom: 6px;">Rules that keep everyone safe</div><ul style="margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 4px;"><sc-for list="{{{{ ivRules }}}}" as="r" hint-placeholder-count="5"><li>{{{{ r.t }}}}</li></sc-for></ul></div>
        </div>
        </sc-if>

        <sc-if value="{{{{ sAmbassadors }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          {head("icAmb", 70, "Ambassadors and champions", "{{ amIntro }}")}
          <div role="note" style="{NOTE} border: 1px dashed oklch(var(--t2) 0.16 70 / 0.8); background: oklch(var(--t1) 0.16 70 / 0.12);"><span style="font-weight: 800;">Pilot.</span> {{{{ amStatus }}}}</div>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr)); gap: 14px;">
            <sc-for list="{{{{ amTiers }}}}" as="t" hint-placeholder-count="3">
              <section class="amp-card" style="{PANEL} display: flex; flex-direction: column; gap: 8px;">
                <h2 style="margin: 0; font-size: 20px; font-weight: 900;">{{{{ t.tier }}}}</h2>
                <div style="{SMALL}"><span style="font-weight: 800;">Who:</span> {{{{ t.who }}}}</div>
                <ul style="margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 4px; font-size: 13.5px;"><sc-for list="{{{{ t.does }}}}" as="d" hint-placeholder-count="3"><li>{{{{ d.d }}}}</li></sc-for></ul>
                <div style="{LABEL}">{{{{ t.time }}}}</div>
              </section>
            </sc-for>
          </div>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr)); gap: 14px;">
            <section style="{PANEL}"><h2 style="{H2}">Our promise to you</h2><ul style="margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 6px; font-size: 13.5px; line-height: 1.5;"><sc-for list="{{{{ amPromise }}}}" as="x" hint-placeholder-count="4"><li>{{{{ x.t }}}}</li></sc-for></ul></section>
            <section style="{PANEL}"><h2 style="{H2}">Code of conduct</h2><ul style="margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 6px; font-size: 13.5px; line-height: 1.5;"><sc-for list="{{{{ amConduct }}}}" as="x" hint-placeholder-count="4"><li>{{{{ x.t }}}}</li></sc-for></ul><p style="margin: 10px 0 0; {SMALL}">Anyone working with young people for the programme follows {term("safeguarding", "safeguarding")} rules and, where needed, has a {term("dbs", "background check")}.</p></section>
          </div>
          <section style="{PANEL} display: flex; flex-wrap: wrap; align-items: center; gap: 14px;"><div style="flex: 1 1 280px; min-width: 0;"><h2 style="margin: 0 0 4px; font-size: 17px; font-weight: 800;">Register your interest</h2><p style="margin: 0; {SMALL}">A short public form on GitHub that asks only for your role, nation, age band and what you would like to do. No names or contact details.</p></div>{ext("amRegister", "Open the form")}</section>
        </div>
        </sc-if>

        <sc-if value="{{{{ sCampaign }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          {head("icCamp", 25, "Campaign and awareness kit", "{{ cpIntro }}")}
          <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 220px), 1fr)); gap: 14px;">
            <sc-for list="{{{{ cpAssets }}}}" as="a" hint-placeholder-count="4"><figure class="amp-card" style="margin: 0; {CARD}"><img src="{{{{ a.src }}}}" alt="{{{{ a.alt }}}}" style="width: 100%; height: 200px; object-fit: contain; border-radius: 10px; background: rgb(var(--film-rgb) / 0.04);" /><figcaption style="font-size: 13.5px; font-weight: 800;">{{{{ a.name }}}}</figcaption><a href="{{{{ a.href }}}}" target="_blank" rel="noopener" style="{LINK} font-size: 12.5px;">Open to print or save<span class="amp-sr"> (opens in a new tab)</span></a></figure></sc-for>
          </div>
          <section style="{PANEL}"><h2 style="{H2}">Posts and messages to adapt</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr)); gap: 12px;"><sc-for list="{{{{ cpPosts }}}}" as="x" hint-placeholder-count="4"><div style="{CARD}"><div style="{LABEL}">{{{{ x.channel }}}}</div><p style="margin: 0; font-size: 13.5px; line-height: 1.55;">{{{{ x.text }}}}</p><button type="button" onClick="{{{{ x.copy }}}}" style="align-self: flex-start; min-height: 36px; border-radius: 999px; padding: 6px 14px; border: 1px solid oklch(var(--t2) 0.16 145 / 0.7); background: transparent; color: rgb(var(--ink-rgb)); font-size: 13px; font-weight: 700; cursor: pointer;">{{{{ x.copied }}}}</button></div></sc-for></div>
            <p style="margin: 12px 0 0; {SMALL}">{{{{ cpSocial }}}}</p>
            <p style="margin: 6px 0 0; {SMALL}"><span style="font-family: 'Space Mono', monospace; font-weight: 700;">{{{{ cpTags }}}}</span> &middot; {{{{ cpTagNote }}}}</p>
          </section>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr)); gap: 14px;">
            <section style="{PANEL}"><h2 style="{H2}">{{{{ cpAsmTitle }}}}</h2><ol style="{OL}"><sc-for list="{{{{ cpAsm }}}}" as="a" hint-placeholder-count="5"><li>{{{{ a.t }}}}</li></sc-for></ol></section>
            <section style="{PANEL}"><h2 style="{H2}">Moments to plan around</h2><ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 8px;"><sc-for list="{{{{ cpMoments }}}}" as="m" hint-placeholder-count="5"><li style="font-size: 13.5px;"><span style="font-weight: 800;">{{{{ m.when }}}}</span> &middot; {{{{ m.what }}}} <span style="font-style: italic; color: rgb(var(--ink-rgb) / 0.72);">({{{{ m.prov }}}})</span></li></sc-for></ul><p style="margin: 10px 0 0; {SMALL}">{{{{ cpMomNote }}}}</p></section>
          </div>
        </div>
        </sc-if>

        <sc-if value="{{{{ sLearn }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          {head("icLearn", 300, "Training and education sessions", "{{ lnIntro }}")}
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr)); gap: 14px;">
            <sc-for list="{{{{ lnMods }}}}" as="m" hint-placeholder-count="4">
              <section class="amp-card" style="{PANEL} display: flex; flex-direction: column; gap: 8px;">
                <div style="{LABEL}">{{{{ m.id }}}} &middot; {{{{ m.mins }}}}</div>
                <h2 style="margin: 0; font-size: 17px; font-weight: 800;">{{{{ m.t }}}}</h2>
                <div style="{SMALL}"><span style="font-weight: 800;">For:</span> {{{{ m.who }}}}</div>
                <div style="font-size: 13px; font-weight: 800;">Afterwards, people can</div>
                <ul style="margin: 0; padding-left: 20px; font-size: 13px; line-height: 1.5;"><sc-for list="{{{{ m.out }}}}" as="o" hint-placeholder-count="2"><li>{{{{ o.o }}}}</li></sc-for></ul>
                <div style="font-size: 13px; font-weight: 800;">Steps</div>
                <ol style="margin: 0; padding-left: 20px; font-size: 13px; line-height: 1.5;"><sc-for list="{{{{ m.steps }}}}" as="x" hint-placeholder-count="3"><li>{{{{ x.x }}}}</li></sc-for></ol>
                <div style="display: flex; flex-wrap: wrap; gap: 4px 14px;"><sc-for list="{{{{ m.screens }}}}" as="g" hint-placeholder-count="2"><button type="button" onClick="{{{{ g.go }}}}" style="{GOBTN}">{{{{ g.label }}}}</button></sc-for></div>
              </section>
            </sc-for>
          </div>
        </div>
        </sc-if>

        <sc-if value="{{{{ sStem }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          {head("icStem", 200, "STEM spotlight: girls in code, engineering, architecture and DevOps", "{{ stIntro }}")}
          <section style="{PANEL}"><h2 style="{H2}">The picture, with sources</h2><ul style="margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 6px;"><sc-for list="{{{{ stFacts }}}}" as="f" hint-placeholder-count="4"><li style="font-size: 13.5px; line-height: 1.5;">{{{{ f.f }}}} <a href="{{{{ f.url }}}}" target="_blank" rel="noopener noreferrer" style="font-size: 12.5px;">Source: {{{{ f.src }}}}<span class="amp-sr"> (opens in a new tab)</span></a></li></sc-for></ul></section>
          <sc-for list="{{{{ stPaths }}}}" as="x" hint-placeholder-count="5">
            <section style="{PANEL}">
              <h2 style="margin: 0 0 4px; display: flex; align-items: center; gap: 8px; font-size: 18px; font-weight: 800;"><span aria-hidden="true" style="{{{{ x.icon }}}}"></span>{{{{ x.p }}}}</h2>
              <p style="margin: 0 0 10px; {SMALL}"><span style="font-weight: 800;">First step:</span> {{{{ x.first }}}}</p>
              <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 250px), 1fr)); gap: 10px;"><sc-for list="{{{{ x.items }}}}" as="o" hint-placeholder-count="3"><div class="amp-card" style="{CARD}"><div style="font-size: 14.5px; font-weight: 800;">{{{{ o.name }}}}</div><div style="{SMALL}">{{{{ o.what }}}}</div><div style="font-size: 12px;">{{{{ o.nations }}}} &middot; <span style="font-style: italic;">{{{{ o.prov }}}}</span></div><a href="{{{{ o.url }}}}" target="_blank" rel="noopener" style="{LINK} font-size: 12.5px;">Visit<span aria-hidden="true" style="{{{{ icExt }}}}"></span><span class="amp-sr"> (opens in a new tab)</span></a></div></sc-for></div>
            </section>
          </sc-for>
          <section style="{PANEL}"><h2 style="{H2}">Learn {term("devops", "DevOps")} on this portal</h2><p style="margin: 0 0 10px; {SMALL}">{{{{ stDevIntro }}}}</p>
            <ol style="{OL}"><sc-for list="{{{{ stDev }}}}" as="d" hint-placeholder-count="7"><li><span style="font-weight: 800;">{{{{ d.s }}}}.</span> {{{{ d.d }}}} <span style="font-family: 'Space Mono', monospace; font-size: 12px; color: rgb(var(--ink-rgb) / 0.78);">{{{{ d.where }}}}</span></li></sc-for></ol>
            <div style="margin-top: 10px; display: flex; flex-wrap: wrap; gap: 12px 20px;">{ext("ivRepo", "Explore the repository")} {ext("ivGood", "Find a good first issue")}</div>
          </section>
          <div role="note" style="{NOTE} border: 1px solid oklch(var(--t1) 0.16 25 / 0.45); background: oklch(var(--t1) 0.16 25 / 0.1);">{{{{ stNote }}}}</div>
        </div>
        </sc-if>
'''

GROUP4 = '''    ["Get involved", [
      ["involve", "Contribute", "dot", 175, 4, "NEW", "contribute help build open source github issue pull request volunteer check source accessibility test translate code devops"],
      ["ambassadors", "Ambassadors & champions", "dia", 70, 4, "NEW", "ambassador champion supporter volunteer represent mentor badge programme"],
      ["campaign", "Campaign kit", "tri", 25, 4, "NEW", "campaign marketing advertising poster flyer social post assembly hashtag awareness collateral"],
      ["learn", "Training & sessions", "sq", 300, 4, "NEW", "training education lesson session plan teacher youth worker workshop module course"],
      ["stem", "STEM spotlight", "ring", 200, 4, "NEW", "stem science technology engineering maths coding code club girls women architecture devops cyber"]
    ]],
'''


def transforms():
    files = '"./data/media.json", "./data/communities.json"]'
    return [
        ("ext4-css", "tooltip and term styles", "  .amp-sr {", TIP_CSS + "\n  .amp-sr {", 1),
        ("ext4-load", "the tooltip and Get involved data load with the rest",
         files + ".map(get));", files[:-1] + ', "./data/tooltips.json", "./data/involve.json"].map(get));', 1),
        ("ext4-load-vars", "name the two new data sets", "const [src, lat, sg, mo, reg, bld, ch, hp, ln, ig, ab, hm, md, cm] =", "const [src, lat, sg, mo, reg, bld, ch, hp, ln, ig, ab, hm, md, cm, tt, iv] =", 1),
        ("ext4-load-state", "keep them in state", "amp: { src, lat, sg, mo, reg, bld, ch, hp, ln, ig, ab, hm, md, cm, loaded", "amp: { src, lat, sg, mo, reg, bld, ch, hp, ln, ig, ab, hm, md, cm, tt, iv, loaded", 1),
        ("ext4-group", "the Get involved group sits after Help & get involved, before the closing bracket of the drawer",
         '    ]]\n  ];', '    ]],\n' + GROUP4.rstrip(",\n") + '\n  ];', 1),
        ("ext4-hash", "the new screens can be linked to", "|media|communities)$/.test(id)", "|media|communities|involve|ambassadors|campaign|learn|stem)$/.test(id)", 1),
        ("ext4-logic", "tooltip layer and Get involved logic", "  async loadPetition() {", LOGIC4 + "\n  async loadPetition() {", 1),
        ("ext4-vals", "their values join renderVals", "...this.ampVals3(s),", "...this.ampVals3(s), ...this.ampVals4(s),", 1),
        ("ext4-mount", "start the tooltip layer and restore the reader's persona when the page mounts",
         "    this.loadAmplifyData();\n", "    this.loadAmplifyData();\n    this.ampTipsOn();\n    this.setState({ persona: this.ampPersona() });\n", 1),
        ("ext4-unmount", "remove the tooltip layer on unmount, inside the design's own unmount", "  componentWillUnmount() {\n", "  componentWillUnmount() {\n    this.ampTipsOff();\n", 1),
        ("ext4-nav-id", "each drawer item carries its id for its tooltip", "label: lbl, sub: sub, flag: flag,", "label: lbl, sub: sub, flag: flag, tip: \"nav:\" + id,", 1),
        ("ext4-nav-tip", "every drawer item explains itself on hover and focus",
         '<button onClick="{{ i.go }}" aria-current="{{ i.cur }}"', '<button onClick="{{ i.go }}" data-tip="{{ i.tip }}" aria-current="{{ i.cur }}"', 1),
        ("ext4-ui-portal", "header control tooltip", '<button onClick="{{ viewPortal }}"', '<button onClick="{{ viewPortal }}" data-tip="ui:portal"', 1),
        ("ext4-ui-both", "header control tooltip", '<button onClick="{{ viewBoth }}"', '<button onClick="{{ viewBoth }}" data-tip="ui:both"', 1),
        ("ext4-ui-app", "header control tooltip", '<button onClick="{{ viewApp }}"', '<button onClick="{{ viewApp }}" data-tip="ui:app"', 1),
        ("ext4-ui-replay", "header control tooltip", '<button onClick="{{ replay }}"', '<button onClick="{{ replay }}" data-tip="ui:replay"', 1),
        ("ext4-ui-access", "header control tooltip", '<button onClick="{{ toggleA11y }}"', '<button onClick="{{ toggleA11y }}" data-tip="ui:access"', 1),
        ("ext4-explainer", "the explainer bar opens every screen, above the ribbon",
         '        <sc-if value="{{ tbShow }}"', explainer() + '        <sc-if value="{{ tbShow }}"', 1),
        ("ext4-screens", "the five Get involved screens", '        <div data-slot="portal-end" style="display: none;"></div>', SCREENS4 + '\n        <div data-slot="portal-end" style="display: none;"></div>', 1),
    ]
