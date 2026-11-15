## What this changes

<!-- One or two sentences. No personal details. -->

Requirement: REQ-<!-- id from data/product.json -->  ·  Issue: #<!-- number, if any -->

## Checklist

- [ ] Changed in `data/` or `tools/`, never by hand in `site/` or the generated docs
- [ ] New words added to `data/glossary.json`: definition, other names, graph links (and tooltips read them from there)
- [ ] `data/changelog.json` lists each new (NEW) or changed (UPD) screen
- [ ] `data/product.json` backlog updated: status, screens and the checks that prove it
- [ ] Every fact has its source, date and provenance (V, S or K); models and samples are labelled
- [ ] Any defect fixed has a check with a negative test and a line in `data/registers.json`
- [ ] No email address, no personal data, no deck or film in the repository
- [ ] All checks pass: `check_repo`, `check_site`, `check_sources`, `check_browser`

A person reviews and merges. Automation never merges.
