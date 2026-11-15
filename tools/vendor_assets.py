"""Vendor the portal's third-party files into vendor/, and record what they are in vendor/VENDOR.json.

Why: the build standard asks for self-contained pages with no runtime dependency on another host. The design loads
React, ReactDOM and Babel from unpkg and its fonts from Google Fonts; for a portal written for young people, a page
that tells Google and unpkg every visitor's IP address is a cost with no benefit. Run once per upgrade:
    python3 -I tools/vendor_assets.py <dir where the npm tarballs were unpacked, one folder per package>
Every file is recorded with its package, version, licence and SHA-384; build_site.py refuses to build if a vendored
file no longer matches (B2), and React, ReactDOM and Babel must equal the bytes the design pinned by SRI.
"""
import base64, hashlib, json, os, shutil, sys

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(R, "vendor")
ICONS = ("scale route landmark layers compass megaphone trending-up calendar-range handshake package hand-heart radar "
         "scroll-text map graduation-cap messages-square file-search list-checks users accessibility library sparkles "
         "palette heart-handshake network book-open-check newspaper activity vote shield-check heart-pulse briefcase "
         "chart-column chart-line coins life-buoy search external-link circle-check triangle-alert clock refresh-cw bug "
         "list-todo git-branch filter globe info circle-alert flag-triangle-right").split()
FONTS = {"chivo": ["300", "400", "400-italic", "600", "700", "900"], "space-mono": ["400", "700"],
         "atkinson-hyperlegible": ["400", "700"]}
FAMILY = {"chivo": "Chivo", "space-mono": "Space Mono", "atkinson-hyperlegible": "Atkinson Hyperlegible"}


def sri(p):
    return "sha384-" + base64.b64encode(hashlib.sha384(open(p, "rb").read()).digest()).decode()


def main(src):
    rec = {"what": "Third-party files the published portal serves itself. Regenerate with tools/vendor_assets.py.", "files": {}}
    def put(pkg_dir, rel, to, pkg, ver, lic):
        a = os.path.join(src, pkg_dir, "package", rel); b = os.path.join(V, to)
        os.makedirs(os.path.dirname(b), exist_ok=True); shutil.copyfile(a, b)
        rec["files"][to] = {"package": pkg, "version": ver, "licence": lic, "sha384": sri(b)}
    for pkg, ver, f in (("react", "18.3.1", "umd/react.production.min.js"), ("react-dom", "18.3.1", "umd/react-dom.production.min.js")):
        put(f"{pkg}-{ver}", f, f"runtime/{os.path.basename(f)}", pkg, ver, "MIT")
        put(f"{pkg}-{ver}", "LICENSE", f"runtime/LICENSE-{pkg}.txt", pkg, ver, "MIT")
    put("babel-standalone-7.29.0", "babel.min.js", "runtime/babel.min.js", "@babel/standalone", "7.29.0", "MIT")
    put("babel-standalone-7.29.0", "LICENSE", "runtime/LICENSE-babel.txt", "@babel/standalone", "7.29.0", "MIT")
    css = ["/* Fonts served by the portal itself (latin subset). Licences: fonts/LICENSE-*.txt (SIL OFL 1.1). */"]
    for fam, styles in FONTS.items():
        d = f"fontsource-{fam}-5.3.0"
        put(d, "LICENSE", f"fonts/LICENSE-{fam}.txt", f"@fontsource/{fam}", "5.3.0", "OFL-1.1")
        for st in styles:
            w, ital = (st.split("-")[0], "italic" if st.endswith("italic") else "normal")
            fn = f"{fam}-latin-{w}-{ital}.woff2"
            put(d, f"files/{fn}", f"fonts/{fn}", f"@fontsource/{fam}", "5.3.0", "OFL-1.1")
            css.append(f"@font-face{{font-family:'{FAMILY[fam]}';font-style:{ital};font-weight:{w};font-display:swap;src:url(./{fn}) format('woff2');}}")
    open(os.path.join(V, "fonts", "fonts.css"), "w", encoding="utf-8").write("\n".join(css) + "\n")
    lv = "1.66.0"
    for n in ICONS:
        put(f"lucide-static-{lv}", f"icons/{n}.svg", f"icons/{n}.svg", "lucide-static", lv, "ISC")
    put(f"lucide-static-{lv}", "LICENSE", "icons/LICENSE.txt", "lucide-static", lv, "ISC")
    put("axe-core-4.10.3", "axe.min.js", "test/axe.min.js", "axe-core", "4.10.3", "MPL-2.0")
    open(os.path.join(V, "VENDOR.json"), "w", encoding="utf-8").write(json.dumps(rec, indent=2, sort_keys=True) + "\n")
    print(len(rec["files"]), "files vendored")


if __name__ == "__main__":
    main(sys.argv[1])
