# Release log

Generated from `data/changelog.json` by `tools/make_docs.py`. The portal shows the same log on its Release log screen, and flags each new (NEW) or changed (UPD) screen in the drawer and on the screen itself.

## 1.0.0 · 2026-11-23 · Planned launch

**Launch at UK Parliament Week 2026.** Public launch planned for the first day of UK Parliament Week (23 to 29 November 2026), subject to the owner's decision to share it.

## 1.0.0-rc.3 · 2026-11-16 · Release candidate

**Campaign kit redesign for UK Parliament Week.** The campaign collateral redesigned from a scan of award-winning youth campaigns, inside the Brand & style rules, with a downloadable graphics pack (defects D30 to D33).

- **UPD** `campaign`: Campaign kit: new-look posters, social card and ambassador badge, drawn from what worked in Give an X, Bite Back, This Girl Can, #LikeAGirl and She Can STEM, using only Amplify's shapes and hues. Three new pieces: a Government Digital and Data careers poster, a poster to fill in for UK Parliament Week groups, and a sticker sheet. Fonts are now embedded so posters print as designed (D30, D31). New graphics pack: one zip with every graphic, images sized for Teams, Viva Engage, email, LinkedIn, Instagram, Stories and TikTok, and a six-slide carousel (D32). New films: a 35-second film and three 15-second vertical shorts for TikTok, Reels, Shorts and Stories, silent with on-screen captions and a transcript each, never playing by themselves.

## 1.0.0-rc.2 · 2026-11-15 · Release candidate

**Safeguarding and honesty fixes before launch.** Four launch blockers fixed (defects D25 to D28), and the readiness record brought up to date.

- **UPD** `research`: Research & design: signing up to take part is paused until Amplify has a named safeguarding lead and procedure (gate G06), and the screen says why in plain words. Withdrawing a research contribution stays available through the contact form (D25).
- **UPD** `ambassadors`: Ambassadors & champions: sign-ups are paused, and the sign-up form is taken down, until safeguarding is in place; the screen says why (D25).
- **UPD** `pledge`: Pledge: the name box is optional and says it is saved only on this device; a new 'Clear my pledges from this device' button removes them; the phone view no longer claims public sharing, a pledge wall, messaging or a message on the day, and the unsourced relaunch sentence is gone (D26, D27).
- **UPD** `trust`: Safeguards & audiences: the privacy promise to parents now matches what the pledge form does (D27).
- **UPD** `golive`: Go-live readiness: G19 closed (pull request 5 merged 15 Nov 2026, 09:26 UTC); G20 closed (owner confirmed 15 Nov 2026 that Amplify is a personal project, so employer agreement does not apply); new Must gate G24, owner sign-off by 22 November; G06 stays open and lists what is paused (D28).

## 1.0.0-rc.1 · 2026-11-15 · Release candidate

**Sources, safeguards, self-checks and help.** Everything below is new or changed since the first published build earlier today.

