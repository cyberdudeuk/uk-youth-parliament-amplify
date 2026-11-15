# Defect and open registers

Generated from `data/registers.json` by `tools/make_docs.py`; shown live on the portal's Portal health screen.

## Defects found and fixed

| Id | Found | What | Root cause | Fix | Check |
|---|---|---|---|---|---|
| D1 | 2026-11-15 | Six design-time image drop-zones would have shipped ('Drop the UKYP or partner logo'). | The design canvas was published as-is. | Build replaces them with illustrations. | S2 |
| D2 | 2026-11-15 | The map's CARTO tiles return 'API key required' images, so its own failure note never showed. | The tile host now needs a key and answers with a 200 image. | Local land outline is the basemap. | S7 |
| D3 | 2026-11-15 | Safeguarding listed HOPELINE247, which closed on 7 September 2026. | Helplines were fixed in the design with no re-verification cadence. | Removed; helplines now carry a checked date and a 30-day review. | S9, C3 |
| D4 | 2026-11-15 | Safeguarding gave The Mix's phone number; its phone helpline has closed. | As D3. | Replaced with its 24/7 text route (THEMIX to 85258). | S9, C3 |
| D5 | 2026-11-15 | The page loaded React, Babel and fonts from unpkg and Google, exposing every visitor's IP address. | The design runtime defaults to CDNs. | Vendored, SRI-verified files served by the portal itself. | S10, B2 |
| D6 | 2026-11-15 | Moving the first build between clones as a patch changed the vendored Leaflet stylesheet's bytes. | Text patches normalise whitespace; vendored files must be byte-exact. | Restored from the package; .gitattributes marks vendor/, site/ and app/ as binary. | B2 |
| D7 | 2026-11-15 | After fonts and scripts were self-hosted, the footer still said they loaded from Google Fonts and unpkg. | The disclosure was hand-written copy with no check tying it to how the page actually loads. | Disclosure rewritten. | S3 |
| D8 | 2026-11-15 | R6 and S6 read a share link being built in JavaScript (href=" + u + ") as a missing file. | The link pattern matched inside script strings. | Both checks skip values that are string concatenations; their negative tests still catch a real missing file. | R6, S6 |
| D9 | 2026-11-15 | CI rebuilt site/build.json with its file list in a different order, so S1 failed on GitHub but passed locally. | The file list followed the filesystem's directory order, which differs between machines. | The file list is sorted. | S1 (caught it in CI) |
| D10 | 2026-11-15 | The outbound-host checks S7 and S9 missed upper-case or spaced tags such as <SCRIPT SRC=...>, so a remote script could have slipped past. Found by GitHub's code scanning. | The patterns were case-sensitive and expected src= with no spaces. | S7 and S9 ignore case and spacing, and S9 also covers img and iframe tags. | S7 and S9, with three new negative tests |

## Open, and who must act

| Id | What | Who |
|---|---|---|
| O1 | No research with young people or disabled users has tested this portal. | Owner, with NYA or a youth panel |
| O2 | Search-sourced (S) and knowledge (K) links are leads until the weekly link check confirms them. | Automated weekly health check; owner reviews the issue |
| O3 | Pre-existing accessibility findings in the original design are tracked as a baseline and must not grow. | Maintainer |
| O4 | Housing, transport, climate and justice sources are not yet vetted. | Maintainer |
| O5 | Easy Read and BSL versions need specialist production. | Owner |
| O6 | Publishing beyond a private artifact (for example GitHub Pages) is the owner's decision. | Owner |
| O7 | Framework entries labelled K (background knowledge) are to be checked against each primary text. | Maintainer, on the next scheduled run with page access |
| O8 | Revise the Toolkit's social media assets for under 16s before the ban applies in spring 2027. | Maintainer, with UKYP input |
| O9 | A line-by-line audit of every figure in the original design's screens against its source; screens are classified, but individual figures not yet re-verified are the design's own. | Maintainer, one screen per weekly run |
| O10 | BSL and ISL versions of key screens, and Welsh, Gaelic and Irish versions of the portal, need deaf-led and native-speaker production. | Owner, with deaf-led organisations and language bodies |
| O11 | Before public launch, the owner confirms that publishing a personal, non-partisan youth participation tool under his own name raises no propriety issue with his employer. | Owner |
