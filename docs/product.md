# Product: vision, strategy, roadmap and backlog

Generated from `data/product.json` by `tools/make_docs.py`; edit that, not this file. The portal shows the same content on its Product & roadmap screen.

Last checked 2026-11-17, reviewed every 30 days.

## Vision

Every young person in the UK knows how to make their voice heard, and is heard, safely.

**Mission:** Carry youth voice further: bring together trusted sources, safe routes into participation and campaign tools for young people, and for the adults who support them, across all four nations.

## Strategy

- **Trusted:** Every fact sourced and dated; models, samples and generated text labelled; checks that prove it on every change.
- **Safe:** Safeguarding first, no personal data, age-appropriate routes, adults acting on a young person's behalf where needed.
- **For everyone:** Accessible to WCAG 2.2 AA, pan-UK, every voice and language, including sign languages.
- **Built with its users:** User-centred design, open research, contributions and ambassadors, all in the open.
- **Looked after:** Self-checking, self-reporting and updated every week, with people deciding anything irreversible.

## Product specification

**What it is:** An independent, unofficial, open-source web portal about youth voice and participation in the UK.

**Who it is for:** Young people aged 11 to 25, parents and carers, youth workers, teachers, club leaders, and adult allies such as councillors, researchers and journalists.

In scope:

- Trusted sources and dated updates
- Routes into youth voice by age and nation
- Campaign planning and tools
- Safeguards, age and access rules
- Get involved: contribute, research, ambassadors, campaign kit, training, STEM and tech
- Self-checking and transparency

Out of scope:

- Collecting personal data or accounts
- Acting for, or speaking as, the UK Youth Parliament, NYA or UK Parliament
- Tracking or advertising
- Party-political positions

Constraints:

- No request to another host when a page loads
- Contact by form only, never an email address
- Everything generated from data; nothing hand-edited in the built site
- People decide merges and publishing

## Update schedule

| What | When | How |
|---|---|---|
| Helplines re-verified | Every 30 days, checked weekly | Weekly upkeep task |
| Sources re-verified | Every 90 days, in turn | Weekly upkeep task |
| What's new and the news ticker | Weekly, and straight away for anything safety-critical | Weekly upkeep task |
| Health checks and link check | Every Monday | GitHub Actions: health.yml |
| Follow-ups due | Every Monday | GitHub Actions: follow-ups.yml |
| Glossary, thesaurus, graph and tooltips | With every release that adds a term | data/glossary.json, enforced by S16 |
| Releases | When the owner merges a reviewed pull request | Release log and drawer flags |
| This page | Every 30 days | data/product.json |

## Roadmap

### Now

- Launch at UK Parliament Week (23 to 29 November 2026) (REQ-01, REQ-13)
- Owner decisions before going public: safeguarding lead and sign-off (merge, propriety and sharing decided) (REQ-25)

### Next

- Research round 1 with young people, parents and youth workers (January to February 2027) (REQ-16, REQ-17)
- Ambassador programme pilot, once safeguarding is confirmed (REQ-14)

### Later

- Welsh, Gaelic, Irish and sign-language versions of the most-used screens (REQ-08)
- Personas and journeys rewritten from research findings (REQ-17)
- Availability monitoring and a vendored-library watch (REQ-24)

## Requirements backlog

