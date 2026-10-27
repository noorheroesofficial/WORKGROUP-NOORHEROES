**Mandatory finalized visual baseline:** Read and apply [Finalized V2 Reusable Design Prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) before implementing this screen. Its latest approved visual rules supersede older conflicting design proposals below; PRD behavior and exact approved content remain authoritative.

# Screen 237 — Family Member Invite

**Documentation only. Execute this prompt only after the documentation and this screen's unresolved decisions are approved. Stop after this screen.**

## 1. Screen identification

- Feature/sub-feature: **F36 — Family Member Invite**.
- Surface: **screen**. Number is controlled review order, not a forced linear user journey.
- Execution status: **Pending documentation approval and screen-specific source reconciliation**.
- Journey entry / previous screen: Contextual entry in source narrative.
- Next screen(s) / result: Parent Settings/Report→generate own-family read-only link; copy/share with parent gate; recipient without app graceful install/account prompt; expiry/auth access contract unverified..
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: [Feature_F36_Ramadan_Mode.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Cross-Cutting System Features (35-37)/Feature_F36_Ramadan_Mode.md>); **§1.7; §1.18; §2.2–2.3; §1.10–1.15**.
- Current mobile reference: [NoorHeroes current preview](https://noorheroes.figma.site/) → selector **⑳ Family Member Invite**; exact text captured below.
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: **Missing corresponding screen reference.** Do not substitute a visually related hub as functional evidence.
- Frame 2 container: `1085:13003`; visual reference: [Family Ramadan Dashboard & Certificate (Refined)](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1085-22850) — `1085:22850`. 
- Reference qualification: Any feature-hub mapping is visual-only; compare exact screen identity before execution..
- Existing screenshot candidates (one-to-one identity is not asserted unless verified in research):
- [Parent-Family Member Invite.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Ramadan Mode/Parent-Family Member Invite.png>)
- Blueprint alignment:
- [01-ramadan-countdown-prep-checklist-themed-home.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/F36_Ramadan_Mode/KMP/01-ramadan-countdown-prep-checklist-themed-home.md>)
- [02-ramadan-journey-map-night-recap.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/F36_Ramadan_Mode/KMP/02-ramadan-journey-map-night-recap.md>)
- [03-mission-detail-story-player-fasting-tracker.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/F36_Ramadan_Mode/KMP/03-mission-detail-story-player-fasting-tracker.md>)
- [04-laylatul-qadr-reflection-variant.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/F36_Ramadan_Mode/KMP/04-laylatul-qadr-reflection-variant.md>)
- [05-eid-countdown-home-reward-reveal-card-generator.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/F36_Ramadan_Mode/KMP/05-eid-countdown-home-reward-reveal-card-generator.md>)
- [06-ramadan-complete-certificate-post-eid-habit.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/F36_Ramadan_Mode/KMP/06-ramadan-complete-certificate-post-eid-habit.md>)
- [07-parent-ramadan-settings-card-dashboard-tab.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/F36_Ramadan_Mode/KMP/07-parent-ramadan-settings-card-dashboard-tab.md>)
- [08-family-aggregate-report-conversion-card-invite.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/F36_Ramadan_Mode/KMP/08-family-aggregate-report-conversion-card-invite.md>)
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: - All FR/header annotations are reference-only pending approval. Dynamic names/counts/prices/dates are fixtures, never fabricate live data. Screenshot promises Link expires in 30 days. No account required to view; KMP08 flags invite contract unknown, so expiry/access promise unverified. Token is visibly truncated example; never embed real share token. See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

Parent Settings/Report→generate own-family read-only link; copy/share with parent gate; recipient without app graceful install/account prompt; expiry/auth access contract unverified.

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

The complete feature obligations are retained in [every-FR register](../10_REQUIREMENT_COVERAGE_REGISTER.md); section 2 identifies the exact screen-inventory row.

## 4. Exact content specification

### Current mobile source — exact captured text

```text
🌙 F.36 RAMADAN MODE
Screen 20: Family Member Invite (Read-Only Report)
Invite Family Members

Share a read-only link to your family's Ramadan report (FR-14)

Read-Only Report Link
No share link generated
No live link exists. Creation, expiry, revocation and consent require a connected parent-authorised service.
Copy Link
Share
```

### Other verified source text / fields

- Invite Family Members
- Read-Only Report Link
- Copy Link
- Share

### Requirement-driven fields and content roles

- Invite Family Members|Read-Only Report Link|Copy Link|Share

Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.

## 5. Visual enhancement instructions

- Preserve inspected seasonal source skin: deep navy night surfaces and warm amber/gold Ramadan accents; do not force standard cream background. Parent seasonal screens retain the inspected pale formal register. Reuse seasonal assets and approved typography; preserve exact content while removing FR annotations only after approval.
- Retain pale formal skin, heading/support, read-only link card and separate Copy/Share actions. Link text wraps/copies safely; do not invent expiry/no-account terms or embed real tokens.

- Preserve content order and screen purpose. Use a vertical auto-layout content stack; horizontal inset 20, base spacing 4/8/12/16/24/32; card content padding 12–16. Keep compact controls next to their labels; align headings and cards to one column edge.
- Preserve existing seasonal skin: Ramadan deep navy, Qadr calm violet and Eid brighter celebratory palette as inspected in references; map approved seasonal token aliases and verify contrast. Do not force the regular cream background onto seasonal screens. Body 14/16; heading 20/24; brand-only display 28/32. Preserve actual font assets; PRD Latin sans, display serif, separate verified Arabic content font.
- Do not import Frame 2's sample statistics, claims, religious text, section additions or combined desktop layouts. Borrow hierarchy, restrained surface separation and image framing only where they support this surface.
- Screen viewport is separate from long content height. Use vertical overflow when content exceeds available height; header/footer may be fixed only with bottom and top content clearance. At 320/360/390/420 logical widths, long labels wrap. At 200% text scale, stack grids or allow scrolling; no fixed text block height or sacred-text ellipsis.
- Essential touch target≥44×44 logical units; younger-child primary tasks≥56 where A2 specifies. Decorative icons have no hit targets. Assets retain aspect ratio; no text burned into illustrations. Safe area and keyboard must never obscure the current action.
- Source frames, unrelated screens and existing design direction remain unchanged. Token/component changes require separate review; never detach or globally mutate a source instance to fix this screen.

## 6. Screen states and conditional scenarios

- generation
- link ready
- copy feedback
- share
- failure retry
- expired link



Only apply states that belong to this surface. List-only empty/skeleton states are not added to legal documents or static intros. Network submit has a pending/timeout/retry result; retry preserves draft and must not duplicate a server-confirmed operation. Voice states need consent + OS grant; denial supplies listen/text/manual alternative. Loading/error/disabled/offline wording missing from source is a content approval gap.

<details><summary>Authoritative state/edge source context — apply screen-relevant cases, not all cases indiscriminately</summary>

Use the linked PRD §1.10–1.15 and the independently mapped states above; unspecified messages remain blocked.

</details>

## 7. Interactions and navigation

- Parent Settings/Report→generate own-family read-only link; copy/share with parent gate; recipient without app graceful install/account prompt; expiry/auth access contract unverified.

For every action below, use the cited preconditions and source validation. Preserve the invoking route and selected child. Back/cancel dismisses only the current overlay or returns to the invoking screen, preserving drafts and completed progress where specified. Unavailable actions remain visibly labeled with their reason and never activate. Permission prompts occur only after parent consent and a deliberate related action. A prototype simulates outcomes; it never validates identity, grants permissions, charges money or mutates production data.

Verified current-preview controls, retained to prevent omitted clickable elements:

- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Copy Link", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Share", "type": null}

For any captured control absent from an explicit action above, reconcile it against the screen-specific source below before wiring. Do not connect it to a convenient unrelated screen. Mark it **unresolved, non-executable** until its actual destination/state is confirmed; the navigation appendix reports this limitation. Decorative source-layer names are not automatically click targets.

<details><summary>Screen-specific PRD specification / click behavior</summary>

No independently named per-screen UX subsection exists. The PRD screen inventory entry, feature click-target table and functional requirements remain the authority; use research evidence and resolve unmatched targets before execution.

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
3. Create `NH/Enhanced/237/Family_Member_Invite/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/Family_Member_Invite`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] F36 behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
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
