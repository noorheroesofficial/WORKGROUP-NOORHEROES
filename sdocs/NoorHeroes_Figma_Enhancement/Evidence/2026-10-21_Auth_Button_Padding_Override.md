
## 2026-10-21 — Authentication button padding override
- Login Send code and Registration Create Account: bottom internal padding 0 px.
- Continue with Google on both screens: top internal padding 0 px.
- Applied to enabled, disabled, animated loading, reduced-motion, and hold instances (22 nodes).
- Other padding remains 14 px. All buttons remain 338 × 56 px; reactions unchanged.
- Verified live Figma properties and screenshots of both screens. No Present playback claim.

## 2026-10-21 — Rollback of last button padding override
User requested rollback. Restore primary button bottom padding and Google button top padding to 14 px on Login and Registration, including all loading/disabled/hold variants. This supersedes the earlier zero-padding override. All 22 node properties verified restored; dimensions and reactions unchanged.
