# Accessibility statement

Amplify aims to meet WCAG 2.2 AA and to be usable by every young person, parent and carer, including disabled and
d/Deaf users and people on slow connections.

## What works now

- Keyboard access with visible focus; a skip link; Escape closes panels.
- Theme, contrast, text size, dyslexia-friendly type, reduced motion, low-data mode and an 11 to 13 reading mode,
  all in the Access panel and all kept in the browser only.
- Motion stops under the in-page switch and under the system's reduced-motion setting.
- Tooltips appear on keyboard focus as well as hover, are linked with `aria-describedby`, stay while the pointer
  moves onto them, never cover what they explain, and close with Escape (WCAG 1.4.13). Every screen also has a
  visible explainer bar, so nothing is available only through a tooltip; touch users read the bar.
- No account, no sign-in, no phone-only contact: every route is a web form.
- Every font, script and icon is served by the portal itself, so it works without third-party services.

## How it is tested

Every pull request runs axe-core against every screen at 1440 px and checks for sideways overflow at 360 px and
1440 px (`tools/check_browser.py`). A baseline records any findings carried over from the original design; it may
only shrink.

## Known gaps

- Not yet tested with disabled or d/Deaf users (open item O1).
- No BSL or ISL video versions, and no full Welsh, Gaelic or Irish versions yet (O10).
- No Easy Read version yet (O5).

## Feedback

Tell us about an accessibility problem through the bug form (choose the accessibility option). If you cannot use the
form, ask your MYP, a youth worker or a trusted adult to raise it for you.
