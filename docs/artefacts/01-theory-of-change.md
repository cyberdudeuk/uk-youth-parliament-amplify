---
artefact:id: P14-TOC-001
artefact:version: 1.0.0
artefact:as-of: 2026-11-20
artefact:review-date: 2027-02-20
project: P14 Amplify youth voice portal
grade: G4
profile: public sector > personal public good (audience includes under-18s)
---

# Theory of change: Amplify youth voice portal

> **How to read this.** Facts marked V were read from this repository on 20 November 2026. Assumptions, measures and risks are proposals written for this kit, not findings. U means unconfirmed. Where another document in this repository already covers a topic, this one links to it rather than repeating it.

## Problem
Young people's issues and the routes to raise them locally are scattered, so many young people don't know how their voice can reach decision makers.

## Long-term outcome
More young people find a local route to raise an issue, safely.

## Chain

| Inputs | Activities | Outputs | Short-term outcomes | Medium-term outcomes |
|---|---|---|---|---|
| The portal design (app/); a dated UK Parliament petition snapshot; local routes data; safeguards, help and launch data (data/) | Publish the issues young people raise, a local routes map, a petition snapshot and ways to get involved; run a campaign kit | site/ built from app/ by tools/build_site.py; data/ as single source; research bundle (plans only) | Visitors find a local route and the campaign kit during UK Parliament Week | Ambassadors and champions sustain local activity |

## Assumptions (proposed; each one testable)

| # | Assumption | How to test it | Evidence today |
|---|---|---|---|
| A1 | A map of local routes helps young people act | Research round 1, after gate G06 | Not tested |
| A2 | No personal data is needed to use the portal | DPIA screening | Stated design intent (U) |

## Measures (proposed)
- Safeguarding gate G06 met before any research or sign-up (gate)
- Petition snapshot shows its date (check_sources)
- Accessibility checks pass (check_browser)

No target is set before a baseline exists.

## What would prove this wrong
If young people go to existing UK Youth Parliament channels instead, turn Amplify into a signposting page to them.

## Status
Launching at UK Parliament Week, 23 to 29 Nov 2026; research paused until gate G06 (V: README, docs/research). Live site: https://cyberdudeuk.github.io/uk-youth-parliament-amplify/
