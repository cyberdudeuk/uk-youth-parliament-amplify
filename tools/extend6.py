"""Sixth set of portal extensions: the Service design screen (user-centred design made visible).

  service  Personas (proto-personas until research Round 1 tests them), each with needs, pain points and safety;
           their user stories with acceptance criteria and the checks that prove them; journeys through the portal;
           service blueprints from user actions to evidence; and the processes and workflows behind every screen.
           Choosing a persona here follows the persona chosen in the explainer bar, and every screen named is a link.
Text comes from data/service-design.json; docs/service-design/ is generated from the same file, and check_site S13
keeps personas, stories, journeys, screens and check ids consistent with the rest of the portal.
"""
from extend import PANEL, LABEL, SMALL
from extend4 import head, H2, CARD, GOBTN, NOTE

LOGIC6 = r'''
  ampVals6(s) {
    const A = s.amp || {}, sd = A.sd || { personas: [], stories: [], journeys: [], blueprints: [], workflows: [] };
    const label = (id) => { try { return this.screenLabel(id) || id; } catch (e) { return id; } };
    const go = (id) => () => this.setState({ screen: id });
    const ids = sd.personas.map((p) => p.id);
    const cur = ids.indexOf(s.svcP) >= 0 ? s.svcP : (ids.indexOf(s.persona) >= 0 ? s.persona : ids[0]);
    const P = sd.personas.find((p) => p.id === cur) || { needs: [], pains: [], uses: [] };
    const role = (id) => (sd.personas.find((p) => p.id === id) || {}).role || id;
    const W = {}; ((A.bld || {}).checks || []).forEach((c) => { W[c.id] = c.what; });
    const js = sd.journeys.filter((j) => j.persona === cur);
    return {
      sService: s.screen === "service", sdStatus: sd.status || "", sdIntro: sd.intro || "",
      sdChips: sd.personas.map((p) => ({ label: p.role, pressed: p.id === cur ? "true" : "false", style: this.ampChip(p.id === cur, 215), pick: () => this.setState({ svcP: p.id }) })),
      sdRole: P.role || "", sdContext: P.context || "", sdGoal: P.goal || "", sdSafety: P.safety || "",
      sdNeeds: P.needs.map((t) => ({ t })), sdPains: P.pains.map((t) => ({ t })),
      sdUses: P.uses.map((id) => ({ label: label(id), go: go(id) })), sdStart: label(P.starts), sdGoStart: go(P.starts),
      sdStories: sd.stories.filter((x) => x.persona === cur).map((x) => ({ id: x.id, text: "As a " + role(x.persona).toLowerCase() + ", I want to " + x.want + ", so that " + x.so + ".",
        where: label(x.screen), go: go(x.screen), accept: x.accept.map((t) => ({ t })), proved: x.proved.map((c) => ({ id: c, what: W[c] || "" })) })),
      sdAllStories: String(sd.stories.length),
      sdJourneys: js.map((j) => ({ id: j.id, title: j.title, stages: j.stages.map((g, k) => ({ n: String(k + 1), stage: g.stage, doing: g.doing, feeling: g.feeling, opp: g.opportunity, where: label(g.screen), go: go(g.screen) })) })),
      sdHasJourney: js.length > 0, sdNoJourney: js.length === 0,
      sdBlue: sd.blueprints.map((b) => ({ id: b.id, title: b.title, cols: "display:grid;grid-template-columns:minmax(120px,0.8fr) repeat(" + b.phases.length + ",minmax(120px,1fr));gap:6px;min-width:" + (140 + b.phases.length * 130) + "px;",
        phases: b.phases.map((ph) => ({ ph })), layers: b.layers.map((l) => ({ layer: l.layer, cells: l.cells.map((c, k) => ({ c, ph: b.phases[k] || "" })) })) })),
      sdFlows: sd.workflows.map((w) => ({ id: w.id, title: w.title, steps: w.steps.map((t) => ({ t })), decision: w.decision, yes: w.yes, no: w.no })),
      sdDocs: ((A.iv || {}).repo || "") + "/tree/main/docs/service-design",
      icService: this.ampIcon("route", "oklch(var(--t3) 0.16 215)", 16)
    };
  }
'''

UL = "margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 4px; font-size: 13.5px; line-height: 1.5;"
CELL = "border: 1px solid rgb(var(--film-rgb) / 0.12); border-radius: 10px; padding: 8px 10px; font-size: 12.5px; line-height: 1.45;"

