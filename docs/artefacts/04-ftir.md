---
artefact:id: P14-FTIR-001
artefact:version: 1.0.0
artefact:as-of: 2026-11-20
artefact:review-date: 2027-02-20
project: P14 Amplify youth voice portal
grade: G4
profile: public sector > personal public good (audience includes under-18s)
---

# Functional, technical and integration requirements (FTIR): Amplify youth voice portal

> **How to read this.** Facts marked V were read from this repository on 20 November 2026. Assumptions, measures and risks are proposals written for this kit, not findings. U means unconfirmed. Where another document in this repository already covers a topic, this one links to it rather than repeating it.

Requirements are stated once, in [docs/product.md](../../docs/product.md). This document says how each is met and checked.

## Functional

| ID | Requirement | Priority | Verified by | State |
|---|---|---|---|---|
| F01 | Build the portal from the design byte for byte (ADR 0001) | Must | tools/check_site.py | Has a check |
| F02 | Local routes map | Must | tools/check_browser.py | Has a check |
| F03 | Petition snapshot carries the date taken | Must | tools/check_sources.py | Has a check |
| F04 | data/ is the single source for sources, updates, safeguards, help and launch | Must | tools/check_repo.py | Has a check |
| F05 | No sign-up or research until a named safeguarding lead and written procedure exist (gate G06) | Must | Gate in docs/go-live.md (U: confirm a check enforces it) | Check named; coverage unconfirmed (U) |
| F06 | Contact by form only | Must | tools/check_repo.py (U) | Check named; coverage unconfirmed (U) |

## Technical

| ID | Requirement | State |
|---|---|---|
| T01 | Code scanning | Present (V: .github/workflows) |
| T02 | Dependency review on pull requests | Present (V: .github/workflows) |
| T03 | OpenSSF Scorecard | Present (V: .github/workflows) |
| T04 | Automated release | Not present |
| T05 | Published by workflow (Pages) | Not present |
| T06 | Documentation kit checked in CI | Present (V: .github/workflows) |

Workflows present (V): `checks.yml`, `codeql.yml`, `dependency-review.yml`, `follow-ups.yml`, `health.yml`, `issue-ack.yml`, `scorecard.yml`.

Tests present (V): none found.

## Integration

| ID | Integration | Direction | State |
|---|---|---|---|
| I01 | UK Parliament petitions | Dated snapshot | Live |
| I02 | govukOS shared page runtime | May reuse; not a govukOS app | By decision |
