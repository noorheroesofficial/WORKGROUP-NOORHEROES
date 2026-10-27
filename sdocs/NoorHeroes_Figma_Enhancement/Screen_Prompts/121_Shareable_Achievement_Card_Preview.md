**Mandatory finalized visual baseline:** Read and apply [Finalized V2 Reusable Design Prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) before implementing this screen. Its latest approved visual rules supersede older conflicting design proposals below; PRD behavior and exact approved content remain authoritative.

# Screen 121 — Shareable Achievement Card Preview

**Documentation only. Execute this prompt only after the documentation and this screen's unresolved decisions are approved. Stop after this screen.**

## 1. Screen identification

- Feature/sub-feature: **A11 — Shareable Achievement Card Preview**.
- Surface: **screen**. Number is controlled review order, not a forced linear user journey.
- Execution status: **BLOCKED for exact approved copy: no exact Frame 1 counterpart verified. Do not fabricate copy, Arabic, educational items, user data or stats.**.
- Journey entry / previous screen: Achievements/Badge Detail "Share" action.
- Next screen(s) / result: Parent Gate → OS Share Sheet, or cancel.
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: [Feature_A11_Rewards_System.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Child App (1-12)/Feature_A11_Rewards_System.md>); **§1.18 row 8; §1.7; §2; §6; §13**.
- Current mobile reference: **Missing independently mapped current-site screen.**
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: **Missing corresponding screen reference.** Do not substitute a visually related hub as functional evidence.
- Frame 2 container: `1085:13003`; visual reference: [Rewards & Avatar Hub](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1085-15876) — `1085:15876`. Related enhanced feature hub for visual patterns only; not an exact screen equivalent
- Reference qualification: ['Required layout has no verified exact source-frame match; access exact approved content before execution.'].
- Existing screenshot candidates (one-to-one identity is not asserted unless verified in research):
- [Achievement Store-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Rewards/Achievement Store-01.png>)
- [Achievement Store-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Rewards/Achievement Store-02.png>)
- [Achievement Store-03.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Rewards/Achievement Store-03.png>)
- [Achievement Store-04.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Rewards/Achievement Store-04.png>)
- [Achievements-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Rewards/Achievements-01.png>)
- [Achievements-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Rewards/Achievements-02.png>)
- [Achievements-03.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Rewards/Achievements-03.png>)
- [Achievements-04.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Rewards/Achievements-04.png>)
- [Family Board.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Rewards/Family Board.png>)
- [Rewards Wallet-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Rewards/Rewards Wallet-01.png>)
- [Rewards Wallet-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Rewards/Rewards Wallet-02.png>)
- [Rewards Wallet-03.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Rewards/Rewards Wallet-03.png>)
- [Rewards Wallet-04.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Rewards/Rewards Wallet-04.png>)
- [Rewards Wallet-05.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Rewards/Rewards Wallet-05.png>)
- [Rewards Wallet-06.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Rewards/Rewards Wallet-06.png>)
- [Rewards Wallet-07.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Rewards/Rewards Wallet-07.png>)
- [Rewards Wallet-08.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Rewards/Rewards Wallet-08.png>)
- [Rewards Wallet-09.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Rewards/Rewards Wallet-09.png>)
- Blueprint alignment:
- [01-shared-rewards-client-module.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A11_Rewards_System/KMP/01-shared-rewards-client-module.md>)
- [02-rewards-wallet-hub-screen.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A11_Rewards_System/KMP/02-rewards-wallet-hub-screen.md>)
- [03-transaction-history-detail-view.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A11_Rewards_System/KMP/03-transaction-history-detail-view.md>)
- [04-achievements-screen-badge-grid-level-progress.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A11_Rewards_System/KMP/04-achievements-screen-badge-grid-level-progress.md>)
- [05-parent-gated-achievement-sharing-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A11_Rewards_System/KMP/05-parent-gated-achievement-sharing-flow.md>)
- [06-daily-mission-weekly-challenge-experience.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A11_Rewards_System/KMP/06-daily-mission-weekly-challenge-experience.md>)
- [07-achievement-store-catalog-purchase-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A11_Rewards_System/KMP/07-achievement-store-catalog-purchase-flow.md>)
- [08-family-board-experience.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A11_Rewards_System/KMP/08-family-board-experience.md>)
- [09-reward-unlock-animation-badge-unlock-modal.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A11_Rewards_System/KMP/09-reward-unlock-animation-badge-unlock-modal.md>)
- [10-rewards-data-freshness-cross-screen-invalidation-engine.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A11_Rewards_System/KMP/10-rewards-data-freshness-cross-screen-invalidation-engine.md>)
- [11-rewards-cross-platform-analytics-instrumentation.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A11_Rewards_System/KMP/11-rewards-cross-platform-analytics-instrumentation.md>)
- [12-rewards-localization-rtl-foundation.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A11_Rewards_System/KMP/12-rewards-localization-rtl-foundation.md>)
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: - CL-01
- CL-04
- CL-09 See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

