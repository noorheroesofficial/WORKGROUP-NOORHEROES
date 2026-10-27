**Mandatory finalized visual baseline:** Read and apply [Finalized V2 Reusable Design Prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) before implementing this screen. Its latest approved visual rules supersede older conflicting design proposals below; PRD behavior and exact approved content remain authoritative.

# Screen 082 — Arabic Letters — Contextual Form Matching (Isolated / Initial / Medial / Final)

**Documentation only. Execute this prompt only after the documentation and this screen's unresolved decisions are approved. Stop after this screen.**

## 1. Screen identification

- Feature/sub-feature: **A5 — Arabic Letters — Contextual Form Matching (Isolated / Initial / Medial / Final)**.
- Surface: **state**. Number is controlled review order, not a forced linear user journey.
- Execution status: **BLOCKED for exact approved copy: no exact Frame 1 counterpart verified. Do not fabricate copy, Arabic, educational items, user data or stats.**.
- Journey entry / previous screen: A5-08 Hear & Match or A5-10 Word Context selected by content metadata.
- Next screen(s) / result: Same owning Arabic exercise flow; no new top-level route.
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: [Feature_A5_Quran_Arabic_Learning.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Child App (1-12)/Feature_A5_Quran_Arabic_Learning.md>); **§1.7 FR-6; absent from §1.18 rows 8–11**.
- Current mobile reference: **Missing independently mapped current-site screen.**
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: **Missing corresponding screen reference.** Do not substitute a visually related hub as functional evidence.
- Frame 2 container: `1085:13003`; visual reference: [Quran & Arabic Learning](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1085-16521) — `1085:16521`. Related enhanced feature hub for visual patterns only; not an exact screen equivalent
- Reference qualification: ['Independent review layout required; existing blueprint defines a content-metadata variant, not a new screen route. Exact exercise catalog unavailable.'].
- Existing screenshot candidates (one-to-one identity is not asserted unless verified in research):
- Missing corresponding local screen reference.
- Blueprint alignment:
- [05-arabic-letters-learning-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A5_Quran_Arabic_Learning/KMP/05-arabic-letters-learning-flow.md>)
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: - CL-11: required mechanic absent from source screen inventory. See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

Enable Arabic Letters — Contextual Form Matching (Isolated / Initial / Medial / Final) in the established A5 journey. Entry: Arabic Letters mode selector / scheduled node practice. Required outcome: Per-answer teaching feedback; Skill Tree progress after bounded exercise.

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

**FR-5** Quran Game modes must include at minimum: ayah ordering, listen-and-select matching ayah, find-the-missing-word, surah-name-to-theme matching (child-safe/approved context only), recitation echo with pronunciation coaching, and progressive-reveal memorization (source §21.9 "Quran Game" game ideas).

**FR-6** Arabic Letters module must include: hear-and-match, tracing, isolated/initial/medial/final form matching, harakah (diacritic) sound pairing, find-the-letter-in-an-approved-word, build-a-word-from-sound-tiles — with spaced review scheduling applied across sessions (source §21.9 "Arabic Letters").

**FR-7** Arabic Letter detailed flow: play phoneme → child selects 1-of-4 letters → child traces the correct shape → letter shown in a familiar word → scheduled for spaced review. Mastery requires correct performance across different question forms and across more than one session (not masterable in a single sitting) — source §21.9.

**FR-6** Arabic Letters module must include: hear-and-match, tracing, isolated/initial/medial/final form matching, harakah (diacritic) sound pairing, find-the-letter-in-an-approved-word, build-a-word-from-sound-tiles — with spaced review scheduling applied across sessions (source §21.9 "Arabic Letters").

**FR-7** Arabic Letter detailed flow: play phoneme → child selects 1-of-4 letters → child traces the correct shape → letter shown in a familiar word → scheduled for spaced review. Mastery requires correct performance across different question forms and across more than one session (not masterable in a single sitting) — source §21.9.

**FR-18** Hint system: hints must be progressive/partial (e.g., eliminate one wrong option, reveal the first letter) rather than immediately revealing the full answer; hint usage is tracked as a data point (`hint_count`) feeding the mastery-confidence calculation, not treated as a penalty visible to the child.

