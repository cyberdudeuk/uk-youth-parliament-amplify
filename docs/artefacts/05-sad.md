---
artefact:id: P14-SAD-001
artefact:version: 1.0.0
artefact:as-of: 2026-11-20
artefact:review-date: 2027-02-20
project: P14 Amplify youth voice portal
grade: G4
profile: public sector > personal public good (audience includes under-18s)
---

# Solution architecture (SAD): Amplify youth voice portal

> **How to read this.** Facts marked V were read from this repository on 20 November 2026. Assumptions, measures and risks are proposals written for this kit, not findings. U means unconfirmed. Where another document in this repository already covers a topic, this one links to it rather than repeating it.

## Context
Young people's issues and the routes to raise them locally are scattered, so many young people don't know how their voice can reach decision makers.

The solution is described in [docs/product.md](../../docs/product.md). It connects with: UK Parliament petitions; govukOS shared page runtime.

## Architecturally significant decisions
These are the decisions already recorded in this repository (V):

- [0001-build-the-portal-from-the-design.md](../adr/0001-build-the-portal-from-the-design.md)

## Quality attributes

| Attribute | How it is met |
|---|---|
| Leaflet 1.9.4 vendored with SRI | Leaflet 1.9.4 vendored with SRI |
| WCAG 2.2 AA | WCAG 2.2 AA (docs/accessibility.md) |
| Content CC BY 4.0 | Content CC BY 4.0 (personal project) |
| Contact | By form only; no email address anywhere (estate rule) |
| Documentation | This kit, checked in CI by `tools/artefact_check.py` |

## Constraints
- Launching at UK Parliament Week, 23 to 29 Nov 2026; research paused until gate G06 (V: README, docs/research).
- No personal data unless a DPIA has been done first.
- Contact by form only.

## Risks (proposed ratings)

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Harm to a young person through contact or research | Low | Very high | Gate G06; DPIA; no personal data |
| Petition data out of date | Medium | Low | Snapshot date shown |
