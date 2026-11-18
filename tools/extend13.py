"""Thirteenth set of portal extensions: see the data, read it easily, and learn by doing (17 November 2026).

  issues     A "How much it matters" panel on Issue domains, in six views of the same sourced data: a wheel of Make Your
             Mark 2024 votes by topic, ranked shares with 2022 alongside, worry (survey) beside votes (ballot), what
             young people have actually done, turnout over ten years, and a plain table. Each domain card now says
             which ballot topic covers it, how many votes that topic drew and which domains share it, so a domain is
             never credited with votes it shares. Selecting a topic drills down to its domains.
  numbers    A new Foundations screen, "Young people in numbers": who young people are (ethnicity, language), their
             stage of life, money and home, where they live (tile maps), what they face, their hopes and voice, and
             the opportunity gaps. Every figure is a CSS chart with a hidden data table, a "show as tables" switch, a
             plain "what this shows" and a "read with care", and V/S provenance per source.
  acad       The four Academy modules were static cards with hard-coded "complete", "in progress" and "locked" states
             and no lessons behind them, and the lede claimed completion fed the launch-readiness gate, which it does
             not (D40). Each module is now a button that opens a sourced lesson with a question; progress is real,
             starts empty and stays on the device.
  drill      Policy landscape manifesto cards and the Campaign hub's votes-at-16 card open the matching issue domain.
             Two unsourced relaunch claims (the D26 defect class) and a stale "three days ago" are corrected.
"""
import json, os

from extend import PANEL, LABEL, SMALL, EYEBROW, H1, LEDE
from extend4 import H2, CARD
from extend11 import A, SEL, BTN

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHART_TYPES = ("donut", "bars", "columns", "dumbbell", "slope", "waffle", "stack", "tiles", "kpi", "list")


def load(name):
    with open(os.path.join(R, "data", name), encoding="utf-8") as f:
        return json.load(f)


