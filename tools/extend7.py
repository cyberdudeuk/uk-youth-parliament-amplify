"""Seventh set of portal extensions: the splash (its Signal and Manifesto treatments), reviewed for accuracy, access
and phones and tablets.

  accuracy   The masthead no longer links "UK Youth" (a different charity) inside "UK Youth Parliament" (D13); the
             Signal headline no longer states votes at 16 as law while the Bill is in the Lords (D14); the Manifesto
             treatment's typed line is credited as Amplify's own words, not a quote from the UKYP manifesto (D15)
  access     The splash is a labelled dialog: Escape enters the portal, Tab stays inside it, and the automatic close
             is cancelled the moment someone points, taps, types or asks for reduced motion (WCAG 2.2.1, 2.4.11; D16);
             the Signal and Manifesto switches say which is on, and both explain themselves with tooltips
  phones     The 650-constituency dot field reflows to 26 columns on a phone and 65 on a tablet, so each seat stays
             visible instead of shrinking to a single pixel
  launch     The Signal treatment names the UK Parliament Week launch dates
"""
from extend import SMALL

LOGIC7 = r'''
  ampSplashOn() {
    if (this._spl || typeof document === "undefined") return;
    const box = () => document.querySelector("[data-amp-splash]");
    const hold = () => { if (this.auto) { clearTimeout(this.auto); this.auto = null; } };
    const enter = () => { hold(); this.setState({ splash: false }, () => { const m = document.getElementById("amp-main"); if (m) m.focus(); }); };
    let reduce = false; try { reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches; } catch (e) { /* no media queries */ }
    if (reduce) setTimeout(hold, 0);  // nothing moves on by itself for people who ask for less motion
    this._spl = {
      key: (e) => {
        const b = box(); if (!this.state.splash || !b) return;
        hold();
        if (e.key === "Escape") { e.preventDefault(); enter(); return; }
        if (e.key === "Tab") {
          const f = Array.from(b.querySelectorAll("a[href], button, [tabindex]:not([tabindex='-1'])")).filter((x) => !x.disabled && x.offsetParent !== null);
          if (!f.length) return;
          const first = f[0], last = f[f.length - 1], a = document.activeElement;
          if (!b.contains(a)) { e.preventDefault(); first.focus(); }
          else if (e.shiftKey && a === first) { e.preventDefault(); last.focus(); }
          else if (!e.shiftKey && a === last) { e.preventDefault(); first.focus(); }
        }
      },
      touch: (e) => { const b = box(); if (b && b.contains(e.target)) hold(); }
    };
    document.addEventListener("keydown", this._spl.key, true);
    document.addEventListener("pointerdown", this._spl.touch, true);
    document.addEventListener("mouseover", this._spl.touch, true);
  }
  ampSplashOff() {
    if (!this._spl) return;
    document.removeEventListener("keydown", this._spl.key, true);
    document.removeEventListener("pointerdown", this._spl.touch, true);
    document.removeEventListener("mouseover", this._spl.touch, true);
    this._spl = null;
  }
  ampVals7(s) {
    return { splashAPressed: s.splashVar === "a" ? "true" : "false", splashBPressed: s.splashVar === "b" ? "true" : "false" };
  }
'''

CSS7 = '''
  @media (max-width: 1024px) { .amp-dots { grid-template-columns: repeat(65, 1fr) !important; } }
  @media (max-width: 420px) { main li[style*="grid-template-columns"] { grid-template-columns: minmax(0, 1fr) !important; gap: 2px !important; } main [style*="white-space: nowrap"] { white-space: normal !important; } }
  @media (max-width: 640px) { .amp-dots { grid-template-columns: repeat(26, 1fr) !important; gap: 3px !important; } }
'''

LAUNCH = '<p style="margin: 12px 0 0; font-family: \'Space Mono\', monospace; font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase; color: oklch(var(--t1) 0.16 70);">Launching in UK Parliament Week &middot; 23 to 29 November 2026 &middot; no sign-in needed</p>'
CREDIT = f'<p style="margin: 14px 0 0; max-width: 62ch; {SMALL}">The line above is Amplify\'s own, on the petition\'s ask: it is not a quotation. The UK Youth Parliament\'s manifesto, <i>Shaping Our Future, Today Not Tomorrow</i> (2024 to 2026), is linked from Issue domains.</p>\n    '


