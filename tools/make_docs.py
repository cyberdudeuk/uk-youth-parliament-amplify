"""Generate CHANGELOG.md, docs/registers.md and the research bundle in docs/research/ and the service design in docs/service-design/
from data/ (one master, no
hand-kept copies). Run by build_site.py; check_site.py S11 fails if any file differs from what this would write."""
import json, os

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def changelog():
    ch = json.load(open(os.path.join(R, "data", "changelog.json"), encoding="utf-8"))
    out = ["# Release log", "", "Generated from `data/changelog.json` by `tools/make_docs.py`. The portal shows the same log on its Release log screen, and flags each new (NEW) or changed (UPD) screen in the drawer and on the screen itself.", ""]
    for r in ch["releases"]:
        out += [f"## {r['version']} · {r['date']} · {r['status']}", "", f"**{r['title']}.** {r['summary']}", ""]
        out += [f"- **{e['kind']}** `{e['screen']}`: {e['what']}" for e in r["entries"]] + ([""] if r["entries"] else [])
    return "\n".join(out).rstrip() + "\n"


def registers():
    g = json.load(open(os.path.join(R, "data", "registers.json"), encoding="utf-8"))
    out = ["# Defect and open registers", "", "Generated from `data/registers.json` by `tools/make_docs.py`; shown live on the portal's Portal health screen.", "", "## Defects found and fixed", "",
           "| Id | Found | What | Root cause | Fix | Check |", "|---|---|---|---|---|---|"]
    out += [f"| {d['id']} | {d['found']} | {d['what']} | {d['root_cause']} | {d['fix']} | {d['check']} |" for d in g["defects"]]
    out += ["", "## Open, and who must act", "", "| Id | What | Who |", "|---|---|---|"]
    out += [f"| {o['id']} | {o['what']} | {o['who']} |" for o in g["open"]]
    return "\n".join(out) + "\n"


def _rs():
    return json.load(open(os.path.join(R, "data", "research.json"), encoding="utf-8"))


GEN = "Generated from `data/research.json` by `tools/make_docs.py`; edit that, not this file. The portal shows the same content on its Research & design screen."
NOTE = "Contact is by form only: no email address is published. Everything posted on GitHub is public, so never post names, schools or contact details."


def r_readme():
    d = _rs()
    rows = [("participant-information.md", "Young people, parents and carers", "What happens, what we keep, your rights"),
            ("consent-forms.md", "Participants and facilitators", "Consent for young people and for parents or carers"),
            ("screener.md", "Whoever arranges sessions", "Questions to recruit a balanced group, and the quotas"),
            ("session-guides.md", "Facilitators", "Timed guides, tasks and a journey template"),
            ("synthesis.md", "Facilitators", "Turning sessions into findings and changes"),
            ("ported.md", "Everyone", "What was ported from the owner's other portals, by MoSCoW")]
    out = ["# Research bundle", "", GEN, "", d["intro"], "", f"**Status:** {d['status']}", "", "| File | For | What it is |", "|---|---|---|"]
    out += [f"| [{f}]({f}) | {w} | {x} |" for f, w, x in rows]
    out += ["", "## Research questions", "", "| Id | When | Question | Methods | Status |", "|---|---|---|---|---|"]
    out += [f"| {q['id']} | {q['horizon']} | {q['text']} | {', '.join(q['methods'])} | {q['status']} |" for q in d["questions"]]
    out += ["", "## Rounds", "", "| Round | When | Who | Status |", "|---|---|---|---|"]
    out += [f"| {r['name']} | {r['when']} | {r['who']} | {r['status']} |" for r in d["rounds"]]
    return "\n".join(out + ["", NOTE]) + "\n"


def r_info():
    d = _rs()
    out = ["# Participant information", "", GEN, "", "## Why we are doing this research", "", d["why"], "", "## Our promise to you", ""]
    out += [f"- {p}" for p in d["promise"]]
    out += ["", "## What happens in a session", ""] + [f"- **{m['name']}** ({m['time']}): {m['what']} {m['young']}" for m in d["methods"]]
    out += ["", "## What we keep", "", d["consent"]["keep"], "", "## Taking part as a group", "", d["sign_up"]["group_route"], "", NOTE]
    return "\n".join(out) + "\n"


def r_consent():
    d = _rs()
    out = ["# Consent forms", "", GEN, "", "Read out and shared in advance, in plain English, easy read or BSL/ISL as needed. Consent can be given by speaking, signing, writing or ticking, and is checked again before any clip is reused.", "",
           "## For the young person", ""] + [f"- [ ] {s}" for s in d["consent"]["young"]]
    out += ["", "## For a parent or carer (required for under 16s)", ""] + [f"- [ ] {s}" for s in d["consent"]["parent"]]
    out += ["", "Session code (never a name): ________    Date: ________    Facilitator (role): ________", "", d["consent"]["keep"], "", NOTE]
    return "\n".join(out) + "\n"