LOGIC13 = r'''
  ampChart(f, SRC) {
    const arr = (x) => (Array.isArray(x) ? x : []), n = (v) => (typeof v === "number" && isFinite(v) ? v : 0);
    const fmt = (v, u) => { const x = n(v); const s = x >= 1000 ? Math.round(x).toLocaleString("en-GB") : String(Math.round(x * 100) / 100); return u === "%" || (u || "").indexOf("%") === 0 ? s + "%" : s; };
    const col = (h, a) => "oklch(var(--t2) 0.16 " + (h || 175) + (a ? " / " + a : "") + ")";
    const pill = (h) => "display:inline-block;border-radius:999px;padding:1px 8px;font-family:'Space Mono',monospace;font-size:10.5px;font-weight:700;background:oklch(var(--t1) 0.16 " + h + " / 0.28);color:oklch(var(--t4) 0.15 " + h + ");";
    const cite = (list) => arr(list).map((id) => { const x = (SRC || {})[id] || {}; const off = x.provenance === "V";
      return { label: x.label || id, url: x.url || "#", prov: off ? "Official" : "Secondary", pStyle: pill(off ? 145 : 70) }; });
    const t = f.type, u = f.unit || "", c = { type: t, isDonut: t === "donut", isBars: t === "bars", isColumns: t === "columns", isDumbbell: t === "dumbbell" || t === "slope",
      isWaffle: t === "waffle", isStack: t === "stack", isTiles: t === "tiles", isKpi: t === "kpi", isList: t === "list", rows: [], legend: [], cells: [], cols: [], tiles: [], items: [], table: [] };
    if (t === "donut" || t === "stack") {
      const segs = arr(f.segments), tot = segs.reduce((a, x) => a + n(x.v), 0) || 1; let acc = 0; const stops = [];
      segs.forEach((x, i) => { const p = t === "stack" ? n(x.v) : (n(x.v) / tot) * 100; const h = x.hue || [175, 70, 300, 25, 145, 215][i % 6];
        if (t === "donut") { stops.push(col(h) + " " + acc.toFixed(2) + "% " + (acc + p).toFixed(2) + "%"); }
        c.legend.push({ t: x.t, val: t === "donut" ? fmt(x.v) : fmt(x.v, "%"), pct: (Math.round(p * 10) / 10) + "%", sw: "flex:0 0 12px;width:12px;height:12px;border-radius:3px;background:" + col(h) + ";",
          seg: "display:block;height:100%;width:" + Math.min(100, p) + "%;background:" + col(h) + ";" });
        c.table.push({ k: x.t, v: (t === "donut" ? fmt(x.v) + " (" + (Math.round(p * 10) / 10) + "%)" : fmt(x.v, "%")) }); acc += p; });
      c.ring = "width:min(100%,200px);aspect-ratio:1;border-radius:50%;background:conic-gradient(" + stops.join(",") + ");-webkit-mask:radial-gradient(circle,transparent 54%,#000 55%);mask:radial-gradient(circle,transparent 54%,#000 55%);";
      c.center = t === "donut" ? fmt(tot) : fmt(segs.reduce((a, x) => a + n(x.v), 0), "%");
    } else if (t === "bars") {
      const it = arr(f.items), mx = n(f.max) || Math.max.apply(null, it.map((x) => n(x.v)).concat([1]));
      c.rows = it.map((x, i) => ({ t: x.t, val: fmt(x.v, u), ref: !!x.ref, derived: !!x.derived,
        bar: "display:block;height:12px;border-radius:999px;width:" + Math.max(1.5, (n(x.v) / mx) * 100) + "%;background:" + (x.ref ? "rgb(var(--ink-rgb) / 0.45)" : col(x.hue || f.hue || 175)) + ";" }));
      c.table = it.map((x) => ({ k: x.t, v: fmt(x.v, u) }));
    } else if (t === "columns") {
      const it = arr(f.items), mx = n(f.max) || Math.max.apply(null, it.map((x) => n(x.v)).concat([1]));
      c.cols = it.map((x) => ({ t: x.t, val: fmt(x.v, u), bar: "display:block;width:100%;border-radius:8px 8px 3px 3px;height:" + Math.max(2, (n(x.v) / mx) * 100) + "%;background:" + col(x.hue || f.hue || 300) + ";" }));
      c.table = it.map((x) => ({ k: x.t, v: fmt(x.v, u) }));
    } else if (t === "dumbbell" || t === "slope") {
      const it = t === "slope" ? [{ t: f.h, a: f.from, b: f.to }] : arr(f.items), mx = n(f.max) || 100;
      c.rows = it.map((x) => { const a = (n(x.a.v) / mx) * 100, b = (n(x.b.v) / mx) * 100, lo = Math.min(a, b), hi = Math.max(a, b);
        return { t: x.t, aT: x.a.t, aV: fmt(x.a.v, u), bT: x.b.t, bV: fmt(x.b.v, u),
          line: "position:absolute;top:50%;height:4px;margin-top:-2px;border-radius:2px;left:" + lo + "%;width:" + (hi - lo) + "%;background:rgb(var(--ink-rgb) / 0.3);",
          aDot: "position:absolute;top:50%;width:16px;height:16px;margin:-8px 0 0 -8px;border-radius:50%;left:" + a + "%;background:" + col(215) + ";border:2px solid rgb(var(--bg1-rgb));",
          bDot: "position:absolute;top:50%;width:16px;height:16px;margin:-8px 0 0 -8px;border-radius:50%;left:" + b + "%;background:" + col(25) + ";border:2px solid rgb(var(--bg1-rgb));",
          aSw: "display:inline-block;width:10px;height:10px;border-radius:50%;background:" + col(215) + ";", bSw: "display:inline-block;width:10px;height:10px;border-radius:50%;background:" + col(25) + ";" }; });
      it.forEach((x) => { c.table.push({ k: x.t + ": " + x.a.t, v: fmt(x.a.v, u) }); c.table.push({ k: x.t + ": " + x.b.t, v: fmt(x.b.v, u) }); });
    } else if (t === "waffle") {
      const k = Math.round(n(f.v));
      for (let i = 0; i < 100; i++) c.cells.push({ s: "display:block;aspect-ratio:1;border-radius:3px;background:" + (i < k ? col(25) : "rgb(var(--film-rgb) / 0.14)") + ";" });
      c.big = fmt(f.v, "%"); c.table = [{ k: f.h, v: fmt(f.v, "%") }];
    } else if (t === "tiles") {
      const it = arr(f.items), vs = it.map((x) => n(x.v)), mx = Math.max.apply(null, vs.concat([1])), mn = Math.min.apply(null, vs);
      c.tiles = it.map((x) => { const r = mx === mn ? 1 : (n(x.v) - mn) / (mx - mn);
        return { t: x.t, val: fmt(x.v, u), s: "grid-row:" + x.r + ";grid-column:" + x.c + ";display:flex;flex-direction:column;justify-content:space-between;gap:2px;min-height:64px;border-radius:12px;padding:7px 8px;border:1px solid rgb(var(--film-rgb) / 0.18);background:oklch(var(--t2) 0.16 25 / " + (0.08 + r * 0.62).toFixed(2) + ");" }; });
      c.refT = f.ref ? f.ref.t + " " + fmt(f.ref.v, u) : ""; c.hasRef = !!f.ref;
      c.lo = fmt(mn, u); c.hi = fmt(mx, u);
      c.table = it.map((x) => ({ k: x.t, v: fmt(x.v, u) }));
    } else if (t === "kpi") { c.big = f.v; c.table = [{ k: f.h, v: f.v }];
    } else if (t === "list") { c.items = arr(f.items).map((x) => ({ t: x.t, cites: cite(x.src) })); c.table = []; }
    c.hasTable = c.table.length > 0; c.role = t === "list" ? "group" : "img";
    c.alt = f.h + (f.where ? " (" + f.where + "). " : ". ") + c.table.map((r) => r.k + ": " + r.v).join("; ");
    return c;
  }
  ampVals13(s) {
    const A = s.amp || {}, arr = (x) => (Array.isArray(x) ? x : []), n = (v) => (typeof v === "number" && isFinite(v) ? v : 0);
    const pill = (h) => "display:inline-block;border-radius:999px;padding:1px 8px;font-family:'Space Mono',monospace;font-size:10.5px;font-weight:700;background:oklch(var(--t1) 0.16 " + h + " / 0.28);color:oklch(var(--t4) 0.15 " + h + ");";
    const srcMap = (o) => { const m = {}; arr((o || {}).sources).forEach((x) => { m[x.id] = x; }); return m; };
    const cite = (list, M) => arr(list).map((id) => { const x = M[id] || {}; const off = x.provenance === "V"; return { label: x.label || id, url: x.url || "#", prov: off ? "Official" : "Secondary", pStyle: pill(off ? 145 : 70) }; });
    const L = {}; this.GROUPS.forEach(([g, items]) => items.forEach(([id, lbl]) => { L[id] = lbl; }));
    const go = (id, extra) => () => this.setState(Object.assign({ screen: id }, extra || {}), () => { try { window.scrollTo(0, 0); } catch (e) { /* no window */ } });
    const tabsOf = (list, cur, set, prefix, hue) => {
      const ids = list.map((t) => t.id);
      const key = (e) => { const c0 = ((e.currentTarget && e.currentTarget.id) || "").replace(prefix, ""); let i = ids.indexOf(c0); if (i < 0) return;
        if (e.key === "ArrowRight") i = (i + 1) % ids.length; else if (e.key === "ArrowLeft") i = (i - 1 + ids.length) % ids.length; else if (e.key === "Home") i = 0; else if (e.key === "End") i = ids.length - 1; else return;
        e.preventDefault(); const o = {}; o[set] = ids[i]; this.setState(o, () => { const b = document.getElementById(prefix + ids[i]); if (b) b.focus(); }); };
      return list.map((t) => ({ label: t.label, tid: prefix + t.id, sel: cur === t.id ? "true" : "false", tab: cur === t.id ? "0" : "-1", key, go: () => { const o = {}; o[set] = t.id; this.setState(o); },
        icon: this.ampIcon(t.icon || "chart-column", cur === t.id ? "oklch(var(--t4) 0.15 " + hue + ")" : "rgb(var(--ink-rgb) / 0.75)", 15),
        style: "display:inline-flex;align-items:center;gap:7px;min-height:40px;padding:8px 14px;border-radius:999px;cursor:pointer;font-size:13.5px;font-weight:800;border:1px solid " + (cur === t.id ? "oklch(var(--t2) 0.15 " + hue + " / 0.9);background:oklch(var(--t1) 0.16 " + hue + " / 0.3);color:rgb(var(--ink-rgb));" : "rgb(var(--film-rgb) / 0.2);background:transparent;color:rgb(var(--ink-rgb) / 0.86);") }));
    };
    const out = {};

    /* ---- Issue domains: how much it matters ---- */
    const sl = A.sl || {}, SLS = srcMap(sl), b24 = arr(sl.ballots)[0] || { topics: [], total: 0 }, b22 = arr(sl.ballots)[1] || { topics: [], total: 0 };
    const T24 = {}; arr(b24.topics).forEach((x) => { T24[x.id] = x; });
    const T22 = {}; arr(b22.topics).forEach((x) => { T22[x.id] = x; });
    const cw = sl.crosswalk || {}, ISS = this.ISSUES || {};
    const domainsOf = (tid) => Object.keys(cw).filter((k) => cw[k] === tid && ISS[k]).map((k) => ({ label: ISS[k][0], go: () => this.setState({ issue: k }, () => { const el = document.getElementById("amp-issue-card"); if (el && el.scrollIntoView) el.scrollIntoView({ block: "start" }); }) }));
    const share = (v, tot) => (tot ? Math.round((n(v) / tot) * 1000) / 10 : 0);
    const SVIEWS = [{ id: "wheel", label: "Wheel", icon: "target" }, { id: "rank", label: "Ranked, with 2022", icon: "chart-column" }, { id: "feel", label: "Worry beside votes", icon: "heart-pulse" },
      { id: "act", label: "What they did", icon: "megaphone" }, { id: "time", label: "Turnout over time", icon: "chart-line" }, { id: "table", label: "Table", icon: "list-checks" }];
    const sv = SVIEWS.some((v) => v.id === s.slView) ? s.slView : "wheel";
    const HUES = [175, 25, 300, 70, 145, 215, 340, 250, 110, 45];
    const topics = arr(b24.topics).map((x, i) => ({ id: x.id, t: x.label, v: x.votes, hue: HUES[i % HUES.length] }));
    const selT = T24[s.slTopic] ? s.slTopic : (topics[0] || {}).id;
    const wheel = this.ampChart({ type: "donut", h: "Make Your Mark 2024 votes by topic", where: "aged 11 to 18", segments: topics }, SLS);
    wheel.legend = wheel.legend.map((l, i) => Object.assign(l, { id: topics[i].id, sel: topics[i].id === selT ? "true" : "false",
      go: () => this.setState({ slTopic: topics[i].id }),
      style: "display:flex;align-items:center;gap:8px;width:100%;min-height:36px;padding:5px 9px;border-radius:10px;cursor:pointer;text-align:left;font-size:13px;color:rgb(var(--ink-rgb));border:1px solid " + (topics[i].id === selT ? "oklch(var(--t2) 0.15 175 / 0.8);background:oklch(var(--t1) 0.16 175 / 0.18);" : "transparent;background:transparent;") }));
    const st = T24[selT] || {}, stDomains = domainsOf(selT);
    const rank = arr(b24.topics).slice().sort((a, b) => b.votes - a.votes).map((x) => { const p = share(x.votes, b24.total), q = T22[x.id] ? share(T22[x.id].votes, b22.total) : null;
      return { t: x.label, val: p + "%", votes: n(x.votes).toLocaleString("en-GB"), was: q === null ? "not on the 2022 ballot" : "2022: " + q + "%" + (T22[x.id].renamed ? " (as " + T22[x.id].label + ")" : ""),
        bar: "display:block;height:12px;border-radius:999px;width:" + (p / 20) * 100 + "%;background:oklch(var(--t2) 0.16 175);",
        tick: q === null ? "display:none;" : "position:absolute;top:-3px;width:3px;height:18px;border-radius:2px;background:rgb(var(--ink-rgb) / 0.75);left:" + Math.min(100, (q / 20) * 100) + "%;" }; });
    const order = arr(b24.topics).slice().sort((a, b) => b.votes - a.votes).map((x) => x.id), nth = (k) => { const i = order.indexOf(k) + 1; return i + (i === 1 ? "st" : i === 2 ? "nd" : i === 3 ? "rd" : "th"); };
    const W = sl.worry || {}, worryRows = arr(W.items).map((x) => { const tv = T24[x.topic] || {}; const p = share(tv.votes, b24.total);
      return { t: x.t, topic: tv.label || "", w: x.pct + "%", v: p + "%", rank: nth(x.topic) + " of " + order.length + " topics", note: x.note || "", hasNote: !!x.note,
        wBar: "display:block;height:10px;border-radius:999px;width:" + x.pct + "%;background:oklch(var(--t2) 0.16 25);",
        vBar: "display:block;height:10px;border-radius:999px;width:" + p + "%;background:oklch(var(--t2) 0.16 175);" }; });
    const Ac = sl.action || {};
    const actBars = this.ampChart({ type: "bars", h: "What 14 to 24 year olds had done in the last three months", unit: "%", max: 100, items: arr(Ac.items).map((x) => ({ t: x.t, v: x.pct, hue: 300 })) }, SLS);
    const actStack = this.ampChart({ type: "stack", h: "How many of the six things they had done", unit: "%", segments: arr(Ac.levels).map((x, i) => ({ t: x.t, v: x.pct, hue: [250, 70, 145][i] })) }, SLS);
    const TO = sl.turnout || {};
    const tcols = this.ampChart({ type: "columns", h: "Make Your Mark votes cast", unit: "", items: arr(TO.years).map((x) => ({ t: x.year, v: x.votes, hue: 175 })) }, SLS);
    tcols.cols = tcols.cols.map((cx, i) => Object.assign(cx, { pct: arr(TO.years)[i].pct + "%" }));
    const card = (k) => { const tid = cw[k]; if (tid === undefined) return null; if (tid === null) return { matched: false, note: (sl.unmatched || {})[k] || "" };
      const tv = T24[tid] || {}; const others = Object.keys(cw).filter((j) => cw[j] === tid && j !== k && ISS[j]).map((j) => ISS[j][0]);
      return { matched: true, topic: tv.label || "", votes: n(tv.votes).toLocaleString("en-GB"), share: share(tv.votes, b24.total) + "%", shared: others.length ? "Shared with " + others.join(", ") + "." : "No other Amplify domain shares this topic." }; };
    const ic = card(s.issue) || { matched: false, note: "" };
    Object.assign(out, {
      slHas: !!sl.ballots, slLede: sl.lede || "", slRule: sl.rule || "", slChecked: sl.checked || "",
      slViews: tabsOf(SVIEWS, sv, "slView", "sl-tab-", 175), slTabId: "sl-tab-" + sv,
      slWheel: sv === "wheel", slRank: sv === "rank", slFeel: sv === "feel", slAct: sv === "act", slTime: sv === "time", slTable: sv === "table",
      slDonut: wheel, slTotal: n(b24.total).toLocaleString("en-GB"), slTurnout: (b24.turnout_pct || share(b24.total, b24.population)) + "%", slNote24: b24.note || "", slNote22: b22.note || "",
      slSelT: st.label || "", slSelV: n(st.votes).toLocaleString("en-GB"), slSelP: share(st.votes, b24.total) + "%", slSelDomains: stDomains, slSelHas: stDomains.length > 0,
      slSelOrphan: (sl.orphans || {})[selT] || "", slSelIsOrphan: !!(sl.orphans || {})[selT],
      slRankRows: rank, slWorry: worryRows, slWorryBase: W.base || "", slTop: arr(W.top).map((x) => ({ t: x.t, v: x.pct + "%" })),
      slActBars: actBars, slActStack: actStack, slActBase: Ac.base || "", slTimeCols: tcols, slTimeNote: TO.note || "",
      slTableRows: arr(b24.topics).map((x) => ({ t: x.label, v24: n(x.votes).toLocaleString("en-GB"), p24: share(x.votes, b24.total) + "%", v22: T22[x.id] ? n(T22[x.id].votes).toLocaleString("en-GB") : "", p22: T22[x.id] ? share(T22[x.id].votes, b22.total) + "%" : "", d: domainsOf(x.id).map((d) => d.label).join(", ") || "None yet" })),
      slAgainst: arr(sl.against).map((t) => ({ t })), slCites: cite(["mym24", "mym22", "mic25", "dofe24"], SLS),
      icMatched: ic.matched, icTopic: ic.topic || "", icVotes: ic.votes || "", icShare: ic.share || "", icShared: ic.shared || "", icUnmatched: !ic.matched && !!ic.note, icNote: ic.note || "",
      icSeeAll: () => { const el = document.getElementById("amp-salience"); if (el && el.scrollIntoView) el.scrollIntoView({ block: "start" }); }
    });

    /* ---- Young people in numbers ---- */
    const nm = A.nm || {}, NMS = srcMap(nm), ntabs = arr(nm.tabs), ntab = ntabs.some((t) => t.id === s.nmTab) ? s.nmTab : ((ntabs[0] || {}).id || "who");
    const asTables = !!s.nmTables;
    const figs = arr(nm.figures).filter((f) => f.tab === ntab).map((f, i) => { const c = this.ampChart(f, NMS);
      return Object.assign(c, { key: ntab + i, h: f.h, where: f.where || "", says: f.says || "", care: f.care || "", derived: !!f.derived, dStyle: pill(300),
        cites: cite(arr(f.src).concat(arr(f.src2)), NMS), showChart: !asTables || !c.hasTable, showTable: asTables && c.hasTable,
        links: arr(f.links).filter((id) => L[id]).map((id) => ({ label: L[id], go: go(id) })), hasLinks: arr(f.links).length > 0 }); });
    Object.assign(out, {
      sNumbers: s.screen === "numbers", icNumbers: this.ampIcon("chart-column", "oklch(var(--t3) 0.16 25)", 16),
      nmLede: nm.lede || "", nmRule: nm.rule || "", nmChecked: nm.checked || "",
      nmKpis: arr(nm.kpis).map((k) => ({ v: k.v, t: k.t, where: k.where, cites: cite(k.src, NMS) })),
      nmTabs: tabsOf(ntabs, ntab, "nmTab", "nm-tab-", 25), nmTabId: "nm-tab-" + ntab, nmFigs: figs,
      nmTables: asTables ? "true" : "false", nmTablesLabel: asTables ? "Show charts" : "Show every chart as a table", toggleNmTables: () => this.setState({ nmTables: !asTables }),
      nmAgainst: arr(nm.against).map((t) => ({ t })),
      nmSources: arr(nm.sources).map((x) => ({ label: x.label, url: x.url, prov: x.provenance === "V" ? "Official" : "Secondary", pStyle: pill(x.provenance === "V" ? 145 : 70), checked: x.checked })),
      nmSrcN: String(arr(nm.sources).length), nmSrcV: String(arr(nm.sources).filter((x) => x.provenance === "V").length)
    });

    /* ---- Academy ---- */
    const ac = A.ac || {}, ACS = srcMap(ac), done = arr(s.acadDone), open = s.acOpen || "", ans = s.acAns || {};
    const mods = arr(ac.modules).map((m) => { const isDone = done.indexOf(m.id) >= 0, isOpen = open === m.id, opened = arr(s.acSeen).indexOf(m.id) >= 0;
      const status = isDone ? "Done" : (opened ? "Started" : "Not started");
      return { id: m.id, n: m.n, t: m.t, d: m.d, status, isOpen: isOpen ? "true" : "false", pid: "amp-lesson",
        icon: this.ampIcon(m.icon || "graduation-cap", "oklch(var(--t3) 0.16 " + m.hue + ")", 18), sStyle: pill(isDone ? 145 : (opened ? 70 : 250)),
        bar: "height:100%;width:" + (isDone ? 100 : (opened ? 50 : 0)) + "%;background:oklch(var(--t2) 0.16 " + m.hue + ");",
        style: "display:flex;flex-direction:column;gap:10px;text-align:left;cursor:pointer;width:100%;color:rgb(var(--ink-rgb));border-radius:20px;padding:18px 20px;border:" + (isOpen ? "2px solid oklch(var(--t2) 0.16 " + m.hue + ")" : "1px solid oklch(var(--t1) 0.16 " + m.hue + " / 0.32)") + ";background:linear-gradient(170deg, oklch(var(--t1) 0.16 " + m.hue + " / 0.10), rgb(var(--film-rgb) / 0.02));",
        go: () => this.setState({ acOpen: isOpen ? "" : m.id, acSeen: arr(s.acSeen).indexOf(m.id) >= 0 ? s.acSeen : arr(s.acSeen).concat([m.id]) }, () => { if (!isOpen) { const el = document.getElementById("amp-lesson"); if (el && el.focus) el.focus(); } }) }; });
    const om = arr(ac.modules).find((m) => m.id === open);
    const q = (om || {}).q || {}, given = om ? ans[om.id] : undefined, right = given === q.a;
    Object.assign(out, {
      acLede: ac.lede || "", acRule: ac.rule || "", acMods: mods, acDoneN: String(arr(ac.modules).filter((m) => done.indexOf(m.id) >= 0).length), acTotal: String(arr(ac.modules).length),
      acHasOpen: !!om, acT: (om || {}).t || "", acN: (om || {}).n || "",
      acSteps: arr((om || {}).steps).map((x, i) => ({ k: String(i + 1), t: x.t, d: x.d, editorial: !!x.editorial, edStyle: pill(300), cites: cite(x.src, ACS), hasCites: arr(x.src).length > 0,
        hasScreen: !!(x.screen && L[x.screen]), screenLabel: L[x.screen] || "", go: go(x.screen) })),
      acQ: q.t || "", acOpts: arr(q.opts).map((o, i) => ({ o, pressed: given === i ? "true" : "false",
        style: "min-height:44px;text-align:left;padding:10px 14px;border-radius:12px;cursor:pointer;font-size:14px;font-weight:700;color:rgb(var(--ink-rgb));border:1px solid " + (given === i ? (i === q.a ? "oklch(var(--t2) 0.16 145);background:oklch(var(--t1) 0.16 145 / 0.25);" : "oklch(var(--t2) 0.16 25);background:oklch(var(--t1) 0.16 25 / 0.2);") : "rgb(var(--film-rgb) / 0.2);background:rgb(var(--film-rgb) / 0.04);"),
        go: () => { const a2 = Object.assign({}, ans); a2[om.id] = i; const d2 = i === q.a && done.indexOf(om.id) < 0 ? done.concat([om.id]) : done; this.setState({ acAns: a2, acadDone: d2 }); } })),
      acAnswered: given !== undefined, acFeedback: given === undefined ? "" : (right ? "Right. " : "Not quite. ") + (q.why || ""),
      acClose: () => this.setState({ acOpen: "" }),
      acReset: () => this.setState({ acadDone: [], acAns: {}, acSeen: [], acOpen: "", announce: "Academy progress cleared from this device." })
    });

    /* ---- Easy Read ---- */
    const er = A.er || {}, erLines = arr(((er.screens || {})[s.screen]) || []);
    Object.assign(out, { tEasy: () => this.setState({ easy: !s.easy }), erPressed: s.easy ? "true" : "false", erBg: this.onBg(!!s.easy), erLabel: s.easy ? "On: summaries at the top" : "Off",
      erShow: !!s.easy && !s.splash && erLines.length > 0, erRule: er.rule || "", erTitle: (L[s.screen] || "This screen") + " in Easy Read",
      erLines: erLines.map(([ic, t]) => ({ t, icon: this.ampIcon(ic, "oklch(var(--t3) 0.16 215)", 30) })),
      erOff: () => this.setState({ easy: false }) });

    /* ---- drill-downs to issue domains ---- */
    const di = (k) => go("issues", { issue: k });
    Object.assign(out, { drDemo: di("demo"), drTransport: di("transport"), drWork: di("work"), drPeriod: di("period"), drPolit: di("polit") });
    return out;
  }
'''