def transforms():
    return [
        ("ext7-css", "dot field reflow for phones and tablets", "  .amp-sr {", CSS7 + "\n  .amp-sr {", 1),
        ("ext7-drawer-scroll", "the drawer scrolls on its own, inside the screen's height, without moving the page (D17)",
         '<nav aria-label="Portal sections" style="flex: 0 0 236px; position: sticky; top: 74px;',
         '<nav aria-label="Portal sections" style="flex: 0 0 236px; position: sticky; top: 74px; align-self: flex-start; max-height: calc(100vh - 90px); overflow-y: auto; overscroll-behavior: contain;', 1),
        ("ext7-dialog", "the splash is a labelled dialog the keyboard can leave with Escape (D16)",
         '<div style="position: fixed; inset: 0; z-index: 90; background: radial-gradi',
         '<div data-amp-splash role="dialog" aria-modal="true" aria-label="Welcome to Amplify" style="position: fixed; inset: 0; z-index: 90; background: radial-gradi', 1),
        ("ext7-no-ukyouth", "no link to UK Youth (a different charity) inside the UK Youth Parliament name (D13)",
         '<a href="https://www.ukyouth.org/" target="_blank" rel="noopener">UK Youth</a> Parliament', 'Independent &middot; not a UKYP service', 1),
        ("ext7-headline", "the headline states where the Bill really is (D14)", "We get the vote at&nbsp;16.", "Votes at 16 is in the&nbsp;Lords. Are we&nbsp;ready?", 1),
        ("ext7-why", "say when the Bill cleared the Commons, before the petition story", "Youth Parliament UK asked the Government to fund",
         "The Representation of the People Bill cleared the Commons on 2 September 2026. Before that, Youth Parliament UK asked the Government to fund", 1),
        ("ext7-launch", "the launch dates on the Signal treatment", "Amplify exists so the next one does not.</p>", "Amplify exists so the next one does not.</p>\n      " + LAUNCH, 1),
        ("ext7-credit", "the Manifesto treatment credits its line as Amplify's own (D15)",
         '<div style="display: flex; flex-wrap: wrap; gap: 24px; margin-top: 26px; padding-top: 16px; border-top: 1px solid rgb(var(--film-rgb) / 0.10);">',
         CREDIT + '<div style="display: flex; flex-wrap: wrap; gap: 24px; margin-top: 26px; padding-top: 16px; border-top: 1px solid rgb(var(--film-rgb) / 0.10);">', 1),
        ("ext7-sig-btn", "the Signal switch says when it is on, and explains itself", '<button onClick="{{ setSplashA }}"', '<button onClick="{{ setSplashA }}" aria-pressed="{{ splashAPressed }}" data-tip="ui:signal"', 1),
        ("ext7-man-btn", "the Manifesto switch says when it is on, and explains itself", '<button onClick="{{ setSplashB }}"', '<button onClick="{{ setSplashB }}" aria-pressed="{{ splashBPressed }}" data-tip="ui:manifesto"', 1),
        ("ext7-dots", "the dot field can reflow", '<div style="display: grid; grid-template-columns: repeat(130, 1fr); gap: 2px;">', '<div class="amp-dots" role="img" aria-label="650 constituencies: each dot is a seat, lit where someone signed" style="display: grid; grid-template-columns: repeat(130, 1fr); gap: 2px;">', 1),
        ("ext7-kit-parent", "the parents' post no longer states votes at 16 as law (D14)", '"Our kids get the vote at 16. Right now,', '"Votes at 16 is going through Parliament. Right now,', 1),
        ("ext7-kit-parent-subj", "the parents' subject line no longer states votes at 16 as law (D14)", '"Your child gets the vote at 16. Are they', '"Your child could soon vote at 16. Are they', 1),
        ("ext7-kit-peer", "the peer post no longer states votes at 16 as law (D14)", '"We get the vote at 16 and nobody taught us how to use it.', '"Votes at 16 is going through Parliament and nobody has taught us how to use a vote.', 1),
        ("ext7-kit-peer-mail", "the peer email no longer states votes at 16 as law (D14)", '"You are getting the vote at 16, and most of us', '"Votes at 16 is going through Parliament, and most of us', 1),
        ("ext7-kit-peer-chat", "the peer chat no longer states votes at 16 as law (D14)", 'We get the vote at 16 and nobody taught us how it works.', 'Votes at 16 is coming through Parliament and nobody has taught us how voting works.', 1),
        ("ext7-logic", "splash keyboard and timing logic", "  async loadPetition() {", LOGIC7 + "\n  async loadPetition() {", 1),
        ("ext7-vals", "its values join renderVals", "...this.ampVals6(s),", "...this.ampVals6(s), ...this.ampVals7(s),", 1),
        ("ext7-mount", "start the splash handling when the page mounts", "    this.ampTipsOn();\n", "    this.ampTipsOn();\n    this.ampSplashOn();\n", 1),
        ("ext7-unmount", "and stop it on unmount", "    this.ampTipsOff();\n", "    this.ampTipsOff();\n    this.ampSplashOff();\n", 1),
    ]
