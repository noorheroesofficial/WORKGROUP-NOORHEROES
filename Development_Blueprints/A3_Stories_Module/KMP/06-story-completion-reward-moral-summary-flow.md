# K-06 — Story Completion, Reward Reveal & Moral Summary Flow

## 1. Feature Context
The client-side orchestration of B-04's completion response: a brief non-randomized reward reveal, the Moral Summary Card, an optional post-story quiz, an AI Next Learning suggestion from pre-approved branches only, and badge-unlock handling — all sourced from a single completion API call using K-03's session-scoped `client_event_id`.

## 2. Parent Feature
Feature A.3 — Stories Module (Animated Storytelling System)

## 3. Sub-feature
2.6 Story Completion, Reward Reveal & Moral Summary Flow (ID: **K-06**)

## 4. Objective
Build the post-playback completion flow screens/state driven by a single idempotent call to B-04, rendering reward reveal, moral summary, optional quiz, and next-learning suggestion in sequence, with graceful quiz-service-unavailable handling.

## 5. Business Requirements
- FR-9: award reward → moral summary via Noor companion → optional quiz → AI Next Learning from pre-approved branches only.
- §2.1 Design: reward reveal celebratory but brief (≤2s), never blocking required next action, never randomized/variable-surprise mechanics.
- FR-18: AI Next Learning suggests only from a pre-approved branch set — never open-ended free-text AI suggestion.
- Error Handling: quiz-service unavailable → completion/reward still finalizes independently, quiz step skipped with a "quiz coming back soon" note.

## 6. Existing Architecture
`feature:stories` player sub-package, triggered by K-03's `PlayerState.Completed(reward)` transition. Calls B-04 exactly once per session via the `client_event_id` established in K-03.

## 7. Existing Code to Reuse
- `feature/stories/player/StoryPlayerViewModel.kt` (K-03, extend with completion-flow orchestration)
- `feature/stories/data/CompletionRepository.kt` (new, B-04 client — created here)
- Shared A.8 Daily Quiz engine screen/component (reuse for Post-Story Quiz, do not fork)
- **Resolved (per A.11 K-09, now fully specified):** the badge/achievement unlock modal and the generic reward-reveal animation are shared `core-design-system` components — `RewardUnlockAnimation(xp, noorPoints, activityType)` and `BadgeUnlockModal(badge, onDismiss)` — built and owned by A.11 K-09. This screen consumes both directly; it must **not** create a local `AchievementBadgeUnlockModal.kt`, and the "Reward Reveal" step below is `RewardUnlockAnimation` with `activityType = "story_complete"`, not a bespoke animation.

