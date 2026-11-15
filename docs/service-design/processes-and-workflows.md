# Processes and workflows

Generated from `data/service-design.json` by `tools/make_docs.py`; edit that, not this file. The portal shows the same content on its Personas & journeys screen.

> **Status:** Proto-personas and assumed journeys, written from the owner's requests, published guidance and the portal's own safeguards. They have not been tested with users yet: research Round 1 (January to February 2027) tests them, and they will change.

## W-BUILD: Build, check and release

```mermaid
flowchart TD
  S0["Edit data/*.json or tools/"]
  S1["Run tools/build_site.py: page, art and docs are generated"]
  S2["Run check_repo, check_site, check_sources and check_browser"]
  S3["Every check also proves it catches a deliberate break"]
  S0 --> S1
  S1 --> S2
  S2 --> S3
  S3 --> D{"Any check failing?"}
  D -- Yes --> Y["Find the root cause, fix it, add a check and a negative test, log the defect, and rerun"]
  D -- No --> N["Push, open a pull request; the owner merges and republishes"]
```

## W-UPKEEP: Weekly upkeep

```mermaid
flowchart TD
  S0["Pull and run every check"]
  S1["Re-verify helplines first, then sources past review"]
  S2["Look for dated, sourced developments"]
  S3["Triage issues; flag any personal data to the owner"]
  S0 --> S1
  S1 --> S2
  S2 --> S3
  S3 --> D{"Anything safety-critical?"}
  D -- Yes --> Y["Fix it first and mark the pull request safety-critical"]
  D -- No --> N["Open the weekly pull request with a plain report"]
```

## W-SAFE: A safeguarding concern

```mermaid
flowchart TD
  S0["Someone posts or says something that suggests risk"]
  S1["Do not reply in public or repeat the details"]
  S2["Point to helplines on Safeguarding & support"]
  S3["Tell the owner straight away"]
  S0 --> S1
  S1 --> S2
  S2 --> S3
  S3 --> D{"Is someone in immediate danger?"}
  D -- Yes --> Y["Call 999, then follow the setting's safeguarding procedure"]
  D -- No --> N["The owner follows the safeguarding procedure and records what was done"]
```

## W-CONTRIB: Contribution triage

```mermaid
flowchart TD
  S0["An Idea, Bug, ambassador or contact issue arrives"]
  S1["Check it contains no personal data"]
  S2["Decide: accept, adapt, defer or decline, with a reason"]
  S3["Small, safe fixes are made in the weekly run"]
  S0 --> S1
  S1 --> S2
  S2 --> S3
  S3 --> D{"Does it need the owner's decision?"}
  D -- Yes --> Y["List it as an open item with the owner as who must act"]
  D -- No --> N["Implement, check, and record it in the release log"]
```

## W-RESEARCH: Research round

```mermaid
flowchart TD
  S0["Recruit through trusted organisations across the quotas"]
  S1["Book interpreters and support before offering sessions"]
  S2["Run sessions with a trusted adult present or nearby"]
  S3["Synthesise into themes within two weeks"]
  S0 --> S1
  S1 --> S2
  S2 --> S3
  S3 --> D{"Does a theme exclude a group?"}
  D -- Yes --> Y["Fix that first, before anything else in the backlog"]
  D -- No --> N["Play findings back to participants, then publish You said, we did"]
```
