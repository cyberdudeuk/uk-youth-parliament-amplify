# Good first issues

Small, real tasks for a first contribution. Each one has a clear finish line and a check that tells you if anything
broke. The owner files these as GitHub issues labelled `good first issue` (open item O13); until then, pick one here and
say which in an issue.

Everything on GitHub is public: never post your name, school, contact details or anyone else's. GitHub is for people
aged 13 and over; 13 to 17 year olds should agree it with a parent or carer first.

| # | Task | Skills | Where | Done when |
| --- | --- | --- | --- | --- |
| 1 | Re-check a source whose review is due: compare its `what` and `use` lines with the organisation's own site, and update `checked` only if you verified it | Reading, care | `data/youth-sources.json` | `check_sources.py` passes and the pull request says what you checked |
| 2 | Keyboard-test one screen and report any control you cannot reach or see focus on | Accessibility | Any screen | A bug issue names the screen and the control |
| 3 | Screen-reader test the tooltips: does each drawer item read its explainer? | Accessibility | Drawer, `tools/extend4.py` | A bug issue or "works" note per screen reader tried |
| 4 | Suggest a clearer tooltip for one screen, for one persona | Plain English | `data/tooltips.json` | `check_site.py` S12 passes |
| 5 | Confirm one "Lead, to confirm" date on the Campaign kit with the organiser's own site, then change it to S with the source | Research | `data/involve.json` | The moment shows as Search-sourced |
| 6 | Add one free STEM opportunity for young people in Scotland, Wales or Northern Ireland, with its official link | Research | `data/youth-sources.json`, `data/involve.json` | `check_sources.py` passes |
| 7 | Find a check without a plain-English docstring line and write one | Python, writing | `tools/check_*.py` | The rule shows in `site/build.json` "checks" |
| 8 | Make the posters' text easier to read at A5: suggest sizes or line breaks | Design | `tools/art.py` | A rebuilt poster you have opened and printed or zoomed |
| 9 | Read `.github/workflows/checks.yml` and add a one-line comment above each step saying what it does | DevOps | `.github/workflows/` | CI passes on your pull request |
| 10 | Break a check on purpose locally, watch the "caught" line, and write up what you learned for the Training screen | DevOps, writing | `tools/check_site.py` | An idea issue with your write-up |
