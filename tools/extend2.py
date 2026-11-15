"""Second set of portal extensions: new/changed flags, release log, help and adoption, feedback, the UK Parliament
Week launch, and guided tours that follow you from screen to screen. Same transform rules as extend.py (B1).

  changes   Release log: every release, what is new (NEW) and changed (UPD), screen by screen, from data/changelog.json
  help      Help & adoption: quick start, user manual, adoption guides per audience, tutorials, and the guided tours
  feedback  Have your say: idea and feature box, bug and issue reporting (GitHub issue forms), and how ideas are handled
  launch    UK Parliament Week launch: dates, plan, activities and a countdown, from data/launch.json
  ribbon    On every screen: the NEW/UPD note for that screen in the current release, or the tour step bar
  flags     Drawer flags come from the release log, so the drawer and the page always agree on what is new or changed
"""
from extend import EYEBROW, H1, LEDE, PANEL, LABEL, SMALL, LINK

REPO = "https://github.com/cyberdudeuk/uk-youth-parliament-amplify"

LOGIC2 = r'''
  ampEntry(id) {
    const ch = (this.state.amp || {}).ch;
    if (!ch) return null;
    const rel = ch.releases.find((r) => r.version === ch.current);
    return rel ? (rel.entries.find((e) => e.screen === id) || null) : null;
  }
  ampFlag(id, designFlag) {
    if (!(this.state.amp || {}).ch) return designFlag;
    const e = this.ampEntry(id);
    return e ? e.kind : "";
  }
  ampVals2(s) {
    const hm = (s.amp || {}).hm || {};
    const ab = (s.amp || {}).ab || { rationale: [], aims: [], goals: [], objectives: [], outcomes: [] };
    const A = s.amp || {}, ch = A.ch || { releases: [], current: "" }, hp = A.hp || { quickstart: [], manual: [], adoption: [], tutorials: [] }, ln = A.ln || { event: {}, plan: [], activities: [] };
    const KH = { NEW: 145, UPD: 70 };
    const kindLabel = (k) => (k === "NEW" ? "New" : "Updated");
    const label = (id) => { try { return this.screenLabel(id) || id; } catch (e) { return id; } };
    const e = this.ampEntry(s.screen);
    const ig = A.ig || { screens: [], classes: {}, views: [] };
    const igE = ig.screens.find((x) => x.screen === s.screen) || null;
    const IH = { Sourced: 145, Model: 215, Sample: 25, Generated: 300, Editorial: 70 };
    const igFlag = !!igE && igE.class !== "Sourced" && igE.class !== "Editorial";
    // tour step bar
    const T = this.TOURS[s.tour] || null, at = s.tourAt;
    const onTour = !!(T && typeof at === "number" && T.steps[at] && T.steps[at][0] === s.screen);
    const nextStep = onTour && T.steps[at + 1] ? T.steps[at + 1] : null;
    // launch countdown
    const start = ln.event.start ? Date.parse(ln.event.start + "T00:00:00Z") : NaN, end = ln.event.end ? Date.parse(ln.event.end + "T23:59:59Z") : NaN, now = Date.now();
    const daysTo = isNaN(start) ? null : Math.ceil((start - now) / 864e5);
    const lnState = isNaN(start) ? "" : now < start ? (daysTo === 1 ? "1 day to go" : daysTo + " days to go") : now <= end ? "Happening this week" : "Launched";
    return {
      sHome: s.screen === "home", hmWhat: hm.what || "", hmFor: hm.for || "", hmSteps: (hm.steps || []).map((x, i) => ({ t: x.t, d: x.d, n: String(i + 1) })),
      hmTiles: (hm.tiles || []).map((x) => ({ label: label(x.id), d: x.d, go: () => this.setState({ screen: x.id }), icon: this.ampIcon(({ hub: "megaphone", sources: "book-open-check", care: "heart-handshake", help: "compass", trust: "shield-check", feedback: "messages-square", latest: "newspaper", about: "info" })[x.id] || "layers", "oklch(var(--t3) 0.16 175)", 24) })),
      icHome: this.ampIcon("compass", "oklch(var(--t3) 0.16 175)", 16), icLife: this.ampIcon("life-buoy", "oklch(var(--t3) 0.16 25)", 22),
      goCare: () => this.setState({ screen: "care" }),
      sAbout: s.screen === "about", abWho: ab.who || "", abProfile: ab.profile || "#", abImpartial: ab.impartial || "", abMission: ab.mission || "", abNote: ab.evidence_note || "",
      abRationale: ab.rationale.map((t) => ({ t })), abAims: ab.aims.map((t) => ({ t })), abGoals: ab.goals.map((t) => ({ t })), abObjectives: ab.objectives.map((t) => ({ t })), abOutcomes: ab.outcomes,
      icAbout: this.ampIcon("info", "oklch(var(--t3) 0.16 175)", 16), icGit: this.ampIcon("git-branch", "currentColor", 15),
      sChanges: s.screen === "changes", sHelp: s.screen === "help", sFeedback: s.screen === "feedback", sLaunch: s.screen === "launch",
      rbShow: !onTour && !!e, rbKind: e ? kindLabel(e.kind) + " in " + ch.current : "", rbWhat: e ? e.what : "",
      rbStyle: "display:flex;flex-wrap:wrap;align-items:center;gap:10px;border-radius:16px;padding:10px 14px;font-size:13.5px;line-height:1.45;border:1px solid oklch(var(--t2) 0.16 " + (e ? KH[e.kind] || 175 : 175) + " / 0.5);background:oklch(var(--t1) 0.16 " + (e ? KH[e.kind] || 175 : 175) + " / 0.14);",
      rbPill: "border-radius:999px;padding:2px 10px;font-family:'Space Mono',monospace;font-size:11px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;background:oklch(var(--t2) 0.16 " + (e ? KH[e.kind] || 175 : 175) + ");color:var(--on-accent);",
      goChanges: () => this.setState({ screen: "changes" }),
      igShow: igFlag, igClass: igE ? (igE.class === "Sample" ? "Sample data" : igE.class === "Model" ? "Planning model" : igE.class === "Generated" ? "Generated text" : igE.class) : "",
      igWhy: igE ? igE.why + (igE.check ? " " + igE.check : "") : "",
      igStyle: "display:flex;flex-wrap:wrap;align-items:center;gap:10px;border-radius:16px;padding:10px 14px;font-size:13.5px;line-height:1.45;border:1px dashed oklch(var(--t2) 0.17 " + (igE ? IH[igE.class] || 25 : 25) + " / 0.8);background:oklch(var(--t1) 0.16 " + (igE ? IH[igE.class] || 25 : 25) + " / 0.12);",
      igPill: "border-radius:6px;padding:2px 9px;font-family:'Space Mono',monospace;font-size:11px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;border:1.5px solid oklch(var(--t3) 0.17 " + (igE ? IH[igE.class] || 25 : 25) + ");color:oklch(var(--t4) 0.15 " + (igE ? IH[igE.class] || 25 : 25) + ");",
      igAppShow: s.view === "app" || s.view === "both", igAppWhy: (ig.views[0] || {}).why || "",
      igRows: ig.screens.map((x) => ({ screen: label(x.screen), cls: x.class, why: x.why, style: "font-family:'Space Mono',monospace;font-size:11px;font-weight:700;color:oklch(var(--t4) 0.15 " + (IH[x.class] || 25) + ");" })),
      igClasses: Object.keys(ig.classes).map((k) => ({ k, v: ig.classes[k], style: "font-weight:800;color:oklch(var(--t4) 0.15 " + (IH[k] || 25) + ");" })),
      tbShow: onTour, tbTitle: onTour ? T.label : "", tbStep: onTour ? "Step " + (at + 1) + " of " + T.steps.length + ": " + T.steps[at][1] : "", tbBody: onTour ? T.steps[at][2] : "",
      tbHasNext: !!nextStep, tbNextLabel: nextStep ? "Next: " + nextStep[1] : "", tbNext: () => nextStep && this.setState({ screen: nextStep[0], tourAt: at + 1 }),
      tbBack: () => this.setState({ screen: "guide", tourAt: null }), tbEnd: () => this.setState({ tourAt: null }),
      releases: ch.releases.map((r) => ({ version: r.version, date: this.ampDate(r.date), status: r.status, title: r.title, summary: r.summary,
        current: r.version === ch.current, hasEntries: r.entries.length > 0,
        entries: r.entries.map((x) => ({ kind: kindLabel(x.kind), screen: label(x.screen), what: x.what, go: () => this.setState({ screen: x.screen }),
          pill: "flex:0 0 auto;border-radius:999px;padding:2px 9px;font-family:'Space Mono',monospace;font-size:10.5px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;background:oklch(var(--t1) 0.16 " + (KH[x.kind] || 175) + " / 0.28);color:oklch(var(--t4) 0.14 " + (KH[x.kind] || 175) + ");" })),
        dot: "flex:0 0 14px;width:14px;height:14px;border-radius:50%;margin-top:4px;background:oklch(var(--t2) 0.17 " + (r.version === ch.current ? 145 : r.status === "Planned launch" ? 70 : 215) + ");" })),
      hpQuick: hp.quickstart.map((t, i) => ({ t, n: String(i + 1) })), hpManual: hp.manual, hpAdopt: hp.adoption.map((a) => ({ who: a.who, steps: a.steps.map((t) => ({ t })) })),
      hpTut: hp.tutorials.map((t) => ({ title: t.title, steps: t.steps.map((x, i) => ({ t: x, n: String(i + 1) })), go: () => this.setState({ screen: t.screen }), cta: "Start on " + label(t.screen) })),
      hpTours: Object.keys(this.TOURS).map((k) => ({ label: this.TOURS[k].label, meta: this.TOURS[k].steps.length + " steps", go: () => this.setState({ tour: k, screen: this.TOURS[k].steps[0][0], tourAt: 0 }) })),
      lnName: ln.event.name || "UK Parliament Week", lnDates: ln.event.start ? this.ampDate(ln.event.start) + " to " + this.ampDate(ln.event.end) : "", lnState, lnUrl: ln.event.url || "#",
      lnWhy: ln.why || "", lnNote: ln.note || "", lnPlan: ln.plan, lnActs: ln.activities.map((a) => ({ title: a.title, what: a.what, go: () => this.setState({ screen: a.screen }), cta: "Open " + label(a.screen) })),
      lnDays: daysTo !== null && daysTo > 0 ? String(daysTo) : "0", lnShowDays: daysTo !== null && daysTo > 0,
      lnHubShow: s.screen === "hub" && !!ln.event.start && now <= end, goLaunch: () => this.setState({ screen: "launch" }),
      icChanges: this.ampIcon("git-branch", "oklch(var(--t3) 0.16 145)", 16), icHelp: this.ampIcon("compass", "oklch(var(--t3) 0.16 300)", 16),
      icFeedback: this.ampIcon("messages-square", "oklch(var(--t3) 0.16 175)", 16), icLaunch: this.ampIcon("landmark", "oklch(var(--t3) 0.16 70)", 16),
      icIdea: this.ampIcon("sparkles", "oklch(var(--t3) 0.16 300)", 26), icBugBig: this.ampIcon("bug", "oklch(var(--t3) 0.16 25)", 26),
      icAsk: this.ampIcon("info", "oklch(var(--t3) 0.16 215)", 26), icList: this.ampIcon("list-checks", "oklch(var(--t3) 0.16 145)", 26),
      icTour: this.ampIcon("route", "currentColor", 16), icFlag: this.ampIcon("flag-triangle-right", "currentColor", 15)
    };
  }
'''

