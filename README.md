# UK Youth Parliament: Amplify portal

A youth voice portal: young people's issues, a local routes map, and a dated
snapshot of a UK Parliament petition.

This repository holds the portal as its own project. It sits outside the
govukOS ecosystem by decision: it is public and written for young people. It
may reuse govukOS's shared page runtime, but it is not a govukOS app.

## What is here

| Path | What it is |
|---|---|
| `app/Amplify Portal.dc.html` | The portal |
| `app/Local Routes Map.html` | The local routes map |
| `app/support.js`, `app/image-slot.js` | The page runtime the portal loads |
| `app/petition-754954.json` | A snapshot of UK Parliament petition 754954, with the date it was taken (see below) |
| `tools/check_repo.py` | The repository's checks (run by CI on every push) |

The portal files are copied byte for byte from the private Claude artifact
they were built in. Each copy is checked against that artifact's SHA-256 (see
`tools/sources.json`).

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
