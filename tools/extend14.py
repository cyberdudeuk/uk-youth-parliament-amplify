"""Fourteenth set of portal extensions: one clear front door (17 November 2026, REQ-35, defect D44).

  Before this release a first visit opened on a splash about petition 754954, which closed in August 2026 with 1,192
  signatures, and on a phone the Home page title sat 1,227px down an 844px screen, under the "This screen" strip
  (up to 200px), Share, two alerts, the news ticker and the launch carousel (D44).

  splash     no longer opens by itself. It tells the petition's story, so it is offered where that story lives: the
             Splash button in the masthead and a "Watch the petition story" button on Campaign hub.
  home       leads with its title and a "Who are you?" chooser: eight doors, each setting the audience the portal
             explains itself for and giving three places to start and a guided tour. The launch carousel follows.
  strip      "This screen" becomes a one-line "About this screen" disclosure, closed by default, that keeps the
             audience picker inside it.
  check      check_browser W10 measures where Home's title lands on a phone and a desktop and fails if it slips back
             below the fold or if the splash opens by itself again.
"""
import os

from extend import LABEL, SMALL
from extend11 import BTN

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CAROUSEL = '          <section aria-roledescription="carousel" aria-label="Spotlights" onMouseEnter="{{ carHoldOn }}" onMouseLeave="{{ carHoldOff }}" onFocus="{{ carHoldOn }}" onBlur="{{ carHoldOff }}">\n            <sc-if value="{{ carHas }}" hint-placeholder-val="{{ true }}">\n            <div aria-roledescription="slide" aria-label="{{ carPos }}" aria-live="polite" class="amp-slide" style="{{ carBg }}">\n              <div style="display: flex; flex-direction: column; gap: 12px;">\n                <span style="{{ carPill }}">{{ carKind }}</span>\n                <h2 style="margin: 0; font-size: clamp(26px, 3.6vw, 40px); font-weight: 900; line-height: 1.06; letter-spacing: -0.035em; text-wrap: balance;">{{ carTitle }}</h2>\n                <p style="margin: 0; font-size: 15.5px; line-height: 1.6; max-width: 60ch;">{{ carBody }}</p>\n                <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 10px;">\n                  <button type="button" onClick="{{ carGo }}" style="min-height: 44px; border-radius: 999px; padding: 10px 20px; border: 0; background: oklch(var(--t2) 0.16 145); color: var(--on-accent); font-size: 14px; font-weight: 800; cursor: pointer;">{{ carCta }}</button>\n                </div>\n              </div>\n              <img src="{{ carArt }}" alt="" style="width: 100%; height: auto; max-height: 200px; object-fit: cover; border-radius: 20px;" />\n            </div>\n            </sc-if>\n            <div style="display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 10px; margin-top: 10px;">\n              <div role="group" aria-label="Choose a slide" style="display: flex; align-items: center; gap: 7px;"><sc-for list="{{ carDots }}" as="d" hint-placeholder-count="5"><button type="button" onClick="{{ d.go }}" aria-label="{{ d.label }}" aria-current="{{ d.current }}" style="{{ d.style }}"></button></sc-for></div>\n              <div style="display: flex; gap: 8px;">\n                <button type="button" onClick="{{ carPrev }}" aria-label="Previous slide" style="min-width: 40px; min-height: 40px; border-radius: 999px; border: 1px solid rgb(var(--film-rgb) / 0.2); background: transparent; color: rgb(var(--ink-rgb)); font-size: 16px; cursor: pointer;">&lsaquo;</button>\n                <button type="button" onClick="{{ carToggle }}" aria-pressed="{{ carPressed }}" style="min-height: 40px; border-radius: 999px; padding: 0 14px; border: 1px solid rgb(var(--film-rgb) / 0.2); background: transparent; color: rgb(var(--ink-rgb)); font-size: 13px; font-weight: 700; cursor: pointer;">{{ carToggleLabel }}</button>\n                <button type="button" onClick="{{ carNext }}" aria-label="Next slide" style="min-width: 40px; min-height: 40px; border-radius: 999px; border: 1px solid rgb(var(--film-rgb) / 0.2); background: transparent; color: rgb(var(--ink-rgb)); font-size: 16px; cursor: pointer;">&rsaquo;</button>\n              </div>\n            </div>\n          </section>\n'
TOURS_OLD = '          <section aria-labelledby="amp-tourin" style="border: 1px solid oklch(var(--t1) 0.16 300 / 0.4); border-radius: 22px; background: oklch(var(--t1) 0.16 300 / 0.1); padding: 18px 20px;">\n            <h2 id="amp-tourin" style="margin: 0 0 10px; font-size: 17px; font-weight: 800;">Start with a guided tour for you</h2>\n            <div style="display: flex; flex-wrap: wrap; gap: 10px;">\n              <sc-for list="{{ hpTours }}" as="t" hint-placeholder-count="5"><button type="button" onClick="{{ t.go }}" style="display: inline-flex; align-items: center; gap: 8px; min-height: 42px; border-radius: 999px; padding: 8px 16px; border: 1px solid oklch(var(--t2) 0.16 300 / 0.6); background: rgb(var(--film-rgb) / 0.05); color: rgb(var(--ink-rgb)); font-size: 13.5px; font-weight: 700; cursor: pointer;"><span aria-hidden="true" style="{{ icTour }}"></span>{{ t.label }}</button></sc-for>\n            </div>\n          </section>\n'
STRIP_OLD = '        <sc-if value="{{ exShow }}" hint-placeholder-val="{{ false }}">\n        <div role="note" aria-label="What this screen is for" class="amp-explainer" style="display: flex; flex-wrap: wrap; align-items: center; gap: 10px 14px; border-radius: 16px; padding: 10px 14px; border: 1px solid oklch(var(--t1) 0.16 215 / 0.45); background: oklch(var(--t1) 0.16 215 / 0.1); font-size: 13.5px; line-height: 1.5;">\n          <span aria-hidden="true" style="{{ icHelp }}"></span>\n          <span style="flex: 1 1 300px; min-width: 0;"><span style="font-weight: 800;">This screen:</span> {{ exTip }}<sc-if value="{{ exHasFor }}" hint-placeholder-val="{{ false }}"> <span style="color: rgb(var(--ink-rgb) / 0.8);">For {{ exWho }}: {{ exFor }}</span></sc-if></span>\n          <label data-tip="ui:persona" style="display: flex; flex-wrap: wrap; align-items: center; gap: 6px 8px; flex: 0 1 auto; min-width: 0; max-width: 100%; font-size: 12.5px; color: rgb(var(--ink-rgb) / 0.8);">Explain for\n            <select value="{{ persona }}" onChange="{{ setPersona }}" style="min-width: 0; max-width: 100%; min-height: 36px; border: 1px solid rgb(var(--film-rgb) / 0.2); border-radius: 10px; background: rgb(var(--film-rgb) / 0.05); color: rgb(var(--ink-rgb)); padding: 6px 10px; font-size: 13px;"><option value="everyone">Everyone</option><option value="young11">Young person, 11 to 15</option><option value="young16">Young person, 16 to 25</option><option value="parent">Parent, guardian or carer</option><option value="worker">Youth worker or group leader</option><option value="teacher">Teacher, tutor or school staff</option><option value="club">Coding or STEM club leader or mentor</option><option value="access">d/Deaf or disabled young person</option><option value="ally">Councillor, policy maker, researcher or journalist</option></select>\n          </label>\n        </div>\n        </sc-if>\n'