CSS13 = '''
  .amp-chart-legend button:focus-visible, .amp-drill:focus-visible, .amp-acmod:focus-visible { outline: 3px solid oklch(var(--t2) 0.16 215); outline-offset: 2px; }
  .amp-drill { transition: transform 0.15s ease, box-shadow 0.15s ease; }
  @media (prefers-reduced-motion: no-preference) { .amp-drill:hover { transform: translateY(-2px); box-shadow: 0 6px 18px rgb(0 0 0 / 0.18); } .amp-kpi { animation: ampPaIn 0.4s ease-out both; } }
  .amp-tilemap { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 6px; }
  .amp-cols { display: flex; align-items: flex-end; gap: 8px; height: 150px; }
  .amp-waffle { display: grid; grid-template-columns: repeat(10, 1fr); gap: 3px; max-width: 220px; }
  .amp-ctable { width: 100%; border-collapse: collapse; font-size: 13px; }
  .amp-ctable th, .amp-ctable td { text-align: left; padding: 5px 8px; border-bottom: 1px solid rgb(var(--film-rgb) / 0.15); vertical-align: top; }
  .amp-ctable td.n { text-align: right; font-variant-numeric: tabular-nums; }
  @media (max-width: 520px) { .amp-tilemap { gap: 4px; } .amp-tilemap > div { min-height: 56px; padding: 5px !important; } .amp-tilemap span { font-size: 10px !important; } }
'''


