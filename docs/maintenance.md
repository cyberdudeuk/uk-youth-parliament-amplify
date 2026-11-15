# Maintenance, upkeep and the self-routines

Amplify maintains itself in the open. This page says what runs, when, where it reports, and what only a person may do.

## Profile and grade

Public-sector profile (a personal project about youth participation in UK democracy), built to **G3: shared or published**,
because young people, parents and carers will use and rely on it. It collects no personal data, so it is not G4; if it
ever collects any, it becomes G4 and needs a data protection impact assessment first.

## The self-routines

| Routine | What it does | Where it runs | Where it reports |
|---|---|---|---|
| Self-verification | `check_repo.py` (R1–R6), `check_site.py` (S1–S11), `check_sources.py` (C1–C9), `check_browser.py` (W1–W4); each check proved by a deliberate break | Every push and pull request (CI) | The pull request's checks |
| Self-repair | `site/` and `CHANGELOG.md` are regenerated from `app/` and `data/`; a transform that no longer matches the design stops the build rather than half-applying | `tools/build_site.py` | Build output |
| Self-assessment | Accessibility (axe-core) against a baseline that may only shrink; overflow at 360 px and 1440 px; content-integrity classes for every screen | CI and weekly | Checks; Portal health screen |
| Self-reporting | The Portal health screen computes freshness, provenance and status every time it opens; the weekly workflow updates one "Portal health" issue | In the page; weekly on GitHub | Portal health screen; the health issue |
| Self-updating and staleness | Every data set and source carries a checked date and a review cadence (30 days for helplines); C3 fails past 1.5× the cadence; `--online` tests every link | Weekly (Monday 06:17 UTC) and the scheduled upkeep run | The health issue |

## The weekly upkeep run

A scheduled task runs a maintenance session each week. It:

1. Pulls `main`, runs every check, and reads the open health issue and any new idea, bug or contact issues.
2. Re-verifies helplines first, then sources past their review date, against each primary site.
3. Updates `data/*.json` (sources, What's new, registers, release log), rebuilds, and reruns every check.
4. Opens a pull request with the changes and a plain report: what changed, what was checked, what stays open.

It never merges, deletes, publishes or changes who can see anything: **people decide the irreversible**. The owner merges.

## Releasing

1. Add the release and its NEW/UPD entries to `data/changelog.json`; set `current`.
2. `python3 -I tools/build_site.py`, then all four checks.
3. Merge, then republish the artifact from `site/`.

## Adding or changing content

- Sources, updates, safeguards, help, launch and integrity live in `data/*.json`: edit there, never in `site/`.
- Every new fact needs a provenance: V (verified against the primary source, with a date), S (search-sourced) or K (a lead).
- Every new screen needs a content-integrity class (C9).