NOTES_OLD = '        <sc-if value="{{ rbShow }}" hint-placeholder-val="{{ false }}">\n        <div role="note" style="{{ rbStyle }}"><span style="{{ rbPill }}">{{ rbKind }}</span><span style="flex: 1 1 240px; min-width: 0;">{{ rbWhat }}</span><button type="button" onClick="{{ goChanges }}" style="border: 0; background: transparent; color: inherit; text-decoration: underline; font-size: 13px; cursor: pointer; padding: 6px;">Release log</button></div>\n        </sc-if>\n        <sc-if value="{{ igShow }}" hint-placeholder-val="{{ false }}">\n        <div role="note" aria-label="About the content on this screen" style="{{ igStyle }}"><span style="{{ igPill }}">{{ igClass }}</span><span style="flex: 1 1 260px; min-width: 0;">{{ igWhy }}</span></div>\n        </sc-if>\n'

STRIP_NEW = '''        <sc-if value="{{ exShow }}" hint-placeholder-val="{{ false }}">
        <details class="amp-explainer" style="border-radius: 14px; padding: 7px 12px; border: 1px solid oklch(var(--t1) 0.16 215 / 0.45); background: oklch(var(--t1) 0.16 215 / 0.08); font-size: 13.5px; line-height: 1.5;">
          <summary style="display: flex; align-items: center; gap: 8px; cursor: pointer; min-height: 30px; font-weight: 800;"><span aria-hidden="true" style="{{ icHelp }}"></span>About this screen<span style="font-weight: 600; color: rgb(var(--ink-rgb) / 0.8);">{{ exSumWho }}</span><sc-if value="{{ igShow }}" hint-placeholder-val="{{ false }}"><span style="{{ igPill }}">{{ igClass }}</span></sc-if><sc-if value="{{ rbShow }}" hint-placeholder-val="{{ false }}"><span style="{{ rbPill }}">{{ rbKind }}</span></sc-if></summary>
          <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px 14px; padding: 6px 0 4px;">
            <span style="flex: 1 1 300px; min-width: 0;">{{ exTip }}<sc-if value="{{ exHasFor }}" hint-placeholder-val="{{ false }}"> <span style="color: rgb(var(--ink-rgb) / 0.8);">For {{ exWho }}: {{ exFor }}</span></sc-if></span>
            <label data-tip="ui:persona" style="display: flex; flex-wrap: wrap; align-items: center; gap: 6px 8px; flex: 0 1 auto; min-width: 0; max-width: 100%; font-size: 12.5px; color: rgb(var(--ink-rgb) / 0.8);">Explain for
              <select value="{{ persona }}" onChange="{{ setPersona }}" style="min-width: 0; max-width: 100%; min-height: 36px; border: 1px solid rgb(var(--film-rgb) / 0.2); border-radius: 10px; background: rgb(var(--film-rgb) / 0.05); color: rgb(var(--ink-rgb)); padding: 6px 10px; font-size: 13px;"><option value="everyone">Everyone</option><option value="young11">Young person, 11 to 15</option><option value="young16">Young person, 16 to 25</option><option value="parent">Parent, guardian or carer</option><option value="worker">Youth worker or group leader</option><option value="teacher">Teacher, tutor or school staff</option><option value="club">Coding or STEM club leader or mentor</option><option value="access">d/Deaf or disabled young person</option><option value="ally">Councillor, policy maker, researcher or journalist</option></select>
            </label>
          </div>
@NOTES@        </details>
        </sc-if>
'''