SCREEN6 = f'''
        <sc-if value="{{{{ sService }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          {head("icService", 215, "Service design: personas, journeys and blueprints", "{{ sdIntro }}")}
          <div role="note" style="{NOTE} border: 1px dashed oklch(var(--t2) 0.16 70 / 0.8); background: oklch(var(--t1) 0.16 70 / 0.12);"><span style="font-weight: 800;">Status.</span> {{{{ sdStatus }}}}</div>
          <div role="group" aria-label="Choose a persona" style="display: flex; flex-wrap: wrap; gap: 8px;"><sc-for list="{{{{ sdChips }}}}" as="c" hint-placeholder-count="8"><button type="button" onClick="{{{{ c.pick }}}}" aria-pressed="{{{{ c.pressed }}}}" style="{{{{ c.style }}}}">{{{{ c.label }}}}</button></sc-for></div>
          <section aria-label="Persona" class="amp-card" style="{PANEL} display: flex; flex-direction: column; gap: 10px;">
            <h2 style="margin: 0; font-size: 20px; font-weight: 900;">{{{{ sdRole }}}}</h2>
            <p style="margin: 0; {SMALL}">{{{{ sdContext }}}}</p>
            <p style="margin: 0; font-size: 15px; font-weight: 800;">Goal: {{{{ sdGoal }}}}</p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 240px), 1fr)); gap: 12px;">
              <div><div style="{LABEL}">Needs</div><ul style="{UL}"><sc-for list="{{{{ sdNeeds }}}}" as="x" hint-placeholder-count="3"><li>{{{{ x.t }}}}</li></sc-for></ul></div>
              <div><div style="{LABEL}">Pain points</div><ul style="{UL}"><sc-for list="{{{{ sdPains }}}}" as="x" hint-placeholder-count="3"><li>{{{{ x.t }}}}</li></sc-for></ul></div>
              <div><div style="{LABEL}">Kept safe by</div><p style="margin: 4px 0 0; font-size: 13.5px; line-height: 1.5;">{{{{ sdSafety }}}}</p></div>
            </div>
            <div style="display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 12px;"><span style="{LABEL}">Starts at</span><button type="button" onClick="{{{{ sdGoStart }}}}" style="{GOBTN}">{{{{ sdStart }}}}</button><span style="{LABEL}">Uses</span><sc-for list="{{{{ sdUses }}}}" as="u" hint-placeholder-count="5"><button type="button" onClick="{{{{ u.go }}}}" style="{GOBTN}">{{{{ u.label }}}}</button></sc-for></div>
          </section>
          <section style="{PANEL}"><h2 style="{H2}">User stories</h2>
            <div style="display: flex; flex-direction: column; gap: 10px;"><sc-for list="{{{{ sdStories }}}}" as="x" hint-placeholder-count="3"><div style="{CARD}"><div style="{LABEL}">{{{{ x.id }}}}</div><div style="font-size: 14px; font-weight: 800; line-height: 1.45;">{{{{ x.text }}}}</div><div style="font-size: 12.5px; font-weight: 800;">Done when</div><ul style="margin: 0; padding-left: 20px; font-size: 13px; line-height: 1.5;"><sc-for list="{{{{ x.accept }}}}" as="a" hint-placeholder-count="2"><li>{{{{ a.t }}}}</li></sc-for></ul><div style="display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 10px; font-size: 12.5px;"><span style="font-weight: 800;">Proved by</span><sc-for list="{{{{ x.proved }}}}" as="p" hint-placeholder-count="2"><span title="{{{{ p.what }}}}" style="font-family: 'Space Mono', monospace; font-weight: 700;">{{{{ p.id }}}}</span></sc-for><button type="button" onClick="{{{{ x.go }}}}" style="{GOBTN}">On {{{{ x.where }}}}</button></div></div></sc-for></div>
            <p style="margin: 10px 0 0; {SMALL}">{{{{ sdAllStories }}}} stories in all; the checks that prove them run on every change, and Portal health lists what each one does.</p></section>
          <section style="{PANEL}"><h2 style="{H2}">Journeys</h2>
            <sc-if value="{{{{ sdNoJourney }}}}" hint-placeholder-val="{{{{ false }}}}"><p style="margin: 0; {SMALL}">No journey is mapped for this persona yet: suggest one with the Idea form.</p></sc-if>
            <sc-for list="{{{{ sdJourneys }}}}" as="j" hint-placeholder-count="1"><div style="margin-bottom: 12px;"><div style="font-size: 15px; font-weight: 800; margin-bottom: 8px;">{{{{ j.id }}}}: {{{{ j.title }}}}</div>
              <ol style="margin: 0; padding: 0; list-style: none; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 200px), 1fr)); gap: 8px;"><sc-for list="{{{{ j.stages }}}}" as="g" hint-placeholder-count="5"><li style="{CARD}"><div style="{LABEL}">{{{{ g.n }}}} &middot; {{{{ g.stage }}}}</div><div style="font-size: 13.5px; font-weight: 700;">{{{{ g.doing }}}}</div><div style="font-size: 12.5px; font-style: italic;">Feels: {{{{ g.feeling }}}}</div><div style="{SMALL}">{{{{ g.opp }}}}</div><button type="button" onClick="{{{{ g.go }}}}" style="{GOBTN}">{{{{ g.where }}}}</button></li></sc-for></ol></div></sc-for>
          </section>
          <section style="{PANEL}"><h2 style="{H2}">Service blueprints</h2><p style="margin: 0 0 10px; {SMALL}">What people do, what the page shows, what happens behind it, the processes that keep it working, and the checks that prove it. Scroll sideways on a small screen.</p>
            <sc-for list="{{{{ sdBlue }}}}" as="b" hint-placeholder-count="2"><div style="margin-bottom: 16px;"><div style="font-size: 15px; font-weight: 800; margin-bottom: 8px;">{{{{ b.id }}}}: {{{{ b.title }}}}</div>
              <div role="region" aria-label="{{{{ b.title }}}}" tabindex="0" style="overflow-x: auto; max-width: 100%;"><div style="{{{{ b.cols }}}}"><div style="{LABEL} padding: 6px 4px;">Layer</div><sc-for list="{{{{ b.phases }}}}" as="p" hint-placeholder-count="4"><div style="{LABEL} padding: 6px 4px; font-weight: 700;">{{{{ p.ph }}}}</div></sc-for>
                <sc-for list="{{{{ b.layers }}}}" as="l" hint-placeholder-count="5"><div style="font-size: 12.5px; font-weight: 800; padding: 8px 4px;">{{{{ l.layer }}}}</div><sc-for list="{{{{ l.cells }}}}" as="c" hint-placeholder-count="4"><div style="{CELL}"><span class="amp-sr">{{{{ l.layer }}}}, {{{{ c.ph }}}}: </span>{{{{ c.c }}}}</div></sc-for></sc-for></div></div></div></sc-for>
          </section>
          <section style="{PANEL}"><h2 style="{H2}">Processes and workflows</h2>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 300px), 1fr)); gap: 12px;"><sc-for list="{{{{ sdFlows }}}}" as="w" hint-placeholder-count="3"><div class="amp-card" style="{CARD}"><div style="{LABEL}">{{{{ w.id }}}}</div><div style="font-size: 14.5px; font-weight: 800;">{{{{ w.title }}}}</div><ol style="margin: 0; padding-left: 20px; font-size: 13px; line-height: 1.5;"><sc-for list="{{{{ w.steps }}}}" as="t" hint-placeholder-count="4"><li>{{{{ t.t }}}}</li></sc-for></ol><div style="font-size: 13px; font-weight: 800;">{{{{ w.decision }}}}</div><div style="font-size: 12.5px;"><span style="font-weight: 800;">Yes:</span> {{{{ w.yes }}}}</div><div style="font-size: 12.5px;"><span style="font-weight: 800;">No:</span> {{{{ w.no }}}}</div></div></sc-for></div>
            <p style="margin: 10px 0 0; {SMALL}">The same content, with flowcharts, is generated in the repository's docs/service-design folder.</p></section>
        </div>
        </sc-if>
'''