TOURS_ADD = '''    newhere: {
      label: "New here", kind: "quick tour", shape: "ring", hue: 145,
      title: "Five minutes to find your way around",
      intro: "Five stops: what Amplify is for, how to stay safe, where the facts come from, what has changed, and how to tell us what you think.",
      steps: [
        ["hub", "Start at the campaign hub", "The headline: why most youth petitions stall, and what Amplify does about it."],
        ["care", "Know where help is", "Free, confidential helplines, checked and dated. In an emergency, call 999."],
        ["sources", "Back every claim", "Filter by theme, nation and who it is for. Cards say how sure we are."],
        ["changes", "See what is new", "Every release, screen by screen. The drawer flags match."],
        ["feedback", "Have your say", "Ideas, features, bugs: all through public forms, with no personal details."]
      ]
    },
    parent: {
      label: "Parents & carers", kind: "role tour", shape: "dia", hue: 340,
      title: "Backing a young campaigner, safely",
      intro: "For parents, carers, guardians and anyone with parental responsibility: what your child is using, how it keeps them safe, and how you can help.",
      steps: [
        ["trust", "Read the parents' section", "What Amplify asks for (nothing), the under-13 rule, and the under-16 social media ban."],
        ["care", "Keep the helplines to hand", "Childline for them, the NSPCC Helpline for you."],
        ["kit", "See the parent pack", "The toolkit writes a version for parents: what the campaign is and how to support it."],
        ["sources", "Choose Parents & carers", "Sources picked for adults, from the Children's Commissioners to the ICO's Children's code."],
        ["feedback", "Tell us what would help", "Parents' ideas shape the next release."]
      ]
    },
    ukpw: {
      label: "UK Parliament Week", kind: "event tour", shape: "sq", hue: 70,
      title: "Use Amplify in UK Parliament Week, 23 to 29 November 2026",
      intro: "Four activities for schools and youth groups during the week, each using a screen of the portal.",
      steps: [
        ["launch", "Open the launch plan", "Dates, the plan and the activities, with a countdown."],
        ["issues", "Run your own ballot", "Vote on which issue your group should campaign on."],
        ["post", "Learn from a stalled petition", "Why 754954 fell short, and what to do differently."],
        ["map", "Write to your MP", "Find your MP and draft a letter together."]
      ]
    },
'''


