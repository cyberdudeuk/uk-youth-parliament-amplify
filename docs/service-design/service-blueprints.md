# Service blueprints

Generated from `data/service-design.json` by `tools/make_docs.py`; edit that, not this file. The portal shows the same content on its Personas & journeys screen.

> **Status:** Proto-personas and assumed journeys, written from the owner's requests, published guidance and the portal's own safeguards. They have not been tested with users yet: research Round 1 (January to February 2027) tests them, and they will change.

## B1: A young person finds a route in and takes part safely

| Layer | Hear | Arrive | Find | Act | Stay safe |
|---|---|---|---|---|---|
| **User actions** | Sees a poster or assembly | Opens on a phone | Checks ages and finds their area | Talks to a trusted adult | Knows who to call |
| **Front stage (the page)** | Campaign kit posters | Home, tour, explainer bar | Your route in, tooltips | Communities hub | Safeguarding & support |
| **Back stage (in the page)** | Drawn in code from brand rules | Data loaded from data/*.json | Stages, ages and the local map | Sources with provenance | Helplines with review dates |
| **Support processes** | Ambassadors and teachers share | Weekly upkeep run | Source re-verification | Group listings checked | Helplines re-verified first, every 30 days |
| **Evidence and checks** | S6 | W1, W2 | W4 | C1, C2 | C3, C4, C5 |

## B2: A parent acts on behalf of a child under 16

| Layer | Learn | Decide | Act | Consent |
|---|---|---|---|---|
| **User actions** | Takes the parents' tour | Reads age rules | Shares or acts for the child | Consents to research |
| **Front stage (the page)** | Guide & tours | Safeguards & audiences | Campaign posts for adults | Research promise and consent |
| **Back stage (in the page)** | Tour steps in data | Age and access table | Share links open only on click | Consent text generated from data |
| **Support processes** | Owner reviews tours | Online safety rules tracked on What's new | No tracking or cookies | Private form and safeguarding lead (O14) |
| **Evidence and checks** | W1 | C9 | S9 | S11 |

## B3: A contribution goes from idea to release

| Layer | Suggest | Triage | Change | Check | Release |
|---|---|---|---|---|---|
| **Contributor actions** | Opens an Idea or Bug form | Reads the decision | Edits data or tools | Runs the checks | Sees it in the release log |
| **Front stage** | Have your say, Contribute | GitHub issue thread | Pull request | CI results | Release log, drawer flags |
| **Back stage** | Issue forms ask no personal data | Weekly run triages and labels | Build from data, never site/ | Checks with negative tests | Changelog drives NEW and UPD flags |
| **Support processes** | Personal data flagged to owner | Owner decides | Review by the owner | GitHub Actions | Owner merges and republishes |
| **Evidence and checks** | R1, S4 | C9 | S1, S8 | W1 to W5 | S11 |

## B4: A helpline changes number or closes

| Layer | Detect | Verify | Fix | Tell |
|---|---|---|---|---|
| **Maintainer actions** | Weekly run checks helplines first | Compares with the service's own site | Updates the source and retires the old number | Adds a What's new entry |
| **Front stage** | Portal health flags review due | Source card shows check date | Safeguarding & support updates | Ribbon shows UPD |
| **Back stage** | 30-day review cycle | Provenance set to V with date | Retired numbers listed | Release log entry |
| **Support processes** | Scheduled weekly task | Primary source only | Pull request marked safety-critical | Owner merges first |
| **Evidence and checks** | C5 | C2 | C3, C4 | S11 |

## B5: A research round with young people

| Layer | Recruit | Prepare | Run | Synthesise | Play back |
|---|---|---|---|---|---|
| **Participant actions** | Registers through a school, group or parent | Reads information, gives consent | Takes part with a trusted adult nearby | Can withdraw within 30 days | Sees findings first |
| **Front stage** | Research & design screen | Participant information, consent forms | Session guides | Synthesis template | You said, we did |
| **Back stage** | Screener with quotas | Interpreters booked first | Notes by session code | Themes and totals only | Findings linked to changes |
| **Support processes** | Private sign-up form (O14) | Background-checked facilitators | Safeguarding lead | Notes deleted after 6 months | Release log and backlog |
| **Evidence and checks** | S11 | S11 | C9 | S11 | C9 |