def chart(v):
    """Markup for one chart object v (from ampChart): a visual plus a data table for screen readers."""
    return f'''<div role="{{{{ {v}.role }}}}" aria-label="{{{{ {v}.alt }}}}">
              <sc-if value="{{{{ {v}.isDonut }}}}" hint-placeholder-val="{{{{ false }}}}"><div style="display: flex; flex-wrap: wrap; align-items: center; gap: 14px 22px;"><div style="position: relative; flex: 0 0 auto; width: min(100%, 200px);"><div style="{{{{ {v}.ring }}}}"></div><div aria-hidden="true" style="position: absolute; inset: 0; display: grid; place-items: center; font-size: 15px; font-weight: 900;">{{{{ {v}.center }}}}</div></div>
                <ul aria-hidden="true" style="list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 4px; flex: 1 1 200px; min-width: 0; font-size: 13px;"><sc-for list="{{{{ {v}.legend }}}}" as="l" hint-placeholder-count="5"><li style="display: flex; align-items: center; gap: 8px;"><span style="{{{{ l.sw }}}}"></span><span style="flex: 1 1 auto;">{{{{ l.t }}}}</span><span style="font-weight: 800; font-variant-numeric: tabular-nums;">{{{{ l.pct }}}}</span></li></sc-for></ul></div></sc-if>
              <sc-if value="{{{{ {v}.isBars }}}}" hint-placeholder-val="{{{{ false }}}}"><ul aria-hidden="true" style="list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 9px;"><sc-for list="{{{{ {v}.rows }}}}" as="r" hint-placeholder-count="5"><li><div style="display: flex; justify-content: space-between; gap: 10px; font-size: 13px; margin-bottom: 3px;"><span>{{{{ r.t }}}}</span><span style="font-weight: 800; font-variant-numeric: tabular-nums;">{{{{ r.val }}}}</span></div><div style="background: rgb(var(--film-rgb) / 0.1); border-radius: 999px;"><span style="{{{{ r.bar }}}}"></span></div></li></sc-for></ul></sc-if>
              <sc-if value="{{{{ {v}.isColumns }}}}" hint-placeholder-val="{{{{ false }}}}"><div aria-hidden="true" class="amp-cols"><sc-for list="{{{{ {v}.cols }}}}" as="k" hint-placeholder-count="3"><div style="flex: 1 1 0; min-width: 0; height: 100%; display: flex; flex-direction: column; justify-content: flex-end; align-items: center; gap: 4px;"><span style="font-size: 12px; font-weight: 800;">{{{{ k.val }}}}</span><span style="{{{{ k.bar }}}}"></span><span style="font-size: 11.5px; text-align: center;">{{{{ k.t }}}}</span></div></sc-for></div></sc-if>
              <sc-if value="{{{{ {v}.isDumbbell }}}}" hint-placeholder-val="{{{{ false }}}}"><div aria-hidden="true" style="display: flex; flex-direction: column; gap: 14px;"><sc-for list="{{{{ {v}.rows }}}}" as="r" hint-placeholder-count="1"><div><div style="font-size: 13px; margin-bottom: 6px;">{{{{ r.t }}}}</div><div style="position: relative; height: 20px; margin: 0 8px; border-radius: 999px; background: rgb(var(--film-rgb) / 0.08);"><span style="{{{{ r.line }}}}"></span><span style="{{{{ r.aDot }}}}"></span><span style="{{{{ r.bDot }}}}"></span></div><div style="display: flex; flex-wrap: wrap; gap: 4px 16px; font-size: 12.5px; margin-top: 6px;"><span><span style="{{{{ r.aSw }}}}"></span> {{{{ r.aT }}}} <b>{{{{ r.aV }}}}</b></span><span><span style="{{{{ r.bSw }}}}"></span> {{{{ r.bT }}}} <b>{{{{ r.bV }}}}</b></span></div></div></sc-for></div></sc-if>
              <sc-if value="{{{{ {v}.isWaffle }}}}" hint-placeholder-val="{{{{ false }}}}"><div style="display: flex; flex-wrap: wrap; align-items: center; gap: 14px 22px;"><div aria-hidden="true" class="amp-waffle"><sc-for list="{{{{ {v}.cells }}}}" as="w" hint-placeholder-count="100"><span style="{{{{ w.s }}}}"></span></sc-for></div><div aria-hidden="true" style="font-size: 34px; font-weight: 900; letter-spacing: -0.03em;">{{{{ {v}.big }}}}<div style="font-size: 12.5px; font-weight: 600;">filled squares out of 100</div></div></div></sc-if>
              <sc-if value="{{{{ {v}.isStack }}}}" hint-placeholder-val="{{{{ false }}}}"><div aria-hidden="true"><div style="display: flex; height: 22px; border-radius: 999px; overflow: hidden; background: rgb(var(--film-rgb) / 0.1);"><sc-for list="{{{{ {v}.legend }}}}" as="l" hint-placeholder-count="3"><span style="{{{{ l.seg }}}}"></span></sc-for></div><ul style="list-style: none; margin: 8px 0 0; padding: 0; display: flex; flex-wrap: wrap; gap: 4px 16px; font-size: 13px;"><sc-for list="{{{{ {v}.legend }}}}" as="l" hint-placeholder-count="3"><li style="display: flex; align-items: center; gap: 6px;"><span style="{{{{ l.sw }}}}"></span>{{{{ l.t }}}} <b>{{{{ l.val }}}}</b></li></sc-for></ul></div></sc-if>
              <sc-if value="{{{{ {v}.isTiles }}}}" hint-placeholder-val="{{{{ false }}}}"><div aria-hidden="true"><div class="amp-tilemap"><sc-for list="{{{{ {v}.tiles }}}}" as="x" hint-placeholder-count="12"><div style="{{{{ x.s }}}}"><span style="font-size: 11px; line-height: 1.2;">{{{{ x.t }}}}</span><span style="font-size: 15px; font-weight: 900;">{{{{ x.val }}}}</span></div></sc-for></div><div style="display: flex; flex-wrap: wrap; align-items: center; gap: 6px 12px; font-size: 12px; margin-top: 8px;"><span>Lighter {{{{ {v}.lo }}}}</span><span style="display: inline-block; width: 90px; height: 10px; border-radius: 999px; background: linear-gradient(90deg, oklch(var(--t2) 0.16 25 / 0.08), oklch(var(--t2) 0.16 25 / 0.7));"></span><span>Darker {{{{ {v}.hi }}}}</span><sc-if value="{{{{ {v}.hasRef }}}}" hint-placeholder-val="{{{{ false }}}}"><span style="font-weight: 800;">{{{{ {v}.refT }}}}</span></sc-if></div></div></sc-if>
              <sc-if value="{{{{ {v}.isKpi }}}}" hint-placeholder-val="{{{{ false }}}}"><div aria-hidden="true" class="amp-kpi" style="font-size: 38px; font-weight: 900; letter-spacing: -0.035em; color: oklch(var(--t3) 0.16 25);">{{{{ {v}.big }}}}</div></sc-if>
              <sc-if value="{{{{ {v}.isList }}}}" hint-placeholder-val="{{{{ false }}}}"><ul style="margin: 0; padding-left: 18px; display: flex; flex-direction: column; gap: 8px; font-size: 13.5px; line-height: 1.55;"><sc-for list="{{{{ {v}.items }}}}" as="x" hint-placeholder-count="3"><li>{{{{ x.t }}}} <sc-for list="{{{{ x.cites }}}}" as="c" hint-placeholder-count="1"><a href="{{{{ c.url }}}}" target="_blank" rel="noopener" style="@A@ font-size: 12px;">{{{{ c.prov }}}} source</a></sc-for></li></sc-for></ul></sc-if>
            </div>'''


def ctable(v, caption):
    return (f'<table class="amp-ctable"><caption class="amp-sr">{caption}</caption><thead><tr><th scope="col">Measure</th><th scope="col" style="text-align: right;">Value</th></tr></thead>'
            f'<tbody><sc-for list="{{{{ {v}.table }}}}" as="r" hint-placeholder-count="5"><tr><th scope="row" style="font-weight: 600;">{{{{ r.k }}}}</th><td class="n">{{{{ r.v }}}}</td></tr></sc-for></tbody></table>')


