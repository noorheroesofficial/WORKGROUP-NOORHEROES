# Screen 009 — Consent Detail / Full Text

**ROLLED BACK at the user's request.** The implementation described below is historical and no longer active. The approved pre-Screen009 Registration/consent layout and routes were restored. Do not use the removed009 node IDs as current destinations.

Status: implemented for user review, 21 October 2026. Do not proceed to Screen 010 without a new request.

## Approved direction

User explicitly selected **“Keep the existing bottom-sheet format.”** The proposed Login-style full-screen overlay was not used. Existing warm-white sheet surfaces, Poppins typography, primary gradient buttons, rounded sheet tops, 26 px horizontal sheet insets and 14 px section gaps were reused. Every mobile frame is 390×844; no additional device-size frames were created.

Location: existing file MR9935oQZACMjndzGIUgq5 → NoorHeroes V2 Design 1128:2 → Onboarding 1270:140 → **009 — Consent Detail / Full Text 1588:337**.

## Reading views

| Document | Frame | Source | Return |
|---|---|---|---|
| Terms & Conditions | 1588:346 | Exact approved draft stack1513:363 | Terms agreement1513:350 |
| Privacy Policy | 1588:381 | Exact approved draft stack1513:401 | Privacy agreement1513:386 |
| Child-data-processing consent | 1588:418 | Same full Privacy Policy1513:401, visibly identified as Privacy Policy | Privacy agreement1513:386 |
| Personalization/AI consent | 1514:354 | Existing draft text1514:381, unchanged | Preferences1511:380 |
| Voice-feature consent | 1514:384 | Existing draft text1514:411, unchanged | Preferences1511:380 |
| Marketing consent | 1514:414 | Existing draft text1514:441, unchanged | Preferences1511:380 |

The three existing optional detail frame IDs were reused and grouped under009. Terms, Privacy and child-data reading views were added; no source/master design was overwritten. The child-data view reuses the approved Privacy text rather than inventing a standalone child-data legal document. This shared-source mapping requires legal review for production.

Each sheet is720px high at y124, with fixed header/Close, a474px vertical document viewport, fixed draft/version status and56px footer action. Optional draft text starts at the viewport origin. Long text remains complete in the scroll container.

## Connections and behavior

Seven Read entry points: existing adult-row Read1459:1103; new Terms/Privacy header Reads1588:614/617; child-data Read1588:620; existing optional Reads1459:1152/1175/1198.

Read → shared loading1588:486 → correct document. Close, footer, backdrop and Escape return to the confirmed invoking agreement/preferences sheet. Read-only views write no required or optional consent choice. The original explicit Terms → close → separate Privacy acknowledgement flow remains in place.

Loading uses the approved329:6 light-dot primary loader, with a still reduced-motion alternative. Default transition is160ms Dissolve; reduced-motion paths are instant. Shared error1588:533 contains Retry; duplicate loading triggers are avoided by replacing the active overlay.

Native controlled scenarios from a reading view: L=online loading, O=offline without cache, C=offline with cached draft, E=load failure, N=online recovery. N also recovers from the error view. These are native prototype fixtures; no real network request or production cache validation occurs.

Missing content disables legal availability and existing account-submission readiness. Existing Terms/Privacy acknowledgement instances now use a Default/Disabled visual-state binding and availability guard. Cancelled loading restores the availability that existed before reading. A failure remains blocking until recovery; cached authorized prototype text remains readable.

## Preservation and necessary dependencies

Login and main Registration layout, copy, inputs, branding, bottom footers and loader styles were not redesigned. Necessary integration changes: Read affordances in agreement sheets, read/return actions, legal-availability-derived readiness and acknowledgement disabled states. Global component masters and original/web/admin designs were not changed. No OTP destination was added.

## Verification

- **96 passing structural/action/geometry checks**, with defaults restored after tests.
- Source paragraphs in Terms/Privacy/child views match their approved source stacks character-for-character. Optional body strings are preserved on their original text node IDs.
- All six viewports, fixed footer clearances,44px Close targets,56px actions and return destinations checked in normal/reduced-motion paths.
- Loading, offline failure, Retry, cached reading, cancelled loading and recovery verified through action interpretation.
- Reading writes no consent choice; entered Registration identifiers are preserved.
- Unavailable-content guards block Terms and Privacy agreement and disable account actions; recovery restores the default acknowledgement state.
- All six reading views and loading/error screenshots reviewed at the standard size. See [contact sheet](2026-10-21_009_Contact_Sheet.png).
- All237 prompt files were read by an inventory scan; Screen009 and relevant A1 source/blueprint/reusable-baseline documents were inspected for this implementation. Later screens were not implemented.

Evidence: [final checks](2026-10-21_009_Final_Verification.json), [node manifest](2026-10-21_009_Node_Manifest.json), [prompt inventory](2026-10-21_009_Prompt_Inventory.json).

Final transition refinement: Read entry and load-result swaps use160ms Dissolve normally and instant transitions with reduced motion. All96 checks rerun and passed: [latest motion-inclusive checks](2026-10-21_009_Final_Motion_Checks.json). Legal acknowledgement visual-state variable1597:310; prior-availability snapshot1594:310.

## Open item and limits

No approved published consent version number exists in the inspected draft sources. The visible footer says **“Version pending legal review”** and **“Prototype draft · Legal review required.”** No version number/date was fabricated. The PRD's production-version-number criterion remains open until approved versioned legal documents are supplied.

Figma Present playback, real screen-reader/focus restoration, production legal approval and actual network/cache behavior remain unverified. Figma browser access restrictions were respected. Native action interpretation does not establish Present playback.
