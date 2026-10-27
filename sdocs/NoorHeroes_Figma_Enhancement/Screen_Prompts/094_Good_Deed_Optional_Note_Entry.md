**Mandatory finalized visual baseline:** Read and apply [Finalized V2 Reusable Design Prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) before implementing this screen. Its latest approved visual rules supersede older conflicting design proposals below; PRD behavior and exact approved content remain authoritative.

# Screen 094 — Good Deed Optional Note Entry

**Documentation only. Execute this prompt only after the documentation and this screen's unresolved decisions are approved. Stop after this screen.**

## 1. Screen identification

- Feature/sub-feature: **A7 — Good Deed Optional Note Entry**.
- Surface: **screen**. Number is controlled review order, not a forced linear user journey.
- Execution status: **BLOCKED for exact approved copy: no exact Frame 1 counterpart verified. Do not fabricate copy, Arabic, educational items, user data or stats.**.
- Journey entry / previous screen: Category Selector.
- Next screen(s) / result: Check-in confirmation.
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: [Feature_A7_Habit_Tracker.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Child App (1-12)/Feature_A7_Habit_Tracker.md>); **§1.18 row 6; §1.7; §2; §6; §13**.
- Current mobile reference: **Missing independently mapped current-site screen.**
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: **Missing corresponding screen reference.** Do not substitute a visually related hub as functional evidence.
- Frame 2 container: `1085:13003`; visual reference: [Habit Builder & Sunnah Tracker](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1085-19961) — `1085:19961`. Related enhanced feature hub for visual patterns only; not an exact screen equivalent
- Reference qualification: ['Required layout has no verified exact source-frame match; access exact approved content before execution.'].
- Existing screenshot candidates (one-to-one identity is not asserted unless verified in research):
- [Habit Checklist-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Habits/Habit Checklist-01.png>)
- [Habit Checklist-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Habits/Habit Checklist-02.png>)
- [Noor Garden-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Habits/Noor Garden-01.png>)
- [Noor Garden-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Habits/Noor Garden-02.png>)
- [Streak Recovery-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Habits/Streak Recovery-01.png>)
- [Streak Recovery-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Habits/Streak Recovery-02.png>)
- Blueprint alignment:
- [01-habit-builder-todays-checklist-experience.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A7_Habit_Tracker/KMP/01-habit-builder-todays-checklist-experience.md>)
- [02-dhikr-counter-interaction-target-adjustment.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A7_Habit_Tracker/KMP/02-dhikr-counter-interaction-target-adjustment.md>)
- [03-good-deed-logging-fasting-tracker-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A7_Habit_Tracker/KMP/03-good-deed-logging-fasting-tracker-flow.md>)
- [04-streak-calendar-state-detail-recovery-mission-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A7_Habit_Tracker/KMP/04-streak-calendar-state-detail-recovery-mission-flow.md>)
- [05-noor-garden-personal-family-visualization.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A7_Habit_Tracker/KMP/05-noor-garden-personal-family-visualization.md>)
- [06-offline-checkin-outbox-chronological-sync-engine.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A7_Habit_Tracker/KMP/06-offline-checkin-outbox-chronological-sync-engine.md>)
- [07-habit-reminder-deep-link-quiet-hours-landing.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A7_Habit_Tracker/KMP/07-habit-reminder-deep-link-quiet-hours-landing.md>)
- [08-parent-area-habit-visibility-reminder-verification-configuration.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A7_Habit_Tracker/KMP/08-parent-area-habit-visibility-reminder-verification-configuration.md>)
- [09-weekly-habit-report-in-app-parent-view.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A7_Habit_Tracker/KMP/09-weekly-habit-report-in-app-parent-view.md>)
- [10-ramadan-mode-checklist-variant-ethical-messaging-safeguards.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A7_Habit_Tracker/KMP/10-ramadan-mode-checklist-variant-ethical-messaging-safeguards.md>)
- [11-habit-tracker-analytics-cross-platform-event-instrumentation.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A7_Habit_Tracker/KMP/11-habit-tracker-analytics-cross-platform-event-instrumentation.md>)
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: - CL-05 See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

Enable Good Deed Optional Note Entry in the established A7 journey. Entry: Category Selector. Required outcome: Check-in confirmation.

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

**FR-1** Habit Builder's "Today" view shows a checklist of the child's currently-configured habits: Salah (by prayer), Quran reading, daily duas, good deeds, dhikr counter, and optionally a Ramadan fasting tracker — scoped by parent configuration and child age (source §6.5, §21.14, screen catalog "Habit Builder").