def btn(handler, label, primary=False, icon=None):
    bg = "oklch(var(--t2) 0.16 145)" if primary else "transparent"
    fg = "var(--on-accent)" if primary else "rgb(var(--ink-rgb) / 0.9)"
    ic = f'<span aria-hidden="true" style="{{{{ {icon} }}}}"></span>' if icon else ""
    return (f'<button type="button" onClick="{{{{ {handler} }}}}" style="display: inline-flex; align-items: center; gap: 7px; min-height: 40px; border-radius: 999px; padding: 8px 16px; '
            f'font-size: 13.5px; font-weight: 700; cursor: pointer; border: 1px solid oklch(var(--t2) 0.16 145 / 0.7); background: {bg}; color: {fg};">{ic}{label}</button>')


def form_card(icon, title, body, template, cta):
    return f'''<div class="amp-card" style="{PANEL} display: flex; flex-direction: column; gap: 10px;">
                <span aria-hidden="true" style="{{{{ {icon} }}}}"></span>
                <h2 style="margin: 0; font-size: 17px; font-weight: 800;">{title}</h2>
                <p style="margin: 0; font-size: 13.5px; line-height: 1.55;">{body}</p>
                <a href="{REPO}/issues/new?template={template}" target="_blank" rel="noopener" style="{LINK} margin-top: auto;">{cta}<span aria-hidden="true" style="{{{{ icExt }}}}"></span><span class="amp-sr"> (opens GitHub in a new tab)</span></a>
              </div>'''


RIBBON = f'''
        <sc-if value="{{{{ tbShow }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div role="region" aria-label="Guided tour" class="amp-tourbar" style="display: flex; flex-wrap: wrap; align-items: center; gap: 12px; border-radius: 18px; padding: 12px 16px; border: 1px solid oklch(var(--t2) 0.16 300 / 0.6); background: linear-gradient(120deg, oklch(var(--t1) 0.16 300 / 0.22), oklch(var(--t1) 0.16 175 / 0.12));">
          <span aria-hidden="true" style="{{{{ icTour }}}}"></span>
          <div style="flex: 1 1 260px; min-width: 0;"><div style="{LABEL}">Tour &middot; {{{{ tbTitle }}}}</div><div style="font-size: 14.5px; font-weight: 800; margin-top: 2px;">{{{{ tbStep }}}}</div><div style="{SMALL} margin-top: 2px;">{{{{ tbBody }}}}</div></div>
          <div style="display: flex; flex-wrap: wrap; gap: 8px;">
            <sc-if value="{{{{ tbHasNext }}}}" hint-placeholder-val="{{{{ false }}}}">{btn("tbNext", "{{ tbNextLabel }}", True)}</sc-if>
            {btn("tbBack", "All tour steps")}
            {btn("tbEnd", "End tour")}
          </div>
        </div>
        </sc-if>
        <sc-if value="{{{{ rbShow }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div role="note" style="{{{{ rbStyle }}}}"><span style="{{{{ rbPill }}}}">{{{{ rbKind }}}}</span><span style="flex: 1 1 240px; min-width: 0;">{{{{ rbWhat }}}}</span><button type="button" onClick="{{{{ goChanges }}}}" style="border: 0; background: transparent; color: inherit; text-decoration: underline; font-size: 13px; cursor: pointer; padding: 6px;">Release log</button></div>
        </sc-if>
        <sc-if value="{{{{ igShow }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div role="note" aria-label="About the content on this screen" style="{{{{ igStyle }}}}"><span style="{{{{ igPill }}}}">{{{{ igClass }}}}</span><span style="flex: 1 1 260px; min-width: 0;">{{{{ igWhy }}}}</span></div>
        </sc-if>
        <sc-if value="{{{{ igAppShow }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div role="note" style="border-radius: 14px; padding: 8px 14px; font-size: 13px; border: 1px dashed oklch(var(--t2) 0.17 25 / 0.8); background: oklch(var(--t1) 0.16 25 / 0.1);"><span style="font-weight: 800;">App view is a design concept.</span> {{{{ igAppWhy }}}}</div>
        </sc-if>
        <sc-if value="{{{{ lnHubShow }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div class="amp-card" style="display: flex; flex-wrap: wrap; align-items: center; gap: 14px; border-radius: 18px; padding: 12px 16px; border: 1px solid oklch(var(--t2) 0.16 70 / 0.55); background: linear-gradient(120deg, oklch(var(--t1) 0.16 70 / 0.2), oklch(var(--t1) 0.16 25 / 0.08));">
          <span aria-hidden="true" style="{{{{ icLaunch }}}}"></span>
          <div style="flex: 1 1 240px; min-width: 0;"><div style="{LABEL}">Launching at {{{{ lnName }}}}</div><div style="font-size: 14.5px; font-weight: 800;">{{{{ lnDates }}}} &middot; <span class="amp-count">{{{{ lnState }}}}</span></div></div>
          {btn("goLaunch", "See the launch plan", True)}
        </div>
        </sc-if>
'''

