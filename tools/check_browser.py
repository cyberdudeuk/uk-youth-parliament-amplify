"""Real-browser checks for the built portal. Run: python3 -I tools/check_browser.py [--update-baseline]
Needs Playwright with Chromium (pip install -r tools/requirements-browser.txt; python3 -m playwright install chromium).

  W1  every screen opens with no script error and no request to another host
  W2  no screen overflows sideways at 320 px (WCAG reflow, a small phone), 768 px (a tablet) or 1440 px (a laptop)
  W3  axe-core finds no serious or critical accessibility issue beyond the recorded baseline for that screen; the
      baseline is the original design's own findings (open item O3) and may only shrink
  W4  the self-reporting screens fill from their data: Trusted sources shows cards, Portal health shows a status
  W6  the splash is safe when opened (from the masthead's Splash button since 1.0.0-rc.9): it is a labelled dialog, Tab stays inside it, Escape enters the portal and moves
      focus to the main content, it never closes by itself once someone has interacted, and it fits a 320 px phone
      and a 768 px tablet without sideways scrolling (D16; vaccinated against a splash with no keyboard handling)
  W7  the light theme passes axe-core with no serious or critical issue beyond the baseline on a sample of screens,
      and the page renders on a phone-class CPU (4x slowdown) within the stated budget, reported every run
  W8  the drawer scrolls on its own within the screen's height without moving the page (D17), and campaign artwork
      opens in an in-page viewer with Print, Save and Close that Escape closes, returning focus (D18; vaccinated
      against a drawer with no scroll of its own)
  W5  tooltips work: hovering a drawer item shows its explainer, keyboard focus on a term links it with
      aria-describedby, and Escape closes it (vaccinated against a page with no tooltip layer)
  W9  the news ticker, alerts, Share and product screens behave: the ticker is a labelled list of links that its button
      pauses (and says so), that stands still under reduced motion with no duplicate read out; an alert can be
      dismissed; Share opens a menu with a copy option when the device has no share sheet; the backlog filter narrows
      the list; and turning the ticker off on Alerts & notifications removes it (vaccinated against a ticker that
      keeps moving after its pause button is pressed)
  W10 one clear front door (D44, 17 November 2026: on a phone Home's title sat 1,227px down an 844px screen and every
      first visit opened on a closed petition's splash): arriving opens no dialog; Home's title starts within the
      first screen at 390 x 844 and at 1440 x 900; the Who are you? chooser is there and choosing a door shows three
      places to start; and the This screen strip is a closed disclosure (vaccinated against a page whose title sits
      below the fold)

Screens are read from data/integrity.json, which check_sources C9 keeps in step with the drawer, so a new screen is
tested without editing this file.

The axe check is vaccinated against a page with a deliberately unlabelled image, which it must flag.
"""
import argparse, asyncio, json, os, sys, threading, http.server, functools, socketserver

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(R, "site")
BASE = os.path.join(R, "tools", "a11y-baseline.json")
AXE = os.path.join(R, "vendor", "test", "axe.min.js")
SCREENS = [x["screen"] for x in json.load(open(os.path.join(R, "data", "integrity.json"), encoding="utf-8"))["screens"]]


SPEED_BUDGET_MS = 9000  # first meaningful paint of Home on a 4x-slowed CPU; tightened as the runtime gets lighter (O16)


