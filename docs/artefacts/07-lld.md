---
artefact:id: P14-LLD-001
artefact:version: 1.0.0
artefact:as-of: 2026-11-20
artefact:review-date: 2027-02-20
project: P14 Amplify youth voice portal
grade: G4
profile: public sector > personal public good (audience includes under-18s)
---

# Low-level design (LLD): Amplify youth voice portal

> **How to read this.** Facts marked V were read from this repository on 20 November 2026. Assumptions, measures and risks are proposals written for this kit, not findings. U means unconfirmed. Where another document in this repository already covers a topic, this one links to it rather than repeating it.

## Build and check commands (V: README)
```
python3 -I tools/build_site.py
python3 -I tools/check_site.py
python3 -I tools/check_repo.py
```

## Scripts (V: file tree)
- `tools/art.py`
- `tools/build_site.py`
- `tools/campaign_art.py`
- `tools/check_browser.py`
- `tools/check_repo.py`
- `tools/check_site.py`
- `tools/check_sources.py`
- `tools/extend.py`
- `tools/extend10.py`
- `tools/extend11.py`
- `tools/extend12.py`
- `tools/extend13.py`
- `tools/extend14.py`
- `tools/extend2.py`
- `tools/extend3.py`
- `tools/extend4.py`
- `tools/extend5.py`
- `tools/extend6.py`
- `tools/extend7.py`
- `tools/extend8.py`
- `tools/extend9.py`
- `tools/follow_ups.py`
- `tools/make_docs.py`
- `tools/make_outline.py`
- `tools/vendor_assets.py`

## Tests (V: file tree)
- No test files found. Adding tests is an open item.

## Workflows (V: .github/workflows)
- `checks.yml`
- `codeql.yml`
- `dependency-review.yml`
- `follow-ups.yml`
- `health.yml`
- `issue-ack.yml`
- `scorecard.yml`

## Repository size
377 files tracked on 20 November 2026.

## Documentation kit
- `docs/artefacts/manifest.yaml` lists every core document, where it is, and its review date.
- `tools/artefact_check.py` checks the kit (rules AC-01 to AC-08, each with a negative test). Run `python3 tools/artefact_check.py --self-test` then `python3 tools/artefact_check.py .`.

## Handover
Someone new can rebuild and verify with the commands above, then read [docs/product.md](../../docs/product.md) and [05-sad.md](05-sad.md).
