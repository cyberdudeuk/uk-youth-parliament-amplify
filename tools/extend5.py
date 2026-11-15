"""Fifth set of portal extensions: the Research & design screen, ported from the owner's other portals.

  research  Take part in user research and in UI, UX, graphic and content design: the panel and its promise to young
            people and families, research questions, methods, rounds, design routes, working groups, You said we did,
            recognition badges, the MoSCoW list of what was ported from DQ Commons, the GitHub repos asset catalogue and
            govukOS, and the System Usability Scale worked out on the device (16 and over; nothing is sent).
Text comes from data/research.json; the research bundle in docs/research/ is generated from the same file.
"""
from extend import PANEL, LABEL, SMALL
from extend4 import head, ext, term, H2, CARD, GOBTN, NOTE, OL

LOGIC5 = r'''
  ampVals5(s) {
    const A = s.amp || {}, rs = A.rs || {}, iv = A.iv || {}, repo = iv.repo || "";
    const label = (id) => { try { return this.screenLabel(id) || id; } catch (e) { return id; } };
    const M = {}; (rs.methods || []).forEach((m) => { M[m.id] = m.name; });
    const names = (ids) => (ids || []).map((i) => M[i] || i).join(", ");
    const bm = rs.benchmark || { items: [], scale: [] }, ans = s.sus || [];
    const done = bm.items.length > 0 && bm.items.every((x, k) => ans[k]);
    const score = done ? ans.reduce((t, a, k) => t + (k % 2 === 0 ? a - 1 : 5 - a), 0) * 2.5 : null;
    const MO = { Must: 25, Should: 70, Could: 175, "Won't": 300 };
    const formUrl = (rs.sign_up || {}).form_url || "";
    return {
      sResearch: s.screen === "research",
      rsStatus: rs.status || "", rsIntro: rs.intro || "", rsWhy: rs.why || "",
      rsHasForm: !!formUrl, rsNoFormShow: !formUrl, rsForm: formUrl, rsNoForm: (rs.sign_up || {}).status_when_empty || "", rsGroup: (rs.sign_up || {}).group_route || "",
      rsInterest: repo + "/issues/new?template=contact.yml",
      rsPromise: (rs.promise || []).map((t) => ({ t })),
      rsDesign: (rs.design || []).map((d) => ({ name: d.name, how: d.how, share: d.share, icon: this.ampIcon(d.icon, "oklch(var(--t3) 0.16 300)", 18) })),
      rsIdea: repo + "/issues/new?template=idea.yml",
      rsMethods: (rs.methods || []).map((m) => ({ name: m.name, time: m.time, what: m.what, young: m.young })),
      rsQs: (rs.questions || []).map((q) => ({ id: q.id, text: q.text, horizon: q.horizon, how: names(q.methods), status: q.status })),
      rsRounds: (rs.rounds || []).map((r) => ({ name: r.name, when: r.when, who: r.who, how: names(r.methods), status: r.status })),
      rsFindings: (rs.findings || []).map((f) => ({ id: f.id, source: f.source, theme: f.theme, evidence: f.evidence, change: f.change, where: label(f.screen), go: () => this.setState({ screen: f.screen }) })),
      rsGroups: rs.groups || [], rsTerms: (rs.group_terms || []).map((t) => ({ t })),
      rsBadges: rs.badges || [], rsBadgeNote: rs.badge_note || "",
      rsPorted: (rs.ported || []).map((p) => ({ what: p.what, from: p.from, moscow: p.moscow, note: p.note, hasNote: !!p.note, done: p.done ? "Done" : "Not yet",
        pill: "display:inline-block;border-radius:999px;padding:2px 9px;font-family:'Space Mono',monospace;font-size:11px;font-weight:700;background:oklch(var(--t1) 0.16 " + (MO[p.moscow] || 175) + " / 0.28);color:oklch(var(--t4) 0.15 " + (MO[p.moscow] || 175) + ");" })),
      rsBundle: repo + "/tree/main/docs/research",
      susCredit: bm.credit || "", susReading: bm.reading || "",
      susItems: bm.items.map((text, k) => ({ n: String(k + 1), text, opts: bm.scale.map((lab, j) => ({ lab, pressed: ans[k] === j + 1 ? "true" : "false",
        pick: () => { const a = (this.state.sus || []).slice(); a[k] = j + 1; this.setState({ sus: a }); },
        style: "min-height:36px;border-radius:999px;padding:6px 11px;font-size:12.5px;font-weight:700;cursor:pointer;border:1px solid " + (ans[k] === j + 1 ? "oklch(var(--t2) 0.16 145)" : "rgb(var(--film-rgb) / 0.2)") + ";background:" + (ans[k] === j + 1 ? "oklch(var(--t1) 0.16 145 / 0.3)" : "transparent") + ";color:rgb(var(--ink-rgb));" })) })),
      susDone: done, susScore: done ? String(score) : "", susLeft: String(bm.items.length - ans.filter(Boolean).length), susShowLeft: !done,
      susReset: () => this.setState({ sus: [] }),
      icResearch: this.ampIcon("pencil-ruler", "oklch(var(--t3) 0.16 300)", 16), icGauge: this.ampIcon("gauge", "oklch(var(--t3) 0.16 145)", 18)
    };
  }
'''