def srtable(v, caption):
    return f'<sc-if value="{{{{ {v}.hasTable }}}}" hint-placeholder-val="{{{{ false }}}}"><div class="amp-sr">' + ctable(v, caption) + '</div></sc-if>'


def fill(s):
    for k, v in (("@PANEL@", PANEL), ("@H2@", H2), ("@CARD@", CARD), ("@SMALL@", SMALL), ("@LABEL@", LABEL), ("@SEL@", SEL), ("@BTN@", BTN),
                 ("@A@", A), ("@EYEBROW@", EYEBROW), ("@H1@", H1), ("@LEDE@", LEDE)):
        s = s.replace(k, v)
    return s


def tablist(var, label, panel):
    return (f'<div role="tablist" aria-label="{label}" style="display: flex; flex-wrap: wrap; gap: 8px;"><sc-for list="{{{{ {var} }}}}" as="t" hint-placeholder-count="6">'
            f'<button type="button" role="tab" id="{{{{ t.tid }}}}" aria-controls="{panel}" aria-selected="{{{{ t.sel }}}}" tabindex="{{{{ t.tab }}}}" onClick="{{{{ t.go }}}}" onKeyDown="{{{{ t.key }}}}" style="{{{{ t.style }}}}"><span aria-hidden="true" style="{{{{ t.icon }}}}"></span>{{{{ t.label }}}}</button></sc-for></div>')


SALIENCE = '''
          <section id="amp-salience" aria-labelledby="amp-sl-h" style="@PANEL@ display: flex; flex-direction: column; gap: 12px;">
            <div><div style="@LABEL@">How much it matters to young people</div><h2 id="amp-sl-h" style="@H2@">What young people voted for, worry about and actually do</h2>
              <p style="margin: 0; font-size: 14px; line-height: 1.6; max-width: 72ch;">{{ slLede }}</p></div>
            ''' + tablist("slViews", "Ways to see how much each issue matters", "sl-panel") + '''
            <div role="tabpanel" id="sl-panel" aria-labelledby="{{ slTabId }}" class="amp-cv-panel" style="display: flex; flex-direction: column; gap: 12px;">
              <sc-if value="{{ slWheel }}" hint-placeholder-val="{{ true }}">
                <p style="margin: 0; @SMALL@">{{ slTotal }} young people aged 11 to 18 voted in Make Your Mark 2024: {{ slTurnout }} of those eligible. Choose a topic to see the Amplify domains it covers.</p>
                <div style="display: flex; flex-wrap: wrap; gap: 16px 24px; align-items: flex-start;">
                  <div style="flex: 0 0 auto; width: min(100%, 220px);" role="img" aria-label="{{ slDonut.alt }}"><div style="position: relative;"><div style="{{ slDonut.ring }}"></div><div aria-hidden="true" style="position: absolute; inset: 0; display: grid; place-items: center; text-align: center; font-size: 13px; font-weight: 900;"><span style="display: block; text-align: center;">{{ slDonut.center }}<span style="display: block; font-size: 11.5px; font-weight: 700;">votes</span></span></div></div></div>
                  <ul class="amp-chart-legend" style="list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 2px; flex: 1 1 260px; min-width: 0;"><sc-for list="{{ slDonut.legend }}" as="l" hint-placeholder-count="10"><li><button type="button" aria-pressed="{{ l.sel }}" onClick="{{ l.go }}" style="{{ l.style }}"><span aria-hidden="true" style="{{ l.sw }}"></span><span style="flex: 1 1 auto;">{{ l.t }}</span><span style="font-weight: 800; font-variant-numeric: tabular-nums;">{{ l.pct }}</span></button></li></sc-for></ul>
                  <div aria-live="polite" style="@CARD@ flex: 1 1 240px; min-width: 0;"><div style="@LABEL@">Selected topic</div><div style="font-size: 16px; font-weight: 900;">{{ slSelT }}</div><div style="font-size: 13.5px;">{{ slSelV }} votes, {{ slSelP }} of all votes</div>
                    <sc-if value="{{ slSelHas }}" hint-placeholder-val="{{ true }}"><div style="font-size: 13px; margin-top: 4px;">Amplify domains in this topic:</div><div style="display: flex; flex-wrap: wrap; gap: 6px;"><sc-for list="{{ slSelDomains }}" as="d" hint-placeholder-count="3"><button type="button" class="amp-drill" onClick="{{ d.go }}" style="@BTN@">{{ d.label }}</button></sc-for></div></sc-if>
                    <sc-if value="{{ slSelIsOrphan }}" hint-placeholder-val="{{ false }}"><p style="margin: 4px 0 0; font-size: 13px;">{{ slSelOrphan }}</p></sc-if></div>
                </div>
                <p style="margin: 0; @SMALL@">{{ slNote24 }}</p>
              </sc-if>
              <sc-if value="{{ slRank }}" hint-placeholder-val="{{ false }}">
                <p style="margin: 0; @SMALL@">Bar: share of 2024 votes (scale to 20%). Dark mark: the same topic's share in 2022, where it was on the ballot. {{ slNote22 }}</p>
                <ul style="list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 10px;"><sc-for list="{{ slRankRows }}" as="r" hint-placeholder-count="10"><li><div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 2px 10px; font-size: 13.5px; margin-bottom: 4px;"><span style="font-weight: 700;">{{ r.t }}</span><span><b>{{ r.val }}</b> <span style="@SMALL@">{{ r.votes }} votes · {{ r.was }}</span></span></div><div aria-hidden="true" style="position: relative; background: rgb(var(--film-rgb) / 0.1); border-radius: 999px;"><span style="{{ r.bar }}"></span><span style="{{ r.tick }}"></span></div></li></sc-for></ul>
              </sc-if>
              <sc-if value="{{ slFeel }}" hint-placeholder-val="{{ false }}">
                <p style="margin: 0; @SMALL@">Red: share of 16 and 17 year olds who say they worry about it. Green: share of all 2024 ballot votes for the matching topic. Both use the same 0 to 100 scale. Worry is widely shared, while a ballot vote picks one topic out of ten, so ballot shares are always much smaller. {{ slWorryBase }}</p>
                <ul style="list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 12px;"><sc-for list="{{ slWorry }}" as="w" hint-placeholder-count="5"><li style="@CARD@"><div style="font-size: 14px; font-weight: 800;">{{ w.t }} <span style="@SMALL@">ballot topic: {{ w.topic }}, ranked {{ w.rank }}</span></div>
                  <div style="display: grid; grid-template-columns: 110px 1fr 48px; gap: 6px 8px; align-items: center; font-size: 12.5px;"><span>Worry about it</span><div aria-hidden="true" style="background: rgb(var(--film-rgb) / 0.1); border-radius: 999px;"><span style="{{ w.wBar }}"></span></div><b>{{ w.w }}</b><span>Ballot votes</span><div aria-hidden="true" style="background: rgb(var(--film-rgb) / 0.1); border-radius: 999px;"><span style="{{ w.vBar }}"></span></div><b>{{ w.v }}</b></div>
                  <sc-if value="{{ w.hasNote }}" hint-placeholder-val="{{ false }}"><p style="margin: 0; @SMALL@">{{ w.note }}</p></sc-if></li></sc-for></ul>
                <div style="@CARD@"><div style="@LABEL@">Most important issue facing the country, 16 and 17 year olds</div><ul style="margin: 0; padding-left: 18px; font-size: 13.5px;"><sc-for list="{{ slTop }}" as="x" hint-placeholder-count="5"><li>{{ x.t }}: <b>{{ x.v }}</b></li></sc-for></ul></div>
              </sc-if>
              <sc-if value="{{ slAct }}" hint-placeholder-val="{{ false }}">
                <p style="margin: 0; @SMALL@">How many have acted, not just cared. {{ slActBase }}</p>
                ''' + chart("slActBars") + srtable("slActBars", "What young people had done") + '''
                <div style="@LABEL@">How many of the six things each person had done</div>
                ''' + chart("slActStack") + srtable("slActStack", "Level of activity") + '''
              </sc-if>
              <sc-if value="{{ slTime }}" hint-placeholder-val="{{ false }}">
                <p style="margin: 0; @SMALL@">Votes cast in each Make Your Mark ballot, with turnout under each year. {{ slTimeNote }}</p>
                <div role="img" aria-label="{{ slTimeCols.alt }}"><div aria-hidden="true" class="amp-cols" style="height: 180px;"><sc-for list="{{ slTimeCols.cols }}" as="k" hint-placeholder-count="8"><div style="flex: 1 1 0; min-width: 0; height: 100%; display: flex; flex-direction: column; justify-content: flex-end; align-items: center; gap: 3px;"><span style="font-size: 10.5px; font-weight: 800;">{{ k.val }}</span><span style="{{ k.bar }}"></span><span style="font-size: 11.5px; font-weight: 700;">{{ k.t }}</span><span style="font-size: 10.5px;">{{ k.pct }}</span></div></sc-for></div></div>
                ''' + srtable("slTimeCols", "Make Your Mark votes by year") + '''
              </sc-if>
              <sc-if value="{{ slTable }}" hint-placeholder-val="{{ false }}">
                <div style="overflow-x: auto;"><table class="amp-ctable"><caption class="amp-sr">Make Your Mark votes by topic, 2024 and 2022</caption><thead><tr><th scope="col">Topic (2024)</th><th scope="col" style="text-align: right;">2024 votes</th><th scope="col" style="text-align: right;">Share</th><th scope="col" style="text-align: right;">2022 votes</th><th scope="col" style="text-align: right;">2022 share</th><th scope="col">Amplify domains</th></tr></thead>
                  <tbody><sc-for list="{{ slTableRows }}" as="r" hint-placeholder-count="10"><tr><th scope="row" style="font-weight: 600;">{{ r.t }}</th><td class="n">{{ r.v24 }}</td><td class="n">{{ r.p24 }}</td><td class="n">{{ r.v22 }}</td><td class="n">{{ r.p22 }}</td><td>{{ r.d }}</td></tr></sc-for></tbody></table></div>
              </sc-if>
            </div>
            <details style="@CARD@"><summary style="cursor: pointer; font-weight: 800; font-size: 14px;">Before you rely on these numbers</summary><ul style="margin: 8px 0 0; padding-left: 18px; font-size: 13.5px; line-height: 1.55; display: flex; flex-direction: column; gap: 4px;"><sc-for list="{{ slAgainst }}" as="x" hint-placeholder-count="3"><li>{{ x.t }}</li></sc-for></ul><p style="margin: 8px 0 0; @SMALL@">{{ slRule }} Last checked {{ slChecked }}.</p></details>
            <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 4px 8px; @SMALL@"><span style="font-weight: 800;">Sources</span><sc-for list="{{ slCites }}" as="c" hint-placeholder-count="4"><a href="{{ c.url }}" target="_blank" rel="noopener" style="@A@ font-weight: 600;">{{ c.label }}</a><span style="{{ c.pStyle }}">{{ c.prov }}</span></sc-for></div>
          </section>
'''

