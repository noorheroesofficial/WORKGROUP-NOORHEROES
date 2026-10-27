# K-06 — Tajweed Learning Flow

## 1. Feature Context
Part of Feature A.5 (Quran & Arabic Learning). Teaches Tajweed rules one at a time: introduction, listen, identification, optional microphone repeat, assessment.

## 2. Parent Feature
A.5 — Quran & Arabic Learning

## 3. Sub-feature
K-06 — Tajweed Learning Flow

## 4. Objective
Render the sequential Tajweed flow (Rule Introduction → Listen → Identification → optional Record → Assessment), routing the optional record step through K-04's shared Recitation Recorder rather than duplicating recording logic.

## 5. Business Requirements
- FR-14: introduce one rule with an approved example → listen at normal/slow speed → identify the rule in an example → optional microphone repeat with visual coaching → short assessment; each step sequential; microphone step skippable/replaced by listen-only per FR-9/FR-13.

## 6. Existing Architecture
`feature-learn` module conventions per K-01–K-05. Reuses `core-kmp-player` for rule-example audio; reuses K-04's `RecitationRecorder`/`RecitationViewModel` in full for the optional record step (no parallel recording implementation).

## 7. Existing Code to Reuse
- `core-kmp-player` for normal/slow-speed audio playback.
- K-04's entire recitation module (recorder, ViewModel, feedback/listen-only screens) — this flow's "optional record" step is a direct reuse, not a reimplementation.
- `LearningApi`/`LearningRepository` (B-03 for identification/assessment attempts).

## 8. Files to Create
- `feature-learn/.../tajweed/RuleIntroductionScreen.kt` + ViewModel
- `feature-learn/.../tajweed/TajweedListenScreen.kt` + ViewModel
- `feature-learn/.../tajweed/RuleIdentificationScreen.kt` + ViewModel
- `feature-learn/.../tajweed/TajweedAssessmentScreen.kt` + ViewModel
- `feature-learn/.../tajweed/TajweedFlowUiState.kt` (shared sequencing state)
- `feature-learn/src/commonTest/kotlin/.../TajweedFlowTest.kt`

## 9. Files to Modify
- `LearnRoute` — add Tajweed flow destinations.

## 10. Backend Requirements
Consumes B-03 for identification/assessment attempts, B-04 (via K-04 reuse) for the optional record step, and the `content` context's Tajweed-rule content endpoint (confirm exact path per Rule 30).

## 11. KMP Requirements
- **Rule Introduction**: renders one rule + approved example.
- **Listen**: normal and slow-speed playback via `core-kmp-player`.
- **Rule Identification Exercise**: submits attempt via B-03.
- **Optional Record step**: directly embeds/routes to K-04's `RecitationRecorderOverlay`/`RecitationViewModel` flow; skippable and replaced by listen-only automatically per the same permission/parent-toggle gating K-04 already implements — no duplicate gating logic here.
- **Assessment**: short assessment closing the flow, submits via B-03.
- **Sequential enforcement**: each step only unlocks after the prior step completes; UI must not allow skipping ahead out of order (though the record step specifically may be skipped/bypassed to listen-only, per FR-14).

## 12. NextJS Requirements
N/A directly.

## 13. API Contract
`POST /v1/learning/attempts` (B-03) for identification/assessment; `POST /v1/learning/recitation` (B-04, via K-04) for the optional record step.

## 14. Database Requirements
No new local persistence; Tajweed content cached via the existing offline-content-download pattern.

## 15. Validation
N/A client-side beyond standard sequencing enforcement.

## 16. Authentication
Reuses existing child-session auth.

## 17. Authorization
Record step inherits K-04's gating (permission + parent toggle) automatically by reuse — no separate authorization logic introduced here.

## 18. Error Handling
| Scenario | Behavior |
|---|---|
| Audio playback failure | Retry/fallback via `core-kmp-player` |
| Attempt submission failure | Non-blocking retry |
| Record step unavailable (gating) | Automatically replaced by listen-only, per K-04's existing behavior |

