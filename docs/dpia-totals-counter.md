# Data protection impact assessment: Amplify totals counter

| | |
|---|---|
| Processing | A cookie-free counter that adds one to a daily total each time a screen of Amplify opens |
| Controller | The owner of Amplify, as an individual (a personal, unpaid project; not on behalf of any employer) |
| Prepared | 20 November 2026, with the counter built and switched off (O18, REQ-37) |
| Status | **Owner sign-off: pending** |
| Review date | 28 February 2027, or earlier if anything below changes |

The counter must stay switched off until the owner signs this assessment off. Check S25 enforces this: the build fails if the counter has an address while the status line above still says "pending".

## 1. Why a DPIA, and what decision it supports

Amplify is for young people aged 11 to 25, and for the adults who support them. Under the ICO's Age appropriate design code (the Children's code), a service likely to be used by children must assess risks to them before any processing starts (standard 2). The owner decided on 20 November 2026 to add a counter. The aim is to see which screens are used, so he can decide what to improve, continue, pause or stop. That decision was recorded as O18 before launch, with these conditions:
- totals only
- no identifiers stored
- no profiling
- figures published on Portal health
- a review date

This assessment tests the build against those conditions.

## 2. What happens, step by step

1. A visitor opens a screen of Amplify, for example `#numbers`.
2. If the counter is switched on, and the browser does not send Global Privacy Control or Do Not Track, and the visitor has not switched counting off in Access, the page sends one HTTPS request to the counter database's API. The request body is `{"s": "numbers"}`. It is sent with credentials omitted (no cookies) and no referrer.
3. The database checks that `numbers` is one of the portal's own 50 screen IDs. If it is, the database adds 1 to that screen's total for today's UTC date. Otherwise it does nothing.
4. Opening Portal health asks the database for the totals of the last 28 days. They are shown there for anyone to see.

What is stored: rows of `(date, screen, total)`. Nothing else.

What is never collected or stored by Amplify:
- cookies
- device storage used for counting
- IP address
- browser or device details
- referrer
- a time finer than a date
- any identifier, hash or fingerprint
- anything typed into the portal

The only thing kept in the visitor's browser is their own "switch counting off" choice. It sits with their other preferences, because they asked for it.

## 3. Personal data in the flow

The totals are not personal data: they cannot relate to anyone.

The request itself is the only point where personal data is touched. Like any web request, it carries the visitor's IP address to the database host, Supabase, which acts as Amplify's processor. Supabase's API gateway logs requests, including IP addresses, for a short period: about 1 day on the free plan, under its own terms. Amplify never receives or stores those logs.

- Lawful basis for that transient processing: legitimate interests (UK GDPR Article 6(1)(f)), namely knowing which parts of a free public service are used.
- Balancing test: no identifier is kept, nothing is linked across visits, and there is no profiling, advertising or sharing. Opting out is one click, and browser privacy signals are honoured automatically. The balance favours the visitor's interests being protected, and this design protects them.

PECR: counting reads and writes nothing on the visitor's device, so regulation 6 is not engaged. The opt-out choice is stored only because the visitor asked for it, so it is strictly necessary. The Data (Use and Access) Act 2025 statistics exemption is therefore not needed. It would apply if a future version did use device storage.

## 4. Children's code: the standards that apply

| Standard | How the counter meets it |
|---|---|
| 1 Best interests | The only purpose is improving a free civic-education service for young people. |
| 2 DPIA | This document. Sign-off before switching on, enforced by S25. |
| 4 Transparency | The footer sentence changes with the counter's state. Portal health and Access explain it in plain words. |
| 5 Detrimental use | No nudging, no engagement scoring, no use of totals to target anyone. |
| 7 Default settings | Counting is on by default only because nothing about the person is kept. Browser privacy signals switch it off automatically. The strongest case against this is in section 6. |
| 8 Data minimisation | One screen ID per request, totals per day, nothing else. |
| 9 Data sharing | None. Totals are published openly on Portal health. |
| 10 Geolocation | None. |
| 12 Profiling | None: no visitor-level data exists to profile. |
| 13 Nudge techniques | None. |

## 5. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation | Residual |
|---|---|---|---|---|
| IP addresses seen by the database host | Certain | Low | Processor terms, London region, short log retention, nothing kept by Amplify | Low |
| Someone inflates the totals (the publishable key is public by design) | Possible | Low | Known screens only, daily cap per screen, and a "read with care" note saying totals are a rough guide | Accepted |
| The counter grows into tracking over time | Possible | High | S25 fails the build if the page sends anything but the screen ID, sends credentials or a referrer, ignores GPC or DNT, or the key is a secret key. W11 tests the real requests in a browser. | Low |
| Counter outage breaks the page | Unlikely | Medium | Requests are fire-and-forget and errors are swallowed. Portal health shows a plain message. | Low |
| The secret service key leaks into the site | Unlikely | High | Only a publishable key is accepted (S25). Row-level security is on, and the table is reachable only through two functions. | Low |
| Amplify's earlier promise of "no analytics" becomes untrue | Certain once switched on | Medium | The footer and About wording change with the counter's state, and S25 fails if "no analytics" remains while the counter is on. Outreach emails sent on 17 November 2026 said Amplify "collects no information about students", which stays true: totals are not information about anyone. | Low |

## 6. The strongest case against, stated first

- **Defaults for children.** The Children's code expects high privacy by default. A counter that is on by default for an 11-year-old could be read as falling short of that.
  - The answer here: no information about the child is kept, so there is no privacy setting being defaulted down.
  - Still, a regulator could prefer off by default. If the owner agrees, the switch can default to off (one change) at the cost of much smaller totals.
- **Third party.** The visitor's IP address reaches a US-headquartered company's infrastructure, even though the data stays in the London region. Supabase's data processing agreement covers international transfers. A self-hosted counter would avoid that, but it needs a server Amplify does not have.
- **Small numbers.** Base rates are low: in its first weeks Amplify may see tens of visits a day. Totals will be noisy, and are easy to over-read or to inflate.

## 7. Retention

Daily totals are kept until the review date. At review the owner decides whether to keep, aggregate to monthly, or delete them. Request logs are kept by Supabase under its terms (about 1 day on the free plan). Amplify keeps no logs.

## 8. Switching on and off

See `data/counter.json` (`switch_on`, `switch_off`) and `docs/counter/schema.sql`. Switching off is immediate on the next publish: with an empty endpoint the page sends nothing anywhere.

## 9. Sign-off

To switch the counter on, the owner replaces the status line at the top with `Owner sign-off: signed <date>`, having read sections 5 and 6.