SCREENS2 = f'''
        <sc-if value="{{{{ sChanges }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          <div>
            <div style="{EYEBROW} color: oklch(var(--t3) 0.16 145);"><span aria-hidden="true" style="{{{{ icChanges }}}}"></span>Sources &amp; updates</div>
            <h1 style="{H1}">Release log</h1>
            <p style="{LEDE}">Every release, newest first, and exactly what is new or changed on which screen. The same flags appear in the drawer and as a note at the top of each screen.</p>
          </div>
          <ol style="list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 14px;">
            <sc-for list="{{{{ releases }}}}" as="r" hint-placeholder-count="3">
              <li class="amp-card" style="{PANEL} display: flex; gap: 16px;">
                <span aria-hidden="true" style="{{{{ r.dot }}}}"></span>
                <div style="flex: 1 1 auto; min-width: 0; display: flex; flex-direction: column; gap: 8px;">
                  <div style="{LABEL}">Version {{{{ r.version }}}} &middot; <time>{{{{ r.date }}}}</time> &middot; {{{{ r.status }}}}</div>
                  <h2 style="margin: 0; font-size: 18px; font-weight: 800; letter-spacing: -0.015em;">{{{{ r.title }}}}</h2>
                  <p style="margin: 0; font-size: 13.5px; line-height: 1.55;">{{{{ r.summary }}}}</p>
                  <sc-if value="{{{{ r.hasEntries }}}}" hint-placeholder-val="{{{{ false }}}}">
                    <ul style="list-style: none; margin: 4px 0 0; padding: 0; display: flex; flex-direction: column; gap: 8px;">
                      <sc-for list="{{{{ r.entries }}}}" as="x" hint-placeholder-count="5">
                        <li style="display: flex; flex-wrap: wrap; align-items: baseline; gap: 10px; font-size: 13.5px; line-height: 1.5;"><span style="{{{{ x.pill }}}}">{{{{ x.kind }}}}</span>
                          <button type="button" onClick="{{{{ x.go }}}}" style="border: 0; background: transparent; color: inherit; font-weight: 800; text-decoration: underline; cursor: pointer; padding: 0; font-size: 13.5px;">{{{{ x.screen }}}}</button><span style="flex: 1 1 260px; min-width: 0;">{{{{ x.what }}}}</span></li>
                      </sc-for>
                    </ul>
                  </sc-if>
                </div>
              </li>
            </sc-for>
          </ol>
          <p style="margin: 0; {SMALL}">The same log is kept in the repository as CHANGELOG.md, generated from the same data.</p>
        </div>
        </sc-if>

        <sc-if value="{{{{ sHelp }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          <div>
            <div style="{EYEBROW} color: oklch(var(--t3) 0.16 300);"><span aria-hidden="true" style="{{{{ icHelp }}}}"></span>Help &amp; get involved</div>
            <h1 style="{H1}">Help, tutorials and guided tours</h1>
            <p style="{LEDE}">A user manual, an adoption guide for each kind of user, step-by-step tutorials, and tours that walk you from screen to screen with a step bar at the top.</p>
          </div>
          <section aria-labelledby="amp-tours" style="border: 1px solid oklch(var(--t1) 0.16 300 / 0.4); border-radius: 24px; background: linear-gradient(150deg, oklch(var(--t1) 0.16 300 / 0.14), rgb(var(--film-rgb) / 0.03)); padding: 22px 24px;">
            <h2 id="amp-tours" style="margin: 0 0 12px; font-size: 19px; font-weight: 900; letter-spacing: -0.025em;">Take a guided tour</h2>
            <div style="display: flex; flex-wrap: wrap; gap: 10px;">
              <sc-for list="{{{{ hpTours }}}}" as="t" hint-placeholder-count="5">
                <button type="button" onClick="{{{{ t.go }}}}" style="display: inline-flex; align-items: center; gap: 8px; min-height: 42px; border-radius: 999px; padding: 8px 16px; border: 1px solid oklch(var(--t2) 0.16 300 / 0.6); background: rgb(var(--film-rgb) / 0.05); color: rgb(var(--ink-rgb)); font-size: 13.5px; font-weight: 700; cursor: pointer;"><span aria-hidden="true" style="{{{{ icTour }}}}"></span>{{{{ t.label }}}} <span style="font-weight: 400; color: rgb(var(--ink-rgb) / 0.7);">&middot; {{{{ t.meta }}}}</span></button>
              </sc-for>
            </div>
          </section>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr)); gap: 14px;">
            <section aria-labelledby="amp-quick" style="{PANEL}">
              <h2 id="amp-quick" style="margin: 0 0 12px; font-size: 17px; font-weight: 800;">Quick start</h2>
              <ol style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 10px;">
                <sc-for list="{{{{ hpQuick }}}}" as="q" hint-placeholder-count="5"><li style="display: flex; gap: 12px;"><span aria-hidden="true" style="flex: 0 0 24px; height: 24px; display: grid; place-items: center; border-radius: 50%; background: oklch(var(--t2) 0.16 300); color: var(--on-accent); font-family: 'Space Mono', monospace; font-size: 12px; font-weight: 700;">{{{{ q.n }}}}</span><span style="font-size: 13.5px; line-height: 1.55;">{{{{ q.t }}}}</span></li></sc-for>
              </ol>
            </section>
            <section aria-labelledby="amp-manual" style="{PANEL}">
              <h2 id="amp-manual" style="margin: 0 0 12px; font-size: 17px; font-weight: 800;">User manual</h2>
              <dl style="margin: 0; display: flex; flex-direction: column; gap: 10px;">
                <sc-for list="{{{{ hpManual }}}}" as="m" hint-placeholder-count="6"><div><dt style="font-size: 14px; font-weight: 800;">{{{{ m.group }}}}</dt><dd style="margin: 2px 0 0; {SMALL}">{{{{ m.what }}}}</dd></div></sc-for>
              </dl>
            </section>
          </div>
          <section aria-labelledby="amp-adopt" style="{PANEL}">
            <h2 id="amp-adopt" style="margin: 0 0 12px; font-size: 17px; font-weight: 800;">Adoption guide: getting started where you are</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 240px), 1fr)); gap: 14px;">
              <sc-for list="{{{{ hpAdopt }}}}" as="a" hint-placeholder-count="4">
                <div style="border-left: 3px solid oklch(var(--t2) 0.16 300); padding-left: 12px;"><div style="font-size: 14.5px; font-weight: 800; margin-bottom: 6px;">{{{{ a.who }}}}</div>
                  <ol style="margin: 0; padding-left: 18px; display: flex; flex-direction: column; gap: 5px;"><sc-for list="{{{{ a.steps }}}}" as="x" hint-placeholder-count="4"><li style="font-size: 13px; line-height: 1.5;">{{{{ x.t }}}}</li></sc-for></ol></div>
              </sc-for>
            </div>
          </section>
          <section aria-labelledby="amp-tut">
            <h2 id="amp-tut" style="margin: 0 0 12px; font-size: 17px; font-weight: 800;">Tutorials</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr)); gap: 14px;">
              <sc-for list="{{{{ hpTut }}}}" as="t" hint-placeholder-count="3">
                <div class="amp-card" style="{PANEL} display: flex; flex-direction: column; gap: 10px;">
                  <h3 style="margin: 0; font-size: 15.5px; font-weight: 800;">{{{{ t.title }}}}</h3>
                  <ol style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 7px;"><sc-for list="{{{{ t.steps }}}}" as="x" hint-placeholder-count="4"><li style="display: flex; gap: 10px; font-size: 13px; line-height: 1.5;"><span style="font-family: 'Space Mono', monospace; font-weight: 700; color: oklch(var(--t4) 0.14 300);">{{{{ x.n }}}}</span><span>{{{{ x.t }}}}</span></li></sc-for></ol>
                  <div style="margin-top: auto;">{btn("t.go", "{{ t.cta }}")}</div>
                </div>
              </sc-for>
            </div>
          </section>
        </div>
        </sc-if>

        <sc-if value="{{{{ sFeedback }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          <div>
            <div style="{EYEBROW} color: oklch(var(--t3) 0.16 175);"><span aria-hidden="true" style="{{{{ icFeedback }}}}"></span>Help &amp; get involved</div>
            <h1 style="{H1}">Have your say: ideas, features, bugs</h1>
            <p style="{LEDE}">Amplify is built with the people who use it. Suggest a feature, share an idea, or tell us something is broken or wrong. Every form is public on GitHub, so never include your name, school, contact details or anything that identifies you or someone else.</p>
          </div>
          <div role="note" style="border: 1px solid oklch(var(--t1) 0.16 25 / 0.45); border-radius: 18px; background: oklch(var(--t1) 0.16 25 / 0.1); padding: 14px 16px; font-size: 13.5px; line-height: 1.55;">If you are under 18, ask a trusted adult before posting. If something has upset you or you are worried about your safety, do not post it here: go to <a href="#care">Safeguarding &amp; support</a>. Under 13? GitHub accounts start at 13, so ask a parent, carer or youth worker to post for you. Cannot use the forms? Ask your MYP, a youth worker or a trusted adult to raise it for you.</div>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr)); gap: 14px;">
            {form_card("icIdea", "Idea or feature", "Something Amplify should do, a screen it should have, or a better way to do something it already does.", "idea.yml", "Suggest an idea")}
            {form_card("icBugBig", "Bug or problem", "Something broken, confusing, inaccessible or slow, on any device.", "bug.yml", "Report a bug")}
            {form_card("icAsk", "Wrong or out of date", "A fact, figure, link or helpline that is wrong or has changed.", "contact.yml", "Tell us what changed")}
          </div>
          <section aria-labelledby="amp-handled" style="{PANEL}">
            <div style="{EYEBROW} color: oklch(var(--t3) 0.16 145); margin-bottom: 6px;"><span aria-hidden="true" style="{{{{ icCheck }}}}"></span>What happens next</div>
            <h2 id="amp-handled" style="margin: 0 0 12px; font-size: 18px; font-weight: 800;">From your idea to the release log</h2>
            <ol style="margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 7px; font-size: 13.5px; line-height: 1.55;">
              <li>Every new idea, bug or correction is read at the weekly upkeep run and labelled.</li>
              <li>A safety-critical correction, such as a helpline that has changed, is fixed first.</li>
              <li>Accepted changes are built, checked and listed in the release log with the screen they affect.</li>
              <li>If an idea is not taken forward, the reason is written on the issue, so you can see the decision.</li>
            </ol>
            <p style="margin: 12px 0 0;"><a href="{REPO}/issues" target="_blank" rel="noopener" style="{LINK}">See every open idea and bug<span aria-hidden="true" style="{{{{ icExt }}}}"></span><span class="amp-sr"> (opens GitHub in a new tab)</span></a></p>
          </section>
        </div>
        </sc-if>

        <sc-if value="{{{{ sLaunch }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          <div>
            <div style="{EYEBROW} color: oklch(var(--t3) 0.16 70);"><span aria-hidden="true" style="{{{{ icLaunch }}}}"></span>Help &amp; get involved</div>
            <h1 style="{H1}">Launching at {{{{ lnName }}}}</h1>
            <p style="{LEDE}">{{{{ lnWhy }}}}</p>
          </div>
          <div class="amp-card" style="display: flex; flex-wrap: wrap; align-items: center; gap: 22px; border-radius: 24px; padding: 22px 24px; border: 1px solid oklch(var(--t2) 0.16 70 / 0.55); background: linear-gradient(130deg, oklch(var(--t1) 0.16 70 / 0.24), oklch(var(--t1) 0.16 25 / 0.1));">
            <sc-if value="{{{{ lnShowDays }}}}" hint-placeholder-val="{{{{ true }}}}"><div style="text-align: center;"><div class="amp-count" style="font-size: clamp(44px, 8vw, 64px); font-weight: 900; line-height: 1; letter-spacing: -0.04em; color: oklch(var(--t4) 0.16 70);">{{{{ lnDays }}}}</div><div style="{LABEL}">days to go</div></div></sc-if>
            <div style="flex: 1 1 260px; min-width: 0;"><div style="font-size: 20px; font-weight: 900;">{{{{ lnDates }}}}</div><div style="font-size: 14px; margin-top: 4px;" role="status">{{{{ lnState }}}}</div>
              <a href="{{{{ lnUrl }}}}" target="_blank" rel="noopener" style="{LINK} margin-top: 8px;">About UK Parliament Week and its free kits<span aria-hidden="true" style="{{{{ icExt }}}}"></span><span class="amp-sr"> (opens in a new tab)</span></a></div>
          </div>
          <section aria-labelledby="amp-plan" style="{PANEL}">
            <h2 id="amp-plan" style="margin: 0 0 12px; font-size: 18px; font-weight: 800;">The launch plan</h2>
            <ol style="list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 10px;">
              <sc-for list="{{{{ lnPlan }}}}" as="p" hint-placeholder-count="4"><li style="display: grid; grid-template-columns: minmax(120px, 170px) minmax(0, 1fr); gap: 12px; font-size: 13.5px; line-height: 1.5;"><span style="font-weight: 800; color: oklch(var(--t4) 0.14 70);">{{{{ p.when }}}}</span><span>{{{{ p.what }}}}</span></li></sc-for>
            </ol>
          </section>
          <section aria-labelledby="amp-acts">
            <h2 id="amp-acts" style="margin: 0 0 12px; font-size: 18px; font-weight: 800;">Activities for schools and youth groups during the week</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 240px), 1fr)); gap: 14px;">
              <sc-for list="{{{{ lnActs }}}}" as="a" hint-placeholder-count="4">
                <div class="amp-card" style="{PANEL} display: flex; flex-direction: column; gap: 10px;"><h3 style="margin: 0; font-size: 15.5px; font-weight: 800;">{{{{ a.title }}}}</h3><p style="margin: 0; font-size: 13.5px; line-height: 1.55;">{{{{ a.what }}}}</p><div style="margin-top: auto;">{btn("a.go", "{{ a.cta }}")}</div></div>
              </sc-for>
            </div>
          </section>
          <p style="margin: 0; {SMALL}">{{{{ lnNote }}}}</p>
        </div>
        </sc-if>
'''