async def splash_checks(b, url):
    bad = []
    for width in (1440, 768, 320):
        ctx = await b.new_context(viewport={"width": width, "height": 800}); pg = await ctx.new_page()
        await pg.goto(url, wait_until="networkidle"); await pg.wait_for_timeout(500)
        await pg.locator('button[data-tip="ui:replay"]').first.click(); await pg.wait_for_timeout(400)
        dlg = pg.locator('[data-amp-splash][role="dialog"]')
        if await dlg.count() == 0: bad.append(f"W6 at {width}px the splash is not a labelled dialog"); await ctx.close(); continue
        over = await pg.evaluate("document.documentElement.scrollWidth - window.innerWidth")
        if over > 1: bad.append(f"W6 the splash overflows sideways by {over}px at {width}px")
        for vb in ('button:has-text("Signal")', 'button:has-text("Manifesto")'):
            await pg.locator(vb).first.click(); await pg.wait_for_timeout(250)
            if await pg.locator(vb).first.get_attribute("aria-pressed") != "true": bad.append(f"W6 at {width}px {vb} does not say it is on")
            over = await pg.evaluate("document.documentElement.scrollWidth - window.innerWidth")
            if over > 1: bad.append(f"W6 the {vb} splash overflows by {over}px at {width}px")
        if width == 1440:
            for _ in range(25): await pg.keyboard.press("Tab")
            inside = await pg.evaluate("!!document.activeElement && !!document.activeElement.closest('[data-amp-splash]')")
            if not inside: bad.append("W6 Tab leaves the splash while it is open")
            await pg.keyboard.press("Escape"); await pg.wait_for_timeout(300)
            if await dlg.count(): bad.append("W6 Escape does not enter the portal")
            elif await pg.evaluate("document.activeElement && document.activeElement.id") != "amp-main": bad.append("W6 after the splash, focus is not on the main content")
            # interaction holds the splash open past its own timer
            await pg.goto(url, wait_until="networkidle"); await pg.locator('button[data-tip="ui:replay"]').first.click(); await pg.mouse.move(400, 300); await pg.wait_for_timeout(15500)
            if await dlg.count() == 0: bad.append("W6 the splash closed by itself after the reader had interacted")
        await ctx.close()
    return bad


DRAWER_JS = """() => { const n = document.querySelector('nav[aria-label="Portal sections"]'); if (!n) return 'no drawer';
  const cs = getComputedStyle(n), r = n.getBoundingClientRect();
  if (r.height > innerHeight) return 'the drawer is taller than the screen';
  if (n.scrollHeight > n.clientHeight + 1 && !/(auto|scroll)/.test(cs.overflowY)) return 'the drawer has more items than fit but cannot scroll';
  const y0 = scrollY; n.scrollTop = 300; return scrollY !== y0 ? 'scrolling the drawer moved the page' : ''; }"""


async def drawer_and_viewer(b, url):
    bad = []
    ctx = await b.new_context(viewport={"width": 1440, "height": 800}); pg = await ctx.new_page()
    await pg.goto(url + "#care", wait_until="networkidle"); await pg.wait_for_timeout(500)
    why = await pg.evaluate(DRAWER_JS)
    if why: bad.append("W8 " + why)
    await pg.goto(url + "#campaign", wait_until="networkidle"); await pg.wait_for_timeout(500)
    await pg.locator('button:has-text("View, print or save")').first.click(); await pg.wait_for_timeout(250)
    box = pg.locator('.amp-lightbox[role="dialog"]')
    if await box.count() == 0: bad.append("W8 campaign artwork does not open in the in-page viewer")
    else:
        for name in ("Print", "Save", "Close"):
            if await box.locator(f'text="{name}"').count() == 0: bad.append(f"W8 the artwork viewer has no {name}")
        await pg.keyboard.press("Escape"); await pg.wait_for_timeout(200)
        if await box.count(): bad.append("W8 Escape does not close the artwork viewer")
        elif "View" not in (await pg.evaluate("document.activeElement.textContent") or ""): bad.append("W8 closing the viewer does not return focus")
    await pg.set_content('<!doctype html><html lang="en"><title>t</title><nav aria-label="Portal sections" style="position:sticky;top:0;height:3000px">x</nav>')
    hit = bool(await pg.evaluate(DRAWER_JS))
    print(("caught     " if hit else "NOT CAUGHT ") + "W8 (a drawer with no scroll of its own)")
    if not hit: bad.append("W8 vaccination failed")
    await ctx.close()
    return bad


TK_MOVING = "(() => { const t = document.querySelector('.amp-tk-track'); return t ? getComputedStyle(t).animationPlayState : 'none'; })()"


