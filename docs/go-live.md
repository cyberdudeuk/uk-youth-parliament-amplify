# Go-live readiness

Generated from `data/readiness.json` by `tools/make_docs.py`; edit that, not this file. The portal shows the same content on its Go-live readiness screen.

What must be true before Amplify goes public at UK Parliament Week, what has been tested and how, what is still open and who must act, and the self-routines that keep it right once it is live. Must items block the public launch; Should and Could items do not, but are tracked.

**Verdict:** not ready to go public yet: 4 Must gates open (G06, G19, G20, G21).

## Gates

| Id | Area | Gate | MoSCoW | Status | Proved by | Who must act |
|---|---|---|---|---|---|---|
| G01 | Accuracy and content | Every screen says whether its content is sourced, a planning model, a sample, generated or editorial | Must | Pass | C9 |  |
| G02 | Accuracy and content | Claims checked against review findings: no other organisation inside UKYP's name, votes at 16 not stated as law, manifesto line credited | Must | Pass | S14 |  |
| G03 | Accuracy and content | Every source has a provenance and a check date; overdue ones are flagged | Must | Pass | C1, C2, C7 |  |
| G04 | Accuracy and content | Search-sourced facts (S) and leads (K) verified against primary sources where they matter most | Should | Partial | C1 | Owner and weekly upkeep |
| G05 | Safeguarding | Helplines current and re-checked every 30 days; safeguarding linked from every Get involved screen | Must | Pass | C3, C4, C5 |  |
| G06 | Safeguarding | A named safeguarding lead and procedure before the ambassador programme or any research with under 18s starts | Must | Open |  | Owner (O12, O14) |
| G07 | Accessibility | WCAG 2.2 AA automated checks: axe-core in dark and light themes, keyboard, tooltips on focus, splash dialog | Must | Pass | W3, W5, W6, W7 |  |
| G08 | Accessibility | Testing with disabled people using their own technology, including d/Deaf BSL and ISL users | Should | Open |  | Owner (research Round 2, O14) |
| G09 | Phones and tablets | No sideways scrolling at 320 px (small phone), 768 px (tablet) and 1440 px, on every screen and the splash; the drawer scrolls on its own | Must | Pass | W2, W6, W8 |  |
| G10 | Phones and tablets | Fast enough on a phone: the page is compiled in the browser by a bundled runtime, which is slow on low-end phones | Should | Partial | W7 | Owner decides (O16) |
| G11 | Privacy and security | Nothing reaches another host on load; no tracking; every library and font served by the portal | Must | Pass | S7, S9, W1 |  |
| G12 | Privacy and security | No email address anywhere; no personal data collected; contact by form only | Must | Pass | R1, S4 |  |
| G13 | Privacy and security | Code scanning clean on every change | Should | Pass | CodeQL |  |
| G14 | Privacy and security | A privacy notice for the research sign-up form | Should | Open |  | Owner (O14) |
| G15 | Operations | Every build verified, every check vaccinated, defects logged with a check | Must | Pass | S1, S8, S11 |  |
| G16 | Operations | Weekly upkeep and weekly health checks scheduled, reporting to one place | Must | Pass | health.yml, upkeep task |  |
| G17 | Operations | Rollback: the previous version is kept and can be restored | Must | Pass | S1 |  |
| G18 | Operations | Posters and cards print on their own; other screens are not yet print-tested | Could | Partial | W8 | Weekly upkeep |
| G19 | Governance | The release candidate is reviewed and merged | Must | Open |  | Owner (pull request 5) |
| G20 | Governance | Propriety: publishing under the owner's own name raises no issue with his employer | Must | Open |  | Owner (O11) |
| G21 | Governance | Decide how the portal is shared (the artifact is private until shared) and the address posters should point to | Must | Open |  | Owner (O15) |
| G22 | Research and UCD | Personas, journeys and stories tested with real users | Should | Open |  | Owner (O1, research Round 1) |
| G23 | Research and UCD | Welsh, Gaelic, Irish and sign-language versions of the most-used screens | Could | Open |  | Owner (O10) |

## Self-routines

| MoSCoW | Routine | Kind | What | Cadence | Where | Status |
|---|---|---|---|---|---|---|
| Must | Build verification | Self-verification | Every named change to the design must match exactly; vendored files match their pinned hashes; data parses | Every build | tools/build_site.py (B1 to B3) | Running |
| Must | Static checks | Self-verification | Repository, site and content rules, each proved by a deliberate break | Every change, in CI | tools/check_repo.py, check_site.py, check_sources.py | Running |
| Must | Browser checks | Self-testing | Every screen at three widths, axe-core in both themes, tooltips, splash, phone speed | Every change, in CI | tools/check_browser.py | Running |
| Must | Weekly health | Self-reporting | All checks plus the online link check, reported to one issue | Mondays | .github/workflows/health.yml | Running |
| Must | Weekly upkeep | Self-updating | Helplines first, then sources past review, new developments, issue triage, a pull request with a report | Mondays 07:23 | Scheduled task | Running |
| Must | Staleness | Self-assessment | Freshness of every source and data file, with 30-day helpline and 90-day source reviews | Live on Portal health | Portal health screen | Running |
| Must | Defect to check | Self-repair | Every defect gets a root cause, a fix, a check with a negative test and a register entry in one commit | Every defect | data/registers.json | Running |
| Must | Accessibility baseline | Self-assessment | The design's own axe findings may only shrink | Every change | tools/a11y-baseline.json | Running |
| Must | Generated documents | Self-documenting | Release log, registers, research bundle and service design are written from data, never by hand | Every build | tools/make_docs.py (S11) | Running |
| Must | Personal data watch | Self-protection | Issues are checked for anything that identifies a person; the owner is told at once | Weekly | Scheduled task | Running |
| Should | Code scanning | Self-verification | CodeQL on Python, JavaScript and workflows | Every change | GitHub code scanning | Running |
| Should | Release flags | Self-describing | NEW and UPD flags in the drawer and on each screen come from the release log | Every release | data/changelog.json | Running |
| Should | Research loop | Self-improving | Rounds, synthesis and You said, we did | Each round | Research & design screen | Set up, not yet run |
| Should | Persona and journey review | Self-improving | Personas, stories and journeys updated from research findings | After each round | data/service-design.json (S13) | Set up, not yet run |
| Should | Accessibility audit by people | Self-assessment | Testing with disabled people using their own technology | Yearly | Research Round 2 | Not yet |
| Could | Availability monitoring | Self-reporting | A check that the published portal loads, from outside the build | Daily | Not yet chosen | Not yet |
| Could | Vendored library watch | Self-updating | Notice when React, Babel, Leaflet or the icons have security releases | Monthly | Not yet chosen | Not yet |
| Could | Retirement plan | Self-retiring | How the portal is archived or handed over if it stops being maintained | Once, reviewed yearly | docs/maintenance.md | Not yet |
| Should | Follow-ups due | Self-reporting | Gathers gates not passed, open items, requirements not done, sources and data files due a re-check and dates coming up into one public issue. | Every Monday | .github/workflows/follow-ups.yml | Set up, runs once merged |
| Must | Issue acknowledgement | Self-protecting | Thanks each new issue, labels it for triage, gives the helplines and flags anything that looks like an email address or phone number for a person to remove. | On every new issue | .github/workflows/issue-ack.yml | Set up, runs once merged |
| Must | Vocabulary in step | Self-verification | Fails the build if a release adds a term, tooltip, graph link or version without its glossary entry, or leaves the graph unparseable. | Every change | check_site S16 | Running |