ISSUE_BALLOT = '''<div style="margin-top: 16px; border: 1px solid rgb(var(--film-rgb) / 0.11); border-radius: 16px; background: rgb(var(--film-rgb) / 0.04); padding: 14px 18px; display: flex; flex-wrap: wrap; gap: 6px 16px; align-items: center;">
              <div style="@LABEL@ flex: 1 1 100%;">In the Make Your Mark 2024 ballot</div>
              <sc-if value="{{ icMatched }}" hint-placeholder-val="{{ true }}"><span style="font-size: 14.5px; font-weight: 800;">{{ icTopic }}</span><span style="font-size: 13.5px;">{{ icVotes }} votes, {{ icShare }} of all votes.</span><span style="@SMALL@">{{ icShared }}</span></sc-if>
              <sc-if value="{{ icUnmatched }}" hint-placeholder-val="{{ false }}"><span style="font-size: 13.5px;">{{ icNote }}</span></sc-if>
              <button type="button" onClick="{{ icSeeAll }}" style="@BTN@">Compare all topics</button>
            </div>
            '''

FIG = '''<article style="@CARD@ gap: 10px;"><div style="display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 10px;"><h3 style="margin: 0; font-size: 15.5px; font-weight: 900;">{{ f.h }}</h3><span style="@SMALL@">{{ f.where }}</span><sc-if value="{{ f.derived }}" hint-placeholder-val="{{ false }}"><span style="{{ f.dStyle }}">Worked out here</span></sc-if></div>
              <sc-if value="{{ f.showChart }}" hint-placeholder-val="{{ true }}">''' + chart("f") + srtable("f", "{{ f.h }}") + '''</sc-if>
              <sc-if value="{{ f.showTable }}" hint-placeholder-val="{{ false }}">''' + ctable("f", "{{ f.h }}") + '''</sc-if>
              <p style="margin: 0; font-size: 13.5px; line-height: 1.55;"><b>What this shows.</b> {{ f.says }}</p>
              <p style="margin: 0; font-size: 13px; line-height: 1.55; color: rgb(var(--ink-rgb) / 0.86);"><b>Read with care.</b> {{ f.care }}</p>
              <sc-if value="{{ f.hasLinks }}" hint-placeholder-val="{{ false }}"><div style="display: flex; flex-wrap: wrap; gap: 6px;"><sc-for list="{{ f.links }}" as="x" hint-placeholder-count="3"><button type="button" class="amp-drill" onClick="{{ x.go }}" style="@BTN@">Open {{ x.label }}</button></sc-for></div></sc-if>
              <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 4px 8px; @SMALL@"><span style="font-weight: 800;">Source</span><sc-for list="{{ f.cites }}" as="c" hint-placeholder-count="1"><a href="{{ c.url }}" target="_blank" rel="noopener" style="@A@ font-weight: 600;">{{ c.label }}</a><span style="{{ c.pStyle }}">{{ c.prov }}</span></sc-for></div>
            </article>'''

NUMBERS = '''
        <sc-if value="{{ sNumbers }}" hint-placeholder-val="{{ false }}">
        <div class="amp-screen" style="display: flex; flex-direction: column; gap: 16px;">
          <div>
            <div style="@EYEBROW@ color: oklch(var(--t3) 0.16 25);"><span aria-hidden="true" style="{{ icNumbers }}"></span>Foundations</div>
            <h1 style="@H1@">Young people in numbers</h1>
            <p style="@LEDE@">{{ nmLede }}</p>
            <p style="margin: 8px 0 0; @SMALL@">{{ nmRule }} <span style="font-weight: 800;">Official</span> means a government, Parliament, regulator or council source; <span style="font-weight: 800;">Secondary</span> a reputable secondary source. Last checked {{ nmChecked }}.</p>
          </div>
          <ul style="list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 210px), 1fr)); gap: 10px;"><sc-for list="{{ nmKpis }}" as="k" hint-placeholder-count="4"><li style="@CARD@"><span class="amp-kpi" style="font-size: 28px; font-weight: 900; letter-spacing: -0.03em; color: oklch(var(--t3) 0.16 25);">{{ k.v }}</span><span style="font-size: 13.5px; line-height: 1.45;">{{ k.t }}</span><span style="@SMALL@">{{ k.where }} · <sc-for list="{{ k.cites }}" as="c" hint-placeholder-count="1"><a href="{{ c.url }}" target="_blank" rel="noopener" style="@A@">{{ c.prov }} source</a></sc-for></span></li></sc-for></ul>
          <div style="display: flex; flex-wrap: wrap; gap: 10px; align-items: center; justify-content: space-between;">
            ''' + tablist("nmTabs", "Young people in numbers", "nm-panel") + '''
            <button type="button" aria-pressed="{{ nmTables }}" onClick="{{ toggleNmTables }}" style="@BTN@">{{ nmTablesLabel }}</button>
          </div>
          <div role="tabpanel" id="nm-panel" aria-labelledby="{{ nmTabId }}" class="amp-cv-panel" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 340px), 1fr)); gap: 12px;">
            <sc-for list="{{ nmFigs }}" as="f" hint-placeholder-count="4">''' + FIG + '''</sc-for>
          </div>
          <section style="@PANEL@"><h2 style="@H2@">Before you rely on these numbers</h2><ul style="margin: 0; padding-left: 18px; display: flex; flex-direction: column; gap: 6px; font-size: 13.5px; line-height: 1.55;"><sc-for list="{{ nmAgainst }}" as="x" hint-placeholder-count="3"><li>{{ x.t }}</li></sc-for></ul></section>
          <section style="@PANEL@"><h2 style="@H2@">Sources for this screen</h2><p style="margin: 0 0 10px; @SMALL@">{{ nmSrcN }} sources, {{ nmSrcV }} of them official.</p>
            <ul style="margin: 0; padding-left: 18px; display: flex; flex-direction: column; gap: 4px; font-size: 13px; line-height: 1.5;"><sc-for list="{{ nmSources }}" as="x" hint-placeholder-count="6"><li><a href="{{ x.url }}" target="_blank" rel="noopener" style="@A@ font-weight: 600;">{{ x.label }}</a> <span style="{{ x.pStyle }}">{{ x.prov }}</span> <span style="@SMALL@">checked {{ x.checked }}</span></li></sc-for></ul></section>
        </div>
        </sc-if>
'''