async def ticker_and_friends(b, url):
    bad = []
    ctx = await b.new_context(viewport={"width": 1440, "height": 900}); pg = await ctx.new_page()
    await pg.goto(url + "#home", wait_until="networkidle"); await pg.wait_for_timeout(600)
    tk = pg.locator('section[aria-label="News for this screen"]')
    if await tk.count() == 0: bad.append("W9 #home has no news ticker"); await ctx.close(); return bad
    if await tk.locator("ul[role=list]:not([aria-hidden]) a[href^='http']").count() < 2: bad.append("W9 the ticker items are not links")
    await pg.mouse.move(5, 5)
    if await pg.evaluate(TK_MOVING) != "running": bad.append("W9 the ticker does not move when nobody is pausing it")
    btn = tk.locator("button[aria-pressed]")
    await btn.click(); await pg.mouse.move(5, 5); await pg.wait_for_timeout(200)
    if await btn.get_attribute("aria-pressed") != "true": bad.append("W9 the ticker's pause button does not say it is pressed")
    if await pg.evaluate(TK_MOVING) != "paused": bad.append("W9 pressing pause does not stop the ticker")
    al = pg.locator('section[aria-label="Alerts for you"] button[aria-label^="Dismiss"]')
    n = await al.count()
    if n == 0: bad.append("W9 #home shows no alert (the launch countdown is due)")
    else:
        await al.first.click(); await pg.wait_for_timeout(200)
        if await pg.locator('section[aria-label="Alerts for you"] button[aria-label^="Dismiss"]').count() != n - 1: bad.append("W9 dismissing an alert does not remove it")
    await pg.evaluate("Object.defineProperty(navigator, 'share', { value: undefined, configurable: true })")
    await pg.locator('button[aria-controls="amp-share-menu"]').first.click(); await pg.wait_for_timeout(200)
    if await pg.locator("#amp-share-menu").count() == 0: bad.append("W9 Share opens nothing when the device has no share sheet")
    elif await pg.locator('#amp-share-menu button:has-text("Copy link")').count() == 0: bad.append("W9 the share menu has no Copy link")
    await pg.goto(url + "#product", wait_until="networkidle"); await pg.wait_for_timeout(500)
    rows = await pg.locator("article.amp-req").count()
    if rows < 10: bad.append(f"W9 #product shows {rows} requirements")
    await pg.locator('select').filter(has=pg.locator('option[value="Could"]')).first.select_option("Could"); await pg.wait_for_timeout(200)
    if not 0 < await pg.locator("article.amp-req").count() < rows: bad.append("W9 the backlog priority filter does not narrow the list")
    await pg.goto(url + "#notify", wait_until="networkidle"); await pg.wait_for_timeout(500)
    await pg.locator('label:has-text("News ticker") input[type=checkbox]').uncheck(); await pg.wait_for_timeout(200)
    await pg.evaluate("location.hash = '#home'"); await pg.wait_for_timeout(400)
    if await pg.locator('section[aria-label="News for this screen"]').count(): bad.append("W9 turning the ticker off does not remove it")
    await ctx.close()
    ctx = await b.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce"); pg = await ctx.new_page()
    await pg.goto(url + "#home", wait_until="networkidle"); await pg.wait_for_timeout(500)
    if await pg.evaluate("(() => { const t = document.querySelector('.amp-tk-track'); return t ? getComputedStyle(t).animationName : 'gone'; })()") != "none": bad.append("W9 the ticker moves under reduced motion")
    if await pg.locator(".amp-tk-dup").first.is_visible(): bad.append("W9 the ticker's duplicate is shown under reduced motion")
    await pg.set_content('<!doctype html><html lang="en"><title>t</title><style>@keyframes m{to{transform:translateX(-50%)}}.amp-tk-track{animation:m 9s linear infinite}</style><section class="amp-tk"><div class="amp-tk-track">x</div><button aria-pressed="true">Pause</button></section>')
    hit = await pg.evaluate(TK_MOVING) == "running"
    print(("caught     " if hit else "NOT CAUGHT ") + "W9 (a ticker that keeps moving after pause)")
    if not hit: bad.append("W9 vaccination failed")
    await ctx.close()
    return bad


HEAD_TOP = "(() => { const h = document.querySelector('#amp-main h1'); return h ? Math.round(h.getBoundingClientRect().top + scrollY) : 99999; })()"


async def front_door(b, url):
    """W10 one clear front door (D44)."""
    bad = []
    for w, h in ((390, 844), (1440, 900)):
        ctx = await b.new_context(viewport={"width": w, "height": h}); pg = await ctx.new_page()
        await pg.goto(url, wait_until="networkidle"); await pg.wait_for_timeout(700)
        if await pg.locator('[data-amp-splash][role="dialog"]').count(): bad.append(f"W10 at {w}px a dialog opens by itself on arrival (D44)")
        top = await pg.evaluate(HEAD_TOP)
        if top > h - 120: bad.append(f"W10 at {w}x{h} Home's title starts at {top}px, below the first screen (D44)")
        if await pg.locator("#amp-doors").count() == 0: bad.append("W10 Home has no Who are you? chooser")
        else:
            await pg.locator('section[aria-labelledby="amp-doors"] ul button').first.click(); await pg.wait_for_timeout(300)
            n = await pg.locator("#amp-door-panel button.amp-card").count()
            if n != 3: bad.append(f"W10 choosing a door shows {n} places to start, not three")
        if await pg.locator("details.amp-explainer[open]").count(): bad.append("W10 the About this screen strip opens by default")
        await ctx.close()
    # vaccination: W10 must fail on a page whose title sits below the fold
    pg = await b.new_page(viewport={"width": 390, "height": 844})
    await pg.set_content('<!doctype html><html lang="en"><title>t</title><main id="amp-main"><div style="height:1200px"></div><h1>Late</h1></main></html>')
    hit = await pg.evaluate(HEAD_TOP) > 844 - 120
    print(("caught     " if hit else "NOT CAUGHT ") + "W10 (a title below the fold)")
    if not hit: bad.append("W10 vaccination failed")
    await pg.close()
    return bad