**FR-4** Habit check-in events store: local date, timezone, source, an optional parent-verification flag, and an optional note category — sensitive personal notes are never required (source §6.5/§21.14).

**FR-6** Parent verification of a habit claim is **optional** per habit/child and must never be framed in copy or UI treatment as "religious policing" — verification is presented as supportive co-participation (e.g., "Mark this together"), never surveillance (source: hard ethical/copy constraint, §6.5/§screen-catalog).

**FR-17** Fasting Tracker (Ramadan/practice fasts) is optional and parent-controlled, with age-appropriate fasting education content linked (source §6.5 Habit Types, §6.5 "fasting tracker (optional, parent-controlled)").

**FR-19** Noor Garden visual progression: each habit type grows a distinct part of a personal progress world (Quran tree, kindness flowers, Salah lanterns, dua stars, Ramadan moon path); siblings contribute to shared Family Garden milestones (e.g., 100 duas, 30 good deeds, 7 family story nights, a complete Ramadan journey) (source §"Noor Garden Progress World").

## 4. Exact content specification

### Requirement-driven fields and content roles

- Not supplied by this source; resolve before execution.

**Exact copy unavailable: execution blocked for copy-dependent design.** Locate the authoritative content registry/original frame; do not insert placeholder, paraphrased or AI-generated copy. This document still specifies the required surface so it is not omitted.

Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.

## 5. Visual enhancement instructions

- Checklist orders configured habits under date/streak summary and large targets. Dhikr receives a distinct large circular counter with decrement/reset alternatives. Garden imagery shows cumulative growth; family view is aggregate only. Recovery uses warm invitation and avoids visual failure/shame.

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

