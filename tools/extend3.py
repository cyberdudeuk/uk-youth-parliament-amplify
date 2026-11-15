"""Third set of portal extensions: the rolling hero carousel with spotlights on Home, the media centre, the
communities hub, and links into the main communication, collaboration and productivity suites.

  carousel     Home's hero: spotlight slides from data/media.json; auto-advances every 7 seconds only when motion is
               on, the system does not ask for reduced motion, and nobody is hovering, focusing or has paused it
  media        Media centre: approved descriptions with copy buttons, key facts with sources, illustrations, rules
  communities  Communities, networks and youth groups, grouped by kind, read from the Trusted sources list
  share        Add to Google or Outlook calendars, share to Microsoft Teams, Google Classroom or WhatsApp, or copy a
               link, each opening only when the person chooses, each labelled with its own terms and age rules
"""
from extend import EYEBROW, H1, LEDE, PANEL, LABEL, SMALL, LINK

LOGIC3 = r'''
  ampCarousel() {
    if (this._carT) return;
    this._carT = setInterval(() => {
      const st = this.state, n = ((st.amp || {}).md || {}).spotlight ? st.amp.md.spotlight.length : 0;
      let reduce = false; try { reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) { /* no media queries */ }
      if (n > 1 && st.screen === "home" && st.motion && !reduce && !st.carPaused && !st.carHold && !st.splash) this.setState({ carIdx: ((st.carIdx || 0) + 1) % n });
    }, 7000);
  }
  ampShare(title, url, start, end) {
    const e = encodeURIComponent, t = e(title), u = e(url);
    const d = (x) => x.replace(/-/g, "");
    const add1 = (x) => new Date(Date.parse(x + "T00:00:00Z") + 864e5).toISOString().slice(0, 10);
    const out = [];
    if (start) {
      out.push({ label: "Google Calendar", href: "https://calendar.google.com/calendar/render?action=TEMPLATE&text=" + t + "&dates=" + d(start) + "/" + d(add1(end || start)) + "&details=" + u });
      out.push({ label: "Outlook calendar", href: "https://outlook.live.com/calendar/0/deeplink/compose?subject=" + t + "&startdt=" + start + "&enddt=" + add1(end || start) + "&allday=true&body=" + u });
    }
    out.push({ label: "Microsoft Teams", href: "https://teams.microsoft.com/share?href=" + u + "&msgText=" + t });
    out.push({ label: "Google Classroom", href: "https://classroom.google.com/share?url=" + u + "&title=" + t });
    out.push({ label: "WhatsApp", href: "https://wa.me/?text=" + t + "%20" + u });
    return out;
  }
  ampVals3(s) {
    const A = s.amp || {}, md = A.md || { spotlight: [], blurbs: [], facts: [], assets: [], rules: [] }, cm = A.cm || { kinds: [] }, src = (A.src || { sources: [] }).sources;
    const label = (id) => { try { return this.screenLabel(id) || id; } catch (e) { return id; } };
    const n = md.spotlight.length, i = n ? (s.carIdx || 0) % n : 0, sl = md.spotlight[i] || {};
    const KH = { Launch: 70, Spotlight: 175, Safety: 25 };
    const byId = {}; src.forEach((x) => { byId[x.id] = x; });
    const PV = { V: "Verified", S: "Search-sourced", K: "Lead, to confirm" };
    const ln = (A.ln || {}).event || {};
    const here = (location.href || "").split("#")[0];
    return {
      sMedia: s.screen === "media", sCommunities: s.screen === "communities",
      carHas: n > 0, carKind: sl.kind || "", carTitle: sl.title || "", carBody: sl.body || "", carCta: sl.cta || "", carArt: "./art/" + (sl.art || "hero.svg"),
      carGo: () => sl.screen && this.setState({ screen: sl.screen }), carPos: n ? "Slide " + (i + 1) + " of " + n : "",
      carPrev: () => this.setState({ carIdx: (i - 1 + n) % n, carPaused: true }), carNext: () => this.setState({ carIdx: (i + 1) % n, carPaused: true }),
      carToggle: () => this.setState({ carPaused: !s.carPaused }), carToggleLabel: s.carPaused ? "Play" : "Pause", carPressed: s.carPaused ? "true" : "false",
      carHoldOn: () => this.setState({ carHold: true }), carHoldOff: () => this.setState({ carHold: false }),
      carDots: md.spotlight.map((x, k) => ({ label: "Show slide " + (k + 1) + ": " + x.title, current: k === i ? "true" : "false", go: () => this.setState({ carIdx: k, carPaused: true }),
        style: "width:" + (k === i ? 26 : 10) + "px;height:10px;border-radius:999px;border:0;padding:0;cursor:pointer;transition:width .25s ease;background:" + (k === i ? "oklch(var(--t2) 0.17 " + (KH[x.kind] || 175) + ")" : "rgb(var(--ink-rgb) / 0.3)") + ";" })),
      carPill: "align-self:flex-start;border-radius:999px;padding:3px 11px;font-family:'Space Mono',monospace;font-size:11px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;background:oklch(var(--t2) 0.17 " + (KH[sl.kind] || 175) + ");color:var(--on-accent);",
      carBg: "position:relative;overflow:hidden;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:20px;align-items:center;border-radius:28px;padding:clamp(20px,3vw,32px);border:1px solid oklch(var(--t1) 0.16 " + (KH[sl.kind] || 175) + " / 0.45);background:linear-gradient(135deg,oklch(var(--t1) 0.16 " + (KH[sl.kind] || 175) + " / 0.22),oklch(var(--t1) 0.16 300 / 0.08));",
      mdBlurbs: md.blurbs.map((b, k) => ({ len: b.len, text: b.text, copy: () => this.copy(b.text, "blurb" + k), copied: s.copied === "blurb" + k ? "Copied" : "Copy" })),
      mdFacts: md.facts, mdAssets: md.assets.map((a) => ({ name: a.name, href: "./" + a.file, file: a.file, view: () => this.ampArt(a.name, "./" + a.file, a.name, a.file) })), mdRules: md.rules.map((t) => ({ t })),
      cmIntro: cm.intro || "", cmSafety: cm.safety || "",
      cmKinds: cm.kinds.map((k) => ({ k: k.k, note: k.note || "", hasNote: !!k.note, items: k.ids.map((id) => byId[id]).filter(Boolean).map((x) => ({ name: x.name, what: x.what, url: x.url, nations: x.nations.join(" · "), prov: PV[x.provenance] || x.provenance })) })),
      shareLaunch: this.ampShare(ln.name || "UK Parliament Week", ln.url || here, ln.start, ln.end),
      sharePortal: this.ampShare("Amplify: youth voice, carried further", here),
      copyLink: () => this.copy(here, "link"), copyLinkLabel: s.copied === "link" ? "Link copied" : "Copy link",
      icMedia: this.ampIcon("newspaper", "oklch(var(--t3) 0.16 300)", 16), icComm: this.ampIcon("users", "oklch(var(--t3) 0.16 175)", 16),
      icPrev: this.ampIcon("chart-line", "currentColor", 14), icShare: this.ampIcon("external-link", "currentColor", 13)
    };
  }
'''


