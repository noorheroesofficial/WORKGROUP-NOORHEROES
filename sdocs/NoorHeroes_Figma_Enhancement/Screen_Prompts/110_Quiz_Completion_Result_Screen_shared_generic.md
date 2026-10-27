**Mandatory finalized visual baseline:** Read and apply [Finalized V2 Reusable Design Prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) before implementing this screen. Its latest approved visual rules supersede older conflicting design proposals below; PRD behavior and exact approved content remain authoritative.

# Screen 110 — Quiz Completion Result Screen (shared, generic)

**Documentation only. Execute this prompt only after the documentation and this screen's unresolved decisions are approved. Stop after this screen.**

## 1. Screen identification

- Feature/sub-feature: **A9 — Quiz Completion Result Screen (shared, generic)**.
- Surface: **screen**. Number is controlled review order, not a forced linear user journey.
- Execution status: **Preserve all literal Frame 1 text; source sample statistics are fixtures only and religious strings remain subject to source verification.**.
- Journey entry / previous screen: End of any quiz/practice attempt (any domain, any A.8 `QuizContext`).
- Next screen(s) / result: Review Mistakes / Try Again / Continue.
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: [Feature_A9_Skill_Tree_Mastery_Engine.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Child App (1-12)/Feature_A9_Skill_Tree_Mastery_Engine.md>); **§1.18 row 1; §1.7; §2; §6; §13**.
- Current mobile reference: **Missing independently mapped current-site screen.**
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: [Html → Body](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1106-3444) — `1106:3444`. Exact/closest named existing frame; preserve purpose and copy; theme/player subtype must be checked
- Frame 2 container: `1085:13003`; visual reference: [Quiz Completion & Mastery Result](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1085-20220) — `1085:20220`. Related enhanced feature hub for visual patterns only; not an exact screen equivalent
- Reference qualification: [].
- Existing screenshot candidates (one-to-one identity is not asserted unless verified in research):
- [Quiz Complete-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Quiz Engine/Quiz Complete-01.png>)
- [Quiz Complete-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Quiz Engine/Quiz Complete-02.png>)
- [Quiz Question-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Quiz Engine/Quiz Question-01.png>)
- [Quiz Question-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Quiz Engine/Quiz Question-02.png>)
- [Quiz Question-03.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Quiz Engine/Quiz Question-03.png>)
- [Quiz Question-04.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Quiz Engine/Quiz Question-04.png>)
- [Quiz Result-01.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Quiz Engine/Quiz Result-01.png>)
- [Quiz Result-02.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Quiz Engine/Quiz Result-02.png>)
- [Quiz Result-03.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Quiz Engine/Quiz Result-03.png>)
- [Quiz Result-04.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Quiz Engine/Quiz Result-04.png>)
- [Quiz Result-05.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Quiz Engine/Quiz Result-05.png>)
- [Quiz Result-06.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Quiz Engine/Quiz Result-06.png>)
- [Quiz Result-07.png](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Screens/Mobile App/Quiz Engine/Quiz Result-07.png>)
- Blueprint alignment:
- [01-shared-mastery-engine-core-module.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A9_Skill_Tree_Mastery_Engine/KMP/01-shared-mastery-engine-core-module.md>)
- [02-quiz-completion-result-screen.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A9_Skill_Tree_Mastery_Engine/KMP/02-quiz-completion-result-screen.md>)
- [03-skill-tree-state-renderer.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A9_Skill_Tree_Mastery_Engine/KMP/03-skill-tree-state-renderer.md>)
- [04-mastery-result-offline-handling-sync.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A9_Skill_Tree_Mastery_Engine/KMP/04-mastery-result-offline-handling-sync.md>)
- [05-cross-domain-mastery-analytics-integration.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A9_Skill_Tree_Mastery_Engine/KMP/05-cross-domain-mastery-analytics-integration.md>)
- [06-cross-domain-parent-mastery-summary.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A9_Skill_Tree_Mastery_Engine/KMP/06-cross-domain-parent-mastery-summary.md>)
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: - CL-02
- CL-04 See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

