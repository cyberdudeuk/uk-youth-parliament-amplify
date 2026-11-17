"""Fourth set of portal extensions: tooltips and explainers for every persona, and the Get involved group.

  tooltips     One accessible tooltip for the whole page, outside the React tree, shown on hover or keyboard focus of
               anything marked data-tip (every drawer item, the header controls and terms in the new screens). It stays
               while the pointer is over it, Escape closes it, and it never covers what it explains (WCAG 1.4.13).
  explainer    A bar on every screen saying what the screen is for, tailored to the persona the reader picks. The pick
               stays on the device (browser storage inside try/catch, with an in-memory fallback) and is never sent.
  involve      Ways to help build, check and look after the portal, by time and skill, with the contribution rules
  ambassadors  Supporter, champion and ambassador levels; sign-ups paused until a safeguarding lead is in place (G06, O12, D25)
  campaign     Posters, a social card and badge drawn in code, template posts, an assembly script and key dates
  learn        Ready-to-run training sessions with audiences, timings, outcomes and the screens to use
  stem         STEM and tech: sourced facts, free opportunities in eight lanes (science, innovation, data and AI, digital,
               cyber, engineering, enterprise architecture, girls in tech), enterprise architecture layers, careers in
               government and the public sector, tech as a youth voice issue, and a DevOps path built on this repo
All text comes from data/tooltips.json and data/involve.json; persona options are read from the data at build time
because an HTML parser drops anything inside a <select> that is not an <option>.
"""
import html
import json
import os