def share_block(list_name, title):
    return f'''<section aria-label="{title}" style="{PANEL}">
              <h2 style="margin: 0 0 6px; font-size: 16px; font-weight: 800;">{title}</h2>
              <p style="margin: 0 0 12px; {SMALL}">These open another service only when you choose one. Each has its own terms, privacy rules and minimum age; social media and messaging apps are for adults and allies sharing on a young person's behalf, especially under 16s from spring 2027.</p>
              <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                <sc-for list="{{{{ {list_name} }}}}" as="x" hint-placeholder-count="5"><a href="{{{{ x.href }}}}" target="_blank" rel="noopener noreferrer" style="display: inline-flex; align-items: center; gap: 6px; min-height: 40px; border-radius: 999px; padding: 8px 14px; border: 1px solid rgb(var(--film-rgb) / 0.2); font-size: 13px; font-weight: 700;">{{{{ x.label }}}}<span aria-hidden="true" style="{{{{ icExt }}}}"></span><span class="amp-sr"> (opens in a new tab)</span></a></sc-for>
                <button type="button" onClick="{{{{ copyLink }}}}" style="min-height: 40px; border-radius: 999px; padding: 8px 14px; border: 1px solid oklch(var(--t2) 0.16 145 / 0.7); background: transparent; color: rgb(var(--ink-rgb)); font-size: 13px; font-weight: 700; cursor: pointer;">{{{{ copyLinkLabel }}}}</button>
              </div>
            </section>'''


