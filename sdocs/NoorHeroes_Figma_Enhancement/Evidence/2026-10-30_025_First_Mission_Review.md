# Screen 025 — First Mission review
Applied in existing Figma V2 on 30 October 2026. Ready for user review; do not proceed to026 without approval.

## Scope and approval
File MR9935oQZACMjndzGIUgq5, mobile page928:2, existing V2 section1128:2.
Read prompts025–033, A1 PRD (FR18, screen inventory25, First Mission summary), KMP blueprint08 and current Screens022–024 baseline. Existing V2 was reused; no duplicate V2 or new file.
Screen025's original copy/reference gap was raised. User explicitly chose: **Use existing app copy; keep destinations pending.**
No existing Picker, Child Lock, recovery, original, web/admin or application code was edited. This is a native editable Figma review screen, not a production mission implementation.

## Nodes
| Role | Node |
|---|---|
| Section025 |2368:12500|
| First-visit screen |2368:12507|
| Mission unavailable |2368:12580|
| Reduced motion |2372:12598|
| External review controls |2368:12652|
| Preview first visit / unavailable / reset demo flags |2368:12655 /2368:12660 /2368:12665|
| Preview reduced motion |2372:12978|
| Local simulation collection |VariableCollectionId:2368:12501|

## Content and presentation
Exact current English app strings reused from core/core-common/src/commonMain/composeResources/values/strings.xml, first_mission_*:
- FIRST MISSION
- Welcome to NoorHeroes, %1$s!
- Start your journey with your very first adventure.
- Meet Your Noor Companion
- Explore the magical world and learn your first daily Dua together!
- Start First Mission
- Go to Home
The unavailable title, Mission unavailable, is the explicit state label from prompt025 §6. No unavailable body text, religious passages, rewards or verification badge was invented.
This does not establish a verified content ID, scholar provenance or a real recommended mission assignment. The approved app copy is used for UI review only.

All mobile states390×844, current night/teal background and approved wordmark, cream366×738 main card at12/82. NH Poppins styles and existing semantic paints reused. Fixed intro and footer, bounded inner scrolling. Intro includes Attention badge502:20; controls reuse NH/Button322:21 and322:81 disabled variants. Hero star is the exact existing approved star SVG exported from2268:12085; corrected SVG dimensions preserve its vector shape. Entire UI remains editable text/components/layout; no full-screen raster capture used.
No new palette or shared/global component masters were changed.

## Interaction boundary
- Start First Mission and Go to Home are visibly disabled and have no reactions, per explicit user decision. Child Home and assigned-content destinations remain pending.
- No existing Profile Picker/Child Lock entry was wired into025. No lock/entitlement checks or child-mode activation were bypassed.
- External review controls can preview the first visit for the currently selected child. Three local shown flags mirror the three existing demo profiles.
- On display, the selected child's shown flag is recorded immediately, following blueprint08. Repeat entry through the review controller is suppressed for that child; another child remains eligible.
- Welcome text reads the selected-child Context name. Only new025 variables are written; no existing auth/lock/profile variables are mutated.
- Review reset clears only025 demo flags.
- Unavailable preview does not consume the first-visit flag. The real fallback/return route remains pending with Home.
- Opening a Figma frame directly is a review bypass, not an application entry gate. Flags are prototype-session data, not durable per-child storage.
- Reduced-motion review keeps approved star shapes as static editable SVG vectors; shared star components were not changed. Its review navigation uses100ms dissolve.

## Verification
47/47 checks passed against actual saved Figma reaction JSON and structural bounds:
- First display, per-child independence, repeated-entry suppression and reset for all three demo profiles.
- Dynamic greeting and punctuation; exact visible app-copy comparison.
- Unavailable state does not consume a mission impression.
- All three states retain standard size/card height, safe fixed footer, only-inner scroll, Poppins and editable component UI.
- Product actions stay disabled/unmapped. Review destinations exist and no shared security variables are written.
- Long-name QA (Abdurrahman Yusuf) wraps without overlap; temporary QA clone removed.
- Reduced-motion artwork has no animation tracks/styles.
Composition screenshots inspected: 2026-10-30_025_First_Visit.png, _Unavailable.png, _Reduced_Motion.png.
Read-only design-system search found no published matches; actual local NH component masters were inspected and reused.
An initial visual issue with cloned vector rescaling was fixed using the source SVG. Figma accepted only if/else-style multi-block serialization, so per-child conditions were flattened into separate condition actions and re-read/tested.

Evidence: 2026-10-30_025_First_Mission_Checks.json; 2026-10-30_025_First_Mission_Ledger.json.

## Limits and next review
Stored-graph evaluation and screenshots do not verify live Present playback, screen readers, device safe areas, OS reduced motion, APIs, real authentication, mission playback or durable once-only storage.
No Child Home, verified mission content or launch target was invented.
Screen025 prompt §11 says: **Stop and wait for my review and approval before moving to another screen.**
Next:026 Forced Update only after025 approval. Prompts026–033 are reviewed for their sequence/source gaps but have not been designed.

## Later prompt source gaps, deferred until their review turn
-026–029 need exact current bootstrap/update/maintenance/offline copy, approved platform store handoff and state-specific retry behavior.
-030 must use enumeration-safe existing OTP recovery context and a verified recovery destination, not a parent/child PIN bypass.
-031–033 require the same legal source/version as existing consent detail. Earlier user-approved NoorHeroes text is draft/legal-review-required; never relabel it production-approved legal copy. Preserve existing bottom-sheet decisions until the specific full-document direction is resolved.

