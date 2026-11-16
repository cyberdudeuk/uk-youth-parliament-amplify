"""Build the published portal (site/) from the design files in app/. Run: python3 -I tools/build_site.py [--date YYYY-MM-DD]

app/ holds the Claude Design project byte for byte (check_repo.py R4 proves it). This script never edits app/: it
copies it into site/ and applies the transforms below, each one named, each one with the reason it exists, and each
one required to match exactly the number of times it says. A transform that matches 0 times, or more than it should,
stops the build, so a change to the design can never be half-applied silently (B1). The build also writes
site/build.json: what was built, from which source bytes, with which transforms.

Why a build at all, rather than publishing app/ as it is: the design is a design canvas. It opens on a side-by-side
review view, has six image drop-zones that read "Drop the … logo", no title, no footer, no disclaimer that it is an
unofficial prototype, and its map loads a stylesheet and street tiles that a published artifact blocks. The build
turns that canvas into a page someone can be sent, and leaves the design as the single source.
"""
import argparse, datetime, hashlib, html, io, json, os, re, shutil, sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(R, "tools"))
import art  # noqa: E402
import extend  # noqa: E402
import extend2  # noqa: E402
import extend3  # noqa: E402
import extend4  # noqa: E402
import extend5  # noqa: E402
import extend6  # noqa: E402
import extend7  # noqa: E402
import extend8  # noqa: E402
import extend9  # noqa: E402
import extend10  # noqa: E402
import make_docs  # noqa: E402

APP, SITE, VENDOR, DATA = (os.path.join(R, d) for d in ("app", "site", "vendor", "data"))
REPO_URL = "https://github.com/cyberdudeuk/uk-youth-parliament-amplify"
LIVE_URL = "https://cyberdudeuk.github.io/uk-youth-parliament-amplify/"  # public on GitHub Pages: owner's decision, 15 Nov 2026 (PR 7)
CONTACT_URL = REPO_URL + "/issues/new?template=contact.yml"
PORTAL_SRC, MAP_SRC = "Amplify Portal.dc.html", "Local Routes Map.html"


class BuildError(Exception):
    pass


def sub(text, name, old, new, count=1):
    n = text.count(old)
    if n != count:
        raise BuildError(f"B1 transform '{name}' expected {count} match(es) and found {n}: the design changed under it")
    return text.replace(old, new)


def mono(size=10.5, alpha=0.7, extra=""):
    return (f"font-family: 'Space Mono', monospace; font-size: {size}px; letter-spacing: 0.14em; text-transform: uppercase; "
            f"color: rgb(var(--ink-rgb) / {alpha});{extra}")