CAROUSEL = f'''
          <section aria-roledescription="carousel" aria-label="Spotlights" onMouseEnter="{{{{ carHoldOn }}}}" onMouseLeave="{{{{ carHoldOff }}}}" onFocus="{{{{ carHoldOn }}}}" onBlur="{{{{ carHoldOff }}}}">
            <sc-if value="{{{{ carHas }}}}" hint-placeholder-val="{{{{ true }}}}">
            <div aria-roledescription="slide" aria-label="{{{{ carPos }}}}" aria-live="polite" class="amp-slide" style="{{{{ carBg }}}}">
              <div style="display: flex; flex-direction: column; gap: 12px;">
                <span style="{{{{ carPill }}}}">{{{{ carKind }}}}</span>
                <h2 style="margin: 0; font-size: clamp(26px, 3.6vw, 40px); font-weight: 900; line-height: 1.06; letter-spacing: -0.035em; text-wrap: balance;">{{{{ carTitle }}}}</h2>
                <p style="margin: 0; font-size: 15.5px; line-height: 1.6; max-width: 60ch;">{{{{ carBody }}}}</p>
                <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 10px;">
                  <button type="button" onClick="{{{{ carGo }}}}" style="min-height: 44px; border-radius: 999px; padding: 10px 20px; border: 0; background: oklch(var(--t2) 0.16 145); color: var(--on-accent); font-size: 14px; font-weight: 800; cursor: pointer;">{{{{ carCta }}}}</button>
                </div>
              </div>
              <img src="{{{{ carArt }}}}" alt="" style="width: 100%; height: auto; max-height: 200px; object-fit: cover; border-radius: 20px;" />
            </div>
            </sc-if>
            <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 10px; margin-top: 10px;">
              <div role="group" aria-label="Choose a slide" style="display: flex; align-items: center; gap: 7px;"><sc-for list="{{{{ carDots }}}}" as="d" hint-placeholder-count="5"><button type="button" onClick="{{{{ d.go }}}}" aria-label="{{{{ d.label }}}}" aria-current="{{{{ d.current }}}}" style="{{{{ d.style }}}}"></button></sc-for></div>
              <div style="display: flex; gap: 8px;">
                <button type="button" onClick="{{{{ carPrev }}}}" aria-label="Previous slide" style="min-width: 40px; min-height: 40px; border-radius: 999px; border: 1px solid rgb(var(--film-rgb) / 0.2); background: transparent; color: rgb(var(--ink-rgb)); font-size: 16px; cursor: pointer;">&lsaquo;</button>
                <button type="button" onClick="{{{{ carToggle }}}}" aria-pressed="{{{{ carPressed }}}}" style="min-height: 40px; border-radius: 999px; padding: 0 14px; border: 1px solid rgb(var(--film-rgb) / 0.2); background: transparent; color: rgb(var(--ink-rgb)); font-size: 13px; font-weight: 700; cursor: pointer;">{{{{ carToggleLabel }}}}</button>
                <button type="button" onClick="{{{{ carNext }}}}" aria-label="Next slide" style="min-width: 40px; min-height: 40px; border-radius: 999px; border: 1px solid rgb(var(--film-rgb) / 0.2); background: transparent; color: rgb(var(--ink-rgb)); font-size: 16px; cursor: pointer;">&rsaquo;</button>
              </div>
            </div>
          </section>
'''