ACADEMY = '''<div style="display: flex; flex-wrap: wrap; align-items: center; gap: 8px 14px;"><span style="font-size: 14px; font-weight: 800;">{{ acDoneN }} of {{ acTotal }} lessons done on this device</span><button type="button" onClick="{{ acReset }}" style="@BTN@">Clear my progress</button></div>
          <ul style="list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr)); gap: 14px;">
            <sc-for list="{{ acMods }}" as="m" hint-placeholder-count="4"><li style="display: flex;"><button type="button" class="amp-acmod amp-drill" aria-expanded="{{ m.isOpen }}" aria-controls="{{ m.pid }}" onClick="{{ m.go }}" style="{{ m.style }}">
              <span style="display: flex; justify-content: space-between; align-items: center; gap: 8px;"><span style="display: inline-flex; align-items: center; gap: 8px; @LABEL@"><span aria-hidden="true" style="{{ m.icon }}"></span>Lesson {{ m.n }}</span><span style="{{ m.sStyle }}">{{ m.status }}</span></span>
              <span style="font-size: 17px; font-weight: 800; letter-spacing: -0.02em;">{{ m.t }}</span>
              <span style="font-size: 13.5px; line-height: 1.5; color: rgb(var(--ink-rgb) / 0.82);">{{ m.d }}</span>
              <span aria-hidden="true" style="display: block; height: 6px; border-radius: 999px; background: rgb(var(--film-rgb) / 0.1); overflow: hidden;"><span style="display: block; {{ m.bar }}"></span></span>
              <span style="font-size: 12.5px; font-weight: 800;">Open the lesson</span>
            </button></li></sc-for>
          </ul>
          <section id="amp-lesson" tabindex="-1" aria-label="Lesson" style="outline: none;">
            <sc-if value="{{ acHasOpen }}" hint-placeholder-val="{{ false }}"><div class="amp-cv-panel" style="@PANEL@ display: flex; flex-direction: column; gap: 12px;">
              <div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px;"><div><div style="@LABEL@">Lesson {{ acN }}</div><h2 style="@H2@">{{ acT }}</h2></div><button type="button" onClick="{{ acClose }}" style="@BTN@">Close the lesson</button></div>
              <ol style="list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 8px;"><sc-for list="{{ acSteps }}" as="x" hint-placeholder-count="4"><li style="@CARD@"><div style="display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 10px;"><span style="@LABEL@">Step {{ x.k }}</span><span style="font-size: 14.5px; font-weight: 900;">{{ x.t }}</span><sc-if value="{{ x.editorial }}" hint-placeholder-val="{{ false }}"><span style="{{ x.edStyle }}">Editorial</span></sc-if></div><div style="font-size: 13.5px; line-height: 1.55;">{{ x.d }}</div>
                <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 4px 10px; @SMALL@"><sc-if value="{{ x.hasCites }}" hint-placeholder-val="{{ false }}"><span style="font-weight: 800;">Source</span><sc-for list="{{ x.cites }}" as="c" hint-placeholder-count="1"><a href="{{ c.url }}" target="_blank" rel="noopener" style="@A@ font-weight: 600;">{{ c.label }}</a><span style="{{ c.pStyle }}">{{ c.prov }}</span></sc-for></sc-if><sc-if value="{{ x.hasScreen }}" hint-placeholder-val="{{ false }}"><button type="button" onClick="{{ x.go }}" style="@BTN@">Open {{ x.screenLabel }}</button></sc-if></div></li></sc-for></ol>
              <fieldset style="border: 1px solid rgb(var(--film-rgb) / 0.18); border-radius: 16px; padding: 14px 16px; margin: 0;"><legend style="font-size: 15px; font-weight: 900; padding: 0 6px;">Check: {{ acQ }}</legend>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 220px), 1fr)); gap: 8px;"><sc-for list="{{ acOpts }}" as="o" hint-placeholder-count="4"><button type="button" aria-pressed="{{ o.pressed }}" onClick="{{ o.go }}" style="{{ o.style }}">{{ o.o }}</button></sc-for></div>
                <p aria-live="polite" style="margin: 10px 0 0; font-size: 14px; line-height: 1.55;">{{ acFeedback }}</p></fieldset>
              <p style="margin: 0; @SMALL@">{{ acRule }}</p>
            </div></sc-if>
          </section>

          '''

EASY_BLOCK = '''
        <sc-if value="{{ erShow }}" hint-placeholder-val="{{ false }}">
        <section aria-labelledby="amp-er-h" lang="en" style="border-radius: 18px; padding: 14px 18px; border: 2px solid oklch(var(--t2) 0.16 215 / 0.6); background: oklch(var(--t1) 0.16 215 / 0.12);">
          <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 6px 12px;"><h2 id="amp-er-h" style="margin: 0; font-size: 18px; font-weight: 900;">{{ erTitle }}</h2><button type="button" onClick="{{ erOff }}" style="@BTN@">Turn Easy Read off</button></div>
          <ul style="list-style: none; margin: 10px 0 0; padding: 0; display: flex; flex-direction: column; gap: 10px;"><sc-for list="{{ erLines }}" as="x" hint-placeholder-count="3"><li style="display: flex; align-items: center; gap: 14px; font-size: 18px; line-height: 1.45; font-weight: 600;"><span aria-hidden="true" style="{{ x.icon }}"></span><span>{{ x.t }}</span></li></sc-for></ul>
        </section>
        </sc-if>
'''

EASY_BTN = '''    <button onClick="{{ tEasy }}" aria-pressed="{{ erPressed }}" data-tip="ui:easyread" style="text-align: left; border: 1px solid rgb(var(--film-rgb) / 0.13); border-radius: 14px; padding: 11px 13px; background: {{ erBg }}; color: rgb(var(--ink-rgb));">
      <div style="font-family: 'Space Mono', monospace; font-size: 10.5px; letter-spacing: 0.14em; text-transform: uppercase; color: rgb(var(--ink-rgb) / 0.7);">Easy Read</div>
      <div style="font-size: 14px; font-weight: 700; margin-top: 2px;">{{ erLabel }}</div>
    </button>
'''

ACAD_OLD = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 14px;">\n            <div style="border: 1px solid oklch(var(--t1) 0.16 175 / 0.28); border-radius: 20px; background: linear-gradient(170deg, oklch(var(--t1) 0.16 175 / 0.10), rgb(var(--film-rgb) / 0.02)); padding: 18px 20px; display: flex; flex-direction: column; gap: 10px;">\n              <div style="display: flex; justify-content: space-between; align-items: baseline;"><span style="font-family: \'Space Mono\', monospace; font-size: 10.5px; letter-spacing: 0.14em; text-transform: uppercase; color: oklch(var(--t3) 0.14 175);">Module 01 &middot; complete</span><span style="font-family: \'Space Mono\', monospace; font-size: 10px; color: rgb(var(--ink-rgb) / 0.7);">14 min</span></div>\n              <h2 style="margin: 0; font-size: 17px; font-weight: 700; letter-spacing: -0.02em;">How a petition actually becomes a debate</h2>\n              <p style="margin: 0; font-size: 13.5px; line-height: 1.5; color: rgb(var(--ink-rgb) / 0.7);">Thresholds, sitting days, the Petitions Committee, and what a government response is and is not.</p>\n              <div style="height: 6px; border-radius: 999px; background: rgb(var(--film-rgb) / 0.1); overflow: hidden;"><div style="height: 100%; width: 100%; background: oklch(var(--t2) 0.16 175);"></div></div>\n            </div>\n            <div style="border: 1px solid oklch(var(--t1) 0.16 175 / 0.28); border-radius: 20px; background: linear-gradient(170deg, oklch(var(--t1) 0.16 175 / 0.10), rgb(var(--film-rgb) / 0.02)); padding: 18px 20px; display: flex; flex-direction: column; gap: 10px;">\n              <div style="display: flex; justify-content: space-between; align-items: baseline;"><span style="font-family: \'Space Mono\', monospace; font-size: 10.5px; letter-spacing: 0.14em; text-transform: uppercase; color: oklch(var(--t3) 0.14 175);">Module 02 &middot; complete</span><span style="font-family: \'Space Mono\', monospace; font-size: 10px; color: rgb(var(--ink-rgb) / 0.7);">11 min</span></div>\n              <h2 style="margin: 0; font-size: 17px; font-weight: 700; letter-spacing: -0.02em;">Writing wording that moves people</h2>\n              <p style="margin: 0; font-size: 13.5px; line-height: 1.5; color: rgb(var(--ink-rgb) / 0.7);">Naming who is affected, the altruism and relevance levers, and where emotive tips into extreme.</p>\n              <div style="height: 6px; border-radius: 999px; background: rgb(var(--film-rgb) / 0.1); overflow: hidden;"><div style="height: 100%; width: 100%; background: oklch(var(--t2) 0.16 175);"></div></div>\n            </div>\n            <div style="border: 1px solid oklch(var(--t2) 0.16 70 / 0.3); border-radius: 20px; background: linear-gradient(170deg, oklch(var(--t2) 0.16 70 / 0.10), rgb(var(--film-rgb) / 0.02)); padding: 18px 20px; display: flex; flex-direction: column; gap: 10px;">\n              <div style="display: flex; justify-content: space-between; align-items: baseline;"><span style="font-family: \'Space Mono\', monospace; font-size: 10.5px; letter-spacing: 0.14em; text-transform: uppercase; color: oklch(var(--t3) 0.13 70);">Module 03 &middot; in progress</span><span style="font-family: \'Space Mono\', monospace; font-size: 10px; color: rgb(var(--ink-rgb) / 0.7);">18 min</span></div>\n              <h2 style="margin: 0; font-size: 17px; font-weight: 700; letter-spacing: -0.02em;">Building a coalition before you need one</h2>\n              <p style="margin: 0; font-size: 13.5px; line-height: 1.5; color: rgb(var(--ink-rgb) / 0.7);">Approaching unions and subject associations, what to ask for, and how to hold them to a send time.</p>\n              <div style="height: 6px; border-radius: 999px; background: rgb(var(--film-rgb) / 0.1); overflow: hidden;"><div style="height: 100%; width: 62%; background: oklch(var(--t3) 0.13 70);"></div></div>\n            </div>\n            <div style="border: 1px solid rgb(var(--film-rgb) / 0.11); border-radius: 20px; background: rgb(var(--film-rgb) / 0.035); padding: 18px 20px; display: flex; flex-direction: column; gap: 10px;">\n              <div style="display: flex; justify-content: space-between; align-items: baseline;"><span style="font-family: \'Space Mono\', monospace; font-size: 10.5px; letter-spacing: 0.14em; text-transform: uppercase; color: rgb(var(--ink-rgb) / 0.62);">Module 04 &middot; locked</span><span style="font-family: \'Space Mono\', monospace; font-size: 10px; color: rgb(var(--ink-rgb) / 0.7);">16 min</span></div>\n              <h2 style="margin: 0; font-size: 17px; font-weight: 700; letter-spacing: -0.02em;">Giving evidence and being interviewed</h2>\n              <p style="margin: 0; font-size: 13.5px; line-height: 1.5; color: rgb(var(--ink-rgb) / 0.7);">Select committee practice drawn from the Youth Select Committee&rsquo;s own sessions, plus broadcast basics.</p>\n              <div style="height: 6px; border-radius: 999px; background: rgb(var(--film-rgb) / 0.1); overflow: hidden;"><div style="height: 100%; width: 0%; background: rgb(var(--film-rgb) / 0.3);"></div></div>\n            </div>\n          </div>\n\n          '