## 4. Exact content specification

### Requirement-driven fields and content roles

- Not supplied by this source; resolve before execution.

**Exact copy unavailable: execution blocked for copy-dependent design.** Locate the authoritative content registry/original frame; do not insert placeholder, paraphrased or AI-generated copy. This document still specifies the required surface so it is not omitted.

Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.

## 5. Visual enhancement instructions

- Metadata-driven contextual letter-form matching variant within Hear & Match/Word Context. Present verified isolated/initial/medial/final form labels and approved glyph options or contextual word positions. Tap-to-match has textual accessible labels; never infer joining form from unverified content.

- Preserve content order and screen purpose. Use a vertical auto-layout content stack; horizontal inset 20, base spacing 4/8/12/16/24/32; card content padding 12–16. Keep compact controls next to their labels; align headings and cards to one column edge.
- Use existing cream `#FAF7F0`, surface `#FFFFFF`, ink `#1C2B33`, teal `#0E7C7B`, gold `#D4A24C`. Gold/bright teal are accents, not untested small-text colors. Body 14/16; heading 20/24; brand-only display 28/32. Preserve actual font assets; PRD Latin sans, display serif, separate verified Arabic content font.
- Do not import Frame 2's sample statistics, claims, religious text, section additions or combined desktop layouts. Borrow hierarchy, restrained surface separation and image framing only where they support this surface.
- Screen viewport is separate from long content height. Use vertical overflow when content exceeds available height; header/footer may be fixed only with bottom and top content clearance. At 320/360/390/420 logical widths, long labels wrap. At 200% text scale, stack grids or allow scrolling; no fixed text block height or sacred-text ellipsis.
- Essential touch target≥44×44 logical units; younger-child primary tasks≥56 where A2 specifies. Decorative icons have no hit targets. Assets retain aspect ratio; no text burned into illustrations. Safe area and keyboard must never obscure the current action.
- Source frames, unrelated screens and existing design direction remain unchanged. Token/component changes require separate review; never detach or globally mutate a source instance to fix this screen.

## 6. Screen states and conditional scenarios

- Ready with verified question/content metadata
- Answer selected; Submit available only when required answer complete
- Submitting; non-blocking retry retains answer and idempotency context
- Supportive answer/explanation or next exercise step
- Progressive hint active; dismiss restores selected answer
- Downloaded lesson offline with queued evidence; unavailable media has retry
- Leaving returns to owner node; mastery requires multiple formats and genuinely separated sessions



Only apply states that belong to this surface. List-only empty/skeleton states are not added to legal documents or static intros. Network submit has a pending/timeout/retry result; retry preserves draft and must not duplicate a server-confirmed operation. Voice states need consent + OS grant; denial supplies listen/text/manual alternative. Loading/error/disabled/offline wording missing from source is a content approval gap.

<details><summary>Authoritative state/edge source context — apply screen-relevant cases, not all cases indiscriminately</summary>

Use the linked PRD §1.10–1.15 and the independently mapped states above; unspecified messages remain blocked.

</details>

## 7. Interactions and navigation

- {"element": "Form label / verified glyph option", "trigger": "Tap or stated accessible gesture", "precondition": "Correct active child and verified source exercise content available", "behavior": "Match specified contextual form using published question metadata", "destination": "Current exercise state", "validation": "Correctness uses published content metadata; no invented answers or raw mastery score. Preserve selection when retrying a failed submission.", "back_cancel": "Return to invoking node/mode with saved committed progress; dismiss hint returns to exercise. Never issue duplicate reward.", "unavailable": "Loading media cannot submit a fabricated answer; provide retry or source-defined non-blocking fallback. Parent-disabled recording uses listen-only."}
- {"element": "Submit match", "trigger": "Tap or stated accessible gesture", "precondition": "Correct active child and verified source exercise content available", "behavior": "Record matching evidence then resume owning Arabic flow", "destination": "Current exercise state", "validation": "Correctness uses published content metadata; no invented answers or raw mastery score. Preserve selection when retrying a failed submission.", "back_cancel": "Return to invoking node/mode with saved committed progress; dismiss hint returns to exercise. Never issue duplicate reward.", "unavailable": "Loading media cannot submit a fabricated answer; provide retry or source-defined non-blocking fallback. Parent-disabled recording uses listen-only."}