DOORS = '''          <section aria-labelledby="amp-doors" style="border: 1px solid rgb(var(--film-rgb) / 0.14); border-radius: 22px; background: rgb(var(--film-rgb) / 0.04); padding: 18px 20px; display: flex; flex-direction: column; gap: 12px;">
            <div><h2 id="amp-doors" style="margin: 0; font-size: 19px; font-weight: 900; letter-spacing: -0.02em;">Who are you?</h2><p style="margin: 4px 0 0; font-size: 13.5px; line-height: 1.5;">{{ hmDoorsIntro }}</p></div>
            <ul role="list" style="list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 190px), 1fr)); gap: 8px;">
              <sc-for list="{{ hmDoors }}" as="d" hint-placeholder-count="8"><li style="display: flex;"><button type="button" aria-pressed="{{ d.pressed }}" aria-controls="amp-door-panel" onClick="{{ d.go }}" class="amp-drill" style="{{ d.style }}"><span aria-hidden="true" style="{{ d.icon }}"></span><span>{{ d.label }}</span></button></li></sc-for>
            </ul>
            <div id="amp-door-panel" aria-live="polite">
              <sc-if value="{{ hmDoorOn }}" hint-placeholder-val="{{ false }}"><div style="border-radius: 16px; padding: 14px 16px; border: 1px solid oklch(var(--t1) 0.16 175 / 0.4); background: oklch(var(--t1) 0.16 175 / 0.08); display: flex; flex-direction: column; gap: 10px;">
                <p style="margin: 0; font-size: 14px; line-height: 1.55;">{{ hmDoorLens }}</p>
                <div style="@LABEL@">Start here</div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 200px), 1fr)); gap: 8px;"><sc-for list="{{ hmDoorRoutes }}" as="r" hint-placeholder-count="3"><button type="button" onClick="{{ r.go }}" class="amp-drill amp-card" style="display: flex; flex-direction: column; gap: 4px; text-align: left; cursor: pointer; color: rgb(var(--ink-rgb)); border-radius: 14px; padding: 12px 14px; border: 1px solid rgb(var(--film-rgb) / 0.16); background: rgb(var(--film-rgb) / 0.05);"><span style="display: flex; align-items: center; gap: 8px; font-size: 14.5px; font-weight: 800;"><span aria-hidden="true" style="{{ r.icon }}"></span>{{ r.label }}</span><span style="font-size: 12.5px; line-height: 1.45;">{{ r.tip }}</span></button></sc-for></div>
                <div style="display: flex; flex-wrap: wrap; gap: 8px; align-items: center;"><button type="button" onClick="{{ hmDoorTour }}" style="@BTN@">Take the tour: {{ hmDoorTourLabel }}</button><sc-if value="{{ hmDoorEasy }}" hint-placeholder-val="{{ false }}"><button type="button" onClick="{{ tEasy }}" aria-pressed="{{ erPressed }}" style="@BTN@">Easy Read summaries: {{ erLabel }}</button></sc-if><span style="@SMALL@">Explaining the portal for {{ exWho }}. Change it under About this screen.</span></div>
              </div></sc-if>
            </div>
          </section>
'''.replace("@LABEL@", LABEL).replace("@BTN@", BTN).replace("@SMALL@", SMALL)