HOME = '\n        <sc-if value="{{ sHome }}" hint-placeholder-val="{{ false }}">\n        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">\n          <section style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 340px), 1fr)); gap: 20px; align-items: center; border-radius: 28px; padding: clamp(20px, 3vw, 34px); border: 1px solid oklch(var(--t1) 0.16 175 / 0.35); background: linear-gradient(140deg, oklch(var(--t1) 0.16 175 / 0.16), oklch(var(--t1) 0.16 300 / 0.08));">\n            <div style="display: flex; flex-direction: column; gap: 12px;">\n              <div style="display: flex; align-items: center; gap: 9px; font-family: \'Space Mono\', monospace; font-size: 10.5px; letter-spacing: 0.16em; text-transform: uppercase; color: oklch(var(--t3) 0.16 175);"><span aria-hidden="true" style="{{ icHome }}"></span>Home</div>\n              <h1 style="margin: 0; font-size: clamp(30px, 4vw, 44px); font-weight: 900; line-height: 1.05; letter-spacing: -0.04em; text-wrap: balance;">Youth voice, carried further</h1>\n              <p style="margin: 0; font-size: 16px; line-height: 1.6; max-width: 62ch;">{{ hmWhat }}</p>\n              <p style="margin: 0; font-size: 14.5px; line-height: 1.55; max-width: 62ch; color: rgb(var(--ink-rgb) / 0.82);">{{ hmFor }}</p>\n            </div>\n            <img src="./art/hero.svg" alt="" style="width: 100%; height: auto; max-height: 220px; object-fit: cover; border-radius: 20px;" />\n          </section>\n          <section aria-labelledby="amp-howto">\n            <h2 id="amp-howto" style="margin: 0 0 12px; font-size: 19px; font-weight: 900; letter-spacing: -0.025em;">How to use Amplify</h2>\n            <ol style="list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 220px), 1fr)); gap: 12px;">\n              <sc-for list="{{ hmSteps }}" as="x" hint-placeholder-count="4"><li class="amp-card" style="border: 1px solid rgb(var(--film-rgb) / 0.12); border-radius: 20px; background: rgb(var(--film-rgb) / 0.04); padding: 16px 18px;"><div style="display: flex; align-items: center; gap: 10px;"><span aria-hidden="true" class="amp-count" style="font-size: 28px; font-weight: 900; color: oklch(var(--t4) 0.16 175);">{{ x.n }}</span><span style="font-size: 15px; font-weight: 800;">{{ x.t }}</span></div><p style="margin: 6px 0 0; font-size: 13.5px; line-height: 1.5;">{{ x.d }}</p></li></sc-for>\n            </ol>\n          </section>\n          <section aria-labelledby="amp-tourin" style="border: 1px solid oklch(var(--t1) 0.16 300 / 0.4); border-radius: 22px; background: oklch(var(--t1) 0.16 300 / 0.1); padding: 18px 20px;">\n            <h2 id="amp-tourin" style="margin: 0 0 10px; font-size: 17px; font-weight: 800;">Start with a guided tour for you</h2>\n            <div style="display: flex; flex-wrap: wrap; gap: 10px;">\n              <sc-for list="{{ hpTours }}" as="t" hint-placeholder-count="5"><button type="button" onClick="{{ t.go }}" style="display: inline-flex; align-items: center; gap: 8px; min-height: 42px; border-radius: 999px; padding: 8px 16px; border: 1px solid oklch(var(--t2) 0.16 300 / 0.6); background: rgb(var(--film-rgb) / 0.05); color: rgb(var(--ink-rgb)); font-size: 13.5px; font-weight: 700; cursor: pointer;"><span aria-hidden="true" style="{{ icTour }}"></span>{{ t.label }}</button></sc-for>\n            </div>\n          </section>\n          <section aria-labelledby="amp-routes">\n            <h2 id="amp-routes" style="margin: 0 0 12px; font-size: 19px; font-weight: 900; letter-spacing: -0.025em;">Go straight to</h2>\n            <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 220px), 1fr)); gap: 12px;">\n              <sc-for list="{{ hmTiles }}" as="x" hint-placeholder-count="8"><button type="button" onClick="{{ x.go }}" class="amp-card" style="text-align: left; display: flex; flex-direction: column; gap: 8px; border: 1px solid rgb(var(--film-rgb) / 0.12); border-radius: 20px; background: rgb(var(--film-rgb) / 0.04); color: rgb(var(--ink-rgb)); padding: 16px 18px; cursor: pointer;"><span aria-hidden="true" style="{{ x.icon }}"></span><span style="font-size: 15px; font-weight: 800;">{{ x.label }}</span><span style="font-size: 13px; line-height: 1.5; color: rgb(var(--ink-rgb) / 0.82);">{{ x.d }}</span></button></sc-for>\n            </div>\n          </section>\n          <div role="note" style="display: flex; flex-wrap: wrap; align-items: center; gap: 12px; border-radius: 18px; padding: 12px 16px; border: 1px solid oklch(var(--t1) 0.16 25 / 0.5); background: oklch(var(--t1) 0.16 25 / 0.1);"><span aria-hidden="true" style="{{ icLife }}"></span><span style="flex: 1 1 260px; font-size: 14px; line-height: 1.5;">Need to talk to someone now? Childline is free on <span style="font-weight: 800;">0800 1111</span>, any time. In an emergency, call <span style="font-weight: 800;">999</span>.</span><button type="button" onClick="{{ goCare }}" style="min-height: 40px; border-radius: 999px; padding: 8px 16px; border: 1px solid oklch(var(--t2) 0.16 25 / 0.7); background: transparent; color: rgb(var(--ink-rgb)); font-weight: 700; cursor: pointer;">All helplines</button></div>\n        </div>\n        </sc-if>\n'
ABOUT = '\n        <sc-if value="{{ sAbout }}" hint-placeholder-val="{{ false }}">\n        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">\n          <div>\n            <div style="display: flex; align-items: center; gap: 9px; font-family: \'Space Mono\', monospace; font-size: 10.5px; letter-spacing: 0.16em; text-transform: uppercase; color: oklch(var(--t3) 0.16 175);"><span aria-hidden="true" style="{{ icAbout }}"></span>Help &amp; get involved</div>\n            <h1 style="margin: 4px 0 6px; font-size: 27px; font-weight: 900; letter-spacing: -0.035em; text-wrap: balance;">About Amplify</h1>\n            <p style="margin: 0; font-size: 17px; line-height: 1.5; font-weight: 700; max-width: 66ch;">{{ abMission }}</p>\n          </div>\n          <section style="border: 1px solid oklch(var(--t1) 0.16 175 / 0.4); border-radius: 24px; background: linear-gradient(150deg, oklch(var(--t1) 0.16 175 / 0.14), rgb(var(--film-rgb) / 0.03)); padding: 22px 24px; display: flex; flex-direction: column; gap: 10px;">\n            <h2 style="margin: 0; font-size: 18px; font-weight: 900;">Who is behind it</h2>\n            <p style="margin: 0; font-size: 14px; line-height: 1.6; max-width: 76ch;">{{ abWho }}</p>\n            <p style="margin: 0; font-size: 14px; line-height: 1.6; max-width: 76ch;">{{ abImpartial }}</p>\n            <a href="{{ abProfile }}" target="_blank" rel="noopener" style="display: inline-flex; align-items: center; gap: 7px; font-size: 14px; font-weight: 800;"><span aria-hidden="true" style="{{ icGit }}"></span>github.com/cyberdudeuk<span aria-hidden="true" style="{{ icExt }}"></span><span class="amp-sr"> (opens GitHub in a new tab)</span></a>\n          </section>\n          <section style="border: 1px solid rgb(var(--film-rgb) / 0.12); border-radius: 22px; background: rgb(var(--film-rgb) / 0.04); padding: 20px 22px;"><h2 style="margin: 0 0 10px; font-size: 17px; font-weight: 800;">Why it exists</h2><ul style="margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 7px;"><sc-for list="{{ abRationale }}" as="x" hint-placeholder-count="4"><li style="font-size: 13.5px; line-height: 1.55;">{{ x.t }}</li></sc-for></ul></section>\n          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr)); gap: 14px;">\n            <section style="border: 1px solid rgb(var(--film-rgb) / 0.12); border-radius: 22px; background: rgb(var(--film-rgb) / 0.04); padding: 20px 22px;"><h2 style="margin: 0 0 10px; font-size: 17px; font-weight: 800;">Aims, on the four cornerstones</h2><ul style="margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 7px;"><sc-for list="{{ abAims }}" as="x" hint-placeholder-count="4"><li style="font-size: 13.5px; line-height: 1.55;">{{ x.t }}</li></sc-for></ul></section>\n            <section style="border: 1px solid rgb(var(--film-rgb) / 0.12); border-radius: 22px; background: rgb(var(--film-rgb) / 0.04); padding: 20px 22px;"><h2 style="margin: 0 0 10px; font-size: 17px; font-weight: 800;">Goals</h2><ul style="margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 7px;"><sc-for list="{{ abGoals }}" as="x" hint-placeholder-count="4"><li style="font-size: 13.5px; line-height: 1.55;">{{ x.t }}</li></sc-for></ul></section>\n            <section style="border: 1px solid rgb(var(--film-rgb) / 0.12); border-radius: 22px; background: rgb(var(--film-rgb) / 0.04); padding: 20px 22px;"><h2 style="margin: 0 0 10px; font-size: 17px; font-weight: 800;">Objectives: what it delivers</h2><ul style="margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 7px;"><sc-for list="{{ abObjectives }}" as="x" hint-placeholder-count="4"><li style="font-size: 13.5px; line-height: 1.55;">{{ x.t }}</li></sc-for></ul></section>\n          </div>\n          <section style="border: 1px solid rgb(var(--film-rgb) / 0.12); border-radius: 22px; background: rgb(var(--film-rgb) / 0.04); padding: 20px 22px;">\n            <h2 style="margin: 0 0 10px; font-size: 17px; font-weight: 800;">Outcomes it is working towards, and how each will be judged</h2>\n            <div role="table" aria-label="Outcomes and how each will be measured" style="display: flex; flex-direction: column; font-size: 13.5px;">\n              <div role="row" class="amp-row4" style="display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 10px; padding: 6px 4px;"><span role="columnheader" style="font-family: \'Space Mono\', monospace; font-size: 10.5px; letter-spacing: 0.14em; text-transform: uppercase;">Outcome</span><span role="columnheader" style="font-family: \'Space Mono\', monospace; font-size: 10.5px; letter-spacing: 0.14em; text-transform: uppercase;">How it will be judged</span></div>\n              <sc-for list="{{ abOutcomes }}" as="o" hint-placeholder-count="4"><div role="row" class="amp-row4" style="display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 10px; padding: 8px 4px; border-top: 1px solid rgb(var(--film-rgb) / 0.1);"><span role="cell" style="font-weight: 700;">{{ o.outcome }}</span><span role="cell">{{ o.measure }}</span></div></sc-for>\n            </div>\n            <p style="margin: 12px 0 0; font-size: 12.5px; line-height: 1.55; color: rgb(var(--ink-rgb) / 0.8);">{{ abNote }}</p>\n          </section>\n        </div>\n        </sc-if>\n'

