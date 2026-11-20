"""Sixteenth set of portal extensions: a cookie-free totals counter, built switched off (20 November 2026, O18, REQ-37).

  The owner asked for the counter on 20 November 2026. O18 set the conditions: totals only, no identifiers stored, no
  profiling, a data protection impact assessment first, figures published on Portal health, and a review date.

  How it works when switched on
    count     each time a screen opens, the page sends one request: {"s": "<screen id>"}. The database adds 1 to
              that screen's total for the day (UTC date). Nothing else is sent or stored: no cookie, no storage used
              for counting, no IP address, no browser details, no referrer, no time finer than a date, no identifier,
              hash or fingerprint. The request goes with credentials omitted and no referrer.
    refuse    a browser that sends Global Privacy Control or Do Not Track is never counted, and anyone can switch
              counting off for themselves in Access and language settings (the choice is kept in this browser's
              preferences, which is what the person asked for).
    allow     the database accepts only the portal's own screen ids, caps each daily total, and keeps only
              totals; reading is limited to totals for the last 1 to 90 days.
    show      Portal health shows the last 28 days as totals, with a "read with care" note.

  Switched off by default: data/counter.json has no endpoint, so the page makes no request at all. Switching on is the
  owner's step (creating the database project is a new resource on his account): run docs/counter/schema.sql, put the
  project URL and publishable key in data/counter.json, and sign off docs/dpia-totals-counter.md. check_site S25
  refuses an endpoint without a signed-off DPIA, a secret key, or a page that counts anything but the screen id.
"""
import json
import os

from extend import LABEL

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = os.path.join(R, "data", "counter.json")


def config():
    with open(CFG, encoding="utf-8") as f:
        c = json.load(f)
    return {"endpoint": c.get("endpoint", ""), "key": c.get("key", "")}


def head_script():
    """The only counter settings the page sees: the endpoint and publishable key, or two empty strings (off)."""
    return "<script>window.__ampCount = " + json.dumps(config(), separators=(", ", ": ")) + ";</script>\n"


LOGIC16 = r'''  ampCountCfg() {
    const c = (typeof window !== "undefined" && window.__ampCount) || {};
    return typeof c.endpoint === "string" && /^https:\/\/[a-z0-9]{20}\.supabase\.co$/.test(c.endpoint) && typeof c.key === "string" && /^sb_publishable_[A-Za-z0-9_-]{10,}$/.test(c.key) ? c : null;
  }
  ampCountRefused() {
    try { return navigator.globalPrivacyControl === true || navigator.doNotTrack === "1" || window.doNotTrack === "1"; } catch (e) { return true; }
  }
  ampCountPost(c, fn, body) {
    return fetch(c.endpoint + "/rest/v1/rpc/" + fn, { method: "POST", headers: { apikey: c.key, "Content-Type": "application/json" }, body: JSON.stringify(body), credentials: "omit", referrerPolicy: "no-referrer", cache: "no-store", keepalive: fn === "amp_count" });
  }
  ampCount() {
    const s = this.state, c = this.ampCountCfg();
    if (!c || !s.screen || s.screen === this._ampLast) return;
    this._ampLast = s.screen;
    if (s.countOff || this.ampCountRefused() || !/^[a-z0-9-]{1,24}$/.test(s.screen)) return;
    try { this.ampCountPost(c, "amp_count", { s: s.screen }).catch(() => {}); } catch (e) { /* counting never breaks the page */ }
    if (s.screen === "health" && !this._ampAsked) {
      this._ampAsked = true;
      this.ampCountPost(c, "amp_totals", { days: 28 }).then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
        .then((rows) => this.setState({ ctRows: Array.isArray(rows) ? rows.slice(0, 2000) : [], ctErr: "" }))
        .catch(() => this.setState({ ctErr: "The counter could not be read just now. The totals are safe; try again later." }));
    }
  }
  ampVals16(s) {
    const c = this.ampCountCfg(), refused = this.ampCountRefused();
    const names = {}; (this.GROUPS || []).forEach((g) => (g[1] || []).forEach((x) => { names[x[0]] = x[1]; }));
    const rows = Array.isArray(s.ctRows) ? s.ctRows : [];
    const n = (x) => { const v = Number(x); return isFinite(v) && v > 0 ? Math.round(v) : 0; };
    const today = new Date().toISOString().slice(0, 10), wk = new Date(Date.now() - 6 * 864e5).toISOString().slice(0, 10);
    const by = {}; let t28 = 0, t7 = 0;
    rows.forEach((r) => { const k = String(r.screen || ""), v = n(r.n), d = String(r.day || ""); if (!/^[a-z0-9-]{1,24}$/.test(k)) return; by[k] = (by[k] || 0) + v; t28 += v; if (d >= wk && d <= today) t7 += v; });
    const top = Object.keys(by).sort((a, b) => by[b] - by[a]).slice(0, 10);
    const NF = this._ampNum || (this._ampNum = new Intl.NumberFormat("en-GB"));
    const label = !c ? "Off for everyone: the counter is not switched on" : refused ? "Not counted: your browser asks sites not to track" : s.countOff ? "Not counted: you switched it off" : "Counted in daily totals";
    return {
      tCount: () => this.setState({ countOff: !s.countOff }), ctPressed: c && !refused && !s.countOff ? "true" : "false",
      ctBg: this.onBg(!!(c && !refused && !s.countOff)), ctLabel: label,
      ctOn: !!c, ctOff: !c, ctErr: s.ctErr || "", ctHasErr: !!s.ctErr, ctHasRows: !!c && rows.length > 0, ctNone: !!c && !s.ctErr && rows.length === 0,
      ct28: NF.format(t28), ct7: NF.format(t7), ctScreens: String(top.length),
      ctTop: top.map((k) => ({ t: names[k] || k, v: NF.format(by[k]) })),
      ctYou: label,
    };
  }
'''