LOGIC14 = r'''
  ampVals14(s) {
    const A = s.amp || {}, hm = A.hm || {}, tt = A.tt || {}, arr = (x) => (Array.isArray(x) ? x : []);
    const L = {}; this.GROUPS.forEach(([g, items]) => items.forEach(([id, lbl]) => { L[id] = lbl; }));
    const p = s.persona || "everyone", doors = arr(hm.doors), cur = doors.find((d) => d.persona === p);
    const pe = arr(tt.personas).find((x) => x.id === p) || {};
    const setP = (v) => () => { try { window.localStorage.setItem("amp-persona", v); } catch (e) { /* storage unavailable: keep it in memory */ } this.setState({ persona: v }); };
    const tours = this.TOURS || {}, tk = cur && tours[cur.tour] ? cur.tour : "newhere";
    return {
      exSumWho: p !== "everyone" && pe.label ? " · explained for " + pe.label : "",
      hmDoorsIntro: hm.doors_intro || "",
      hmDoors: doors.map((d) => ({ label: d.label, pressed: d.persona === p ? "true" : "false", go: setP(d.persona === p ? "everyone" : d.persona),
        icon: this.ampIcon(d.icon || "users", "oklch(var(--t3) 0.16 175)", 18),
        style: "display:flex;align-items:center;gap:9px;width:100%;min-height:48px;text-align:left;cursor:pointer;padding:10px 13px;border-radius:14px;font-size:14px;font-weight:800;color:rgb(var(--ink-rgb));border:" + (d.persona === p ? "2px solid oklch(var(--t2) 0.16 175);background:oklch(var(--t1) 0.16 175 / 0.2);" : "1px solid rgb(var(--film-rgb) / 0.18);background:transparent;") })),
      hmDoorOn: !!cur, hmDoorLens: pe.lens || "", hmDoorEasy: !!(cur && cur.easy),
      hmDoorRoutes: arr((cur || {}).routes).filter((id) => L[id]).map((id) => ({ label: L[id], tip: (((tt.screens || {})[id]) || {}).tip || "",
        icon: this.navIcon(id, "dot") + "oklch(var(--t2) 0.16 175);", go: () => this.setState({ screen: id }, () => { try { window.scrollTo(0, 0); } catch (e) { /* no window */ } }) })),
      hmDoorTour: () => this.setState({ tour: tk, screen: tours[tk].steps[0][0], tourAt: 0 }), hmDoorTourLabel: (tours[tk] || {}).label || "",
      hubStory: () => { this.setState({ splash: true, typed: "" }); },
      openAccess: () => this.setState({ a11yOpen: true }, () => { try { window.scrollTo(0, 0); } catch (e) { /* no window */ } })
    };
  }
'''