def r_screener():
    d = _rs()
    out = ["# Screener and quotas", "", GEN, "", "Asked in a form that keeps contact details private. No question on GitHub ever asks who someone is.", "", "## Questions", ""]
    out += [f"{i}. **{q['q']}** {q['a']}." for i, q in enumerate(d["screener"], 1)]
    out += ["", "## Quotas", "", d["quotas_note"], "", "| Group | Minimum |", "|---|---|"] + [f"| {q['group']} | {q['min']} |" for q in d["quotas"]]
    out += ["", "## Signing up", "", d["sign_up"]["status_when_empty"], "", NOTE]
    return "\n".join(out) + "\n"


def r_sessions():
    d = _rs()
    out = ["# Session guides", "", GEN, ""]
    for s in d["sessions"]:
        out += [f"## {s['title']}", "", "| Minutes | Part | What happens |", "|---|---|---|"] + [f"| {x['min']} | {x['part']} | {x['detail']} |" for x in s["steps"]] + ["", s["note"], ""]
    out += ["## Journey template (UX and service design)", "", "| Stage | What I do | What I think or feel | What helps | What gets in the way |", "|---|---|---|---|---|"]
    out += [f"| {st} | | | | |" for st in ("Hear about Amplify", "First visit", "Find my route in", "Take part", "Come back", "Tell others")]
    out += ["", "## Design routes", ""] + [f"- **{x['name']}:** {x['how']} {x['share']}" for x in d["design"]]
    return "\n".join(out + ["", NOTE]) + "\n"


def r_synthesis():
    d = _rs()
    out = ["# Synthesis", "", GEN, "", "## Steps", ""] + [f"{i}. {s}" for i, s in enumerate(d["synthesis"], 1)]
    out += ["", "## Template", "", "| Theme | Evidence (session codes, never names) | Sessions | Severity (blocks, slows, annoys) | Change or backlog item |", "|---|---|---|---|---|", "| | | | | |"]
    out += ["", "## You said, we did", "", "| Id | Source | Theme | Evidence | What changed |", "|---|---|---|---|---|"]
    out += [f"| {f['id']} | {f['source']} | {f['theme']} | {f['evidence']} | {f['change']} |" for f in d["findings"]]
    out += ["", "## Benchmark", "", f"{d['benchmark']['credit']} {d['benchmark']['scoring']} {d['benchmark']['reading']}"]
    return "\n".join(out + ["", NOTE]) + "\n"


def r_ported():
    d = _rs()
    out = ["# Ported from the owner's other portals", "", GEN, "",
           "How participation, engagement and user research work in DQ Commons, the GitHub repos asset catalogue and govukOS, and what Amplify has taken from each, prioritised with MoSCoW.", "",
           "| MoSCoW | What | From | Done | Note |", "|---|---|---|---|---|"]
    order = {"Must": 0, "Should": 1, "Could": 2, "Won't": 3}
    out += [f"| {p['moscow']} | {p['what']} | {p['from']} | {'Yes' if p['done'] else 'Not yet'} | {p['note']} |" for p in sorted(d["ported"], key=lambda p: order[p["moscow"]])]
    return "\n".join(out) + "\n"


def _sd():
    return json.load(open(os.path.join(R, "data", "service-design.json"), encoding="utf-8"))


SDGEN = "Generated from `data/service-design.json` by `tools/make_docs.py`; edit that, not this file. The portal shows the same content on its Personas & journeys screen."


def _sdhead(title):
    d = _sd()
    return [f"# {title}", "", SDGEN, "", f"> **Status:** {d['status']}", ""]


def _role(d, pid):
    return next((p["role"] for p in d["personas"] if p["id"] == pid), pid)


def sd_readme():
    d = _sd()
    out = _sdhead("Service design") + [d["intro"], "", "| File | What it is |", "|---|---|"]
    out += [f"| [{f}]({f}) | {w} |" for f, w in (("personas.md", "Who Amplify is for"), ("user-stories.md", "What each persona needs to do, and the checks that prove it"),
                                                ("journeys.md", "Journeys through the portal, stage by stage"), ("service-blueprints.md", "From user actions to evidence"),
                                                ("processes-and-workflows.md", "The processes behind every screen, as flowcharts"))]
    return "\n".join(out) + "\n"


def sd_personas():
    d = _sd()
    out = _sdhead("Personas")
    for p in d["personas"]:
        out += [f"## {p['role']}", "", f"*{p['context']}*", "", f"**Goal:** {p['goal']}", "", f"**Needs:** {'; '.join(p['needs'])}", "",
                f"**Pain points:** {'; '.join(p['pains'])}", "", f"**Kept safe by:** {p['safety']}", "", f"**Starts at:** {p['starts']}", "", f"**Uses:** {', '.join(p['uses'])}", ""]
    return "\n".join(out).rstrip() + "\n"