async def light_and_speed(b, url, axe, base):
    bad = []
    ctx = await b.new_context(viewport={"width": 1440, "height": 900}); pg = await ctx.new_page()
    for sc in ("home", "sources", "stem", "research", "care"):
        await pg.goto(url + "#" + sc, wait_until="networkidle"); await pg.wait_for_timeout(500)
        await pg.evaluate("document.body.setAttribute('data-theme', 'light')"); await pg.wait_for_timeout(200)
        await pg.add_script_tag(content=axe)
        res = await pg.evaluate("axe.run(document, {resultTypes: ['violations']}).then(r => r.violations.filter(v => ['serious','critical'].includes(v.impact)).map(v => v.id + ':' + v.nodes.length))")
        allowed = set(base.get("light:" + sc, []))
        for v in res:
            rid, n = v.split(":"); prev = next((int(a.split(":")[1]) for a in allowed if a.startswith(rid + ":")), None)
            if prev is None or int(n) > prev: bad.append(f"W7 light theme #{sc}: new or worse accessibility issue {v} (baseline {prev})")
        FOUND_LIGHT["light:" + sc] = sorted(res)
    await ctx.close()
    ctx = await b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True); pg = await ctx.new_page()
    cdp = await ctx.new_cdp_session(pg); await cdp.send("Emulation.setCPUThrottlingRate", {"rate": 4})
    import time; start = time.time()
    await pg.goto(url + "#home", wait_until="load")
    await pg.locator("main h1").first.wait_for(state="visible", timeout=60000)
    ms = int((time.time() - start) * 1000)
    print(f"W7 Home on a phone-class CPU (4x slowdown): {ms} ms to first heading (budget {SPEED_BUDGET_MS} ms)")
    if ms > SPEED_BUDGET_MS: bad.append(f"W7 Home took {ms} ms to render on a phone-class CPU, over the {SPEED_BUDGET_MS} ms budget")
    await ctx.close()
    return bad


FOUND_LIGHT = {}


async def tips(pg):
    """W5 on an open page: returns a list of problems (empty when tooltips behave)."""
    bad = []
    nav = pg.locator('[data-tip^="nav:"]').first
    if await nav.count() == 0: return ["W5 no drawer item carries a tooltip"]
    await nav.hover(); await pg.wait_for_timeout(150)
    tip = pg.locator("#amp-tip")
    if await tip.count() == 0 or not await tip.is_visible() or not (await tip.inner_text()).strip(): bad.append("W5 hovering a drawer item shows no tooltip")
    await pg.keyboard.press("Escape"); await pg.wait_for_timeout(100)
    if await tip.count() and await tip.is_visible(): bad.append("W5 Escape does not close the tooltip")
    return bad


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a): pass
    h = functools.partial(Quiet, directory=SITE)
    srv = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}/index.html"


