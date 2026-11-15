"""Real-browser checks for the built portal. Run: python3 -I tools/check_browser.py [--update-baseline]
Needs Playwright with Chromium (pip install -r tools/requirements-browser.txt; python3 -m playwright install chromium).

  W1  every screen opens with no script error and no request to another host
  W2  no screen overflows sideways at 360 px (a phone) or 1440 px (a laptop)
  W3  axe-core finds no serious or critical accessibility issue beyond the recorded baseline for that screen; the
      baseline is the original design's own findings (open item O3) and may only shrink
  W4  the self-reporting screens fill from their data: Trusted sources shows cards, Portal health shows a status

The axe check is vaccinated against a page with a deliberately unlabelled image, which it must flag.
"""
import argparse, asyncio, json, os, sys, threading, http.server, functools, socketserver

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(R, "site")
BASE = os.path.join(R, "tools", "a11y-baseline.json")
AXE = os.path.join(R, "vendor", "test", "axe.min.js")
SCREENS = ("hub momentum plan coal kit pledge radar policy map acad ysc post track prof incl res ai brand care graph corner "
           "route state issues guide sources latest trust health changes help feedback launch about home media communities").split()


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
        for width in (1440, 360):
            ctx = await b.new_context(viewport={"width": width, "height": 900})
            for sc in SCREENS:
                pg = await ctx.new_page(); errs, ext = [], []
                pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
                pg.on("request", lambda r: ext.append(r.url) if not r.url.startswith(("http://127.0.0.1", "data:", "blob:")) else None)
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
                    if sc == "health" and (await pg.locator("[role=status]").first.inner_text()).strip() in ("", "Checking…"): bad.append("W4 #health never reached a status")
                await pg.close()
            await ctx.close()
        # vaccination: axe must flag an unlabelled image
        pg = await b.new_page(); await pg.set_content('<!doctype html><html lang="en"><title>t</title><img src="data:,">'); await pg.add_script_tag(content=axe)
        v = await pg.evaluate("axe.run(document).then(r => r.violations.map(v => v.id))")
        print(("caught     " if "image-alt" in v else "NOT CAUGHT ") + "W3 (axe flags an unlabelled image)")
        if "image-alt" not in v: bad.append("W3 vaccination failed: axe did not flag an unlabelled image")
        await b.close()
    srv.shutdown()
    if update:
        json.dump(found, open(BASE, "w"), indent=1, sort_keys=True); print("baseline written:", BASE)
    else:
        for sc, got in found.items():  # the baseline may only shrink: note improvements so it can be tightened
            if set(got) != set(base.get(sc, [])) and not any(b.startswith("W3 #" + sc) for b in bad):
                print(f"note: #{sc} improved against its baseline; run with --update-baseline to lock that in")
    print(f"amplify browser: {len(SCREENS)} screens at 1440 and 360 px, W1-W4 problems: {len(bad)}")
    if bad:
        print("\n".join(bad[:40])); sys.exit(1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--update-baseline", action="store_true")
    asyncio.run(run(ap.parse_args().update_baseline))