UL = "margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 6px; font-size: 13.5px; line-height: 1.5;"

SCREEN5 = f'''
        <sc-if value="{{{{ sResearch }}}}" hint-placeholder-val="{{{{ false }}}}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          {head("icResearch", 300, "Shape Amplify: user research and design", "{{ rsIntro }}")}
          <div role="note" style="{NOTE} border: 1px dashed oklch(var(--t2) 0.16 70 / 0.8); background: oklch(var(--t1) 0.16 70 / 0.12);"><span style="font-weight: 800;">Status.</span> {{{{ rsStatus }}}}</div>
          <section style="{PANEL} display: flex; flex-direction: column; gap: 10px;">
            <h2 style="margin: 0; font-size: 17px; font-weight: 800;">Join the research panel</h2>
            <sc-if value="{{{{ rsHasForm }}}}" hint-placeholder-val="{{{{ false }}}}">{ext("rsForm", "Open the private sign-up form")}</sc-if>
            <sc-if value="{{{{ rsNoFormShow }}}}" hint-placeholder-val="{{{{ true }}}}"><p style="margin: 0; font-size: 13.5px; line-height: 1.55;">{{{{ rsNoForm }}}}</p><div>{ext("rsInterest", "Register interest with the contact form")}</div></sc-if>
            <p style="margin: 0; {SMALL}"><span style="font-weight: 800;">As a group:</span> {{{{ rsGroup }}}}</p>
          </section>
          <section style="{PANEL}"><h2 style="{H2}">Our promise to young people and families</h2><ul style="{UL}"><sc-for list="{{{{ rsPromise }}}}" as="p" hint-placeholder-count="6"><li>{{{{ p.t }}}}</li></sc-for></ul><p style="margin: 10px 0 0; {SMALL}">Every session follows {term("safeguarding", "safeguarding")} rules, and facilitators have a {term("dbs", "background check")}.</p></section>
          <section style="{PANEL}"><h2 style="{H2}">Design with us</h2><p style="margin: 0 0 10px; {SMALL}">You do not need to take part in a session to shape Amplify. Pick a kind of design and share your work in the open, without names, faces or school logos.</p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr)); gap: 10px;"><sc-for list="{{{{ rsDesign }}}}" as="d" hint-placeholder-count="4"><div class="amp-card" style="{CARD}"><div style="display: flex; align-items: center; gap: 8px; font-size: 14.5px; font-weight: 800;"><span aria-hidden="true" style="{{{{ d.icon }}}}"></span>{{{{ d.name }}}}</div><div style="{SMALL}">{{{{ d.how }}}}</div><div style="font-size: 12.5px;"><span style="font-weight: 800;">Share it:</span> {{{{ d.share }}}}</div></div></sc-for></div>
            <div style="margin-top: 10px;">{ext("rsIdea", "Share a design or rewrite")}</div></section>
          <section style="{PANEL}"><h2 style="{H2}">Ways to take part</h2><div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 250px), 1fr)); gap: 10px;"><sc-for list="{{{{ rsMethods }}}}" as="m" hint-placeholder-count="6"><div style="{CARD}"><div style="font-size: 14px; font-weight: 800;">{{{{ m.name }}}}</div><div style="{LABEL}">{{{{ m.time }}}}</div><div style="{SMALL}">{{{{ m.what }}}}</div><div style="font-size: 12.5px; font-style: italic;">{{{{ m.young }}}}</div></div></sc-for></div></section>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 340px), 1fr)); gap: 14px;">
            <section style="{PANEL}"><h2 style="{H2}">What we want to learn</h2><ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 10px;"><sc-for list="{{{{ rsQs }}}}" as="q" hint-placeholder-count="5"><li style="font-size: 13.5px; line-height: 1.5;"><span style="font-family: 'Space Mono', monospace; font-size: 11.5px; font-weight: 700;">{{{{ q.id }}}} &middot; {{{{ q.horizon }}}}</span><br />{{{{ q.text }}}}<br /><span style="{SMALL}">{{{{ q.how }}}} &middot; {{{{ q.status }}}}</span></li></sc-for></ul></section>
            <section style="{PANEL}"><h2 style="{H2}">Research rounds</h2><ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 10px;"><sc-for list="{{{{ rsRounds }}}}" as="r" hint-placeholder-count="3"><li style="font-size: 13.5px; line-height: 1.5;"><span style="font-weight: 800;">{{{{ r.name }}}}</span><br />{{{{ r.when }}}} &middot; {{{{ r.status }}}}<br /><span style="{SMALL}">{{{{ r.who }}}}. {{{{ r.how }}}}.</span></li></sc-for></ul><div style="margin-top: 10px;">{ext("rsBundle", "The research bundle: information, consent, screener, guides")}</div></section>
          </div>
          <section style="{PANEL}"><h2 style="{H2}">You said, we did</h2><div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr)); gap: 10px;"><sc-for list="{{{{ rsFindings }}}}" as="f" hint-placeholder-count="4"><div style="{CARD}"><div style="{LABEL}">{{{{ f.id }}}} &middot; {{{{ f.source }}}}</div><div style="font-size: 14px; font-weight: 800;">{{{{ f.theme }}}}</div><div style="{SMALL}"><span style="font-weight: 800;">We did:</span> {{{{ f.change }}}}</div><div style="font-size: 12px; color: rgb(var(--ink-rgb) / 0.75);">Evidence: {{{{ f.evidence }}}}</div><button type="button" onClick="{{{{ f.go }}}}" style="{GOBTN}">See {{{{ f.where }}}}</button></div></sc-for></div></section>
          <section aria-labelledby="amp-sus-h" style="{PANEL}">
            <h2 id="amp-sus-h" style="margin: 0 0 4px; display: flex; align-items: center; gap: 8px; font-size: 17px; font-weight: 800;"><span aria-hidden="true" style="{{{{ icGauge }}}}"></span>How easy is Amplify to use? (16 and over)</h2>
            <p style="margin: 0 0 12px; {SMALL}">Ten quick statements. Your score is worked out on this device and nothing is sent or stored. {{{{ susCredit }}}}</p>
            <ol style="margin: 0; padding-left: 22px; display: flex; flex-direction: column; gap: 12px;"><sc-for list="{{{{ susItems }}}}" as="i" hint-placeholder-count="10"><li style="font-size: 13.5px;"><div style="margin-bottom: 6px; font-weight: 700;">{{{{ i.text }}}}</div><div role="group" aria-label="{{{{ i.text }}}}" style="display: flex; flex-wrap: wrap; gap: 6px;"><sc-for list="{{{{ i.opts }}}}" as="o" hint-placeholder-count="5"><button type="button" onClick="{{{{ o.pick }}}}" aria-pressed="{{{{ o.pressed }}}}" style="{{{{ o.style }}}}">{{{{ o.lab }}}}</button></sc-for></div></li></sc-for></ol>
            <div role="status" aria-live="polite" style="margin-top: 14px; display: flex; flex-wrap: wrap; align-items: center; gap: 12px;">
              <sc-if value="{{{{ susDone }}}}" hint-placeholder-val="{{{{ false }}}}"><span style="font-size: 22px; font-weight: 900;">Your score: {{{{ susScore }}}} out of 100</span><span style="{SMALL}">{{{{ susReading }}}}</span></sc-if>
              <sc-if value="{{{{ susShowLeft }}}}" hint-placeholder-val="{{{{ true }}}}"><span style="{SMALL}">{{{{ susLeft }}}} statements left to answer.</span></sc-if>
              <button type="button" onClick="{{{{ susReset }}}}" style="min-height: 36px; border-radius: 999px; padding: 6px 14px; border: 1px solid rgb(var(--film-rgb) / 0.2); background: transparent; color: rgb(var(--ink-rgb)); font-size: 13px; font-weight: 700; cursor: pointer;">Start again</button>
            </div>
          </section>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr)); gap: 14px;">
            <section style="{PANEL}"><h2 style="{H2}">Working groups</h2><ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 8px;"><sc-for list="{{{{ rsGroups }}}}" as="g" hint-placeholder-count="5"><li style="font-size: 13.5px; line-height: 1.5;"><span style="font-weight: 800;">{{{{ g.name }}}}</span> <span style="{LABEL}">{{{{ g.status }}}}</span><br />{{{{ g.purpose }}}}</li></sc-for></ul><ul style="margin: 12px 0 0; padding-left: 20px; {SMALL}"><sc-for list="{{{{ rsTerms }}}}" as="t" hint-placeholder-count="4"><li>{{{{ t.t }}}}</li></sc-for></ul></section>
            <section style="{PANEL}"><h2 style="{H2}">Recognition</h2><ul style="margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 8px;"><sc-for list="{{{{ rsBadges }}}}" as="b" hint-placeholder-count="6"><li style="font-size: 13.5px; line-height: 1.5;"><span style="font-weight: 800;">{{{{ b.name }}}}</span> <span style="{LABEL}">{{{{ b.confirm }}}}</span><br />{{{{ b.how }}}}</li></sc-for></ul><p style="margin: 10px 0 0; {SMALL}">{{{{ rsBadgeNote }}}}</p></section>
          </div>
          <section style="{PANEL}"><h2 style="{H2}">What we brought over from the owner's other portals</h2><p style="margin: 0 0 10px; {SMALL}">How participation and research work in DQ Commons, the GitHub repos asset catalogue and govukOS, and what Amplify has taken from each, prioritised as Must, Should, Could or Won't have this time.</p>
            <div style="display: flex; flex-direction: column; gap: 8px;"><sc-for list="{{{{ rsPorted }}}}" as="p" hint-placeholder-count="8"><div style="{CARD} flex-direction: row; flex-wrap: wrap; align-items: baseline; gap: 6px 12px;"><span style="{{{{ p.pill }}}}">{{{{ p.moscow }}}}</span><span style="flex: 1 1 280px; min-width: 0; font-size: 13.5px; font-weight: 700;">{{{{ p.what }}}}</span><span style="{SMALL}">{{{{ p.from }}}} &middot; {{{{ p.done }}}}</span><sc-if value="{{{{ p.hasNote }}}}" hint-placeholder-val="{{{{ false }}}}"><span style="flex: 1 1 100%; {SMALL}">{{{{ p.note }}}}</span></sc-if></div></sc-for></div></section>
        </div>
        </sc-if>
'''