NAV6 = '      ["service", "Personas & journeys", "ring", 215, 4, "NEW", "service design personas user stories journeys blueprints processes workflows ucd user centred design needs"],\n'


def transforms():
    return [
        ("ext6-load", "the service design data loads with the rest", '"./data/research.json"].map(get));', '"./data/research.json", "./data/service-design.json"].map(get));', 1),
        ("ext6-load-vars", "name it", "cm, tt, iv, rs] =", "cm, tt, iv, rs, sd] =", 1),
        ("ext6-load-state", "keep it in state", "cm, tt, iv, rs, loaded", "cm, tt, iv, rs, sd, loaded", 1),
        ("ext6-nav", "Personas & journeys joins Get involved, after Research & design", '      ["ambassadors", "Ambassadors & champions",', NAV6 + '      ["ambassadors", "Ambassadors & champions",', 1),
        ("ext6-hash", "the screen can be linked to", "|stem|research)$/.test(id)", "|stem|research|service)$/.test(id)", 1),
        ("ext6-logic", "Service design logic", "  async loadPetition() {", LOGIC6 + "\n  async loadPetition() {", 1),
        ("ext6-vals", "its values join renderVals", "...this.ampVals5(s),", "...this.ampVals5(s), ...this.ampVals6(s),", 1),
        ("ext6-screen", "the Service design screen", '        <div data-slot="portal-end" style="display: none;"></div>', SCREEN6 + '\n        <div data-slot="portal-end" style="display: none;"></div>', 1),
    ]
