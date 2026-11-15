"""Eighth set of portal extensions: Go-live readiness.

  golive  The gates that must be passed before the public launch, by area and MoSCoW, each with its status, the checks
          that prove it and who must act; a live count of verified, search-sourced and lead sources; the latest check
          results from build.json; and the self-routines that keep the portal right once it is live, with their cadence
          and whether they are running. Text comes from data/readiness.json; docs/go-live.md is generated from it, and
          check_site S15 keeps every gate's evidence pointing at a real check and every open gate naming who must act.
"""
from extend import PANEL, LABEL, SMALL
from extend4 import H2, CARD, NOTE

LOGIC8 = r'''
  ampVals8(s) {
    const A = s.amp || {}, rd = A.rd || { gates: [], routines: [] }, src = (A.src || { sources: [] }).sources;
    const SH = { Pass: 145, Partial: 70, Open: 25, Fail: 25 }, MH = { Must: 25, Should: 70, Could: 175 };
    const W = {}; ((A.bld || {}).checks || []).forEach((c) => { W[c.id] = c.what; });
    const mustOpen = rd.gates.filter((g) => g.moscow === "Must" && g.status !== "Pass");
    const pill = (h) => "display:inline-block;border-radius:999px;padding:2px 9px;font-family:'Space Mono',monospace;font-size:11px;font-weight:700;background:oklch(var(--t1) 0.16 " + h + " / 0.28);color:oklch(var(--t4) 0.15 " + h + ");";
    const areas = []; rd.gates.forEach((g) => { if (areas.indexOf(g.area) < 0) areas.push(g.area); });
    const n = (p) => String(src.filter((x) => x.provenance === p).length);
    return {
      sGolive: s.screen === "golive", rdIntro: rd.intro || "",
      rdReady: mustOpen.length === 0, rdNotReady: mustOpen.length > 0,
      rdVerdict: mustOpen.length === 0 ? "Ready to go live: every Must gate is passed." : "Not ready to go public yet: " + mustOpen.length + " Must " + (mustOpen.length === 1 ? "gate is" : "gates are") + " still open, and each one is for the owner to decide.",
      rdCounts: [["Pass", 145], ["Partial", 70], ["Open", 25]].map(([k, h]) => ({ k, n: String(rd.gates.filter((g) => g.status === k).length), style: pill(h) })),
      rdV: n("V"), rdS: n("S"), rdK: n("K"), rdBuild: (A.bld || {}).build_id || "", rdChecks: String(Object.keys(W).length),
      rdAreas: areas.map((a) => ({ area: a, gates: rd.gates.filter((g) => g.area === a).map((g) => ({ id: g.id, item: g.item, status: g.status, moscow: g.moscow, sStyle: pill(SH[g.status] || 25), mStyle: pill(MH[g.moscow] || 175),
        who: g.who, hasWho: !!g.who, note: g.note, hasNote: !!g.note, ev: g.evidence.map((e) => ({ e, what: W[e] || e })), hasEv: g.evidence.length > 0 })) })),
      rdRoutines: rd.routines.map((r) => ({ routine: r.routine, kind: r.kind, what: r.what, cadence: r.cadence, where: r.where, moscow: r.moscow, status: r.status,
        mStyle: pill(MH[r.moscow] || 175), sStyle: pill(r.status === "Running" ? 145 : (r.status.indexOf("Set up") === 0 ? 70 : 25)) })),
      icGolive: this.ampIcon("rocket", "oklch(var(--t3) 0.16 145)", 16)
    };
  }
'''