## 8. Files to Create
- `feature/stories/completion/CompletionRewardRevealScreen.kt` (composes A.11 K-09's `RewardUnlockAnimation` + `MoralSummaryCard`; does not implement its own reward animation)
- `feature/stories/completion/MoralSummaryCard.kt`
- `feature/stories/completion/NextLearningSuggestionCard.kt`
- `feature/stories/data/CompletionRepository.kt` (B-04 client)
- `feature/stories/viewmodel/CompletionFlowViewModel.kt` (+ State/Event files)
- `test/feature/stories/CompletionFlowViewModelTest.kt`
- `androidTest/feature/stories/CompletionRewardRevealScreenTest.kt`

## 9. Files to Modify
- `feature/stories/player/StoryPlayerViewModel.kt` (K-03) — on `PlayerState.Completed`, hand off to `CompletionFlowViewModel` using the same `client_event_id`

## 10. KMP Requirements
- `CompletionFlowViewModel.completeSession(episodeId, finalPositionSeconds, clientEventId, completionMethod)`: calls B-04 exactly once; on retry (e.g., process death recovery), reuses the identical `clientEventId` — never regenerates it, relying on B-04's server-side idempotency for a safe retry.
- Reward Reveal: ≤2s celebratory animation, consistent/predictable presentation (no randomized visual surprise), never blocks the "Continue" action — the child can tap through immediately if they choose.
- Moral Summary Card renders `source: ai|human_fallback` transparently to the flow logic (visually identical to the child regardless of source — the distinction is purely for internal analytics, never surfaced as a UI difference).
- Post-Story Quiz: optional step, delegates entirely to the shared A.8 quiz component; if the quiz service is unavailable, render a "quiz coming back soon" note and proceed directly to Next Learning — reward/completion state is already finalized by this point regardless.
- Next Learning: renders only the pre-approved branch suggestions returned by B-04's response — the UI has no free-text input or open-ended AI suggestion surface at all (architecturally impossible to violate FR-18 from the client side).
- Badge Unlock Modal shown only if `reward.badge_id` is present in the response; dismissing returns to the main completion flow, never blocks progression.

## 11. Required API
**User API** — B-04 `POST /v1/content/{id}/complete` (single call per session, idempotent).

## 12. Offline First
If completion occurs offline, the call queues via the same offline-outbox mechanism established in K-07 (reuse, do not duplicate); the UI proceeds optimistically through reward-reveal/moral-summary using locally-computed provisional values where safe (e.g., XP amount if deterministic and known client-side from content config) and reconciles/corrects on sync if the server response differs — per Edge Case 1's "never abruptly re-lock without explanation" spirit applied here to rewards as well.

## 13. Local Data
Reuses K-07's offline-sync outbox for the completion call when offline.

## 14. Localization
Moral summary text, next-learning suggestion labels, and "quiz coming back soon" copy sourced from shared localization resources / server-supplied locale-resolved text.

## 15. RTL
Moral Summary Card (parchment background, speech-bubble shape), reward reveal, and next-learning card all mirror layout correctly.

## 16. Analytics
Emit `story_completion_threshold_reached`, `story_completed`, `story_reward_awarded`, `story_badge_unlocked`, `moral_summary_shown` (source: ai|human_fallback), `post_story_quiz_started`, `post_story_quiz_completed`, `next_learning_suggested`, `next_learning_accepted`, `episode_unlocked` via `AnalyticsTracker`.

## 17. Performance
Reward-reveal animation must not block input — implement as a non-modal, dismissible-immediately overlay, never a forced-wait screen.

## 18. Security
Next Learning suggestions are rendered strictly from B-04's response data — no client-side generation or free-text surface exists, eliminating any possibility of an unapproved AI suggestion reaching the child from this screen.

## 19. Testing
- Unit: single-call-per-session enforcement (retry reuses `clientEventId`), quiz-unavailable graceful skip, badge-modal-only-when-present logic.
- UI: reward reveal is non-blocking and dismissible immediately, moral summary renders identically regardless of `source` value, Next Learning renders only server-supplied options with zero free-text input anywhere on screen.
- Integration: offline completion queues and reconciles correctly on reconnect.

## 20. AI Coding Agent Implementation Steps

**Task 01 — Implement `CompletionRepository`**
Objective: B-04 client with offline-queue-aware fire semantics. Follow: `core-network`/K-07's offline-outbox pattern. Tests: single-call idempotent-retry test. Definition of Done: test passes.

**Task 02 — Implement `CompletionFlowViewModel`**
Objective: Orchestrates the full sequence (reveal → moral summary → optional quiz → next learning → optional badge modal) from a single B-04 response. Dependencies: Task 01, K-03's `client_event_id`. Tests: sequence-ordering test, single-call enforcement. Definition of Done: tests pass.

**Task 03 — Implement `CompletionRewardRevealScreen`**
Objective: ≤2s non-blocking celebratory animation, consistent presentation (no randomization). Follow: `core-designsystem`. Dependencies: Task 02. Tests: non-blocking-dismissal test. Definition of Done: test passes.

**Task 04 — Implement `MoralSummaryCard`**
Objective: Parchment-style card, Noor companion illustration, calm centered text — visually identical regardless of `source`. Dependencies: Task 02. Tests: source-value-visual-parity test. Definition of Done: test passes.

**Task 05 — Wire Post-Story Quiz Delegation with Graceful Unavailability**
Objective: Delegate to the shared A.8 quiz component; "quiz coming back soon" fallback note on service unavailability. Dependencies: existing A.8 component, Task 02. Tests: quiz-unavailable-skip test confirming reward/completion state is unaffected. Definition of Done: test passes.

**Task 06 — Implement `NextLearningSuggestionCard`**
Objective: Renders only server-supplied pre-approved branch options — no free-text/open-ended input control exists in this Composable at all. Dependencies: Task 02. Tests: static-analysis-style check confirming no `TextField`/free-input component exists in this file. Definition of Done: check passes.

**Task 07 — Wire A.11 K-09's `BadgeUnlockModal` (Reuse Only, No Local Build)**
Objective: Import and invoke `core-design-system`'s `BadgeUnlockModal(badge, onDismiss)` (A.11 K-09) when B-04's response includes an unlocked badge; `onDismiss` returns to this screen's own next step, not to A.11's Achievements screen (that destination only applies when the modal is opened from within the Rewards feature itself). Do Not Change/Do Not Build: no local `AchievementBadgeUnlockModal.kt` file — resolved per §7, no longer an open question. Dependencies: Task 02, A.11 K-09. Tests: shown-only-when-badge-id-present test; test confirming this module contains no locally-defined badge-modal Composable of its own. Definition of Done: both tests pass.

**Task 08 — Wire Hand-off from K-03's `PlayerState.Completed`**
Objective: On completion, transition control to `CompletionFlowViewModel` using the identical session `client_event_id`. Dependencies: K-03, Task 02. Tests: hand-off ID-continuity test. Definition of Done: test passes.

**Task 09 — Add Analytics Instrumentation**
Objective: Nine events per §16. Tests: fake-tracker assertions. Definition of Done: exactly one call site per event.

**Task 10 — Full RTL Pass**
Objective: Verify mirroring across all completion-flow cards. Tests: RTL snapshot tests. Definition of Done: baselines captured.

**Task 11 — Add Full Test Suite**
Objective: Complete coverage per §19. Definition of Done: all green.

**Task 12 — Final Code Review**
Objective: Confirm zero free-text/open-ended AI suggestion surface exists anywhere in this flow, confirm exactly one B-04 call fires per playback session even across process-death/retry scenarios. Definition of Done: checklist in §21 checked.

## 21. Final Verification Checklist
- [ ] Exactly one B-04 completion call fires per session, using the session-scoped `client_event_id`, even across retries
- [ ] Reward reveal is ≤2s, non-blocking, and never uses randomized/variable presentation
- [ ] Moral Summary Card renders identically regardless of `source: ai|human_fallback`
- [ ] Quiz-service unavailability shows a graceful note and never blocks reward/completion (already finalized independently)
- [ ] Next Learning renders exclusively server-supplied pre-approved options — zero free-text/open-ended input exists in this flow
- [ ] Badge Unlock Modal shown only when `reward.badge_id` is present
- [ ] Offline completion queues and reconciles correctly on reconnect
- [ ] All nine analytics events fire correctly

## 22. Definition of Done
The completion flow reliably and idempotently orchestrates reward, moral summary, optional quiz, and safely-bounded next-learning suggestions from a single B-04 call — closing the loop that K-03's player state machine opens on `PlayerState.Completed`.