def footer(meta):
    """The usual footer: disclaimers, disclosures, transparency, contact, then the barcode and QR colophon."""
    h = html.escape
    col = "display: flex; flex-direction: column; gap: 8px; min-width: 0;"
    p = "margin: 0; font-size: 13px; line-height: 1.6; color: rgb(var(--ink-rgb) / 0.8);"
    def block(title, body):
        return f'<section style="{col}"><h2 style="margin: 0; {mono(10.5, 0.72)}">{title}</h2>{body}</section>'
    disclaimers = block("Disclaimers", f'''
      <p style="{p}">Amplify is an independent, unofficial prototype. It is not a service of, and is not endorsed by, the UK Youth Parliament, the National Youth Agency or UK Parliament.</p>
      <p style="{p}">Petition 754954 figures come from a snapshot of UK Parliament&rsquo;s published data taken on {h(meta["petition_date_long"])}. The petition closed on 11 August 2026, so the counts are final. Screens marked prototype, sample or model show planning figures, not records.</p>
      <p style="{p}">Links to other organisations are for information, not endorsement. Worried about your safety? Go to <a href="#care">Safeguarding &amp; support</a>.</p>''')
    disclosures = block("Disclosures", f'''
      <p style="{p}">Designed in Claude Design and built with Claude, Anthropic&rsquo;s AI model. AI-made content can contain mistakes: check the linked source before you rely on a figure.</p>
      <p style="{p}">No sign-in, no cookies, no analytics. Settings and any pledges you add are kept in this browser only and are never sent. Every font, script and icon is served by the portal itself. Links to other sites, and the share and calendar buttons, contact those services only when you choose them, under their own terms and age rules.</p>
      <p style="{p}">The copilot answers only where a live model connection is available; elsewhere it says so rather than guessing.</p>''')
    transparency = block("Transparency", f'''
      <p style="{p}">Build <span style="font-family: 'Space Mono', monospace;">{h(meta["build_id"])}</span>, built {h(meta["built_long"])} from the design project&rsquo;s source files; every transform from design to page is listed in <span style="font-family: 'Space Mono', monospace;">build.json</span>.</p>
      <p style="{p}">Next review due {h(meta["review_long"])}. How the portal is checking itself right now: <a href="#health">Portal health</a>. Who it is for and the safeguards it follows: <a href="#trust">Safeguards &amp; audiences</a>.</p>
      <p style="{p}">Source, checks and history: <a href="{REPO_URL}" target="_blank" rel="noopener">github.com/cyberdudeuk/uk-youth-parliament-amplify</a>. Code: MIT. Written content: see the repository&rsquo;s content licence.</p>
      <p style="{p}">Contains Parliamentary information licensed under the <a href="https://www.parliament.uk/site-information/copyright-parliament/open-parliament-licence/" target="_blank" rel="noopener">Open Parliament Licence v3.0</a>.</p>''')
    contact = block("Contact", f'''
      <p style="{p}">Questions, corrections and suggestions go through the <a href="{CONTACT_URL}" target="_blank" rel="noopener">contact form</a>.</p>
      <p style="{p}">The form is public. Do not include your name, contact details or anything that identifies a young person.</p>
      <p style="{p}">Who is behind it: <a href="#about">About Amplify</a> &middot; <a href="https://github.com/cyberdudeuk" target="_blank" rel="noopener">github.com/cyberdudeuk</a>. Ideas and bugs: <a href="#feedback">Have your say</a>.</p>
      <p style="{p}">Cannot use the form? Ask your MYP, a youth worker or a trusted adult to raise it for you.</p>''')
    colophon = f'''
      <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 18px; margin-top: 22px; padding-top: 18px; border-top: 1px solid rgb(var(--film-rgb) / 0.11);">
        <img src="./art/qr.svg" width="76" height="76" alt="QR code linking to the portal's source repository on GitHub" style="display: block; border-radius: 8px; background: #fff; padding: 4px;" />
        <img src="./art/barcode.svg" width="190" height="56" alt="Barcode of build {h(meta["build_id"])}" style="display: block; border-radius: 6px; background: #fff; padding: 4px 6px;" />
        <p style="margin: 0; flex: 1 1 240px; {mono(10, 0.66, ' line-height: 1.8; letter-spacing: 0.08em;')}">Colophon &middot; Amplify &middot; set in Chivo, Space Mono and Atkinson Hyperlegible &middot; six primitives, four cornerstones &middot; build {h(meta["build_id"])}</p>
      </div>'''
    return f'''
  <footer role="contentinfo" aria-label="About this portal" style="margin: 0 20px 96px; padding: 24px 24px 20px; border: 1px solid rgb(var(--film-rgb) / 0.11); border-radius: 22px; background: rgb(var(--film-rgb) / 0.035); backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px);">
    <div style="display: flex; flex-wrap: wrap; align-items: baseline; gap: 10px; margin-bottom: 18px;">
      <span style="font-size: 18px; font-weight: 900; letter-spacing: -0.03em;">Amplify</span>
      <span style="{mono(10.5, 0.66)}">Youth voice, carried further &middot; unofficial prototype</span>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 22px;">{disclaimers}{disclosures}{transparency}{contact}
    </div>{colophon}
  </footer>
'''


GF_P = '''<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
<link href="https://fonts.googleapis.com/css2?family=Chivo:ital,wght@0,300;0,400;0,600;0,700;0,900;1,400&family=Space+Mono:wght@400;700&family=Atkinson+Hyperlegible:wght@400;700&display=swap" rel="stylesheet" />'''


def meta_tags(meta):
    ld = {"@context": "https://schema.org", "@type": "WebSite", "name": "Amplify", "identifier": meta["build_id"], "version": meta["build_id"],
          "dateModified": meta["built"], "inLanguage": "en-GB", "audience": [{"@type": "PeopleAudience", "suggestedMinAge": 11, "suggestedMaxAge": 25}, {"@type": "Audience", "audienceType": "Parents, carers and guardians"}],
          "isAccessibleForFree": True, "license": REPO_URL + "/blob/main/LICENSE", "url": LIVE_URL, "codeRepository": REPO_URL}
    return (f'<meta name="artefact:id" content="amplify-portal">\n<meta name="artefact:version" content="{meta["build_id"]}">\n'
            f'<meta name="artefact:class" content="portal">\n<meta name="artefact:as-of" content="{meta["built"]}">\n'
            f'<meta name="artefact:review-date" content="{meta["review"]}">\n<script type="application/ld+json">{json.dumps(ld)}</script>\n')


