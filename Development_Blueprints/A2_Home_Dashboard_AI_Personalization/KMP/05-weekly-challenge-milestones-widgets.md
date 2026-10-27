# K-05 — Weekly Challenge & Milestones Widgets

## 1. Feature Context
NoorHeroes Child App (KMP). Renders "Weekly Challenge & Progress Map" and "Milestones & Reward Summary" sections on Home.

## 2. Parent Feature
A.2 — Child Home Dashboard & AI Personalization

## 3. Sub-feature
2.5 Weekly Challenge & Milestones Widgets (ID: K-05)

## 4. Objective
Build both widgets consuming B-06's challenge/achievement data, with correct empty-state handling (Join Challenge CTA, next-achievable teaser) rather than blank modules.

## 5. Business Requirements
Per PRD §2.2:
- Weekly Challenge: progress map illustration, % complete, days remaining; "Join Challenge" CTA state when zero participation; static description on error (not blank).
- Milestones: badge/achievement mini-cards, "view all" link; teaser of next achievable milestone when zero achievements (not blank).

## 6. Existing Architecture
Plugs into K-01's `SectionState`/`HomeUiState`.

## 7. Existing Code to Reuse
K-01's `SectionState`, shimmer pattern; `:core:design-system` progress-map/badge tokens.

## 8. Files to Create
- `feature/home/src/commonMain/kotlin/.../components/WeeklyChallengeWidget.kt`
- `feature/home/src/commonMain/kotlin/.../components/MilestonesWidget.kt`
- `feature/home/src/commonMain/kotlin/.../models/ChallengeSummary.kt`, `.../models/MilestoneSummary.kt`

## 9. Files to Modify
- `HomeScreen.kt`, `HomeUiState.kt` (K-01)

## 10. Backend Requirements
Consumes `sections.weekly_challenge` and `sections.milestones` from B-01, sourced from B-06; join action calls `POST /v1/challenges/{challenge_id}/join`.

## 11. KMP Requirements
- Weekly Challenge widget: progress map, percent complete, days remaining; if `challenge == null`, render "Join Challenge" CTA state with challenge description instead of a progress bar.
- Milestones widget: recent badge mini-cards + "view all" link to Achievements screen; if zero recent unlocks, render `next_teaser` as a preview card, not a blank module.
- Join action calls the join endpoint and optimistically updates to the joined/in-progress visual.

## 12. NextJS Requirements
Not applicable.

## 13. API Contract
`GET /v1/challenges/weekly` and `GET /v1/children/{id}/achievements` (via B-01 aggregation) per B-06 §13; `POST /v1/challenges/{challenge_id}/join` for the join action.

## 14. Database Requirements
Not applicable directly.

## 15. Validation
Distinguish "no active challenge" (`null` object, valid state → Join CTA or description-only) from "Challenge Service error" (static fallback description, per PRD §2.2 table) — these produce similar-looking UI but different telemetry.

## 16. Authentication
N/A (inherits session).

## 17. Authorization
N/A at UI layer.

## 18. Error Handling
Challenge widget: static fallback description + hidden progress map on error. Milestones widget: hides on error (per PRD §2.2 table "Hides section").

## 19. Offline First
Cached progress/badges shown with "may be outdated" marker if stale, consistent with K-07's offline cache contract.

## 20. Local Data
Reads from `HomeUiState` populated via K-07's cache-or-network repository.

## 21. Localization
Widget labels, challenge title, badge titles via string resources/pre-localized backend strings.

## 22. RTL
Progress map illustration and days-remaining counter mirror correctly; badge mini-card row scrolls in correct RTL direction.

## 23. Analytics
`weekly_challenge_widget_viewed`, `weekly_challenge_joined`, `milestones_widget_viewed`.

## 24. Performance
Progress map illustration should be a lightweight vector/Composable, not a heavy bitmap re-rendered on every recomposition.

## 25. Security
N/A beyond standard scoped-session access.

## 26. Library Requirements
Compose Multiplatform, existing navigation library.

## 27. Testing
- Compose UI: challenge widget renders correctly for null-challenge (Join CTA), joined-in-progress, and error states.
- Compose UI: milestones widget renders correctly for zero-achievements (teaser) and populated states.
- Unit: join action optimistic-update logic.

