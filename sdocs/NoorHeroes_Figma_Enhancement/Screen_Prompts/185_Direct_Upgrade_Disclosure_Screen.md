**Mandatory finalized visual baseline:** Read and apply [Finalized V2 Reusable Design Prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) before implementing this screen. Its latest approved visual rules supersede older conflicting design proposals below; PRD behavior and exact approved content remain authoritative.

# Screen 185 — Direct Upgrade Disclosure Screen

**Documentation only. Execute this prompt only after the documentation and this screen's unresolved decisions are approved. Stop after this screen.**

## 1. Screen identification

- Feature/sub-feature: **C24 — Direct Upgrade Disclosure Screen**.
- Surface: **screen**. Number is controlled review order, not a forced linear user journey.
- Execution status: **Requirement-driven missing reference; exact labels/content need approval before execution**.
- Journey entry / previous screen: Plan Comparison "Upgrade".
- Next screen(s) / result: Platform Purchase Flow (external).
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: [Feature_C24_Subscription_Billing.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Parent Area In-App (19-26)/Feature_C24_Subscription_Billing.md>); **§1.18 row 4; §1.7; §2; §6; §13**.
- Current mobile reference: [NoorHeroes current preview](https://noorheroes.figma.site/) → selector **Missing in inspected site catalogue**; exact text captured below.
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: **Missing corresponding screen reference.** Do not substitute a visually related hub as functional evidence.
- Frame 2 container: `1085:13003`; visual reference: **Missing corresponding screen reference.** Do not substitute a visually related hub as functional evidence.
- Reference qualification: No independently verified equivalent for this screen; global style inspiration must not replace approved copy.
- Existing screenshot candidates (one-to-one identity is not asserted unless verified in research):
- Missing corresponding local screen reference.
- Blueprint alignment:
- [01-subscription-landing-screen-entry-points.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C24_Subscription_Billing/KMP/01-subscription-landing-screen-entry-points.md>)
- [02-plan-comparison-screen.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C24_Subscription_Billing/KMP/02-plan-comparison-screen.md>)
- [03-trial-upgrade-disclosure-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C24_Subscription_Billing/KMP/03-trial-upgrade-disclosure-flow.md>)
- [04-play-billing-handoff-server-validated-activation.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C24_Subscription_Billing/KMP/04-play-billing-handoff-server-validated-activation.md>)
- [05-invoice-history-detail-screens.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C24_Subscription_Billing/KMP/05-invoice-history-detail-screens.md>)
- [06-cancellation-retry-restore-purchase-flows.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C24_Subscription_Billing/KMP/06-cancellation-retry-restore-purchase-flows.md>)
- [07-shared-entitlement-repository-cross-feature-contract.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C24_Subscription_Billing/KMP/07-shared-entitlement-repository-cross-feature-contract.md>)
- [08-child-mode-billing-invisibility-safeguard.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C24_Subscription_Billing/KMP/08-child-mode-billing-invisibility-safeguard.md>)
- [09-downgrade-child-selector-trigger-c21-delegation.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C24_Subscription_Billing/KMP/09-downgrade-child-selector-trigger-c21-delegation.md>)
- [10-renewal-payment-failure-notification-deeplink-handling.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C24_Subscription_Billing/KMP/10-renewal-payment-failure-notification-deeplink-handling.md>)
- [11-free-plan-second-child-upgrade-prompt.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C24_Subscription_Billing/KMP/11-free-plan-second-child-upgrade-prompt.md>)
- [12-premium-content-lock-icon-upsell-tapthrough.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C24_Subscription_Billing/KMP/12-premium-content-lock-icon-upsell-tapthrough.md>)
- [13-renewal-reminder-banner-component.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/C24_Subscription_Billing/KMP/13-renewal-reminder-banner-component.md>)
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: - P-C24-01: Inspected Plan Comparison-01.png Free Family Starter says Up to 2 children; C24 FR-1 says 1 active child. Source image also offers Limited AI questions (5/day), absent from FR-1 plan list. Preserve evidence and resolve before execution.
- P-C24-02: Android-focused landing label Manage on Play Store must become actual platform-specific store management affordance on iOS; iOS equivalent behavior is supported by FR-3 App Store purchase reference but exact copy requires source verification. See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

Present transparent parent-only subscription choices and store-managed billing with server-verified entitlement. Screen-specific role: Direct Upgrade Disclosure Screen.

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

The complete feature obligations are retained in [every-FR register](../10_REQUIREMENT_COVERAGE_REGISTER.md); section 2 identifies the exact screen-inventory row.

## 4. Exact content specification

### Requirement-driven fields and content roles

- Selected plan
- Actual store price/cadence
- Renewal disclosure
- Continue to platform purchase
- Cancel

**Exact copy unavailable: execution blocked for copy-dependent design.** Locate the authoritative content registry/original frame; do not insert placeholder, paraphrased or AI-generated copy. This document still specifies the required surface so it is not omitted.

Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.

## 5. Visual enhancement instructions

- Screen scope: Direct Upgrade Disclosure Screen. Arrange only these vertical content roles: Selected plan → Actual store price/cadence → Renewal disclosure → Continue to platform purchase → Cancel. Use one clear heading and context row; source-approved primary action follows this screen content. Reuse local shared components without pulling other module sections onto this screen. Retain verified source content order where it differs; required missing content requires source approval before placement.

- Preserve content order and screen purpose. Use a vertical auto-layout content stack; horizontal inset 20, base spacing 4/8/12/16/24/32; card content padding 12–16. Keep compact controls next to their labels; align headings and cards to one column edge.
- Use existing cream `#FAF7F0`, surface `#FFFFFF`, ink `#1C2B33`, teal `#0E7C7B`, gold `#D4A24C`. Gold/bright teal are accents, not untested small-text colors. Body 14/16; heading 20/24; brand-only display 28/32. Preserve actual font assets; PRD Latin sans, display serif, separate verified Arabic content font.
- Do not import Frame 2's sample statistics, claims, religious text, section additions or combined desktop layouts. Borrow hierarchy, restrained surface separation and image framing only where they support this surface.
- Screen viewport is separate from long content height. Use vertical overflow when content exceeds available height; header/footer may be fixed only with bottom and top content clearance. At 320/360/390/420 logical widths, long labels wrap. At 200% text scale, stack grids or allow scrolling; no fixed text block height or sacred-text ellipsis.
- Essential touch target≥44×44 logical units; younger-child primary tasks≥56 where A2 specifies. Decorative icons have no hit targets. Assets retain aspect ratio; no text burned into illustrations. Safe area and keyboard must never obscure the current action.
- Source frames, unrelated screens and existing design direction remain unchanged. Token/component changes require separate review; never detach or globally mutate a source instance to fix this screen.

## 6. Screen states and conditional scenarios

- Default for Direct Upgrade Disclosure Screen Applicable pending/success/error only for actions explicitly named in action_rules Cached offline read only where supported; online-only mutations show sourced reconnect reason Back/cancel restores invoking context; actual unresolved source behavior blocks execution



Only apply states that belong to this surface. List-only empty/skeleton states are not added to legal documents or static intros. Network submit has a pending/timeout/retry result; retry preserves draft and must not duplicate a server-confirmed operation. Voice states need consent + OS grant; denial supplies listen/text/manual alternative. Loading/error/disabled/offline wording missing from source is a content approval gap.

<details><summary>Authoritative state/edge source context — apply screen-relevant cases, not all cases indiscriminately</summary>

### 1.10 Edge Cases

1. A parent starts a 7-day trial, then immediately cancels within the first hour → the trial entitlement remains active (Mobile Family level) for the remainder of the 7 days, since canceling a trial means "don't auto-convert," not "revoke immediately" — consistent with the platform's general "access continues until the period ends" cancellation philosophy applied even to trials.
2. The Play Store webhook for a successful day-7 trial conversion is delayed by several hours → the app continues to honor the last-verified (trial) entitlement through the signed grace window; if the webhook arrives within that window, entitlement updates correctly; if it doesn't arrive before the grace window expires, the reconciliation job queries the store directly to resolve the actual state rather than leaving it ambiguous indefinitely.
3. A parent on Premium Family (8 children, 6 active) downgrades to Mobile Family (4 children) → the system must select which 2 of the 6 active children become disabled; consistent with the trial-cancellation pattern, the parent is prompted to choose, with the deterministic most-recently-active fallback applying if no selection is made within 24 hours, generalized here from "select 1 of many" to "select N of many to keep" as needed for the specific plan-capacity delta.
4. A parent's payment fails, enters the grace period (`PastDue`), and recovers payment on the very last day of the grace window → the account returns to `ActivePaid` and no children are disabled, since the grace period's entire purpose is to avoid disrupting access while payment issues are resolved.
5. A parent restores a purchase on a new device (e.g., after reinstalling the app or switching devices) → the restore-purchase flow re-validates the existing store receipt server-side and re-establishes the correct entitlement state without requiring a new purchase, consistent with standard app-store restore-purchase expectations.
6. A parent attempts to browse premium content while on the Free plan → the content is shown with a lock icon in the relevant parent-approved discovery context (never hidden entirely), and tapping it routes to the Subscription upsell — this premium content is never silently absent from a catalog/browse view.
7. A family's annual plan is approaching its renewal date, and the 7-day reminder notification would fire during the child's configured bedtime window → since this is a parent-facing notification type, not a child-facing one, it is unaffected by the child's own bedtime/quiet-hours configuration (cross-ref C.23's scope being specifically per-child; parent notification timing is governed by the Parent Area's own notification preferences, C.25).
8. A parent's family has children added via different historical plan tiers (e.g., 4 children added while on Premium Family, then downgraded) → the system's enforcement of "how many children may be *active* at once" is always evaluated against the *current* plan, regardless of historical tier at the time each child was originally added — there is no grandfathering of past capacity.
9. Two webhook events for the same underlying billing event arrive (e.g., a retried delivery from the store) → idempotent processing on `provider_event_id` ensures the second delivery is a safe no-op, never double-processing a renewal or cancellation event.
10. A parent attempts to upgrade mid-trial (before day 7) directly to Premium Family rather than waiting for the standard Mobile Family auto-conversion → this is supported as a direct upgrade path; the trial's scheduled day-7 conversion logic is superseded by the explicit upgrade, which takes effect immediately per FR-9's "Upgrade unlocks immediately" rule.

### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Store webhook delayed | Last verified entitlement honored within a signed grace window; reconciliation job resolves any lingering ambiguity (FR-6) |
| Duplicate webhook delivery | Idempotent on `provider_event_id`, safe no-op on replay (Edge Case 9) |
| Payment failure on renewal | Email/push reminder, grace period (`PastDue`), no child-mode billing messaging at any point |
| Restore-purchase request | Server-side receipt re-validation, entitlement re-established without a new purchase |
| Plan-capacity-reducing downgrade with more active children than the new plan allows | Parent prompted to select which children remain active; deterministic 24-hour fallback if no selection |

### 1.12 Empty States
- Zero invoice history yet (new subscriber, first billing cycle not yet processed) → friendly "Your first invoice will appear here after your trial converts" framing.

### 1.13 Loading States
- Plan Comparison/Subscription screen: skeleton plan-card shimmer while entitlement/plan data loads.

### 1.14 Offline States
- Subscription screen renders last-cached entitlement/plan state when offline; purchase/upgrade/cancel actions require connectivity and clearly indicate this if attempted offline, given their store-billing-API dependency.

### 1.15 Permission States
- No new runtime permissions; all purchase actions route through the OS-level Play Store/App Store billing sheet, which has its own standard permission/account context outside this app's control.



</details>

## 7. Interactions and navigation

- Entry: Plan Comparison "Upgrade". Primary result: Platform Purchase Flow (external). Apply only the named screen required_fields; parent-sensitive mutations pass fresh C19 gate. Back/cancel returns to invoking surface without committing. Exact unspecified controls/copy remain approval gaps.

For every action below, use the cited preconditions and source validation. Preserve the invoking route and selected child. Back/cancel dismisses only the current overlay or returns to the invoking screen, preserving drafts and completed progress where specified. Unavailable actions remain visibly labeled with their reason and never activate. Permission prompts occur only after parent consent and a deliberate related action. A prototype simulates outcomes; it never validates identity, grants permissions, charges money or mutates production data.

Verified current-preview controls, retained to prevent omitted clickable elements:

- Not supplied by this source; resolve before execution.

For any captured control absent from an explicit action above, reconcile it against the screen-specific source below before wiring. Do not connect it to a convenient unrelated screen. Mark it **unresolved, non-executable** until its actual destination/state is confirmed; the navigation appendix reports this limitation. Decorative source-layer names are not automatically click targets.

<details><summary>Screen-specific PRD specification / click behavior</summary>

Screen: Direct Upgrade Disclosure Screen
Source PRD_Documents/Parent Area In-App (19-26)/Feature_C24_Subscription_Billing.md §1.18 row 4; §1.7; §2; §6; §13
Purpose: Present transparent parent-only subscription choices and store-managed billing with server-verified entitlement. Screen-specific role: Direct Upgrade Disclosure Screen.
Fields: Selected plan; Actual store price/cadence; Renewal disclosure; Continue to platform purchase; Cancel
Action contract:
Entry: Plan Comparison "Upgrade". Primary result: Platform Purchase Flow (external). Apply only the named screen required_fields; parent-sensitive mutations pass fresh C19 gate. Back/cancel returns to invoking surface without committing. Exact unspecified controls/copy remain approval gaps.
States:
Default for Direct Upgrade Disclosure Screen Applicable pending/success/error only for actions explicitly named in action_rules Cached offline read only where supported; online-only mutations show sourced reconnect reason Back/cancel restores invoking context; actual unresolved source behavior blocks execution

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
3. Create `NH/Enhanced/185/Direct_Upgrade_Disclosure_Screen/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/Direct_Upgrade_Disclosure_Screen`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] C24 behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
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