SCREENS3 = f'''
        <sc-if value="{{{{ sMedia }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          <div>
            <div style="{EYEBROW} color: oklch(var(--t3) 0.16 300);"><span aria-hidden="true" style="{{{{ icMedia }}}}"></span>Help &amp; get involved</div>
            <h1 style="{H1}">Media centre</h1>
            <p style="{LEDE}">Approved descriptions, key facts with their sources, illustrations you can use, and the rules for using them. For anything else, use the contact form.</p>
          </div>
          <div role="note" style="border: 1px solid oklch(var(--t1) 0.16 70 / 0.5); border-radius: 16px; background: oklch(var(--t1) 0.16 70 / 0.1); padding: 12px 16px; font-size: 13.5px; line-height: 1.55;">Amplify is independent and unofficial. Please do not describe it as a UK Youth Parliament, National Youth Agency or UK Parliament service, and do not identify any young person without their agreement and a parent's or carer's consent.</div>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr)); gap: 14px;">
            <sc-for list="{{{{ mdBlurbs }}}}" as="b" hint-placeholder-count="2">
              <div class="amp-card" style="{PANEL} display: flex; flex-direction: column; gap: 10px;"><div style="{LABEL}">About Amplify in {{{{ b.len }}}}</div><p style="margin: 0; font-size: 14px; line-height: 1.6;">{{{{ b.text }}}}</p><button type="button" onClick="{{{{ b.copy }}}}" style="align-self: flex-start; min-height: 38px; border-radius: 999px; padding: 6px 14px; border: 1px solid oklch(var(--t2) 0.16 145 / 0.7); background: transparent; color: rgb(var(--ink-rgb)); font-size: 13px; font-weight: 700; cursor: pointer;">{{{{ b.copied }}}}</button></div>
            </sc-for>
          </div>
          <section style="{PANEL}"><h2 style="margin: 0 0 10px; font-size: 16px; font-weight: 800;">Key facts, with sources</h2><ul style="margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 6px;"><sc-for list="{{{{ mdFacts }}}}" as="f" hint-placeholder-count="3"><li style="font-size: 13.5px; line-height: 1.5;">{{{{ f.f }}}} <span style="color: rgb(var(--ink-rgb) / 0.72);">Source: {{{{ f.src }}}}.</span></li></sc-for></ul></section>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr)); gap: 14px;">
            <section style="{PANEL}"><h2 style="margin: 0 0 10px; font-size: 16px; font-weight: 800;">Illustrations and marks</h2><ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 8px;"><sc-for list="{{{{ mdAssets }}}}" as="a" hint-placeholder-count="4"><li style="font-size: 13.5px;"><button type="button" onClick="{{{{ a.view }}}}" style="border: 0; background: transparent; padding: 4px 0; color: oklch(var(--t4) 0.15 175); font-size: 13.5px; font-weight: 700; text-decoration: underline; cursor: pointer;">{{{{ a.name }}}}</button> <span style="color: rgb(var(--ink-rgb) / 0.7);">&middot; view, print or save</span></li></sc-for></ul><p style="margin: 10px 0 0; {SMALL}">Illustrations are drawn in code from the portal's own shapes and may be reused with credit to Amplify.</p></section>
            <section style="{PANEL}"><h2 style="margin: 0 0 10px; font-size: 16px; font-weight: 800;">Rules for using them</h2><ul style="margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 6px;"><sc-for list="{{{{ mdRules }}}}" as="r" hint-placeholder-count="3"><li style="font-size: 13.5px; line-height: 1.5;">{{{{ r.t }}}}</li></sc-for></ul></section>
          </div>
          {share_block("sharePortal", "Share Amplify into your tools")}
        </div>
        </sc-if>

        <sc-if value="{{{{ sCommunities }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          <div>
            <div style="{EYEBROW} color: oklch(var(--t3) 0.16 175);"><span aria-hidden="true" style="{{{{ icComm }}}}"></span>Help &amp; get involved</div>
            <h1 style="{H1}">Communities, networks and youth groups</h1>
            <p style="{LEDE}">{{{{ cmIntro }}}}</p>
          </div>
          <div role="note" style="border: 1px solid oklch(var(--t1) 0.16 25 / 0.45); border-radius: 16px; background: oklch(var(--t1) 0.16 25 / 0.1); padding: 12px 16px; font-size: 13.5px; line-height: 1.55;">Listing a group is not an endorsement, and each group runs its own safeguarding and privacy policies. {{{{ cmSafety }}}} Worried about anything? Go to <a href="#care">Safeguarding &amp; support</a>.</div>
          <sc-for list="{{{{ cmKinds }}}}" as="k" hint-placeholder-count="4">
            <section style="{PANEL}">
              <h2 style="margin: 0 0 6px; font-size: 18px; font-weight: 800;">{{{{ k.k }}}}</h2>
              <sc-if value="{{{{ k.hasNote }}}}" hint-placeholder-val="{{{{ false }}}}"><p style="margin: 0 0 10px; {SMALL}">{{{{ k.note }}}}</p></sc-if>
              <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 250px), 1fr)); gap: 10px; margin-top: 8px;">
                <sc-for list="{{{{ k.items }}}}" as="x" hint-placeholder-count="4"><div class="amp-card" style="border: 1px solid rgb(var(--film-rgb) / 0.1); border-radius: 16px; padding: 12px 14px; display: flex; flex-direction: column; gap: 6px;"><div style="font-size: 14.5px; font-weight: 800;">{{{{ x.name }}}}</div><div style="{SMALL}">{{{{ x.what }}}}</div><div style="font-size: 12px;">{{{{ x.nations }}}} &middot; <span style="font-style: italic;">{{{{ x.prov }}}}</span></div><a href="{{{{ x.url }}}}" target="_blank" rel="noopener" style="{LINK} font-size: 12.5px;">Visit<span aria-hidden="true" style="{{{{ icExt }}}}"></span><span class="amp-sr"> (opens in a new tab)</span></a></div></sc-for>
              </div>
            </section>
          </sc-for>
        </div>
        </sc-if>
'''