1. Child checks in a habit at 11:58pm local time, and the check-in's server-processing completes at 12:01am due to a slow network request → the `local_date` recorded must reflect the time of the **client-side check-in action** (captured client-side at tap time and sent in the request payload), not the server's processing timestamp, to avoid an unfair day-boundary mismatch.
2. Child rapidly taps a habit checkbox on/off multiple times before the request completes (accidental double-tap or indecision) → idempotent handling via `client_request_id` per distinct intended state ensures the final persisted state matches the child's last intended action, without duplicate reward issuance and without a flickering UI.
3. Parent disables a previously-visible habit type while the child has an active streak partially built on that habit type → the historical streak/reward data for that habit is preserved (not deleted), but it's removed from today's checklist going forward; if the disabled habit was the sole contributor to an active daily streak chain, the streak's continuation now depends on other still-enabled habits or a different meaningful activity, evaluated fairly (the child isn't penalized retroactively for the parent's configuration change).
4. Two children share a device; Child A checks in a habit, then the device switches to Child B before Child A's offline check-in has synced → the queued offline check-in remains correctly attributed to Child A's `child_id` (captured at action time, not sync time) and syncs correctly regardless of which child's session is currently active when connectivity returns.
5. Family Streak threshold is met by the combined effort of multiple siblings on the same day, but one sibling's individual check-in event hasn't synced yet (still offline) → the Family Streak's authoritative server-side evaluation only counts confirmed, synced check-ins; the family reward/milestone fires once that sibling's event syncs and crosses the threshold (no premature/optimistic family-level reward issuance based on unconfirmed client state).
6. Child sets up a recurring Dhikr Counter target, then changes the target mid-day after having already partially completed today's count → today's progress is preserved proportionally against the new target (not reset to zero), with a sensible recalculation (e.g., if they did 50 of an old 100 target and change to a new 150 target, they're now at 50/150, not back to 0/150).
7. A child's account is flagged for Mercy Day usage many days in a row (e.g., genuinely inconsistent engagement rather than occasional grace) → the system does not editorialize or "punish" this pattern through any UI signal, but the Habit Intelligence Model's missed-pattern detection (FR-14) may still surface a gentle, supportive suggestion — this is fundamentally different from any punitive escalation, and the distinction must be preserved in implementation (suggestion frequency may increase, tone never sharpens).
8. Parent enables "parent verification" for a habit, but is unavailable/offline for an extended period and never verifies a pending claim → the child's own streak/reward progress is **not blocked** waiting on parent verification (verification is supplementary/optional context for the parent, never a gate on the child's actual reward/streak mechanics) — this must be true even though FR-6 allows verification to exist, since verification is "optional" precisely in this sense.
9. Ramadan mode activates mid-cycle while a child has an active non-Ramadan streak → the streak doesn't reset; "meaningful activity" eligibility simply expands to include the newly-relevant Ramadan-specific habit types for that period, then reverts appropriately when Ramadan mode ends (no streak discontinuity purely due to the seasonal mode switch).
10. A child attempts to log an excessive number of "good deeds" in a single day (e.g., 50 taps) in an apparent attempt to inflate engagement metrics or test the system → the daily cap (FR-3) limits actual reward issuance to the configured cap regardless of tap count, and an anomalous-volume pattern may be flagged for fraud/abuse monitoring (not shown to the child as an error — the excess taps simply don't yield additional reward, framed neutrally).
11. Child's server-maintained timezone record becomes stale/incorrect (e.g., they moved permanently to a new timezone months ago but the system never updated) → there must be a mechanism (automatic detection via repeated device-timezone-mismatch signals, or explicit parent/child confirmation) to update the server-maintained timezone of record without requiring a manual support ticket for every case, while still being resistant to abuse (frequent flip-flopping triggers a different, more conservative grace path than a single stable shift).
12. A habit check-in attempt is made for a `local_date` significantly in the past (e.g., backfilling after being offline for several days while traveling with no connectivity at all) → the system must support reconciling a batch of queued historical check-ins on reconnect, each evaluated against its own correct historical `local_date`, with the streak state machine re-computed correctly across the gap (not just blindly applied as if it were "today") — this is a more complex version of the standard offline-sync pattern, specific to a calendar-day-sensitive feature.

### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Habit check-in sync fails (network) | Local state already updated (offline-first); background retry with exponential backoff; never shown as a child-facing error, since the local experience already succeeded |
| Streak state-machine evaluation service unavailable | Last-known cached streak display shown with no alarming "error" framing; recalculated once the service is reachable, never silently reset to zero as a fallback |
| Family Streak aggregation service degraded | Personal/individual habit check-ins and rewards proceed unaffected; Family Garden visual simply doesn't update until the aggregation service recovers, shown as a gentle "growing..." state rather than an error |
| Dhikr Counter audio pronunciation asset fails to load | Counter still fully functional without audio (silent tactile counting), audio retried in background |
| Backfilled historical check-in conflicts with an already-recorded entry for that date | Idempotent merge — existing entry wins, no duplicate reward, no error shown |
| Parent verification request fails to deliver/notify parent | Child's progress is entirely unaffected (per Edge Case 8); parent sees the pending-verification item next time they open the relevant screen, no urgency-framed error |

### 1.12 Empty States
- New child, zero habits configured by parent yet → Habit Builder shows a friendly "ask a grown-up to set up your first habit" prompt with a parent deep-link (consistent with A.2 Edge Case 9).
- Zero streak history yet → Streak display shows a warm "Let's start your first day!" framing rather than a "0" presented starkly.
- Family Garden with zero family-level milestones reached yet → shows the garden's "seedling" starting state with a description of the first milestone to work toward.

### 1.13 Loading States
- Habit checklist: skeleton checklist shimmer (rare given offline-first design — mostly relevant on true first load).
- Streak calendar: skeleton calendar grid.

### 1.14 Offline States
- Full offline check-in functionality per FR-2; persistent (non-alarming) "syncing..." indicator when there's a pending local queue.
- Dhikr Counter and other purely-local-interaction habit types function identically offline.

### 1.15 Permission States
- No new runtime permissions; relies on existing notification permission (shared with A.12) for habit reminders.

</details>

## 7. Interactions and navigation

- {"element": "Check-in confirmation", "trigger": "Tap the corresponding source-defined control", "precondition": "Active correct child session; relevant content/permission/unlock state satisfied per cited requirements", "behavior": "Check-in confirmation", "destination": "Check-in confirmation", "validation": "Preserve cited source-specific validation; no simulated outcome may bypass parent gate, learned status, content unlock or offline availability", "back_cancel": "Dismiss overlay to originating screen; screen back returns to caller with context preserved; unresolved explicit destination must be approved", "unavailable": "Disabled or source-specific explanation when permission/unlock/content requirements fail"}

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
3. Create `NH/Enhanced/094/Good_Deed_Optional_Note_Entry/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/Good_Deed_Optional_Note_Entry`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] A7 behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
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