async def run(update):
    from playwright.async_api import async_playwright
    srv, url = serve()
    axe = open(AXE, encoding="utf-8").read()
    base = json.load(open(BASE)) if os.path.exists(BASE) else {}
    found, bad = {}, []
    async with async_playwright() as p:
        exe = os.environ.get("CHROME") or None
        b = await p.chromium.launch(executable_path=exe, args=["--no-sandbox"])
        for width in (1440, 768, 320):
            ctx = await b.new_context(viewport={"width": width, "height": 900})
            for sc in SCREENS:
                pg = await ctx.new_page(); errs, ext = [], []
                pg.on("pageerror", lambda e, errs=errs: errs.append(str(e)[:200]))
                pg.on("request", lambda r, ext=ext: ext.append(r.url) if not r.url.startswith(("http://127.0.0.1", "data:", "blob:")) else None)
                await pg.goto(url + "#" + sc, wait_until="networkidle"); await pg.wait_for_timeout(700)
                if errs: bad.append(f"W1 #{sc} at {width}px: script error {errs[0]}")
                if ext: bad.append(f"W1 #{sc} at {width}px: request to another host {ext[0][:80]}")
                over = await pg.evaluate("document.documentElement.scrollWidth - window.innerWidth")
                if over > 1: bad.append(f"W2 #{sc} overflows sideways by {over}px at {width}px")
                if width == 1440:
                    await pg.add_script_tag(content=axe)
                    res = await pg.evaluate("axe.run(document, {resultTypes: ['violations']}).then(r => r.violations.filter(v => ['serious','critical'].includes(v.impact)).map(v => v.id + ':' + v.nodes.length))")
                    found[sc] = sorted(res)
                    allowed = set(base.get(sc, []))
                    for v in res:
                        rid, n = v.split(":"); prev = next((int(a.split(":")[1]) for a in allowed if a.startswith(rid + ":")), None)
                        if prev is None or int(n) > prev: bad.append(f"W3 #{sc}: new or worse accessibility issue {v} (baseline {prev})")
                    if sc == "sources" and await pg.locator("article.amp-card").count() < 5: bad.append("W4 #sources shows no source cards")
                    if sc == "stem":
                        t = pg.locator(".amp-term").first
                        await t.focus(); await pg.wait_for_timeout(100)
                        if await t.get_attribute("aria-describedby") != "amp-tip": bad.append("W5 #stem: a focused term is not linked to its tooltip")
                    if sc == "home": bad += [f"{x} (#home)" for x in await tips(pg)]
                    if sc == "health" and (await pg.locator("[role=status]").first.inner_text()).strip() in ("", "Checking…"): bad.append("W4 #health never reached a status")
                await pg.close()
            await ctx.close()
        bad += await splash_checks(b, url)
        bad += await front_door(b, url)
        bad += await drawer_and_viewer(b, url)
        bad += await ticker_and_friends(b, url)
        bad += await light_and_speed(b, url, axe, base)
        # vaccination: W6 must fail on a splash with no keyboard handling
        pg = await b.new_page(); await pg.set_content('<!doctype html><html lang="en"><title>t</title><div data-amp-splash role="dialog" aria-label="x"><button>a</button></div><main id="amp-main" tabindex="-1">m</main>')
        await pg.keyboard.press("Escape"); hit = await pg.locator("[data-amp-splash]").count() > 0
        print(("caught     " if hit else "NOT CAUGHT ") + "W6 (a splash that ignores Escape)")
        if not hit: bad.append("W6 vaccination failed")
        await pg.close()
        # vaccination: axe must flag an unlabelled image
        pg = await b.new_page(); await pg.set_content('<!doctype html><html lang="en"><title>t</title><img src="data:,">'); await pg.add_script_tag(content=axe)
        v = await pg.evaluate("axe.run(document).then(r => r.violations.map(v => v.id))")
        print(("caught     " if "image-alt" in v else "NOT CAUGHT ") + "W3 (axe flags an unlabelled image)")
        if "image-alt" not in v: bad.append("W3 vaccination failed: axe did not flag an unlabelled image")
        await pg.set_content('<!doctype html><html lang="en"><title>t</title><button data-tip="nav:home">Home</button>')
        hit = bool(await tips(pg))
        print(("caught     " if hit else "NOT CAUGHT ") + "W5 (a page with no tooltip layer)")
        if not hit: bad.append("W5 vaccination failed: a page with no tooltip layer passed")
        await b.close()
    srv.shutdown()
    if update:
        found.update(FOUND_LIGHT); json.dump(found, open(BASE, "w"), indent=1, sort_keys=True); print("baseline written:", BASE)
    else:
        for sc, got in found.items():  # the baseline may only shrink: note improvements so it can be tightened
            if set(got) != set(base.get(sc, [])) and not any(b.startswith("W3 #" + sc) for b in bad):
                print(f"note: #{sc} improved against its baseline; run with --update-baseline to lock that in")
    print(f"amplify browser: {len(SCREENS)} screens at 1440, 768 and 320 px, W1-W10 problems: {len(bad)}")
    if bad:
        print("\n".join(bad[:40])); sys.exit(1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--update-baseline", action="store_true")
    asyncio.run(run(ap.parse_args().update_baseline))