| Id | Requirement | MoSCoW | Status | From | Screens | Proved by |
|---|---|---|---|---|---|---|
| REQ-01 | Build and publish the portal from the original design | Must | Done | Owner, 15 Nov 2026 | home, hub | S1, R4 |
| REQ-02 | Trusted, authoritative youth sources, prioritised with MoSCoW | Must | Done | Owner, 15 Nov 2026 | sources | C1, C2 |
| REQ-03 | Maintenance and upkeep with self-routines | Must | Done | Owner, 15 Nov 2026 | health, golive | S8, S11 |
| REQ-04 | Professional iconography, visual effects and motion, with reduced motion respected | Should | Done | Owner, 15 Nov 2026 | home | W1, W6 |
| REQ-05 | Safeguards for every audience, including parents and carers | Must | Done | Owner, 15 Nov 2026 | trust, care | C3, C4, C5 |
| REQ-06 | User-centred, inclusive and accessible to all | Must | Done | Owner, 15 Nov 2026 | trust, service | W3, W7 |
| REQ-07 | Pan-UK coverage | Must | Done | Owner, 15 Nov 2026 | sources, map | C1 |
| REQ-08 | d/Deaf participation and all UK official and sign languages | Should | In progress | Owner, 15 Nov 2026 | trust | W3 |
| REQ-09 | New and changed flags, release log, ideas and bugs, manual, tours | Must | Done | Owner, 15 Nov 2026 | changes, help, feedback | S11 |
| REQ-10 | Label sample, model and generated content and say why; otherwise sourced content | Must | Done | Owner, 15 Nov 2026 | health | C9, S14 |
| REQ-11 | Social media ban, age-related access and adults acting on a young person's behalf | Must | Done | Owner, 15 Nov 2026 | trust | W4 |
| REQ-12 | Who is behind the portal, its purpose and outcomes | Must | Done | Owner, 15 Nov 2026 | about | S5 |
| REQ-13 | Home page, carousel, media centre, communities hub, sharing into everyday tools, map labels | Should | Done | Owner, 15 Nov 2026 | home, media, communities, launch | S9, W1 |
| REQ-14 | Tooltips for every persona; contribute, ambassadors, campaign kit, training, STEM | Should | Done | Owner, 15 Nov 2026 | involve, ambassadors, campaign, learn, stem | S12, W5, W8 |
| REQ-15 | Participation in research and design, ported from the owner's other portals | Should | Done | Owner, 15 Nov 2026 | research | S11 |
| REQ-16 | Run user research with young people | Should | Planned | Owner, 15 Nov 2026 | research | C9 |
| REQ-17 | Personas, stories, journeys, blueprints and workflows | Should | Done | Owner, 15 Nov 2026 | service | S13 |
| REQ-18 | Review and elevate the splash, phones and tablets; full pre-launch testing | Must | Done | Owner, 15 Nov 2026 | golive, home | W2, W6, S14, S15 |
| REQ-19 | Fix campaign kit viewing, printing and saving; independent drawer scrolling | Must | Done | Owner, 15 Nov 2026 | campaign, media | W8 |
| REQ-20 | Enterprise architecture, government professions, apprenticeships and schemes; science, innovation, data, digital, cyber and technology | Should | Done | Owner, 15 Nov 2026 | stem | C1 |
| REQ-21 | Glossary, thesaurus, graph and tooltips updated with every new term | Must | Done | Owner, 15 Nov 2026 | graph | S16 |
| REQ-22 | Transparent vision, strategy, roadmap and backlog, traced on GitHub with follow-up workflows; alerts; news ticker | Must | Done | Owner, 15 Nov 2026 | product, latest | S17, W9 |
| REQ-23 | Faster loading on low-end phones: compiled at build time, with no in-browser compiler shipped and cached formatters | Should | Done | Readiness review, 15 Nov 2026 | golive | S24, W7 |
| REQ-24 | Availability monitoring and vendored-library watch | Could | Planned | Readiness review, 15 Nov 2026 | golive | S15 |
| REQ-25 | Owner decisions before the public launch (publishing, merge and propriety decided 15 Nov 2026; safeguarding lead and owner sign-off still open) | Must | Waiting on owner | Readiness review, 15 Nov 2026 | golive | S15 |
| REQ-26 | The public address opens the built portal, labelled independent and unofficial | Must | Done | Gap review, 15 Nov 2026 | home, about | R8 |
| REQ-27 | Inside Parliament: how Parliament's time works, a day in the life of an MYP, an MP and a peer, who does what, the building and who changes the rules, every fact sourced | Should | Done | Owner request, 17 Nov 2026 | parliament | S21, S16, S12 |
| REQ-28 | Related themes to build next: the four nations' youth parliaments and legislatures, local democracy, registering to vote and elections, how a Bill becomes law, lobbying skills, careers in Parliament, heritage | Could | Done | Owner request, 17 Nov 2026 | parliament, civic | S21 |
| REQ-29 | Every way to take part: political and civic routes by age and nation (register, vote, stand, serve, influence, how laws are made, civic life), every fact sourced, with a register of participation gaps | Should | Done | Owner request, 17 Nov 2026 | civic | S21, S16, S12 |
| REQ-30 | Participation gaps still open: election calendar by nation, parties explained neutrally, devolved law-making, local council routes, accessible voting guides, registration and turnout chart, community organising, youth media, civic tech | Could | Done | Gap register on Every way to take part, 17 Nov 2026 | civic | S21 |
| REQ-31 | Show how much each issue matters to young people: ballot votes, worries and actions, in several views, with domains mapped to ballot topics | Should | Done | Owner request, 17 Nov 2026 | issues | S23, S12 |
| REQ-32 | Young people in numbers: demographic, ethnic and language, socio-economic, geographic, life-stage, challenges, hopes and opportunity data, every figure sourced and explained | Should | Done | Owner request, 17 Nov 2026 | numbers | S23, S12 |
| REQ-33 | Academy lessons that are real, interactive and sourced, with honest progress kept on the device | Must | Done | Owner question, 17 Nov 2026 (D40) | acad | S23 |
| REQ-34 | Easy Read summaries for every screen, switched on in Access and language settings | Should | Done | Owner request, 17 Nov 2026 (D41) | incl, home | S23, S12 |
| REQ-35 | One clear front door: Home first, with a who-are-you chooser; the closed-petition splash, alerts, ticker and carousel moved below the page title; a compact This screen strip that holds Easy Read | Must | Done | Owner question, 17 Nov 2026: on a phone the page title sits over 1,200px down | home, hub | W10 |
| REQ-36 | Every card that names something opens it: cards that name a screen, setting or issue now open it; figure tiles, swatches and definitions stay as they are, because a click would add nothing | Should | Done | Drill-down audit, 17 Nov 2026 (97 static cards on 29 screens) | policy, coal, track, post, radar, brand, trust, ai | S23 |
| REQ-37 | A cookie-free totals counter: one per screen opened per day, nothing that identifies anyone, published on Portal health, built switched off until its DPIA is signed off | Should | Done | Owner, 20 Nov 2026 (O18) | health, incl | S25, W11 |

## How it is traced, tracked and managed on GitHub

1. **Ask.** Ideas, bugs, contact, research interest and ambassador interest arrive through public issue forms that ask for no personal details. (`.github/ISSUE_TEMPLATE/`)
2. **Acknowledge.** A workflow thanks the person, labels the issue for triage, and flags anything that looks like personal data so it can be removed. (`.github/workflows/issue-ack.yml`)
3. **Triage.** Each week the upkeep run decides: accept, adapt, defer or decline, with a reason. Accepted items become requirements here (REQ ids). (`Scheduled task`)
4. **Build.** Changes are made in data/ or tools/ on a branch; a pull request links the requirement and issue it serves. (`Pull requests (template with a checklist)`)
5. **Check.** Every check runs on every pull request, in a real browser too; each requirement names the checks that prove it. (`.github/workflows/checks.yml`)
6. **Release.** The owner merges and republishes; the release log and drawer flags update from data/changelog.json. (`data/changelog.json`)
7. **Follow up.** Every Monday a workflow gathers what is due: open items, gates not passed, overdue sources and coming dates, into one Follow-ups issue. (`.github/workflows/follow-ups.yml`)