def transforms(meta):
    """(name, reason, old, new, count): applied in order to the portal page."""
    img = lambda f, alt, r: (f'<img src="./art/{f}" alt="{html.escape(alt)}" '
                             f'style="display: block; width: 100%; height: 100%; object-fit: cover; border-radius: {r}px;" />')
    corners = []
    for name, ph in (("participation", "Participation: young people leading a session"),
                     ("equality", "Equality: a mixed group, real setting"),
                     ("education", "Education: informal learning in a youth club"),
                     ("empowerment", "Empowerment: a young person speaking to power")):
        corners.append((f"slot-{name}", "a drop-zone cannot ship; the brand's primitives replace the photo",
                        f'<image-slot id="amp-corner-{name}" shape="rounded" radius="14" placeholder="{ph}"></image-slot>',
                        img(f"{name}.svg", "", 14), 1))
    return [
        ("lang", "screen readers need the page language", "<html>", '<html lang="en">', 1),
        ("head", "a published page needs a title, a description and an icon",
         '<meta name="viewport" content="width=device-width, initial-scale=1">\n',
         '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
         '<title>Amplify: youth voice, carried further</title>\n'
         '<meta name="description" content="An unofficial prototype campaign portal for UK Youth Parliament campaigners: petition 754954 against what it needed, launch windows, coalitions, toolkits and safeguarding.">\n'
         '<link rel="icon" href="./art/favicon.svg" type="image/svg+xml">\n' + SHARE_TAGS, 1),
        ("no-image-slot-runtime", "the drop-zone runtime is design-time only, and asks for a state file that does not exist",
         '<script src="./image-slot.js"></script>\n', "", 1),
        ("default-view", "the side-by-side review view is for design review; a published portal opens on the portal",
         "&quot;options&quot;:[&quot;Portal&quot;,&quot;Both&quot;,&quot;App&quot;],&quot;default&quot;:&quot;Both&quot;",
         "&quot;options&quot;:[&quot;Portal&quot;,&quot;Both&quot;,&quot;App&quot;],&quot;default&quot;:&quot;Portal&quot;", 1),
        ("default-view-fallback", "the same default where props are absent",
         '((this.props || {}).defaultView || "Both")', '((this.props || {}).defaultView || "Portal")', 1),
        ("slot-splash-logo", "no partner logo is licensed; the Amplify mark beside it already identifies the page",
         '<div style="width: 132px; height: 54px; margin-left: 6px;">\n        <image-slot id="amp-splash-logo" shape="rounded" radius="14" placeholder="Drop the UKYP or partner logo"></image-slot>\n      </div>',
         f'<span style="margin-left: 6px; border: 1px solid rgb(var(--film-rgb) / 0.2); border-radius: 999px; padding: 6px 12px; {mono(10, 0.72)}">Unofficial prototype</span>', 1),
        ("slot-hero", "a drop-zone cannot ship; the annual sitting is drawn instead",
         '<image-slot id="amp-hub-hero" shape="rounded" radius="18" placeholder="Hero image — MYPs at the annual sitting"></image-slot>',
         img("hero.svg", "Illustration: members seated on facing benches at the annual sitting", 18), 1),
        *corners,
        ("masthead-unofficial", "the masthead names UKYP; it must also say this is not UKYP's own service",
         'color: rgb(var(--ink-rgb) / 0.62);">UKYP campaign engine</span>',
         'color: rgb(var(--ink-rgb) / 0.62);">UKYP campaign engine</span>\n'
         f'      <span title="Not a service of the UK Youth Parliament, the National Youth Agency or UK Parliament" style="border: 1px solid oklch(var(--t2) 0.14 70 / 0.5); border-radius: 999px; padding: 3px 9px; {mono(9.5, 0.8)}">Unofficial prototype</span>', 1),
        ("splash-unofficial", "the splash is the first screen; the disclaimer belongs on it too",
         "Where a screen is a prototype or a planning model, it says so on the screen.</p>",
         "Where a screen is a prototype or a planning model, it says so on the screen. Amplify is an independent, unofficial prototype: not a service of, or endorsed by, the UK Youth Parliament, the National Youth Agency or UK Parliament.</p>", 1),
        ("pledge-samples", "the five seed pledges read as real people; they are invented and must say so",
         'margin-bottom: 12px;">Latest pledges</div>',
         'margin-bottom: 12px;">Latest pledges &middot; the first five are invented samples; any you add stay in this browser</div>', 1),
        ("pledge-local", "say where a pledge goes: nowhere, it stays on this device",
         "No pledge is shown publicly with a full name unless you are over 16.",
         "No pledge is shown publicly with a full name unless you are over 16. In this prototype a pledge is saved in your browser only: nothing is sent.", 1),
        ("copilot-ready", "the copilot only knew the design host's window.claude.complete; on the published page the model is reached through the artifact's sample capability",
         "if (!window.claude || !window.claude.complete) {", "if (!(await this.modelReady())) {", 2),
        ("copilot-call", "route both copilot calls through one helper that picks whichever model connection the host offers",
         "await window.claude.complete({", "await this.complete({", 2),
        ("copilot-helpers", "the helper itself: design host first, then the published artifact's sample capability, else none (the existing fallback text then shows)",
         "  async runChat() {",
         """  modelReady() {
    if (window.claude && window.claude.complete) return Promise.resolve(true);
    if (!this._samplePromise) {
      this._samplePromise = (window.claude && typeof window.claude.use === "function")
        ? Promise.resolve(window.claude.use("sample")).catch(() => null) : Promise.resolve(null);
    }
    return this._samplePromise.then((s) => { this._sample = s; return !!s; });
  }
  async complete(o) {
    if (window.claude && window.claude.complete) return window.claude.complete(o);
    const m = o.messages || [];
    const input = [{ role: "user", content: (o.system || "") + "\\n\\n---\\n\\n" + (m[0] ? m[0].content : "") }].concat(m.slice(1));
    const r = await this._sample(input, { cache: false, modelTier: "quick" });
    return (r && r.text) || "";
  }

  async runChat() {""", 1),
        ("self-hosted-fonts", "fonts served by the portal itself: no visitor's IP address goes to Google",
         GF_P, '<link href="./vendor/fonts/fonts.css" rel="stylesheet" />', 1),
        ("self-hosted-runtime", "React, ReactDOM and Babel served by the portal itself; support.js reads window.__resources before any CDN",
         '<script src="./support.js"></script>\n',
         '<script>window.__resources = {"https://unpkg.com/react@18.3.1/umd/react.production.min.js": "./vendor/runtime/react.production.min.js", "https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js": "./vendor/runtime/react-dom.production.min.js", "https://unpkg.com/@babel/standalone@7.29.0/babel.min.js": "./vendor/runtime/babel.min.js"};</script>\n<script src="./support.js"></script>\n', 1),
        ("self-describing", "machine-readable identity, version, as-of and review dates (build standard: self-describing)",
         '<link rel="icon" href="./art/favicon.svg" type="image/svg+xml">\n',
         '<link rel="icon" href="./art/favicon.svg" type="image/svg+xml">\n' + meta_tags(meta), 1),
        ("helplines-papyrus", "HOPELINE247 closed on 7 September 2026 (defect D3); NHS 111 is where the administrators point people",
         '["Papyrus HOPELINE247", "0800 068 4141", "For anyone under 35 having thoughts of suicide, and for people worried about them.", "https://www.papyrus-uk.org/"],',
         '["NHS 111", "111 \\u00b7 urgent help", "Urgent mental health support when it is not an emergency. In an emergency call 999.", "https://111.nhs.uk/"],', 1),
        ("helplines-mix", "The Mix's phone helpline has closed; its 24/7 text route is what its own site gives (defect D4)",
         '["The Mix", "0808 808 4994", "Support for under-25s across mental health, money, work and relationships.", "https://www.themix.org.uk/"],',
         '["The Mix", "Text THEMIX to 85258", "Support for under-25s across mental health, money, work and relationships, with 24/7 crisis text support.", "https://www.themix.org.uk/"],', 1),
        ("helplines-samaritans-welsh", "Samaritans' free Welsh Language Line, verified 15 November 2026",
         '"Any age, any problem. Free from any phone and never shows on the bill."',
         '"Any age, any problem. Free from any phone and never shows on the bill. Welsh Language Line: 0808 164 0123."', 1),
        *extend.transforms(meta["n_sources"], meta["n_latest"]),
        *extend2.transforms(),
        *extend3.transforms(),
        *extend4.transforms(),
        *extend5.transforms(),
        *extend6.transforms(),
        *extend7.transforms(),
        *extend8.transforms(),
        *extend9.transforms(),
        *extend10.transforms(),
        ("footer", "the usual footer: disclaimers, disclosures, transparency, contact and colophon",
         "    </sc-if>\n\n  </div>\n</div>\n\n\n\n\n<div style=\"position: fixed; right: 18px;",
         "    </sc-if>\n\n  </div>\n" + footer(meta) + "</div>\n\n\n\n\n<div style=\"position: fixed; right: 18px;", 1),
    ]