ACCESS_BTN = '''    <button onClick="{{ tCount }}" aria-pressed="{{ ctPressed }}" data-tip="ui:counter" style="text-align: left; border: 1px solid rgb(var(--film-rgb) / 0.13); border-radius: 14px; padding: 11px 13px; background: {{ ctBg }}; color: rgb(var(--ink-rgb));">
      <div style="font-family: 'Space Mono', monospace; font-size: 10.5px; letter-spacing: 0.14em; text-transform: uppercase; color: rgb(var(--ink-rgb) / 0.7);">Totals counter</div>
      <div style="font-size: 14px; font-weight: 700; margin-top: 2px;">{{ ctLabel }}</div>
    </button>
'''

HEALTH_ANCHOR = ('          <div style="border: 1px solid rgb(var(--film-rgb) / 0.12); border-radius: 22px; background: rgb(var(--film-rgb) / 0.04); padding: 20px 22px;">\n'
                 '            <div style="font-family: \'Space Mono\', monospace; font-size: 10.5px; letter-spacing: 0.14em; text-transform: uppercase; color: rgb(var(--ink-rgb) / 0.78); margin-bottom: 10px;">Freshness</div>\n')

PANEL = '''          <section aria-labelledby="amp-ct-h" style="border: 1px solid rgb(var(--film-rgb) / 0.12); border-radius: 22px; background: rgb(var(--film-rgb) / 0.04); padding: 20px 22px; display: flex; flex-direction: column; gap: 10px;">
            <h2 id="amp-ct-h" style="@LABEL@ margin: 0;">Screens opened: totals only</h2>
            <sc-if value="{{ ctOff }}" hint-placeholder-val="{{ true }}"><p style="margin: 0; font-size: 14px; line-height: 1.6;">The totals counter is built but switched off. While it is off the portal sends nothing anywhere, so there are no figures to show here.</p></sc-if>
            <sc-if value="{{ ctOn }}" hint-placeholder-val="{{ false }}"><p style="margin: 0; font-size: 14px; line-height: 1.6;">Each time a screen opens, one is added to that screen's total for the day. No cookies, nothing stored on your device for counting, and nothing that identifies you or your browser. Last 28 days, by UTC date.</p></sc-if>
            <sc-if value="{{ ctHasRows }}" hint-placeholder-val="{{ false }}">
            <div style="display: flex; flex-wrap: wrap; gap: 18px;">
              <div><div class="amp-count" style="font-size: 26px; font-weight: 900;">{{ ct28 }}</div><div style="@LABEL@">Last 28 days</div></div>
              <div><div class="amp-count" style="font-size: 26px; font-weight: 900;">{{ ct7 }}</div><div style="@LABEL@">Last 7 days</div></div>
              <div><div class="amp-count" style="font-size: 26px; font-weight: 900;">{{ ctScreens }}</div><div style="@LABEL@">Screens listed</div></div>
            </div>
            <div role="table" aria-label="The most-opened screens in the last 28 days" style="display: flex; flex-direction: column; font-size: 13.5px;">
              <div role="row" style="display: grid; grid-template-columns: 1fr auto; gap: 10px; padding: 6px 0; border-bottom: 1px solid rgb(var(--film-rgb) / 0.12);"><span role="columnheader" style="@LABEL@">Screen</span><span role="columnheader" style="@LABEL@">Opened</span></div>
              <sc-for list="{{ ctTop }}" as="r" hint-placeholder-count="5"><div role="row" style="display: grid; grid-template-columns: 1fr auto; gap: 10px; padding: 6px 0; border-bottom: 1px solid rgb(var(--film-rgb) / 0.08);"><span role="cell">{{ r.t }}</span><span role="cell" style="font-variant-numeric: tabular-nums;">{{ r.v }}</span></div></sc-for>
            </div>
            </sc-if>
            <sc-if value="{{ ctNone }}" hint-placeholder-val="{{ false }}"><p style="margin: 0; font-size: 13.5px;">No totals yet.</p></sc-if>
            <sc-if value="{{ ctHasErr }}" hint-placeholder-val="{{ false }}"><p role="status" style="margin: 0; font-size: 13.5px;">{{ ctErr }}</p></sc-if>
            <p style="margin: 0; font-size: 13px; line-height: 1.6; color: rgb(var(--ink-rgb) / 0.8);"><span style="font-weight: 800;">Read with care:</span> these are screens opened, not people. Anyone can add to the totals, and browsers that ask sites not to track, or people who switch counting off, are never counted. Treat them as a rough guide. Your setting: {{ ctYou }} (change it in Access).</p>
          </section>
'''