- **NEW** `home`: Home: a landing page after the splash that explains what Amplify is, who it is for and how to use it, with tours and quick routes. A rolling hero carousel with spotlights, which pauses on hover, focus or the pause button and stops under reduced motion.
- **NEW** `sources`: Trusted sources: official and voluntary-sector sources, filterable by theme, nation and audience, each checked and dated, with a pan-UK coverage grid.
- **NEW** `latest`: What's new: dated changes since the design, from the April 2027 wage rates to the under-16 social media ban.
- **NEW** `trust`: Safeguards & audiences: who the portal is for, including parents and carers, the frameworks it follows, and how it reaches every voice. Includes a d/Deaf participation checklist and every UK official and sign language, with what is supported and what is open. Adds age-related access: which routes a young person can use themselves at each age, and how an adult can act on their behalf.
- **NEW** `health`: Portal health: the portal checks its own freshness and shows its checks, defects and open items.
- **NEW** `changes`: This release log.
- **NEW** `help`: Help & adoption: a user manual, adoption guides for each audience and step-by-step tutorials.
- **NEW** `feedback`: Have your say: an idea and feature box, bug and issue reporting, and how suggestions are handled. Under 13s are told an adult can post for them, as GitHub accounts start at 13.
- **NEW** `launch`: UK Parliament Week launch: the plan and activities for launching Amplify during UKPW 2026. Add UK Parliament Week to Google or Outlook calendars, and share it to Teams, Google Classroom or WhatsApp, for adults and allies.
- **NEW** `about`: About Amplify: who is behind it, why it exists, its mission, aims, goals, objectives and the outcomes it is working towards.
- **UPD** `guide`: Three new guided tours: new here, parents and carers, and the UK Parliament Week launch. Tours now show a step bar on every screen they visit.
- **UPD** `care`: Helplines re-checked: HOPELINE247 removed (closed 7 September 2026), The Mix now by text, NHS 111 added, Samaritans' Welsh line added.
- **UPD** `map`: Local routes map: a land outline replaces street tiles that no longer load.
- **UPD** `hub`: Illustrations replace the empty image boxes, and a launch countdown for UK Parliament Week.
- **UPD** `corner`: Cornerstone illustrations drawn from the brand's six shapes.
- **NEW** `media`: Media centre: approved descriptions with copy buttons, key facts with sources, illustrations and the rules for using them.
- **NEW** `communities`: Communities, networks and youth groups hub, by kind of group, for every UK nation.
- **NEW** `involve`: Contribute: ways to help build, check and look after the portal by time and skill, the roles you could take on, how a change gets in, and the rules that keep contributors safe.
- **NEW** `research`: Research & design: join the research panel, or help with UI, UX, graphic and content design. It sets out a safeguarding promise for young people and families, research questions and rounds, You said we did, working groups, badges and a usability score worked out on your device. It also lists, by MoSCoW, what was ported from DQ Commons, the GitHub repos asset catalogue and govukOS. A research bundle is generated in docs/research/.
- **NEW** `service`: Personas & journeys: eight proto-personas, including a d/Deaf or disabled young person, with needs, pain points and safety; 18 user stories, each with the checks that prove it; six journeys; five service blueprints; and five workflows, from build and release to a safeguarding concern. The same content, with flowcharts, is generated in docs/service-design/.
- **NEW** `ambassadors`: Ambassadors and champions: supporter, champion and ambassador levels, a safeguarding promise and code of conduct, and a no-personal-details form to register interest. A pilot until the owner confirms it (O12).
- **NEW** `campaign`: Campaign kit: two printable posters, a social card and an ambassador badge drawn in code, posts to adapt, a five-minute assembly and dates to plan around.
- **NEW** `learn`: Training and sessions: eight ready-to-run sessions, from Democracy in 20 minutes to DevOps in an afternoon, each with outcomes, steps and the screens to use.
- **NEW** `stem`: STEM spotlight: a shout-out for girls and young women in coding, engineering, architecture and DevOps, with sourced facts, free opportunities and a DevOps path built on this portal's own pipeline.
- **UPD** `sources`: Trusted sources: a new STEM, coding and engineering theme with twelve sourced organisations and programmes, including TechFirst, which took over CyberFirst on 1 September 2026.
- **UPD** `home`: Tooltips everywhere: every drawer item and header control explains itself on hover or keyboard focus, and an explainer bar on each screen can be tailored to who you are: young person, parent or carer, youth worker, teacher, club leader or ally.
- **NEW** `golive`: Go-live readiness: the gates for the public launch by area and MoSCoW, each with its status, the checks that prove it and who must act, plus the self-routines that keep the portal right once it is live. Since then: the owner's publishing decision is recorded (public on GitHub Pages since 15 November 2026), the public address opens this portal rather than the original design, and posters and sharing point to it.
- **UPD** `home`: Splash (Signal and Manifesto): no longer links a different charity inside the UK Youth Parliament's name, no longer states votes at 16 as law while the Bill is in the Lords, and credits the typed line as Amplify's own words. It is now a labelled dialog: Escape enters, Tab stays inside, and it never closes by itself once you interact. It names the launch dates, and the constituency dots reflow on phones and tablets. Toolkit messages no longer state votes at 16 as law either.
- **UPD** `campaign`: Campaign kit and Media centre: artwork opens in an in-page viewer with Print (only the artwork prints), Save and a copy on GitHub, because the host blocks opening files in a new tab. The drawer now scrolls on its own on every screen.
- **UPD** `stem`: STEM & tech: now covers science, innovation, data and AI, digital, cyber, engineering and enterprise architecture (its business, data, application, technology and security layers, each with its government role). It adds a section on careers in government and the public sector, with apprenticeships, internships and graduate schemes across all four nations, and links tech to youth voice. 16 new sourced organisations and schemes.
- **NEW** `product`: Product, roadmap & backlog: vision, mission, strategy, product specification, update schedule, roadmap (now, next, later) and a requirements backlog, each requirement traced to the screens that deliver it and the checks that prove it, plus how it is all tracked on GitHub and the new words in this release.
- **NEW** `notify`: Alerts & notifications: launch countdown, updated since your last visit, safety notices, dates coming up and upkeep notices, each dismissible, with choices kept in this browser only; plus an Atom news feed and GitHub watching, with no email list and no tracking.
- **UPD** `graph`: Glossary & graph: the new terms from this release (safeguarding, Online Safety Act, open source, CI, DevOps, user-centred design, enterprise architecture, apprenticeships, AI literacy, roadmap and more), each with other names, links in the graph and a matching tooltip. Also published as a SKOS vocabulary (glossary-skos.json).
- **UPD** `home`: Every screen: a Share button (your device's share menu, or copy the link and share to Teams, Classroom or WhatsApp), the alerts that apply, and a news ticker chosen for that screen, which pauses on hover, on focus and with its own button, and stands still if you prefer reduced motion.

## 0.1.0 · 2026-11-15 · Published

**First published build.** The Claude Design project turned into a page that can be sent: portal view first, unofficial-prototype notices, the footer and colophon, and fonts and scripts served by the portal itself.