SCREEN8 = f'''
        <sc-if value="{{{{ sGolive }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          <div>
            <div style="display: flex; align-items: center; gap: 9px; font-family: 'Space Mono', monospace; font-size: 10.5px; letter-spacing: 0.16em; text-transform: uppercase; color: oklch(var(--t3) 0.16 145);"><span aria-hidden="true" style="{{{{ icGolive }}}}"></span>Sources &amp; updates</div>
            <h1 style="margin: 4px 0 6px; font-size: 27px; font-weight: 900; letter-spacing: -0.035em; text-wrap: balance;">Go-live readiness</h1>
            <p style="margin: 0; font-size: 15px; line-height: 1.55; color: rgb(var(--ink-rgb) / 0.82); max-width: 68ch;">{{{{ rdIntro }}}}</p>
          </div>
          <div role="status" style="{NOTE} border: 1px solid oklch(var(--t2) 0.16 70 / 0.7); background: oklch(var(--t1) 0.16 70 / 0.12); font-size: 15px; font-weight: 800;">{{{{ rdVerdict }}}}</div>
          <div style="display: flex; flex-wrap: wrap; gap: 10px 18px; align-items: center;"><sc-for list="{{{{ rdCounts }}}}" as="c" hint-placeholder-count="3"><span style="font-size: 13.5px;"><span style="{{{{ c.style }}}}">{{{{ c.k }}}}</span> {{{{ c.n }}}}</span></sc-for><span style="{SMALL}">Sources: {{{{ rdV }}}} verified, {{{{ rdS }}}} search-sourced, {{{{ rdK }}}} leads. Build {{{{ rdBuild }}}}, {{{{ rdChecks }}}} checks.</span></div>
          <sc-for list="{{{{ rdAreas }}}}" as="a" hint-placeholder-count="4">
            <section style="{PANEL}"><h2 style="{H2}">{{{{ a.area }}}}</h2>
              <div style="display: flex; flex-direction: column; gap: 8px;"><sc-for list="{{{{ a.gates }}}}" as="g" hint-placeholder-count="3"><div style="{CARD}"><div style="display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 10px;"><span style="{LABEL}">{{{{ g.id }}}}</span><span style="{{{{ g.sStyle }}}}">{{{{ g.status }}}}</span><span style="{{{{ g.mStyle }}}}">{{{{ g.moscow }}}}</span><span style="flex: 1 1 260px; min-width: 0; font-size: 14px; font-weight: 700;">{{{{ g.item }}}}</span></div>
                <sc-if value="{{{{ g.hasEv }}}}" hint-placeholder-val="{{{{ false }}}}"><div style="display: flex; flex-wrap: wrap; gap: 4px 10px; font-size: 12.5px;"><span style="font-weight: 800;">Proved by</span><sc-for list="{{{{ g.ev }}}}" as="e" hint-placeholder-count="2"><span title="{{{{ e.what }}}}" style="font-family: 'Space Mono', monospace; font-weight: 700;">{{{{ e.e }}}}</span></sc-for></div></sc-if>
                <sc-if value="{{{{ g.hasWho }}}}" hint-placeholder-val="{{{{ false }}}}"><div style="font-size: 12.5px;"><span style="font-weight: 800;">Who must act:</span> {{{{ g.who }}}}</div></sc-if>
                <sc-if value="{{{{ g.hasNote }}}}" hint-placeholder-val="{{{{ false }}}}"><div style="{SMALL}">{{{{ g.note }}}}</div></sc-if></div></sc-for></div>
            </section>
          </sc-for>
          <section style="{PANEL}"><h2 style="{H2}">Self-routines that keep it right</h2><p style="margin: 0 0 10px; {SMALL}">What runs on its own, how often, and where, prioritised as Must, Should or Could have.</p>
            <div style="display: flex; flex-direction: column; gap: 8px;"><sc-for list="{{{{ rdRoutines }}}}" as="r" hint-placeholder-count="6"><div style="{CARD}"><div style="display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 10px;"><span style="{{{{ r.mStyle }}}}">{{{{ r.moscow }}}}</span><span style="{{{{ r.sStyle }}}}">{{{{ r.status }}}}</span><span style="font-size: 14px; font-weight: 800;">{{{{ r.routine }}}}</span><span style="{LABEL}">{{{{ r.kind }}}} &middot; {{{{ r.cadence }}}}</span></div><div style="{SMALL}">{{{{ r.what }}}} <span style="font-family: 'Space Mono', monospace; font-size: 12px;">{{{{ r.where }}}}</span></div></div></sc-for></div></section>
        </div>
        </sc-if>
'''

NAV8 = '\n      ["golive", "Go-live readiness", "tri", 145, 4, "NEW", "go live readiness launch checklist gates tests routines release blockers moscow"]'
HEALTH = '      ["health", "Portal health", "ring", 145, 4, "NEW", "health self check freshness staleness provenance checks defects open register status"]'


def transforms():
    return [
        ("ext8-load", "the readiness data loads with the rest", '"./data/service-design.json"].map(get));', '"./data/service-design.json", "./data/readiness.json"].map(get));', 1),
        ("ext8-load-vars", "name it", "cm, tt, iv, rs, sd] =", "cm, tt, iv, rs, sd, rd] =", 1),
        ("ext8-load-state", "keep it in state", "cm, tt, iv, rs, sd, loaded", "cm, tt, iv, rs, sd, rd, loaded", 1),
        ("ext8-nav", "Go-live readiness sits after Portal health", HEALTH + "\n    ]],", HEALTH + "," + NAV8 + "\n    ]],", 1),
        ("ext8-hash", "the screen can be linked to", "|research|service)$/.test(id)", "|research|service|golive)$/.test(id)", 1),
        ("ext8-logic", "readiness logic", "  async loadPetition() {", LOGIC8 + "\n  async loadPetition() {", 1),
        ("ext8-vals", "its values join renderVals", "...this.ampVals7(s),", "...this.ampVals7(s), ...this.ampVals8(s),", 1),
        ("ext8-screen", "the Go-live readiness screen", '        <div data-slot="portal-end" style="display: none;"></div>', SCREEN8 + '\n        <div data-slot="portal-end" style="display: none;"></div>', 1),
    ]