For every action below, use the cited preconditions and source validation. Preserve the invoking route and selected child. Back/cancel dismisses only the current overlay or returns to the invoking screen, preserving drafts and completed progress where specified. Unavailable actions remain visibly labeled with their reason and never activate. Permission prompts occur only after parent consent and a deliberate related action. A prototype simulates outcomes; it never validates identity, grants permissions, charges money or mutates production data.

Verified current-preview controls, retained to prevent omitted clickable elements:

- Not supplied by this source; resolve before execution.

For any captured control absent from an explicit action above, reconcile it against the screen-specific source below before wiring. Do not connect it to a convenient unrelated screen. Mark it **unresolved, non-executable** until its actual destination/state is confirmed; the navigation appendix reports this limitation. Decorative source-layer names are not automatically click targets.

<details><summary>Screen-specific PRD specification / click behavior</summary>

No independently named per-screen UX subsection exists. The PRD screen inventory entry, feature click-target table and functional requirements remain the authority; use research evidence and resolve unmatched targets before execution.

</details>

## 8. Motion and animation specification

| Trigger | Start → end / direction | Timing | Interruption / leave | Reduced motion | Figma approach |
|---|---|---|---|---|---|
| State response changes | Previous state→new labeled state; no decorative entrance | 120ms dissolve;no delay | Interruptible; ignore stale completion after leaving | Instant replace with same labels | State variants via Change to or separately labeled scenario frames |
| Press/release enabled control | Rest→pressed→rest; preserve hit area | 100ms ease-out scale.96 (proposal);0ms delay | Release/cancel reverses; disabled has no activation | Color/border pressed feedback only | While pressing → Change to pressed; On click → approved action |



Timing not quoted from the PRD is a labeled design proposal. No loop, flashing or parallax is required. Animate compositor-friendly opacity/transform; never delay an enabled essential action. Stop all animation/media/recording simulation on leave; no second reward reveal on restore. Status/validation always has visible text/icon independently of motion.

## 9. Figma implementation instructions — future approved execution

1. Open the exact page/node links in section2. Confirm the source text/identity; stop if the references disagree or required copy is unavailable.
2. Locate the approved reference frame. Duplicate only that frame into a user-approved enhanced-design working area; preserve original nodes and IDs. If no frame exists, create only the missing requirement-driven surface after its layout/copy approval, using approved shared assets.
3. Create `NH/Enhanced/082/Arabic_Letters_Contextual_Form_Matching_Isolated_Initial_Medial_Final/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/Arabic_Letters_Contextual_Form_Matching_Isolated_Initial_Medial_Final`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] A5 behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
- [ ] Every captured product control has an approved trigger, precondition, destination/state and cancel/back result; no unresolved control is silently wired.
- [ ] Applicable states are visibly reviewable; retry/draft/permission-denial/resume behavior matches the cited rules. No irrelevant states were added.
- [ ] All body text/background pairs≥4.5:1 and large text≥3:1; status has text/icon, not color alone.
- [ ] Touch targets≥44×44; no clipped text or action overlap at320/360/390/420 widths or200% text scaling; Arabic/Urdu RTL tested with numeral exceptions.
- [ ] Motion timing/interruptibility matches section8; reduced motion retains all feedback; navigation is immediately available.
- [ ] Reference IDs and any new working-node IDs recorded; original and unrelated nodes unchanged.
- [ ] Sample data/price/religious verification provenance is identified; missing legal/localized/educational content blocks execution rather than being fabricated.
- [ ] Default and relevant alternate states captured as evidence and compared; screen approved by user before proceeding.

## 11. Review and correction instructions

Implement only this screen and its necessary local dependencies after approval. Do not modify unrelated screens or source frames. Report inaccessible references, missing requirements and unmatched controls. List changes, exact-copy comparison and acceptance checks performed, with evidence and created node IDs. Record unresolved questions. **Stop and wait for my review and approval before moving to another screen.**