CSS14 = '''
  @media (max-width: 600px) {
    header > div:first-child > span:nth-child(2) { display: none; }
    header button[data-tip="ui:both"] { display: none; }
    header { gap: 6px 8px !important; padding-top: 8px !important; padding-bottom: 8px !important; }
    section[aria-label="Alerts for you"] > div { padding: 7px 10px !important; gap: 4px 8px !important; font-size: 13px !important; }
    section[aria-label="Alerts for you"] > div > span:first-child { display: none !important; }
    section[aria-label="Alerts for you"] > div > span:nth-child(3) { flex: 1 1 0 !important; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
    section[aria-label="Alerts for you"] > div > span:nth-child(2) { display: none !important; }
    section[aria-label="Alerts for you"] > div > button { min-height: 32px !important; padding: 4px 10px !important; font-size: 12px !important; }
    .amp-share { margin-bottom: -10px; }
  }
'''

HUB_H1 = '<h1 style="margin: 0; font-size: clamp(28px, 3.4vw, 44px); line-height: 1.02; font-weight: 900; letter-spacing: -0.04em; max-width: 22ch;">Only 4.5% of petitions reach a government response.</h1>'


def transforms():
    return [
        ("ext14-splash-off", "D44: the splash no longer opens by itself on arrival", "splash: !this.screenFromHash(),", "splash: false,", 1),
        ("ext14-splash-timer", "D46: no auto-close timer is armed on arrival, now that the splash starts closed; a stale one closed a replayed splash mid-read",
         "    }, 55);\n    this.auto = setTimeout(() => this.setState({ splash: false }), this.splashMs());",
         "    }, 55);\n    if (this.state.splash) this.auto = setTimeout(() => this.setState({ splash: false }), this.splashMs());", 1),
        ("ext14-replay-timer", "D46: replay clears any earlier timer before arming its own, so only one can ever close the splash",
         'replay: () => { this.setState({ splash: true, typed: "" }); this.auto = setTimeout',
         'replay: () => { clearTimeout(this.auto); this.setState({ splash: true, typed: "" }); this.auto = setTimeout', 1),
        ("ext14-notes-out", "D44: the content-integrity and what-changed notes no longer sit above every title", NOTES_OLD, "", 1),
        ("ext14-strip", "D44: This screen becomes a closed one-line disclosure holding the audience picker, the content class and what changed",
         STRIP_OLD, STRIP_NEW.replace("@NOTES@", NOTES_OLD.replace("        <", "          <")), 1),
        ("ext14-carousel-out", "D44: the launch carousel no longer sits above Home's title", CAROUSEL, "", 1),
        ("ext14-doors", "Home leads with Who are you?, then the carousel", TOURS_OLD, DOORS + CAROUSEL, 1),
        ("ext14-hub-story", "the petition story is offered where it lives, on Campaign hub", HUB_H1,
         HUB_H1 + '<button type="button" onClick="{{ hubStory }}" style="margin-top: 12px; ' + BTN.replace('"', "'") + '">Watch the petition story</button>', 1),
        ("ext14-css", "D44: on a phone the masthead and alerts take less of the first screen", "  .amp-sr {", CSS14 + "\n  .amp-sr {", 1),
        ("ext14-incl-access", "the access features card opens the settings it describes", "Built in, switchable, live</div>",
         'Built in, switchable, live</div><button type="button" onClick="{{ openAccess }}" class="amp-drill" style="margin: 0 0 12px; ' + BTN.replace('"', "'") + '">Open Access and language settings</button>', 1),
        ("ext14-incl-easy", "the committed features card lets you switch on the Easy Read that has shipped", "Committed, not yet shipped</div>",
         'Committed, not yet shipped</div><button type="button" onClick="{{ tEasy }}" aria-pressed="{{ erPressed }}" class="amp-drill" style="margin: 0 0 12px; ' + BTN.replace('"', "'") + '">Easy Read summaries: {{ erLabel }}</button>', 1),
        ("ext14-logic", "front door values", "  async loadPetition() {", LOGIC14 + "\n  async loadPetition() {", 1),
        ("ext14-vals", "its values join renderVals", "...this.ampVals13(s),", "...this.ampVals13(s), ...this.ampVals14(s),", 1),
    ]
