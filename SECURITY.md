# Security policy

Please report security problems privately. Do not open a public issue.

- **GitHub private vulnerability reporting:** [report a vulnerability](https://github.com/cyberdudeuk/uk-youth-parliament-amplify/security/advisories/new).
  This works once the repository owner has switched on private vulnerability reporting.

No email address is published, by the owner's decision (contact is by form only).

## What is in scope

The portal is a set of static pages with no server, no accounts and no sign-in. The most likely issues are cross-site
scripting through the page runtime or the petition data, a page loading something it should not, or a supply-chain problem
in the GitHub Actions workflows.

## Automated checks

- **CodeQL** scans the JavaScript, the Python checks and the workflows on every pull request, on `main` and weekly.
- **Dependency review** stops a pull request that adds a dependency with a known vulnerability of moderate severity or worse.
- **Dependabot** proposes updates to the pinned GitHub Actions weekly.
- **OpenSSF Scorecard** checks how the repository is run, weekly.
- `tools/check_repo.py` runs on every push (see the README).