LAUNCH_SHARE = share_block("shareLaunch", "Put UK Parliament Week in your calendar or share it")

GROUP3 = '''      ["communities", "Communities & groups", "dot", 175, 4, "NEW", "communities networks youth groups youth councils clubs scouts guides youth parliament assembly local"],
      ["media", "Media centre", "sq", 300, 4, "NEW", "media centre press blurb description facts illustrations logo brand assets rules share"],
'''


def transforms():
    return [
        ("ext3-group", "the communities hub and media centre join Help & get involved",
         '      ["help", "Help & tutorials",', GROUP3 + '      ["help", "Help & tutorials",', 1),
        ("ext3-hash", "the new screens can be linked to", "|about|home)$/.test(id)", "|about|home|media|communities)$/.test(id)", 1),
        ("ext3-logic", "carousel, media, communities and share logic", "  async loadPetition() {", LOGIC3 + "\n  async loadPetition() {", 1),
        ("ext3-vals", "their values join renderVals", "...this.ampVals2(s),", "...this.ampVals2(s), ...this.ampVals3(s),", 1),
        ("ext3-start", "start the carousel clock once the data has loaded", "loaded: true, failed: !(src && lat && sg) } });", "loaded: true, failed: !(src && lat && sg) } }, () => this.ampCarousel());", 1),
        ("ext3-unmount", "stop the carousel clock if the page unmounts, inside the design's own unmount", "  componentWillUnmount() {\n", "  componentWillUnmount() {\n    if (this._carT) clearInterval(this._carT);\n", 1),
        ("ext3-carousel", "the rolling hero carousel replaces Home's static hero",
         '          <section style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 340px), 1fr)); gap: 20px; align-items: center; border-radius: 28px;',
         CAROUSEL + '          <section style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 340px), 1fr)); gap: 20px; align-items: center; border-radius: 28px;', 1),
        ("ext3-launch-share", "calendar and sharing links for the launch",
         '          <p style="margin: 0; {SMALL}">{{ lnNote }}</p>'.replace("{SMALL}", SMALL),
         LAUNCH_SHARE + '\n          <p style="margin: 0; ' + SMALL + '">{{ lnNote }}</p>', 1),
        ("ext3-screens", "the media centre and communities hub", '        <div data-slot="portal-end" style="display: none;"></div>', SCREENS3 + '\n        <div data-slot="portal-end" style="display: none;"></div>', 1),
    ]