GROUP2 = '''
    ["Help & get involved", [
      ["about", "About Amplify", "dot", 175, 5, "NEW", "about who mission purpose aims goals objectives outcomes rationale why owner GitHub profile"],
      ["launch", "UK Parliament Week launch", "sq", 70, 4, "NEW", "launch UK Parliament Week UKPW 23 November 2026 countdown activities schools youth groups"],
      ["help", "Help & tutorials", "ring", 300, 5, "NEW", "help user manual adoption guide tutorials guided tours how to get started parents schools youth groups"],
      ["feedback", "Have your say", "dot", 175, 3, "NEW", "feedback idea suggestion feature request bug issue problem report correction"]
    ]]'''


def transforms():
    return [
        ("ext2-sources-group-changes", "the release log sits with the other sources and updates",
         '      ["trust", "Safeguards & audiences",', '      ["changes", "Release log", "bar", 145, 3, "NEW", "release log changelog changes new updated version history what changed"],\n      ["trust", "Safeguards & audiences",', 1),
        ("ext2-group", "help, feedback and the launch get their own drawer group",
         '      ["health", "Portal health", "ring", 145, 4, "NEW", "health self check freshness staleness provenance checks defects open register status"]\n    ]]',
         '      ["health", "Portal health", "ring", 145, 4, "NEW", "health self check freshness staleness provenance checks defects open register status"]\n    ]],' + GROUP2, 1),
        ("ext2-hash", "the new screens can be linked to", "|sources|latest|trust|health)$/.test(id)", "|sources|latest|trust|health|changes|help|feedback|launch|about|home)$/.test(id)", 1),
        ("ext2-home-group", "Home leads the drawer",
         '    ["Foundations", [\n', '    ["Foundations", [\n      ["home", "Home", "dot", 175, 4, "NEW", "home start welcome what is amplify who is it for how to use"],\n', 1),
        ("ext2-home-default", "after the splash, the portal opens on Home",
         '[(this.props || {}).entryScreen] || "hub",', '[(this.props || {}).entryScreen] || "home",', 1),
        ("ext2-tours", "three new guided tours, alongside the design's own", "  TOURS = {\n", "  TOURS = {\n" + TOURS_ADD, 1),
        ("ext2-tour-step", "a tour step remembers where it is, so the step bar can follow you",
         "        go: () => this.setState({ screen: id })\n      })),\n      tourKit", "        go: () => this.setState({ screen: id, tourAt: i })\n      })),\n      tourKit", 1),
        ("ext2-flags-a", "drawer flags come from the release log, so drawer and page agree",
         "items: items.map(([id, lbl, shape, hue, sub, flag]) => ({", "items: items.map(([id, lbl, shape, hue, sub, flag0]) => { const flag = this.ampFlag(id, flag0); return {", 1),
        ("ext2-flags-b", "close the item function opened by ext2-flags-a",
         "            go: () => this.setState({ screen: id })\n          }))\n        };", "            go: () => this.setState({ screen: id })\n          }; })\n        };", 1),
        ("ext2-logic", "logic for flags, the release log, help, feedback, the launch and the tour bar",
         "  async loadPetition() {", LOGIC2 + "\n  async loadPetition() {", 1),
        ("ext2-ribbon", "the tour bar, the new/updated note and the launch strip, at the top of every screen",
         '      <main id="amp-main" tabindex="-1" style="flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; gap: 14px; outline: none;">',
         '      <main id="amp-main" tabindex="-1" style="flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; gap: 14px; outline: none;">' + RIBBON, 1),
        ("ext2-screens", "the five new screens", '        <div data-slot="portal-end" style="display: none;"></div>', HOME + ABOUT + SCREENS2 + '\n        <div data-slot="portal-end" style="display: none;"></div>', 1),
    ]
