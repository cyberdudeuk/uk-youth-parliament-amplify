# Contributing

Thank you for helping. Anyone can raise a question, report a problem or suggest a change. You do not need to write code.

## Ways to take part

- **Ask, report or suggest:** the [contact form](https://github.com/cyberdudeuk/uk-youth-parliament-amplify/issues/new?template=contact.yml).
- **Security problems:** report them privately, as [SECURITY.md](SECURITY.md) explains. Do not open a public issue.

Issues are public. Do not include personal data, anyone's contact details or anything that identifies a young person.

## Making a change

- Work on a short-lived branch and open a pull request. The owner reviews every change.
- The portal files in `app/` are copied byte for byte from their source artifact. Do not retype or hand-edit them: a change
  must come from the source, with the new SHA-256 recorded in `tools/sources.json`.
- Run `python3 -I tools/check_repo.py` before you push. CI runs it again.
- Every defect gets a check in the same commit as its fix, with a negative test proving the check fails when it should.
- No email address anywhere. No decks or films. No blueprints or input files once their features are built.
- Plain English and British spelling.

## Code of conduct

Everyone taking part follows the [code of conduct](CODE_OF_CONDUCT.md).
