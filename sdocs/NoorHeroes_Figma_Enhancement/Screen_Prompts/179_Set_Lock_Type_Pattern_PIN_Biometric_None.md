**Mandatory finalized visual baseline:** Read and apply [Finalized V2 Reusable Design Prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) before implementing this screen. Its latest approved visual rules supersede older conflicting design proposals below; PRD behavior and exact approved content remain authoritative.

# Screen 179 — Set Lock Type (Pattern/PIN/Biometric/None)

**Documentation only. Execute this prompt only after the documentation and this screen's unresolved decisions are approved. Stop after this screen.**

## 1. Screen identification

- Feature/sub-feature: **C23 — Set Lock Type (Pattern/PIN/Biometric/None)**.
- Surface: **screen**. Number is controlled review order, not a forced linear user journey.
- Execution status: **Requirement-driven missing reference; exact labels/content need approval before execution**.
- Journey entry / previous screen: Child Locks & Sessions.
- Next screen(s) / result: Child Locks & Sessions (saved).
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: [Feature_C23_Parental_Controls.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Parent Area In-App (19-26)/Feature_C23_Parental_Controls.md>); **§1.18 row 7; §1.7; §2; §6; §13**.
- Current mobile reference: [NoorHeroes current preview](https://noorheroes.figma.site/) → selector **Missing in inspected site catalogue**; exact text captured below.
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: **Missing corresponding screen reference.** Do not substitute a visually related hub as functional evidence.
- Frame 2 container: `1085:13003`; visual reference: **Missing corresponding screen reference.** Do not substitute a visually related hub as functional evidence.
- Reference qualification: No independently verified equivalent for this screen; global style inspiration must not replace approved copy.
- Existing screenshot candidates (one-to-one identity is not asserted unless verified in research):
- Missing corresponding local screen reference.
- Blueprint alignment:
- [01-controls-landing-navigation.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C23_Parental_Controls/KMP/01-controls-landing-navigation.md>)
- [02-screen-time-settings-usage-display.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C23_Parental_Controls/KMP/02-screen-time-settings-usage-display.md>)
- [03-quiet-hours-bedtime-settings.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C23_Parental_Controls/KMP/03-quiet-hours-bedtime-settings.md>)
- [04-ai-permissions-settings.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C23_Parental_Controls/KMP/04-ai-permissions-settings.md>)
- [05-content-age-level-settings.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C23_Parental_Controls/KMP/05-content-age-level-settings.md>)
- [06-child-locks-sessions-management.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C23_Parental_Controls/KMP/06-child-locks-sessions-management.md>)
- [07-usage-heartbeat-manager-offline-failclosed-engine.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C23_Parental_Controls/KMP/07-usage-heartbeat-manager-offline-failclosed-engine.md>)
- [08-restriction-enforcement-ui-calm-rest-bedtime-block.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C23_Parental_Controls/KMP/08-restriction-enforcement-ui-calm-rest-bedtime-block.md>)
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: No screen-specific ID supplied; still check global G-01–G-10 and source content differences. See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

Give verified parents per-child healthy usage, AI, content eligibility and lock/session controls within the platform safety ceiling. Screen-specific role: Set Lock Type (Pattern/PIN/Biometric/None).

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

The complete feature obligations are retained in [every-FR register](../10_REQUIREMENT_COVERAGE_REGISTER.md); section 2 identifies the exact screen-inventory row.

## 4. Exact content specification

### Requirement-driven fields and content roles

- None/Pattern/PIN/device biometric
- Configured credential input
- Save

**Exact copy unavailable: execution blocked for copy-dependent design.** Locate the authoritative content registry/original frame; do not insert placeholder, paraphrased or AI-generated copy. This document still specifies the required surface so it is not omitted.

Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.

## 5. Visual enhancement instructions

- Screen scope: Set Lock Type (Pattern/PIN/Biometric/None). Arrange only these vertical content roles: None/Pattern/PIN/device biometric → Configured credential input → Save. Use one clear heading and context row; source-approved primary action follows this screen content. Reuse local shared components without pulling other module sections onto this screen. Retain verified source content order where it differs; required missing content requires source approval before placement.

- Preserve content order and screen purpose. Use a vertical auto-layout content stack; horizontal inset 20, base spacing 4/8/12/16/24/32; card content padding 12–16. Keep compact controls next to their labels; align headings and cards to one column edge.
- Use existing cream `#FAF7F0`, surface `#FFFFFF`, ink `#1C2B33`, teal `#0E7C7B`, gold `#D4A24C`. Gold/bright teal are accents, not untested small-text colors. Body 14/16; heading 20/24; brand-only display 28/32. Preserve actual font assets; PRD Latin sans, display serif, separate verified Arabic content font.
- Do not import Frame 2's sample statistics, claims, religious text, section additions or combined desktop layouts. Borrow hierarchy, restrained surface separation and image framing only where they support this surface.
- Screen viewport is separate from long content height. Use vertical overflow when content exceeds available height; header/footer may be fixed only with bottom and top content clearance. At 320/360/390/420 logical widths, long labels wrap. At 200% text scale, stack grids or allow scrolling; no fixed text block height or sacred-text ellipsis.
- Essential touch target≥44×44 logical units; younger-child primary tasks≥56 where A2 specifies. Decorative icons have no hit targets. Assets retain aspect ratio; no text burned into illustrations. Safe area and keyboard must never obscure the current action.
- Source frames, unrelated screens and existing design direction remain unchanged. Token/component changes require separate review; never detach or globally mutate a source instance to fix this screen.

## 6. Screen states and conditional scenarios

- Default for Set Lock Type (Pattern/PIN/Biometric/None) Applicable pending/success/error only for actions explicitly named in action_rules Cached offline read only where supported; online-only mutations show sourced reconnect reason Back/cancel restores invoking context; actual unresolved source behavior blocks execution



Only apply states that belong to this surface. List-only empty/skeleton states are not added to legal documents or static intros. Network submit has a pending/timeout/retry result; retry preserves draft and must not duplicate a server-confirmed operation. Voice states need consent + OS grant; denial supplies listen/text/manual alternative. Loading/error/disabled/offline wording missing from source is a content approval gap.

<details><summary>Authoritative state/edge source context — apply screen-relevant cases, not all cases indiscriminately</summary>

### 1.10 Edge Cases

1. A child is mid-quiz when the daily screen-time limit is reached → the current question is allowed to complete and the score saved, then the rest screen appears — consistent with the platform's general "never lose in-progress reward-eligible progress due to a restriction" principle.
2. A child's bedtime window begins while they are mid-episode of a Story (not specifically a Quran lesson, but a similar "don't cut off mid-content" concern applies) → playback pauses at the nearest natural content boundary (e.g., end of the current scene/segment) rather than literally mid-sentence, generalizing FR-5's Quran-specific example to all content types with a similar respect-for-content-boundaries principle.
3. A parent grants a screen-time override while the child's session is already in the "calm rest screen" blocked state → the override should unblock that same session immediately (the child doesn't need to fully exit and re-enter), consistent with a smooth, non-punitive parent-assist experience.
4. A child is offline when their locally-cached signed policy's grace period expires (e.g., several days of being offline well past the policy's signed validity window) → the app fails closed, applying the most conservative reasonable restriction (e.g., treating it as if the daily limit were already reached) rather than failing open to unlimited use, consistent with FR-4's "never unlimited when disconnected" rule.
5. A parent changes a child's screen-time limit mid-session (e.g., lowering it from another device while the child is actively using the app) → consistent with the platform's general "changes apply at next session" pattern (already established for screen-time/bedtime elsewhere), the active session is not abruptly interrupted by this specific kind of change, though a bedtime-window change taking effect mid-session is a distinct, generally hard-enforced cutoff per FR-2 item 5 regardless of when it was configured (bedtime windows are evaluated against current time continuously, not "locked in" at session start the way a daily-limit value might be).
6. A parent disables AI for a child while that child is mid-recitation-attempt in A.5's pronunciation flow → consistent with A.5's own established edge case (§1.10 Edge Case 2), the in-progress UI gracefully exits to listen-only mode on the next app-state check, never leaving a dangling broken control.
7. Two co-guardians on different devices simultaneously adjust the same child's screen-time limit to different values → standard last-write-wins semantics apply (consistent with the platform's general low-stakes-preference-conflict handling, distinct from the optimistic-concurrency protection applied to higher-stakes actions like child deletion in C.21) — this is a low-risk-enough setting that a simple last-write-wins is acceptable, though the resulting value is always clearly visible to both parents on next view.
8. A Content Age Level override would place a child's eligible band *below* their actual DOB-derived band (a parent choosing more conservative content) → this is fully supported and respected identically to an above-DOB-band override; the system has no asymmetric restriction on which direction a parent can adjust.
9. A device is revoked from Child Locks & Sessions while that device is mid-API-call (e.g., submitting a habit check-in at the exact moment of revocation) → the in-flight request is allowed to complete if it was already authenticated before the revocation took effect (avoiding data loss for an action the child had already legitimately initiated), but any subsequent request from that device fails authentication immediately after.
10. A parent attempts to set a daily screen-time limit of 0 minutes (effectively fully blocking a child) → this is accepted as a valid, if unusual, configuration (a parent's prerogative), resulting in the child immediately seeing the calm rest screen on any session attempt, with no special-casing or warning beyond standard confirmation of the setting being saved.

### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Device clock manipulated | Server-authoritative counter unaffected; usage evaluated against signed server time |
| Offline beyond signed grace period | Fails closed to the most conservative restriction state (Edge Case 4) |
| Bedtime cutoff mid-content | Stops at the nearest natural content boundary, never mid-word/mid-sentence (FR-5/Edge Case 2) |
| Parent override requested while child is blocked | Unblocks the existing session immediately, no re-entry required (Edge Case 3) |
| AI disabled mid-recitation-attempt | In-progress UI gracefully exits to listen-only on next app-state check (Edge Case 6) |
| Device revoked mid-in-flight-request | Already-authenticated in-flight request completes; subsequent requests fail immediately |

### 1.12 Empty States
- A child with no screen-time policy configured yet → defaults to no daily limit (unrestricted) with a clear "no limit set" indicator on the Controls screen, never an ambiguous blank field.

### 1.13 Loading States
- Controls screens: skeleton form shimmer while current settings load.

### 1.14 Offline States
- Controls screens themselves require connectivity to save changes (server-authoritative); viewing current settings may render from cache with a staleness indicator.

### 1.15 Permission States
- No new runtime permissions; microphone-related AI Permissions settings here govern *server-side* feature availability, distinct from the OS-level microphone permission itself (both must be true for recording features to appear, per A.5's established pattern).



</details>

## 7. Interactions and navigation

- Select none/pattern/PIN/OS biometric → only applicable input/enrollment path
  Save → fresh Parent Gate → persist only salted hash/OS assertion; return selected Child Locks & Sessions
  OS biometric unavailable → hide unavailable choice and offer configured alternative
  Cancel → original lock unchanged

For every action below, use the cited preconditions and source validation. Preserve the invoking route and selected child. Back/cancel dismisses only the current overlay or returns to the invoking screen, preserving drafts and completed progress where specified. Unavailable actions remain visibly labeled with their reason and never activate. Permission prompts occur only after parent consent and a deliberate related action. A prototype simulates outcomes; it never validates identity, grants permissions, charges money or mutates production data.

Verified current-preview controls, retained to prevent omitted clickable elements:

- Not supplied by this source; resolve before execution.

For any captured control absent from an explicit action above, reconcile it against the screen-specific source below before wiring. Do not connect it to a convenient unrelated screen. Mark it **unresolved, non-executable** until its actual destination/state is confirmed; the navigation appendix reports this limitation. Decorative source-layer names are not automatically click targets.

<details><summary>Screen-specific PRD specification / click behavior</summary>

Screen: Set Lock Type (Pattern/PIN/Biometric/None)
Source PRD_Documents/Parent Area In-App (19-26)/Feature_C23_Parental_Controls.md §1.18 row 7; §1.7; §2; §6; §13
Purpose: Give verified parents per-child healthy usage, AI, content eligibility and lock/session controls within the platform safety ceiling. Screen-specific role: Set Lock Type (Pattern/PIN/Biometric/None).
Fields: None/Pattern/PIN/device biometric; Configured credential input; Save
Action contract:
Select none/pattern/PIN/OS biometric → only applicable input/enrollment path
Save → fresh Parent Gate → persist only salted hash/OS assertion; return selected Child Locks & Sessions
OS biometric unavailable → hide unavailable choice and offer configured alternative
Cancel → original lock unchanged
States:
Default for Set Lock Type (Pattern/PIN/Biometric/None) Applicable pending/success/error only for actions explicitly named in action_rules Cached offline read only where supported; online-only mutations show sourced reconnect reason Back/cancel restores invoking context; actual unresolved source behavior blocks execution

</details>

## 8. Motion and animation specification

| Trigger | Start → end / direction | Timing | Interruption / leave | Reduced motion | Figma approach |
|---|---|---|---|---|---|
| Approved forward/back action | Current frame→destination, preserving directional history | 250ms ease-in-out;no delay | Reversible with Back; cancel pending animation when leaving | Instant navigation or ≤100ms dissolve | Navigate to + Dissolve; matched-layer Smart Animate only after layer-name/structure check |
| Press/release enabled control | Rest→pressed→rest; preserve hit area | 100ms ease-out scale.96 (proposal);0ms delay | Release/cancel reverses; disabled has no activation | Color/border pressed feedback only | While pressing → Change to pressed; On click → approved action |



Timing not quoted from the PRD is a labeled design proposal. No loop, flashing or parallax is required. Animate compositor-friendly opacity/transform; never delay an enabled essential action. Stop all animation/media/recording simulation on leave; no second reward reveal on restore. Status/validation always has visible text/icon independently of motion.

## 9. Figma implementation instructions — future approved execution

1. Open the exact page/node links in section2. Confirm the source text/identity; stop if the references disagree or required copy is unavailable.
2. Locate the approved reference frame. Duplicate only that frame into a user-approved enhanced-design working area; preserve original nodes and IDs. If no frame exists, create only the missing requirement-driven surface after its layout/copy approval, using approved shared assets.
3. Create `NH/Enhanced/179/Set_Lock_Type_Pattern_PIN_Biometric_None/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/Set_Lock_Type_Pattern_PIN_Biometric_None`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] C23 behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
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
