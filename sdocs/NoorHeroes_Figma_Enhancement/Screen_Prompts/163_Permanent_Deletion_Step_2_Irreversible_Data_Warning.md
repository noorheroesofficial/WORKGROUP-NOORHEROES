**Mandatory finalized visual baseline:** Read and apply [Finalized V2 Reusable Design Prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) before implementing this screen. Its latest approved visual rules supersede older conflicting design proposals below; PRD behavior and exact approved content remain authoritative.

# Screen 163 — Permanent Deletion — Step 2: Irreversible-Data Warning

**Documentation only. Execute this prompt only after the documentation and this screen's unresolved decisions are approved. Stop after this screen.**

## 1. Screen identification

- Feature/sub-feature: **C21 — Permanent Deletion — Step 2: Irreversible-Data Warning**.
- Surface: **screen**. Number is controlled review order, not a forced linear user journey.
- Execution status: **Reference available; unresolved conflicts require approval before design**.
- Journey entry / previous screen: Step-Up Gate success.
- Next screen(s) / result: Confirm / Cancel.
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: [Feature_C21_Multi_Child_Management.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Parent Area In-App (19-26)/Feature_C21_Multi_Child_Management.md>); **§1.18 row 11; §1.7; §2; §6; §13**.
- Current mobile reference: [NoorHeroes current preview](https://noorheroes.figma.site/) → selector **Delete Child Warning**; exact text captured below.
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: [Child Deletion - Irreversible Warning](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1113-7899) — `1113:7899`. 
- Frame 2 container: `1085:13003`; visual reference: **Missing corresponding screen reference.** Do not substitute a visually related hub as functional evidence.
- Reference qualification: No independently verified equivalent for this screen; global style inspiration must not replace approved copy.
- Existing screenshot candidates (one-to-one identity is not asserted unless verified in research):
- [Delete Child Warning-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Child Management/Delete Child Warning-01.png>)
- [Delete Child Warning-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Child Management/Delete Child Warning-02.png>)
- [Delete Child Warning-03.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Child Management/Delete Child Warning-03.png>)
- [Delete Child Warning-04.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Child Management/Delete Child Warning-04.png>)
- Blueprint alignment:
- [01-child-management-list-screen.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C21_Multi_Child_Management/KMP/01-child-management-list-screen.md>)
- [02-per-child-action-menu-disabled-card-state.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C21_Multi_Child_Management/KMP/02-per-child-action-menu-disabled-card-state.md>)
- [03-add-edit-child-form-dob-lock-integration.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C21_Multi_Child_Management/KMP/03-add-edit-child-form-dob-lock-integration.md>)
- [04-disable-reenable-confirmation-flows.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C21_Multi_Child_Management/KMP/04-disable-reenable-confirmation-flows.md>)
- [05-permanent-deletion-warning-confirmation-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C21_Multi_Child_Management/KMP/05-permanent-deletion-warning-confirmation-flow.md>)
- [06-reorder-mode-interaction.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C21_Multi_Child_Management/KMP/06-reorder-mode-interaction.md>)
- [07-plan-capacity-blocked-state-subscription-upsell.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C21_Multi_Child_Management/KMP/07-plan-capacity-blocked-state-subscription-upsell.md>)
- [08-trial-cancellation-forced-selection-screen.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C21_Multi_Child_Management/KMP/08-trial-cancellation-forced-selection-screen.md>)
- [09-offline-child-management-caching-sync.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C21_Multi_Child_Management/KMP/09-offline-child-management-caching-sync.md>)
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: - P-C21-01: Inspected Delete Child Warning-01.png adds typed AISHA confirmation and only-warning footer. C21 §2.2 specifies equally sized Cancel/Permanently Delete, serious tone, no artificial delay; name typing is absent from PRD. Approval needed on retaining extra friction/copy.
- P-C21-02: C25 FR-8 points to C21 FR-8 step 7 for account deletion cancellation; actual C21 FR-8 governs plan capacity. C26 links full account deletion into C21, but C21 has only child-deletion screens. Full account deletion warning, 7-day countdown, pending access policy and support-cancellation destination need authoritative reconciliation, not invention.
- P-C21-03: Blueprint refers to Add:Edit Child-01/02.png; actual filesystem uses Add_Edit Child-01/02.png. Use actual paths.
- P-C21-04: Add_Edit Child-01.png uses Age / Enter age instead of PRD C21 FR-6 DOB picker; language, level, interests, goal and AI toggle are not visible. Inspect continuation Add_Edit Child-02 before concluding missing; preserve conflict between age and immutable DOB. See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

Manage child profiles while retaining disabled data, enforcing capacity and clearly warning before irreversible deletion. Screen-specific role: Permanent Deletion — Step 2: Irreversible-Data Warning.

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

The complete feature obligations are retained in [every-FR register](../10_REQUIREMENT_COVERAGE_REGISTER.md); section 2 identifies the exact screen-inventory row.

## 4. Exact content specification

### Current mobile source — exact captured text

```text
👧
Delete Aisha's Profile?

Remove this sample profile from the preview?

Only Aisha's sample profile is removed from this session. No live account or learning data is changed.

Type Aisha to confirm:
Cancel
Remove preview profile

You can cancel and keep the profile as it is. Refreshing restores sample profiles.
```

### Frame 1 — exact layer text (separate source; differences need approval)

```text
👧🏼
Delete Aisha's Profile?
Deleted data cannot be
recovered. This action is
permanent.
All of Aisha's learning progress,
achievements, and saved content will be
permanently deleted. This cannot be
undone.
Type AISHA to confirm:
Type name here
Cancel
Permanently Delete
⚠️
This is your only warning. There is no undo.
9:41
```

### Requirement-driven fields and content roles

- Child identity
- Deleted data cannot be recovered. This action is permanent.
- Cancel
- Permanently Delete

Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.

## 5. Visual enhancement instructions

- Screen scope: Permanent Deletion — Step 2: Irreversible-Data Warning. Arrange only these vertical content roles: Child identity → Deleted data cannot be recovered. This action is permanent. → Cancel → Permanently Delete. Use one clear heading and context row; source-approved primary action follows this screen content. Reuse local shared components without pulling other module sections onto this screen. Retain verified source content order where it differs; required missing content requires source approval before placement.

- Preserve content order and screen purpose. Use a vertical auto-layout content stack; horizontal inset 20, base spacing 4/8/12/16/24/32; card content padding 12–16. Keep compact controls next to their labels; align headings and cards to one column edge.
- Use existing cream `#FAF7F0`, surface `#FFFFFF`, ink `#1C2B33`, teal `#0E7C7B`, gold `#D4A24C`. Gold/bright teal are accents, not untested small-text colors. Body 14/16; heading 20/24; brand-only display 28/32. Preserve actual font assets; PRD Latin sans, display serif, separate verified Arabic content font.
- Do not import Frame 2's sample statistics, claims, religious text, section additions or combined desktop layouts. Borrow hierarchy, restrained surface separation and image framing only where they support this surface.
- Screen viewport is separate from long content height. Use vertical overflow when content exceeds available height; header/footer may be fixed only with bottom and top content clearance. At 320/360/390/420 logical widths, long labels wrap. At 200% text scale, stack grids or allow scrolling; no fixed text block height or sacred-text ellipsis.
- Essential touch target≥44×44 logical units; younger-child primary tasks≥56 where A2 specifies. Decorative icons have no hit targets. Assets retain aspect ratio; no text burned into illustrations. Safe area and keyboard must never obscure the current action.
- Source frames, unrelated screens and existing design direction remain unchanged. Token/component changes require separate review; never detach or globally mutate a source instance to fix this screen.

## 6. Screen states and conditional scenarios

- Default for Permanent Deletion — Step 2: Irreversible-Data Warning Applicable pending/success/error only for actions explicitly named in action_rules Cached offline read only where supported; online-only mutations show sourced reconnect reason Back/cancel restores invoking context; actual unresolved source behavior blocks execution



Only apply states that belong to this surface. List-only empty/skeleton states are not added to legal documents or static intros. Network submit has a pending/timeout/retry result; retry preserves draft and must not duplicate a server-confirmed operation. Voice states need consent + OS grant; denial supplies listen/text/manual alternative. Loading/error/disabled/offline wording missing from source is a content approval gap.

<details><summary>Authoritative state/edge source context — apply screen-relevant cases, not all cases indiscriminately</summary>

### 1.10 Edge Cases

1. A parent attempts to edit a child's DOB after the first save → the field is read-only/locked, with an explanation that changes require Support.
2. A parent disables their only active child while another device still has that child's session active → that device's session is invalidated on its very next API call.
3. A parent initiates permanent deletion, passes step-up, sees the warning, but backs out before final confirmation → no deletion occurs; the profile is entirely unaffected.
4. A parent reorders children while one is mid-deletion-confirmation for a different child → these are independent actions, neither blocks the other.
5. A family's plan capacity decreases while more children are active than the new limit allows, before the parent completes the forced-selection step → a defined safe default applies (most-recently-active child remains enabled) rather than an undefined/inconsistent state.
6. A parent deletes a child profile with an unusual per-child entitlement tied to it → deletion proceeds per the standard flow; entitlement cascade is handled by C.24's own logic.
7. Step-up authentication expires mid-form → re-attempting to save triggers a fresh step-up prompt rather than silently failing or silently saving.
8. Two co-guardians edit the same child's profile from different devices nearly simultaneously → last-write-wins at the database layer; each UI reflects a fresh fetch before allowing a save.
9. A parent deletes the only remaining active child → allowed, with a gentle informational note (not a hard block) that the family will have zero active children.
10. A re-enabled child's notification binding is re-established the next time their profile is selected via Who Is Learning (C.19/B.17), not separately orchestrated here.

### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Attempt to edit DOB | Field locked/read-only with a brief explanation |
| Add Child beyond plan capacity | Inline block with upsell path |
| Duplicate nickname on save | Inline rejection with differentiation guidance |
| Re-enable beyond plan capacity | Inline block with upsell path |
| Step-up auth expires mid-form | Fresh step-up prompt on save attempt |
| Deletion flow abandoned before final confirm | No action taken; profile unaffected |

### 1.12 Empty States
- Zero children (after deleting all) → list shows only "+ Add Child" with a friendly prompt.

### 1.13 Loading States
- List: skeleton card-list shimmer. Save: button spinner, rest of form remains visible.

### 1.14 Offline States
- List renders read-only from cache; all mutating actions require connectivity, shown clearly.

### 1.15 Permission States
- No new runtime permissions; step-up handled entirely by C.19.



</details>

## 7. Interactions and navigation

- Entry: Step-Up Gate success. Primary result: Confirm / Cancel. Apply only the named screen required_fields; parent-sensitive mutations pass fresh C19 gate. Back/cancel returns to invoking surface without committing. Exact unspecified controls/copy remain approval gaps.

For every action below, use the cited preconditions and source validation. Preserve the invoking route and selected child. Back/cancel dismisses only the current overlay or returns to the invoking screen, preserving drafts and completed progress where specified. Unavailable actions remain visibly labeled with their reason and never activate. Permission prompts occur only after parent consent and a deliberate related action. A prototype simulates outcomes; it never validates identity, grants permissions, charges money or mutates production data.

Verified current-preview controls, retained to prevent omitted clickable elements:

- {"disabled": false, "label": "Type Aisha to confirm removal from preview", "placeholder": "Type name here", "tag": "INPUT", "text": "", "type": "text"}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Cancel", "type": null}
- {"disabled": true, "label": null, "placeholder": null, "tag": "BUTTON", "text": "Remove preview profile", "type": null}

For any captured control absent from an explicit action above, reconcile it against the screen-specific source below before wiring. Do not connect it to a convenient unrelated screen. Mark it **unresolved, non-executable** until its actual destination/state is confirmed; the navigation appendix reports this limitation. Decorative source-layer names are not automatically click targets.

<details><summary>Screen-specific PRD specification / click behavior</summary>

Screen: Permanent Deletion — Step 2: Irreversible-Data Warning
Source PRD_Documents/Parent Area In-App (19-26)/Feature_C21_Multi_Child_Management.md §1.18 row 11; §1.7; §2; §6; §13
Purpose: Manage child profiles while retaining disabled data, enforcing capacity and clearly warning before irreversible deletion. Screen-specific role: Permanent Deletion — Step 2: Irreversible-Data Warning.
Fields: Child identity; Deleted data cannot be recovered. This action is permanent.; Cancel; Permanently Delete
Action contract:
Entry: Step-Up Gate success. Primary result: Confirm / Cancel. Apply only the named screen required_fields; parent-sensitive mutations pass fresh C19 gate. Back/cancel returns to invoking surface without committing. Exact unspecified controls/copy remain approval gaps.
States:
Default for Permanent Deletion — Step 2: Irreversible-Data Warning Applicable pending/success/error only for actions explicitly named in action_rules Cached offline read only where supported; online-only mutations show sourced reconnect reason Back/cancel restores invoking context; actual unresolved source behavior blocks execution

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
3. Create `NH/Enhanced/163/Permanent_Deletion_Step_2_Irreversible_Data_Warning/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/Permanent_Deletion_Step_2_Irreversible_Data_Warning`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] C21 behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
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