## 19. Offline First
Rule content/audio downloadable and offline-usable; identification/assessment attempts queue via `SyncQueue` when offline; record step inherits K-04's connectivity-required stance.

## 20. Local Data
Content cached via existing downloadable-content Room schema.

## 21. Localization
Rule text/examples localized via `core-common/localization`.

## 22. RTL
Full RTL layout; Tajweed-rule Arabic-text examples rendered with correct diacritic display (shares typography requirements with K-03).

## 23. Analytics
`tajweed_rule_introduced`, `tajweed_identification_attempted`, `tajweed_assessment_completed` via `AnalyticsTracker`; record-step events are K-04's existing recitation event set (not duplicated here).

## 24. Performance
Standard Compose recomposition hygiene; no special concerns beyond K-03/K-04's established patterns.

## 25. Security
No new sensitive surface — the record step's privacy guarantees are entirely inherited from K-04's reuse.

## 26. Library Requirements
Koin, Ktor, Room (SyncQueue), Compose Multiplatform, `core-kmp-player`. Reuses `core-audio-recording` via K-04, does not redeclare it.

## 27. Testing
- Unit: sequential-step enforcement (cannot skip ahead out of order, except the record step's designed skip-to-listen-only behavior).
- Integration: record step correctly delegates to K-04's existing recorder flow with identical gating behavior (no divergence in permission/toggle logic between K-03's and K-06's record entry points).
- Integration: offline content usable, attempt sync on reconnect.

## 28. Documentation
KDoc noting the record step is a direct reuse of K-04, not a parallel implementation — any future recording-behavior change must be made in K-04 only.

## 29. AI Coding Agent Implementation Steps

**Task 01 — Confirm Tajweed Content API**
- Task ID: K-06-T01
- Objective: Verify the `content` context's Tajweed-rule endpoint shape.
- Dependencies: None (verification task).
- Definition of Done: Endpoint confirmed and documented in §13.

**Task 02 — Build Rule Introduction & Listen Screens**
- Task ID: K-06-T02
- Dependencies: K-06-T01.
- Definition of Done: Screens render correctly, normal/slow playback verified.

**Task 03 — Build Rule Identification Screen**
- Task ID: K-06-T03
- Dependencies: K-06-T01, B-03.
- Definition of Done: Attempt submission verified against staging.

**Task 04 — Embed K-04's Recitation Flow as the Optional Record Step**
- Task ID: K-06-T04
- Implementation Details: Direct composition of K-04's `RecitationRecorderOverlay`/`RecitationViewModel` into the Tajweed flow's navigation graph — no new recording code written.
- Dependencies: K-04, K-06-T03.
- Definition of Done: Record step behaves identically to K-03's/K-07's usage (verified via shared test suite or explicit parity test).

**Task 05 — Build Assessment Screen**
- Task ID: K-06-T05
- Dependencies: K-06-T01, B-03.
- Definition of Done: Assessment attempt submission verified.

**Task 06 — Wire Sequencing & Routes**
- Task ID: K-06-T06
- Files to Modify: `LearnRoute`.
- Dependencies: K-06-T02–T05.
- Definition of Done: Full flow navigable end-to-end in correct sequence.

**Task 07 — Tests**
- Task ID: K-06-T07
- Dependencies: K-06-T01–T06.
- Definition of Done: All green in CI.

## 30. Definition of Done
Tajweed flow live with correct sequential enforcement, optional record step fully delegated to K-04 (zero duplicated recording logic), offline content support, fully tested.

## 31. Final Verification Checklist
- [ ] Steps enforced in correct sequence (Introduction → Listen → Identification → optional Record → Assessment)
- [ ] Record step is a direct reuse of K-04, not a parallel implementation
- [ ] Record step correctly skippable/replaced by listen-only per the same gating as K-03/K-07
- [ ] Offline content usable, attempts sync on reconnect
- [ ] RTL/diacritic rendering verified for Tajweed-rule Arabic examples
- [ ] Full test suite green in CI