NAV5 = '      ["research", "Research & design", "dia", 300, 4, "NEW", "user research design ux ui interaction graphic content design co-design usability test panel survey interview feedback participate"],\n'


def transforms():
    return [
        ("ext5-load", "the research data loads with the rest", '"./data/tooltips.json", "./data/involve.json"].map(get));', '"./data/tooltips.json", "./data/involve.json", "./data/research.json"].map(get));', 1),
        ("ext5-load-vars", "name it", "cm, tt, iv] =", "cm, tt, iv, rs] =", 1),
        ("ext5-load-state", "keep it in state", "cm, tt, iv, loaded", "cm, tt, iv, rs, loaded", 1),
        ("ext5-nav", "Research & design joins Get involved, after Contribute", '      ["ambassadors", "Ambassadors & champions",', NAV5 + '      ["ambassadors", "Ambassadors & champions",', 1),
        ("ext5-hash", "the screen can be linked to", "|learn|stem)$/.test(id)", "|learn|stem|research)$/.test(id)", 1),
        ("ext5-logic", "Research & design logic", "  async loadPetition() {", LOGIC5 + "\n  async loadPetition() {", 1),
        ("ext5-vals", "its values join renderVals", "...this.ampVals4(s),", "...this.ampVals4(s), ...this.ampVals5(s),", 1),
        ("ext5-screen", "the Research & design screen", '        <div data-slot="portal-end" style="display: none;"></div>', SCREEN5 + '\n        <div data-slot="portal-end" style="display: none;"></div>', 1),
    ]
