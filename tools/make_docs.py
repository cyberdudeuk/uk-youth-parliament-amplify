"""Generate CHANGELOG.md and docs/registers.md from data/ (one master, no hand-kept copies).
Run by build_site.py; check_site.py S11 fails if either file differs from what this would write."""
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


def write():
    os.makedirs(os.path.join(R, "docs"), exist_ok=True)
    open(os.path.join(R, "CHANGELOG.md"), "w", encoding="utf-8").write(changelog())
    open(os.path.join(R, "docs", "registers.md"), "w", encoding="utf-8").write(registers())


if __name__ == "__main__":
    write()