def sd_stories():
    d = _sd()
    out = _sdhead("User stories") + ["Each story names the checks that prove it; they run on every change.", "", "| Id | Story | Where | Done when | Proved by |", "|---|---|---|---|---|"]
    out += [f"| {x['id']} | As a {_role(d, x['persona']).lower()}, I want to {x['want']}, so that {x['so']}. | {x['screen']} | {'<br>'.join(x['accept'])} | {', '.join(x['proved'])} |" for x in d["stories"]]
    return "\n".join(out) + "\n"


def sd_journeys():
    d = _sd()
    out = _sdhead("Journeys")
    for j in d["journeys"]:
        out += [f"## {j['id']}: {j['title']} ({_role(d, j['persona'])})", "", "| Stage | Doing | Feeling | Screen | Opportunity |", "|---|---|---|---|---|"]
        out += [f"| {g['stage']} | {g['doing']} | {g['feeling']} | {g['screen']} | {g['opportunity']} |" for g in j["stages"]] + [""]
    return "\n".join(out).rstrip() + "\n"


def sd_blueprints():
    d = _sd()
    out = _sdhead("Service blueprints")
    for b in d["blueprints"]:
        out += [f"## {b['id']}: {b['title']}", "", "| Layer | " + " | ".join(b["phases"]) + " |", "|---|" + "---|" * len(b["phases"])]
        out += [f"| **{l['layer']}** | " + " | ".join(l["cells"]) + " |" for l in b["layers"]] + [""]
    return "\n".join(out).rstrip() + "\n"


def sd_workflows():
    d = _sd()
    out = _sdhead("Processes and workflows")
    q = lambda t: t.replace('"', "'")
    for w in d["workflows"]:
        out += [f"## {w['id']}: {w['title']}", "", "```mermaid", "flowchart TD"]
        out += [f'  S{i}["{q(t)}"]' for i, t in enumerate(w["steps"])]
        out += [f"  S{i} --> S{i + 1}" for i in range(len(w["steps"]) - 1)]
        out += [f'  S{len(w["steps"]) - 1} --> D{{"{q(w["decision"])}"}}', f'  D -- Yes --> Y["{q(w["yes"])}"]', f'  D -- No --> N["{q(w["no"])}"]', "```", ""]
    return "\n".join(out).rstrip() + "\n"


def golive():
    d = json.load(open(os.path.join(R, "data", "readiness.json"), encoding="utf-8"))
    out = ["# Go-live readiness", "", "Generated from `data/readiness.json` by `tools/make_docs.py`; edit that, not this file. The portal shows the same content on its Go-live readiness screen.", "", d["intro"], ""]
    must = [g for g in d["gates"] if g["moscow"] == "Must" and g["status"] != "Pass"]
    out += [f"**Verdict:** {'ready to go live' if not must else 'not ready to go public yet: ' + str(len(must)) + ' Must gates open (' + ', '.join(g['id'] for g in must) + ')'}.", "",
            "## Gates", "", "| Id | Area | Gate | MoSCoW | Status | Proved by | Who must act |", "|---|---|---|---|---|---|---|"]
    out += [f"| {g['id']} | {g['area']} | {g['item']} | {g['moscow']} | {g['status']} | {', '.join(g['evidence'])} | {g['who']} |" for g in d["gates"]]
    out += ["", "## Self-routines", "", "| MoSCoW | Routine | Kind | What | Cadence | Where | Status |", "|---|---|---|---|---|---|---|"]
    out += [f"| {r['moscow']} | {r['routine']} | {r['kind']} | {r['what']} | {r['cadence']} | {r['where']} | {r['status']} |" for r in d["routines"]]
    return "\n".join(out) + "\n"


DOCS = {"CHANGELOG.md": changelog, "docs/registers.md": registers, "docs/research/README.md": r_readme,
        "docs/research/participant-information.md": r_info, "docs/research/consent-forms.md": r_consent,
        "docs/research/screener.md": r_screener, "docs/research/session-guides.md": r_sessions,
        "docs/research/synthesis.md": r_synthesis, "docs/research/ported.md": r_ported,
        "docs/service-design/README.md": sd_readme, "docs/service-design/personas.md": sd_personas,
        "docs/service-design/user-stories.md": sd_stories, "docs/service-design/journeys.md": sd_journeys,
        "docs/service-design/service-blueprints.md": sd_blueprints, "docs/service-design/processes-and-workflows.md": sd_workflows,
        "docs/go-live.md": golive}


def write():
    for path, fn in DOCS.items():
        os.makedirs(os.path.dirname(os.path.join(R, path)) or R, exist_ok=True)
        open(os.path.join(R, path), "w", encoding="utf-8").write(fn())


if __name__ == "__main__":
    write()