def map_transforms():
    return [
        ("map-back-link", "the portal is index.html in the built site", 'href="./Amplify Portal.dc.html"', 'href="./index.html"', 1),
        ("map-leaflet-css", "a published artifact blocks stylesheets from unpkg; ship the same bytes (SRI-verified at build)",
         '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha384-sHL9NAb7lN7rfvG5lfHpm643Xkcjzp4jFvuavGOndn6pjVqS6ny56CAt3nsEVT4H" crossorigin="anonymous">',
         '<link rel="stylesheet" href="./vendor/leaflet-1.9.4/leaflet.css">', 1),
        ("map-leaflet-js", "serve Leaflet from the site too, so the map has no third-party script dependency",
         '<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha384-cxOPjt7s7Iz04uaHJceBmS+qpjv2JkIHNVcuOrM+YHwZOmJGBXI00mdUXEq65HTH" crossorigin="anonymous"></script>',
         '<script src="./vendor/leaflet-1.9.4/leaflet.js"></script>', 1),
        ("map-fonts", "map fonts served by the portal itself",
         '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Chivo:wght@400;600;700;900&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">',
         '<link href="./vendor/fonts/fonts.css" rel="stylesheet">', 1),
        ("map-labels", "labels on the map: nation names always, area names from zoom level 7 so the UK view stays readable",
         '    m.bindTooltip(a[0], { direction: "top" });\n    markers[i] = m;\n  });\n',
         '    m.bindTooltip(a[0], { direction: "top", permanent: true, className: "amp-pinlabel", offset: [0, -12] });\n    markers[i] = m;\n  });\n'
         '  [["England", 52.75, 0.05], ["Scotland", 57.35, -5.3], ["Wales", 52.65, -4.75], ["Northern Ireland", 53.95, -7.55]].forEach(function (n) {\n'
         '    L.tooltip({ permanent: true, direction: "center", className: "amp-nationlabel", interactive: false }).setLatLng([n[1], n[2]]).setContent(n[0]).addTo(map);\n  });\n'
         '  function ampLabels() { document.getElementById("map").classList.toggle("amp-labels-on", map.getZoom() >= 7); }\n'
         '  map.on("zoomend", ampLabels); ampLabels();\n', 1),
        ("map-label-css", "label styles: readable on both themes, hidden area labels until zoomed in",
         "<style>\n", "<style>\n  .leaflet-tooltip.amp-nationlabel { background: rgb(4 12 11 / 0.55); border: 0; border-radius: 6px; padding: 3px 7px; box-shadow: none; color: rgb(var(--ink-rgb) / 0.75); font: 700 13px/1 'Space Mono', monospace; letter-spacing: 0.14em; text-transform: uppercase; text-shadow: 0 1px 3px rgb(0 0 0 / 0.6); }\n  .leaflet-tooltip.amp-nationlabel::before { display: none; }\n  .leaflet-tooltip.amp-pinlabel { display: none; font: 600 12px/1.2 Chivo, sans-serif; padding: 2px 6px; }\n  #map.amp-labels-on .leaflet-tooltip.amp-pinlabel { display: block; }\n", 1),
        ("map-icon", "favicon", "<title>Local routes in — Amplify</title>",
         '<title>Local routes in — Amplify</title>\n<link rel="icon" href="./art/favicon.svg" type="image/svg+xml">', 1),
        ("map-outline", "street tiles are remote images, which a published artifact blocks; draw a local land outline under the markers so the map always shows where an area is",
         "  setTiles();\n\n  var PETITION = null;\n",
         "  setTiles();\n"
         "  var outline = null;\n"
         "  function outlineStyle() { var light = document.body.dataset.theme === \"light\"; return { color: light ? \"#5b7f78\" : \"#3f6f66\", weight: 1, fillColor: light ? \"#dcece4\" : \"#10241f\", fillOpacity: 0.9 }; }\n"
         "  fetch(new URL(\"./vendor/outline.json\", document.baseURI).href).then(function (r) { return r.ok ? r.json() : null; }).then(function (g) {\n"
         "    if (!g) return; outline = L.geoJSON(g, { style: outlineStyle, interactive: false }).addTo(map); outline.bringToBack();\n"
         "  }).catch(function () { /* the markers and search still work */ });\n\n  var PETITION = null;\n", 1),
        ("map-outline-theme", "the outline follows the theme toggle, as the tiles do",
         "    setTiles();\n    renderList(qEl.value);", "    setTiles(); if (outline) outline.setStyle(outlineStyle());\n    renderList(qEl.value);", 1),
        ("map-no-street-tiles", "the design's CARTO tiles now answer every request with an 'API key required' image (a 200, so the page's own tileerror fallback never fires), and a published artifact blocks remote images anyway: the local outline is the basemap",
         """    tiles = L.tileLayer("https://{s}.basemaps.cartocdn.com/" + (light ? "light_all" : "dark_all") + "/{z}/{x}/{y}{r}.png", {
      attribution: "\\u00a9 OpenStreetMap contributors \\u00a9 CARTO", subdomains: "abcd", maxZoom: 12, crossOrigin: true
    });
    tiles.on("tileerror", function () {
      if (tileFailed) return; tileFailed = true;
      var note = document.getElementById("tile-note"); if (note) note.hidden = false;
    });
    tiles.addTo(map);
""", "    /* street tiles removed by the build: see build.json, transform map-no-street-tiles */\n", 1),
        ("map-attribution", "credit what the map now draws",
         'Basemap &copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors, &copy; <a href="https://carto.com/attributions" target="_blank" rel="noopener">CARTO</a>.',
         'Land outline from <a href="https://www.naturalearthdata.com/" target="_blank" rel="noopener">Natural Earth</a> (public domain), 1:50m.', 1),
        ("map-outline-attribution", "the map's own attribution control names the outline source",
         "outline = L.geoJSON(g, { style: outlineStyle, interactive: false })",
         "outline = L.geoJSON(g, { style: outlineStyle, interactive: false, attribution: \"Natural Earth\" })", 1),
    ]