Enable Shareable Achievement Card Preview in the established A11 journey. Entry: Achievements/Badge Detail "Share" action. Required outcome: Parent Gate → OS Share Sheet, or cancel.

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

**FR-5** Reward Engine Flow (canonical, source §6.6/the "Reward Engine Flow" diagram block, items 1–9): (1) activity service validates completion + idempotency key, (2) reward engine checks rule version, age band, quality threshold, daily cap, and duplicate key, (3) XP/Noor Heroes Points appended to the ledger, (4) achievement counters update, (5) badge/streak/milestone rules evaluated, (6) wallet balance re-projected from the ledger, (7) parent report updates, (8) an eligible push notification is sent, (9) the completion screen displays a reward summary/animation.

**FR-10** Daily Missions (3 per day) and the Weekly Challenge are time-boxed; progress resets at window close, but **expired seasonal challenges archive rather than disappear** (source: NoorHeroes Blueprint screen catalog "Challenges — Navigation Flow: Surfaced as a Home card and as its own tile under Rewards; expired seasonal challenges archive rather than disappear").

**FR-11** The Achievement Store (`catalog_items`) sells cosmetic/avatar/story-world items priced exclusively in Noor Heroes Points — items are sourced only from the admin-managed catalog, never user-uploaded content (source §9.4, Consolidated Blueprint navigation table "Avatar... Items are sourced only from AvatarItems catalog; no user uploads").

**FR-12** Achievement-card sharing is parent-gated: generating a shareable card requires Parent Profile verification, routes through the OS share sheet only after that gate, and the card itself never includes child ID, DOB, or location (source: screen catalog "Achievements — Navigation Flow: Sharing routes through the OS share sheet only after Parent Profile verification; no child ID/DOB/location ever appears on the card").

## 4. Exact content specification

### Requirement-driven fields and content roles

- Not supplied by this source; resolve before execution.

**Exact copy unavailable: execution blocked for copy-dependent design.** Locate the authoritative content registry/original frame; do not insert placeholder, paraphrased or AI-generated copy. This document still specifies the required surface so it is not omitted.

Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.

## 5. Visual enhancement instructions

- Clearly separate XP level/progression from spendable Noor Heroes Points. Wallet shows deterministic reasons, badge preview, three daily missions and weekly challenge. Store prices use points only with text. Family Board is aggregate only; owned items, purchase confirmation and shortfall must be distinguishable.

- Preserve content order and screen purpose. Use a vertical auto-layout content stack; horizontal inset 20, base spacing 4/8/12/16/24/32; card content padding 12–16. Keep compact controls next to their labels; align headings and cards to one column edge.
- Use existing cream `#FAF7F0`, surface `#FFFFFF`, ink `#1C2B33`, teal `#0E7C7B`, gold `#D4A24C`. Gold/bright teal are accents, not untested small-text colors. Body 14/16; heading 20/24; brand-only display 28/32. Preserve actual font assets; PRD Latin sans, display serif, separate verified Arabic content font.
- Do not import Frame 2's sample statistics, claims, religious text, section additions or combined desktop layouts. Borrow hierarchy, restrained surface separation and image framing only where they support this surface.
- Screen viewport is separate from long content height. Use vertical overflow when content exceeds available height; header/footer may be fixed only with bottom and top content clearance. At 320/360/390/420 logical widths, long labels wrap. At 200% text scale, stack grids or allow scrolling; no fixed text block height or sacred-text ellipsis.
- Essential touch target≥44×44 logical units; younger-child primary tasks≥56 where A2 specifies. Decorative icons have no hit targets. Assets retain aspect ratio; no text burned into illustrations. Safe area and keyboard must never obscure the current action.
- Source frames, unrelated screens and existing design direction remain unchanged. Token/component changes require separate review; never detach or globally mutate a source instance to fix this screen.