from extend import EYEBROW, H1, LEDE, PANEL, LABEL, SMALL, LINK

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# The pack's release file (D38): its total download count is the one measure of the kit's use that needs no tracking
_PR = json.load(open(os.path.join(R, "data", "involve.json"), encoding="utf-8"))["campaign"]["pack_release"]
PACK_URL = f"https://github.com/cyberdudeuk/uk-youth-parliament-amplify/releases/download/{_PR['tag']}/amplify-graphics-pack.zip"

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
      key: (e) => { if (e.key === "Escape" && !el.hidden) hide(); else if (e.key === "Escape" && this.state.art) this.ampArtClose(); else if (e.key === "Tab" && this.state.art) { const bx = document.querySelector(".amp-lightbox"); const f = bx ? Array.from(bx.querySelectorAll("a[href], button")) : []; if (f.length) { const a = document.activeElement, i = f.indexOf(a); if (i < 0 || (e.shiftKey && i === 0) || (!e.shiftKey && i === f.length - 1)) { e.preventDefault(); (e.shiftKey ? f[f.length - 1] : f[0]).focus(); } } } },
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
  ampArt(name, src, alt, file) {
    this._artBack = document.activeElement;
    this.setState({ art: { name, src, alt, file }, artMsg: "" }, () => { const c = document.getElementById("amp-art-close"); if (c) c.focus(); });
  }
  async ampArtSave() {
    const a = this.state.art || {}, name = (a.file || "artwork.svg").split("/").pop();
    const say = (t) => this.setState({ artMsg: t });
    let dl = null;
    try { dl = window.claude && window.claude.use ? await window.claude.use("downloads") : null; } catch (e) { dl = null; }
    if (!dl) { say("Saving is not available in this view: use Copy on GitHub, or right-click the picture and save it."); return; }
    try {
      const r = await fetch(new URL(a.src, document.baseURI).href); const text = await r.text();
      await dl.save({ filename: name, data: text }); say("Saved " + name + ".");
    } catch (e) {
      const c = (e && e.code) || "";
      say(c === "declined" ? "Not saved." : c === "rate_limited" ? "A save is already waiting for your answer." : "Saving did not work here: use Copy on GitHub instead.");
    }
  }
  ampArtClose() { this.setState({ art: null }, () => { if (this._artBack && this._artBack.focus) this._artBack.focus(); }); }
  ampArtPrint() {
    const b = document.body; b.classList.add("amp-print-art");
    const done = () => { b.classList.remove("amp-print-art"); window.removeEventListener("afterprint", done); };
    window.addEventListener("afterprint", done);
    try { window.print(); } catch (e) { /* printing blocked by the host: the fallback link stays on screen */ }
    setTimeout(done, 60000);
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
      artOpen: !!s.art, artName: (s.art || {}).name || "", artSrc: (s.art || {}).src || "", artAlt: (s.art || {}).alt || "",
      artFile: ((s.art || {}).file || "").split("/").pop(), artGit: repo + "/blob/main/site/" + ((s.art || {}).file || ""),
      artClose: () => this.ampArtClose(), artPrint: () => this.ampArtPrint(), artSave: () => this.ampArtSave(), artMsg: s.artMsg || "",
      persona: p, setPersona: (e) => { const v = e.target.value; try { window.localStorage.setItem("amp-persona", v); } catch (err) { /* storage unavailable: keep it in memory */ } this.setState({ persona: v }); },
      ivIntro: inv.intro || "", ivRepo: repo, ivContrib: repo + "/blob/main/CONTRIBUTING.md", ivGood: repo + "/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22",
      ivWays: inv.ways.map((w) => ({ time: w.time, icon: this.ampIcon(w.icon, "oklch(var(--t3) 0.16 175)", 18), items: w.items.map((i) => ({ t: i.t, how: i.how, go: go(i.screen), where: label(i.screen) })) })),
      ivRoles: inv.roles, ivRules: inv.rules.map((t) => ({ t })), ivHow: inv.how.map((h, k) => ({ n: String(k + 1), s: h.s, d: h.d })),
      amStatus: amb.status || "", amIntro: amb.intro || "", amTiers: amb.tiers.map((t) => ({ tier: t.tier, who: t.who, time: t.time, does: t.does.map((d) => ({ d })) })),
      amPromise: amb.promise.map((t) => ({ t })), amConduct: amb.conduct.map((t) => ({ t })),
      amPaused: amb.paused || "Sign-ups open once safeguarding is in place.",  // D25: no sign-up link while readiness gate G06 is open
      cpVideos: (cp.videos || []).map((v) => ({ name: v.name, src: "./" + v.file, poster: "./" + v.poster, use: v.use, transcript: v.transcript })), cpVideoNote: cp.video_note || "",
      cpIntro: cp.intro || "", cpAssets: cp.assets.map((a) => ({ name: a.name, src: "./" + a.file, alt: a.alt, view: () => this.ampArt(a.name, "./" + a.file, a.alt, a.file) })),
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
      stEaIntro: (st.ea || {}).intro || "", stEaSrc: (st.ea || {}).source || "", stEa: ((st.ea || {}).layers || []).map((l) => ({ layer: l.layer, what: l.what, role: l.role })),
      stCarIntro: (st.careers || {}).intro || "", stCareers: ((st.careers || {}).groups || []).map((g) => ({ g: g.g, items: g.ids.map((id) => byId[id]).filter(Boolean).map((o) => ({ name: o.name, what: o.what, use: o.use, url: o.url, nations: o.nations.join(" · "), kind: o.kind, prov: PV[o.provenance] || o.provenance })) })),
      stVoiceIntro: (st.tech_voice || {}).intro || "", stVoice: ((st.tech_voice || {}).links || []).map((l) => ({ t: l.t, where: label(l.screen), go: go(l.screen) })),
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
  @media print { body.amp-print-art * { visibility: hidden !important; } body.amp-print-art .amp-lightbox, body.amp-print-art .amp-lightbox-art { visibility: visible !important; }
    body.amp-print-art .amp-lightbox { position: absolute !important; inset: 0 !important; background: #fff !important; padding: 0 !important; }
    body.amp-print-art .amp-lightbox-art { max-height: none !important; height: 100vh !important; border-radius: 0 !important; } }
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
        <sc-if value="{{{{ artOpen }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div class="amp-lightbox" role="dialog" aria-modal="true" aria-label="{{{{ artName }}}}" style="position: fixed; inset: 0; z-index: 95; display: flex; flex-direction: column; gap: 12px; padding: clamp(10px, 3vw, 28px); background: rgb(0 0 0 / 0.82); overflow: auto;">
          <div class="amp-lightbox-controls" style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px; color: #fff;">
            <span style="flex: 1 1 200px; min-width: 0; font-size: 15px; font-weight: 800;">{{{{ artName }}}}</span>
            <button type="button" onClick="{{{{ artPrint }}}}" style="min-height: 40px; border-radius: 999px; padding: 8px 16px; border: 0; background: oklch(0.85 0.15 145); color: #06100f; font-size: 13.5px; font-weight: 800; cursor: pointer;">Print</button>
            <button type="button" onClick="{{{{ artSave }}}}" style="min-height: 40px; border-radius: 999px; padding: 8px 16px; border: 1px solid #fff; background: transparent; color: #fff; font-size: 13.5px; font-weight: 800; cursor: pointer;">Save</button>
            <a href="{{{{ artGit }}}}" target="_blank" rel="noopener noreferrer" style="display: inline-flex; align-items: center; min-height: 40px; border-radius: 999px; padding: 8px 16px; border: 1px solid rgb(255 255 255 / 0.5); color: #fff; font-size: 13.5px; font-weight: 700;">Copy on GitHub<span class="amp-sr"> (opens in a new tab)</span></a>
            <button type="button" id="amp-art-close" onClick="{{{{ artClose }}}}" style="min-height: 40px; border-radius: 999px; padding: 8px 16px; border: 1px solid #fff; background: transparent; color: #fff; font-size: 13.5px; font-weight: 800; cursor: pointer;">Close</button>
          </div>
          <img class="amp-lightbox-art" src="{{{{ artSrc }}}}" alt="{{{{ artAlt }}}}" style="flex: 1 1 auto; min-height: 0; width: 100%; max-height: calc(100vh - 120px); object-fit: contain; background: #fff; border-radius: 12px;" />
          <p class="amp-lightbox-controls" role="status" aria-live="polite" style="margin: 0; font-size: 13px; font-weight: 700; color: #fff;">{{{{ artMsg }}}}</p>
          <p class="amp-lightbox-controls" style="margin: 0; font-size: 12.5px; color: rgb(255 255 255 / 0.85);">Save asks you to confirm the file first. If Print does nothing, the page you are viewing this in is blocking it: save the file and print it from your device, or use Copy on GitHub. Escape closes this view.</p>
        </div>
        </sc-if>
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
          <div role="note" style="{NOTE} border: 1px dashed oklch(var(--t2) 0.16 70 / 0.8); background: oklch(var(--t1) 0.16 70 / 0.12);"><span style="font-weight: 800;">Sign-ups paused.</span> {{{{ amStatus }}}}</div>
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
          <section aria-labelledby="amp-amb-paused" style="{PANEL} display: flex; flex-direction: column; gap: 6px;"><h2 id="amp-amb-paused" style="margin: 0; font-size: 17px; font-weight: 800;">Signing up is paused</h2><p style="margin: 0; font-size: 13.5px; line-height: 1.55;">We are not taking sign-ups from anyone, of any age, until Amplify has a named adult responsible for keeping you safe (a safeguarding lead) and a written plan for what happens if something worries us. {{{{ amPaused }}}}</p><p style="margin: 0; {SMALL}">Please do not post on GitHub to sign up. Worried about your safety? Use the helplines on Safeguarding &amp; support.</p></section>
        </div>
        </sc-if>

        <sc-if value="{{{{ sCampaign }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          {head("icCamp", 175, "Campaign and awareness kit", "{{ cpIntro }}")}
          <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 220px), 1fr)); gap: 14px;">
            <sc-for list="{{{{ cpAssets }}}}" as="a" hint-placeholder-count="4"><figure class="amp-card" style="margin: 0; {CARD}"><button type="button" onClick="{{{{ a.view }}}}" aria-label="View {{{{ a.name }}}}" style="border: 0; padding: 0; background: rgb(var(--film-rgb) / 0.04); border-radius: 10px; cursor: zoom-in;"><img src="{{{{ a.src }}}}" alt="{{{{ a.alt }}}}" style="display: block; width: 100%; height: 200px; object-fit: contain; border-radius: 10px;" /></button><figcaption style="font-size: 13.5px; font-weight: 800;">{{{{ a.name }}}}</figcaption><button type="button" onClick="{{{{ a.view }}}}" style="{GOBTN}">View, print or save</button></figure></sc-for>
          </div>
          <section aria-labelledby="amp-films" style="{PANEL}"><h2 id="amp-films" style="{H2}">Films and short videos</h2><p style="margin: 0 0 12px; {SMALL}">{{{{ cpVideoNote }}}}</p>
            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 240px), 1fr)); gap: 14px;"><sc-for list="{{{{ cpVideos }}}}" as="v" hint-placeholder-count="4"><figure class="amp-card" style="margin: 0; {CARD}"><video controls preload="none" playsinline poster="{{{{ v.poster }}}}" src="{{{{ v.src }}}}" aria-label="{{{{ v.name }}}}" style="display: block; width: 100%; max-height: 360px; background: #06100f; border-radius: 10px;"></video><figcaption style="font-size: 13.5px; font-weight: 800;">{{{{ v.name }}}}</figcaption><p style="margin: 0; {SMALL}">{{{{ v.use }}}}</p><details style="font-size: 13px;"><summary style="cursor: pointer; font-weight: 700;">Transcript</summary><p style="margin: 6px 0 0; line-height: 1.5;">{{{{ v.transcript }}}}</p></details><a href="{{{{ v.src }}}}" download style="{GOBTN}">Download the video</a></figure></sc-for></div></section>
          <section aria-labelledby="amp-pack" style="{PANEL} display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px;"><div><h2 id="amp-pack" style="{H2}">Graphics pack</h2><p style="margin: 0; font-size: 13.5px; line-height: 1.55;">Every poster, the sticker sheet and badge, plus ready-sized images for Teams, Viva Engage, email, LinkedIn, Instagram, Stories and TikTok, and a six-slide carousel. One zip, free to use and remix with credit.</p></div><div style="display: flex; flex-direction: column; gap: 4px;"><a href="{PACK_URL}" style="{GOBTN}">Download the graphics pack (.zip)</a><a href="./art/amplify-graphics-pack.zip" download style="{SMALL}">or download it from this site</a><span style="{SMALL}">Downloads from GitHub are counted in total only; we never see who downloaded it.</span></div></section>
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
          {head("icStem", 200, "STEM and tech: science, innovation, data, digital, cyber and technology", "{{ stIntro }}")}
          <section style="{PANEL}"><h2 style="{H2}">The picture, with sources</h2><ul style="margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 6px;"><sc-for list="{{{{ stFacts }}}}" as="f" hint-placeholder-count="4"><li style="font-size: 13.5px; line-height: 1.5;">{{{{ f.f }}}} <a href="{{{{ f.url }}}}" target="_blank" rel="noopener noreferrer" style="font-size: 12.5px;">Source: {{{{ f.src }}}}<span class="amp-sr"> (opens in a new tab)</span></a></li></sc-for></ul></section>
          <sc-for list="{{{{ stPaths }}}}" as="x" hint-placeholder-count="5">
            <section style="{PANEL}">
              <h2 style="margin: 0 0 4px; display: flex; align-items: center; gap: 8px; font-size: 18px; font-weight: 800;"><span aria-hidden="true" style="{{{{ x.icon }}}}"></span>{{{{ x.p }}}}</h2>
              <p style="margin: 0 0 10px; {SMALL}"><span style="font-weight: 800;">First step:</span> {{{{ x.first }}}}</p>
              <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 250px), 1fr)); gap: 10px;"><sc-for list="{{{{ x.items }}}}" as="o" hint-placeholder-count="3"><div class="amp-card" style="{CARD}"><div style="font-size: 14.5px; font-weight: 800;">{{{{ o.name }}}}</div><div style="{SMALL}">{{{{ o.what }}}}</div><div style="font-size: 12px;">{{{{ o.nations }}}} &middot; <span style="font-style: italic;">{{{{ o.prov }}}}</span></div><a href="{{{{ o.url }}}}" target="_blank" rel="noopener" style="{LINK} font-size: 12.5px;">Visit<span aria-hidden="true" style="{{{{ icExt }}}}"></span><span class="amp-sr"> (opens in a new tab)</span></a></div></sc-for></div>
            </section>
          </sc-for>
          <section style="{PANEL}"><h2 style="{H2}">Enterprise architecture, layer by layer</h2><p style="margin: 0 0 10px; {SMALL}">{{{{ stEaIntro }}}}</p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 240px), 1fr)); gap: 10px;"><sc-for list="{{{{ stEa }}}}" as="l" hint-placeholder-count="6"><div class="amp-card" style="{CARD}"><div style="font-size: 14.5px; font-weight: 800;">{{{{ l.layer }}}}</div><div style="{SMALL}">{{{{ l.what }}}}</div><div style="font-size: 12.5px;"><span style="font-weight: 800;">Government role:</span> {{{{ l.role }}}}</div></div></sc-for></div>
            <p style="margin: 10px 0 0; {SMALL}">{{{{ stEaSrc }}}}</p></section>
          <section style="{PANEL}"><h2 style="{H2}">Careers in government and the public sector</h2><p style="margin: 0 0 10px; {SMALL}">{{{{ stCarIntro }}}}</p>
            <sc-for list="{{{{ stCareers }}}}" as="g" hint-placeholder-count="4"><div style="margin-bottom: 12px;"><div style="{LABEL} margin-bottom: 6px;">{{{{ g.g }}}}</div><div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 250px), 1fr)); gap: 10px;"><sc-for list="{{{{ g.items }}}}" as="o" hint-placeholder-count="3"><div class="amp-card" style="{CARD}"><div style="font-size: 14.5px; font-weight: 800;">{{{{ o.name }}}}</div><div style="{SMALL}">{{{{ o.what }}}}</div><div style="font-size: 12.5px;">{{{{ o.use }}}}</div><div style="font-size: 12px;">{{{{ o.kind }}}} &middot; {{{{ o.nations }}}} &middot; <span style="font-style: italic;">{{{{ o.prov }}}}</span></div><a href="{{{{ o.url }}}}" target="_blank" rel="noopener" style="{LINK} font-size: 12.5px;">Visit<span aria-hidden="true" style="{{{{ icExt }}}}"></span><span class="amp-sr"> (opens in a new tab)</span></a></div></sc-for></div></div></sc-for></section>
          <section style="{PANEL}"><h2 style="{H2}">Tech is a youth voice issue</h2><p style="margin: 0 0 10px; {SMALL}">{{{{ stVoiceIntro }}}}</p><ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 6px;"><sc-for list="{{{{ stVoice }}}}" as="v" hint-placeholder-count="4"><li style="font-size: 13.5px;">{{{{ v.t }}}} <button type="button" onClick="{{{{ v.go }}}}" style="{GOBTN}">{{{{ v.where }}}}</button></li></sc-for></ul></section>
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
      ["campaign", "Campaign kit", "tri", 175, 4, "NEW", "campaign marketing advertising poster flyer social post assembly hashtag awareness collateral"],
      ["learn", "Training & sessions", "sq", 300, 4, "NEW", "training education lesson session plan teacher youth worker workshop module course"],
      ["stem", "STEM & tech", "ring", 200, 4, "NEW", "stem science innovation data ai digital cyber technology engineering maths coding code club girls women enterprise architecture devops apprenticeships careers government fast stream"]
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
