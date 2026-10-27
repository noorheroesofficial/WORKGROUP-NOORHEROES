# K-10 — Progressive Hint Overlay

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). A cross-cutting overlay component providing progressive, partial hints in any exercise, backed by B-05.

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
K-10 — Progressive Hint Overlay

## 4. Objective
Render a reusable Hint Overlay invoked from any exercise's "Hint" control, displaying server-supplied progressive hint text and never synthesizing reveal content client-side.

## 5. Business Requirements
- FR-18: hints progressive/partial, never revealing the full answer; hint usage tracked, never a visible penalty.
- Edge Case 8: question types without a meaningful partial hint fall back to an explanatory micro-hint.

## 6. Existing Architecture
`feature-learn` module conventions per K-01–K-09. This is a shared, cross-cutting component consumed by K-03, K-05, K-06, K-07, K-08 wherever a hint control appears.

## 7. Existing Code to Reuse
- `LearningApi`/`LearningRepository` extended with B-05's hint-fetch call.
- `core-designsystem`'s existing modal/overlay presentation pattern (confirm if a shared overlay/bottom-sheet primitive already exists in `core-designsystem` before building a new one).

## 8. Files to Create
- `feature-learn/.../hint/HintOverlay.kt` (Composable, reusable across all exercise screens)
- `feature-learn/.../hint/HintOverlayViewModel.kt`
- `feature-learn-domain/.../GetHintUseCase.kt`
- `feature-learn/src/commonTest/kotlin/.../HintOverlayViewModelTest.kt`

## 9. Files to Modify
- `core-network/.../api/LearningApi.kt` — add `getHint(questionId, level)`.
- K-03, K-05, K-06, K-07, K-08's hint-control entry points — wire to launch `HintOverlay`.

## 10. Backend Requirements
Consumes B-05 (`GET /v1/learning/hints/{question_id}?level=1`) exclusively.

## 11. KMP Requirements
- **Progressive levels**: renders `hint_level` 1/2/3 sequentially as the child requests more, each level's text supplied entirely by the server response — the client renders whatever level text is returned and never synthesizes additional reveal content locally.
- **Fallback handling**: if B-05 returns a generic-encouragement fallback (service degraded or no-meaningful-partial-hint question type), render it identically to a normal hint (no special "broken" UI state).
- **Resume**: dismissing the overlay resumes the underlying exercise state exactly where the child left off — no exercise-state loss.
- **Hint control styling**: small, secondary-styled, always visibly present but never pulsing/highlighted in a way that pressures use (per PRD §2.1 UX requirement).
- **`hint_count` tracking**: this overlay itself does not mutate `hint_count` — the invoking exercise screen increments its own local counter and includes it in its own B-03/B-04 attempt submission (consistent with B-05's "read-only, no double-counting" design).

## 12. NextJS Requirements
N/A.

## 13. API Contract
`GET /v1/learning/hints/{question_id}?level=1` per B-05 §13.

## 14. Database Requirements
No local persistence — hints are lightweight, fetched fresh (or short-TTL cached at the network layer if `core-network` provides a generic HTTP cache, not a dedicated local table).

## 15. Validation
N/A client-side beyond standard fetch handling.

## 16. Authentication
Reuses existing child-session auth.

## 17. Authorization
N/A beyond authenticated child session (hints are free-tier accessible per PRD).

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Hint fetch failure | Generic encouragement fallback text rendered identically to a normal hint (per B-05's own graceful-degradation design) |
| Unknown question_id | Should not occur in practice (exercise screens always pass valid IDs); if it does, render the fallback text rather than an error |

## 19. Offline First
Hints require connectivity (lightweight fetch); if offline, show a brief "hints need internet" inline message without blocking the underlying exercise.

## 20. Local Data
N/A.

## 21. Localization
`hint_text` resolved server-side per locale (B-05 delegates to the `localization` context) — client renders as-is.

## 22. RTL
Full RTL layout for the overlay.

## 23. Analytics
`hint_requested` (hint_level) via `AnalyticsTracker`.

## 24. Performance
Lightweight overlay, no special performance concerns.

## 25. Security
No sensitive data.

## 26. Library Requirements
Koin, Ktor, Compose Multiplatform.

## 27. Testing
- Unit: overlay never synthesizes hint text locally — always renders exactly the server-provided string for the requested level.
- Unit: `hint_count` is NOT mutated by this component (verified via a test asserting no write/state-mutation call exists in this ViewModel targeting `hint_count`).
- UI test: dismissing the overlay resumes the exact prior exercise state (no state loss).
- Integration: fallback text renders identically to a normal hint on service failure (no distinct "broken" UI state).

## 28. Documentation
KDoc noting this component is intentionally "dumb" — it renders server text only and must never gain local hint-generation logic in the future.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Extend `LearningApi` with Hint Fetch**
- Task ID: K-10-T01
- Files to Modify: `LearningApi.kt`.
- Dependencies: B-05.
- Definition of Done: Call succeeds against staging.

**Task 02 — Implement `GetHintUseCase`**
- Task ID: K-10-T02
- Dependencies: K-10-T01.
- Definition of Done: Use case unit-tested.

**Task 03 — Implement `HintOverlayViewModel` and `HintOverlay` Composable**
- Task ID: K-10-T03
- Implementation Details: Progressive-level state, fallback handling, resume-on-dismiss behavior.
- Dependencies: K-10-T02.
- Definition of Done: Component renders correctly across levels 1-3 and the fallback case in Compose Preview.

**Task 04 — Wire Hint Controls Across Exercise Screens**
- Task ID: K-10-T04
- Files to Modify: K-03, K-05, K-06, K-07, K-08's hint-control entry points.
- Dependencies: K-10-T03, K-03, K-05, K-06, K-07, K-08.
- Definition of Done: Hint control on each screen correctly launches the overlay and resumes state on dismiss.

**Task 05 — Tests**
- Task ID: K-10-T05
- Dependencies: K-10-T01–T04.
- Definition of Done: All green in CI.

## 30. Definition of Done
Hint Overlay live and reused consistently across all exercise screens, never synthesizes content locally, never mutates `hint_count` itself, resumes exercise state cleanly, fully tested.

## 31. Final Verification Checklist
- [ ] Hint text always exactly server-provided, never client-synthesized
- [ ] `hint_count` mutation happens only in the invoking exercise screen's own attempt submission, never in this component
- [ ] Fallback text renders identically to a normal hint (no distinct broken-state UI)
- [ ] Dismissing the overlay resumes the exact prior exercise state
- [ ] Hint control styled per UX spec (secondary, non-pulsing)
- [ ] Full test suite green in CI