def rule_ids():
    """The checks that guard the build, read from the check scripts' own docstrings (one master, no copy)."""
    out = []
    for f in ("check_repo.py", "check_site.py", "check_sources.py", "check_browser.py"):
        p = os.path.join(R, "tools", f)
        if not os.path.exists(p): continue
        doc = open(p, encoding="utf-8").read().split('"""')[1]
        for m in re.finditer(r"^\s{2}([RSCW]\d+)\s{1,3}(.+(?:\n\s{5,}\S.*)*)", doc, re.M):
            out.append({"id": m.group(1), "what": re.sub(r"\s+", " ", m.group(2)).strip()})
    return out


def sri(path):
    import base64
    return "sha384-" + base64.b64encode(hashlib.sha384(open(path, "rb").read()).digest()).decode()


PACK_README = """Amplify graphics pack: UK Parliament Week 2026

Free to use and remix with credit to Amplify (CC BY 4.0). Everything is drawn in code from the portal's six shapes
and four hues, with no photographs. Open any .svg in a web browser to view it, print it (A4, no margins) or save it
as PDF. Fonts are built in.

print/     A4 posters, the sticker sheet, the social card and the ambassador badge
platform/  hero-16x9 (email, Viva Engage, Slack, Bluesky, X), header-3x1 (Teams announcement),
           linkedin-1200x627, portrait-1080x1350 (Instagram, LinkedIn), story-1080x1920 (Stories, TikTok, Reels),
           carousel-1 to carousel-6 (Instagram or LinkedIn carousel, 4:5)

Every QR code opens the live portal. Amplify is independent and unofficial: not a service of the
UK Youth Parliament, NYA or UK Parliament. Contact: use the contact form on the portal.
"""