MANI = [  # (issue key, title, status old, status new, hue)
    ("Demo", "Votes at 16 with political education", "MHCLG &middot; DfE &middot; half won", "MHCLG &middot; DfE &middot; half won", 175),
    ("Transport", "Free public transport for young people", "DfT &middot; live petition", "DfT &middot; councils set most fares", 70),
    ("Work", "Minimum wage parity for under-22s", "DBT &middot; Low Pay Commission", "DBT &middot; Low Pay Commission", 300),
    ("Period", "Period dignity in public spaces", "DHSC &middot; UKYP campaign running", "DHSC &middot; UKYP campaign running", 250),
    ("Polit", "Standardised political literacy for all", "DfE &middot; petition relaunching", "DfE &middot; petition 754954 closed at 1,192", 145),
]


def mani(key, title, old, new, hue):
    o = (f'<div style="border-radius: 16px; padding: 15px 17px; background: oklch(var(--t1) 0.16 {hue} / 0.10); border: 1px solid oklch(var(--t1) 0.16 {hue} / 0.26);"><div style="font-size: 15px; font-weight: 700;">{title}</div>'
         f'<div style="font-family: \'Space Mono\', monospace; font-size: 11px; color: oklch(var(--t3) 0.16 {hue}); margin-top: 5px;">{old}</div></div>')
    n = (f'<button type="button" class="amp-drill" onClick="{{{{ dr{key} }}}}" style="display: block; width: 100%; text-align: left; cursor: pointer; color: rgb(var(--ink-rgb)); border-radius: 16px; padding: 15px 17px; background: oklch(var(--t1) 0.16 {hue} / 0.10); border: 1px solid oklch(var(--t1) 0.16 {hue} / 0.26);">'
         f'<span style="display: block; font-size: 15px; font-weight: 700;">{title}</span><span style="display: block; font-family: \'Space Mono\', monospace; font-size: 11px; color: oklch(var(--t3) 0.16 {hue}); margin-top: 5px;">{new}</span>'
         f'<span style="display: block; font-size: 12px; font-weight: 800; margin-top: 8px;">Open the issue domain</span></button>')
    return (f"ext13-drill-{key.lower()}", f"the {title} card opens its issue domain", o, n, 1)


def transforms():
    acad_old = ACAD_OLD
    t = [
        ("ext13-load", "the salience, numbers, academy and Easy Read data load with the rest", '"./data/civic.json"].map(get));',
         '"./data/civic.json", "./data/salience.json", "./data/numbers.json", "./data/academy.json", "./data/easyread.json"].map(get));', 1),
        ("ext13-load-vars", "name them", "gl, pd, pa, cv] =", "gl, pd, pa, cv, sl, nm, ac, er] =", 1),
        ("ext13-load-state", "keep them in state", "gl, pd, pa, cv, loaded", "gl, pd, pa, cv, sl, nm, ac, er, loaded", 1),
        ("ext13-nav", "Young people in numbers sits before Issue domains in Foundations", '\n      ["issues", "Issue domains",',
         '\n      ["numbers", "Young people in numbers", "bar", 25, 7, "NEW", "numbers statistics data facts figures demographics population ethnicity language Welsh poverty free school meals SEN care NEET mental health young carers region map aspirations hopes voice opportunity gaps"],\n      ["issues", "Issue domains",', 1),
        ("ext13-hash", "the screen can be linked to", "|notify|parliament|civic)$/.test(id)", "|notify|parliament|civic|numbers)$/.test(id)", 1),
        ("ext13-icon", "its drawer icon", 'civic: "heart-handshake" };', 'civic: "heart-handshake", numbers: "chart-column" };', 1),
        ("ext13-css", "chart, tile map, waffle and drill-down styles (reduced-motion safe)", "  .amp-sr {", CSS13 + "\n  .amp-sr {", 1),
        ("ext13-logic", "chart engine, salience, numbers, academy and drill-down values", "  async loadPetition() {", LOGIC13 + "\n  async loadPetition() {", 1),
        ("ext13-vals", "its values join renderVals", "...this.ampVals11(s), ...this.ampVals12(s),", "...this.ampVals11(s), ...this.ampVals12(s), ...this.ampVals13(s),", 1),
        ("ext13-numbers", "the Young people in numbers screen", '        <div data-slot="portal-end" style="display: none;"></div>', fill(NUMBERS) + '\n        <div data-slot="portal-end" style="display: none;"></div>', 1),
        ("ext13-salience", "the How much it matters panel follows the domain card",
         "<p style=\"margin: 0; font-family: 'Space Mono', monospace; font-size: 10.5px; line-height: 1.8; color: rgb(var(--ink-rgb) / 0.8);\">Positions marked UKYP",
         fill(SALIENCE) + "\n          <p style=\"margin: 0; font-family: 'Space Mono', monospace; font-size: 10.5px; line-height: 1.8; color: rgb(var(--ink-rgb) / 0.8);\">Positions marked UKYP", 1),
        ("ext13-issue-ballot", "each domain card says which ballot topic covers it and who shares it",
         '<div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 20px; padding-top: 17px; border-top: 1px solid rgb(var(--film-rgb) / 0.11);">',
         fill(ISSUE_BALLOT) + '<div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 20px; padding-top: 17px; border-top: 1px solid rgb(var(--film-rgb) / 0.11);">', 1),
        ("ext13-issue-card-id", "the domain card can be scrolled to from the wheel",
         '<h2 style="margin: 0; font-size: 23px; font-weight: 900; letter-spacing: -0.035em;">{{ issueTitle }}</h2>',
         '<h2 id="amp-issue-card" style="margin: 0; font-size: 23px; font-weight: 900; letter-spacing: -0.035em; scroll-margin-top: 80px;">{{ issueTitle }}</h2>', 1),
        ("ext13-acad-cards", "D40: the Academy modules open real, sourced lessons with honest progress", acad_old, fill(ACADEMY), 1),
        ("ext13-acad-lede", "D40: completion does not feed the launch-readiness gate; say what is true",
         "Completion feeds the launch-readiness gate, so learning is a prerequisite rather than an extra.",
         "Open a lesson, read its steps and answer one question. Progress stays on this device and nothing is sent.", 1),
        ("ext13-acad-keywords", "D40: there are no badges to earn", "learn political literacy quiz training earn badges", "learn political literacy quiz training lessons modules petition evidence coalition wording", 1),
        ("ext13-prefs", "Easy Read and Academy progress are remembered with the other preferences, inside try/catch", '"planPledges"]', '"planPledges", "easy", "acadDone"]', 2),
        ("ext13-relaunch", "D26 class: no source says the petition will relaunch in the autumn term",
         '"Re-launch in the autumn term with subject associations and unions committed before day one"',
         '"If a new petition is started, have subject associations and unions committed before day one"', 1),
        ("ext13-relaunch-track", "D42: the Track record entry also asserted a relaunch no source supports",
         '"Re-launch in the autumn term, anchored to UK Parliament Week, with adult-ally lists committed before day one."',
         '"Any relaunch would be best anchored to UK Parliament Week, with adult-ally lists committed before day one. None has been announced."', 1),
        ("ext13-incl-easyread", "Inclusion & reach says what has shipped: Easy Read summaries now cover every screen",
         "Easy Read version of every campaign ask</span> &mdash; one idea per page with a supporting image.",
         "Easy Read version of every campaign ask</span> &mdash; one idea per page with a supporting image. Easy Read summaries of every screen shipped in 1.0.0-rc.8: switch them on in Access and language settings.", 1),
        ("ext13-stale-date", "a relative date went stale: say the date, not \"three days ago\"",
         "Report stage and third reading, three days ago.", "Report stage and third reading.", 1),
        ("ext13-hub-drill", "the votes-at-16 card on Campaign hub opens its issue domain",
         '<h2 style="margin: 0; font-size: 17px; line-height: 1.25; font-weight: 700; letter-spacing: -0.02em;">Votes at 16, with more political education throughout school</h2>',
         '<h2 style="margin: 0; font-size: 17px; line-height: 1.25; font-weight: 700; letter-spacing: -0.02em;">Votes at 16, with more political education throughout school</h2>'
         '<button type="button" class="amp-drill" onClick="{{ drDemo }}" style="align-self: flex-start; ' + BTN.replace('"', "'") + '">Open the issue domain</button>', 1),
    ]
    t += [
        ("ext13-easy-toggle", "an Easy Read switch in Access and language settings", '    <button onClick="{{ tData }}"', EASY_BTN + '    <button onClick="{{ tData }}"', 1),
        ("ext13-easy-block", "the Easy Read summary shows at the top of every screen when switched on", '        </sc-if>\n\n        <div class="amp-share"',
         '        </sc-if>\n' + fill(EASY_BLOCK) + '\n        <div class="amp-share"', 1),
    ]
    t += [mani(*m) for m in MANI]
    return t