## 6. Screen states and conditional scenarios

- Default as described in cited source



Only apply states that belong to this surface. List-only empty/skeleton states are not added to legal documents or static intros. Network submit has a pending/timeout/retry result; retry preserves draft and must not duplicate a server-confirmed operation. Voice states need consent + OS grant; denial supplies listen/text/manual alternative. Loading/error/disabled/offline wording missing from source is a content approval gap.

<details><summary>Authoritative state/edge source context — apply screen-relevant cases, not all cases indiscriminately</summary>

### 1.10 Edge Cases

1. A reward-eligible activity completes offline and queues locally, but by the time it syncs, the relevant reward rule version has been updated by Admin → the ledger entry is processed using the rule version that was **active at the time the activity was actually completed** (timestamped client-side, validated server-side within a reasonable bound), not the rule version active at sync time — consistent with the platform's general principle of not retroactively penalizing a child for a timing artifact of connectivity.
2. A child crosses a daily cap exactly mid-activity (e.g., their 5th of 5 capped habit check-ins for the day, then attempts a 6th) → the 6th attempt's underlying activity (e.g., the habit check-in itself, per A.7) still succeeds at the feature level if that feature's own rules allow it, but this Reward Service simply does not append a 6th ledger entry — the cap is a reward-issuance boundary, not necessarily a feature-functionality boundary.
3. A badge's unlock criteria reference an achievement counter that gets corrected/recalculated due to a data-quality fix → if the correction would cause a badge to newly qualify, it is awarded retroactively with its actual original criteria-met timestamp where determinable; if a correction would mean a badge *should not* have been awarded, the badge is **not** revoked once granted (consistent with the platform's "badges are sticky once earned" principle established in A.6 Edge Case 2, generalized here as the canonical rule for this entire system).
4. A seasonal Weekly Challenge spans a calendar boundary where a child's account is mid-subscription-downgrade → reward eligibility for completing the challenge is unaffected by subscription tier, consistent with A.6's always-free-tier philosophy extended in spirit here — premium-gated content's rewards are naturally unavailable only because the content itself isn't accessible, not because of a reward-tier restriction layered on top.
5. Two different consuming features (e.g., A.8's Quiz Engine and A.10's Games Module) both attempt to award XP for what is essentially the same underlying skill-practice moment → each emits its own distinct, correctly-attributed ledger entry — this is not treated as a duplicate/farming pattern unless the exact same `idempotency_key`/event is involved.
6. A family's Family Board goal is met by combined sibling contributions, but one sibling's contributing event is still offline/unsynced at the moment the combined total appears to cross the threshold from a different sibling's freshly-synced perspective → consistent with A.7's Family Streak handling, the Family Board's authoritative server-side evaluation only counts confirmed, synced contributions.
7. A child's Achievement Store purchase succeeds, but the subsequent avatar-inventory "equip" call fails (network) → the Noor Heroes Points debit and the inventory-ownership grant are committed atomically as part of the purchase transaction; equip is a separate, retriable, idempotent action that doesn't need to re-succeed for ownership to be valid.
8. A duplicate Achievement Store claim is attempted (e.g., a double-tap on "Claim" before the UI disables) → resolved via idempotency, shown to the child as "already claimed" rather than an error or a double-debit (source: navigation table, "Duplicate-claim and ledger-conflict states resolve via idempotency, shown as 'already claimed'").
9. A store webhook for a related entitlement check (e.g., confirming premium status that gates a specific cosmetic item's availability) is delayed → the app uses the last verified entitlement plus a grace window, then reconciles once the webhook arrives.
10. A child attempts to claim a Weekly Challenge reward a second time after the challenge has already been claimed once and the window has since closed and re-opened for a new challenge instance → each challenge instance has its own distinct identity/ledger-reason-id, so a "second" claim against a genuinely new instance is legitimate — only a literal repeat claim against the same instance is blocked.
11. A reconciliation job detects a wallet-balance discrepancy that cannot be cleanly explained by normal ledger-sum logic → the job corrects the cached balance to match the ledger's true sum and flags the incident for manual review rather than silently "fixing" it without any record.
12. A badge has a `season_id` (a seasonal/Ramadan-specific badge) and the season ends before a child who was close to qualifying actually completes the criteria → the badge becomes unavailable for new qualification going forward, but a child who did qualify within the season window retains it permanently once earned — seasonal scoping affects earnability, not retention of an already-earned badge.

### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Duplicate reward-award request (network retry) | Ledger's unique idempotency constraint prevents the second post; standing reconciliation job confirms wallet projection integrity (FR-4/FR-14) |
| Store webhook delayed (entitlement-gated cosmetic item) | Last verified entitlement + grace window used, reconciled later (Edge Case 9) |
| Achievement Store duplicate claim | Resolved via idempotency, shown as "already claimed" (Edge Case 8) |
| Wallet-balance projection drift detected | Standing reconciliation job self-heals and logs the incident |
| Offline reward-eligible activity completion | Queues as "pending" locally, validates and finalizes on sync (FR-6) |
| Purchase succeeds but equip call fails | Ownership already committed; equip is independently retriable |

### 1.12 Empty States
- New child, zero reward history → Wallet shows a friendly "Start learning to earn your first XP!" framing rather than a stark "0" balance with no context.
- Zero badges earned yet → Achievements screen shows the first achievable milestone as a clear, motivating teaser rather than an empty grid.
- Zero Family Board contributions yet (new multi-child family) → shows the first shared goal's description with a "let's start together" framing.

### 1.13 Loading States
- Wallet: skeleton balance/ledger-list shimmer.
- Achievement Store: skeleton item-grid shimmer.

### 1.14 Offline States
- Wallet displays last-synced cached balance with an "offline, may be outdated" indicator; reward-eligible activity completions queue per FR-6.
- Achievement Store purchases require connectivity.

### 1.15 Permission States
- No new runtime permissions specific to this system.

</details>

## 7. Interactions and navigation

- {"element": "Parent Gate → OS Share Sheet, or cancel", "trigger": "Tap the corresponding source-defined control", "precondition": "Active correct child session; relevant content/permission/unlock state satisfied per cited requirements", "behavior": "Parent Gate → OS Share Sheet, or cancel", "destination": "Parent Gate → OS Share Sheet, or cancel", "validation": "Preserve cited source-specific validation; no simulated outcome may bypass parent gate, learned status, content unlock or offline availability", "back_cancel": "Dismiss overlay to originating screen; screen back returns to caller with context preserved; unresolved explicit destination must be approved", "unavailable": "Disabled or source-specific explanation when permission/unlock/content requirements fail"}

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
| Approved forward/back action | Current frame→destination, preserving directional history | 250ms ease-in-out;no delay | Reversible with Back; cancel pending animation when leaving | Instant navigation or ≤100ms dissolve | Navigate to + Dissolve; matched-layer Smart Animate only after layer-name/structure check |
| Press/release enabled control | Rest→pressed→rest; preserve hit area | 100ms ease-out scale.96 (proposal);0ms delay | Release/cancel reverses; disabled has no activation | Color/border pressed feedback only | While pressing → Change to pressed; On click → approved action |



Timing not quoted from the PRD is a labeled design proposal. No loop, flashing or parallax is required. Animate compositor-friendly opacity/transform; never delay an enabled essential action. Stop all animation/media/recording simulation on leave; no second reward reveal on restore. Status/validation always has visible text/icon independently of motion.

## 9. Figma implementation instructions — future approved execution

1. Open the exact page/node links in section2. Confirm the source text/identity; stop if the references disagree or required copy is unavailable.
2. Locate the approved reference frame. Duplicate only that frame into a user-approved enhanced-design working area; preserve original nodes and IDs. If no frame exists, create only the missing requirement-driven surface after its layout/copy approval, using approved shared assets.
3. Create `NH/Enhanced/121/Shareable_Achievement_Card_Preview/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/Shareable_Achievement_Card_Preview`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] A11 behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
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
