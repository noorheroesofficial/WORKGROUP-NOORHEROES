# Registration consent bottom sheets — completed 2026-10-21

User authorized fictional sample data and draft legal wording for the prototype. Legal review remains required before production.

## Final layout and nodes
- Main Registration 1459:256: one compact acceptance row 1513:429, followed by Optional preferences 1459:1128 with exactly 14 px gap.
- Removed only original inline Terms/Privacy rows and the required group from V2. Moved existing adult and child-data controls to their respective sheets.
- Terms 1513:350, Privacy 1513:386, Optional preferences 1511:380.
- Optional detail sheets: Personalization/AI 1514:354, Voice-feature 1514:384, Marketing 1514:414.
- Existing branding, card action footer, loaders, input and submit behavior retained.
- Field height 72 by default, 104 on validation; helper y86. Input/method/error actions updated accordingly.
- Approved 14 px arrow asset 1253:47 reused; empty artwork canvas remains unfilled.

## Required sequence
1. Compact row opens Terms. Reading/opening never grants consent.
2. Adult confirmation remains separate and initially unchecked. Terms contains age, child profile, child data and fictional Ayaan sample sections.
3. I Agree & Continue requires adult confirmation. It records Terms only, closes the Terms sheet, then opens separate Privacy.
4. Privacy explains collection, purpose, optional processing, safeguards and access/deletion as draft wording. Child-data processing remains a separate unchecked choice.
5. Acknowledge & Continue requires Terms, adult and child-data confirmation. It records Privacy acknowledgement and closes to Registration.
6. Main summary is checked only when all four required choices are true. Selected checkbox can revoke all four; label reopens Terms.
7. Close, backdrop, Escape and Back grant nothing and preserve prior explicit progress. Privacy Back closes before reopening Terms.
8. Optional choices remain independent and initially off. Done and detail swaps preserve values. Each Read opens its matching draft detail.
9. No unconfirmed OTP destination was added. Existing Create Account/Google gates remain intact.

## Layout and motion
390×844 prototype; same Poppins, warm-white sheets, components, palette and 14 px spacing. Legal sheets are 390×720 at y124 with 410 px document scroll area, a fixed 56 px action and 24 px bottom inset. Editable long text wraps with Auto Layout. Close/Back and preferences use at least 44 px targets.
Entry uses 280 ms Move In from bottom; reduced motion is instant. Optional detail swaps also have an instant reduced-motion path.

## Verification
22 structural/layout checks passed, including all 16 required-choice combinations, explicit agreement, close-before-open action order, cancellation, offline gating and optional independence. Seven follow-up checks passed for detail routes, reduced motion and validation helper bounds.
Screenshots of Registration, Terms, Privacy, preferences and one detail reviewed. Corrected text wrapping and empty vector canvas fill before final review. Exact copy and node manifests are in the adjacent JSON.

Present playback remains untested because of the existing browser permission restriction. Structural action order is not proof of runtime playback. Native input, screen-reader behavior, backend/network processing and real consent recording were not tested. Draft text makes no claim of legal approval or implemented production safeguards.

## Responsive follow-up — 2026-10-21
All six new consent/detail overlays have stretch backdrops, responsive horizontal sizing, and bottom positioning. Legal panels use flexible document viewport height; paragraphs and fixed actions resize with the panel. At 320×568, legal panels are 320×444, inner body/actions 268 px wide, with 134 px scroll viewport; text wraps without horizontal clipping. Optional sheet remains 380 px high at y188. Checked six panel bounds, two button widths and two legal text widths. Compact screenshots reviewed; all frames restored to 390×844, no QA frames created. Additional results: Evidence/2026-10-21_Consent_Bottom_Sheets_Responsive.json. Total: 39 structural/graph/layout checks passed; Present playback remains unverified.
