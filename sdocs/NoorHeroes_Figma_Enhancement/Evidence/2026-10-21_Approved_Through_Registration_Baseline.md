# Approved NoorHeroes V2 baseline — through Registration

Saved 21 October 2026 following the user's confirmation: “Correct design until registration done no changes required, save context for next and or future reference.”

## Approval and scope

The current design through Registration is finalized and accepted by the user. This includes Splash, Language Selection, the four Intro screens, Login, Registration, and their current consent/preferences sheets, loading and error treatments. Do not redesign, adjust, rebuild, migrate, or reconnect these approved screens without a new explicit request. No next screen has been selected or authorized by this confirmation.

This is design approval. It does not assert production authentication, legal approval, backend integration, device-keyboard verification, or Figma Present playback.

## Resume references

- Existing file: `MR9935oQZACMjndzGIUgq5`; Mobile page `928:2`.
- Main section: **NoorHeroes V2 Design** `1128:2`; current module **Onboarding** `1270:140`.
- Login: screen `1355:2696`, section `1355:2565`.
- Registration: screen `1459:256`, section `1459:216`.
- Shared approved symbol: `1299:19`; linked wordmark: `1345:1449`. Preserve existing screen-specific size, transparency and placement.
- [Current context](../CURRENT_CONTEXT_AND_NEXT_SCREEN.md) — latest dated entries supersede historical measurements.
- [Reusable design prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) — apply automatically to future equivalent roles.
- [Latest implementation and verification handoff](2026-10-21_NH_Input_Handoff.md).
- [Final native action checks](2026-10-21_NH_Input_Final_Action_Checks.json).

## Standards to preserve

- Design new screens at **390×844** only, inside the existing V2 file. Create a module section only when starting that PRD module. Do not create all future sections upfront.
- Use finalized screens as the visual source of truth. Preserve Poppins role styles, semantic colors, existing branding, icon meaning, alignment, Auto Layout, cards and component treatments. PRD/blueprints remain authoritative for functionality, subject to explicit user decisions.
- Intro bottom icon canvases: **14×14 px**, centered artwork, **2 px** icon-to-text gap, with optical balance. Preserve current transparent controls, compact supporting pills and existing navigation/motion.
- Authentication card/content widths at the standard viewport: **366/338 px**. Preserve current **14 px** section gaps and card padding; use actual component-specific internal padding rather than imposing 14 px universally.
- NH TextField source **357:2**, boundary reference **356:127**: **56 px** boundary, **8 px vertical / 16 px horizontal** internal padding, **12 px** radius, Poppins **16/26** value text. Total label/input group **88 px** normally, **116 px** with error. These supersede older 72/104 px field-group values.
- Consuming NH TextField instances: Login `1563:936`, Registration `1563:1399`; retain Empty/Filled/Focused/Error bindings and country selection overlays.
- Buttons retain **56 px** height and their approved appearance during loading. Send code/Create use **329:6** light dots on the primary gradient. Google uses **329:33** dark dots on its white surface; Send code remains visible but disabled during Google processing. No extra visible “Creating account...” line.
- Reuse NH Button **322:99**, Loading Button **329:49** and Snackbar **1420:18**. Snackbar has square corners, dark **#1C2B33**, Poppins 12 px message, gold Retry action and appropriate per-outcome visibility. Do not revive obsolete local masters/sections.
- Keep compact Registration consent copy and existing checkbox/text alignment, current Optional preferences spacing, fixed bottom account footers, and separate scrolling legal sheets. Main Registration content remains fixed/non-scrollable as approved.
- Terms → close first sheet → separate Privacy sheet. Retain adult and child-data consent gates; optional Personalization/AI, Voice-feature and Marketing remain independent and initially unchecked. Legal/sample content remains draft and fictional.
- Connect only confirmed existing destinations. **OTP remains pending approval and unmapped.** Do not invent a placeholder screen or route.

## Functional companion and verification boundary

Code Layers are disabled on this Figma account. User approved maintaining editable Figma plus the existing local companion under `Authentication_Redesign_2026-10-18/prototype/`.

Run `node server.cjs` there and open `http://127.0.0.1:8766/`. Active runtime: `app-v2.js`, `auth-core.cjs`, `auth-v2.css`, `server.cjs`. The older port 8765 server is separate. The companion supports true typing, international validation, controlled HTTP errors, Snackbar recovery, consent gates, duplicate guards and Retry-After. It calls no production authentication/OAuth service. Draft values persist in RAM across local navigation/errors; language uses localStorage.

Latest evidence: five passing automated test groups, 32 passing native action-interpreter checks, eight variant mappings and 245-country asset/data checks; browser and screenshot checks documented in the handoff. Native Figma uses controlled presets, not arbitrary text input or real HTTP. Figma Present, real device keyboard and production services remain unverified. These limits do not reopen the user's finalized visual approval.

## Start the next task

Read this baseline, current context and reusable prompt. Inspect live Figma read-only to account for any manual edits. Read the newly requested screen's Markdown prompt and relevant PRD/blueprint. Reuse approved patterns; change only the newly authorized screen and its necessary dependencies. Preserve all approved screens and original/web/admin designs. Stop for the user's review at the appropriate screen gate.
