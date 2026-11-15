# Contributing

Thank you for helping. Anyone can raise a question, report a problem or suggest a change. You do not need to write code.

## Ways to take part

The portal's **Get involved** screens set out every way to help, matched to your time and skills, with the roles,
the ambassador programme, a campaign kit, training sessions and a STEM spotlight. Their text lives in
`data/involve.json`, so change it there rather than copying it here.

- **Ask, report or suggest:** the [contact form](https://github.com/cyberdudeuk/uk-youth-parliament-amplify/issues/new?template=contact.yml),
  or the [idea](https://github.com/cyberdudeuk/uk-youth-parliament-amplify/issues/new?template=idea.yml) and
  [bug](https://github.com/cyberdudeuk/uk-youth-parliament-amplify/issues/new?template=bug.yml) forms.
- **Ambassadors and champions:** [register interest](https://github.com/cyberdudeuk/uk-youth-parliament-amplify/issues/new?template=ambassador.yml)
  (a pilot until the owner confirms it, open item O12).
- **A first contribution:** start with an issue labelled `good first issue`; [docs/good-first-issues.md](docs/good-first-issues.md)
  lists the starters.
- **Security problems:** report them privately, as [SECURITY.md](SECURITY.md) explains. Do not open a public issue.

Issues are public. Do not include personal data, anyone's contact details or anything that identifies a young person.

### Age and safety

GitHub accounts are for people aged 13 and over. If you are 13 to 17, agree it with a parent or carer first; under 13s
can take part through a trusted adult, such as a teacher, youth worker or club leader, who posts for them. If you are
worried about yourself or someone else, do not post here: use the helplines on the portal's Safeguarding & support screen.

### Where things live

| To change | Edit | Never edit |
| --- | --- | --- |
| Content: sources, updates, help, tooltips, Get involved | `data/*.json` | `site/` (it is built) |
| Screens and behaviour | `tools/extend*.py`, `tools/build_site.py` | `app/` (copied from the design) |
| Illustrations, posters and cards | `tools/art.py` | the SVGs in `site/art/` |
| Checks | `tools/check_*.py`, each with a negative test | |

Then run `python3 -I tools/build_site.py`, and the checks below.

## Making a change

- Work on a short-lived branch and open a pull request. The owner reviews every change.
- The portal files in `app/` are copied byte for byte from their source artifact. Do not retype or hand-edit them: a change
  must come from the source, with the new SHA-256 recorded in `tools/sources.json`.
- Run `python3 -I tools/check_repo.py`, `check_site.py` and `check_sources.py` before you push (and `tools/check_browser.py`
  if you changed a screen). CI runs them all again. Each check also proves it still catches a deliberate break.
- Every defect gets a check in the same commit as its fix, with a negative test proving the check fails when it should.
- No email address anywhere. No decks or films. No blueprints or input files once their features are built.
- Plain English and British spelling.

## Code of conduct

Everyone taking part follows the [code of conduct](CODE_OF_CONDUCT.md).
