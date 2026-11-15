# UK Youth Parliament: Amplify portal

A youth voice portal: young people's issues, a local routes map, and a dated
snapshot of a UK Parliament petition.

This repository holds the portal as its own project. It sits outside the
govukOS ecosystem by decision: it is public and written for young people. It
may reuse govukOS's shared page runtime, but it is not a govukOS app.

## What is here

| Path | What it is |
|---|---|
| `app/Amplify Portal.dc.html` | The portal, as designed (the design source, byte for byte) |
| `app/Local Routes Map.html` | The local routes map |
| `app/support.js`, `app/image-slot.js` | The page runtime the portal loads |
| `app/petition-754954.json` | A snapshot of UK Parliament petition 754954, with the date it was taken (see below) |
| `site/` | The published portal, built from `app/` by `tools/build_site.py`. Never edit it by hand |
| `vendor/` | Leaflet 1.9.4 (the bytes the design pinned by SRI) and the land outline the map draws |
| `tools/build_site.py`, `tools/art.py` | The build: each design-to-page transform is named, with its reason, in `site/build.json` |
| `data/` | The single source of truth for sources, updates, safeguards, help, launch, integrity, registers and the release log |
| `tools/check_repo.py`, `tools/check_site.py`, `tools/check_sources.py`, `tools/check_browser.py` | Repository, site, content and real-browser checks (CI on every push; weekly health run) |
| `SECURITY.md` | How to report a security problem privately, and the automated security checks |
| `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` | How to take part, and the conduct expected |
| `.github/workflows/` | CI: the repository checks, CodeQL, dependency review and OpenSSF Scorecard |
| `.github/dependabot.yml` | Weekly updates for the pinned GitHub Actions |

The portal files are copied byte for byte from the private Claude artifact
they were built in. Each copy is checked against that artifact's SHA-256 (see
`tools/sources.json`).

## What the portal covers

Campaign planning around petition 754954, plus: a directory of trusted official and voluntary-sector sources for
young people, parents and carers and adult allies across all four UK nations; dated updates; safeguards, frameworks
and audiences (including d/Deaf young people and every UK official and sign language); help, tutorials and guided
tours; an idea and bug box; a release log; a self-checking Portal health screen; and the plan to launch at
UK Parliament Week, 23 to 29 November 2026. Where content is a sample, a planning model or generated text, the screen
says so and why.

See `docs/maintenance.md` for the self-routines and upkeep, `docs/accessibility.md` for the accessibility statement,
`docs/registers.md` for defects and open items, and `CHANGELOG.md` for the release log.

## Build and publish

```sh
pip install -r tools/requirements.txt
python3 -I tools/build_site.py      # app/ -> site/
python3 -I tools/check_site.py      # S1-S8, each proved by a negative test
python3 -m http.server --directory site 8000
```

The build turns the design canvas into a page that can be sent: it opens on
the portal rather than the side-by-side review view, replaces the six image
drop-zones with illustrations drawn from the brand's six primitives, says on
the splash, the masthead and the footer that this is an unofficial prototype,
labels the five seed pledges as invented samples, adds the footer (disclaimers,
disclosures, transparency, contact form, barcode and QR colophon), connects the
copilot to the published host's model capability, and gives the map a local
land outline (the design's CARTO street tiles now return "API key required"
images). `site/` is published as a private Claude artifact.

## Not here, by rule

- **Decks and films.** They are not kept in any repository unless the owner
  says so for that piece. This portal has none.
- **Blueprints and input files.** They are not kept once every feature they
  describe is built.
- **Email addresses and personal contact details.** Contact is by the issue
  form only ([open a contact issue](../../issues/new/choose)).

`tools/check_repo.py` enforces all three, and it fails on purpose against a
deliberately broken copy to prove each rule bites (its negative tests).

## Run it

Open `app/Amplify Portal.dc.html` from a local web server, because the page
loads its runtime and data with relative paths:

```sh
python3 -m http.server --directory app 8000
# then open http://localhost:8000/Amplify%20Portal.dc.html
```

## Data and licences

- **Code:** MIT (`LICENSE`).
- **Written content and images:** see `LICENCE-CONTENT.md`.
- **Petition data:** UK Parliament e-petitions data, which Parliament publishes
  under the Open Parliament Licence v3.0 (UK Parliament's dataset certificate
  for e-petitions; some reusers cite the Open Government Licence, so confirm
  on petition.parliament.uk before relying on it). The file is not Parliament's
  record itself: it is a summary made from that record (signature totals, the
  count by nation, region and constituency, and the named MPs, who are public
  office holders), and it names its own source URL. It was fetched on
  1 October 2026 (its `fetched` field, also recorded in `tools/sources.json`).
  The petition closed on 11 August 2026, so its counts are final. The summary is
  kept byte for byte as the portal uses it. Contains Parliamentary information
  licensed under the Open Parliament Licence v3.0.

## Checks

```sh
python3 -I tools/check_repo.py
```
