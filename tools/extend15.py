"""Fifteenth set of portal extensions: compile at build time, not in the browser (20 November 2026, O16, D48).

  What O16 assumed: the page compiled itself in the browser with Babel on every visit, which is what made it slow on
  low-end phones.

  What a profile on a phone-class CPU (4x slowdown, 390x844) showed on 20 November 2026:
    - Babel (3,137,752 bytes) was shipped but never requested: no screen uses a JSX import, so the browser never
      compiled anything with it. Shipping it cost nothing on load, but it kept a 3 MB compiler in the site and, if a
      JSX import were ever added, the runtime would fetch and run it on every visit.
    - About 1.0 s went on parsing the 885 KB page and its script, about 0.5 s on the runtime's own template
      compiler, and 146 ms on a single function, ampDate, which built a new date formatter on every call.

  What this release does
    compile   Babel is no longer shipped. The runtime's Babel slot points at a 1-line local stub that throws, so a
              JSX import would fail loudly in testing instead of quietly fetching a compiler from a CDN (fail closed).
    format    dates and numbers use one cached Intl formatter each, built once per page load, with dates also cached
              by value.
    check     check_site S24 fails if Babel is shipped again, if the Babel slot points anywhere but the stub, if the
              page gains a JSX import or a text/babel script, or if a per-call toLocaleDateString comes back.

  What it does not do: precompile the runtime's templates. That means rewriting the vendored runtime, which is not
  safe three days before launch; W7 keeps measuring, and the remaining cost is recorded on O16.
"""

STUB_NAME = "no-in-browser-compiler.js"
STUB = ("/* Amplify compiles at build time (O16, D48). Nothing on this site should ask for an in-browser compiler. */\n"
        "throw new Error(\"Amplify: an in-browser compiler was requested; this site compiles at build time (O16)\");\n")

BABEL_MAP_OLD = '"https://unpkg.com/@babel/standalone@7.29.0/babel.min.js": "./vendor/runtime/babel.min.js"'
BABEL_MAP_NEW = '"https://unpkg.com/@babel/standalone@7.29.0/babel.min.js": "./vendor/runtime/' + STUB_NAME + '"'

DATE_OLD = ('  ampDate(d) { const t = new Date(String(d) + "T00:00:00Z"); return isNaN(t) ? String(d) : '
            't.toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric", timeZone: "UTC" }); }')
DATE_NEW = ('  ampDate(d) {\n'
            '    const k = String(d), C = this._ampDates || (this._ampDates = new Map());\n'
            '    if (C.has(k)) return C.get(k);\n'
            '    const F = this._ampDateFmt || (this._ampDateFmt = new Intl.DateTimeFormat("en-GB", { day: "numeric", month: "short", year: "numeric", timeZone: "UTC" }));\n'
            '    const t = new Date(k + "T00:00:00Z"), out = isNaN(t) ? k : F.format(t);\n'
            '    C.set(k, out); return out;\n'
            '  }')

FMT_OLD = 'const fmt = (n) => n.toLocaleString("en-GB");'
FMT_NEW = 'const __ampNum = new Intl.NumberFormat("en-GB");\nconst fmt = (n) => __ampNum.format(n);'


def transforms():
    return [
        ("ext15-no-babel", "O16, D48: the in-browser compiler is not shipped; the runtime's Babel slot points at a local stub that throws",
         BABEL_MAP_OLD, BABEL_MAP_NEW, 1),
        ("ext15-date", "D48: dates are formatted by one cached Intl formatter, and each value once, instead of a new formatter per call",
         DATE_OLD, DATE_NEW, 1),
        ("ext15-fmt", "D48: numbers are formatted by one cached Intl formatter",
         FMT_OLD, FMT_NEW, 1),
    ]