Enable Quiz Completion Result Screen (shared, generic) in the established A9 journey. Entry: End of any quiz/practice attempt (any domain, any A.8 `QuizContext`). Required outcome: Review Mistakes / Try Again / Continue.

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

**FR-4** A child can retry any practice item without losing XP or breaking a streak — mastery-affecting accuracy and reward-affecting participation are fully decoupled systems (source §6.3, shared architectural principle with A.8's quiz engine).

**FR-6** Quiz Completion Result flow (the shared result screen after any quiz/practice attempt): validate the attempt and its idempotency key → calculate skill evidence → post the reward-ledger entry (unconditional, per A.8 FR-5) → show a result screen with **strengths and exactly one concrete next step** → offer `Review Mistakes`, `Try Again`, or `Continue` → record a parent-report event (source §21.10 "Quiz Completion" flow, items 1–7).

**FR-10** A withdrawn/safety-flagged quiz item's evidence is excluded from mastery-score computation even if the response was recorded before withdrawal (shared rule with A.8 FR-11, enforced once here at the mastery-aggregation layer so every domain inherits it automatically).

## 4. Exact content specification

### Frame 1 — exact layer text (separate source; differences need approval)

```text
Mastery Milestone Reached!
Wonderful Exploration!
Your thoughtful practice today showed
wonderful curiosity, patience, and care.
Your Strengths Today
You're getting really
confident with Surah Al-
Fatiha recitation & rhythm!
Beautiful Cadence
Spot-on connection with key
vocabulary meanings!
Thoughtful Understanding
🌱
Next Step
2-min listen
Gentle Listening
Try listening to Ayat 4–7 at a
relaxed tempo to master the
vowel transitions.
Play Gentle Audio Preview
Continue Journey
Review Mistakes
Try Again
Step 3 of 4
```

### Requirement-driven fields and content roles

- Not supplied by this source; resolve before execution.

Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.

## 5. Visual enhancement instructions

- Strengths precede exactly one concrete Next Step. Review Mistakes, Try Again and Continue have equal visual weight; omit Review Mistakes when none exist. Never expose raw mastery/confidence scores. Offline saved screen avoids provisional result claims.

- Preserve content order and screen purpose. Use a vertical auto-layout content stack; horizontal inset 20, base spacing 4/8/12/16/24/32; card content padding 12–16. Keep compact controls next to their labels; align headings and cards to one column edge.
- Use existing cream `#FAF7F0`, surface `#FFFFFF`, ink `#1C2B33`, teal `#0E7C7B`, gold `#D4A24C`. Gold/bright teal are accents, not untested small-text colors. Body 14/16; heading 20/24; brand-only display 28/32. Preserve actual font assets; PRD Latin sans, display serif, separate verified Arabic content font.
- Do not import Frame 2's sample statistics, claims, religious text, section additions or combined desktop layouts. Borrow hierarchy, restrained surface separation and image framing only where they support this surface.
- Screen viewport is separate from long content height. Use vertical overflow when content exceeds available height; header/footer may be fixed only with bottom and top content clearance. At 320/360/390/420 logical widths, long labels wrap. At 200% text scale, stack grids or allow scrolling; no fixed text block height or sacred-text ellipsis.
- Essential touch target≥44×44 logical units; younger-child primary tasks≥56 where A2 specifies. Decorative icons have no hit targets. Assets retain aspect ratio; no text burned into illustrations. Safe area and keyboard must never obscure the current action.
- Source frames, unrelated screens and existing design direction remain unchanged. Token/component changes require separate review; never detach or globally mutate a source instance to fix this screen.

## 6. Screen states and conditional scenarios

- Default as described in cited source
- Answer selected where submission required
- Submitting / explanation shown
- Media loading or graceful skip when relevant
- Cached-bank offline / resume at saved index
- All correct (no Review Mistakes)
- Some incorrect with supportive review
- Server-confirmed reward versus pending offline state
- Mastery threshold accent only when confirmed
- Bedtime calm/reduced-motion variant



Only apply states that belong to this surface. List-only empty/skeleton states are not added to legal documents or static intros. Network submit has a pending/timeout/retry result; retry preserves draft and must not duplicate a server-confirmed operation. Voice states need consent + OS grant; denial supplies listen/text/manual alternative. Loading/error/disabled/offline wording missing from source is a content approval gap.

<details><summary>Authoritative state/edge source context — apply screen-relevant cases, not all cases indiscriminately</summary>

### 1.10 Edge Cases

1. A child answers correctly across two sessions but always via the exact same question format (e.g., always multiple choice, never audio match) for a skill that has multiple available formats → the cross-format-transfer component of the mastery formula appropriately limits confidence growth, keeping the skill in `Practicing` rather than `Mastered` until transfer evidence exists, consistent with FR-2/FR-5.
2. A child has overwhelming evidence of mastery on a skill, then gets one unusual wrong answer (e.g., a misclick) → a single low-quality data point should not catastrophically collapse a strongly-evidenced mastery state; the recency/weighting formula must be resilient to single-attempt noise, not just simplistically averaging.
3. Two different domains (e.g., a Quran skill and a hypothetical future Islamic Facts skill) are tagged on the same quiz question (cross-domain question reuse) → mastery evidence updates correctly and independently for both domains' respective skill nodes from the same single response event, without conflation.
4. A child reaches `Needs Refresh` on multiple skills simultaneously across different domains on the same day → the platform-wide daily-prompt cap (default 2, per FR-8) applies globally across all domains combined, not per-domain (a child should not see 2 Quran refreshes AND 2 Arabic refreshes on the same day if the intent is to cap total daily review load) — this requires the engine to coordinate the cap centrally rather than each domain enforcing its own independent cap.
5. A child selects `Review Mistakes` from the Quiz Completion Result, reviews the explanations, then closes the app without selecting `Continue` explicitly → the underlying quiz attempt is still considered complete (reward already issued per A.8's unconditional rule) regardless of whether the child formally dismisses the result screen — no dangling "incomplete" state should result from simply not tapping a final button.
6. A new domain is configured by Admin with a skill-node catalog that has a prerequisite cycle (e.g., copy-paste error from another domain's graph) → the shared engine's cycle-detection validation (same mechanism specified in A.5 §9 for curriculum graphs) applies uniformly to any domain's graph, not just Quran/Arabic's.
7. A child's mastery-score computation coincides with a quiz-completion event for a withdrawn-question-containing attempt (per FR-10) — the score computed and the score that *would have been* computed without the exclusion are different; this difference itself should be logged for content-quality monitoring (a spike in withdrawal-driven exclusions for a given skill might indicate a content-quality issue in that skill's question pool worth flagging to Admin).
8. A child attempts to "game" the spaced-repetition scheduler by intentionally answering incorrectly on a skill they've already mastered, theoretically to trigger more frequent review sessions (an unusual but conceivable motivation, e.g., wanting more practice) → the system doesn't need to detect or prevent this; if a child genuinely wants more practice, more low-confidence evidence naturally extending their practice opportunities is not a harmful outcome, so no special anti-gaming logic is required here (distinct from genuinely harmful gaming like reward-farming, which IS prevented elsewhere).
9. Mastery-score formula parameters (the relative weights of accuracy/recency/difficulty/transfer) are updated by Admin for model-quality-improvement reasons → already-computed historical mastery states are **not retroactively recalculated** under the old evidence with new weights (which could cause confusing, unexplained state changes for children with no new activity) — the new weights apply only to future evidence-driven recalculations, with a clear changelog/versioning of which formula version produced which historical state.
10. A child's account is merged/migrated (e.g., a rare data-correction scenario) and brings mastery evidence from two previously-separate `child_id` records for the same skill → the engine must have a defined, tested reconciliation behavior (e.g., taking the union of evidence, recalculating from scratch) rather than undefined behavior from a naive merge.
11. A `skill_node`'s prerequisite is itself a node from a different domain (a genuinely cross-domain prerequisite, e.g., a hypothetical future "basic Arabic literacy" prerequisite gating a Quran-domain node) → the engine's prerequisite-evaluation logic must support cross-domain references without special-casing, since `skill_node` and `skill_node_state` are domain-agnostic tables by design.
12. The spaced-repetition decay function computes a `next_review_at` date that has already passed by the time the batch scheduler runs (e.g., due to a scheduler outage/delay) → the review is still correctly queued (not skipped) on the next successful run, with the existing daily-prompt cap preventing a backlog from dumping many overdue reviews on the child at once.

### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Mastery-score computation service unavailable post-quiz | Reward issuance (unconditional, A.8) still completes independently; mastery update queues for retry, Quiz Completion Result screen shows strengths/next-step based on the most recent available state rather than blocking on a synchronous recomputation |
| Spaced Repetition Scheduler batch job failure | No reviews lost — overdue reviews queue correctly on next successful run (Edge Case 12), capped per the standing daily limit |
| Cross-domain prerequisite graph contains a cycle (admin error) | Rejected at admin-save time with the cycle path shown (shared validation mechanism with A.5) |
| Quiz attempt's idempotency key resubmitted (e.g., network retry of the completion call) | Returns the original mastery/reward result, never double-processes evidence |

### 1.12 Empty States
- New child, zero mastery evidence for a domain → all relevant skill nodes show `Locked`/`Ready` states appropriately per prerequisite graph, never an error or blank tree (consistent with A.5's first-time experience).
- Quiz Completion Result with zero mistakes to review → "Review Mistakes" option simply isn't offered (only `Try Again`/`Continue` shown), consistent with A.8 Edge Case 11.

### 1.13 Loading States
- Quiz Completion Result: brief "calculating your progress..." state if mastery computation hasn't completed synchronously within a short budget, though typically near-instant given the p95 < 300ms target.

### 1.14 Offline States
- Mastery-state display uses last-synced cached state when offline; recomputation requiring fresh evidence happens upon reconnect sync, consistent with A.5/A.8's offline patterns.

### 1.15 Permission States
- No new runtime permissions specific to this engine.

</details>

## 7. Interactions and navigation

- {"element": "Review Mistakes", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "Review only missed items and explanations; no new scored attempt", "destination": "Review only missed items and explanations; no new scored attempt", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}
- {"element": "Try Again", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "Fresh quiz/practice attempt with new attempt id", "destination": "Fresh quiz/practice attempt with new attempt id", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}
- {"element": "Continue", "trigger": "Tap", "precondition": "Screen-specific availability from cited requirements; correct active child and source content", "behavior": "Originating consuming feature; no penalty", "destination": "Originating consuming feature; no penalty", "validation": "Use applicable source states; server data authoritative; retain per-screen gates and offline constraints", "back_cancel": "Return to originating screen/state; preserve committed progress; cancel non-committal preview without side effects", "unavailable": "Use the screen-specific disabled, prerequisite, offline, or permission fallback; do not invent a bypass"}

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
| Data-confirmed success or first entry | Hidden status→visible check/progress; splash logo opacity0→1 scale.98→1 | 400ms ease-out; splash≤1200ms; reward total≤2000ms;no mandatory wait | Skippable/interruptible; stop on leave; no reward repeats after resume | Static success/brand state | Smart Animate between matching states; After delay only for visual sequence, never server validation |
| Press/release enabled control | Rest→pressed→rest; preserve hit area | 100ms ease-out scale.96 (proposal);0ms delay | Release/cancel reverses; disabled has no activation | Color/border pressed feedback only | While pressing → Change to pressed; On click → approved action |



Timing not quoted from the PRD is a labeled design proposal. No loop, flashing or parallax is required. Animate compositor-friendly opacity/transform; never delay an enabled essential action. Stop all animation/media/recording simulation on leave; no second reward reveal on restore. Status/validation always has visible text/icon independently of motion.

## 9. Figma implementation instructions — future approved execution

1. Open the exact page/node links in section2. Confirm the source text/identity; stop if the references disagree or required copy is unavailable.
2. Locate the approved reference frame. Duplicate only that frame into a user-approved enhanced-design working area; preserve original nodes and IDs. If no frame exists, create only the missing requirement-driven surface after its layout/copy approval, using approved shared assets.
3. Create `NH/Enhanced/110/Quiz_Completion_Result_Screen_shared_generic/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/Quiz_Completion_Result_Screen_shared_generic`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] A9 behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
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
