# ADR 0001: Build the published portal from the design, by named transforms

Date: 15 November 2026 · Status: accepted

## Context

The portal was designed in Claude Design. The design file is a canvas: it opens on a review view, has image
drop-zones, loads React, Babel and fonts from CDNs, and carries no footer, safeguards or data layer.

## Options

1. Publish the design as it is. Fast, but ships drop-zones, CDN calls and no disclaimers.
2. Fork the design and edit the copy by hand. Flexible, but the design and the portal drift apart for good.
3. Keep the design byte for byte in `app/`, and build `site/` from it with named transforms that must each match
   exactly as often as they say.

## Decision

Option 3. Content lives in `data/*.json`; extensions live in `tools/extend.py` and `tools/extend2.py`; every
transform is listed with its reason in `site/build.json`.

## Consequences

- A change to the design that moves an anchor stops the build (B1) instead of silently half-applying.
- The design can be re-exported from Claude Design and rebuilt.
- The cost: transforms are text patches over a large file, so each new feature must anchor carefully.