## 28. Documentation
KDoc distinguishing "no active challenge" (valid empty state) from "service error" (degraded state) for both widgets, since the visual difference is subtle but the underlying `SectionState` and telemetry implications differ.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Define Challenge & Milestone Models**
- Objective: Typed models for both widgets.
- Why Required: Type-safe mapping from B-01/B-06 data.
- Existing Architecture to Follow: K-01 conventions.
- Existing Files to Reuse: `SectionState`.
- Files to Create: `models/ChallengeSummary.kt`, `models/MilestoneSummary.kt`
- Files to Modify: `HomeUiState.kt`
- Implementation Details: `ChallengeSummary(challengeId, title, percentComplete, daysRemaining, joined: Boolean)` nullable-wrapped appropriately; `MilestoneSummary(recent: List<Badge>, nextTeaser: Badge?)`.
- Business Rules: `ChallengeSummary? = null` is a distinct, valid state from `SectionState.Error`.
- Validation: N/A.
- Error Handling: N/A.
- Security: N/A.
- Performance: `@Immutable`.
- Localization: Pre-localized strings.
- RTL: N/A.
- Analytics: N/A.
- Tests: Mapping unit tests distinguishing null-challenge vs. error.
- Documentation: KDoc.
- Dependencies: K-01 Task 01.
- Do Not Change: N/A.
- Expected Result: Models defined.
- Definition of Done: Unit tests pass.

**Task 02 — Build `WeeklyChallengeWidget` with Join Action**
- Objective: Widget UI + join interaction.
- Why Required: Primary UI deliverable.
- Existing Architecture to Follow: `:core:design-system` tokens.
- Existing Files to Reuse: K-01 shimmer.
- Files to Create: `components/WeeklyChallengeWidget.kt`
- Files to Modify: `HomeScreen.kt`
- Implementation Details: Renders progress map when `ChallengeSummary` present and joined; "Join Challenge" CTA + description when present but not joined or null; static description + hidden map on `Error`.
- Business Rules: Join action optimistically flips to in-progress visual, reconciled on server response.
- Validation: N/A.
- Error Handling: Static fallback on error per §18.
- Security: N/A.
- Performance: N/A.
- Localization: String resources.
- RTL: Verified.
- Analytics: `weekly_challenge_widget_viewed`, `weekly_challenge_joined`.
- Tests: Compose UI tests for all three states.
- Documentation: KDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working widget.
- Definition of Done: Tests pass.

**Task 03 — Build `MilestonesWidget` with Teaser Fallback**
- Objective: Widget UI with next-achievable teaser on zero achievements.
- Why Required: Primary UI deliverable.
- Existing Architecture to Follow: `:core:design-system` tokens.
- Existing Files to Reuse: K-01 shimmer.
- Files to Create: `components/MilestonesWidget.kt`
- Files to Modify: `HomeScreen.kt`
- Implementation Details: Renders recent badge mini-cards + "view all" link when `recent` non-empty; renders `nextTeaser` preview card when `recent` empty; hides on `Error`.
- Business Rules: Never renders a truly blank module.
- Validation: N/A.
- Error Handling: Hides on error.
- Security: N/A.
- Performance: N/A.
- Localization: String resources.
- RTL: Verified badge-row direction.
- Analytics: `milestones_widget_viewed`.
- Tests: Compose UI tests for populated/teaser/error states.
- Documentation: KDoc.
- Dependencies: Task 01.
- Do Not Change: N/A.
- Expected Result: Working widget.
- Definition of Done: Tests pass.

## 30. Definition of Done
Both widgets correctly distinguish empty-but-valid states from error states, never render blank modules, and support the challenge-join interaction; all tests green.

## 31. Final Verification Checklist
- [ ] Challenge widget shows Join CTA (not progress bar) when unjoined
- [ ] Challenge widget shows static description (not blank) on service error
- [ ] Milestones widget shows next-achievable teaser (not blank) on zero achievements
- [ ] Milestones widget hides on service error
- [ ] Join action optimistic update reconciles correctly with server response
- [ ] All tests pass