def transforms():
    return [
        ("ext16-head", "O18: the counter's only settings (empty, so off) are given to the page in one inline line",
         '<script src="./support.js"></script>\n', head_script() + '<script src="./support.js"></script>\n', 1),
        ("ext16-prefs", "O18: switching counting off is remembered with the other preferences",
         '"easy", "acadDone"]', '"easy", "acadDone", "countOff"]', 2),
        ("ext16-access", "O18: a counting switch in Access and language settings",
         '    <button onClick="{{ tEasy }}" aria-pressed="{{ erPressed }}" data-tip="ui:easyread"',
         ACCESS_BTN + '    <button onClick="{{ tEasy }}" aria-pressed="{{ erPressed }}" data-tip="ui:easyread"', 1),
        ("ext16-health", "O18: Portal health publishes the totals, with a read-with-care note",
         HEALTH_ANCHOR, PANEL.replace("@LABEL@", LABEL) + HEALTH_ANCHOR, 1),
        ("ext16-hook", "O18: one count per screen opened, after the page has rendered it",
         "  componentDidUpdate() {\n    this.syncBody();\n", "  componentDidUpdate() {\n    this.syncBody();\n    this.ampCount();\n", 1),
        ("ext16-logic", "O18: counter logic", "  async loadPetition() {", LOGIC16 + "\n  async loadPetition() {", 1),
        ("ext16-vals", "O18: counter values join renderVals", "...this.ampVals14(s),", "...this.ampVals14(s), ...this.ampVals16(s),", 1),
    ]


SCHEMA = "-- Amplify totals counter (O18, REQ-37). Run once in the project's SQL editor.\n-- Generated by tools/build_site.py from the portal's own screen list; do not edit by hand.\n-- Stores totals only: one row per screen per UTC day. No IP address, no browser details, no identifier.\n\ncreate table if not exists public.amp_daily (\n  day date not null,\n  screen text not null check (screen ~ '^[a-z0-9-]{1,24}$'),\n  n integer not null default 0 check (n >= 0 and n <= 1000000),\n  primary key (day, screen)\n);\nalter table public.amp_daily enable row level security;\nrevoke all on table public.amp_daily from public, anon, authenticated;\n\n-- Add one to today's total for a known screen. Anything else is ignored.\ncreate or replace function public.amp_count(s text) returns void\nlanguage plpgsql security definer set search_path = '' as $$\nbegin\n  if s is null or not (s = any (array[@IDS@])) then return; end if;\n  insert into public.amp_daily as d (day, screen, n) values ((now() at time zone 'utc')::date, s, 1)\n  on conflict (day, screen) do update set n = least(d.n + 1, 1000000);\nend; $$;\n\n-- Totals for the last 1 to 90 days, newest first. Totals only: there is nothing else to read.\ncreate or replace function public.amp_totals(days integer) returns table (day date, screen text, n integer)\nlanguage sql stable security definer set search_path = '' as $$\n  select d.day, d.screen, d.n from public.amp_daily d\n  where d.day > (now() at time zone 'utc')::date - least(greatest(coalesce(days, 28), 1), 90)\n  order by d.day desc, d.n desc;\n$$;\n\nrevoke all on function public.amp_count(text) from public;\nrevoke all on function public.amp_totals(integer) from public;\ngrant execute on function public.amp_count(text) to anon;\ngrant execute on function public.amp_totals(integer) to anon;\n"


def screen_ids(page):
    """The portal's screen ids, read from the page's own hash router (one master)."""
    import re
    m = re.search(r"\^\(([a-z0-9|-]+)\)\$", page)
    if not m:
        raise ValueError("O18: the page's screen list was not found, so the counter cannot know which screens exist")
    return m.group(1).split("|")


def schema_sql(ids):
    return SCHEMA.replace("@IDS@", ", ".join("'" + i + "'" for i in ids))