def graphics_pack(arts, path):
    """The Campaign kit's downloadable pack: a deterministic zip (fixed dates, sorted names) so S1 can rebuild it
    byte for byte. Added 16 Nov 2026: the kit offered each graphic one at a time and no pack (owner's request)."""
    import zipfile
    import campaign_art
    files = {f"print/{n}": s for n, s in arts.items() if n in CAMPAIGN_FILES}
    files.update({f"platform/{n}": s for n, s in campaign_art.pack().items()})
    files["README.txt"] = PACK_README
    # Stored, not deflated: deflate output depends on the zlib version, so CI rebuilt different bytes (D33)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_STORED) as z:
        for n in sorted(files):
            info = zipfile.ZipInfo("amplify-graphics-pack/" + n, date_time=(2026, 11, 16, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o644 << 16
            z.writestr(info, files[n])


CAMPAIGN_FILES = ("poster-involve.svg", "poster-stem.svg", "poster-careers.svg", "poster-remix.svg", "sticker-sheet.svg",
                  "social-card.svg", "badge-ambassador.svg")


# Link previews: without these, every share on LinkedIn, Teams, Viva Engage or Slack showed no image (D34, 16 Nov 2026)
SHARE_TAGS = '<meta property="og:type" content="website">\n<meta property="og:site_name" content="Amplify">\n<meta property="og:title" content="Amplify: youth voice, carried further">\n<meta property="og:description" content="A free, independent and unofficial portal that helps young people across the UK be heard: trusted sources, safe ways to take part and campaign tools. Launches in UK Parliament Week, 23 to 29 November 2026.">\n<meta property="og:url" content="https://cyberdudeuk.github.io/uk-youth-parliament-amplify/site/index.html">\n<meta property="og:image" content="https://cyberdudeuk.github.io/uk-youth-parliament-amplify/site/media/campaign/share-card.jpg">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:image:alt" content="Amplify. Youth voice, carried further. Launches Monday 23 November 2026, UK Parliament Week. Special mentions: STEM, girls and young women in tech, Government Digital and Data careers. Independent and unofficial.">\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:image:alt" content="Amplify. Youth voice, carried further. Launches Monday 23 November 2026, UK Parliament Week. Special mentions: STEM, girls and young women in tech, Government Digital and Data careers. Independent and unofficial.">\n'


def build(date, out=SITE):
    src = json.load(open(os.path.join(R, "tools", "sources.json"), encoding="utf-8"))
    pet = json.load(open(os.path.join(APP, "petition-754954.json"), encoding="utf-8"))
    h = hashlib.sha256()
    for f in sorted(src["files"]):
        h.update(f.encode()); h.update(open(os.path.join(R, f), "rb").read())
    for f in ["tools/build_site.py", "tools/art.py", "tools/extend.py", "tools/extend2.py", "tools/extend3.py", "tools/extend4.py", "tools/extend5.py", "tools/extend6.py", "tools/extend7.py", "tools/extend8.py", "tools/extend9.py", "tools/extend10.py", "tools/make_docs.py", "vendor/VENDOR.json"] + sorted("data/" + n for n in os.listdir(DATA)):
        h.update(f.encode()); h.update(open(os.path.join(R, f), "rb").read())
    digest = h.hexdigest()
    d = datetime.date.fromisoformat(date)
    pd = datetime.date.fromisoformat(pet["fetched"])
    meta = {"build_id": f"AMP-{d:%Y%m%d}-{digest[:8]}", "built": date, "built_long": f"{d.day} {d:%B %Y}",
            "petition_date_long": f"{pd.day} {pd:%B %Y}", "inputs_sha256": digest,
            "review": (d + datetime.timedelta(days=30)).isoformat(),
            "n_sources": len(json.load(open(os.path.join(DATA, "youth-sources.json"), encoding="utf-8"))["sources"]),
            "n_latest": len(json.load(open(os.path.join(DATA, "latest.json"), encoding="utf-8"))["items"])}
    rv = datetime.date.fromisoformat(meta["review"]); meta["review_long"] = f"{rv.day} {rv:%B %Y}"
    for f in sorted(os.listdir(DATA)):  # B3: every data file parses
        try: json.load(open(os.path.join(DATA, f), encoding="utf-8"))
        except Exception as e: raise BuildError(f"B3 data/{f} is not valid JSON: {e}") from e

    # Every vendored file is the file VENDOR.json recorded, and the runtime is the bytes the design pinned (B2).
    ven = json.load(open(os.path.join(VENDOR, "VENDOR.json"), encoding="utf-8"))["files"]
    for f, rec in ven.items():
        got = sri(os.path.join(VENDOR, f))
        if got != rec["sha384"]:
            raise BuildError(f"B2 vendor/{f} changed since it was vendored: {got} where VENDOR.json records {rec['sha384']}")
    support = open(os.path.join(APP, "support.js"), encoding="utf-8").read()
    for f in ("runtime/react.production.min.js", "runtime/react-dom.production.min.js", "runtime/babel.min.js"):
        if ven[f]["sha384"] not in support:
            raise BuildError(f"B2 vendor/{f} is not the file the design's runtime pins by SRI")

    # Leaflet: the vendored bytes must be the bytes the design pinned by SRI (B2).
    pinned = {"leaflet.css": "sha384-sHL9NAb7lN7rfvG5lfHpm643Xkcjzp4jFvuavGOndn6pjVqS6ny56CAt3nsEVT4H",
              "leaflet.js": "sha384-cxOPjt7s7Iz04uaHJceBmS+qpjv2JkIHNVcuOrM+YHwZOmJGBXI00mdUXEq65HTH"}
    for f, want in pinned.items():
        got = sri(os.path.join(VENDOR, "leaflet-1.9.4", f))
        if got != want:
            raise BuildError(f"B2 vendor/leaflet-1.9.4/{f} is not the pinned file: {got} where the design pins {want}")

    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(os.path.join(out, "art")); os.makedirs(os.path.join(out, "vendor", "leaflet-1.9.4"))
    log = []

    def apply(text, ts):
        for name, why, old, new, n in ts:
            text = sub(text, name, old, new, n); log.append({"name": name, "why": why, "matches": n})
        return text

    portal = apply(open(os.path.join(APP, PORTAL_SRC), encoding="utf-8").read(), transforms(meta))
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(portal)
    mp = apply(open(os.path.join(APP, MAP_SRC), encoding="utf-8").read(), map_transforms())
    open(os.path.join(out, MAP_SRC), "w", encoding="utf-8").write(mp)
    for f in ("support.js", "petition-754954.json"):
        shutil.copyfile(os.path.join(APP, f), os.path.join(out, f))
    for f, to in (("leaflet.css", "leaflet.css"), ("leaflet.js", "leaflet.js"), ("LICENSE", "LICENSE.txt")):  # .txt: hosts serve files by extension
        shutil.copyfile(os.path.join(VENDOR, "leaflet-1.9.4", f), os.path.join(out, "vendor", "leaflet-1.9.4", to))
    shutil.copyfile(os.path.join(VENDOR, "outline.json"), os.path.join(out, "vendor", "outline.json"))
    for f in ven:  # runtime, fonts and icons; the test-only axe file stays out of the site
        if f.startswith("test/"): continue
        os.makedirs(os.path.join(out, "vendor", os.path.dirname(f)), exist_ok=True)
        shutil.copyfile(os.path.join(VENDOR, f), os.path.join(out, "vendor", f))
    shutil.copyfile(os.path.join(VENDOR, "fonts", "fonts.css"), os.path.join(out, "vendor", "fonts", "fonts.css"))
    media = os.path.join(R, "media")  # campaign films and their poster frames (owner asked for them on the portal, 16 Nov 2026)
    for d, _, names in os.walk(media):
        for n in sorted(names):
            rel = os.path.relpath(os.path.join(d, n), media)
            os.makedirs(os.path.join(out, "media", os.path.dirname(rel)), exist_ok=True)
            shutil.copyfile(os.path.join(d, n), os.path.join(out, "media", rel))
    os.makedirs(os.path.join(out, "data"))
    for f in sorted(os.listdir(DATA)):
        shutil.copyfile(os.path.join(DATA, f), os.path.join(out, "data", f))

    arts = {"hero.svg": art.hero(), "favicon.svg": art.favicon()}
    for n in art.HUE:
        arts[f"{n}.svg"] = art.corner(n)
    import segno, barcode
    from barcode.writer import SVGWriter
    qr_inline = segno.make(LIVE_URL, error="m").svg_inline(scale=3, border=0, dark="#06100f", light="#ffffff")  # posters send people to the live portal
    arts.update({"poster-involve.svg": art.poster_involve(qr_inline), "poster-stem.svg": art.poster_stem(qr_inline),
                 "poster-careers.svg": art.poster_careers(qr_inline), "poster-remix.svg": art.poster_remix(qr_inline),
                 "social-card.svg": art.social_card(), "badge-ambassador.svg": art.badge_ambassador(), "sticker-sheet.svg": art.sticker_sheet()})
    for f, s in arts.items():
        open(os.path.join(out, "art", f), "w", encoding="utf-8").write(s)
    graphics_pack(arts, os.path.join(out, "art", "amplify-graphics-pack.zip"))
    segno.make(REPO_URL, error="m").save(os.path.join(out, "art", "qr.svg"), scale=4, border=2, dark="#06100f", light="#ffffff")
    buf = io.BytesIO()
    barcode.get("code128", meta["build_id"], writer=SVGWriter()).write(buf, {"module_height": 12, "font_size": 6, "text_distance": 3, "quiet_zone": 2})
    open(os.path.join(out, "art", "barcode.svg"), "wb").write(buf.getvalue())

    for name, text in (("feed.xml", extend9.feed(meta)), ("glossary-skos.json", extend9.skos(meta))):  # Atom feed; SKOS vocabulary
        with open(os.path.join(out, name), "w", encoding="utf-8") as f:
            f.write(text)

    files = {}
    for root, _, names in os.walk(out):
        for n in sorted(names):
            p = os.path.join(root, n); rel = os.path.relpath(p, out).replace(os.sep, "/")
            files[rel] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    manifest = {"what": "The published Amplify portal, built from the design files in app/ by tools/build_site.py",
                **meta, "design_artifact": src["artifact"], "repository": REPO_URL, "checks": rule_ids(),
                "transforms": log, "files": dict(sorted(files.items()))}  # sorted: directory order differs by filesystem (D9)
    open(os.path.join(out, "build.json"), "w", encoding="utf-8").write(json.dumps(manifest, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    a = ap.parse_args()
    try:
        m = build(a.date)
        make_docs.write()
    except BuildError as e:
        sys.exit(str(e))
    print(f"built {m['build_id']}: {len(m['transforms'])} transforms, {len(m['files'])} files in site/")
