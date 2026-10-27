**Mandatory finalized visual baseline:** Read and apply [Finalized V2 Reusable Design Prompt](../12_FINALIZED_V2_REUSABLE_DESIGN_PROMPT.md) before implementing this screen. Its latest approved visual rules supersede older conflicting design proposals below; PRD behavior and exact approved content remain authoritative.

# Screen 105 — Quiz Question Screen — Image Match

**Documentation only. Execute this prompt only after the documentation and this screen's unresolved decisions are approved. Stop after this screen.**

## 1. Screen identification

- Feature/sub-feature: **A8 — Quiz Question Screen — Image Match**.
- Surface: **screen**. Number is controlled review order, not a forced linear user journey.
- Execution status: **Preserve all literal Frame 1 text; source sample statistics are fixtures only and religious strings remain subject to source verification.**.
- Journey entry / previous screen: Quiz Entry Card.
- Next screen(s) / result: Per-Answer Explanation.
- Platforms: Android and iOS mobile, shared Compose experience. OS permission, biometric, store and back behavior are simulated and annotated separately.
- Index and branch owners: [Master index](../00_MASTER_INDEX.md), [inventory](../02_SCREEN_INVENTORY_AND_ORDER.md).

## 2. Reference mapping

- PRD: [Feature_A8_Daily_Quiz_Engine.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/PRD_Documents/Child App (1-12)/Feature_A8_Daily_Quiz_Engine.md>); **§1.18 row 5; §1.7; §2; §6; §13**.
- Current mobile reference: [NoorHeroes current preview](https://noorheroes.figma.site/) → selector **Quiz Question**; exact text captured below.
- Figma page: `📱 NH Mobile `, `928:2`.
- Frame 1 container: `1095:2`; corresponding screen: [Quiz Question Screen](https://www.figma.com/design/MR9935oQZACMjndzGIUgq5/NoorHeroes-APP?node-id=1106-3276) — `1106:3276`. Exact/closest named existing frame; preserve purpose and copy; theme/player subtype must be checked
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
- [01-shared-quiz-engine-core-module.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A8_Daily_Quiz_Engine/KMP/01-shared-quiz-engine-core-module.md>)
- [02-quiz-session-state-management-resume-flow.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A8_Daily_Quiz_Engine/KMP/02-quiz-session-state-management-resume-flow.md>)
- [03-question-type-renderers-accessibility-paths.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A8_Daily_Quiz_Engine/KMP/03-question-type-renderers-accessibility-paths.md>)
- [04-per-answer-explanation-non-punitive-feedback-ui.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A8_Daily_Quiz_Engine/KMP/04-per-answer-explanation-non-punitive-feedback-ui.md>)
- [05-retry-set-accuracy-independent-completion-experience.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A8_Daily_Quiz_Engine/KMP/05-retry-set-accuracy-independent-completion-experience.md>)
- [06-offline-quiz-bank-sync-withdrawn-question-handling.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A8_Daily_Quiz_Engine/KMP/06-offline-quiz-bank-sync-withdrawn-question-handling.md>)
- [07-parent-concept-summary-report.md](<C:/Users/Sarva/Documents/WORKGROUP-NOORHEROES/Development_Blueprints/A8_Daily_Quiz_Engine/KMP/07-parent-concept-summary-report.md>)
- Components/assets: reuse actual cited reference layers/assets after checking ownership; extracted frame descendants have zero component instances. Component architecture is proposed in [shared guidelines](../05_DESIGN_SYSTEM_AND_COMPONENT_GUIDELINES.md); do not pretend reusable instances already exist.
- Gaps / conflicts: - CL-04 See [decision register](../09_OPEN_QUESTIONS_AND_APPROVALS.md). Missing references remain missing; do not create a replacement direction.

## 3. Screen purpose

Enable Quiz Question Screen — Image Match in the established A8 journey. Entry: Quiz Entry Card. Required outcome: Per-Answer Explanation.

Primary and secondary actions and expected results are defined in section 7. Preserve the role and entry conditions above; do not expose parent-only content in child mode.

Screen-specific mandatory requirement excerpts (when individually mapped):

**FR-1** Daily Quiz assembles exactly 5 questions per session, sourced from a mix of recently-learned content and identified weak skills (source §6.3/§21.9).

**FR-2** Supported question types: multiple choice, sequence/ordering, true/false, image match, audio match (source §6.3/§21.9/§23.5) — the engine must support all five types as first-class, reusable across every consuming feature.

**FR-5** Quiz completion always awards effort XP, regardless of accuracy; accuracy independently feeds the Skill Mastery model's confidence calculation but never reduces or withholds the base participation reward (source §6.3/§21.9/§A.5 FR-16 cross-reference — a hard, platform-wide rule restated here as this engine's authoritative implementation point).

**FR-6** Parent-facing reporting from any quiz attempt must surface concepts/skills addressed, not a bare numeric score as the headline (source §6.3/§21.9).

**FR-7** Each question records: `question_id`, `content_version_id`, attempt number, answer, response time, hint count, and an offline flag (source §21.9 "Detailed sample screen" data fields) — this data model is shared across all question types and all consuming features.

**FR-9** The Quiz Engine must be embeddable/contextualized by the calling feature — a Daily Quiz widget instance (Home), a Learn-tab skill-practice instance (A.5), a post-Story instance (A.3, "3 to 5 questions"), and a Dua recall instance (A.6, "1 to 3 questions") all use the same underlying attempt/response/scoring contract, parameterized by question count and source pool rather than divergent implementations.

**FR-10** Offline quiz attempts are supported when the question bank was included in a content download package; results sync on reconnect with idempotent submission (cross-ref A.3/A.5/A.6 offline patterns).

**FR-11** A quiz attempt that references a question later withdrawn for safety reasons must still sync for historical record purposes, but the withdrawn item is **excluded from mastery and reward calculation** even if the attempt predates the withdrawal and is syncing late (source: Error & Edge-Case Matrix, "Offline quiz uses a withdrawn question → Sync the attempt for history, but exclude the withdrawn item from mastery/reward if it was withdrawn for safety reasons").

**FR-12** Distractor (wrong-answer-option) quality is governed by the Quiz Builder's content-authoring validation, including a "preview for mobile and screen reader" check before publish (source §23.5) — this engine's read path trusts that published questions have passed this authoring-side quality gate.

**FR-13** Question versions are locked after publication (source §23.5 "Version lock after publication") — an in-flight quiz session must never have a question's content change underneath it mid-attempt; edits create a new version for future sessions only.

**FR-14** Quiz attempts are idempotent via `client_request_id` at the attempt level, consistent with the platform's universal idempotency pattern (source §9.3 `quiz_attempts`/`quiz_responses` schema notes).

**FR-15** The engine must support per-question skill-tagging (linking a question to one or more skill/mastery nodes) so that a single quiz session can simultaneously update mastery confidence across multiple distinct skills.

## 4. Exact content specification

### Current mobile source — exact captured text

```text
Question 1 of 5

💡
📖
Quran Knowledge
Multiple Choice

How many surahs (chapters) are in the Quran?

A

112 surahs

B

114 surahs

C

116 surahs

D

120 surahs
```

### Frame 1 — exact layer text (separate source; differences need approval)

```text
Daily Quest • Prophet Stories
3 Quest Streak
Quest 2 of 5
Option A
The Dove
Option B • Selected
The Hoopoe (Hud-hud)
Option C
The Falcon
Option D
The Swallow
Need a clue? (1 left)
Check Answer
Take your time! Learning is an adventure.
Prophet Sulayman (as)
Which bird delivered the letter
from Prophet Sulayman (as) to
the Queen of Sheba?
Tap to hear story
9:41
Active Quiz Session
```

### Requirement-driven fields and content roles

- Not supplied by this source; resolve before execution.

Captured names, values, dates, progress and prices are reference fixtures, not live facts. Preserve strings for comparison only; do not fabricate new data. Religious text, translations, Arabic glyphs and scholar/verification claims require original content IDs and review provenance. No machine translation or content invention. Unknown locale strings remain blocked, not translated here. Demo labels such as Default/Loading/FR annotations are recorded source text; whether to remove them from the product requires the audit decision.

## 5. Visual enhancement instructions

- Approved image options each include descriptive alt-text; matching prompt and selected icon/border. Media-failure question skips as unanswered, not wrong.

- Preserve content order and screen purpose. Use a vertical auto-layout content stack; horizontal inset 20, base spacing 4/8/12/16/24/32; card content padding 12–16. Keep compact controls next to their labels; align headings and cards to one column edge.
- Use existing cream `#FAF7F0`, surface `#FFFFFF`, ink `#1C2B33`, teal `#0E7C7B`, gold `#D4A24C`. Gold/bright teal are accents, not untested small-text colors. Body 14/16; heading 20/24; brand-only display 28/32. Preserve actual font assets; PRD Latin sans, display serif, separate verified Arabic content font.
- Do not import Frame 2's sample statistics, claims, religious text, section additions or combined desktop layouts. Borrow hierarchy, restrained surface separation and image framing only where they support this surface.
- Screen viewport is separate from long content height. Use vertical overflow when content exceeds available height; header/footer may be fixed only with bottom and top content clearance. At 320/360/390/420 logical widths, long labels wrap. At 200% text scale, stack grids or allow scrolling; no fixed text block height or sacred-text ellipsis.
- Essential touch target≥44×44 logical units; younger-child primary tasks≥56 where A2 specifies. Decorative icons have no hit targets. Assets retain aspect ratio; no text burned into illustrations. Safe area and keyboard must never obscure the current action.
- Source frames, unrelated screens and existing design direction remain unchanged. Token/component changes require separate review; never detach or globally mutate a source instance to fix this screen.

## 6. Screen states and conditional scenarios

- Question ready
- Selected answer where applicable
- Submitting / retry with same response context
- Immediate explanation for correct and incorrect
- Progressive hint
- Offline cached question bank / resumable session
- Media-loading or graceful unanswered skip only for image/audio types



Only apply states that belong to this surface. List-only empty/skeleton states are not added to legal documents or static intros. Network submit has a pending/timeout/retry result; retry preserves draft and must not duplicate a server-confirmed operation. Voice states need consent + OS grant; denial supplies listen/text/manual alternative. Loading/error/disabled/offline wording missing from source is a content approval gap.

<details><summary>Authoritative state/edge source context — apply screen-relevant cases, not all cases indiscriminately</summary>

### 1.10 Edge Cases

1. A child's weak-skill pool is empty (e.g., a brand-new learner with very little history) → the 5-question assembly falls back to a sensible default mix (recent content + a small set of foundational/placement-relevant questions) rather than failing to produce a full 5-question set.
2. A child has so many weak skills that more than 5 qualify for inclusion → the assembly algorithm prioritizes (e.g., by recency-of-weakness, skill importance, or balanced topic coverage) rather than arbitrarily; this prioritization logic should be deterministic and explainable for QA/debugging purposes, not a black box.
3. A retry-set question is also answered incorrectly a second time → the system does not infinitely re-loop the same question within one session; after a bounded number of retry rounds (e.g., 1 retry round), the session concludes with supportive framing and the concept is flagged more strongly for future weak-skill prioritization, rather than trapping the child in an endless retry loop.
4. A child attempts a quiz offline using a downloaded question bank, and one of those questions happens to be a "weak skill" question whose weak-skill status has since changed server-side (the child since improved on it through other practice) → the offline-served question bank reflects whatever was true at download time; on sync, the server's authoritative mastery model is what's actually updated (the stale client-side weak-skill framing doesn't cause incorrect mastery double-counting, since mastery is recalculated server-side from the actual response data, not from the client's assumed reason-for-inclusion).
5. A child rapidly answers all 5 questions in an implausibly short time (e.g., random tapping) → `response_time_ms` is recorded and may feed an anomaly/quality signal for mastery-confidence weighting (a suspiciously fast correct answer contributes less confidence than a thoughtfully-timed one), without blocking the child's reward (effort XP is unconditional per FR-5) or accusing them of cheating in any visible way.
6. Two consuming features (e.g., Stories' post-episode quiz and Home's Daily Quiz widget) could theoretically select overlapping questions for the same child on the same day → this is acceptable and not treated as an error (repetition across distinct contexts has its own spaced-repetition value), but the weak-skill-pool logic should avoid recommending the *exact same* question instance twice within a very short time window (e.g., the same hour) to avoid a jarring "didn't I just answer this" experience.
7. An image-match or audio-match question's media asset fails to load mid-quiz → the question gracefully skips (treated as unanswered, not as an incorrect answer) with a brief explanation ("This question will come back another time") and the assembly logic backfills if possible, or the session simply proceeds with 4 questions rather than blocking entirely.
8. A child uses the maximum hint level on every question → mastery-confidence is appropriately discounted for heavily-hinted correct answers (consistent with A.5 FR-18's "hint usage... feeding the mastery-confidence calculation"), but this is invisible to the child — no UI signal makes them feel penalized for using hints.
9. A quiz attempt spans a midnight boundary (started at 11:58pm, finished at 12:03am) → the attempt is attributed to the day it was *started* for daily-quiz-eligibility purposes (a child shouldn't be blocked from "today's" Daily Quiz just because they happened to finish a late-night one slightly past midnight, nor should they be able to get two Daily Quiz instances by timing it this way — the eligibility window logic must handle this gracefully, consistent in spirit with A.7's local_date handling).
10. A parent-facing skill-summary report is requested for a quiz attempt that included questions from multiple distinct skill domains (e.g., a Daily Quiz mixing a Quran question and a Dua question) → the report correctly attributes each question's contribution to its respective skill domain's mastery tracking, never conflating them into one ambiguous combined score.
11. A child completes the main 5-question set with zero incorrect answers → no retry set is offered (there's nothing to retry); the completion flow proceeds directly to the reward/summary screen without an empty or skipped-feeling intermediate step.
12. A quiz session is abandoned mid-way (child closes the app after 2 of 5 questions) → partial progress is not silently lost; on next entry, the child is offered to resume the same session (if still within a reasonable time window) rather than being forced to restart from question 1, consistent with the platform's general resumability philosophy (A.1 FR-16 spirit).

### 1.11 Error Handling

| Scenario | System Behavior |
|---|---|
| Question-set assembly service unavailable | Falls back to a cached/default deterministic question set rather than blocking quiz access entirely |
| Media asset failure (image/audio question) | Graceful skip per Edge Case 7, never a hard quiz-blocking error |
| Quiz attempt submission fails (network) | Local state preserved (offline-first), retried with idempotency key, never re-prompts the child to re-answer already-answered questions |
| Mastery/reward processing failure post-completion | Completion UI still shows (the child's experience isn't blocked), with reward/mastery reconciliation happening asynchronously and retried server-side |
| Withdrawn question encountered mid-session (rare, real-time withdrawal during an active session) | The specific question is excluded from that session's remaining flow if not yet answered; if already answered, the response is still recorded but flagged for mastery/reward exclusion per FR-11 |

### 1.12 Empty States
- Zero quiz history yet (brand-new learner) → first-time quiz framing rather than a stark "no data" report for parents.
- A consuming feature (e.g., Dua Learning) has no qualifying question pool for a specific item → that quiz entry point is simply not offered (consistent with A.6 FR-6, "Recall Quiz... only offered for duas already marked Learned" — absence is expected, not an error state).

### 1.13 Loading States
- Question-set assembly: brief skeleton/loading state, typically near-instant given p95 < 500ms target.
- Per-answer explanation: pre-fetched alongside the question payload, so there is no additional loading state between answer submission and explanation display.

### 1.14 Offline States
- Full offline quiz-taking for downloaded question banks; results queue and sync per FR-10/FR-11.

### 1.15 Permission States
- No new runtime permissions; audio-match questions reuse existing media-playback capability, no microphone involvement (quizzes are answer-selection based, not recitation-recording based — that's A.5's distinct Tajweed/recitation flow).

</details>

## 7. Interactions and navigation

- {"element": "Image option / accessible description", "trigger": "Tap or stated accessible gesture", "precondition": "Correct active child and verified source exercise content available", "behavior": "Select corresponding approved image identifier", "destination": "Current exercise state", "validation": "Correctness uses published content metadata; no invented answers or raw mastery score. Preserve selection when retrying a failed submission.", "back_cancel": "Return to invoking node/mode with saved committed progress; dismiss hint returns to exercise. Never issue duplicate reward.", "unavailable": "Loading media cannot submit a fabricated answer; provide retry or source-defined non-blocking fallback. Parent-disabled recording uses listen-only."}
- {"element": "Submit", "trigger": "Tap or stated accessible gesture", "precondition": "Correct active child and verified source exercise content available", "behavior": "Record answer then Explanation", "destination": "A8-08 Explanation", "validation": "Correctness uses published content metadata; no invented answers or raw mastery score. Preserve selection when retrying a failed submission.", "back_cancel": "Return to invoking node/mode with saved committed progress; dismiss hint returns to exercise. Never issue duplicate reward.", "unavailable": "Loading media cannot submit a fabricated answer; provide retry or source-defined non-blocking fallback. Parent-disabled recording uses listen-only."}
- {"element": "Media failure fallback", "trigger": "Tap or stated accessible gesture", "precondition": "Correct active child and verified source exercise content available", "behavior": "Skip unanswered; backfill if available; progress may show four questions", "destination": "Current exercise state", "validation": "Correctness uses published content metadata; no invented answers or raw mastery score. Preserve selection when retrying a failed submission.", "back_cancel": "Return to invoking node/mode with saved committed progress; dismiss hint returns to exercise. Never issue duplicate reward.", "unavailable": "Loading media cannot submit a fabricated answer; provide retry or source-defined non-blocking fallback. Parent-disabled recording uses listen-only."}

For every action below, use the cited preconditions and source validation. Preserve the invoking route and selected child. Back/cancel dismisses only the current overlay or returns to the invoking screen, preserving drafts and completed progress where specified. Unavailable actions remain visibly labeled with their reason and never activate. Permission prompts occur only after parent consent and a deliberate related action. A prototype simulates outcomes; it never validates identity, grants permissions, charges money or mutates production data.

Verified current-preview controls, retained to prevent omitted clickable elements:

- {"disabled": false, "label": "Leave quiz", "placeholder": null, "tag": "BUTTON", "text": "", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "💡", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "A\n\n112 surahs", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "B\n\n114 surahs", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "C\n\n116 surahs", "type": null}
- {"disabled": false, "label": null, "placeholder": null, "tag": "BUTTON", "text": "D\n\n120 surahs", "type": null}

For any captured control absent from an explicit action above, reconcile it against the screen-specific source below before wiring. Do not connect it to a convenient unrelated screen. Mark it **unresolved, non-executable** until its actual destination/state is confirmed; the navigation appendix reports this limitation. Decorative source-layer names are not automatically click targets.

<details><summary>Screen-specific PRD specification / click behavior</summary>

#### Screen: Quiz Question Screen (generic template across types)

- **Purpose:** Present one question clearly with type-appropriate interaction.
- **Components:** Progress indicator (dots or "Question 2 of 5"), question prompt (text/image/audio depending on type), answer-options area (2-4 multiple-choice cards, drag-to-order tiles for sequence, true/false large dual buttons, tap-to-match grid for image/audio match), Hint control (secondary, always visible), Submit/auto-advance-on-select behavior depending on type.
- **States:** Default, Answer-selected-not-yet-submitted (where applicable), Submitting, Explanation-shown, Media-loading, Media-load-failed-skip.
- **Accessibility:** Sequence/ordering questions must support a non-drag alternative (e.g., numbered-tap-to-place) for accessibility; audio-match questions provide a text-transcript fallback option; image-match questions provide descriptive alt-text per option.
- **Responsive Rules:** Answer-option grids reflow for tablet (more columns) without changing interaction model.



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
3. Create `NH/Enhanced/105/Quiz_Question_Screen_Image_Match/Default` in that area. Do not move the original frames or change their parent containers.
4. Apply existing verified styles/tokens. Proposed new component/token definitions require approval; use local screen dependencies without altering the source/global library.
5. Reuse approved assets. Build Header, Content, Footer and named section containers with auto layout; text hugs height and wraps within fixed available width.
6. Arrange content in the approved vertical hierarchy specified above; retain exact string punctuation, Arabic glyphs, language order and data provenance.
7. Configure viewport safe areas, vertical overflow and fixed footer clearance; test 320/360/390/420 widths and 200% type. Keep individual overlays scrollable when their content is tall.
8. Create only applicable variants: `State=Default|Loading|Error|Offline|Disabled|Selected` as relevant, not a universal empty list of variants. Label scenario frames and parent-context eligibility.
9. Connect each approved section7 trigger with Navigate to, Back, Open overlay, Close overlay or Change to. Preserve return destination and optional conditional branches. Variables/conditionals may simulate selected profile/answer only; production session/security rules remain annotations.
10. Apply section8 transitions; Smart Animate requires matching layer names/hierarchy. Provide a separate ReducedMotion test starting point. No unsupported claim of real network, OTP, mic, biometric or payment execution.
11. Name layers `Header`, `Content/Quiz_Question_Screen_Image_Match`, `Footer`, `Status`, `Control/<exact label>`. Name state frames with screen number and state; log created IDs after execution.
12. Compare screenshots and exact text with all available sources; report source gaps and changes. Do not proceed to the next prompt.

## 10. Acceptance criteria

- [ ] Every required content role/field above is present; exact source strings match character-for-character, including sacred text and punctuation. Conflicting strings have explicit approval.
- [ ] A8 behavior and cited screen entry/exits are preserved; all parent-only controls are gated.
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
